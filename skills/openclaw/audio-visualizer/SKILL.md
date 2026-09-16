---
name: audio-visualizer
description: >-
  Render audio thuần (podcast, nhạc, câu nói hay) thành video sóng/phổ động kèm bìa, tiêu đề để
  đăng TikTok/Shorts/Reels. Dùng khi người dùng nói "audio thành video", "podcast lên TikTok",
  "video sóng nhạc", "làm hình cho audio". audio-mix ra audio, skill này ra video; slideshow-video
  dùng ảnh.
layer: produce
---

# Video trực quan hoá audio

> Render audio thành video có sóng/phổ chuyển động, kèm ảnh bìa + tiêu đề, để audio thuần đăng được lên nền tảng video. Tất cả đi qua
> `skills/shared/scripts/audio_viz.py`, **đừng tự ghép tay filter showwaves/showcqt**.

> Xuất audio (mix) xem **audio-mix**; làm video từ ảnh xem **slideshow-video**;
> thêm phụ đề cho video có sẵn xem **auto-subtitle**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| File audio | Có | Podcast/nhạc/đoạn video nói (không đưa thì hỏi) |
| Khung hình | Có | Khi người dùng hoặc task phía trên chưa nói rõ ngang/dọc (hoặc độ phân giải cụ thể), phải hỏi lại và chờ xác nhận trước khi làm; không được im lặng suy theo nền tảng, Profile hay giá trị mặc định, đã rõ rồi thì không hỏi lại |
| Chế độ | Không | `cqt` (mặc định, nhạc nhìn đẹp nhất) / `bars` / `waves` / `spectrum` |
| Ảnh bìa | Không | Ảnh bìa đặt giữa (bìa album/ảnh đại diện/ảnh chủ đề) |
| Tiêu đề | Không | Dòng chữ tiêu đề ở trên cùng |

## Đầu ra (`outputs/<chủ đề>/`)

- Video trực quan hoá (`*.mp4`, audio đã nhúng sẵn)
- Báo cáo: chế độ, thời lượng, khung hình

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/audio_viz.py` (`render -h` để xem tham số).

```bash
# Nhạc/câu đắt: phổ nhạc CQT (nhảy theo nốt, nhìn đẹp nhất)
python skills/shared/scripts/audio_viz.py render -i clip.mp3 \
  -o outputs/<chủ đề>/out.mp4 --mode cqt --title "Câu đắt số này" --cover cover.jpg

# Podcast/video nói: dải sóng dưới đáy + ảnh bìa
python skills/shared/scripts/audio_viz.py render -i podcast.mp3 \
  -o outputs/<chủ đề>/out.mp4 --mode waves --cover avatar.png --size 1080x1920

# Cột nhảy theo nhịp / phổ âm cuộn
python skills/shared/scripts/audio_viz.py render -i song.mp3 -o out.mp4 --mode bars
python skills/shared/scripts/audio_viz.py render -i song.mp3 -o out.mp4 --mode spectrum
```

## Chọn chế độ thế nào

| Chế độ | Cảm giác nhìn | Hợp với |
|------|------|------|
| `cqt` | Phổ nốt nhạc toàn màn hình, nhảy theo giai điệu | Nhạc, nội dung có giai điệu (mặc định) |
| `bars` | Cột phổ ở đáy, cảm giác bắt nhịp mạnh | Nhạc, cắt theo nhịp, radio |
| `waves` | Đường sóng ở đáy, gọn và sạch | Podcast, video nói, phỏng vấn |
| `spectrum` | Phổ âm cuộn toàn màn hình, chất công nghệ | Nhạc điện tử/chủ đề công nghệ, tạo không khí |

`--bg-image` đổi ảnh nền, `--color` đổi màu nền, `--wave-color` đổi màu sóng.

## Nhận biết Profile

- Có Profile: `platforms.md` chỉ dùng để gợi ý khung hình, vẫn phải để người dùng xác nhận; phong cách tiêu đề/ảnh bìa bám theo kênh;
  kênh podcast/video nói mặc định `waves`, kênh nhạc mặc định `cqt`/`bars`.
- Không có Profile: xác nhận ngang/dọc trước; mặc định chế độ cqt.

## Quy tắc

1. Audio dài thì dùng audio-editing/text-condenser cắt ra đoạn câu đắt rồi mới trực quan hoá, đừng render cả tập.
2. Nhúng nguyên tiếng gốc vào bản xuất, không resample làm mất chất lượng.
3. Ảnh bìa được thu phóng đúng tỉ lệ và căn giữa, tiêu đề tự viền để bảo đảm dễ đọc.
4. Sản phẩm gom hết vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Trực quan hoá sóng/phổ audio bằng ffmpeg `showwaves`/`showfreqs`/`showspectrum`/`showcqt` là cách chuẩn để podcast/kênh audio
lên được nền tảng video. Các filter trực quan hoá cùng phần ghép ảnh bìa/tiêu đề được gói thành script chạy ra kết quả xác định.
