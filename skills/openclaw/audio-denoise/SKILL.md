---
name: audio-denoise
description: >-
  Khử ồn bản ghi: lọc tiếng nền, rè điện, gió, ù bằng chuỗi filter ffmpeg
  (afftdn/highpass/lowpass), 3 mức từ cơ bản tới RNN, kèm báo cáo trước–sau. Dùng khi người dùng
  nói "khử ồn", "lọc tạp âm", "bản ghi bị rè", "có tiếng gió". audio-editing làm thao tác chung,
  skill này chuyên khử ồn.
layer: produce
---

# Khử ồn âm thanh

Dọn tiếng ồn nền trong bản ghi. SKILL chuyên trách khử ồn - gói các filter khử ồn của ffmpeg qua script dùng chung `skills/shared/scripts/audio_ops.py denoise`, đưa ra ba mức (từ lọc cơ bản tới mạng nơ-ron RNN), tham số cố định, tái lập được, không ghép lệnh tại chỗ.

> Thao tác âm thanh chung (cắt/chuyển mã/âm lượng/tách/nối/fade in-out/đổi tốc độ) xem **audio-editing**. SKILL này chỉ lo khử ồn.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| input_file | Có | Đường dẫn file âm thanh hoặc video |
| tier | Không | `1` / `2` / `3` (mặc định `2`) |
| output_file | Không | Mặc định `outputs/<chủ đề>/{filename}-clean.{ext}` |
| mix | Không | Cường độ khử ồn 0.0-1.0 (mặc định 0.8, chỉ dùng cho tier3 RNNoise) |
| preserve_original | Không | Giữ lại file gốc (mặc định true) |

Định dạng hỗ trợ: wav, mp3, flac, aac, m4a, mp4, mkv, mov.

## Đầu ra

- File âm thanh đã khử ồn (đặt vào `outputs/<chủ đề>/`)
- Báo cáo xử lý: thông tin file gốc, tier và chuỗi filter đã dùng, thông tin file đầu ra, so sánh dung lượng

## Ba mức khử ồn (ứng với `--tier` của script)

Script tự chọn chuỗi filter theo tier và in ra lệnh ffmpeg thực sự chạy.

### Tier 1 - Khử ồn cơ bản (bộ lọc sẵn có của ffmpeg)

Cắt tiếng ù tần số thấp, tiếng xì tần số cao + khử ồn FFT, thuần ffmpeg, không phụ thuộc bên ngoài.
Filter: `highpass=f=80,lowpass=f=8000,afftdn=nr=12:nf=-40:tn=1`
Phù hợp: nhiễu nhẹ, cần xử lý nhanh mà không cần model.

### Tier 2 - Khử ồn tăng cường (FFT mạnh hơn + trung bình phi cục bộ)

Khử ồn FFT quyết liệt hơn, chồng thêm anlmdn, vẫn thuần ffmpeg.
Filter: `highpass=f=70,afftdn=nr=24:nf=-30:tn=1,anlmdn=s=0.0005`
Phù hợp: nhiễu trung bình, tiếng nền ổn định (điều hoà/quạt/nhiễu nền). **Mức mặc định**.

### Tier 3 - Khử ồn bằng mạng nơ-ron RNN (arnndn + hậu xử lý)

RNNoise tối ưu cho giọng người + tiền xử lý highpass + nén động + chuẩn hoá độ lớn.
Filter: `highpass=f=60,arnndn=m=<model>:mix=<mix>,acompressor=...,loudnorm=...`
Phù hợp: bản ghi giọng nói, podcast, phỏng vấn, môi trường nhiễu phức tạp.
**Cần model RNNoise `sh.rnnn`; thiếu thì script tự hạ xuống Tier2 và in hướng dẫn tải.**

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/audio_ops.py`.

### 1. Dò file đầu vào

```bash
python skills/shared/scripts/audio_ops.py info input_file
```

Script tự kiểm tra ffmpeg/ffprobe, thiếu thì báo cách cài. Cho người dùng xem thời lượng/bitrate/số kênh, xác định là audio hay video.

### 2. Chuẩn bị model RNN (chỉ Tier3)

Kiểm tra xem `skills/shared/scripts/models/sh.rnnn` cạnh script đã có chưa. Chưa có thì tải:

```bash
mkdir -p skills/shared/scripts/models
curl -L https://github.com/GregorR/rnnoise-models/raw/master/somnolent-hogwash-2018-09-01/sh.rnnn \
  -o skills/shared/scripts/models/sh.rnnn
```

Không tải cũng được - script sẽ tự hạ xuống Tier2. Cũng có thể dùng `--model <path>` để chỉ model khác.

### 3. Chạy khử ồn

```bash
# Tier2 mặc định
python skills/shared/scripts/audio_ops.py denoise input.wav -o outputs/<chủ đề>/input-clean.wav --tier 2
# Tier3 (RNNoise, giọng người)
python skills/shared/scripts/audio_ops.py denoise input.wav -o outputs/<chủ đề>/input-clean.wav --tier 3 --mix 0.8
```

- Script sẽ in lệnh ffmpeg thực sự chạy (thực thi minh bạch).
- **Đầu vào là video thì tự thêm `-c:v copy`**: chỉ xử lý luồng tiếng, luồng hình giữ nguyên.

### 4. Kiểm tra đầu ra + báo cáo

Xử lý xong script tự in thời lượng/bitrate/số kênh/tần số lấy mẫu của file đầu ra. Cần so sánh đầy đủ thì:

```bash
python skills/shared/scripts/audio_ops.py info outputs/<chủ đề>/input-clean.wav
```

Nội dung báo cáo: gốc vs đầu ra (định dạng/thời lượng/dung lượng/tần số lấy mẫu), tier và chuỗi filter đã dùng, thay đổi dung lượng.

## Quy tắc

1. **Tuyệt đối không xoá file gốc** - kể cả khi người dùng không nêu `preserve_original`.
2. **Dò trước, xử lý sau** - luôn chạy `info` xem thông tin file trước đã.
3. **Đầu vào video thì chỉ động vào tiếng** - script tự thêm `-c:v copy`.
4. **Thực thi minh bạch** - script in ra lệnh ffmpeg thực tế.
5. **Khi khử ồn quá tay** - nên hạ tier hoặc `--mix` (ví dụ 0.8 xuống 0.5).
6. **Không phụ thuộc Profile** - xử lý âm thanh không cần hồ sơ tài khoản.

## Tham khảo khi tự phát triển

- Tài liệu filter afftdn/arnndn/anlmdn của FFmpeg
- [xiph/rnnoise](https://github.com/xiph/rnnoise) - triệt nhiễu bằng RNN
- [GregorR/rnnoise-models](https://github.com/GregorR/rnnoise-models) - model huấn luyện sẵn
- [timsainb/noisereduce](https://github.com/timsainb/noisereduce) - spectral gating bằng Python (phương án thay thế)
