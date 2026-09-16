---
name: skill-publish-scheduler
description: >-
  Hẹn giờ đăng hàng loạt từ bảng "nội dung × nền tảng × giờ đăng": nhập lịch, xem hàng đợi, tính
  mục đến hạn, đến giờ giao SKILL đăng từng nền tảng, ghi lại trạng thái; thuần script, không tự
  đăng. Dùng khi người dùng nói "hẹn giờ đăng", "đăng theo lịch", "hàng đợi đăng", "đến giờ tự
  đăng".
layer: publish
---

# Hẹn giờ đăng hàng loạt theo lịch

> Quản lý một bảng lịch đăng (nội dung x nền tảng x giờ), đến giờ thì giao việc cho SKILL đăng của từng nền tảng. Chạy qua
> `scripts/publish_queue.py` (thuần thư viện chuẩn). **SKILL này lo điều phối và trạng thái, việc đăng thật giao cho publisher của từng nền tảng**
> (SKILL đăng của từng nền tảng - adapter VN dựng ở Giai đoạn 5).

## Đầu vào

Bảng lịch đăng dạng CSV (header phải có `publish_at, platform, content`, tuỳ chọn `title, note`):
```csv
publish_at,platform,content,title
2026-08-01 09:00,xiaohongshu,outputs/note1,Bài buổi sáng
2026-08-01 20:00,douyin,outputs/<chủ đề>/final.mp4,Video buổi tối
```
Hoặc file JSON tương đương.

## Thực thi

Đường dẫn script (tính từ gốc dự án): `skills/openclaw/skill-publish-scheduler/scripts/publish_queue.py` (mỗi subcommand đều có `-h`).

```bash
Q=outputs/publish-queue/q.json
python <skill>/scripts/publish_queue.py import --file plan.csv --queue $Q   # nhập lịch đăng
python <skill>/scripts/publish_queue.py list  --queue $Q                    # xem hàng đợi
python <skill>/scripts/publish_queue.py due   --queue $Q                    # các mục đến hạn lúc này
python <skill>/scripts/publish_queue.py run   --queue $Q                    # in kế hoạch giao việc cho mục đến hạn
# Theo kế hoạch, giao từng mục cho publisher của nền tảng tương ứng để đăng, xong thì ghi lại trạng thái:
python <skill>/scripts/publish_queue.py mark  --queue $Q --id 1 --status done
```

## Quy trình giao việc khi đến hạn (điều phối)

1. `due`/`run` cho ra các mục đến hạn ngay lúc này.
2. **Với từng mục đến hạn**: theo `platform` mà giao cho SKILL đăng tương ứng thực hiện việc đăng thật
   (một nền tảng, hoặc dùng cross-platform-publish). Trước khi đăng thì chỉnh định dạng nội dung cho hợp nền tảng.
3. Đăng thành công/thất bại xong thì `mark` để ghi lại trạng thái (có thể kết hợp skill-publish-notify đẩy kết quả, skill-publish-log lưu nhật ký).
4. Khi cần "canh giờ tự kích hoạt", để tác vụ định kỳ của OpenClaw chạy `run` theo chu kỳ (script này chỉ tính đến hạn một lần, không chạy thường trú).

## Quy tắc

1. SKILL này không trực tiếp điều khiển trình duyệt/API để đăng - chỉ lo lịch và trạng thái, việc đăng giao cho publisher của từng nền tảng.
2. `--now` cho phép ghi đè thời gian hiện tại để chạy thử (xem tại một thời điểm sẽ đăng những gì), không ảnh hưởng thời gian thật.
3. Giờ đăng dùng định dạng `YYYY-MM-DD HH:MM`; cùng một thời điểm thì nhiều nền tảng sẽ đến hạn cùng lúc.
4. Mỗi mục đăng xong bắt buộc phải `mark`, tránh đăng trùng.
5. Việc kích hoạt theo giờ phụ thuộc tầng trên (OpenClaw cron / tự chạy định kỳ), script này là bộ tính đến hạn không trạng thái + hàng đợi lưu bền.

## Nguồn tham khảo

Lịch đăng → tính đến hạn → giao việc → ghi lại trạng thái là vòng khép kín chuẩn để đưa lịch nội dung ra đăng thật. Tách tầng điều phối và đăng thật:
điều phối là script thuần (test được), đăng thì giao cho publisher của từng nền tảng (phụ thuộc môi trường).
