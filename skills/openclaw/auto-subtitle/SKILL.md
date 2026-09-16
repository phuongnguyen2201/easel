---
name: auto-subtitle
description: >-
  Nhận dạng giọng nói trong audio/video thành file phụ đề (SRT/ASS/TXT/JSON), tuỳ chọn đốt phụ đề
  vào video. Dùng khi người dùng nói "phụ đề tự động", "bóc băng video", "gắn phụ đề", "đốt phụ
  đề". Dịch phụ đề có sẵn → subtitle-translate; cắt clip dài kèm đốt phụ đề → clipify.
layer: produce
---

# Phụ đề tự động (nhận dạng giọng nói thành phụ đề)

Nhận dạng giọng người trong audio/video thành phụ đề. Dựa trên script dùng chung `skills/shared/scripts/asr.py` (bọc faster-whisper),
tham số cố định, tái lập được, ngắt dòng theo dấu câu cho dễ đọc. Tuỳ chọn đốt phụ đề vào video (dùng lại `skills/shared/scripts/video_ops.py` / bộ lọc subtitles của ffmpeg).

> Chỉ làm "giọng nói → file phụ đề (+ tuỳ chọn đốt vào video)". Dựng video nói chung xem **video-editing**; chỉ khử tiếng ồn xem **audio-denoise**; cắt clip thông minh từ video dài kèm đốt phụ đề xem **clipify**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| input_file | Có | Đường dẫn file audio hoặc video (video tự tách âm thanh) |
| format | Không | `srt` (mặc định) / `ass` / `txt` / `json` |
| language | Không | `auto` (mặc định) hoặc mã ISO 639-1 như `vi`/`en` |
| model | Không | `tiny`/`base` (mặc định)/`small`/`medium`/`large-v3`, càng lớn càng chính xác và càng chậm |
| burn | Không | Có đốt phụ đề vào video hay không (cần đầu vào là video) |

Hỗ trợ: audio mp3/wav/m4a/aac/flac...; video mp4/mkv/mov/webm...

## Đầu ra

- File phụ đề ghi vào `outputs/<chủ đề>/` (SRT/ASS/TXT/JSON)
- Nếu đốt phụ đề: video có phụ đề cứng (`*-sub.mp4`)
- Báo cáo: ngôn ngữ nhận dạng, số dòng phụ đề, model đã dùng, đường dẫn đầu ra

## Chuẩn bị trước

- Lần chạy đầu sẽ tải model từ HuggingFace, **cần proxy ra mạng ngoài**. Script đọc biến môi trường `EASEL_PROXY` hoặc `http(s)_proxy` làm proxy;
  không đặt biến nào thì kết nối thẳng. Cũng có thể `export https_proxy=... http_proxy=...` trước để chỉ định.
- Môi trường CPU dùng mặc định `--device cpu --compute-type int8` là đủ.

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/asr.py`, `skills/shared/scripts/video_ops.py`.

### 1. Tạo file phụ đề

```bash
# Video → SRT (tự tách âm thanh + tự nhận diện ngôn ngữ)
python skills/shared/scripts/asr.py transcribe \
  -i input.mp4 -o "outputs/<chủ đề>/input.srt" --language vi

# Video → ASS (có style, **cỡ chữ/lề tự thích ứng theo video ngang hay dọc**): đầu vào video tự dò chiều rộng và chiều cao
python skills/shared/scripts/asr.py transcribe \
  -i input.mp4 -o "outputs/<chủ đề>/input.ass" --format ass --model small
# Audio thuần → ASS: không dò được kích thước, mặc định khung dọc 1080x1920; khung ngang thêm --res 1920x1080
python skills/shared/scripts/asr.py transcribe \
  -i voice.mp3 -o "outputs/<chủ đề>/voice.ass" --format ass --res 1920x1080
```

- **Style ASS tự thích ứng theo kích thước video đích**: cỡ chữ tính theo **cạnh ngắn** (min(w,h)*0.05, dọc/ngang đều xấp xỉ vừa, không còn quá to khi nằm ngang),
  lề dưới tính theo chiều cao, lề trái phải tính theo chiều rộng, `PlayRes` = kích thước thật. Đầu vào video tự dò; audio thuần dùng `--res <rộng>x<cao>` để chỉ định.
  **Muốn phụ đề cứng có style thì ưu tiên đốt file ASS này** (mục dưới), đỡ việc hơn SRT trần + tự điền force_style, lại tự thích ứng.
- Mặc định mỗi dòng ~18 chữ, quá dài thì tự xuống dòng/tách dòng phụ đề; chỉnh bằng `--max-line-chars`.
- Không truyền `-o` thì script lấy tên file đầu vào làm tên thư mục dự án, ví dụ `talk.mp4` xuất ra `outputs/talk/talk.srt`; dự án đã có sẵn thì nên ghi rõ `-o "outputs/<chủ đề>/<tên file>.<format>"`.
- Xem model/ngôn ngữ khả dụng: `python skills/shared/scripts/asr.py info`.

### 2. (Tuỳ chọn) Đốt phụ đề vào video

Khi người dùng muốn "phụ đề cứng/đốt vào video", dùng bộ lọc `subtitles` (SRT) hoặc `ass` (ASS) của ffmpeg:

```bash
# Đốt SRT (tuỳ biến được style)
ffmpeg -y -i input.mp4 \
  -vf "subtitles=outputs/<chủ đề>/input.srt:force_style='FontName=Noto Sans CJK SC,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=2'" \
  -c:a copy "outputs/<chủ đề>/input-sub.mp4"

# Đốt ASS (style đã nằm sẵn trong file ass, giữ nguyên bản)
ffmpeg -y -i input.mp4 \
  -vf "ass=outputs/<chủ đề>/input.ass" \
  -c:a copy "outputs/<chủ đề>/input-sub.mp4"
```

- Khi đường dẫn có ký tự đặc biệt, bọc giá trị của `subtitles=` bằng nháy đơn và escape dấu hai chấm.
- Cần phụ đề mềm (tắt được) thay vì đốt cứng: `ffmpeg -i in.mp4 -i sub.srt -c copy -c:s mov_text out.mp4`.

### 3. Sản phẩm và báo cáo

- File phụ đề và video đã đốt phụ đề đều ghi vào `outputs/<chủ đề>/`.
- Báo cho người dùng: ngôn ngữ nhận dạng, số dòng phụ đề, model, đường dẫn file; gợi ý có thể đổi `--model`/`--max-line-chars` rồi chạy lại.

## Quy tắc

1. **Video phải tách âm thanh trước** - script tự dùng ffmpeg tách wav 16kHz mono, không đụng vào video gốc.
2. **Ngắt câu dễ đọc** - ngắt dòng theo dấu câu/độ dài, tránh một dòng quá dài.
3. **Tuyệt đối không xoá file gốc** - chỉ tạo file mới vào `outputs/`.
4. **Chọn model** - cần nhanh dùng `base`, cần chính xác dùng `small`/`medium`; CPU dùng int8.
5. **Đốt phụ đề cần đầu vào là video** - audio thuần không đốt được, chỉ xuất file phụ đề.
6. **Không phụ thuộc Profile** - bóc băng không cần hồ sơ (Profile) kênh.

## Nguồn tham khảo

- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) - suy luận Whisper tăng tốc bằng CTranslate2
- [openai/whisper](https://github.com/openai/whisper) - model Whisper gốc và phương pháp ASR
- Bộ lọc `subtitles` / `ass` của FFmpeg (đốt phụ đề)
