---
name: chart-visualization
description: >-
  Vẽ biểu đồ từ dữ liệu, 25+ loại: cột, đường, tròn, radar, sankey, sơ đồ tư duy, lưu đồ; gọi AntV
  API qua mạng, trả URL ảnh tĩnh. Dùng khi người dùng nói "vẽ biểu đồ", "biểu đồ cột/tròn", "làm
  chart". Infographic/GIF render cục bộ → infographic; báo cáo cả trang từ CSV/JSON → data-report.
layer: produce
---

Dựa trên nội dung người dùng nhập, trực quan hoá dữ liệu thành biểu đồ.

## Khác gì các SKILL biểu đồ còn lại

Cả ba đều "sinh biểu đồ", nhưng cơ chế và sản phẩm khác nhau, định tuyến theo nhu cầu:

- **chart-visualization (SKILL này)** = gọi API AntV từ xa (gpt-vis), cho ra **URL ảnh tĩnh**, 25+ loại biểu đồ, nhanh nhất để có một tấm. Cần một biểu đồ thống kê chuẩn, lấy luôn link ảnh thì dùng nó.
- **infographic** = render JS cục bộ, cho ra **infographic / biểu đồ động GIF** (mẫu danh sách/quy trình/so sánh/phân cấp + hoạt hình từng khung). Cần infographic có cấu trúc xuất được SVG, hoặc GIF/MP4 có hiệu ứng vào, thì dùng nó.
- **data-report** = nhập CSV/Excel/JSON, cho ra **báo cáo trực quan cả trang** (thẻ KPI + nhiều biểu đồ + insight dữ liệu + bảng). Cần một trang báo cáo đầy đủ chứ không phải một tấm hình thì dùng nó.

## Các bước
1. Phân tích dữ liệu và nhu cầu của người dùng, chọn loại biểu đồ hợp nhất
2. Dựng body JSON đúng đặc tả
3. Dùng công cụ curl gọi API để sinh ảnh biểu đồ
4. Xuất URL ảnh trả về dưới dạng ảnh Markdown

## Hướng dẫn chọn biểu đồ

Dựa vào đặc điểm dữ liệu và nhu cầu của người dùng, chọn loại biểu đồ hợp nhất:

- **Chuỗi thời gian**: dùng `line` (xu hướng) hoặc `area` (xu hướng tích luỹ); hai đơn vị đo khác nhau thì dùng `dual-axes`
- **So sánh**: dùng `bar` (so sánh phân loại nằm ngang) hoặc `column` (so sánh phân loại dựng đứng); phân bố tần suất dùng `histogram`
- **Tỉ trọng**: dùng `pie` (cơ cấu tỉ lệ) hoặc `treemap` (tỉ trọng phân cấp)
- **Quan hệ và luồng**: dùng `scatter` (tương quan), `sankey` (dòng chảy) hoặc `venn` (giao nhau giữa các tập)
- **Phân cấp và dạng cây**: dùng `organization-chart` hoặc `mind-map`
- **Loại chuyên biệt**:
  - `radar`: so sánh đa chiều
  - `funnel`: tỉ lệ chuyển đổi qua từng giai đoạn
  - `liquid`: phần trăm/tiến độ
  - `word-cloud`: tần suất từ trong văn bản
  - `boxplot` / `violin`: phân bố thống kê
  - `network-graph`: quan hệ nút phức tạp
  - `fishbone-diagram`: phân tích nhân quả
  - `flow-diagram`: lưu đồ
  - `spreadsheet`: bảng dữ liệu có cấu trúc hoặc pivot table

## Giao diện API

POST https://antv-studio.alipay.com/api/gpt-vis

> Endpoint này là dịch vụ gpt-vis công cộng miễn phí do AntV/Alipay vận hành, không cần key; dịch vụ công có thể bị bóp lưu lượng hoặc thay đổi, khi trả về lỗi thì thử lại hoặc lùi về render cục bộ (infographic chế độ A).

Body yêu cầu là JSON, bắt buộc có trường `type` và `source: "chart-visualization-skills"`.

Ví dụ:
```bash
curl -X POST https://antv-studio.alipay.com/api/gpt-vis \
  -H "Content-Type: application/json" \
  -d '{"type":"line","source":"chart-visualization-skills","data":[{"time":"2025-01","value":100}],"title":"Biểu đồ ví dụ"}'
```

Ví dụ kết quả trả về:
```json
{"success":true,"resultObj":"https://..."}
```

Xuất URL trong `resultObj` dưới dạng ảnh Markdown: `![Biểu đồ](URL)`

## Các loại biểu đồ được hỗ trợ

| Nhóm | Loại biểu đồ |
|------|---------|
| So sánh | biểu đồ thanh ngang (bar), biểu đồ cột (column), biểu đồ thác nước (waterfall), biểu đồ hai trục (dual-axes) |
| Xu hướng | biểu đồ miền (area), biểu đồ đường (line), biểu đồ phân tán (scatter) |
| Phân bố | biểu đồ hộp (boxplot), biểu đồ tần suất (histogram), biểu đồ violin (violin), biểu đồ phễu (funnel) |
| Tỉ trọng | biểu đồ tròn (pie), biểu đồ sóng nước (liquid), mây từ khoá (word-cloud) |
| Phân cấp | sơ đồ tổ chức (organization-chart), sơ đồ tư duy (mind-map), biểu đồ cây ô chữ nhật (treemap), biểu đồ sankey (sankey) |
| Quan hệ | sơ đồ quan hệ (network-graph), biểu đồ Venn (venn) |
| Quy trình | lưu đồ (flow-diagram), sơ đồ xương cá (fishbone-diagram) |
| Đa chiều | biểu đồ radar (radar) |
| Bảng | bảng/pivot table (spreadsheet) |

## Tham số tuỳ chọn dùng chung

| Tham số | Kiểu | Mặc định | Mô tả |
|------|------|--------|------|
| theme | string | "default" | Chủ đề: "default" / "academy" / "dark" |
| width | number | 600 | Chiều rộng biểu đồ |
| height | number | 400 | Chiều cao biểu đồ |
| title | string | "" | Tiêu đề biểu đồ |
| style.texture | string | "default" | Vân nét: "default" / "rough" (kiểu vẽ tay) |

Biểu đồ có trục toạ độ còn hỗ trợ: axisXTitle, axisYTitle.

## Định dạng data của từng biểu đồ

- **area / line**: `{time: string, value: number, group?: string}[]`, tuỳ chọn stack: boolean
- **bar**: `{category: string, value: number, group?: string}[]`, tuỳ chọn group / stack (mặc định stack: true)
- **column**: `{category: string, value: number, group?: string}[]`, tuỳ chọn group (mặc định true) / stack
- **scatter**: `{x: number, y: number, group?: string}[]`
- **pie**: `{category: string, value: number}[]`, tuỳ chọn innerRadius: number (0-1)
- **radar**: `{name: string, value: number, group?: string}[]`
- **funnel**: `{category: string, value: number}[]`
- **waterfall**: `{category: string, value?: number, isTotal?: boolean, isIntermediateTotal?: boolean}[]`
- **dual-axes**: categories: string[], series: {type: "column"|"line", data: number[], axisYTitle?: string}[]
- **histogram**: `number[]`, tuỳ chọn binNumber: number
- **boxplot / violin**: `{category: string, value: number, group?: string}[]`
- **liquid**: percent: number (0-1), tuỳ chọn shape: "circle"|"rect"|"pin"|"triangle"
- **word-cloud**: `{text: string, value: number}[]`
- **sankey**: `{source: string, target: string, value: number}[]`, tuỳ chọn nodeAlign
- **treemap**: `{name: string, value: number, children?: ...}[]` (sâu tối đa 3 lớp)
- **venn**: `{sets: string[], value: number, label?: string}[]`
- **network-graph / flow-diagram**: `{nodes: {name: string}[], edges: {source: string, target: string, name?: string}[]}`
- **fishbone-diagram / mind-map**: `{name: string, children?: ...}` (sâu tối đa 3 lớp)
- **organization-chart**: `{name: string, description?: string, children?: ...}` (sâu tối đa 3 lớp), tuỳ chọn orient: "horizontal"|"vertical"
- **spreadsheet**: `Record<string, string | number>[]`, tuỳ chọn rows / columns / values (trường của pivot table)
