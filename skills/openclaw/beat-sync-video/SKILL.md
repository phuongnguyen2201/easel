---
name: beat-sync-video
description: >-
  Dựng video bắt nhịp: phát hiện beat nhạc nền, chuyển ảnh/clip đúng nhịp kèm hiệu ứng zoom/nháy
  trắng cho thật cháy. Dùng khi người dùng nói "video bắt nhịp", "cắt theo beat", "ảnh chuyển theo
  nhạc", "bắt beat". slideshow-video mỗi ảnh thời lượng cố định, chuyển mềm; skill này cắt cứng
  theo nhịp.
layer: produce
---

# Video bắt nhịp (cắt theo beat)

> Dùng librosa phát hiện nhịp của nhạc nền, cắt cứng hình ngay trên nhịp, thêm hiệu ứng theo nhịp, ra video ngắn "bắt beat" cháy.
> Mọi thứ đi qua `skills/shared/scripts/beatsync.py`, **đừng tự đếm nhịp hay tự ghép filter** - script đã lo
> phát hiện nhịp, chia đoạn, lặp tư liệu, đồng bộ tiếng hình.

> Album mềm mỗi ảnh một thời lượng cố định xem **slideshow-video**; chủ đề -> AI dựng ảnh và giọng đọc xem **auto-short-video**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Nhạc nền | Có | File nhạc quyết định điểm bắt nhịp (nhịp càng mạnh càng đẹp; chưa có thì hỏi) |
| Tư liệu | Có | Một loạt ảnh và/hoặc clip ngắn (theo thứ tự, dùng lặp lại), hoặc một thư mục |
| Khung hình | Có | Khi người dùng hoặc task phía trước chưa nói rõ ngang/dọc (hoặc độ phân giải cụ thể), phải hỏi lại và chờ xác nhận trước khi dựng; không được tự suy theo nền tảng, Profile hay giá trị mặc định, đã rõ rồi thì không hỏi lại |
| Tần suất cắt | Không | Mấy nhịp cắt một lần (mặc định mỗi 2 nhịp) |
| Hiệu ứng | Không | `zoom` đẩy tới (mặc định) / `flash` nháy trắng / `none` |

## Đầu ra (`outputs/<chủ đề>/`)

- Video bắt nhịp hoàn chỉnh (`*.mp4`)
- Báo cáo: số đoạn bắt nhịp, tổng thời lượng, BPM phát hiện được, hiệu ứng

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/beatsync.py` (`build -h` / `beats -h`).

### 1. (Tuỳ chọn) Xem nhịp trước
```bash
python skills/shared/scripts/beatsync.py beats --music <nhạc>
# In ra tempo (BPM) và các mốc thời gian của nhịp, để biết nên đặt --every bao nhiêu
```

### 2. Dựng video bắt nhịp
```bash
python skills/shared/scripts/beatsync.py build \
  -i 1.jpg 2.jpg 3.jpg 4.jpg --music <nhạc> \
  -o "outputs/<chủ đề>/show.mp4" \
  --size 1080x1920 --every 2 --effect zoom
```
- Tư liệu = ảnh hoặc clip ngắn, **số lượng có thể ít hơn số đoạn bắt nhịp** (tự động lặp lại).
- `--every 1` cắt ở mọi nhịp (chớp nhanh, cần nhiều tư liệu); `--every 4` mỗi ô nhịp cắt một lần (thong thả).
- `--effect flash` nháy trắng đầu đoạn cho "cháy" hơn; `--effect none` cắt cứng gọn gàng.
- `--max-duration 15` giới hạn độ dài thành phẩm (ví dụ làm clip TikTok 15s).
- Cũng có thể `--images-dir <thư mục>` nạp tư liệu hàng loạt (sắp theo tên file).

## Nhận biết Profile

- Có Profile: `platforms.md` chỉ dùng để gợi ý khung hình, vẫn phải để người dùng xác nhận; phong cách bắt nhịp (chớp nhanh/thong thả) và hiệu ứng bám tông kênh
  (kênh trend/thể thao thiên về chớp nhanh flash, kênh đời sống/chữa lành thiên về zoom thong thả).
- Không có Profile: xác nhận ngang/dọc trước; mặc định mỗi 2 nhịp, hiệu ứng zoom.

## Quy tắc

1. Nhịp nhạc càng rõ thì bắt nhịp càng chuẩn; khi không có nhịp rõ, script tự lùi về cắt đều khoảng và ghi chú trong báo cáo.
2. Bắt nhịp phải **cắt cứng** (không thêm transition), thêm vào là nhoè mất cảm giác nhịp - đây là chủ ý thiết kế.
3. Thiếu tư liệu thì tự lặp; đủ tư liệu nên để `--every 1~2` để mỗi đoạn là một hình mới.
4. Thành phẩm mặc định dài bằng nhạc, dùng `--max-duration` để khớp giới hạn thời lượng của nền tảng.
5. Sản phẩm luôn nằm trong `outputs/<chủ đề>/`.

## Nguồn tham khảo

Phát hiện nhịp dùng `beat_track` của librosa (cường độ onset + quy hoạch động để tìm điểm nhịp), cắt cứng hình đúng điểm nhịp là cách làm
chuẩn của video bắt beat. Gói nhịp -> chia đoạn -> render từng đoạn -> đồng bộ tiếng hình thành script xác định, tránh đếm nhịp tay bị lệch.
