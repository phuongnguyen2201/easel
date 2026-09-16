---
name: meme-generator
description: >-
  Làm meme/ảnh chế: chữ lớn trắng viền đen trên/dưới kiểu kinh điển, hoặc dải chữ kiểu ảnh phản
  ứng ("khi mà..."); tự xuống dòng, cỡ chữ (Pillow). Dùng khi người dùng nói "làm meme", "ảnh
  chế", "thêm chữ vào ảnh", "ảnh phản ứng". Thẻ trích dẫn tinh tế → card-quote; watermark →
  image-editing.
layer: produce
---

# Meme / Ảnh chế

> Thêm chữ meme vào ảnh. Hai kiểu bố cục: chữ lớn trên/dưới đè lên ảnh kiểu kinh điển, hoặc thêm dải màu đặc kèm chữ (kiểu ảnh phản ứng).
> Chạy qua `skills/shared/scripts/meme_ops.py`, **đừng tự tính cỡ chữ/ngắt dòng** - script đã tự chỉnh cỡ chữ,
> tự ngắt dòng cho cả tiếng Việt lẫn tiếng Anh, chữ trắng viền đen.

> Thẻ câu đắt tinh tế xem **card-quote**; thẻ kiến thức ảnh-chữ xem **card-xiaohongshu**; thêm watermark xem **image-editing**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Ảnh nền | Có | Ảnh nền meme/ảnh chụp màn hình/ảnh phản ứng (chưa có thì hỏi) |
| Chữ | Có | Chữ trên/dưới (overlay) hoặc chữ trong dải (bar) |
| Bố cục | Không | `overlay` đè chữ trên/dưới (mặc định) / `top-bar` dải chữ trên / `bottom-bar` dải chữ dưới |

## Đầu ra (`outputs/<chủ đề>/`)

- Ảnh meme (jpg/png)

## Các bước thực hiện

Đường dẫn script (so với gốc dự án): `skills/shared/scripts/meme_ops.py` (`make -h` để xem tham số).

```bash
# Chữ lớn trên/dưới kiểu kinh điển (chữ trắng viền đen đè lên ảnh)
python skills/shared/scripts/meme_ops.py make -i cat.jpg \
  -o "outputs/<chủ đề>/out.jpg" --top "Sếp bảo" --bottom "Yêu cầu này đơn giản mà"

# Ảnh phản ứng: dải chữ phía trên (kiểu "khi mà...")
python skills/shared/scripts/meme_ops.py make -i react.jpg \
  -o "outputs/<chủ đề>/out.jpg" --layout top-bar \
  --caption "Khi sáng thứ Hai mở máy lên thấy cả đống tin nhắn"

# Dải đen chữ trắng ở dưới
python skills/shared/scripts/meme_ops.py make -i img.jpg -o out.png \
  --layout bottom-bar --caption "Cuộc sống mà" --bar-color black --text-color white
```

## Chọn bố cục thế nào

| Bố cục | Hiệu ứng | Dùng cho |
|------|------|------|
| `overlay` (mặc định) | Chữ trắng viền đen đè lên ảnh, trên/dưới | Meme kinh điển (top/bottom text) |
| `top-bar` | Thêm dải trắng chữ đen phía trên ảnh | Ảnh phản ứng, "khi mà..." |
| `bottom-bar` | Thêm dải chữ phía dưới ảnh | Cà khịa, chốt ý |

- Tiếng Anh mặc định chuyển in hoa (cho "chất meme" hơn), tắt bằng `--no-upper`.
- Độ dày viền chữ `--stroke` (overlay, mặc định tự chỉnh theo cỡ chữ).

## Quy tắc

1. Chữ phải cô đọng - meme sống nhờ câu ngắn, đừng viết cả đoạn dài.
2. Cỡ chữ/ngắt dòng để script tự chỉnh, đừng nhồi chữ quá dài (script sẽ tự thu nhỏ nhưng dài quá vẫn xấu).
3. overlay dùng --top/--bottom; bố cục bar dùng --caption.
4. Cần nền trong suốt hoặc chồng nhiều lớp thì xuất `.png`, đăng ảnh thường thì dùng `.jpg`.
5. Sản phẩm để hết vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Meme kinh điển (font Impact, chữ trắng viền đen xếp trên/dưới) và ảnh phản ứng có dải chữ là những định dạng lan truyền mạnh trên mạng xã hội. Dùng Pillow để
tự chỉnh cỡ chữ, ngắt dòng khi trộn nhiều ngôn ngữ và vẽ viền, cho kết quả ổn định, lặp lại được.
