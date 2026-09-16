---
name: remove-bg
description: >-
  Tách nền ảnh bằng phân đoạn AI (rembg), không cần phông xanh: xuất PNG trong suốt, thay nền
  trắng/màu hoặc cảnh mới. Dùng khi người dùng nói "tách nền", "xoá phông", "ảnh nền trắng", "thay
  nền", "tách sản phẩm". Video phông xanh → green-screen; phương án ảnh sản phẩm →
  ecom-details-image.
layer: produce
---

# Tách nền ảnh / đổi nền cho ảnh

> Dùng rembg (phân đoạn ngữ nghĩa bằng AI) để tách chủ thể ra, xuất PNG trong suốt hoặc thay nền mới. Không cần phông xanh. Tất cả đi qua
> `skills/shared/scripts/remove_bg.py`.

> Tách phông xanh cho **video** xem **green-screen**; phương án ảnh thương mại điện tử xem **ecom-details-image**;
> phóng to/thu nhỏ, cắt ảnh, đóng dấu thông thường xem **image-editing**.

## Chuẩn bị trước

Lần chạy đầu tự tải model (~4-170MB tuỳ model), cần proxy ra ngoài (script đọc `EASEL_PROXY`/`http(s)_proxy`, không đặt thì nối thẳng). Tự kiểm tra trước:
```bash
python skills/shared/scripts/remove_bg.py check
```

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Ảnh | Có | Ảnh cần tách nền (chưa đưa thì hỏi) |
| Nền đầu ra | Không | Trong suốt (mặc định) / màu đơn sắc / thay bằng ảnh nền |
| Model | Không | Tổng quát / chân dung / tinh xảo, xem bảng dưới |

## Đầu ra (`outputs/<chủ đề>/`)

- Ảnh đã tách nền (nền trong suốt thì dùng `.png`)
- Báo cáo: model đã dùng, dạng nền đầu ra

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/remove_bg.py` (xem tham số bằng `remove -h`).

```bash
# Nền trong suốt (bắt buộc xuất .png)
python skills/shared/scripts/remove_bg.py remove -i product.jpg \
  -o outputs/<chủ đề>/cutout.png

# Ảnh chính nền trắng cho thương mại điện tử
python skills/shared/scripts/remove_bg.py remove -i product.jpg \
  -o outputs/<chủ đề>/white.jpg --bg-color white

# Thay nền bằng cảnh mới
python skills/shared/scripts/remove_bg.py remove -i person.jpg \
  -o outputs/<chủ đề>/scene.png --bg-image scene.jpg

# Chân dung + viền tóc mượt
python skills/shared/scripts/remove_bg.py remove -i portrait.jpg \
  -o outputs/<chủ đề>/cut.png --model u2net_human_seg --alpha-matting
```

## Chọn model

| Model | Phù hợp cho |
|------|------|
| `u2net` (mặc định) | Chủ thể tổng quát |
| `u2netp` | Nhẹ và nhanh (chất lượng thấp hơn chút) |
| `u2net_human_seg` | Chuyên cho ảnh chân dung |
| `isnet-general-use` | Phân đoạn tổng quát tinh hơn |
| `silueta` | Model tổng quát dung lượng nhỏ |

Khi tách chưa sạch hoặc viền còn rối: đổi sang model tinh hơn, hoặc thêm `--alpha-matting` (chậm nhưng viền đẹp hơn, hợp với tóc/lông).

## Quy tắc

1. Muốn nền trong suốt thì **bắt buộc xuất .png** (jpg không hỗ trợ nền trong, script sẽ tự chuyển nền trắng và báo lại).
2. Ảnh chính thương mại điện tử dùng `--bg-color white`; đổi cảnh thì dùng `--bg-image` (tự phủ và cắt theo tỉ lệ).
3. Ảnh chân dung ưu tiên `u2net_human_seg`, sản phẩm/tổng quát thì dùng `u2net`.
4. Chất lượng tách phụ thuộc độ tương phản giữa chủ thể và nền; ảnh phức tạp hoặc tương phản thấp thì không bảo đảm hoàn hảo.
5. Sản phẩm đều đi vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Tách nền dùng rembg (dòng model u2net phát hiện/phân đoạn đối tượng nổi bật) + suy luận CPU bằng onnxruntime, là
phương án phổ biến khi không có GPU. Ghép nền mới dùng Pillow alpha_composite. Việc nạp model, chèn proxy, ghép nền được gói vào script xác định.
