---
name: voice-clone
description: >-
  Tải mẫu giọng của chính người dùng để nhân bản giọng riêng qua provider đám mây (người dùng tự
  có key), rồi tổng hợp lời dẫn, thuyết minh, giọng bán hàng bằng giọng đó. Dùng khi người dùng
  nói "clone giọng", "nhân bản giọng tôi", "lồng tiếng bằng giọng tôi". Giọng có sẵn →
  tts-voiceover.
layer: produce
---

# Lồng tiếng bằng giọng nhân bản

> Dùng mẫu giọng của chính bạn để nhân bản chất giọng, rồi tổng hợp bất kỳ nội dung nào. Đi qua provider đám mây (người dùng tự có key), máy ở nhà không cần GPU.
> Tất cả đều đi qua `skills/shared/scripts/voice_clone.py`.

> Không muốn nhân bản, chỉ dùng giọng công cộng có sẵn thì xem **tts-voiceover** (edge-tts, miễn phí không cần key);
> nhạc/BGM do AI sinh thì xem **ai-music**; trộn giọng đã tổng hợp với BGM thì xem **audio-mix**.

## Chuẩn bị: cấu hình API key

> **Luật sắt về đường dẫn khi kiểm cấu hình**: trước hết `cd` vào thư mục gốc dự án Easel ghi ở cuối `AGENTS.md`, xác nhận thư mục hiện tại có `.env` và `skills/shared/scripts/`, rồi mới chạy registry, `check`, `enroll` hay `clone`. Không được đổi sang `./shared/scripts/...` của workspace, cũng không được lấy cớ `env` / `printenv` không hiện biến để kết luận thiếu `VOICE_BASE_URL`/key. Khi `check` hỗ trợ thì truyền rõ `--env-file .env`.

Chọn provider và điền key vào `.env`, rồi `check` để kiểm offline:
```bash
python skills/shared/scripts/voice_clone.py check --provider minimax --env-file .env
```

| provider | Dịch vụ | Cần điền trong .env |
|----------|------|----------|
| `dashscope` | Alibaba CosyVoice, nhân bản giọng | `DASHSCOPE_API_KEY` (tuỳ chọn `DASHSCOPE_TTS_MODEL`/`DASHSCOPE_BASE_URL`) |
| `minimax` | MiniMax nhân bản giọng nói | `MINIMAX_API_KEY`, `MINIMAX_GROUP_ID` (tuỳ chọn `MINIMAX_MODEL`) |
| `fish-audio` | Fish Audio | `FISH_API_KEY` (tuỳ chọn `FISH_BASE_URL`) |
| `openai-compatible` | Tương thích OpenAI /audio/speech | `VOICE_API_KEY`, `VOICE_BASE_URL` (voice dựng sẵn, không phải nhân bản zero-shot) |
| `gemini` | Google Gemini TTS | `GEMINI_API_KEY` (tuỳ chọn `GEMINI_TTS_MODEL`/`GEMINI_VOICE`/`GEMINI_BASE_URL`) |

> ⚠️ Mỗi provider được cài theo tài liệu API công khai, endpoint/tên model có thể ghi đè bằng env để khớp tham số thực tế.

Trước khi chạy hãy chạy `model_registry.py configured --group voice --env-file .env`. Chỉ có một cái khả dụng thì chọn rõ cái đó; nhiều cái khả dụng mà người dùng không nêu tên thì liệt kê provider/model rồi hỏi lần này dùng cái nào, không tự ý chọn theo `VOICE_PROVIDER`.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Mẫu giọng | Bắt buộc khi nhân bản | Giọng của chính bạn, rõ và không ồn (thường 10s-1min, cụ thể xem yêu cầu của provider) |
| Nội dung | Bắt buộc khi tổng hợp | Phần chữ muốn đọc ra bằng giọng đã nhân bản |

## Đầu ra (`outputs/<chủ đề>/`)

- File âm thanh giọng đã tổng hợp (mp3/wav)

## Các bước thực hiện

Đường dẫn script (tương đối so với gốc dự án): `skills/shared/scripts/voice_clone.py` (mỗi subcommand đều hỗ trợ `-h`).

### 1. Đăng ký chất giọng (enroll, lấy voice_id)
```bash
# minimax: tải file mẫu lên
python skills/shared/scripts/voice_clone.py enroll --provider minimax \
  --sample me.mp3 --name my_voice
# dashscope: dùng URL mẫu truy cập được từ Internet công cộng
python skills/shared/scripts/voice_clone.py enroll --provider dashscope \
  --sample-url https://.../me.wav --name myv
```
(fish-audio dùng model_id sẵn có hoặc audio tham chiếu nội tuyến, openai-compatible dùng tên voice dựng sẵn, không cần enroll.)

### 2. Tổng hợp (clone)
```bash
python skills/shared/scripts/voice_clone.py clone --provider minimax \
  --voice-id my_voice --text "Chào cả nhà, chào mừng tới kênh của mình" --speed 1.0 \
  -o "outputs/<chủ đề>/vo.mp3"
```
fish-audio cũng có thể đưa thẳng audio tham chiếu: `--sample ref.mp3 --sample-text "phần chữ của audio tham chiếu"`.

## Lằn ranh đỏ về tuân thủ (bắt buộc giữ)

1. **Chỉ được nhân bản giọng mà bạn có quyền dùng** (chính bạn, hoặc người đã cho phép rõ ràng).
2. **Không được nhân bản giọng người khác/người nổi tiếng để gây hiểu nhầm, lừa đảo, mạo danh, nguỵ tạo**.
3. Nội dung tổng hợp không được dùng cho thông tin sai lệch hoặc mục đích xâm phạm quyền.
   - Vượt lằn ranh thì không làm, và nói rõ lý do với người dùng.

## Quy tắc

1. Chất lượng mẫu quyết định kết quả nhân bản: rõ tiếng, không ồn nền, ngữ điệu tự nhiên, đủ dài.
2. `check` xác nhận key trước, rồi enroll, rồi clone.
3. Giọng đã tổng hợp có thể nối **audio-mix** để thêm BGM, nối **auto-subtitle** để ra phụ đề, nối vào video.
4. Sản phẩm thống nhất đưa vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Các dịch vụ nhân bản giọng trên đám mây phổ biến: Alibaba CosyVoice (nhân bản giọng), MiniMax (nhân bản giọng nói + T2A), Fish Audio,
TTS tương thích OpenAI. Nhân bản zero-shot chạy tại máy (GPT-SoVITS/CosyVoice bản local) cần GPU, nên đi qua provider đám mây.
