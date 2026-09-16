---
name: comparison-card
description: >-
  Làm ảnh so sánh A vs B / "một ảnh nói hết": bảng thông số, ưu–nhược; render HTML+CSS thành thẻ
  chụp được, chia sẻ Facebook/Threads. Dùng khi người dùng nói "A vs B", "so sánh thông số", "cái
  nào tốt hơn". Biểu đồ số liệu → chart-visualization; infographic nhiều chiều → infographic.
layer: produce
---

# Ảnh so sánh / một ảnh nói hết

> Tạo thẻ so sánh trực quan A vs B, một ảnh chụp là thấy rõ khác biệt, hợp để chia sẻ mạng xã hội.

> ⚠️ **Trước khi tạo phải đọc hệ thống thiết kế [card-design](../card-design/SKILL.md)** (khoá bảng màu/cấp bậc font/lấp đầy khung hình/khử cảm giác AI rẻ tiền). Ảnh so sánh dùng bộ khung "bảng so sánh" (hai cột trái phải, ≥5 dòng so sánh, chiều cao dòng đồng nhất), tránh gradient, emoji, khoảng trắng chết ở đáy.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| `items` | Có | 2-4 đối tượng cần so sánh (tên) |
| `dimensions` | Không | Danh sách tiêu chí so sánh (giá, hiệu năng, tính năng...); không nêu thì tự trích |
| `data` | Không | Dữ liệu so sánh có cấu trúc (JSON/bảng); không đưa thì SKILL tự tra và điền |
| `layout` | Không | Kiểu bố cục: `table` (mặc định) / `versus` / `pros_cons` |
| `size` | Không | Preset kích thước: `xiaohongshu`(1080x1440) / `weibo`(1080x1080) / `wechat`(1080x1920) / `auto` |
| `style` | Không | Phong cách thị giác: lấy từ **thư viện phong cách card-design** (Swiss tối giản/tạp chí biên tập/đen vàng cao cấp...), không nêu thì chọn theo loại nội dung/Profile |
| `winner` | Không | Có đánh dấu mục thắng hay không: `true` / `false` (mặc định `false`) |

### Giải thích các kiểu bố cục

| Kiểu | Mô tả | Trường hợp dùng |
|------|------|----------|
| `table` | Bảng thông số kinh điển, hàng = tiêu chí, cột = đối tượng | So sánh sản phẩm nhiều tiêu chí, nhiều thông số |
| `versus` | Bố cục VS đối xứng trái phải, có đường chia ở giữa | So sánh trực quan hai đối tượng |
| `pros_cons` | Chia cột ưu/nhược, xanh cho ưu, đỏ cho nhược | Phân tích ưu nhược của một sản phẩm |

## Đầu ra

- File HTML hoàn chỉnh, mở được bằng trình duyệt và chụp màn hình
- Kích thước thẻ cố định (px), chụp ra đúng như nhìn thấy
- Ghi vào thư mục `outputs/<chủ đề>/`

## Các bước thực hiện

### Step 1 - Phân tích yêu cầu so sánh

1. Chốt các đối tượng so sánh (2-4 cái)
2. Chốt tiêu chí so sánh:
   - Người dùng đã nêu → dùng luôn
   - Người dùng không nêu → tự suy ra tiêu chí phổ biến theo loại đối tượng (ví dụ điện thoại: giá/màn hình/chip/pin/camera)
3. Chốt kiểu bố cục và kích thước

### Step 2 - Thu thập và sắp xếp dữ liệu

Nếu người dùng đã đưa đủ dữ liệu:
- Cấu trúc hoá thẳng thành ma trận so sánh

Nếu người dùng chỉ đưa tên đối tượng, không đưa dữ liệu:
- Dùng WebSearch tra thông số then chốt của từng đối tượng
- Đối chiếu chéo để kiểm độ chính xác (ít nhất 2 nguồn)
- Ghi rõ nguồn dữ liệu

Sắp dữ liệu thành ma trận chuẩn:
```json
{
  "items": ["A", "B"],
  "dimensions": [
    {"name": "Giá", "values": ["9.990.000d", "12.990.000d"], "winner": "A"},
    {"name": "Hiệu năng", "values": ["Snapdragon 8 Gen3", "A17 Pro"], "winner": "B"}
  ]
}
```

### Step 3 - Dựng thẻ HTML

1. Đọc `references/comparison-template.html` làm template gốc
2. Chọn cấu trúc bố cục theo kiểu `layout`
3. Đổ dữ liệu vào template
4. **Áp bảng màu/font của phong cách card-design đã chọn** (khoá spec, cả bảng đồng nhất; không tự chế màu)
5. Đặt kích thước thẻ (tham số `size`)
6. Nếu `winner` là true, đánh dấu mục thắng bằng chỉ dấu thị giác (highlight/icon vương miện)

### Step 4 - Tinh chỉnh thị giác

- Bảo đảm chữ không tràn khỏi ô
- Dữ liệu dạng số canh phải, dạng chữ canh trái
- Mục thắng highlight bằng **màu nhấn** của phong cách card-design đã chọn, mục yếu dùng xám trung tính (không hard-code một màu xanh lá nào)
- Thêm phần ghi nguồn dữ liệu và ngày ở đáy thẻ
- Tuân thủ luật sắt của card-design: cấm gradient công nghệ xanh tím, cấm dùng emoji làm icon, lấp đầy khung không chừa khoảng trắng chết

### Step 5 - Ghi file

Ghi HTML vào thư mục `outputs/<chủ đề>/assets/`, tên file theo mẫu: `{A}_vs_{B}_so-sanh_{ngay}.html`

### Step 6 - Render ra ảnh (đừng chụp màn hình thủ công)

Dùng script dùng chung để render tự động:

```bash
python skills/shared/scripts/render_card.py \
  --html "outputs/<chủ đề>/assets/A_vs_B_so-sanh.html" \
  --out "outputs/<chủ đề>/A_vs_B_so-sanh.png" \
  --full-page --width 1080 --height 1440
```

Kích thước chỉnh theo preset nền tảng khớp với Profile (mặc định Xiaohongshu 1080x1440). Script dùng playwright+chromium, có timeout cho CDN/font nên không treo; lần đầu cần `pip install playwright && playwright install chromium`.

## Nhận biết Profile

- **Có Profile**: đọc bảng màu thương hiệu từ `style.md` để thay màu mặc định của template; đọc tên kênh từ `identity.md` làm watermark; đọc nền tảng chủ lực từ `platforms.md` để tự khớp kích thước
- **Không có Profile**: dùng bảng màu tươi sáng mặc định, không watermark, kích thước mặc định Xiaohongshu (1080x1440)

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
