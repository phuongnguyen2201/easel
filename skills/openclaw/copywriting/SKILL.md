---
name: copywriting
description: >-
  Chắt lọc điểm bán, viết tiêu đề, thân, CTA bán hàng cho seeding, quảng cáo, khuyến mãi, trang
  sản phẩm, landing page. Dùng khi người dùng nói "bài seeding", "viết quảng cáo", "mô tả sản
  phẩm". Bài ảnh-chữ trọn bộ → xhs-note-creator, tăng follow → social-content, ép khung →
  post-formatter.
layer: produce
---

# Viết nội dung marketing

> Viết và tối ưu nội dung chuyển đổi cao cho bối cảnh marketing trong nước: seeding, quảng cáo feed, chắt lọc điểm bán, khuyến mãi sự kiện, trang chi tiết sản phẩm, landing page. Áp khung kinh điển, đặt vào ngữ cảnh trong nước.

## Ranh giới trách nhiệm

| Tình huống | Giao cho ai | Vì sao |
|------|--------|--------|
| **Nội dung marketing hướng bán hàng/chuyển đổi** (điểm bán seeding, quảng cáo feed, sự kiện, trang sản phẩm, landing page) | **SKILL này** | Lấy mục tiêu "thúc đẩy mua/chuyển đổi", nói điểm bán, nói lợi ích, đưa CTA |
| **Bài ảnh-chữ trọn bộ** (nhiều thẻ + caption + hashtags + khử mùi AI + kiểm tra cả quy trình) | `xhs-note-creator` | Cửa vào chính cho bài ảnh-chữ/seeding, không phải một đoạn nội dung lẻ |
| Nội dung social phổ thông (định dạng bản địa đa nền tảng, hook, hashtag, dẫn dắt tương tác) | `social-content` | Thiên về vận hành nội dung/tăng follow, không ép chuyển đổi |
| Bài có cấu trúc ép đúng khung PAS/AIDA/BAB/STAR (200-250 chữ, dàn trang cho mobile) | `post-formatter` | Chuyên làm bài chuẩn hoá theo một khung duy nhất |

Phân vai một câu: **muốn bán hàng thì tìm copywriting, muốn bài ảnh-chữ trọn bộ thì tìm xhs-note-creator, muốn tăng follow thì tìm social-content, muốn ép khung cố định và dàn trang thì tìm post-formatter.** Có thể nối chuỗi (SKILL này ra nội dung điểm bán → post-formatter dàn thành bài → social-content thích ứng nhiều nền tảng).

## Đầu vào

Người dùng cung cấp các thông tin sau trong prompt (thiếu thì chủ động hỏi):

1. **Loại nội dung** - seeding / quảng cáo feed / chắt lọc điểm bán / khuyến mãi sự kiện / trang sản phẩm / landing page
2. **Sản phẩm/dịch vụ** - bán gì, điểm bán cốt lõi, khác gì đối thủ, mang lại kết quả gì
3. **Hành động mục tiêu** - muốn người dùng làm gì (đặt hàng, nhận voucher, thêm giỏ, bấm link, nhắn tin tư vấn, tới cửa hàng)
4. **Bối cảnh/nền tảng chạy** - Facebook / feed quảng cáo TikTok / quảng cáo story-feed / sàn thương mại điện tử / landing page... (ảnh hưởng độ dài, giọng, dạng CTA)
5. **Tư liệu làm bằng chứng** (nếu có) - doanh số, đánh giá, thành phần/thông số, case, chứng nhận
6. **Khán giả** - ai đọc, băn khoăn gì khi mua

## Đầu ra

Giao đúng cấu trúc theo loại nội dung (chi tiết xem `references/copy-frameworks.md`), thường gồm:

- **Tiêu đề chính/hook mở đầu** + 2-3 phương án dự phòng
- **Thân bài** (tổ chức theo khung đã chọn: điểm đau → giải pháp → điểm bán → tin cậy → CTA...)
- **Danh sách điểm bán** (FAB: tính năng → ưu thế → lợi ích, từng dòng)
- **CTA/dẫn dắt hành động** + 2-3 phương án dự phòng
- **Chú thích các yếu tố then chốt**: nói rõ lý do chọn và khung/nguyên tắc đã dùng

## Các bước thực hiện

1. **Thu thập bối cảnh** - xác nhận loại nội dung, điểm bán sản phẩm, hành động mục tiêu, bối cảnh chạy, khán giả, bằng chứng; thiếu gì chủ động hỏi.
2. **Chốt giọng** - định giọng theo Profile hoặc chỉ dẫn của người dùng (seeding thiên gần gũi chân thật, feed thiên nói thẳng, sự kiện thiên gấp gáp, trang sản phẩm thiên chuyên nghiệp).
3. **Chắt lọc điểm bán** - dùng FAB để dịch đặc tính sản phẩm thành lợi ích người dùng (định nghĩa khung xem `skills/shared/references/copy-frameworks.md`), xếp thứ tự chính phụ.
4. **Chọn khung, dựng cấu trúc** - theo mục đích nội dung mà chọn khung trong `skills/shared/references/copy-frameworks.md` (AIDA / PAS / FAB / 4U / BAB), rồi theo loại nội dung lấy **mẫu cấu trúc** tương ứng trong `references/copy-frameworks.md`.
5. **Viết tiêu đề/hook** - dùng công thức tiêu đề/hook trong `skills/shared/references/hook-title-formulas.md` để ra 2-3 phương án.
6. **Lấp thân bài** - đẩy từng đoạn, mỗi đoạn một luận điểm; dùng `references/natural-transitions.md` để giữ mạch nối tự nhiên, khẩu ngữ trôi chảy.
7. **Gọt phong cách + cửa khử mùi AI (bắt buộc)** - theo `references/writing-style-rules.md` để bắt phong cách **đặc thù của nội dung marketing** (nói lợi ích, tín hiệu tin cậy lên trước, câu hỏi tu từ/so sánh, CTA phải có lý do); **khử mùi AI đi theo nguồn chuẩn text-polisher và phải qua cửa** (`../text-polisher/references/{phrases-to-remove,structures-to-avoid,zh-ai-markers}.md`) - tự chấm mùi AI **≥45/50**, chất lượng tổng **≥35/50**, chưa đạt thì sửa rồi mới giao. SKILL này không giữ bản sao quy tắc khử AI.
8. **Viết CTA** - theo hành động mục tiêu, ra 2-3 phương án CTA.
9. **Kiểm số chữ (bắt buộc với loại có ràng buộc độ dài)** - quảng cáo feed, màn đầu trang sản phẩm, landing page... có giới hạn ký tự/dung lượng thì dùng script để phán, không đếm bằng mắt:
   ```bash
   python3 skills/shared/scripts/wordcount.py count -f "outputs/<chủ đề>/copy.txt"
   ```
   Đọc `social_count` rồi đối chiếu với giới hạn ký tự của vị trí đăng, vượt thì giao `text-condenser` nén rồi đếm lại.
10. **Lắp ráp và giao** - ráp nội dung + chú thích + phương án dự phòng theo định dạng "Đầu ra", ghi vào `outputs/`.

## Nguyên tắc cốt lõi khi viết

- **Rõ ràng trước tiên** - khi rõ ràng xung đột với sáng tạo thì chọn rõ ràng, người đọc hiểu đang bán gì trong 3 giây.
- **Nói lợi ích chứ không nói tính năng** - tính năng nói "nó là gì", lợi ích nói "điều đó nghĩa là gì với bạn" (cốt lõi của FAB).
- **Phải cụ thể** - "8 giờ sáng ra khỏi nhà trong 10 phút vẫn kịp giờ" > "tiết kiệm thời gian, hiệu quả"; có số thì dùng số.
- **Dùng lời của người dùng** - soi gương cách nói thật trong bình luận, bài viết, tin nhắn tư vấn, đừng dùng từ tự sướng của thương hiệu.
- **Mỗi đoạn một luận điểm** - mỗi đoạn chỉ đẩy một luận cứ, dựng chuỗi "rung động → tin tưởng → hành động" dọc bài.
- **Tín hiệu tin cậy lên trước** - quyết định mua trong nước nặng về đánh giá và tâm lý đám đông, nên doanh số/đánh giá/chứng nhận phải xuất hiện sớm.
- **CTA phải có lý do** - đừng chỉ nói "bấm mua", kèm theo vì sao phải mua ngay (giới hạn thời gian, giới hạn số lượng, quà tặng, mỏ neo giá).

## Lướt nhanh các loại nội dung

Mẫu cấu trúc và điểm mấu chốt của từng loại xem `references/copy-frameworks.md` (định nghĩa khung xem `skills/shared/references/copy-frameworks.md`). Khác biệt cốt lõi:

| Loại | Khung chính | Giọng | Mấu chốt |
|------|----------|------|------|
| Bài seeding | Điểm đau-giải pháp / trải nghiệm thật | Gần gũi, chân thật, bớt mùi quảng cáo | Đặt vào bối cảnh, trải nghiệm thật, tránh quảng cáo lộ liễu bị bóp tương tác |
| Quảng cáo feed | AIDA / 4U | Nói thẳng, bắt mắt | Dòng đầu định sống chết, lợi ích lên trước, CTA rõ ràng |
| Chắt lọc điểm bán | FAB | Cô đọng | Dịch từng dòng tính năng → ưu thế → lợi ích, xếp chính phụ |
| Sự kiện/khuyến mãi | Gấp gáp + mỏ neo giá trị | Có nhịp, có sức ép thời gian | Mức ưu đãi rõ, tạo gấp gáp, giảm chi phí ra quyết định |
| Trang sản phẩm | FAB + xử lý phản đối | Chuyên nghiệp, đáng tin | Phân tầng điểm bán, trực quan hoá thông số, dẹp băn khoăn |
| Landing page/trang sản phẩm | AIDA + khối có cấu trúc | Tuỳ khán giả | Tuyên ngôn giá trị ở màn đầu, bảo chứng tin cậy, một CTA chính duy nhất |

## Nhận biết Profile

- **Có Profile**: đọc `style.md` (giọng/phong cách diễn đạt), `audience.md` (hồ sơ khán giả), `preferences.md` (lằn ranh đỏ, điều cấm kỵ), chỉnh tông giọng, câu chữ, góc điểm bán khớp hết với Profile.
- **Không có Profile**: chủ động hỏi giọng ưa thích (gần gũi/chuyên nghiệp/gấp gáp), khán giả, cá tính thương hiệu; không có thì lùi về giọng chuyên nghiệp phổ thông, cuối bản giao ghi chú "nếu cung cấp Profile của kênh sẽ có nội dung bám thương hiệu hơn".
