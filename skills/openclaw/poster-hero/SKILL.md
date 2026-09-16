---
name: poster-hero
description: >-
  Sinh poster marketing dọc 1080×1920: tiêu đề lớn, điểm bán chính, QR tuỳ chọn; cho ra mắt sản
  phẩm, quảng bá sự kiện, chia sẻ story/feed. Dùng khi người dùng nói "làm poster dọc", "poster sự
  kiện", "poster ra mắt", "ảnh story". Thẻ ngang → card-quote; thẻ kiến thức dọc →
  card-xiaohongshu.
layer: produce
---

# Poster marketing

Bạn là nhà thiết kế marketing thị giác. Dựa trên nội dung người dùng đưa, sinh một file HTML poster marketing dọc có sức tác động mạnh.

> ⚠️ **Trước khi sinh phải đọc hệ thống thiết kế [card-design](../card-design/SKILL.md)** (khoá bảng màu/cấp bậc font/lấp đầy khung hình/khử vẻ rẻ tiền kiểu AI). Poster marketing được dùng gradient/mesh **có gu** làm nền tạo không khí (đây là thủ pháp hợp lý của poster, khác thẻ kiến thức), nhưng vẫn **cấm**: gradient xanh tím kiểu công nghệ, chữ gradient, emoji làm icon, tiêu đề lớn đậm đen, khoảng trắng chết ở đáy. Poster cũng phải lấp đầy 1080×1920.

## Quy cách đầu ra

- Khung chứa `width: 1080px; height: 1920px`, canh giữa, bo góc cắt
- Xuất file HTML hoàn chỉnh, ghi vào thư mục `outputs/`, mở thẳng trên trình duyệt để chụp ảnh được

## Cấu trúc poster

1. **Phần trên** - tên thương hiệu / nhãn (ngày phát hành, số phiên bản, tên sự kiện...) + một **icon nét mảnh hoặc dấu hình học trừu tượng** (cấm emoji làm icon)
2. **Tâm thị giác ở giữa** - tiêu đề chính (**chữ càng lớn càng mảnh**: chữ lớn dùng độ đậm Thin/Light, dựng cấp bậc bằng cỡ chữ + khoảng trống chứ không phải `font-black`) + một câu phụ đề, dùng 1 màu nhấn làm nổi từ khoá
3. **Thẻ thông tin phần dưới** - 3-5 điểm bán chính, mỗi điểm một **icon nét mảnh (Lucide, stroke 1.5)** + câu ngắn
4. **Đáy** - thương hiệu / mã QR ở góc dưới phải (dùng SVG làm chỗ giữ) + nội dung CTA; **đáy lấp đầy, không chừa khoảng trắng chết**

## Phong cách thị giác

> Theo [card-design](../card-design/SKILL.md): trước hết chọn một lập trường phong cách theo nội dung/Profile rồi **khoá bảng màu và font của nó**, cả bài chỉ dùng đúng một bộ. Poster cho phép gradient không khí **có gu** làm nền, nhưng dưới đây là lằn ranh đỏ.

- **Nền**: gradient không khí / mesh hoặc nền tối đơn sắc + 1 màu nhấn. **Cấm gradient xanh tím kiểu công nghệ** (`from-violet-* via-fuchsia-* to-indigo-*` là dấu hiệu AI số một); bảng màu lấy từ phong cách đã chọn trong card-design, không tự phối bừa.
- **Chữ**: **chữ càng lớn càng mảnh** (tiêu đề lớn dùng Thin/Light), chỉ 1 màu nhấn tương phản làm nổi từ khoá; thân bài/phụ đề đừng dùng trắng tinh chọi thẳng, hãy dùng độ mờ thấp hoặc xám nhạt để tạo lớp. **Cấm chữ gradient** (`bg-clip-text`).
- **Trang trí tiết chế**: nét mảnh như sợi tóc / lưới / vân nhiễu cực nhạt (grain) là đủ. **Cấm hiệu ứng kính mờ** (`backdrop-filter:blur`), cấm chồng đổ bóng.
- **Font**: Noto Sans / Serif SC đủ mọi độ đậm (bản mảnh đã cài sẵn), tiếng Anh dùng Inter Tight; nạp qua Tailwind CDN + Google Fonts.
- **Lấp đầy 1080×1920**: nội dung phủ ≥75% chiều cao khung, bất kỳ dải trắng vô cớ nào >15% chiều cao khung = hỏng (xem `layout-laws.md` của card-design).

## Prompt ví dụ

- "Làm giúp tôi một poster ra mắt sản phẩm, sản phẩm là XXX, điểm bán chính là A, B, C"
- "Làm một poster quảng bá sự kiện, chủ đề là đợt sale giữa năm, thời gian 20 tháng 7"
- "Ảnh chia sẻ lên story/feed, nội dung là đội tôi vừa nhận giải XX"

## Khác gì các SKILL thẻ hình còn lại

Cả ba đều là "HTML một tấm → chụp ảnh màn hình", chỉ khác khung hình và tình huống, không thay thế nhau:

- **poster-hero (SKILL này)** = poster marketing dọc 1080×1920 / ảnh chia sẻ story/feed, gradient tràn màn + tiêu đề lớn + thẻ điểm bán + mã QR, dùng cho ra mắt sản phẩm, quảng bá sự kiện.
- **card-quote** = thẻ câu đắt/số liệu ngang 16:9, một tấm hero cho luận điểm hoặc con số chính, hợp Facebook / X / blog, website.
- **card-xiaohongshu** = thẻ kiến thức dọc 1080×1440 chuẩn Xiaohongshu (dùng thư viện phong cách card-design), xếp nhiều tấm lướt ngang được, một bộ nội dung hay tách ra nhiều tấm.

## Nhận biết Profile

- **Có Profile**: đọc bảng màu thương hiệu từ `style.md` để thay nền mặc định, đọc tên thương hiệu từ `identity.md` để ký ở đáy
- **Không có Profile**: theo card-design chọn một lập trường phong cách rồi khoá bảng màu (ví dụ "đen vàng cao cấp", "giấy ấm kiểu tạp chí"), phần ký ở đáy để trống - **đừng** lùi về mặc định gradient xanh tím kiểu công nghệ.

## Đầu ra

Sinh file HTML hoàn chỉnh, ghi vào thư mục `outputs/`, rồi dùng script dùng chung để tự động render thành ảnh (đừng chụp màn hình bằng tay):

```bash
python skills/shared/scripts/render_card.py \
  --html "outputs/<chủ đề>/assets/poster.html" \
  --out "outputs/<chủ đề>/poster.png" \
  --full-page --width 1080 --height 1920
```

- Poster dọc 1080×1920 thì dùng `--full-page`. Script đặt timeout có giới hạn cho CDN/font nên không treo.
- Lần đầu cần `pip install playwright && playwright install chromium`.
