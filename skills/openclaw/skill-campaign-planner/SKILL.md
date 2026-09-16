---
name: skill-campaign-planner
description: >-
  Lập kế hoạch campaign cho Tết, sale 11.11/Black Friday, ra mắt sản phẩm, sự kiện: mục tiêu, nhịp
  khởi động – bùng nổ – kéo dài, ma trận nội dung đa kênh, minigame, phân tầng KOL, ngân sách, rủi
  ro, KPI. Dùng khi người dùng nói "kế hoạch marketing", "chạy campaign Tết", "sale 11.11 làm gì".
layer: plan
---

# Lập kế hoạch sự kiện / marketing (campaign-planner)

> Ra một phương án campaign marketing chạy được thật, phủ mục tiêu -> nhịp -> ma trận nội dung -> minigame -> nguồn lực -> rủi ro -> chỉ số hậu kiểm.
> Phương pháp chuyên môn nằm ở `references/campaign-frameworks.md`, file này chỉ nói quy trình. **Định nghĩa quy tắc và mô hình, không áp case cụ thể.**

> Bắt trend cho một đề tài đơn lẻ xem skill-trend-rider; quy hoạch nội dung theo series xem skill-content-strategy;
> Booking quảng cáo/collab xem skill-collab-proposal; SKILL này lo **toàn bộ kế hoạch cho một campaign marketing**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Loại campaign | Có | Marketing dịp lễ / đợt sale lớn sàn TMĐT / ra mắt sản phẩm / tạo sóng sự kiện / kỷ niệm thành lập... |
| Mục tiêu | Nên có | Tăng follow / chuyển đổi / độ phủ / kéo khách mới / xả tồn kho (quyết định nhịp và trọng tâm minigame) |
| Thời gian | Nên có | Ngày diễn ra / mốc đợt sale lớn (quyết định lịch khởi động - bùng nổ - kéo dài) |
| Nguồn lực | Tuỳ chọn | Ngân sách, nền tảng dùng được, có KOL/KOC hay không, sản phẩm/mức ưu đãi |

Thiếu thông tin thì bổ sung các mục then chốt (loại/mục tiêu/thời gian) trước, rồi mới ra phương án.

## Các bước thực hiện

1. **Xác định loại campaign và mục tiêu cốt lõi**, đọc `references/campaign-frameworks.md` mục "I. Ánh xạ mục tiêu -> cách đánh" để chốt cách đánh chính
   (kiểu độ phủ/kiểu chuyển đổi/kiểu kéo khách mới có trọng tâm chiến lược khác nhau).
2. **Dựng nhịp campaign**: theo mục "II. Mô hình nhịp marketing" tách thành giai đoạn khởi động / bùng nổ / kéo dài (đợt sale lớn thêm các mốc gom nhu cầu / chốt thanh toán),
   mỗi giai đoạn chốt mục tiêu, trọng tâm nội dung, mật độ đăng.
3. **Xếp ma trận nội dung**: theo mục "III. Ma trận nội dung", xếp bảng giai đoạn x nền tảng x định dạng nội dung (nền tảng nào lo seeding/chuyển đổi/tạo sóng).
   Việc thích ứng đa nền tảng giao cho skill-content-repurposing triển khai.
4. **Thiết kế minigame tương tác**: từ mục "IV. Thư viện minigame" chọn cơ chế hợp mục tiêu (quay thưởng/thử thách/khoe đơn/đăng ký trước/mua chung/collab...), nói rõ cơ chế và mục đích.
5. **Phân bổ nguồn lực**: theo mục "V. Phân tầng KOL và ngân sách", đề xuất phân tầng KOL (top tạo sóng/tầm trung seeding/người thường phủ số lượng) và tỉ lệ ngân sách ước lượng.
6. **Rủi ro và tuân thủ**: theo mục "VI. Rủi ro và lằn ranh tuân thủ", liệt kê bẫy thường gặp của loại campaign này (quảng cáo sai sự thật, dụ dỗ, quy định nền tảng, khủng hoảng truyền thông).
7. **Chỉ số hiệu quả**: theo mục "VII. Chỉ số hiệu quả", đưa KPI đo được theo từng giai đoạn và cách tính khi hậu kiểm (kết hợp skill-social-performance-review).
8. Xuất phương án có cấu trúc: mục tiêu -> bảng lịch nhịp -> bảng ma trận nội dung -> minigame -> nguồn lực/ngân sách -> rủi ro -> KPI.

## Nhận biết Profile

- Có Profile: mục tiêu/nền tảng/tông giọng bám `identity.md`+`platforms.md`; minigame và giọng bài viết khớp `style.md`;
  tuân thủ theo lằn ranh trong `preferences.md`; đề xuất ngân sách/KOL khớp quy mô kênh.
- Không có Profile: ra phương án chung theo loại campaign, ghi chú cần người dùng bổ sung thông tin ngân sách/nền tảng/sản phẩm để tinh chỉnh.

## Quy tắc

1. Phương án bắt buộc **chạy được thật**: đưa lịch nhịp cụ thể, phân vai nền tảng, cơ chế minigame, không viết khẩu hiệu suông.
2. Nhịp là cốt lõi - khởi động gom nhu cầu, bùng nổ dồn lực, kéo dài chốt hạ, đừng rải đều hoả lực.
3. Minigame phục vụ mục tiêu: kiểu chuyển đổi nặng ưu đãi/tính cấp bách, kiểu độ phủ nặng chủ đề/cảm giác tham gia, đừng chất bừa minigame.
4. Nói rõ rủi ro và lằn ranh tuân thủ (nhất là giá/quảng cáo trong đợt sale lớn), không đề xuất minigame dụ dỗ vi phạm.
5. Đưa KPI đo được và cách tính khi hậu kiểm, phương án khép vòng tới đánh giá hiệu quả.

## Nguồn tham khảo

Đúc kết từ phương pháp luận chung về campaign content marketing (nhịp marketing khởi động - bùng nổ - kéo dài, góc nhìn AISAS/AARRR, mốc gom nhu cầu - chốt thanh toán của đợt sale lớn,
phân tầng KOL khi chạy), bản địa hoá cho nền tảng nội địa TQ (Xiaohongshu seeding, Douyin bùng nổ, cộng đồng chuyển đổi, WeChat OA tích luỹ). Đóng khung thành mô hình
dùng lại được, không gắn với case thương hiệu cụ thể.
