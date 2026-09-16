---
name: skill-data-tracker
description: >-
  Ghi và phân tích số liệu kênh: (A) snapshot theo ngày (follower, tương tác); (B) xu hướng tăng
  trưởng (tốc độ, đổi nhịp, dự báo mốc); (C) vòng đời bài từ đăng tới suy giảm (bùng nổ nhanh/tăng
  đều/đuôi dài). Dùng khi người dùng nói "ghi số liệu hôm nay", "follower hôm nay", "vòng đời
  bài".
layer: attribute
---

# Ghi số liệu mạng xã hội và phân tích xu hướng

> Ghi snapshot chỉ số mạng xã hội, phân tích xu hướng tăng người theo dõi, bám vòng đời nội dung, lấy dữ liệu chuỗi thời gian để ra quyết định vận hành.

## Vị trí trong tầng dữ liệu

SKILL này là **nền lưu người theo dõi / snapshot chuỗi thời gian** của chuỗi quy kết, nơi duy nhất có thẩm quyền lưu snapshot theo thời gian của số người theo dõi, lượng tương tác và vòng đời nội dung (`outputs/_analytics/snapshots/{profile}/{platform}/{date}.json`).

- **Chỉ lưu snapshot theo thời gian, không lưu sự kiện đăng bài** - metadata mỗi lần đăng (tiêu đề / link / loại / SKILL nguồn) do `skill-publish-log` giữ (`outputs/_analytics/publish-log.json`). Nền này không ghi trùng sự kiện đăng, tránh cùng một dữ kiện nằm ở hai nơi.
- **Bên tiêu thụ (chỉ đọc, không ghi ngược)** - `skill-publish-analytics` chế độ D (quy kết tăng trưởng) và `skill-social-performance-review` (so kỳ trước / xu hướng người theo dõi) lấy snapshot này làm **nguồn có thẩm quyền cho chuỗi thời gian người theo dõi**.

| Nền lưu | Lưu gì | Ai giữ |
|------|--------|--------|
| `outputs/_analytics/snapshots/{profile}/{platform}/{date}.json` | Snapshot theo thời gian của người theo dõi / tương tác (SKILL này) | skill-data-tracker |
| `outputs/_analytics/publish-log.json` | Sự kiện đăng bài | skill-publish-log |

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| mode | Có | record / growth / lifecycle |
| platform | Mode A: Có | Tên nền tảng (Facebook/TikTok/YouTube/Zalo...) |
| followers | Mode A: Có | Số người theo dõi hiện tại |
| total_likes | Mode A: Không | Tổng lượt thích |
| total_posts | Mode A: Không | Tổng số bài/video |
| post_snapshots | Mode A: Không | Dữ liệu từng bài gần đây (dùng để bám vòng đời) |
| post_title | Mode C: Có | Tiêu đề hoặc mã định danh bài cần bám |
| time_range | Mode B: Không | Cửa sổ phân tích (mặc định 30 ngày gần nhất) |

## Đầu ra

### Mode A - Ghi snapshot

```markdown
# Bản ghi snapshot số liệu
- Ngày: {date} | Nền tảng: {platform} | Profile: {profile_name}

## Chỉ số kênh
| Chỉ số | Giá trị hiện tại | Lần ghi trước | Thay đổi |
|------|--------|---------|------|

## Snapshot bài viết (nếu có)
| Tiêu đề | Ngày đăng | Thích | Lưu | Bình luận | Chia sẻ |

Snapshot đã lưu tại: outputs/_analytics/snapshots/{profile}/{platform}/{date}.json
```

### Mode B - Xu hướng tăng trưởng

```markdown
# Phân tích xu hướng tăng trưởng
- Nền tảng: {platform} | Khoảng: {start} → {end} | Điểm dữ liệu: {count}

## Xu hướng tăng người theo dõi
| Ngày | Người theo dõi | Tăng trong ngày | Tỉ lệ tăng trong ngày |

## Chỉ số then chốt
- Tăng trung bình ngày/tuần | Hướng xu hướng: tăng tốc/ổn định/chậm lại
- Mức tăng cao nhất/thấp nhất trong một ngày
- Dự báo mốc: giữ tốc độ này, sau {X} ngày sẽ vượt {milestone} người theo dõi
- Insight xu hướng: {phân tích lý do tăng tốc/chậm lại và đề xuất}
```

### Mode C - Vòng đời nội dung

```markdown
# Phân tích vòng đời nội dung
- Bài: {post_title} | Đăng: {published_at} | Nền tảng: {platform}

## Dữ liệu vòng đời
| Ngày thứ | Ngày | Thích | Lưu | Bình luận | Chia sẻ | Tăng trong ngày |
(mỗi dòng một mốc Day 0 / 1 / 3 / 7 / 14 / 30)

## Phân loại và insight
- Loại: bùng nổ nhanh/tăng đều/đuôi dài | Ngày đỉnh: Day {peak} | Chu kỳ bán rã: {days} ngày
- Căn cứ phân loại và gợi ý chiến lược tiếp theo
```

## Lưu trữ dữ liệu

Đường dẫn file snapshot: `outputs/_analytics/snapshots/{profile}/{platform}/{date}.json`

```json
{
  "date": "2026-07-22",
  "platform": "tiktok",
  "profile": "Nhà sáng tạo công nghệ",
  "account_metrics": {
    "followers": 5200,
    "total_likes": 42000,
    "total_posts": 89
  },
  "post_snapshots": [
    {
      "post_id": "người dùng cung cấp hoặc tự đánh số",
      "title": "tiêu đề bài",
      "published_at": "2026-07-20",
      "likes": 350,
      "collects": 120,
      "comments": 28,
      "shares": 15
    }
  ]
}
```

## Các bước thực thi

Đọc/ghi snapshot, tính tỉ lệ tăng, trung bình trượt, ngoại suy mốc và phân loại vòng đời đều do `scripts/track.py`
làm theo cách xác định. LLM lo điền tham số (từ Profile/đầu vào người dùng), đọc JSON script trả về, viết đề xuất tăng trưởng.
**Đừng tự tính tỉ lệ tăng, đừng nhẩm trung bình trượt, đừng sửa tay file JSON snapshot.**

### Mode A - Ghi snapshot

1. Lấy chỉ số từ Profile (`identity.md` lấy tên profile, `platforms.md` lấy nền tảng) hoặc từ đầu vào người dùng; trường nào thiếu thì hỏi một lần.
2. Gọi script (mỗi ngày một snapshot, cùng ngày thì ghi đè; tự tính delta so với snapshot trước):

```bash
python3 skills/openclaw/skill-data-tracker/scripts/track.py snapshot --profile "Nhà sáng tạo công nghệ" --platform tiktok \
  --followers 5200 --total-likes 42000 --total-posts 89 [--date 2026-07-22] \
  [--posts du-lieu-tung-bai.json]   # --posts la mang, gom post_id/title/published_at/likes/collects/comments/shares
```

3. Hiển thị `snapshot` + `delta_vs_last` + đường dẫn lưu mà script trả về.

### Mode B - Xu hướng tăng trưởng

```bash
python3 skills/openclaw/skill-data-tracker/scripts/track.py trend --profile "Nhà sáng tạo công nghệ" --metric followers \
  [--platform tiktok] [--since 2026-07-01] [--until 2026-07-31]
```

Script trả về: mức tăng và tỉ lệ tăng từng ngày, trung bình trượt 7 ngày, `trend_direction` (tăng tốc/ổn định/chậm lại),
`milestone` + `milestone_eta_days` (≤30 ngày, vượt ngưỡng trả null), `warning` (<3 điểm là không đủ mẫu).
LLM dựa vào đó viết insight xu hướng và đề xuất gắn với khán giả (có Profile thì đọc `audience.md`).

### Mode C - Vòng đời nội dung

```bash
python3 skills/openclaw/skill-data-tracker/scripts/track.py lifecycle --profile "Nhà sáng tạo công nghệ" \
  --platform tiktok --post-title "Đồ cắm trại" --metric likes
```

Script dựng lại chuỗi thời gian của bài qua các snapshot, trả về mức tăng từng ngày, `peak_day`, `half_life_days`,
`lifecycle_type` (bùng nổ nhanh/tăng đều/đuôi dài/không đủ dữ liệu). LLM theo loại đó viết chiến lược nội dung tiếp theo.

### Xuất view quy kết tăng trưởng

Ghi snapshot xong thì sinh view dẫn xuất mà `skill-publish-analytics` chế độ D cần; đừng tự tay nuôi thêm một sổ người theo dõi khác:

```bash
python3 skills/openclaw/skill-data-tracker/scripts/track.py export-followers
```

Mặc định gộp toàn bộ Profile và nền tảng vào `outputs/_analytics/follower-log.json`; có thể lọc bằng `--profile` hoặc `--platform`.

## Nhận biết Profile

**Khi có Profile:**
- Đọc `identity.md` lấy tên profile, dùng làm tên thư mục snapshot
- Đọc `platforms.md` để tự điền tham số platform, hỗ trợ ghi nhiều nền tảng cùng lúc
- Đọc `audience.md` để đề xuất tăng trưởng gắn với khán giả trong phần phân tích
- Thư mục snapshot tách theo profile/platform: `outputs/_analytics/snapshots/{profile_name}/{platform}/`

**Khi không có Profile:**
- Yêu cầu người dùng nêu rõ tham số platform
- Thư mục snapshot dùng "default": `outputs/_analytics/snapshots/default/{platform}/`
- Phân tích tăng trưởng không kết luận gì về khán giả
- Ghi chú thêm "cung cấp Profile sẽ tự gắn thông tin nền tảng và kênh"

## Quy tắc

1. **Không sửa, không xoá** - file snapshot đã có chỉ đọc, ghi lại cùng ngày cùng nền tảng là trường hợp ghi đè duy nhất được phép
2. **Mỗi ngày một snapshot** - mỗi nền tảng tối đa một snapshot trong ngày, ghi lại trong ngày sẽ đè dữ liệu hôm đó
3. **Tối thiểu 3 điểm dữ liệu** - tính tỉ lệ tăng cần ít nhất 3 điểm, thiếu thì báo cảnh báo chứ không phán xu hướng suông
4. **Dự báo không quá 30 ngày** - dự báo mốc dựa trên ngoại suy xu hướng gần đây, không quá 30 ngày để tránh gây hiểu sai
5. **Minh bạch nguồn dữ liệu** - mọi chỉ số đến từ đầu vào người dùng hoặc file snapshot, không bịa số, không giả định chỉ số chưa được cung cấp

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
