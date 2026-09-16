---
name: tts-voiceover
description: >-
  Chuyển văn bản thành giọng đọc AI (lời dẫn, thuyết minh, đọc bài): có VOICE_PROVIDER → TTS đám
  mây giọng tự nhiên có cảm xúc; không key → edge-tts dự phòng (giọng máy hơn). Xuất mp3/wav/m4a +
  SRT tách câu. Dùng khi người dùng nói "lồng tiếng AI", "TTS", "tạo giọng đọc", "đọc đoạn này
  lên".
layer: produce
---

# Lồng tiếng chuyển văn bản thành giọng nói (TTS Voiceover)

> **Luật cứng khi kiểm tra cấu hình**: `cd` về gốc dự án Easel ghi ở cuối `AGENTS.md` trước, xác nhận thư mục hiện tại có `.env` và `skills/shared/scripts/`. Cấu hình TTS đám mây chỉ được kết luận bằng `model_registry.py configured --group voice --env-file .env` và `voice_clone.py check ... --env-file .env` chạy từ gốc dự án; không chạy `./shared/scripts/...` trong workspace, cũng không dùng `env` / `printenv` để suy ra thiếu Key/URL.

Tổng hợp bài viết / kịch bản thành giọng AI (video nói, lời dẫn, đọc bài). Script dùng chung `skills/shared/scripts/tts.py speak`:
**Mặc định ưu tiên bản closed-source** - đã khai `VOICE_PROVIDER` (+ VOICE_API_KEY) trong `.env` thì đi cloud TTS closed-source (voice_clone,
tổng hợp theo câu + ghép + SRT tách câu, có cảm xúc, giống người thật), **không có key mới lùi về edge** (nghe mùi AI, khô cứng, chỉ để dự phòng).
`--engine closed/edge` để ép chọn; voice closed-source truyền voice-id qua `--voice` (ví dụ `FunAudioLLM/CosyVoice2-0.5B:alex`),
lời dẫn mặc định là alex, có thể ghi đè bằng `VOICE_NARRATOR_VOICE_ID`. Giọng sau khi tổng hợp có thể đưa sang `audio_ops.py`/`video_ops.py` để mix hoặc gắn vào video.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| text / file | Có | Văn bản cần lồng tiếng, hoặc đường dẫn file văn bản (văn bản dài nên dùng --file) |
| voice | Không | Voice, mặc định `zh-CN-XiaoxiaoNeural` (Xiaoxiao) |
| rate/volume/pitch | Không | Tinh chỉnh tốc độ đọc / âm lượng / cao độ |
| output | Không | Mặc định `outputs/<chủ đề>/{name}.mp3` |

## Đầu ra

- File audio lồng tiếng (mp3, tuỳ chọn wav/m4a), đặt vào `outputs/<chủ đề>/`
- Tuỳ chọn xuất kèm phụ đề SRT (`--subtitle`) để burn chữ vào video
- In ra lệnh edge-tts thực chạy + thời lượng/dung lượng/voice của file kết quả

## Yêu cầu trước: proxy ra ngoài

edge-tts gọi dịch vụ trực tuyến của Microsoft, **bắt buộc truy cập được internet**. Trong mạng nội bộ thì đặt proxy trước:

```bash
export https_proxy=http://<proxy-host>:<port> http_proxy=http://<proxy-host>:<port>
```

Script tự đọc biến môi trường proxy và truyền thẳng cho edge-tts (cũng có thể ghi đè bằng `--proxy`).

## Các bước thực thi

Đường dẫn script (tương đối gốc dự án): `skills/shared/scripts/tts.py`. Mỗi subcommand đều hỗ trợ `-h`.

### 0. Chọn voice (tuỳ chọn)

```bash
python skills/shared/scripts/tts.py voices          # Voice tiếng Trung thông dụng + mô tả ngắn
python skills/shared/scripts/tts.py voices --all    # Lấy toàn bộ voice zh- (cần internet)
```

### 1. Tổng hợp giọng đọc speak

```bash
# Đơn giản nhất: một câu → mp3
python skills/shared/scripts/tts.py speak --text "Chào mừng bạn đến với nội dung số này" \
  -o "outputs/<chủ đề>/intro.mp3"

# Văn bản dài đọc từ file + đổi voice + tăng tốc 10%
python skills/shared/scripts/tts.py speak --file script.txt \
  -o "outputs/<chủ đề>/narration.mp3" --voice zh-CN-YunxiNeural --rate +10%

# Xuất kèm phụ đề SRT (để burn chữ vào video)
python skills/shared/scripts/tts.py speak --file script.txt \
  -o "outputs/<chủ đề>/vo.mp3" --subtitle "outputs/<chủ đề>/vo.srt"

# Xuất wav (cần ffmpeg, tiện xử lý không mất chất về sau)
python skills/shared/scripts/tts.py speak --text "..." \
  -o "outputs/<chủ đề>/vo.wav" --format wav
```

Tham số: `--rate +10%` (tốc độ đọc), `--volume +20%` (âm lượng), `--pitch +2Hz` (cao độ).

### 2. Hậu kỳ (tuỳ chọn, tái dùng script dùng chung sẵn có)

Có giọng rồi thì nối tiếp script hạ nguồn theo nhu cầu, không cần dựng lại năng lực trong SKILL này:

```bash
# 1) Lồng tiếng + mix BGM (giọng gốc 1.0 / BGM 0.3) → dùng audio_ops concat / video_ops bgm
python skills/shared/scripts/video_ops.py bgm -i vo.mp3 -o vo_bgm.mp3 \
  --music bgm.mp3 --voice-volume 1.0 --music-volume 0.3

# 2) Chuẩn hoá âm lượng giọng về mức loudness mạng xã hội (-14 LUFS)
python skills/shared/scripts/audio_ops.py normalize vo.mp3 -o vo_norm.mp3

# 3) Gắn giọng đọc làm lời dẫn vào video
python skills/shared/scripts/video_ops.py bgm -i clip.mp4 -o clip_vo.mp4 \
  --music vo.mp3 --voice-volume 0.4 --music-volume 1.0
```

## Voice tiếng Trung thông dụng

| Voice | Đặc điểm |
|------|------|
| `zh-CN-XiaoxiaoNeural` | Xiaoxiao - giọng nữ, ấm áp thân thiện, lựa chọn chung (mặc định) |
| `zh-CN-XiaoyiNeural` | Xiaoyi - giọng nữ, trẻ trung sôi nổi, video nói/seeding |
| `zh-CN-YunxiNeural` | Yunxi - giọng nam, trong trẻo tự nhiên, lời dẫn/thuyết minh |
| `zh-CN-YunyangNeural` | Yunyang - giọng nam, chuyên nghiệp điềm đạm, tin tức/bản tin |
| `zh-CN-YunjianNeural` | Yunjian - giọng nam, trầm dày mạnh mẽ, nội dung nhiệt huyết |

Tiếng Quảng Đông dùng `zh-HK-HiuMaanNeural` (HiuMaan), giọng Đài Loan dùng `zh-TW-HsiaoChenNeural` (HsiaoChen).

## Quy tắc

1. **Tuyệt đối không ghi đè tư liệu gốc** - chỉ ghi file mới vào `outputs/<chủ đề>/`.
2. **Văn bản dài thì dùng --file** - tránh lệnh quá dài / lỗi escape xuống dòng.
3. **Đặt proxy trước** - edge-tts cần internet, lỗi mạng thì script báo rõ.
4. **Không dựng lại năng lực đã có** - mix/chuẩn hoá/gắn lời dẫn vào video thì tái dùng audio_ops.py / video_ops.py.
5. **Không có Profile vẫn chạy được** - không có hồ sơ thì dùng voice mặc định Xiaoxiao.

## Nhận biết Profile

Có Profile thì đọc voice / tốc độ đọc / tone nền tảng mà kênh ưa dùng (ví dụ video nói thiên về Xiaoyi sôi nổi,
nội dung kiến thức thiên về Yunyang điềm đạm) làm tham số mặc định; không có Profile thì lùi về mặc định chung (Xiaoxiao, tốc độ thường).
