---
name: image-editing
description: >-
  Gia công ảnh có sẵn: resize, cắt, pad theo tỉ lệ nền tảng, đổi định dạng png/jpg/webp, nén về
  dung lượng đích, watermark, bo góc, ghép nhiều ảnh. Dùng khi người dùng nói "đổi kích thước",
  "nén ảnh", "gắn watermark", "đúng kích thước Facebook/TikTok". Thiết kế và render ảnh mới →
  card-*.
layer: produce
---

# Gia công ảnh

> Xử lý xác định trên **ảnh đã có**: resize/cắt/pad/đổi định dạng/nén/watermark/bo góc/ghép/thumbnail.
> Mọi thao tác đều chạy qua `skills/shared/scripts/image_ops.py` (thuần Pillow), không tự chế script.

## Đầu vào

- Một hoặc nhiều đường dẫn file ảnh đã tồn tại (png/jpg/webp... các định dạng Pillow hỗ trợ)
- Thao tác đích và tham số (kích thước, tỉ lệ, chất lượng, chữ watermark, kiểu ghép...)

## Đầu ra

- File ảnh sau xử lý (đường dẫn do người dùng chỉ định, mặc định ghi vào `outputs/<chủ đề>/`)
- Mỗi lệnh in lại `✅ đường dẫn (rộng x cao, dung lượng KB)`; `info` trả ra json

## Ranh giới (tách bạch với card-*)

- card-quote / card-xiaohongshu / poster-hero / comparison-card = **thiết kế và render ảnh mới** (HTML -> chụp màn hình)
- image-editing = **gia công ảnh có sẵn**, không làm thiết kế thị giác, không sinh nội dung, chỉ xử lý mức pixel
- Cần "sinh ảnh từ dữ liệu/chữ" -> dùng chart/infographic/card-*; SKILL này chỉ xử lý file ảnh có sẵn

## Các bước thực thi

1. Xác nhận ảnh đầu vào tồn tại, chốt rõ thao tác đích và tham số
2. Chạy subcommand tương ứng của `image_ops.py` từ **thư mục gốc dự án** (xem bên dưới)
3. Khi cần kích thước theo nền tảng, tra `references/platform-sizes.md` để lấy tỉ lệ/pixel gợi ý
4. Báo lại đường dẫn và kích thước đầu ra; nhiều thao tác có thể nối chuỗi (ví dụ resize trước rồi compress)

## Tra cứu lệnh nhanh

Đường dẫn script thống nhất là `skills/shared/scripts/image_ops.py`, tất cả đều hỗ trợ `-h` để xem tham số.

```bash
# Resize: theo rộng/cao/phần trăm, --keep-ratio giữ tỉ lệ trong khung, không kéo méo
python skills/shared/scripts/image_ops.py resize -i in.jpg -o out.jpg --width 1080
python skills/shared/scripts/image_ops.py resize -i in.jpg -o out.jpg --percent 50
python skills/shared/scripts/image_ops.py resize -i in.jpg -o out.jpg --width 1080 --height 1440 --keep-ratio

# Cắt: cắt theo toạ độ hoặc cắt giữa về đúng kích thước chỉ định
python skills/shared/scripts/image_ops.py crop -i in.jpg -o out.jpg --box 100,50,900,650
python skills/shared/scripts/image_ops.py crop -i in.jpg -o out.jpg --width 1080 --height 1080

# Pad về tỉ lệ đích (lõi của việc khớp mạng xã hội): pad ảnh bất kỳ thành 1:1 / 9:16 / 16:9
python skills/shared/scripts/image_ops.py pad -i in.jpg -o out.png --ratio 9:16 --background "#ffffff"
python skills/shared/scripts/image_ops.py pad -i in.jpg -o out.png --ratio 1:1 --background "20,20,30"

# Đổi định dạng png/jpg/webp
python skills/shared/scripts/image_ops.py convert -i in.png -o out.webp --format webp --quality 85

# Nén: cố định chất lượng hoặc ép sát trần dung lượng file (jpg/webp)
python skills/shared/scripts/image_ops.py compress -i in.jpg -o out.jpg --quality 80
python skills/shared/scripts/image_ops.py compress -i in.jpg -o out.jpg --max-kb 200

# Watermark: chữ (vị trí/độ mờ/cỡ chữ/màu, tự tìm font hệ thống) hoặc ảnh (góc dưới bên phải...)
python skills/shared/scripts/image_ops.py watermark -i in.jpg -o out.png --text "@tên kênh" --position bottom-right --opacity 0.5 --size 40
python skills/shared/scripts/image_ops.py watermark -i in.jpg -o out.png --image logo.png --position bottom-right --scale 0.3 --opacity 0.8

# Bo góc (xuất png nền trong suốt); --radius-percent 50 cho ra hình tròn
python skills/shared/scripts/image_ops.py round -i in.jpg -o out.png --radius 60
python skills/shared/scripts/image_ops.py round -i avatar.jpg -o out.png --radius-percent 50

# Ghép nhiều ảnh: ngang/dọc/lưới NxM (cột x hàng), --cell-width/height cho ô đồng đều
python skills/shared/scripts/image_ops.py collage -i a.jpg b.jpg c.jpg -o out.jpg --mode horizontal --gap 12
python skills/shared/scripts/image_ops.py collage -i 1.jpg 2.jpg 3.jpg 4.jpg -o out.jpg --grid 2x2 --gap 10 --cell-width 540 --cell-height 540

# Thumbnail (pixel của cạnh dài nhất)
python skills/shared/scripts/image_ops.py thumbnail -i in.jpg -o thumb.jpg --size 256

# Đọc thông tin ảnh (json: kích thước/định dạng/tỉ lệ/dung lượng/kênh trong suốt)
python skills/shared/scripts/image_ops.py info -i in.jpg
```

## Kiến thức chuyên môn: kích thước gợi ý theo nền tảng

Gợi ý cho các nền tảng thông dụng xem `references/platform-sizes.md`. Ghi nhớ nhanh:

- Xiaohongshu ảnh dọc kèm chữ: **1080×1440** (3:4); video/poster dọc Xiaohongshu: **1080×1920** (9:16)
- Ảnh đơn WeChat Moments / ảnh vuông dùng chung: **1:1** (ví dụ 1080×1080)
- Câu đắt/ảnh bìa nằm ngang: **16:9** (ví dụ 1920×1080); ảnh đầu bài WeChat OA 900×383
- Ảnh kèm bài Weibo: **1:1 hoặc 4:3**; ảnh bìa Douyin/Video Channels: **9:16 (1080×1920)**

Hướng khớp kích thước: ưu tiên `pad` (thêm viền, không cắt nội dung, không méo) để giữ trọn khung hình; muốn tràn viền thì `crop` cắt giữa về tỉ lệ đích;
chỉ cần giảm dung lượng thì dùng `resize`/`compress`.

## Nhận biết Profile

- Có Profile: chữ watermark mặc định lấy tên kênh/handle; tỉ lệ đầu ra mặc định bám nền tảng chính của kênh (ví dụ kênh Xiaohongshu mặc định 1080×1440)
- Không có Profile: chạy theo tham số người dùng nêu rõ, tỉ lệ mặc định giữ như ảnh gốc, watermark cần người dùng cấp chữ

## Phụ thuộc và xử lý lỗi

- Phụ thuộc: Pillow (đã cài sẵn, `python -c "import PIL"` chạy được), còn lại thuần thư viện chuẩn, không thêm bên thứ ba
- Script có sẵn kiểm tra biên: file không tồn tại / khung cắt vượt biên / tỉ lệ hoặc màu không hợp lệ -> mã thoát 2 và in `ERROR:`
- Không tìm thấy font hệ thống thì hạ xuống font mặc định của PIL kèm `WARN`, có thể dùng `--font` để chỉ định
- Tự kiểm tra: `python skills/shared/scripts/image_ops.py --selftest`
