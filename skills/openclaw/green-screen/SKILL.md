---
name: green-screen
description: >-
  Tách nhân vật quay trên phông xanh/xanh dương, ghép vào nền mới: ảnh, video, màu đơn hay chính
  tiền cảnh làm mờ. Dùng khi người dùng nói "tách phông xanh", "đổi nền video", "xoá phông xanh",
  "chromakey". video-reframe chỉ đổi khung; ai-image-gen sinh ảnh mới, skill này xử lý phông xanh
  đã quay.
layer: produce
---

# Tách phông xanh / ghép nền mới

> Tách tiền cảnh trên phông xanh rồi ghép vào nền mới. Tất cả đi qua `skills/shared/scripts/chromakey.py`,
> **đừng tự ghép tay filter chromakey/overlay** - script đã lo phần tách nền, khử tràn màu (despill), hoà viền,
> co giãn nền, giữ âm thanh.

> Chỉ đổi khung hình xem **video-reframe**; sinh hình từ đầu bằng AI xem **ai-video-gen**; dựng phim phổ thông xem **video-editing**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Video tiền cảnh | Có | Tư liệu quay trên phông xanh lá/xanh dương (không đưa thì hỏi) |
| Nền | Có | Chọn một trong bốn: ảnh / video / màu đơn / chính tiền cảnh làm mờ |
| Màu phông | Không | Mặc định xanh lá `0x00ff00`; phông xanh dương dùng `0x0000ff` |

## Đầu ra (`outputs/<chủ đề>/`)

- Video sau khi ghép (`*-composited.mp4`)
- Báo cáo: độ phân giải, màu đã tách bỏ, nền đã dùng

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/chromakey.py` (`key -h` để xem tham số).

```bash
# Ghép vào nền là ảnh
python skills/shared/scripts/chromakey.py key -i "<video phông xanh>" \
  --bg "<ảnh nền>" -o "outputs/<chủ đề>/<tên>-composited.mp4"

# Ghép vào nền là video (nền tự lặp cho đủ thời lượng)
python skills/shared/scripts/chromakey.py key -i "<video phông xanh>" \
  --bg "<video nền>" -o "outputs/<chủ đề>/<tên>.mp4"

# Ghép vào nền màu đơn
python skills/shared/scripts/chromakey.py key -i "<video phông xanh>" \
  --bg-color white -o "outputs/<chủ đề>/<tên>.mp4"

# Nền = chính tiền cảnh phóng to làm mờ (tạo cảm giác xoá phông)
python skills/shared/scripts/chromakey.py key -i "<video phông xanh>" \
  --bg-blur -o "outputs/<chủ đề>/<tên>.mp4"
```

## Chỉnh tham số (khi tách chưa sạch)

- **Còn viền xanh / tách không sạch**: tăng `--similarity` (mặc định 0.30, có thể lên 0.4).
- **Viền nhân vật bị ăn mất / thủng lỗ**: giảm `--similarity`, hoặc tăng `--blend` (mặc định 0.10) để làm mềm viền.
- **Nhân vật ám xanh (tràn màu)**: script đã tự chạy `despill`; vẫn rõ thì do phông đánh sáng không đều, là lỗi tư liệu.
- **Phông xanh dương**: `--color 0x0000ff`.

## Quy tắc

1. Màu phông mặc định là xanh lá; phông xanh dương/màu khác thì chỉ định bằng `--color`.
2. Nền chọn một trong bốn (`--bg` / `--bg-color` / `--bg-blur`), loại trừ nhau.
3. Nền tự co giãn và cắt theo khung tiền cảnh, nền video tự lặp cho đủ thời lượng tiền cảnh.
4. Âm thanh của tiền cảnh được giữ tự động.
5. Chất lượng tách phụ thuộc tư liệu (phông sạch màu tới đâu, ánh sáng đều tới đâu); script cố hết sức, nhưng quay tệ thì không cứu được.
6. Sản phẩm đều vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Tách phông xanh dùng ffmpeg `chromakey` (sinh alpha theo khoảng cách màu) + `despill` (chặn tràn màu ở viền nhân vật) +
`overlay` để ghép, là phương án tách nền chuẩn không cần GPU. Ngưỡng màu, hoà viền, thích ứng nền được đóng gói thành script tất định.
