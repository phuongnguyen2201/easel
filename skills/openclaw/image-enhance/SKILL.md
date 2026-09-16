---
name: image-enhance
description: >-
  Nâng chất ảnh mờ/tối/nhiễu: phóng to 2x/4x, khử nhiễu, làm nét, tự động tương phản/bão hoà. Dùng
  khi người dùng nói "ảnh bị mờ", "làm nét ảnh", "phóng to không vỡ", "chỉnh sáng ảnh". Không phải
  AI siêu phân giải: vẽ thêm chi tiết → ai-image-gen; resize/cắt/watermark → image-editing.
layer: produce
---

# Nâng chất ảnh / phóng to

> Phóng to chất lượng cao + khử nhiễu + làm nét + chỉnh màu, cứu ảnh mờ/tối/nhiều nhiễu. Chạy qua
> `skills/shared/scripts/img_enhance.py`.

> ⚠️ **Xử lý xác định kiểu truyền thống, không phải AI siêu phân giải** - cải thiện được mờ/nhiễu nhẹ tới vừa, nhưng không tạo chi tiết từ hư không.
> Cần AI siêu phân giải/vẽ lại thì dùng **ai-image-gen** (image-to-image). Resize/cắt/nén/watermark thông thường xem **image-editing**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Ảnh | Có | Ảnh cần nâng chất (chưa đưa thì hỏi) |
| Hệ số phóng to | Không | Mặc định 2x; đặt 1 là chỉ nâng chất, không phóng to |
| Hạng mục nâng chất | Không | Một nút `--auto`, hoặc chỉ định riêng khử nhiễu/làm nét/tương phản/bão hoà |

## Đầu ra (`outputs/<chủ đề>/`)

- Ảnh sau khi nâng chất
- Báo cáo: kích thước gốc → kích thước mới, đã chạy những xử lý nào

## Các bước thực thi

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/img_enhance.py` (`enhance -h` để xem tham số).

```bash
# Nâng chất một nút + phóng to 2x (hay dùng nhất)
python skills/shared/scripts/img_enhance.py enhance -i blurry.jpg \
  -o "outputs/<chủ đề>/out.jpg" --scale 2 --auto

# Ảnh nhiều nhiễu: khử nhiễu + 4x + làm nét mạnh
python skills/shared/scripts/img_enhance.py enhance -i photo.jpg \
  -o "outputs/<chủ đề>/out.png" --scale 4 --denoise --sharpen 1.5

# Chỉ chỉnh màu, không phóng to (ảnh tối/bị xám)
python skills/shared/scripts/img_enhance.py enhance -i img.jpg \
  -o "outputs/<chủ đề>/out.jpg" --scale 1 --auto
```

## Tinh chỉnh tham số

- **Vẫn mờ**: công cụ này không tạo được chi tiết, chuyển sang ai-image-gen (image-to-image) để siêu phân giải.
- **Làm nét quá tay, bị nhiễu/viền trắng**: hạ `--sharpen` (mặc định auto=1.0).
- **Màu quá bão hoà**: `--saturation 1.0` để tắt tăng màu, hoặc hạ thấp hơn.
- **Nhiễu bị phóng to theo**: thêm `--denoise` (khử nhiễu trước khi phóng to).

## Quy tắc

1. Chốt kỳ vọng trước: đây là "cải thiện" chứ không phải "vẽ lại", ảnh mờ nặng thì đừng hứa thành nét căng.
2. Có nhiễu thì bắt buộc `--denoise` (chạy trước khi phóng to, tránh nhiễu bị phóng to theo).
3. Phóng to thống nhất dùng resample Lanczos chất lượng cao; đừng mù quáng bật 4x (file phình to mà không thêm chi tiết).
4. Sản phẩm đều đi vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Resample Lanczos + làm nét UnsharpMask + khử nhiễu OpenCV fastNlMeans + tự động tương phản là bộ nâng chất ảnh truyền thống
không cần GPU. Siêu phân giải thật sự (Real-ESRGAN...) cần GPU/model, ở đây thay bằng ai-image-gen image-to-image.
