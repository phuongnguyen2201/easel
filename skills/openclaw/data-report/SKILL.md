---
name: data-report
description: >-
  Sinh trang báo cáo trực quan từ CSV/Excel/JSON: KPI, biểu đồ, bảng dữ liệu, insight; report.py
  tính từ dữ liệu thật, ra HTML hoặc ảnh dài. Dùng khi người dùng nói "báo cáo dữ liệu",
  "CSV/Excel ra báo cáo", "dashboard KPI". Một biểu đồ → chart-visualization; infographic/GIF →
  infographic.
layer: produce
---

# Báo cáo trực quan hoá dữ liệu

Bạn là chuyên gia trực quan hoá dữ liệu. Biến dữ liệu CSV/Excel/JSON người dùng đưa thành một
báo cáo HTML trực quan tự chứa (thẻ KPI + biểu đồ + insight + bảng dữ liệu).

Đọc dữ liệu, tổng hợp, vẽ biểu đồ, ráp HTML đều do `scripts/report.py` làm một cách xác định,
bạn chỉ lo khâu cần hiểu là "viết phần insight", đừng tự tính tổng hợp hay tự ghép biểu đồ.

## Khác gì các SKILL biểu đồ còn lại

Cả ba đều "ra biểu đồ" nhưng cơ chế và sản phẩm khác nhau, định tuyến theo nhu cầu:

- **data-report (SKILL này)** = đầu vào CSV/Excel/JSON, cho ra **trang báo cáo trực quan đầy đủ** (thẻ KPI + nhiều biểu đồ + insight + bảng). Cần một trang báo cáo hoàn chỉnh thì dùng nó.
- **chart-visualization** = gọi API từ xa của AntV, cho ra **một URL ảnh tĩnh duy nhất** (25+ loại). Chỉ cần một biểu đồ thống kê chuẩn, lấy luôn link ảnh thì dùng nó.
- **infographic** = render JS tại máy, cho ra **infographic / biểu đồ động GIF**. Cần infographic có cấu trúc hoặc GIF/MP4 có chuyển động thì dùng nó.

## Đầu vào

- File dữ liệu: `.csv` / `.json` / `.xlsx` (Excel cần môi trường có openpyxl, thiếu thì script sẽ báo)
- Tuỳ chọn: tiêu đề báo cáo, tên cột KPI muốn làm nổi bật

## Đầu ra

- Một file báo cáo HTML tự chứa (biểu đồ nhúng base64, mở offline được), ghi vào `outputs/<chủ đề>/`
- Tuỳ chọn: render HTML thành một ảnh dài để chia sẻ mạng xã hội

## Các bước thực hiện

### 1. Đọc tổng quan dữ liệu (để bạn viết insight)

```bash
python skills/openclaw/data-report/scripts/report.py analyze "<file dữ liệu>"
```

Trả về JSON: số hàng/cột, kiểu và phần thiếu của từng cột, min/max/mean/median/sum/std của cột số,
Top 5 của từng cột phân loại. **Dựa vào đó xác định dữ liệu đang nói gì**, chuẩn bị insight cho bước 3.

### 2. Sinh HTML báo cáo

```bash
python skills/openclaw/data-report/scripts/report.py report "<file dữ liệu>" \
  -o "outputs/<chủ đề>/report.html" \
  --title "Tiêu đề báo cáo" \
  --kpi "Tên cột 1" "Tên cột 2"   # tuỳ chọn, không đưa thì tự chọn cột số
```

Script tự động: tính KPI (tổng hợp cột số), tự chọn loại và vẽ 2-4 biểu đồ (chuỗi thời gian → đường,
phân loại → cột, tỉ trọng → tròn), ráp thành trang HTML gồm thẻ KPI + biểu đồ nhúng + bảng dữ liệu.
matplotlib chạy backend Agg và đã cấu hình sẵn font Unicode có dấu nên không lỗi font.

### 3. Viết bổ sung phần insight (tuỳ chọn nhưng nên làm)

Dựa trên tổng quan ở bước 1, bổ sung 3-5 insight vào HTML vừa sinh (mở đầu bằng emoji, giống báo
cáo tuần sản phẩm: xu hướng, bất thường, so sánh, đề xuất hành động). Dùng Edit chèn vào khu
insight của báo cáo là xong - dữ liệu đều là thật, **đừng bịa số**, chỉ diễn giải.

### 4. Render thành ảnh dài để chia sẻ (tuỳ chọn)

```bash
python skills/shared/scripts/render_card.py \
  --html "outputs/<chủ đề>/report.html" \
  --out "outputs/<chủ đề>/report.png" \
  --full-page --width 1080
```

## Nhận biết Profile

- **Có Profile**: đọc màu chủ đạo thương hiệu từ `style.md`, dùng Edit sửa biến `--main` trong HTML cho đồng bộ màu.
- **Không có Profile**: dùng bảng màu chuyên nghiệp mặc định của script.

## Điểm cốt lõi

- **Bắt buộc dùng script để phân tích dữ liệu thật**, KPI và biểu đồ do script tính từ dữ liệu, đừng tự gõ số.
- Insight là phần duy nhất bạn "sáng tác", phần còn lại đi qua script để bảo đảm tính xác định.
- Không có cột số thì script vẫn xuất bảng dữ liệu (có in WARN), báo cáo vẫn dùng được.
