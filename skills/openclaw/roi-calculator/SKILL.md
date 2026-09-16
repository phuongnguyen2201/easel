---
name: roi-calculator
description: >-
  Tính ROI content marketing từ dữ liệu chạy quảng cáo: CTR/CPC/CPM/ROAS, CPA, lợi nhuận, so với
  chuẩn ngành; một chiến dịch hoặc so sánh nhiều chiến dịch theo ROI, gợi ý chia ngân sách. Dùng
  khi người dùng nói "tính ROI", "chạy ads hiệu quả không", "CTR/CPC/CPM/ROAS", "hiệu quả quảng
  cáo".
layer: attribute
---

# Máy tính ROI cho nội dung chạy quảng cáo

> Từ dữ liệu chạy quảng cáo người dùng đưa vào, tính các chỉ số marketing chuẩn, đối chiếu chuẩn ngành, xuất báo cáo phân tích có cấu trúc.

## Đầu vào

Người dùng cung cấp một tập con bất kỳ của các trường sau (thiếu trường nào thì bỏ qua chỉ số phụ thuộc trường đó):

| Trường | Mã | Đơn vị | Mức cần thiết |
|------|------|------|--------|
| Chi phí quảng cáo | ad_spend | CNY | Cốt lõi (bằng 0 hoặc thiếu thì chuyển sang chế độ organic) |
| Lượt hiển thị | impressions | lượt | Tuỳ chọn |
| Lượt click | clicks | lượt | Tuỳ chọn |
| Lượt tương tác | engagements | lượt (thích + bình luận + chia sẻ) | Tuỳ chọn |
| Số chuyển đổi | conversions | lượt | Tuỳ chọn |
| Giá trị đơn trung bình | avg_order_value | CNY | Tuỳ chọn |
| Chi phí sản xuất nội dung | production_cost | CNY | Tuỳ chọn, mặc định không tính |

**Hai chế độ:**

- **Mode A - phân tích một chiến dịch**: một bộ dữ liệu đầu vào, xuất thẻ chỉ số đầy đủ
- **Mode B - so sánh nhiều chiến dịch**: nhiều bộ dữ liệu (bảng hoặc từng dòng), sắp theo ROI giảm dần, so sánh ngang

## Đầu ra

### Tính chỉ số (bảng công thức)

Các chỉ số dưới đây chỉ tính khi mẫu số có dữ liệu và khác 0, nếu không thì ghi "thiếu dữ liệu, đã bỏ qua":

| Chỉ số | Công thức | Trường phụ thuộc |
|------|------|----------|
| CTR (tỉ lệ click) | clicks / impressions | impressions, clicks |
| CPC (chi phí mỗi click) | ad_spend / clicks | ad_spend, clicks |
| CPM (chi phí mỗi 1000 lượt hiển thị) | (ad_spend / impressions) * 1000 | ad_spend, impressions |
| CPE (chi phí mỗi lượt tương tác) | ad_spend / engagements | ad_spend, engagements |
| Tỉ lệ chuyển đổi | conversions / clicks | conversions, clicks |
| CPA (chi phí mỗi chuyển đổi) | ad_spend / conversions | ad_spend, conversions |
| Doanh thu | conversions * avg_order_value | conversions, avg_order_value |
| ROAS (doanh thu trên chi phí quảng cáo) | revenue / ad_spend | revenue, ad_spend |
| Tổng chi phí | ad_spend + production_cost | ad_spend (thiếu production_cost thì tính 0) |
| Lợi nhuận | revenue - total_cost | revenue, total_cost |
| ROI | (revenue - total_cost) / total_cost | revenue, total_cost |

### Định dạng đầu ra

**Mode A - phân tích một chiến dịch:**

```
## Báo cáo hiệu quả quảng cáo

### Dữ liệu gốc
(các trường người dùng cung cấp)

### Chỉ số tính được
| Chỉ số | Giá trị | Công thức | So với chuẩn |
|------|----|------|----------|
| CTR  | x% | clicks/impressions | ▲ cao hơn trung bình ngành |
| ...  |    |      |          |

### Chú giải so sánh chuẩn
▲ cao hơn trung bình ngành (tốt)
▼ thấp hơn trung bình ngành (cần lưu ý)
≈ xấp xỉ trung bình ngành (mức bình thường)
⚠ lệch rõ rệt (vượt chuẩn 2 lần hoặc thấp hơn 50%)

### Chẩn đoán
- Điểm nổi bật: (liệt kê chỉ số cao hơn chuẩn và phân tích lợi thế)
- Cần tối ưu: (liệt kê chỉ số thấp hơn chuẩn và hướng cải thiện cụ thể)
- Đánh giá chung: (một câu tổng kết hiệu quả đợt chạy này)
```

**Mode B - so sánh nhiều chiến dịch:**

```
## So sánh ngang nhiều chiến dịch (ROI giảm dần)

| Chiến dịch | Chi phí | Doanh thu | ROI | ROAS | CTR | CPC | Đánh giá chung |
|------|------|------|-----|------|-----|-----|----------|
| ...  |      |      |     |      |     |     |          |

### Phân tích chiến dịch tốt nhất / kém nhất
(so chênh lệch chỉ số then chốt giữa chiến dịch ROI cao nhất và thấp nhất, tìm nguồn gốc khoảng cách)

### Gợi ý chia ngân sách
(dựa trên hiệu suất từng chiến dịch, đề xuất tỉ lệ dồn ngân sách về chiến dịch ROI cao)

### Gợi ý tối ưu
(hướng cải thiện cụ thể cho chiến dịch kém hiệu quả)
```

## Các bước thực hiện

> **Tính toán xác định giao cho script, LLM chỉ diễn giải.** Mọi chỉ số ở bảng trên (gồm doanh thu/lợi nhuận suy ra, chế độ organic tính thêm tỉ lệ tương tác),
> việc chuyển chế độ organic, kiểm tra trường dữ liệu, Mode B sắp ROI giảm dần, tất cả đều do
> [`scripts/calc.py`](scripts/calc.py) lo (dùng lại `safe_div` của `skills/shared/scripts/social_stats.py`,
> chia 0 hoặc thiếu trường đều trả `null`, không nhẩm tay, không đoán số).

1. **Đọc đầu vào** - trích các trường dữ liệu từ prompt của người dùng, nhận biết Mode A (một bộ dữ liệu) hay Mode B (nhiều bộ dữ liệu)
2. **Gọi script tính chỉ số** -
   - Mode A (một chiến dịch):
     ```bash
     python3 skills/openclaw/roi-calculator/scripts/calc.py single --name "Tên chiến dịch" \
       --ad-spend 5000 --impressions 100000 --clicks 3000 \
       --engagements 8000 --conversions 150 --avg-order-value 200 \
       --production-cost 1000
     ```
   - Mode B (nhiều chiến dịch, ROI giảm dần): gom các chiến dịch vào một file mảng JSON rồi
     ```bash
     python3 skills/openclaw/roi-calculator/scripts/calc.py multi --file campaigns.json
     ```
   Script tự lo: tính lần lượt 11 chỉ số (mẫu số bằng 0 hoặc thiếu thì trả `null` và coi là "thiếu dữ liệu"),
   suy ra doanh thu -> ROAS/lợi nhuận/ROI, `ad_spend` bằng 0 hoặc thiếu thì chuyển chế độ organic (bỏ nhóm chỉ số chi phí),
   kiểm tra trường (số âm / hiển thị < click / chuyển đổi > click ghi vào `warnings`), Mode B sắp theo `roi_pct` giảm dần và gắn `roi_rank`.
3. **Nạp chuẩn ngành** - đọc [benchmarks.md](references/benchmarks.md) để lấy dữ liệu chuẩn ngành (số liệu gốc theo thị trường Trung Quốc)
4. **Chọn chuẩn để đối chiếu** -
   - Có Profile: đọc `platforms.md` để xác định nền tảng chính, chọn chuẩn của nền tảng đó
   - Không có Profile: dùng mức trung bình chung của các nền tảng
5. **Đối chiếu chuẩn (LLM diễn giải)** - so từng chỉ số script xuất ra với chuẩn, gắn ▲ cao hơn / ▼ thấp hơn / ≈ ngang / ⚠ lệch rõ rệt
6. **Viết chẩn đoán (LLM diễn giải)** - tổng hợp điểm nổi bật và điểm cần tối ưu, đưa gợi ý cải thiện làm được ngay; chuyển tiếp `warnings` của script
7. **Phần thêm cho Mode B (LLM diễn giải)** - dựa trên thứ hạng ROI script đã sắp, đánh dấu tốt nhất/kém nhất, phân tích nguyên nhân chênh lệch, đề xuất cách chia ngân sách

## Chế độ nội dung organic

Khi ad_spend bằng 0 hoặc thiếu, tự động chuyển:

- Bỏ qua mọi chỉ số nhóm chi phí (CPC/CPM/CPE/CPA/ROAS/ROI/lợi nhuận)
- Chỉ tính: CTR (nếu có impressions + clicks), tỉ lệ tương tác (engagements / impressions)
- Tiêu đề báo cáo ghi rõ "Phân tích hiệu quả nội dung organic"
- Đối chiếu bằng chuẩn của lượng tiếp cận tự nhiên (thường cao hơn lượng trả phí)

## Nhận biết Profile

**Khi có Profile:**
- Đọc `platforms.md` để biết nền tảng chạy chính, dùng khoảng chuẩn riêng của nền tảng đó
- Đọc `audience.md` để nắm đặc điểm khán giả, làm ngữ cảnh cho việc đánh giá tỉ lệ chuyển đổi
- Kết luận so sánh dùng chuẩn chính xác theo từng nền tảng

**Khi không có Profile:**
- Dùng mức trung bình tổng hợp của các nền tảng làm chuẩn
- Cuối báo cáo ghi chú: "Cung cấp Profile của kênh (kèm thông tin nền tảng) sẽ có đối chiếu chuẩn riêng theo nền tảng"

## Quy tắc

1. **Không bịa đầu vào** - mọi chỉ số chỉ tính từ dữ liệu người dùng đưa, thiếu trường thì bỏ qua chỉ số phụ thuộc
2. **Công thức minh bạch** - ghi công thức bên cạnh mỗi chỉ số để người dùng kiểm được
3. **Đối chiếu chuẩn** - so với chuẩn ngành, ghi rõ cao hơn/thấp hơn/ngang bằng
4. **Chấp nhận thiếu dữ liệu** - thiếu trường thì không giả định số, bỏ qua và nói rõ "thiếu dữ liệu X nên không tính được"
5. **Tự chuyển organic** - ad_spend bằng 0 hoặc thiếu thì tự chuyển chế độ organic, không báo lỗi

## Ghi chú tự phát triển

**Nguồn dữ liệu chuẩn (cập nhật định kỳ references/benchmarks.md):**
- Báo cáo chuẩn ngành chính thức của Google Ads / Meta Ads
- Sách trắng hiệu quả quảng cáo của Ocean Engine / Qianchuan (chuẩn thị trường Trung Quốc)
- Báo cáo ngành của Newrank / Feigua / Chanmama (chuẩn thị trường Trung Quốc)
- Dữ liệu công khai từ trung tâm nhà sáng tạo của các nền tảng

**Hướng phát triển tiếp:**
- Thêm so sánh theo chuỗi thời gian (tuần liền kề, cùng kỳ tháng)
- Hỗ trợ chuẩn tự đặt (người dùng đưa mức trung bình lịch sử làm mốc so sánh)
- Kết nối nguồn dữ liệu API thật (Ocean Engine / Xiaohongshu Juguang / WeChat Ads)
- Xuất biểu đồ phễu (phễu impressions → clicks → conversions)
- Hỗ trợ mô hình attribution (chạm đầu / chạm cuối / attribution tuyến tính)
- Liên thông với SKILL content-postmortem, lấy dữ liệu quảng cáo nuôi lại chiến lược nội dung

**Quy tắc bảo trì dữ liệu chuẩn:**
- Mỗi quý đối chiếu báo cáo ngành mới nhất để hiệu chỉnh các khoảng số trong benchmarks.md
- Ghi thời điểm thu thập dữ liệu, chuẩn quá hạn trên 6 tháng thì gắn nhắc ⚠
- Khuyến khích người dùng đưa dữ liệu lịch sử của chính họ để dần dựng chuẩn nội bộ cấp kênh
