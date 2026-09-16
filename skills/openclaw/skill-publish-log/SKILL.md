---
name: skill-publish-log
description: >-
  Quản lý nhật ký đăng: ghi từng lần đăng (nền tảng, tiêu đề, link, thời gian, số liệu ban đầu),
  tra cứu theo nền tảng/từ khoá, thống kê số bài và tổng tương tác để hậu kiểm. Dùng khi người
  dùng nói "ghi lại bài vừa đăng", "tháng này đăng bao nhiêu", "lịch sử đăng", "lần trước đăng
  gì".
layer: attribute
---

# Quản lý nhật ký đăng bài

> Ghi nhận, tra cứu, thống kê thông tin mỗi lần đăng nội dung mạng xã hội, làm nền dữ liệu cho hậu kiểm và quy kết.

## Định vị tầng dữ liệu

SKILL này là **nền dữ liệu sự kiện đăng bài** của chuỗi quy kết, nơi lưu duy nhất và có thẩm quyền là `outputs/_analytics/publish-log.json` (nền tảng / tiêu đề / link / thời gian / số liệu ban đầu / tag / SKILL nguồn của mỗi lần đăng).

- **Chỉ lưu sự kiện đăng bài, không lưu chuỗi thời gian người theo dõi** - snapshot theo thời gian của số người theo dõi và lượng tương tác do `skill-data-tracker` giữ (`outputs/_analytics/snapshots/`). Nền này không ghi lặp chuỗi thời gian đó, tránh cùng một dữ kiện nằm ở hai nơi.
- **Bên tiêu thụ (chỉ đọc, không ghi ngược)** - `skill-publish-analytics` (khung giờ / tag / loại / quy kết tăng trưởng) và `skill-social-performance-review` (hậu kiểm hàng tháng) đọc nền này để quy kết.

| Nền dữ liệu | Lưu gì | Ai giữ |
|------|--------|--------|
| `outputs/_analytics/publish-log.json` | Sự kiện đăng bài (SKILL này) | skill-publish-log |
| `outputs/_analytics/snapshots/{profile}/{platform}/{date}.json` | Snapshot chuỗi thời gian người theo dõi / tương tác | skill-data-tracker |

## Đầu vào

Người dùng cung cấp một trong các thông tin sau trong prompt:

### Chế độ ghi nhận (ghi)
- **Bắt buộc**: nền tảng, tiêu đề (hoặc tóm tắt nội dung)
- **Tuỳ chọn**: link, thời gian đăng (mặc định là thời điểm hiện tại), loại nội dung (ảnh-chữ/video/livestream), số liệu ban đầu (lượt xem/like/bình luận/chia sẻ), SKILL liên quan (nội dung do SKILL nào tạo), ghi chú

### Chế độ tra cứu (đọc)
- Tra theo khoảng thời gian: "tháng này đăng gì" "một tuần gần đây"
- Lọc theo nền tảng: "trên Facebook đã đăng những gì"
- Tìm theo từ khoá: "nhật ký đăng về AI"
- Xem bản ghi gần nhất: "lần trước đăng gì"

### Chế độ thống kê (tổng hợp)
- Thống kê theo thời gian: "tháng này đăng bao nhiêu bài"
- Thống kê theo nền tảng: "số bài đăng từng nền tảng"
- Tổng hợp số liệu: "xếp hạng tổng tương tác"

## Đầu ra

### Chế độ ghi nhận

Xác nhận ghi thành công, trả về tóm tắt bản ghi:

```
Đã ghi nhận lần đăng:
- Nền tảng: Facebook
- Tiêu đề: "5 công cụ AI đang bị đánh giá thấp"
- Thời gian: 2026-07-22 14:30
- Link: https://...
- Mã bản ghi: #042
```

### Chế độ tra cứu

Trả về danh sách bản ghi khớp (dạng bảng):

```markdown
| # | Ngày | Nền tảng | Tiêu đề | Link | Loại |
|---|------|------|------|------|------|
| 042 | 07-22 | Facebook | 5 công cụ AI đang bị đánh giá thấp | [link] | ảnh-chữ |
| 041 | 07-20 | TikTok | Thực hành dựng video bằng AI | [link] | video |
```

### Chế độ thống kê

Trả về thông tin thống kê có cấu trúc:

```markdown
## Thống kê đăng bài tháng này (2026-07)

- Tổng số bài: 12
- Theo nền tảng: Facebook 5 | TikTok 4 | YouTube 2 | Zalo 1
- Theo loại: ảnh-chữ 7 | video 4 | livestream 1
- Tổng tương tác: like 2.340 | bình luận 189 | chia sẻ 67
```

## Định dạng lưu trữ

Dữ liệu lưu ở `outputs/_analytics/publish-log.json`, cấu trúc như sau:

```json
{
  "version": "1.0",
  "entries": [
    {
      "id": 42,
      "platform": "Facebook",
      "title": "5 công cụ AI đang bị đánh giá thấp",
      "url": "https://...",
      "type": "ảnh-chữ",
      "published_at": "2026-07-22T14:30:00+07:00",
      "logged_at": "2026-07-22T14:35:00+07:00",
      "initial_metrics": {
        "views": null,
        "likes": null,
        "comments": null,
        "shares": null
      },
      "skill_source": "skill-card-xiaohongshu",
      "profile": "my-xhs-account",
      "tags": ["AI", "gợi ý công cụ"],
      "notes": ""
    }
  ]
}
```

**Giải thích trường:**
- `id`: mã tự tăng
- `platform`: nền tảng đăng
- `title`: tiêu đề hoặc tóm tắt nội dung
- `url`: link bài đăng (có thể để trống)
- `type`: loại nội dung (ảnh-chữ/video/livestream/bài viết)
- `published_at`: thời gian đăng thực tế
- `logged_at`: thời gian ghi vào nhật ký
- `initial_metrics`: số liệu ngay lúc đăng (cho phép trống một phần)
- `skill_source`: SKILL đã tạo ra nội dung (có thể để trống)
- `profile`: Profile kênh liên quan (có thể để trống)
- `tags`: tag nội dung
- `notes`: ghi chú

## Các bước thực hiện

Đọc/ghi, tự tăng id, lọc, tổng hợp đều do `scripts/log.py` làm một cách tất định (ghi nguyên tử, an toàn khi chia cho 0).
LLM chỉ lo hiểu ý người dùng -> dựng tham số -> đọc JSON script trả về -> sinh đầu ra cho người đọc.
**Đừng sửa JSON thủ công, đừng nhẩm thống kê trong đầu.**

1. **Xác định chế độ thao tác**: từ prompt của người dùng nhận ra là ghi nhận, tra cứu hay thống kê
2. **Thiếu thông tin thì hỏi lại**: chế độ ghi nhận cần tối thiểu nền tảng và tiêu đề, thiếu thì nhắc bổ sung
3. **Gọi script** (file dữ liệu chưa có thì script tự khởi tạo cấu trúc rỗng):

```bash
# Ghi nhận (id tự tăng, ghi nguyên tử trở lại outputs/_analytics/publish-log.json)
python3 skills/openclaw/skill-publish-log/scripts/log.py record --platform Facebook --title "tiêu đề" \
  --type ảnh-chữ --url "https://..." --views 1000 --likes 120 \
  --comments 30 --shares 10 --tags "AI,gợi ý công cụ" [--published-at "thời gian ISO"] \
  [--skill-source skill-xxx] [--profile "tên Profile"] [--notes "ghi chú"]

# Tra cứu (lọc theo nền tảng/thời gian/từ khoá/Profile, --latest lấy bản ghi gần nhất)
python3 skills/openclaw/skill-publish-log/scripts/log.py query --platform Facebook --since 2026-07-01 \
  [--until 2026-07-31] [--keyword AI] [--profile "tên Profile"] [--latest] [--limit N]

# Thống kê (gom theo platform/type/month: số lượng + tổng tương tác + điểm tổng hợp trung bình)
python3 skills/openclaw/skill-publish-log/scripts/log.py stat --by platform --since 2026-07-01
```

4. **Đọc kết quả**: chuyển JSON sang định dạng bảng/tóm tắt ở mục "Đầu ra" của SKILL.md rồi trình cho người dùng;
   trường `warning` script trả về (mẫu chưa đủ) nếu khác rỗng thì phải truyền lại nguyên văn.

## Nhận biết Profile

### Khi có Profile

- Đọc `platforms.md` để tự điền trường `platform` (suy ra từ nền tảng chính)
- Đọc `identity.md` lấy tên kênh, tự gắn vào trường `profile`
- Khi thống kê có thể tổng hợp theo chiều Profile (kênh)
- Khi tra cứu mặc định chỉ hiện bản ghi của Profile hiện tại

### Khi không có Profile

- `platform` phải do người dùng chỉ định rõ
- Trường `profile` để trống
- Thống kê và tra cứu phủ toàn bộ bản ghi, không lọc theo kênh
- Ghi chú thêm: "Nếu cung cấp Profile kênh, có thể tự gắn nền tảng và thống kê nhóm theo kênh"

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
