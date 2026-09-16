---
name: video-intro-outro
description: >-
  Tạo thẻ mở đầu/kết thúc (tiêu đề, tiêu đề phụ, logo, kêu gọi theo dõi) và nối vào video chính
  bằng cắt cứng hoặc fade. Dùng khi người dùng nói "thêm intro/outro", "làm đoạn mở đầu", "thẻ kết
  thúc", "cuối video kêu gọi theo dõi". poster-hero ra ảnh bìa tĩnh, skill này ra video nối được.
layer: produce
---

# Thẻ mở đầu / thẻ kết thúc video

> Sinh **thẻ video** mở đầu/kết thúc (tiêu đề + tiêu đề phụ + logo + kêu gọi theo dõi), rồi ghép mở đầu + video chính + kết thúc
> sau khi chuẩn hoá thành một bản hoàn chỉnh. Tất cả đi qua `skills/shared/scripts/intro_outro.py`, **đừng tự ghép tay
> drawtext / xfade** - script đã lo đường dẫn font, đồng nhất tham số hình-tiếng, tính offset thời gian chuyển cảnh.

> Chỉ làm "thẻ mở đầu/kết thúc + ghép nối". Ảnh bìa tĩnh xem **poster-hero**; dựng cắt thông thường xem **video-editing**;
> quy trình đầy đủ "một câu -> thành phẩm" xem **auto-short-video**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Video chính | Bắt buộc khi ghép | Video cần thêm mở đầu/kết thúc (không đưa thì hỏi) |
| Tiêu đề/tiêu đề phụ | Nên có | Nội dung như chủ đề phần mở đầu, lời cảm ơn phần kết |
| CTA kêu gọi theo dõi | Hay dùng ở phần kết | Ví dụ "Like + Theo dõi để không lạc nhau" |
| logo | Tuỳ chọn | Ảnh logo thương hiệu, đặt chồng phía trên tiêu đề |
| Khung hình | Tuỳ chọn | Mặc định dọc 1080x1920; khi ghép thì mặc định bám theo video chính |
| Nền | Tuỳ chọn | Màu đơn / gradient hai màu / ảnh |

## Đầu ra (`outputs/<chủ đề>/`)

- Đoạn thẻ mở đầu / kết thúc (`intro.mp4` / `outro.mp4`)
- Bản hoàn chỉnh sau khi ghép (`*-final.mp4`)
- Báo cáo: thời lượng thẻ, khung hình, kiểu chuyển cảnh

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/intro_outro.py` (mọi subcommand đều hỗ trợ `-h`).

### 1. Sinh thẻ mở đầu
```bash
python skills/shared/scripts/intro_outro.py card \
  --title "Chủ đề số này" --subtitle "Giải thích gọn trong 3 phút" \
  --gradient --color 0x1a2a6c --color2 0xb21f1f \
  --size 1080x1920 --duration 2.5 -o "outputs/<chủ đề>/intro.mp4"
```

### 2. Sinh thẻ kết thúc (kèm kêu gọi theo dõi)
```bash
python skills/shared/scripts/intro_outro.py card --preset outro \
  --title "Cảm ơn đã xem" --cta "Like + Theo dõi để không lạc nhau" \
  --color black --size 1080x1920 --duration 2.5 \
  -o "outputs/<chủ đề>/outro.mp4"
```
Chọn một kiểu nền: `--color <màu>` (màu đơn) / `--gradient` (dùng kèm `--color`/`--color2` cho gradient hai màu) /
`--bg-image <ảnh>` (nền ảnh, tự cắt cho đầy khung). `--logo <ảnh>` để chồng logo thương hiệu.

### 3. Ghép vào video chính
```bash
# Cắt cứng (mặc định, ổn nhất)
python skills/shared/scripts/intro_outro.py attach --main "<video chính>" \
  --intro "outputs/<chủ đề>/intro.mp4" \
  --outro "outputs/<chủ đề>/outro.mp4" \
  -o "outputs/<chủ đề>/<tên>-final.mp4"

# Chuyển cảnh mờ dần
python skills/shared/scripts/intro_outro.py attach --main "<video chính>" \
  --intro "outputs/<chủ đề>/intro.mp4" --transition fade --trans-duration 0.5 \
  -o "outputs/<chủ đề>/<tên>-final.mp4"
```
`--intro` / `--outro` phải có ít nhất một, cũng có thể chỉ thêm một cái. `--transition` chọn trong
`none/fade/fadeblack/fadewhite/wipeleft/slideup/circleopen`. Khung hình mặc định bám theo video chính,
`--size` để ép cứng.

## Nhận biết Profile

- Có Profile: giọng tiêu đề/CTA bám persona trong `style.md`; có logo/màu chủ đạo thương hiệu thì dùng cho `--logo` và
  `--color`; khung hình mặc định theo nền tảng chính trong `platforms.md` (Douyin/Xiaohongshu dọc 1080x1920, Bilibili/ngang 1920x1080).
- Không có Profile: dùng nội dung trung tính và nền tối mặc định, dọc 1080x1920, cuối cùng nhắc người dùng có thể đưa thông tin thương hiệu để tuỳ biến.

## Quy tắc

1. Thời lượng thẻ mặc định 2.5s, phần mở đầu đừng dài quá (2-3s là vừa), tránh làm người xem bỏ đi.
2. Câu chữ gọn - tiêu đề một câu, tiêu đề phụ một câu, CTA một câu, đừng chất chữ.
3. Trước khi ghép, script tự chuẩn hoá ba đoạn về cùng khung hình/frame rate/track tiếng, **đừng** tự chuyển định dạng trước.
4. Thời lượng chuyển cảnh tự giới hạn trong độ dài đoạn liền kề, dài quá sẽ bị bóp lại.
5. Sản phẩm đều đi vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Thẻ mở đầu/kết thúc và thẻ kêu gọi theo dõi là chuẩn mực của video ngắn và YouTube; phần hiện thực tham khảo ffmpeg drawtext (lớp chữ)
và xfade/acrossfade (chồng lấn hình-tiếng khi chuyển cảnh) theo tổ hợp xác định, gói phần offset thời gian và căn chỉnh tham số dễ sai vào trong script.
