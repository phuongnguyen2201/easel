---
name: ai-music
description: >-
  Sinh nhạc nền/BGM gốc (không lời hoặc có hát) cho video ngắn, mạng xã hội qua provider cắm được
  (MUSIC_PROVIDER, tự có key): gửi async → poll → tải, rồi cắt/gắn vào video. Dùng khi người dùng
  nói "tạo nhạc nền", "nhạc AI", "BGM cho video", "sáng tác nhạc". Giọng người → tts-voiceover.
layer: produce
---

# Nhạc AI / Sinh BGM (AI Music)

Sinh **nhạc nền gốc / nhạc phối / nhạc không lời** cho video ngắn, Vlog và nội dung mạng xã hội. Toàn bộ chạy qua script dùng chung
`skills/shared/scripts/ai_music.py` bọc API sinh nhạc (provider cắm được),
gửi bất đồng bộ → poll → tải về. Nhạc tạo ra đưa tiếp cho `audio_ops.py` / `video_ops.py`
để cắt, chuẩn hoá âm lượng hoặc gắn vào video.

**Ranh giới**: SKILL này chỉ làm nhạc nền / nhạc phối. Cần **giọng người nói / lời dẫn / đọc thành tiếng** thì dùng `tts-voiceover`.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| prompt | Có | Mô tả phong cách / cảm xúc / nhạc cụ (ví dụ "lo-fi tươi sáng, piano + trống nhẹ, mở đầu vlog") |
| provider | Không | `dashscope` hoặc `suno-compatible`, cũng có thể dùng env `MUSIC_PROVIDER` |
| lyrics | Không | Lời bài hát (đưa lời vào thì chuyển sang chế độ có hát, không còn là nhạc không lời) |
| duration | Không | Thời lượng (giây), một số provider hỗ trợ |
| instrumental | Không | Nhạc không lời (BGM không có giọng hát) |
| output | Không | Mặc định `outputs/<chủ đề>/{name}.mp3` |

## Đầu ra

- File nhạc (mp3, đặt vào `outputs/<chủ đề>/`)
- In ra provider / model thực sự đã gửi, quá trình poll tác vụ, đường dẫn xuất cuối cùng

## Cấu hình (các biến môi trường cần đặt)

> **Luật sắt về đường dẫn kiểm tra cấu hình**: trước tiên `cd` vào thư mục gốc dự án Easel ghi ở cuối `AGENTS.md`, xác nhận thư mục hiện tại có `.env` và `skills/shared/scripts/`, rồi mới chạy registry, `check` hay lệnh sinh nội dung. Không được đổi sang `./shared/scripts/...` của workspace, cũng không được kết luận là chưa cấu hình chỉ vì `env` / `printenv` không hiện biến.

Đặt trong `.env` ở gốc dự án hoặc trong biến môi trường (script tự dò ngược lên để tìm `.env`). Người dùng tự điền key.

**Dùng chung**

```bash
MUSIC_PROVIDER=dashscope        # hoặc suno-compatible; cũng có thể ghi đè bằng --provider
```

**provider = dashscope** (DashScope / Bailian của Alibaba Cloud)

```bash
DASHSCOPE_API_KEY=...           # bắt buộc (tên khác: DASHSCOPE_KEY / ALIYUN_API_KEY)
DASHSCOPE_MUSIC_MODEL=audio-generation  # tuỳ chọn (tương thích tên cũ DASHSCOPE_MODEL)
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/api/v1   # tuỳ chọn
```

**provider = suno-compatible** (API gateway bên thứ ba kiểu Suno)

```bash
MUSIC_API_KEY=...               # bắt buộc
MUSIC_BASE_URL=https://api.example.com/v1   # bắt buộc, địa chỉ gốc API của bạn
MUSIC_MODEL=music-1             # tuỳ chọn, chỉnh theo tên model của nhà cung cấp
```

## Các bước thực hiện

Chạy trước `python skills/shared/scripts/model_registry.py configured --group music --env-file .env`. Chỉ có một provider khả dụng thì truyền thẳng `--provider`; nhiều provider khả dụng mà người dùng chưa chỉ định thì liệt kê lựa chọn để hỏi, không tự ý chọn theo `MUSIC_PROVIDER`.

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/ai_music.py`. Mỗi lệnh con đều hỗ trợ `-h`.

### 1. Tự kiểm cấu hình bằng check (không gửi request)

```bash
python skills/shared/scripts/ai_music.py check --provider dashscope
```

Thiếu key sẽ liệt kê rõ thiếu env nào (kèm gợi ý tên khác). Cấu hình đủ rồi mới đi tiếp.

### 2. Sinh nhạc bằng generate

```bash
# BGM không lời (dashscope)
python skills/shared/scripts/ai_music.py generate --provider dashscope \
  --prompt "lo-fi hip hop tươi sáng, piano + trống nhẹ, hợp đoạn mở đầu vlog" \
  --duration 30 --instrumental \
  -o outputs/<chủ đề>/vlog-bgm.mp3

# Có hát (suno-compatible, đã đưa lời)
python skills/shared/scripts/ai_music.py generate --provider suno-compatible \
  --prompt "dân ca ấm áp, guitar đệm hát" \
  --lyrics "$(cat lyrics.txt)" \
  -o outputs/<chủ đề>/song.mp3
```

`--poll-interval` (nhịp poll, mặc định 5s), `--timeout` (hết giờ, mặc định 300s) chỉnh theo nhu cầu.

### 3. Hậu kỳ (tuỳ chọn, tái dùng script chung đã có, không dựng lại trong SKILL này)

```bash
# 1) Cắt về đúng độ dài cần cho đoạn mở đầu
python skills/shared/scripts/audio_ops.py trim outputs/<chủ đề>/vlog-bgm.mp3 \
  -o outputs/<chủ đề>/bgm-8s.mp3 --duration 8

# 2) Chuẩn hoá về độ to chuẩn mạng xã hội (-14 LUFS)
python skills/shared/scripts/audio_ops.py normalize outputs/<chủ đề>/vlog-bgm.mp3 \
  -o outputs/<chủ đề>/bgm-norm.mp3

# 3) Gắn BGM vào video (chỉnh được tỉ lệ âm lượng tiếng gốc/BGM, tự lặp và cắt bớt)
python skills/shared/scripts/video_ops.py bgm -i clip.mp4 -o clip_bgm.mp4 \
  --music outputs/<chủ đề>/vlog-bgm.mp3 --voice-volume 1.0 --music-volume 0.3
```

## Quy tắc

1. **check trước, generate sau** - thiếu key thì check báo rõ ràng, không phí một request lỗi.
2. **Tuyệt đối không ghi đè tư liệu gốc** - chỉ ghi file mới vào `outputs/<chủ đề>/`.
3. **Không dựng lại năng lực đã có** - cắt / chuẩn hoá / gắn BGM vào video đều tái dùng `audio_ops.py` / `video_ops.py`.
4. **provider cắm được** - đổi nhà cung cấp chỉ cần đổi `--provider` + env, quy trình SKILL không đổi.
5. **Phân vai với tts-voiceover** - nhạc nền/nhạc phối tìm ai-music, lồng giọng người tìm tts-voiceover.
   Hai bên ghép được: ai-music ra BGM + tts-voiceover ra lời dẫn → `video_ops.py bgm` để trộn.
