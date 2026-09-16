---
name: skill-short-link
description: >-
  Gắn tham số UTM (nguồn/kênh/chiến dịch) vào link nội dung/quảng cáo rồi rút gọn qua dịch vụ công
  khai không cần key để theo dõi nguồn truy cập và hiệu quả campaign từ Facebook, TikTok, Zalo.
  Dùng khi người dùng nói "rút gọn link", "tạo short link", "link UTM", "link theo dõi",
  "tinyurl".
layer: publish
---

# Short link + theo dõi UTM

> Gắn tham số theo dõi UTM vào link rồi rút gọn, để đo hiệu quả kéo traffic của từng nền tảng. Chạy `scripts/shortlink.py` (thuần thư viện chuẩn, không phụ thuộc,
> short link dùng dịch vụ công khai không cần key: TinyURL / is.gd / v.gd).

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| URL | Có | Link landing page/sản phẩm/biểu mẫu |
| source | Bắt buộc khi gắn UTM | Nền tảng nguồn, ví dụ facebook/tiktok/zalo |
| medium | Bắt buộc khi gắn UTM | Kênh, ví dụ social/video/cpc |
| campaign | Bắt buộc khi gắn UTM | Tên chiến dịch, ví dụ tet/newproduct |

## Thực thi

Đường dẫn script (tính từ gốc dự án): `skills/openclaw/skill-short-link/scripts/shortlink.py` (mỗi subcommand đều có `-h`).

```bash
# Làm một phát: gắn UTM + rút gọn (hay dùng nhất)
python <skill>/scripts/shortlink.py both --url "https://shop.example.com/item/123" \
  --source facebook --medium social --campaign tet

# Chỉ gắn tham số UTM
python <skill>/scripts/shortlink.py utm --url "https://a.com/p" \
  --source tiktok --medium video --campaign summer --content "Video A"

# Chỉ rút gọn
python <skill>/scripts/shortlink.py short --url "https://a.com/very/long/url" --provider tinyurl
```

- Dịch vụ short link mặc định là `tinyurl` (ổn nhất, nhận mọi URL); cũng có thể dùng `--provider isgd`/`vgd` (hỗ trợ `--alias` để tự đặt mã ngắn,
  nhưng chặn một số tên miền).
- Chạy nhiều nền tảng thì nên **mỗi nền tảng một short link riêng** (khác source), như vậy trong báo cáo mới tách được traffic theo nền tảng.

## Quy tắc

1. Mỗi kênh chạy sinh một short link riêng (phân biệt bằng utm_source), không thì không quy được traffic về từng nền tảng.
2. Đặt tên campaign theo một quy ước thống nhất (ví dụ `tet`, `tên-sản-phẩm-tháng`) để sau này gộp số liệu cho dễ.
3. `--content` dùng để A/B nhiều biến thể trong cùng chiến dịch (ví dụ "Video A"/"Bài ảnh B").
4. Đây là dịch vụ short link công khai của bên thứ ba; chiến dịch quan trọng nên tự dựng tên miền rút gọn riêng (SKILL này chỉ để ra link cho nhanh).

## Nguồn tham khảo

UTM là bộ tham số theo dõi nguồn dùng chung cho GA và các nền tảng phân tích (utm_source/medium/campaign/term/content).
Short link đi qua API công khai không cần key của TinyURL / is.gd / v.gd. Viết thuần bằng urllib.
