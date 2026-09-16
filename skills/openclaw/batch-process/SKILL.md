---
name: batch-process
description: >-
  Áp một thao tác cho cả thư mục ảnh/video/audio: nén, watermark, đổi định dạng, scale, đổi tỉ lệ,
  chuẩn hoá âm lượng. Dùng khi người dùng nói "xử lý hàng loạt", "nén cả thư mục", "watermark cả
  loạt", "chuyển hết sang dọc". image-editing/video-editing/audio-editing xử lý một file.
layer: general
---

# Xử lý hàng loạt (theo thư mục)

> Áp cùng một thao tác cho toàn bộ ảnh/video/audio trong một thư mục. Chạy qua `skills/shared/scripts/batch_process.py`,
> uỷ thác lần lượt cho script xác định tương ứng (image_ops / video_ops / audio_ops).

> Xử lý một file xem image-editing / video-editing / audio-editing; SKILL này là **bản chạy hàng loạt theo thư mục** của chúng.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Thư mục | Có | Thư mục chứa file cần xử lý |
| Loại | Có | `image` / `video` / `audio` (quyết định dùng script ops nào + cách lọc file) |
| Thao tác | Có | Subcommand của ops (như resize/compress/watermark/aspect/convert/normalize) |
| Tham số thao tác | Tuỳ thao tác | Viết sau `--`, truyền nguyên xi sang script ops |

## Đầu ra (mặc định `<thư mục>/batch_out/`)

- File sau xử lý giữ nguyên tên; báo số file thành công/thất bại.

## Thực thi

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/batch_process.py` (`run -h` / `list -h`).

```bash
# Xem trước sẽ xử lý những file nào
python skills/shared/scripts/batch_process.py list --dir imgs --type image

# Nén hàng loạt ảnh xuống 500KB
python skills/shared/scripts/batch_process.py run --dir imgs --type image --op compress \
  --out-dir out -- --max-kb 500

# Gắn watermark hàng loạt
python skills/shared/scripts/batch_process.py run --dir imgs --type image --op watermark \
  -- --text "@kênh của tôi" --position bottom-right

# Chuyển hàng loạt video sang dọc 9:16
python skills/shared/scripts/batch_process.py run --dir clips --type video --op aspect \
  --out-dir out -- --ratio 9:16 --mode pad

# Chuyển hàng loạt audio sang mp3 (đổi phần mở rộng bằng --ext)
python skills/shared/scripts/batch_process.py run --dir raw --type audio --op convert \
  --out-dir out --ext .mp3 -- --bitrate 192k
```

## Thao tác khả dụng (truyền sang script ops, xem tham số bằng `<script> <op> -h`)

- **image** (image_ops): resize / crop / pad / convert / compress / watermark / round / thumbnail
- **video** (video_ops): compress / aspect / watermark / speed / gif / frame
- **audio** (audio_ops): convert / normalize / denoise / fade / speed / trim

## Quy tắc

1. Chạy `list` xem trước phạm vi file, chắc chắn đúng rồi mới `run`.
2. Tham số sau `--` truyền nguyên xi sang script ops; chưa chắc tham số thì chạy bản một file (image-editing...) kiểm chứng một lần.
3. Đổi định dạng đầu ra bằng `--ext` (như `.mp3`/`.png`), nếu không sẽ giữ phần mở rộng gốc.
4. Xử lý hàng loạt chạy tuần tự (tránh quá tải); số lượng lớn thì chờ, file lỗi được liệt kê riêng chứ không làm dừng cả lượt.
5. Mặc định xuất ra `<thư mục>/batch_out/`, không ghi đè file gốc.

## Nguồn tham khảo

Tái dùng script xác định sẵn có của dự án (image_ops/video_ops/audio_ops), SKILL này chỉ duyệt thư mục + uỷ thác từng
file + tổng hợp kết quả, không cài lại logic xử lý.
