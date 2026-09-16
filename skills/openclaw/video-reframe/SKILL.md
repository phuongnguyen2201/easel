---
name: video-reframe
description: >-
  Đổi khung hình video thông minh (9:16/16:9/1:1): nền mờ lấp không viền đen, cắt theo tiêu điểm
  hoặc cắt giữ mặt ở giữa. Dùng khi người dùng nói "chuyển ngang sang dọc", "đổi sang 9:16", "bỏ
  viền đen", "cắt giữ mặt". Cắt khung đơn giản → video-editing; cắt clip bám mặt động → clipify.
layer: produce
---

# Đổi khung hình video thông minh (dọc ngang qua lại)

> Đưa video về tỉ lệ khung hình đích, có ba chiến lược để chọn. Tất cả chạy qua `skills/shared/scripts/reframe.py`,
> **đừng tự ghép filter crop/overlay bằng tay** - script đã tính sẵn kích thước cắt, biên tiêu điểm, căn số chẵn, giữ audio.

| Chế độ | Hiệu quả | Dùng khi |
|------|------|------|
| `blur` (mặc định) | Giữ nguyên khung gốc căn giữa + phóng to làm mờ chính nó làm nền, **không viền đen** | Hay dùng nhất khi chuyển ngang sang dọc, không mất nội dung |
| `crop` | Cắt theo vị trí tiêu điểm về tỉ lệ đích, **không viền đen nhưng mất rìa** | Chủ thể rõ ràng, muốn phủ kín màn hình |
| `smart` | cv2 phát hiện khuôn mặt → lấy vị trí trung vị của mặt làm tiêu điểm để cắt | Video nói/video có người, chuyển ngang sang dọc |

> Cần bám mặt động theo từng cảnh để pan thì xem **clipify**; chỉ muốn thêm viền đen/cắt giữa thì xem **video-editing** `aspect`.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| File video | Có | Video cần chuyển (chưa đưa thì hỏi) |
| Tỉ lệ đích | Có | `9:16` / `16:9` / `1:1` / `4:5` / `3:4` / `4:3` / `21:9` |
| Chế độ | Không | `blur` (mặc định) / `crop` / `smart` |
| Tiêu điểm | Không | Ở chế độ crop, khi chủ thể không nằm giữa thì dùng `--focus-x` (0 trái 1 phải) |

## Đầu ra (`outputs/<chủ đề>/`)

- Video sau khi chuyển (`*-<tỉ lệ>.mp4`)
- Báo cáo: kích thước nguồn → đích, tỉ lệ, chiến lược đã dùng, tiêu điểm khuôn mặt (khi dùng smart)

## Các bước thực hiện

Đường dẫn script (tương đối gốc dự án): `skills/shared/scripts/reframe.py` (`reframe -h` để xem tham số).

```bash
# Chuyển ngang sang dọc, lấp nền mờ (ổn nhất, không mất khung hình)
python skills/shared/scripts/reframe.py reframe -i <video> \
  -o "outputs/<chủ đề>/<tên>-9x16.mp4" --ratio 9:16 --mode blur

# Cắt theo tiêu điểm, chủ thể lệch phải thì kéo tiêu điểm về 0.65
python skills/shared/scripts/reframe.py reframe -i <video> \
  -o "outputs/<chủ đề>/<tên>-9x16.mp4" --ratio 9:16 --mode crop --focus-x 0.65

# Cắt theo nhận diện khuôn mặt (video nói/video có người)
python skills/shared/scripts/reframe.py reframe -i <video> \
  -o "outputs/<chủ đề>/<tên>-9x16.mp4" --ratio 9:16 --mode smart
```
`--size WxH` ép được độ phân giải cuối (mặc định suy ra từ tỉ lệ và độ phân giải nguồn, ví dụ 1280x720 → 720x1280).

## Nhận biết Profile

- Có Profile: tỉ lệ đích mặc định lấy theo nền tảng chính trong `platforms.md` (Douyin/Xiaohongshu dọc 9:16, Bilibili ngang 16:9,
  WeChat Moments/ins vuông 1:1); kênh dạng video nói/có người mặc định chế độ `smart`.
- Không có Profile: mặc định chế độ `blur` + hỏi nền tảng/tỉ lệ đích.

## Quy tắc

1. Không chắc chọn cái nào: chuyển ngang sang dọc thì ưu tiên `blur` (không mất khung hình); chủ thể rõ và muốn phủ kín thì dùng `crop`; người nói trước ống kính thì dùng `smart`.
2. Khi `smart` không phát hiện được khuôn mặt thì tự lùi về cắt giữa, và ghi rõ trong báo cáo.
3. Audio tự động được giữ (copy), không encode lại âm thanh.
4. Độ phân giải đầu ra bị ép căn số chẵn (yêu cầu của H.264), không cần xử lý tay.
5. Sản phẩm đều nằm trong `outputs/<chủ đề>/`.

## Nguồn tham khảo

Lấp nền mờ (blurred bars) là cách làm phổ biến khi thích ứng màn dọc; cắt theo nhận diện khuôn mặt tham khảo ý tưởng của
AI-Youtube-Shorts-Generator, dùng OpenCV Haar cascade tìm vị trí trung vị khuôn mặt để định tiêu điểm. Hình học cắt và kẹp biên được đóng gói thành script xác định.
