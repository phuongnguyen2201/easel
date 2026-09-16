---
name: video-editing
description: >-
  Dựng video bằng ffmpeg: cắt, ghép, đổi tốc độ, bỏ khoảng lặng, chèn chữ, đổi tỉ lệ, lấy ảnh bìa,
  GIF, nén, BGM/watermark. Dùng khi người dùng nói "cắt video", "ghép video", "nén video". Đổi
  khung thông minh → video-reframe; cắt highlight → clipify/video-highlights; tạo mới →
  ai-video-gen.
layer: produce
---

# Dựng video

Xử lý video phổ thông bằng chỉ dẫn ngôn ngữ tự nhiên. Mọi thao tác đều gọi script dùng chung
`skills/shared/scripts/video_ops.py` (bọc ffmpeg/ffprobe qua subprocess),
**đừng tự ghép lệnh ffmpeg tại chỗ** - script đã lo đồng bộ tiếng/hình, đường dẫn font, giá trị mã hoá mặc định,
bắt lỗi và các điểm dễ sai khác.

> Chạy từ thư mục gốc dự án. Đường dẫn script tương đối: `skills/shared/scripts/video_ops.py`.
> Mỗi subcommand đều hỗ trợ `-h` để xem tham số.

## Đầu vào

- Đường dẫn file video + mô tả thao tác (người dùng không đưa đường dẫn thì hỏi)
- Tuỳ chọn: nền tảng đích/tỉ lệ khung hình/khoảng thời gian và các tham số khác

## Đầu ra

Video/ảnh sau xử lý, lưu vào `outputs/<chủ đề>/`. Script sẽ in `✅ <đường dẫn> (dung lượng)`.

## Ranh giới với clipify

- **clipify** = **quy trình chuyên biệt**: cắt thông minh video dài + pan bám mặt + burn phụ đề từng chữ.
  Dùng khi cần "tìm đoạn hay trong video dài, làm thành video ngắn dọc có phụ đề".
- **video-editing (SKILL này)** = xử lý dựng phim phổ thông. Dùng khi làm một thao tác lẻ hoặc tự phối hợp nhiều thao tác.
  Không bám mặt, không burn phụ đề (đó là việc của clipify).

## Tra nhanh subcommand

Chạy `python skills/shared/scripts/video_ops.py info -i <video>` xem rõ thông tin nguồn trước rồi mới thao tác.

| Subcommand | Công dụng | Tham số chính |
|--------|------|----------|
| `cut` | Cắt theo thời điểm bắt đầu/kết thúc | `--start --end`/`--duration`, `--reencode` để cắt chính xác |
| `concat` | Ghép nhiều đoạn | `--mode demuxer` (cùng thông số, không mất chất)/`filter` (khác thông số, đưa về chuẩn chung) |
| `speed` | Đổi tốc độ (đồng bộ tiếng/hình) | `--factor 2.0` |
| `silence-cut` | Dò và bỏ khoảng lặng (jump cut) | `--noise -30 --min-silence 0.5 --pad 0.05` (bí danh `mute-cut`) |
| `text` | Chèn chữ lên hình | `--text --position --fontsize --color --start --end --box` |
| `aspect` | Đổi tỉ lệ ngang/dọc | `--ratio 9:16 --mode pad` (thêm viền)/`crop` (cắt bớt) |
| `frame` | Trích khung làm ảnh bìa | `--time 00:00:03 --width` |
| `gif` | Chuyển sang GIF | `--start --end --fps 12 --width 480` |
| `compress` | Nén | `--crf 26` hoặc `--bitrate 2M`, `--scale` để hạ độ phân giải |
| `bgm` | Mix thêm nhạc nền | `--music --voice-volume 1.0 --music-volume 0.3` |
| `watermark` | Chèn watermark ảnh | `--logo --position --width --opacity` |
| `info` | Thời lượng/độ phân giải/fps/bitrate (json) | `-i` |

Vị trí của `text` / `watermark` chọn một trong bảy: `center top bottom top-left top-right
bottom-left bottom-right`. Font CJK được dò tự động (wqy-microhei / Noto CJK),
cũng có thể chỉ định rõ bằng `--font`.

## Ví dụ thường dùng

```bash
V=skills/shared/scripts/video_ops.py

# Cắt đoạn 00:02:00-00:15:00
python $V cut -i in.mp4 -o out.mp4 --start 00:02:00 --end 00:15:00

# Chuyển ngang sang dọc (nhu cầu bắt buộc khi làm bản dọc cho mạng xã hội): thêm viền không cắt hoặc cắt cho đầy khung
python $V aspect -i in.mp4 -o vertical.mp4 --ratio 9:16 --mode pad
python $V aspect -i in.mp4 -o vertical.mp4 --ratio 9:16 --mode crop

# Bỏ khoảng lặng + tăng tốc 1.25 lần (jump cut trước, đổi tốc độ sau)
python $V silence-cut -i in.mp4 -o t.mp4
python $V speed -i t.mp4 -o out.mp4 --factor 1.25

# Trích khung ở giây thứ 3 làm ảnh bìa
python $V frame -i in.mp4 -o cover.jpg --time 00:00:03 --width 1080

# Chuyển đoạn giây 2-6 sang GIF
python $V gif -i in.mp4 -o clip.gif --start 2 --end 6 --fps 12 --width 480

# Chèn chữ "Theo dõi mình nhé" trong 5 giây tại giây thứ 60 (đáy khung hình, có khung nền)
python $V text -i in.mp4 -o out.mp4 --text "Theo dõi mình nhé" --position bottom --box --start 60 --end 65

# Thêm BGM (giọng gốc 1.0 / BGM 0.3), chèn watermark góc dưới phải, nén
python $V bgm -i in.mp4 -o out.mp4 --music bgm.mp3 --music-volume 0.3
python $V watermark -i in.mp4 -o out.mp4 --logo logo.png --position bottom-right --width 120
python $V compress -i in.mp4 -o small.mp4 --crf 26 --scale 720
```

## Thao tác kết hợp

Nối chuỗi: sản phẩm của bước trước là đầu vào của bước sau. Thứ tự điển hình `cut → silence-cut → speed → text →
aspect → compress`. Chuyển sang bản dọc để cuối cùng (chèn chữ trên khung hình cuối dễ kiểm soát hơn).

## Quy chuẩn nền tảng (bảng rút gọn)

| Nền tảng | Tỉ lệ | Thời lượng | Ghi chú |
|------|------|------|------|
| Douyin/Video Channels/Reels | 9:16 | ≤60s là khung vàng, 3s đầu quyết định thành bại | 1080x1920 |
| Video Xiaohongshu | 9:16 / 3:4 | ≤60s | Ưu tiên bản dọc |
| Bilibili/YouTube bản ngang | 16:9 | Từ vài phút trở lên | 1920x1080 |
| Instagram Feed | 4:5 / 1:1 | Ngắn | 4:5 chiếm màn hình nhiều hơn |

Quy chuẩn chi tiết hơn thì tra `references/` khi cần (nếu có).

## Yêu cầu môi trường

- **ffmpeg + ffprobe** - ✅ đã cài (script kiểm tra ngay khi khởi động, thiếu thì báo lỗi và thoát)
- **Burn phụ đề/phụ đề từng chữ** - dùng clipify (cần whisper); SKILL này chỉ chèn chữ bằng `text`

## Chỉ dẫn cho Agent

1. **Chạy `info` trước** để xem tỉ lệ/thời lượng/có tiếng hay không của nguồn rồi mới quyết định thao tác
2. **Mỗi thao tác gọi đúng subcommand tương ứng**, đừng tự viết ffmpeg; không chắc tham số thì dùng `<subcommand> -h`
3. **Nhiều thao tác thì nối chuỗi**, sản phẩm trung gian có thể để ở `.drafts/`
4. **Sản phẩm xuất ra** `outputs/<chủ đề>/`, cuối cùng báo lại đường dẫn và thời lượng
