---
name: skill-post-scorer
description: >-
  Chấm tiềm năng tương tác của bản nháp bài đăng dựa trên hiệu quả lịch sử, xuất thẻ điểm 5 chiều,
  gợi ý sửa. Dùng khi người dùng nói "chấm điểm bài", "bài này có viral không", "đánh giá bản
  nháp". Đề tài chưa làm → skill-topic-evaluator; hậu kiểm sau đăng →
  skill-social-performance-review.
layer: attribute
---

# Chấm điểm hiệu quả bài đăng

> Chấm tiềm năng tương tác cho bản nháp bài đăng mạng xã hội, xuất thẻ điểm có cấu trúc dựa trên dữ liệu hiệu quả lịch sử.

**Nạp xong là bắt đầu quy trình chấm điểm ngay, không tóm tắt, không chờ xác nhận.**

## Đầu vào

Người dùng đưa bản nháp bài đăng trong prompt, hỗ trợ các dạng sau:

- **Nội dung text**: dán thẳng bài viết
- **Đường dẫn file**: trỏ tới file nháp trong `outputs/`
- **Chỉ định nền tảng**: tuỳ chọn, nêu nền tảng mục tiêu (Facebook, TikTok, YouTube Shorts, Zalo, blog/website...)

Ví dụ prompt:
```
Execute /skill-post-scorer
Bài:
Mất 3 năm tôi mới hiểu ra một điều:
Nội dung hay nhất không phải "viết" ra, mà là "chắt" ra.
Sau đây là 5 cách chắt nội dung tôi đúc kết được...
```

## Đầu ra

Xuất thẻ điểm dạng khối mã:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Thẻ điểm hiệu quả bài đăng
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Độ mạnh hook        ██████████  8/10
Khớp voice          ███████░░░  7/10
Mật độ giá trị      ████████░░  8/10
Cấu trúc/trình bày  ███████░░░  7/10
Sẵn sàng đăng       ██████░░░░  6/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tổng điểm           36/50
Kết luận            Đáng đăng, nên tối ưu hook
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Gợi ý cải thiện:
1. [chiều yếu nhất] gợi ý sửa cụ thể
2. ...
```

## Các bước thực thi

### Bước 1: lấy bài

Đọc nội dung bài người dùng dán. Nếu prompt không có text bài, chủ động hỏi người dùng đưa vào.

### Bước 2: nạp dữ liệu chấm điểm

Lấy dữ liệu hiệu quả theo thứ tự ưu tiên:

1. **Dữ liệu lịch sử trong Profile**: kiểm dấu `=== EASEL ACCOUNT PROFILE ===`, đọc dữ liệu bài cũ ở đường dẫn mà `performance_data` trỏ tới
2. **Dữ liệu người dùng đưa**: hỏi người dùng có file xuất dữ liệu bài cũ không (trung tâm nhà sáng tạo/trang quản trị của từng nền tảng đều xuất được CSV/Excel, hoặc gom thành mảng JSON)
3. **Chuẩn chung**: không có gì ở trên thì dùng dữ liệu chuẩn trong `references/fallback-benchmarks.md`

### Bước 3: phân tích bài hiệu quả cao

> **Điểm tương tác và lọc Top 10% giao cho script, LLM chỉ đúc rút đặc trưng.** Do
> [`scripts/score.py`](scripts/score.py) đảm nhiệm (tái dùng
> `engagement_score` của `../../shared/scripts/social_stats.py`).

Khi có dữ liệu lịch sử/dữ liệu người dùng, gom bài thành mảng JSON (mỗi bản ghi có trường like và comment), rồi gọi:

```bash
python3 skills/openclaw/skill-post-scorer/scripts/score.py top --input history.json
python3 skills/openclaw/skill-post-scorer/scripts/score.py top --input history.json --top-pct 5
```

Script tự động: tính từng bản ghi theo `điểm tương tác = like + comment x 3` (nhận các trường likes/reactions,
comments), sắp giảm dần theo điểm tương tác, tính ngưỡng Top N% và phân bố (trung bình/trung vị/cao nhất/thấp nhất),
cảnh báo khi mẫu quá ít. **Sau khi LLM nhận danh sách bài Top từ script**, đúc rút đặc trưng chung:

- Kiểu hook mở đầu (đặt câu hỏi, số liệu, kể chuyện, phản trực giác)
- Độ dài text và nhịp đoạn
- Đặc trưng trình bày (danh sách, ngắt đoạn, dùng emoji)
- Kiểu kêu gọi hành động (CTA)
- Phân loại chủ đề
- Nhịp câu (dài ngắn xen kẽ, tần suất ngắt câu)

Không có dữ liệu lịch sử thì bỏ qua bước này, dùng thẳng đặc trưng mẫu chung trong `references/fallback-benchmarks.md`.

### Bước 4: chấm 5 chiều

Chấm theo 5 chiều, mỗi chiều 1-10 điểm, tổng 50 điểm.

Tiêu chí chấm chi tiết xem `references/scoring-criteria.md`.

| Chiều | Trọng tâm đánh giá |
|------|----------|
| Độ mạnh hook | Hai câu đầu có chặn được cú lướt, tạo tò mò hay đồng cảm không |
| Khớp voice | Có hợp giọng, persona và thói quen diễn đạt quen thuộc của kênh không |
| Mật độ giá trị | Mỗi đoạn có cho insight cụ thể hay chỉ nói chung chung |
| Cấu trúc/trình bày | Cách trình bày có hợp thói quen đọc của nền tảng mục tiêu không |
| Sẵn sàng đăng | Đăng được ngay hay còn phải trau chuốt, bổ sung |

**Kỷ luật chấm điểm:**
- Chấm thật, không nịnh
- Trừ khi bài đúng là khớp đặc trưng của nhóm Top 10%, không cho quá 8 điểm
- Có dữ liệu thật thì nói bằng dữ liệu, không có thì ghi rõ "dựa trên chuẩn chung"

### Bước 5: xuất thẻ điểm

Xuất thẻ điểm theo đúng định dạng ở phần "Đầu ra" bên trên, gồm:
- Điểm 5 chiều (kèm thanh tiến độ trực quan)
- Tổng điểm và kết luận
- Gợi ý sửa cụ thể cho chiều yếu nhất

Tiêu chuẩn kết luận:
- **40-50**: xuất sắc, đăng luôn
- **30-39**: đáng đăng, nên tối ưu các điểm yếu đã đánh dấu
- **20-29**: cần sửa, tập trung cải thiện 1-2 chiều yếu nhất
- **< 20**: nên viết lại

> Thang chia chi tiết hơn (kèm cách phát biểu kết luận ở từng mốc ranh giới) xem `references/fallback-benchmarks.md`, hai nơi cùng một chuẩn.

### Bước 6: đề nghị viết lại

Xuất thẻ điểm xong thì chủ động đề nghị:

> Bạn có muốn tôi viết lại phần bị chấm thấp nhất không?

Nếu người dùng đồng ý, viết lại có trọng điểm cho chiều yếu nhất, giữ nguyên phần còn lại, viết xong chấm lại để đối chiếu.

## Nhận biết Profile

### Có Profile

- Đọc trường `voice` / `tone`, dùng làm chuẩn đánh giá "Khớp voice"
- Đọc trường `platform`, chỉnh quy tắc thích ứng nền tảng của "Cấu trúc/trình bày"
- Đọc file dữ liệu lịch sử mà trường `performance_data` trỏ tới, dùng dữ liệu thật thay chuẩn chung
- Đọc trường `topics` / `niche`, đánh giá nội dung có nằm trong định vị của kênh không

### Không Profile

- "Khớp voice" hạ xuống thành đánh giá độ dễ đọc chung
- "Cấu trúc/trình bày" dùng thực hành tốt chung của mạng xã hội
- Dùng dữ liệu chuẩn trong `references/fallback-benchmarks.md`
- Cuối thẻ điểm ghi chú: "nếu cung cấp Profile của kênh (kèm dữ liệu hiệu quả lịch sử), điểm sẽ chính xác hơn"
