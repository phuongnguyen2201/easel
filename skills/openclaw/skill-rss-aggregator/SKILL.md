---
name: skill-rss-aggregator
description: >-
  Tổng hợp feed RSS/Atom của blogger, báo, Newsletter: kéo bài mới, lọc theo từ khoá, khung thời
  gian, bỏ trùng, xếp theo thời gian, ra tóm tắt đề tài/tin. Dùng khi người dùng nói "RSS",
  "feed", "Newsletter", "theo dõi blogger", "có bài gì mới". Thuần thư viện chuẩn, không phụ thuộc
  ngoài.
layer: discover
---

# Tổng hợp RSS / Newsletter

> Gom bản cập nhật mới nhất của một loạt nguồn đã đăng ký thành bản tóm tắt, dùng để chọn đề tài hằng ngày và theo dõi tin tức. Chạy qua `scripts/rss_digest.py`
> (parse RSS 2.0 / Atom thuần thư viện chuẩn), không phụ thuộc bên thứ ba.

> Bảng trend toàn mạng xem skill-trending-topics; tin tức ngành xem skill-news-intelligence; SKILL này tập trung
> tổng hợp cập nhật từ **nguồn do người dùng tự chọn**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Nguồn đăng ký | Có | `--url` một hoặc nhiều, hoặc `--feeds` file danh sách (mỗi dòng một URL RSS/Atom) |
| Từ khoá | Tuỳ chọn | Chỉ giữ mục có tiêu đề/tóm tắt khớp (ngăn cách bằng dấu phẩy) |
| Khung thời gian | Tuỳ chọn | Chỉ giữ N ngày gần nhất |

## Thực hiện

Đường dẫn script (tương đối so với gốc dự án): `skills/openclaw/skill-rss-aggregator/scripts/rss_digest.py`.

```bash
# Gom nhiều nguồn, lọc AI/mô hình lớn, 7 ngày gần nhất, xuất tóm tắt Markdown
python <skill>/scripts/rss_digest.py fetch --feeds feeds.txt \
  --keyword AI,LLM,Agent --since 7 -o "outputs/<chủ đề>/digest.md"

# Xem nhanh một nguồn
python <skill>/scripts/rss_digest.py fetch --url https://example.com/feed.xml --limit 20
```

`feeds.txt` mỗi dòng một URL (dòng mở đầu bằng `#` là chú thích). Đầu ra `.md` thì tự động Markdown, còn lại là JSON.

## Dùng kết quả thế nào

1. Bản tóm tắt tổng hợp → chọn đề tài từ đó, nạp cho skill-topic-evaluator để đánh giá tính khả thi, skill-content-matrix để xếp đề tài.
2. Lọc từ khoá để khoá vào ngách, chỉ xem các cập nhật liên quan tới kênh.
3. Chạy định kỳ (kết hợp hẹn giờ của OpenClaw) để làm "bản tin hằng ngày/hằng tuần".

## Nhận biết Profile

- Có Profile: từ khoá mặc định lấy theo từ khoá ngách trong `identity.md`; chỉ đẩy các cập nhật liên quan tới định vị của kênh.
- Không có Profile: không lọc hoặc lọc theo từ khoá người dùng đưa, tổng hợp toàn bộ.

## Quy tắc

1. Khi không tìm được RSS của một nền tảng, nhiều site/trang WeChat OA có thể dùng RSSHub để sinh RSS, nhắc người dùng cấu hình.
2. Mục không có pubDate thì không bị khung thời gian xoá nhầm (giữ lại, xếp cuối).
3. Bản tóm tắt chỉ liệt kê tiêu đề/nguồn/ngày/đoạn trích và link, không kéo toàn văn (tôn trọng bản quyền).
4. Nguồn kéo lỗi thì bỏ qua và báo lại, không làm gián đoạn cả lượt tổng hợp.

## Nguồn tham khảo

RSS 2.0 / Atom là định dạng đăng ký XML chuẩn; site không có RSS thường dùng RSSHub để sinh. SKILL này dùng stdlib
xml.etree để parse (tương thích cả hai định dạng + làm sạch HTML + ngày RFC822/ISO), lọc từ khoá/khung thời gian + bỏ trùng và sắp xếp.
