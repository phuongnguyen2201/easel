---
name: video-chapters
description: >-
  Chia chương và lập mục lục timestamp cho video trung/dài (chương YouTube, phần mô tả) để người
  xem nhảy nhanh, tăng tỉ lệ xem hết. Dùng khi người dùng nói "chia chương video", "mục lục
  timestamp", "chapters", "thêm mốc thời gian". video-to-article viết thành bài, skill này chỉ ra
  mục lục.
layer: produce
---

# Chương video / mục lục timestamp

> Sinh mục lục timestamp chương cho video trung/dài (dùng được ở phần mô tả của Bilibili/YouTube). Transcript kèm mốc thời gian chạy `asr.py`,
> **việc chia chương và đặt tên chương do bạn (LLM) làm**.

> Ra bài viết hoàn chỉnh: xem **video-to-article**; ra phụ đề: xem **auto-subtitle**; cắt thành video ngắn: xem **video-highlights**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| File video | Có | Video trung/dài (hướng dẫn/review/bài giảng/phát lại livestream; không đưa thì hỏi) |
| Nền tảng đích | Không | Bilibili / YouTube / dùng chung (ảnh hưởng định dạng và cách diễn đạt) |
| Số chương | Không | Số chương mong muốn (mặc định chia tự nhiên theo nội dung, thường 5-12 đoạn) |

## Đầu ra (`outputs/<chủ đề>/`)

- `chapters.txt` - mục lục timestamp (mỗi dòng `mm:ss tên chương`, dán thẳng vào phần mô tả được)
- `chapters.json` - dạng cấu trúc (start tính bằng giây + tiêu đề), để chương trình dùng
- `transcript.txt` - bản transcript gốc (để tra lại)

## Các bước thực thi

Đường dẫn script (tương đối gốc dự án): `skills/shared/scripts/asr.py`.

### 1. Transcript kèm mốc thời gian
```bash
python skills/shared/scripts/asr.py transcribe -i <video> --format json \
  -o "outputs/<chủ đề>/transcript.json"
```
(Lần đầu chạy ASR cần proxy ra ngoài để tải model, xem phần yêu cầu trước của auto-subtitle.)

### 2. Chia chương (bạn tự làm)
Đọc transcript.json (mỗi đoạn có start/end), chia chương theo **điểm chuyển chủ đề**:
- Tìm điểm đổi chủ đề làm ranh giới chương (không cắt đều theo thời gian mà cắt theo nội dung).
- **Chương đầu bắt đầu từ 00:00** (nền tảng yêu cầu, không thì tính năng chương không chạy).
- Tên mỗi chương 6-16 chữ, mở đầu bằng động từ hoặc nêu thẳng điểm đáng xem (ví dụ "Thử pin thực tế và cái kết", "3 phút để bạn dùng thành thạo"), không viết "Phần một".
- Số chương vừa phải (quá vụn thì khán giả khó chịu, quá thô thì vô dụng), thường 5-12 đoạn; video ngắn (<3 phút) thường không cần chia chương.
- Chương ngắn nhất ≥10 giây (YouTube yêu cầu khoảng cách giữa hai chương liền kề ≥10s).

### 3. Xuất mục lục
Ghi `chapters.txt` (mỗi dòng `mm:ss tên chương`, dòng đầu bắt buộc là `00:00`):
```
00:00 Mở đầu | Hôm nay bàn gì
01:24 Cái bẫy đầu tiên: xxx
03:50 Phần thử nghiệm thực tế
...
```
Đồng thời ghi `chapters.json`: `[{"start": 0, "title": "Mở đầu | Hôm nay bàn gì"}, ...]`.

## Khác biệt định dạng theo nền tảng

- **YouTube**: dán vào phần mô tả video, mốc đầu bắt buộc `0:00`, có ≥3 chương và mỗi chương ≥10s thì tự kích hoạt.
- **Bilibili**: dùng làm "điểm xem/chương trên thanh tiến trình" hoặc phần mô tả phân P, định dạng `mm:ss tiêu đề`.
- **Dùng chung**: `chapters.txt` đọc được ở mọi nơi.

## Quy tắc

1. Ranh giới chương xác định theo **điểm chuyển chủ đề**, không cắt đều theo thời gian.
2. Chương đầu bắt buộc 00:00; khoảng cách giữa hai chương liền kề ≥10s.
3. Tên chương nêu thẳng điểm đáng xem, ngắn gọn hấp dẫn, không dùng tên rỗng kiểu "Phần một".
4. Không bịa nội dung video không nói; chia chương đúng theo transcript.
5. Sản phẩm đều đưa vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Timestamp chương là cách làm chuẩn để tăng tỉ lệ xem hết và khả năng tìm kiếm trên YouTube/Bilibili (chương đầu 0:00, khoảng cách ≥10s là quy tắc cứng của nền tảng).
Transcript dùng faster-whisper (asr.py) để ra mốc thời gian, việc chia chủ đề giao cho LLM - tách bạch phần IO xác định và phần phân chia ngữ nghĩa.
