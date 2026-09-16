---
name: multi-voice-dubbing
description: >-
  Lồng tiếng nhiều vai: cast gán giọng từng vai, mỗi dòng thoại có cảm xúc, ra track nhiều giọng +
  phụ đề tên vai. Dùng khi người dùng nói "lồng tiếng hội thoại", "lồng tiếng hai người", "mỗi vai
  một giọng". Một giọng → tts-voiceover; clone giọng → voice-clone; phim ngắn → short-drama.
layer: produce
---

# Lồng tiếng nhiều vai / hội thoại (Multi-voice Dubbing)

Tổng hợp "hội thoại nhiều người / kịch bản nhiều vai" thành **track nhiều giọng** - mỗi vai một giọng khớp persona của vai đó,
không còn kiểu "cả video một giọng". Engine lõi `skills/shared/scripts/multivoice.py`:
gọi `tts.py` (edge-tts, nhiều giọng miễn phí) hoặc `voice_clone.py` (provider cloud giàu biểu cảm / giọng clone) để tổng hợp từng dòng,
đẩy emotion của mỗi dòng vào **kênh cảm xúc thật** của provider, `ffmpeg` nối thành một track + sinh phụ đề người nói khớp thời gian.

> Phần sáng tạo (ai nói gì, cảm xúc gì) do bạn - LLM - tạo ra; ánh xạ giọng nằm trong cast. Phần IO tất định (tổng hợp từng dòng/nối/phụ đề) giao cho engine.
> Sản phẩm `voice.mp3` dùng thẳng làm narration cho `auto-short-video/assemble.py` hoặc ghép vào video bất kỳ; `voice.srt` là phụ đề kèm tên vai.

## Phân tầng chất lượng lồng tiếng (quan trọng: trị bệnh "đọc đều như AI")

**edge-tts không có engine cảm xúc**, chỉ đổi được tốc độ và cao độ, chỉnh cỡ nào cũng vẫn là giọng máy đọc đều. Muốn "giống người thật" bắt buộc dùng **provider cloud** có kênh cảm xúc (người dùng tự lo key, **không cần GPU**):

| Engine (`engine` trong cast) | Chất lượng | Cần gì | Cơ chế cảm xúc |
|---|---|---|---|
| `edge` (mặc định, miễn phí đỡ lưng) | ⚠️ đều đều, máy móc, chỉ để nháp | không cần key, cần mạng ngoài | chỉ chỉnh nhẹ rate/pitch/volume |
| `clone`+`openai-compatible`→**SiliconFlow CosyVoice2** (khuyên dùng) | tốt, tiếng Trung tự nhiên | VOICE_API_KEY (rẻ, tặng credit cho người mới) | lệnh nội tuyến `<\|endofprompt\|>` |
| `clone`+`gemini` | tốt, **miễn phí thật** | GEMINI_API_KEY (bậc miễn phí của Google, ở Trung Quốc cần proxy) | tiền tố ngôn ngữ tự nhiên |
| `clone`+`minimax` / `dashscope` | tốt, có cảm xúc | key của từng nhà | enum emotion / instruct |

**Khuyên dùng SiliconFlow** (CosyVoice2 trên cloud, không cần GPU, ổn nhất với tiếng Trung), cấu hình ghi vào `.env`:
```bash
VOICE_PROVIDER=openai-compatible
VOICE_BASE_URL=https://api.siliconflow.cn/v1
VOICE_API_KEY=<key của bạn>
VOICE_MODEL=FunAudioLLM/CosyVoice2-0.5B
VOICE_INSTRUCT_MODE=inline
```
Vai trong cast: `--engine clone --provider openai-compatible --voice-id FunAudioLLM/CosyVoice2-0.5B:alex` (8 giọng alex/anna/benjamin/...).

- **emotion từng dòng tự dẫn dắt diễn xuất**: `emotion` của mỗi dòng trong `lines.json` (giận dữ/khóc nấc/cười khẩy/dịu dàng...) → engine đổi thành tham số cảm xúc tương ứng theo từng provider. Viết càng cụ thể càng bám vai.
- Muốn "giống người thật" → ít nhất phải cho vai chính/vai then chốt một provider cloud (`engine=clone`); có key mới có cảm xúc, thiếu key thì tự lùi về edge (đều đều) kèm cảnh báo.
- Cấu hình provider xem ở đầu file `voice_clone.py` (env của từng nhà); `voice_clone.py check --provider <tên>` kiểm offline xem key đã đủ chưa.

## Ai sẽ dùng

Thoại phim ngắn (short-drama đã uỷ thác sẵn bên trong), **giảng paper dạng hỏi đáp hai người** (paper-explainer: người giảng + người hỏi),
kịch bản phỏng vấn/podcast, kịch truyền thanh, mọi video nói có "nhiều người nói". Video nói một người cả đoạn thì dùng **tts-voiceover** là đủ.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| cast.json | Có | Bảng chọn vai: mỗi người nói → một giọng (giọng edge + pitch/rate, hoặc giọng clone). Có cả mục "dẫn chuyện/người giảng" |
| lines.json | Có | Thoại từng dòng: mảng có thứ tự `[{speaker, text, emotion}]` (speaker lấy tên trong cast; emotion kiểu lạnh/giận/căng/dịu, tự khớp ngữ điệu) |
| Đường dẫn ra | Không | voice.mp3 (mặc định thoả thuận với bên gọi); voice.srt cùng tên |

## Các bước thực thi

### 1. Chọn vai (cast.json) - đọc hướng dẫn chọn vai để chốt giọng

Đọc `skills/shared/references/voice-casting.md` trước (bảng đối chiếu giọng → nguyên mẫu nhân vật + cách tách giọng cùng giới + dẫn chuyện tách riêng + ngữ điệu cảm xúc).
Chốt cho **mỗi người nói** một giọng hợp giới tính/tuổi/khí chất/thân phận, dẫn chuyện và người giảng đứng riêng, khác mọi vai:

```bash
python skills/shared/scripts/multivoice.py cast init  --cast "<đường dẫn>/cast.json"
python skills/shared/scripts/multivoice.py cast add   --cast "<đường dẫn>/cast.json" \
    --name "Lâm Sách" --role male_lead --voice zh-CN-YunxiNeural --rate=-5% --pitch=-3Hz --note "nam chính lạnh lùng"   # tham số giá trị âm phải dùng dấu bằng
python skills/shared/scripts/multivoice.py cast add   --cast "<đường dẫn>/cast.json" \
    --name "Tô Vãn" --role female_lead --voice zh-CN-XiaoxiaoNeural --note "nữ chính dịu dàng"
python skills/shared/scripts/multivoice.py cast check --cast "<đường dẫn>/cast.json"    # kiểm tra: giọng hợp lệ / dẫn chuyện riêng / không trùng giọng
```
> cast.json cũng có thể viết tay (chỉ là JSON). Muốn một vai **có cảm xúc như người thật** (trị bệnh AI đọc đều) → cho vai đó dùng provider cloud:
> ```bash
> python skills/shared/scripts/multivoice.py cast add --cast "<đường dẫn>/cast.json" \
>     --name "Tổng tài" --role male_lead --engine clone --provider minimax --voice-id <id giọng của bạn> --note "giọng clone/giàu biểu cảm"
> ```
> Phải cấu hình key của provider tương ứng trong `.env` (`voice_clone.py check --provider minimax`); thiếu key thì vai đó **tự lùi về edge** (đều đều) kèm cảnh báo.

### 2. Thoại từng dòng (lines.json)

Tách kịch bản / bản thoại thành từng dòng có thứ tự:
```json
{"lines":[
  {"speaker":"người giảng","text":"Paper này giải quyết một vấn đề then chốt.","emotion":"bình"},
  {"speaker":"người hỏi","text":"Khoan đã, vì sao các phương pháp hiện có không dùng được?","emotion":"ngạc nhiên"},
  {"speaker":"người giảng","text":"Vì chúng bỏ qua phụ thuộc theo thời gian.","emotion":"chắc nịch"}
]}
```
speaker phải trùng tên trong cast (lệch thì lùi về giọng dẫn chuyện kèm cảnh báo); emotion là tuỳ chọn.

### 3. Tổng hợp track nhiều giọng + phụ đề

```bash
python skills/shared/scripts/multivoice.py dub \
    --cast "<đường dẫn>/cast.json" --lines "<đường dẫn>/lines.json" -o "<đường dẫn>/voice.mp3"
```
Ra `voice.mp3` (mỗi vai một giọng riêng, cảm xúc tự chỉnh ngữ điệu) + `voice.srt` (kèm tên vai, thời gian bám đúng độ dài đo được của từng dòng).
`dub` sẽ in ra **đã dùng mấy giọng** - kiểm cho chắc là ≥2 giọng (hội thoại nhiều người không thể chỉ có một giọng).

### 4. Đưa vào video

- `voice.mp3` làm narration + `voice.srt` làm phụ đề, đưa vào `auto-short-video/scripts/assemble.py` (ghép ảnh/video).
- Hoặc trộn với BGM (**audio-mix**), ghép vào video có sẵn (**video-editing**).

## Hạ cấp

- Mất mạng ngoài / edge-tts không thông → không tổng hợp được, phải nói thật (nhiều giọng phụ thuộc edge-tts).
- cast chỉ định giọng clone nhưng thiếu key hoặc lỗi → vai đó **tự lùi về giọng edge miễn phí** kèm cảnh báo, không chặn.
- Người nói không có trong cast → lùi về giọng dẫn chuyện kèm cảnh báo (nên bổ sung vào cast).

## Nhận biết Profile

- **Có Profile**: `style.md` hoà vào việc chọn khí chất giọng (khí chất vai → giọng); `preferences.md` lọc lằn ranh đỏ trong thoại.
- **Không có Profile**: chọn giọng theo bảng đối chiếu mặc định trong voice-casting.md.

## Quy tắc

1. **Hội thoại nhiều người bắt buộc nhiều giọng**: mỗi người nói một giọng riêng, dẫn chuyện/người giảng đứng riêng - tuyệt đối không để cả video một giọng (`cast check` + số giọng của `dub` gác cửa).
2. **Muốn giống người thì lên provider cloud**: edge chỉ hợp bản nháp; thành phẩm và vai then chốt dùng `engine=clone`+provider (có kênh cảm xúc thật), không cần GPU.
3. **Giọng phải hợp nhân vật**: theo bảng nguyên mẫu trong voice-casting.md + dùng pitch/rate để tách các vai cùng giới.
4. **Gắn nhãn cảm xúc cho cụ thể**: mỗi dòng lines đều ghi emotion (giận dữ/khóc nấc/cười khẩy/dịu dàng...), sẽ được đẩy vào kênh cảm xúc của provider để dẫn dắt diễn xuất.
5. **Lưu lại phần tất định**: cast.json / lines.json ghi ra file, sửa thoại hay đổi giọng chỉ cần chạy lại `dub`, không phải làm lại từ đầu.

## Nguồn tham khảo

Xem `EASEL-META.md`. Lồng tiếng nhiều giọng (cast + lines từng dòng + tổng hợp từng dòng theo giọng của vai + ffmpeg nối + phụ đề người nói) là do Easel tự làm;
bên dưới bọc edge-tts (tts.py) và clone trên cloud (voice_clone.py).
