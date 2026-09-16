---
name: slideshow-video
description: >-
  Ghép album ảnh thành video: Ken Burns, chuyển cảnh, nhạc nền, phụ đề từng ảnh, tự khớp khung
  dọc/vuông/ngang. Dùng khi người dùng nói "ảnh thành video", "mấy tấm ảnh này làm video", "video
  album ảnh", "slideshow ảnh". auto-short-video tự sinh ảnh/giọng từ chủ đề; skill này ghép ảnh có
  sẵn.
layer: produce
---

# Album ảnh → video

> Ghép một loạt ảnh thành một video: Ken Burns (zoom chậm) + chuyển cảnh giữa các ảnh + nhạc nền + phụ đề từng ảnh,
> tự khớp khung hình đích. Toàn bộ chạy qua `skills/shared/scripts/slideshow.py`, **đừng tự ghép tay
> zoompan / xfade** - script đã lo phần quy đổi số frame, offset chuyển cảnh và canh độ dài tiếng với hình.

> Chỉ làm "ảnh có sẵn → video". Muốn tự sinh ảnh/giọng từ chủ đề theo pipeline đầy đủ thì xem **auto-short-video**;
> cắt dựng video có sẵn xem **video-editing**; làm một tấm ảnh bìa/poster xem **poster-hero**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Ảnh | Có | Một loạt đường dẫn ảnh (theo thứ tự), hoặc một thư mục ảnh (sắp theo tên file) |
| Khung hình | Có | Khi người dùng hoặc task phía trên chưa nói rõ ngang/dọc/vuông (hoặc độ phân giải cụ thể), phải hỏi và chờ xác nhận trước khi làm; không được tự suy theo nền tảng, Profile hay giá trị mặc định, đã rõ rồi thì đừng hỏi lại |
| Thời lượng mỗi ảnh | Không | Mặc định 3 giây một tấm |
| Chuyển cảnh | Không | Mặc định mờ dần `fade`; `none` là cắt cứng |
| BGM | Không | File nhạc nền (tự lặp/cắt theo độ dài phim/fade ở cuối) |
| Phụ đề từng ảnh | Không | Mỗi tấm một câu phụ đề |

## Đầu ra (`outputs/<chủ đề>/`)

- Video thành phẩm (`*.mp4`)
- Báo cáo: số ảnh, tổng thời lượng, khung hình, kiểu chuyển cảnh, có BGM hay không

## Các bước thực thi

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/slideshow.py` (`build -h` để xem đủ tham số).

### Dùng cơ bản
```bash
python skills/shared/scripts/slideshow.py build \
  -i 1.jpg 2.jpg 3.jpg -o "outputs/<chủ đề>/show.mp4" \
  --size 1080x1920 --per 3 --transition fade
```

### Kèm BGM + phụ đề từng ảnh
```bash
python skills/shared/scripts/slideshow.py build --images-dir ./photos \
  -o "outputs/<chủ đề>/show.mp4" \
  --bgm ./music.mp3 --bgm-volume 0.7 \
  --captions "Câu mở đầu|Chú thích ảnh 2|Chú thích ảnh 3"
```
Phụ đề cũng có thể đưa qua `--captions-file <file>` (mỗi dòng ứng với một ảnh).

### Biến thể hay dùng
- **Ảnh đứng yên (không zoom)**: `--no-kenburns`, đi kèm `--fit pad` (chèn viền) hoặc `--fit crop` (cắt cho đầy khung).
- **Đổi chuyển cảnh**: `--transition` chọn được `fade/fadeblack/fadewhite/wipeleft/wiperight/slideup/slidedown/circleopen/dissolve/none`.
- **Khung theo nền tảng**: TikTok/Reels dọc `1080x1920`, feed/story vuông `1080x1080`, YouTube/ngang `1920x1080`.

## Bám theo Profile

- Có Profile: `platforms.md` chỉ dùng để gợi ý khung hình, vẫn phải để người dùng xác nhận; giọng phụ đề bám `style.md`;
  gợi ý phong cách BGM bám tông của kênh (vui tươi/chữa lành/máu lửa).
- Không có Profile: hỏi ngang/dọc/vuông trước; chuyển cảnh mặc định fade + Ken Burns.

## Quy tắc

1. Thứ tự ảnh = thứ tự trong video; dùng `--images-dir` thì sắp theo tên file, cần thì đổi tên trước.
2. Thời lượng chuyển cảnh tự giới hạn trong thời lượng mỗi ảnh (không vượt `--per`).
3. BGM tự lặp cho đủ rồi cắt theo độ dài thành phẩm, fade ở cuối; không có BGM thì chèn track im lặng cho dễ đăng.
4. Số câu phụ đề có thể ít hơn số ảnh (ảnh dư thì không có phụ đề), không bắt buộc một đối một.
5. Sản phẩm đều đi vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Ken Burns (zoom và dịch chậm) + chuyển cảnh chồng mờ + BGM là cách làm chuẩn cho video album/bộ ảnh (cùng hướng
với các công cụ video ngắn như MoneyPrinterTurbo); SKILL này dùng lại phương án zoompan của bộ dựng auto-short-video, gói phần quy đổi số frame và
tính offset xfade thành script tất định, tránh viết tay chuỗi filter rồi sai.
