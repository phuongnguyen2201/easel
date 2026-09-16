---
name: skill-publish-checklist
description: >-
  Kiểm đủ trước khi đăng: rà tiêu đề, ảnh bìa, hashtag, định dạng, nhãn tuân thủ, link, CTA. Dùng
  khi người dùng nói "kiểm tra xem đăng được chưa", "checklist trước khi đăng", "còn thiếu gì
  không". skill-quality-gate kiểm duyệt tuân thủ sâu và chấm chất lượng; checklist chỉ kiểm nhanh.
layer: publish
---

# Kiểm tính đầy đủ trước khi đăng

> Chốt chặn cuối trước khi đăng, rà từng mục xem nội dung đã đủ chưa, chặn các lỗi sơ đẳng như thiếu tiêu đề, thiếu ảnh bìa, thiếu hashtag.

## Khác gì các SKILL còn lại

| SKILL | Định vị | Độ sâu kiểm |
|---|---|---|
| **publish-checklist** (SKILL này) | Kiểm tính đầy đủ - "có sót gì không" | Nông, tick từng mục |
| skill-quality-gate | Tuân thủ sâu + soát chất lượng | Sâu, chấm điểm + trả về làm lại |
| skill-persona-check | Nhất quán persona | Chiều phong cách/tông giọng |
| skill-risk-scanner | Độ nguyên bản + bản quyền | Chiều đạo văn/vi phạm |

## Đầu vào

Người dùng đưa nội dung sắp đăng, nhận các dạng sau:

- **Đường dẫn thư mục sản phẩm**: trỏ tới thư mục sản phẩm đầy đủ trong `outputs/<chủ đề>/` (gồm meta.json, phần thân, ảnh...)
- **Một bài viết dạng text**: dán thẳng nội dung bài
- **Hỗn hợp**: bài viết + đường dẫn ảnh + meta.json

Có thể nêu nền tảng đích (Xiaohongshu, Douyin, Weibo, WeChat OA, LinkedIn, X...), không nêu thì kiểm theo bộ chung.

## Đầu ra

Xuất báo cáo kiểm có cấu trúc, định dạng JSON:

```json
{
  "status": "ready | not_ready",
  "score": "7/10",
  "platform": "tên nền tảng hoặc generic",
  "checklist": [
    {
      "item": "tên mục kiểm",
      "status": "pass | fail | warn",
      "detail": "mô tả cụ thể"
    }
  ],
  "blocking_issues": ["vấn đề bắt buộc sửa mới đăng được"],
  "warnings": ["vấn đề nên sửa nhưng không chặn đăng"],
  "summary": "tóm tắt một câu: đăng được / còn thiếu gì"
}
```

- `status` là `ready`: mọi mục bắt buộc đều đạt, đăng được
- `status` là `not_ready`: còn vấn đề chặn đăng, liệt kê các mục phải sửa

## Các bước thực thi

### Step 1 - Nhận dạng hình thái nội dung và nền tảng đích

1. Xác định đầu vào là thư mục sản phẩm hay một bài viết rời
2. Nếu có `meta.json`, đọc các trường `platform`, `type` (ảnh-chữ/video), `title`, `tags`...
3. Nếu có ngữ cảnh Profile, đọc trường `platform` để chốt nền tảng đích
4. Không xác định được nền tảng thì dùng checklist chung

### Step 2 - Rà từng mục (checklist chung)

Rà theo các chiều sau, gắn nhãn pass / fail / warn:

**Mục bắt buộc (fail là chặn đăng):**

| # | Mục kiểm | Kiểm cái gì |
|---|---|---|
| 1 | **Tiêu đề** | Có tiêu đề chưa; độ dài tiêu đề có trong giới hạn nền tảng không |
| 2 | **Phần thân/nội dung** | Có nội dung thực chất không; có bị rỗng hay còn placeholder không |
| 3 | **Ảnh bìa/khung đầu** | Bài ảnh-chữ đã có ảnh bìa chưa; video đã có khung bìa chưa |
| 4 | **Định dạng đủ** | Cấu trúc Markdown có đủ không; ảnh tham chiếu có hợp lệ không; link có mở được không |

**Mục khuyến nghị (warn nhưng không chặn):**

| # | Mục kiểm | Kiểm cái gì |
|---|---|---|
| 5 | **Hashtag** | Có hashtag chưa; số lượng có nằm trong khoảng hợp lý 3-10 không |
| 6 | **CTA (kêu gọi hành động)** | Có câu dẫn tương tác không (thích, lưu, theo dõi, bình luận...) |
| 7 | **Link còn dùng được** | URL trong bài có đúng định dạng không |
| 8 | **Quy cách ảnh** | Kích thước ảnh có hợp yêu cầu nền tảng không (dọc/ngang/vuông) |
| 9 | **Độ dài bài** | Số chữ có nằm trong khoảng nền tảng khuyến nghị không |
| 10 | **Dùng emoji** | Có emoji vừa đủ để dễ đọc không (tuỳ nền tảng) |

### Step 3 - Kiểm riêng theo nền tảng (thêm vào khi biết nền tảng)

Tuỳ nền tảng đích mà bổ sung mục kiểm:

**Xiaohongshu:**
- Số thẻ có nằm trong 3-9 tấm không
- Chữ trên mỗi thẻ có ≤ 80 chữ không
- Có caption (bài viết kèm khi đăng) không
- Ảnh bìa có phải 3:4 dọc không (1080×1440, tỉ lệ chuẩn của Xiaohongshu)

**Douyin/Video Channels:**
- Thời lượng video có trong giới hạn không
- Có phụ đề không
- Ảnh bìa đã có tiêu đề đủ hút chưa

**Weibo:**
- Phần thân có ≤ 2000 chữ không
- Định dạng hashtag chủ đề có đúng không (#chủ đề#)

**WeChat OA:**
- Có tóm tắt/lời dẫn không
- Có link bài gốc không
- Kích thước ảnh bìa có phải 2.35:1 không

**X/Twitter:**
- Mỗi bài có ≤ 280 ký tự không
- Có cần tách thành thread không

**LinkedIn:**
- Phần thân có ≤ 3000 ký tự không
- Có CTA mang tính chuyên môn không

> Số chữ/kích thước của các nền tảng trên là **giá trị tham khảo (as of 2026-07)**, lấy quy tắc mới nhất của nền tảng làm chuẩn (ví dụ X Premium đã nới trần ký tự mỗi bài).

### Step 4 - Sinh báo cáo kiểm

1. Gộp kết quả của toàn bộ mục kiểm
2. Đếm số mục đạt / tổng số, tính điểm mức hoàn chỉnh
3. Tách vấn đề chặn đăng (blocking_issues) khỏi khuyến nghị (warnings)
4. Chốt `status`: có bất kỳ mục fail thì là `not_ready`, còn lại là `ready`
5. Viết tóm tắt một câu

### Step 5 - Xuất kết luận và đề xuất

- `ready`: báo người dùng đăng được, liệt kê đề xuất tối ưu (nếu có)
- `not_ready`: nêu rõ các mục còn thiếu, chỉ cách bổ sung cụ thể

## Nhận biết Profile

- **Có Profile**: đọc `platforms.md` để chốt nền tảng đích, bật các mục kiểm riêng theo nền tảng; đọc `style.md` để soi phong cách ảnh bìa có khớp không; đọc `identity.md` để kiểm độ đầy đủ của tên kênh và thông tin liên quan
- **Không có Profile**: chỉ kiểm tính đầy đủ theo bộ chung (Step 2), bỏ qua phần riêng theo nền tảng; trong báo cáo ghi chú "đưa Profile của kênh (kèm thông tin nền tảng) sẽ bật được các mục kiểm riêng theo nền tảng"

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
