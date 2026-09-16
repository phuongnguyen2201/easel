---
name: skill-social-performance-review
description: >-
  Hậu kiểm hiệu quả mạng xã hội theo tháng trên Facebook/TikTok/YouTube/Zalo: bài tốt/kém nhất,
  trụ cột, định dạng, đề xuất tháng sau. Dùng khi người dùng nói "hậu kiểm tháng", "tháng này hiệu
  quả sao", "báo cáo tháng", "tổng kết vận hành". skill-publish-analytics quy kết từ nhật ký đăng.
layer: attribute
---

# Hậu kiểm hiệu quả theo tháng

> Phân tích hiệu quả nội dung mạng xã hội tháng trước, tìm ra mô hình hiệu quả và nguyên nhân thất bại, xuất báo cáo hậu kiểm khách hàng đọc được và đề xuất làm được cho tháng sau.

## Định vị tầng dữ liệu

SKILL này là **tầng tiêu thụ** trong chuỗi quy kết, không dựng thêm nền dữ liệu:

- **Nguồn chuẩn của dữ liệu người theo dõi / chuỗi thời gian là nền snapshot `skill-data-tracker`** (`outputs/_analytics/snapshots/`); nền sự kiện đăng bài là `skill-publish-log` (`outputs/_analytics/publish-log.json`). Có dữ liệu nền tương ứng thì ưu tiên lấy ra để so tháng liền kề và xem xu hướng người theo dõi.
- **File tạm và sản phẩm của SKILL này không phải nền dữ liệu** - `outputs/<chủ đề>/.tmp-{tháng}.json` ở giai đoạn 3 là đầu vào đã chuẩn hoá (dùng xong xoá ngay), `context/best-performers.md`, `context/review-history.md` là phần đọng lại của hậu kiểm, đều không lưu trùng chuỗi thời gian người theo dõi hay bản thân sự kiện đăng bài.
- Khi thiếu dữ liệu nền, lùi về đầu vào CSV / ảnh chụp màn hình / lời kể (xem "Chất lượng dữ liệu"), không chặn việc hậu kiểm.

## Đầu vào

Người dùng cung cấp các thông tin sau trong prompt:

- **Tháng hậu kiểm**: dữ liệu của tháng nào
- **Nền tảng**: Xiaohongshu / Douyin / Bilibili / Weibo / WeChat OA (chọn nhiều được)
- **Nguồn dữ liệu** (theo thứ tự ưu tiên):
  - Xuất CSV (Xiaohongshu Creator Center / Douyin Creator Service Platform / Bilibili Creative Center / Weibo Data Center)
  - Ảnh chụp màn hình (trang tổng quan số liệu trong backend từng nền tảng)
  - Lời kể (người dùng mô tả bài nào tốt/kém)
- **Bối cảnh kinh doanh** (tuỳ chọn): trong tháng có sự kiện đặc biệt, khuyến mãi, quảng cáo trả tiền hay không

Prompt ví dụ:
```
Execute /skill-social-performance-review
Tháng: 6/2025
Nền tảng: Xiaohongshu
Dữ liệu: đính kèm ảnh chụp backend
Bối cảnh: giữa tháng 6 có làm một bài tổng hợp chia sẻ đồ tốt
```

## Đầu ra

Báo cáo hậu kiểm tháng có cấu trúc, lưu vào `outputs/<chủ đề>/[tên khách hàng]-social-review-[tháng]-[năm].md`.

Báo cáo gồm: tổng quan tháng, phân tích bài tốt nhất/kém nhất, bóc tách trụ cột nội dung và định dạng, insight chính, đề xuất tháng sau.

Mẫu báo cáo đầy đủ xem `references/report-template.md`.

## Chất lượng dữ liệu

SKILL thích ứng với ba mức chất lượng dữ liệu, thiếu dữ liệu vẫn không dừng phân tích:

| Mức | Nguồn dữ liệu | Độ sâu phân tích |
|------|----------|----------|
| **Đầy đủ** | Xuất CSV + ảnh tổng quan kênh | Chấm từng bài, so sánh chỉ số đầy đủ |
| **Một phần** | Ảnh chụp hoặc danh sách bài Top/Bottom | Phân tích mô hình, ghi rõ chỗ thiếu dữ liệu |
| **Tối thiểu** | Người dùng kể bài nào tốt/kém | Phân tích định tính + đề xuất dựa trên best practice |

Ghi rõ nguồn dữ liệu và mức chất lượng ngay đầu báo cáo.

## Các bước thực hiện

### Giai đoạn 0 - Chuẩn bị môi trường

Đọc các file bối cảnh sau (có thì đọc, không có thì bỏ qua và ghi lại):

- `context/brand-style.md` - trụ cột nội dung, định vị nền tảng, mục tiêu
- `context/content-calendar.md` - lịch đăng tháng trước
- `context/best-performers.md` - các bài hiệu quả cao trong quá khứ
- `context/review-history.md` - xu hướng điểm chấm qua các kỳ
- File mới nhất trong `outputs/<chủ đề>/` - hậu kiểm tháng trước (dùng để so tháng liền kề)

### Giai đoạn 1 - Thu thập thông tin

Thu thập tháng hậu kiểm, nền tảng, nguồn dữ liệu, bối cảnh kinh doanh và mục tiêu trong tháng.

Nếu người dùng chưa chuẩn bị dữ liệu xuất, hướng dẫn các bước xuất:
- **Xiaohongshu**: Creator Center → Data Center → Content Analysis → chọn khoảng thời gian
- **Douyin**: Creator Service Center → Data Dashboard → Content Analysis
- **Bilibili**: Creative Center → Data Center → Video Analysis
- **Weibo**: Weibo Data Center → Content Analysis
- **WeChat OA**: backend WeChat OA → Statistics → Content Analysis

Nếu không xuất được, xin người dùng cung cấp: Top 3 bài + Bottom 3 bài + biến động người theo dõi + bài có kết quả bất ngờ.

### Giai đoạn 2 - Chuẩn hoá dữ liệu

Nhận CSV / ảnh chụp / lời kể, trích đồng nhất: ngày đăng, loại bài, tóm tắt nội dung, lượt tiếp cận, tương tác, lưu/click, chia sẻ, tỉ lệ tương tác.

**Quy tắc làm sạch**:
- Bài chạy quảng cáo trả tiền loại khỏi chuẩn tự nhiên, ghi chú riêng
- Reels/video ngắn có lượt tiếp cận phồng lên tự nhiên, khi so định dạng phải ghi rõ
- Khoảng thời gian không đăng bài ghi riêng

### Giai đoạn 3 - Phân tích hiệu quả

**Trước hết đổ dữ liệu đã chuẩn hoá thành JSON, giao `scripts/review.py` tính toán tất định, rồi bạn mới diễn giải.**
Đừng tự tính tỉ lệ tương tác, đừng nhẩm xếp Top/Bottom, đừng nhẩm so tháng liền kề và điểm có trọng số.

Ghi dữ liệu đã chuẩn hoá ở giai đoạn 2 thành JSON đầu vào (`outputs/<chủ đề>/.tmp-{tháng}.json`):

```json
{
  "month": "2026-06", "platform": "xiaohongshu",
  "followers": 5200, "followers_change": 180,
  "previous": {"avg_engagement_rate_pct": 4.2, "reach": 42000},
  "plan": {"planned_posts": 12},
  "benchmark": {"engagement_rate_avg": 0.04},
  "posts": [
    {"title": "...", "date": "2026-06-05", "type": "carousel", "pillar": "đồ tốt",
     "reach": 8000, "impressions": null, "views": null,
     "likes": 420, "comments": 60, "saves": 300, "shares": 40}
  ]
}
```

Trường có thể thiếu (bài quảng cáo trả tiền loại ra trước rồi mới đưa vào posts). Mẫu số tỉ lệ tương tác ưu tiên reach → impressions → views.
Thiếu `previous`/`plan`/`benchmark` thì phần phân tích tương ứng hạ cấp, không dừng. Chạy:

```bash
python3 skills/openclaw/skill-social-performance-review/scripts/review.py score --input "outputs/<chủ đề>/assets/2026-06.json"
```

Script trả về: tỉ lệ tương tác và điểm tổng từng bài, Top3/Bottom3 (Xiaohongshu xếp theo lượt lưu, còn lại xếp theo tỉ lệ tương tác),
gộp theo trụ cột, gộp theo định dạng, so tháng liền kề (tỉ lệ tương tác/tiếp cận/người theo dõi), điểm nội bộ có trọng số và các chiều đã dùng, `warnings`.

Dựa vào kết quả script hoàn thành 7 mục phân tích (chi tiết xem `references/analysis-framework.md`): ảnh chụp kênh / bài tốt nhất /
bài kém nhất / hiệu quả trụ cột nội dung / hiệu quả định dạng / phân tích câu mở (script không làm, phải đọc câu đầu bài viết) / nhịp đăng bài.
Dữ liệu chuẩn tham khảo `references/benchmarks.md`. Phân tích xong thì xoá JSON tạm.

### Giai đoạn 4 - Quan sát đối thủ (tuỳ chọn)

Chỉ chạy khi có kênh đối thủ và đã cấu hình Playwright/Firecrawl MCP.
Quan sát tần suất đăng, tổ hợp nội dung, định dạng ưa dùng và mức tương tác của đối thủ tháng trước, rút ra 4-6 ý so sánh.

Không có công cụ MCP thì bỏ qua và ghi chú trong báo cáo.

### Giai đoạn 5 - Insight và đề xuất

- **Insight chính** (2-4 ý): nối nhân quả, giải thích mô hình cốt lõi của kết quả trong tháng
- **Đề xuất tháng sau** (3-5 ý, xếp theo tác động dự kiến): mỗi ý gồm "làm gì / căn cứ dữ liệu / triển khai thế nào"
- **Điều chỉnh lịch đăng**: đề xuất thay đổi cụ thể về tỉ lệ trụ cột, tổ hợp định dạng, chiến lược câu mở, tần suất đăng

Đề xuất phải cụ thể và làm được - đừng viết "đăng carousel nhiều hơn", hãy viết "carousel tăng từ 2 lên 4 bài mỗi tháng, tập trung vào [trụ cột hiệu quả nhất]".

### Giai đoạn 6 - Xuất kết quả

1. **Báo cáo**: theo mẫu `references/report-template.md` xuất ra `outputs/<chủ đề>/`
2. **Cập nhật bối cảnh**:
   - `context/best-performers.md` - thêm Top 3 của tháng này
   - `context/review-history.md` - thêm một dòng tóm tắt tháng (tiếp cận / tỉ lệ tương tác / biến động người theo dõi / điểm)
3. **Gợi ý bàn giao**: chỉ cho người dùng cách dùng kết quả hậu kiểm để lên lịch đăng tháng sau

### Điểm nội bộ

Điểm tổng 1-10 do trường `internal_score` của `scripts/review.py score` đưa ra tất định
(**đừng tự nhẩm trọng số**), ghi vào `context/review-history.md`. Các chiều và trọng số:

| Chiều | Trọng số |
|------|------|
| Tỉ lệ tương tác vs chuẩn | 25% |
| Xu hướng tăng người theo dõi | 20% |
| Hiệu quả bài tốt nhất | 20% |
| Tỉ lệ thực hiện lịch đăng | 15% |
| Xu hướng tiếp cận | 20% |

Script sẽ loại các chiều thiếu dữ liệu và chuẩn hoá lại trọng số còn lại, `dimensions_used` ghi rõ các chiều thực sự tham gia.

## Lưu ý

- **Lưu/thích là chỉ số quan trọng nhất trên Xiaohongshu** - cho thấy người dùng thấy nội dung có giá trị, ưu tiên hơn lượt hiển thị
- **Mỗi nền tảng có chỉ số cốt lõi khác nhau** - Xiaohongshu nhìn lượt lưu, Douyin nhìn tỉ lệ xem hết, Bilibili nhìn lượt tặng coin, Weibo nhìn lượt chia sẻ lại
- **Thiếu dữ liệu không bỏ hậu kiểm** - hậu kiểm định tính dựa trên trí nhớ người dùng vẫn có giá trị, ghi rõ giới hạn và thúc đẩy xuất dữ liệu tháng sau
- **Bài quảng cáo trả tiền làm nhiễu chuẩn tự nhiên** - phải xác nhận và loại ra
- **Video ngắn có tiếp cận phồng lên** - phục vụ cả người chưa theo dõi, đừng so tiếp cận trực tiếp với bài ảnh kèm chữ
- **Phần đề xuất mới là cốt lõi** - nhà sáng tạo muốn biết nhất là tháng sau nên làm gì

## Nhận biết Profile

- **Có Profile**:
  - Đọc `platform` để chốt nền tảng phân tích và chuẩn so sánh
  - Đọc trụ cột nội dung để bóc tách theo trụ cột
  - Đọc phong cách thương hiệu để soát tính nhất quán của nội dung
  - Đọc đường dẫn dữ liệu lịch sử để phân tích so tháng liền kề
- **Không có Profile**:
  - Hỏi người dùng nền tảng mục tiêu và mục tiêu trong tháng
  - Dùng chuẩn chung trong `references/benchmarks.md`
  - Bỏ qua phân tích trụ cột (hoặc để người dùng kể phân loại trụ cột)
  - Ghi chú: "nếu cung cấp Profile của kênh, có thể bật bóc tách trụ cột và phân tích xu hướng lịch sử"
