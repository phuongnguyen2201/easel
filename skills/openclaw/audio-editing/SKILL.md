---
name: audio-editing
description: >-
  Xử lý âm thanh chung: cắt, đổi định dạng mp3/wav/m4a/aac, chuẩn hoá âm lượng, tách audio từ
  video, nối đoạn, fade in/out, đổi tốc độ giữ cao độ. Dùng khi người dùng nói "cắt audio",
  "chuyển sang mp3", "chỉnh âm lượng", "tách tiếng từ video", "tăng tốc audio". Khử ồn →
  audio-denoise.
layer: produce
---

# Xử lý âm thanh chung

Các thao tác âm thanh chung ngoài khử ồn: cắt, đổi định dạng, chuẩn hoá âm lượng, tách audio, nối đoạn, fade in/out, đổi tốc độ. Tất cả đi qua script dùng chung `skills/shared/scripts/audio_ops.py` bọc ffmpeg, tham số xác định, tái lập được, không ghép lệnh thủ công tại chỗ.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| input_file | Có | Đường dẫn file âm thanh hoặc video |
| operation | Có | trim / convert / normalize / extract / concat / fade / speed / denoise / info |
| output_file | Không | Mặc định `outputs/<chủ đề>/{name}-{op}.{ext}` |

Định dạng hỗ trợ: wav / mp3 / m4a / aac / flac; container video mp4 / mkv / mov (tách audio).

## Đầu ra

- File âm thanh sau xử lý (đặt vào `outputs/<chủ đề>/`)
- Mỗi thao tác in ra lệnh ffmpeg thực chạy + thời lượng/bitrate/số kênh/sample rate của file xuất

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/audio_ops.py`. Mọi lệnh con đều hỗ trợ `-h`.

### 0. Kiểm tra môi trường + thăm dò file

```bash
python skills/shared/scripts/audio_ops.py info input.mp3
```

Script tự kiểm tra ffmpeg/ffprobe, thiếu thì hiện hướng dẫn cài. Chạy `info` xem thời lượng/bitrate/số kênh trước rồi mới động tay.

### 1. Cắt trim

```bash
# Thời điểm bắt đầu và kết thúc
python skills/shared/scripts/audio_ops.py trim in.mp3 -o outputs/<chủ đề>/clip.mp3 --start 00:00:05 --end 00:00:20
# Điểm bắt đầu + thời lượng
python skills/shared/scripts/audio_ops.py trim in.mp3 -o clip.mp3 --start 5 --duration 15
```

### 2. Đổi định dạng convert

```bash
python skills/shared/scripts/audio_ops.py convert in.wav -o out.mp3 --bitrate 192k
python skills/shared/scripts/audio_ops.py convert in.m4a -o out.wav --sample-rate 44100 --channels 2
```

Định dạng xuất do phần mở rộng quyết định (mp3/wav/m4a/aac).

### 3. Chuẩn hoá âm lượng normalize

```bash
python skills/shared/scripts/audio_ops.py normalize in.mp3 -o out.mp3
```

Mặc định loudnorm về -14 LUFS / -1.5 dBTP (mức loudness chung cho mạng xã hội/podcast). Ghi đè bằng `--i --tp --lra`.

### 4. Tách audio extract

```bash
python skills/shared/scripts/audio_ops.py extract video.mp4 -o audio.m4a
python skills/shared/scripts/audio_ops.py extract video.mp4 -o audio.aac --copy   # Không encode lại, nhanh nhất
```

### 5. Nối đoạn concat

```bash
python skills/shared/scripts/audio_ops.py concat a.mp3 b.mp3 c.mp3 -o all.mp3
```

Nối theo đúng thứ tự tham số; cách encode lại tương thích với nhiều sample rate/container khác nhau.

### 6. Fade in/out fade

```bash
python skills/shared/scripts/audio_ops.py fade in.mp3 -o out.mp3 --fade-in 2 --fade-out 3
```

`--fade-out` tự canh về N giây trước điểm kết thúc.

### 7. Đổi tốc độ speed (giữ cao độ)

```bash
python skills/shared/scripts/audio_ops.py speed in.mp3 -o out.mp3 --factor 1.5   # Nhanh gấp 1.5
python skills/shared/scripts/audio_ops.py speed in.mp3 -o out.mp3 --factor 0.8   # Chậm lại
```

Dựa trên atempo để giữ cao độ; vượt khoảng 0.5-2.0 thì tự nối tầng.

### 8. Khử ồn denoise (dự phòng, cần chuyên sâu thì dùng audio-denoise)

```bash
python skills/shared/scripts/audio_ops.py denoise in.wav -o out.wav --tier 2
```

## Ranh giới với audio-denoise

- **audio-denoise**: SKILL chuyên khử ồn, lo trọn quy trình chọn mức, tải model, báo cáo khử ồn - cần khử ồn nghiêm túc thì dùng nó.
- **audio-editing**: xử lý âm thanh chung. Lệnh con `denoise` chỉ là phương án tiện tay, cả hai gọi cùng một `audio_ops.py denoise`, năng lực như nhau, định vị khác nhau.

## Quy tắc

1. **Tuyệt đối không xoá file gốc** - chỉ ghi file mới vào `outputs/<chủ đề>/`.
2. **Chạy info trước rồi mới xử lý** - xem thông tin file để tránh thao tác nhầm.
3. **Đầu vào là video thì chỉ động vào audio** - denoise với video sẽ tự `-c:v copy`; chỉ muốn rút tiếng thì dùng extract.
4. **Thực thi minh bạch** - script sẽ in ra lệnh ffmpeg thực chạy.
5. **Không có Profile vẫn dùng được** - xử lý âm thanh không phụ thuộc hồ sơ (Profile) kênh.

## Nhận biết Profile

Có Profile thì chọn tham số mặc định theo thiên hướng nền tảng (loudness cho video ngắn, bitrate mục tiêu); không có Profile thì lùi về mặc định chung (-14 LUFS, 192k).
