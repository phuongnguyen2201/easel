---
name: infographic
description: >-
  Biến dữ liệu/văn bản thành infographic, render cục bộ: (A) tĩnh AntV 50+ mẫu lưu đồ/so
  sánh/SWOT; (B) GIF động đua cột/số chạy/tiến độ/đường mọc. Dùng khi người dùng nói "làm
  infographic", "biểu đồ động/GIF", "sơ đồ SWOT". Một ảnh URL → chart-visualization; báo cáo cả
  trang → data-report.
layer: produce
---

# Làm infographic

> Biến dữ liệu hoặc nội dung chữ thành infographic trực quan, hỗ trợ hai chế độ xuất: infographic AntV tĩnh và GIF động

## Khác gì các SKILL biểu đồ khác

Đều "sinh biểu đồ" được, nhưng cơ chế và sản phẩm khác nhau, định tuyến theo nhu cầu:

- **infographic (SKILL này)** = render cục bộ. Hai loại sản phẩm: **infographic** tĩnh (AntV DSL, danh sách/lưu đồ/so sánh/phân cấp HTML→SVG) + **biểu đồ GIF động** (matplotlib dựng từng khung→GIF).
- **chart-visualization** = gọi API AntV từ xa, cho ra **URL một ảnh tĩnh** (hơn 25 kiểu), nhanh nhất khi chỉ cần một ảnh.
- **data-report** = nhận CSV/Excel/JSON, cho ra **báo cáo trực quan cả trang** (thẻ KPI + nhiều biểu đồ + insight + bảng).

**Ranh giới hai chế độ**: cần **infographic vector tĩnh** (xuất được SVG, nhiều mẫu) → chế độ A; cần **GIF biết chuyển động** (ảnh động đăng mạng xã hội/story, như đua cột, số chạy, tiến độ, đường mọc) → chế độ B.

## Đầu vào

Nội dung chữ, dữ liệu hoặc mô tả chủ đề do người dùng đưa. Có thể là dữ liệu có cấu trúc (CSV/JSON), mô tả bằng ngôn ngữ tự nhiên, hoặc chỉ là một dãy số liệt kê.

## Đầu ra

- Chế độ tĩnh: `outputs/<chủ đề>/infographic.html` (mở bằng trình duyệt, xuất được SVG)
- Chế độ động: `outputs/<chủ đề>/chart.gif` (`scripts/gif_chart.py` cho ra thẳng GIF đăng mạng xã hội được)

## Các bước thực hiện

### Bước 1: Chốt chế độ xuất

Hỏi người dùng chọn định dạng đầu ra:

1. **Infographic tĩnh** (AntV Infographic) - hơn 50 mẫu: danh sách, lưu đồ, so sánh, phân cấp, sơ đồ quan hệ; render vector, xuất được SVG
2. **GIF động** (`scripts/gif_chart.py`) - 4 kiểu animation viral: đua cột / số chạy / tiến độ / đường mọc, cho ra thẳng GIF

Nếu yêu cầu đã rõ (kiểu "làm ảnh động đua cột" hay "làm cái lưu đồ"), chọn luôn chế độ tương ứng, khỏi hỏi lại.

### Bước 2: Phân tích nội dung và chọn biểu đồ

Phân tích đầu vào của người dùng, rút ra cấu trúc thông tin chính (tiêu đề, mô tả, các mục dữ liệu...). Chọn mẫu/kiểu biểu đồ phù hợp.

**Mấu chốt: phải tôn trọng ngôn ngữ người dùng nhập. Người dùng nhập tiếng Việt thì mọi chữ trên hình phải là tiếng Việt.**

### Bước 3: Render

- **Chế độ A (AntV tĩnh)** → đọc `references/antv-templates.md`: quy tắc cú pháp DSL, hướng dẫn chọn mẫu, danh sách mẫu khả dụng, mẫu render HTML. Sinh HTML lưu vào `outputs/`, rồi báo đường dẫn.

- **Chế độ B (GIF động)** → gọi `scripts/gif_chart.py <lệnh con>`, không cần tự viết code animation. Lệnh con theo kiểu biểu đồ:

  | Lệnh con | Dùng cho | Cấu trúc JSON của dữ liệu |
  |--------|------|----------------|
  | `bar-race` | Đua cột (thứ hạng đổi theo thời gian, món viral của data viz) | `{"title","times":[...],"series":{"tên":[giá trị theo từng mốc]}}` |
  | `count-up` | Số chạy tăng dần (KPI từ 0 lên mục tiêu) | `{"title","items":[{"label","value","suffix"}]}` hoặc `{"label","value"}` |
  | `progress` | Animation tiến độ (`--style ring`/`bar`) | `{"label","value","max","color"}` |
  | `line-grow` | Đường gấp khúc mọc dần | `{"title","x":[...],"series":{"tên":[giá trị]}}` |

  Tham số chung: `--output x.gif`, `--data f.json` (`-` là đọc stdin, bỏ trống thì dùng ví dụ có sẵn), `--title`, `--width` (mặc định 900), `--height`, `--fps` (mặc định 20), `--duration` (giây, mặc định 4).

  Cách gọi điển hình (ghi dữ liệu ra JSON tạm trước, rồi gọi script):
  ```bash
  python skills/openclaw/infographic/scripts/gif_chart.py bar-race --data data.json \
    --output outputs/tang-truong-do-thi/dua-cot.gif --width 900 --duration 5
  ```
  Script tự đặt font chữ, backend Agg, bảng màu thích ứng để ghìm dung lượng. Tự kiểm tra: `python skills/openclaw/infographic/scripts/gif_chart.py --selftest`.

## Cấu trúc thư mục

```
infographic/
├── SKILL.md                    File này (quy trình chạy + con trỏ tới references)
├── scripts/
│   └── gif_chart.py            Chế độ B: runtime GIF động (matplotlib+Pillow, 4 lệnh con)
└── references/
    ├── antv-templates.md       Chế độ A: đặc tả đầy đủ infographic AntV tĩnh
    └── gif-charts.md           Chế độ B: tham khảo cách chọn biểu đồ/định dạng dữ liệu
```
