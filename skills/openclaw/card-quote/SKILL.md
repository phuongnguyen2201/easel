---
name: card-quote
description: >-
  Sinh thẻ trích dẫn/thẻ số liệu ngang 16:9 (một câu hero hay cụm số chính) để chia sẻ trên
  Facebook, Threads/X, LinkedIn. Dùng khi người dùng nói "làm thẻ trích dẫn", "thẻ quote", "thẻ số
  liệu", "thẻ ngang chia sẻ". Thẻ kiến thức dọc → card-xiaohongshu; poster dọc marketing →
  poster-hero.
layer: produce
---

# Thẻ câu đắt

> Render HTML thành một ảnh → chụp màn hình để chia sẻ. Khung ngang 16:9, một câu hero đắt / một cụm số liệu chính.

> ⚠️ **Trước khi tạo phải đọc hệ thống thiết kế [card-design](../card-design/SKILL.md)** (chọn lập trường/khoá bảng màu/chữ càng lớn càng mảnh/cấm cảm giác AI rẻ tiền). Thẻ câu đắt đặc biệt sống nhờ phân cấp bố cục - tránh chữ gradient, tiêu đề đen đậm, căn giữa mọi thứ.

## Bộ khung (chọn 1 trong 2, tuỳ nội dung là "quan điểm" hay "con số")

Trước tiên theo card-design chọn phong cách và khoá bảng màu, rồi áp bộ khung tương ứng bên dưới.

### A. Thẻ câu đắt (một quan điểm hero)

- Khung chứa `w-[1600px] h-[900px]`, chọn nền tối / nền sáng tuỳ cảm xúc nội dung.
- Giữa thẻ là một câu hero đắt (**chữ càng lớn càng mảnh**, giới hạn 2-3 dòng, từ đắt nhất dùng 1 màu nhấn).
- Bên dưới là chữ ký / nguồn trích (không có handle cá nhân thì dùng tên nguồn hoặc tên thương hiệu, đừng nhét chỗ trống ảnh đại diện).
- Góc trên bên trái gắn nhãn nhỏ (`Insight` / `Quan điểm` / `Quote`); góc dưới bên phải là watermark thương hiệu.
- Vân nền tinh tế (grid / dot / noise rất nhạt), cấm glassmorphism và chữ gradient.

### B. Thẻ số liệu (một cụm số chính)

- Cùng khung hình, 1 số chính **cỡ chữ cực lớn** (chiếm tâm thị giác) + đơn vị/chú thích chữ nhỏ bên cạnh.
- 2-4 chỉ số phụ xếp ngang, mỗi cái là "số lớn + một dòng nhãn", căn theo lưới.
- Có thể thêm một câu kết luận/chú thích nguồn (`Nguồn dữ liệu · tính đến X`) để tăng độ tin cậy.
- Số dùng font đều nét hoặc Inter Tight, tránh dùng emoji làm icon.

## Thích ứng theo nền tảng

- **Facebook**: khung ngang gắn thẳng vào bài; câu đắt phải ngắn, tách ra share riêng vẫn hiểu; watermark để tên thương hiệu.
- **LinkedIn**: thiên về lý tính, thẻ số liệu + một câu kết luận là hợp nhất; nguồn trích phải rõ.
- **Blog/website**: dùng làm ảnh minh hoạ trong bài hoặc mở rộng thành ảnh bìa; bảng màu theo màu chủ đạo của trang.
- **X/Threads (thị trường quốc tế)**: giữ handle trong phần chữ ký; còn lại giống thẻ câu đắt.

## Render ra ảnh (bắt buộc, đừng chụp màn hình thủ công)

Sau khi tạo HTML, dùng script render dùng chung để tự xuất ảnh (playwright + chromium, đã cấu hình đi qua proxy để tải CDN/font):

```bash
python skills/shared/scripts/render_card.py \
  --html "outputs/<chủ đề>/assets/card.html" \
  --out "outputs/<chủ đề>/card.png" \
  --full-page --width 1600 --height 900
```

- Khung ngang 16:9 dùng `--width 1600 --height 900`.
- Script đặt timeout có giới hạn cho CDN/font bên ngoài (mặc định quá 20s vẫn chạy tiếp), không treo; dùng proxy môi trường để tải Tailwind/Google Fonts.
- Lần đầu dùng cần `pip install playwright && playwright install chromium` (xem phần phụ thuộc của dự án).

## Khác biệt với các SKILL thẻ khác

Cả ba đều là "HTML một ảnh → chụp màn hình", chỉ khác khung hình và tình huống, không thay thế nhau:

- **card-quote (SKILL này)** = thẻ câu đắt/số liệu khung ngang 16:9, một quan điểm hero hoặc một cụm số chính, hợp Facebook / LinkedIn / X / blog.
- **card-xiaohongshu** = thẻ kiến thức dọc 1080×1440 (theo thư viện phong cách card-design), ghép nhiều tấm để lướt được. Dùng khi cần chở nhiều quan điểm, bộ kiến thức trọn gói.
- **poster-hero** = poster marketing dọc 1080×1920 / ảnh chia sẻ lên story/feed, tiêu đề lớn + điểm bán + mã QR, dùng cho ra mắt sản phẩm, quảng bá sự kiện.
