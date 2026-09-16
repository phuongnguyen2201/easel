---
name: skill-trend-rider
description: >-
  Lên phương án bắt một trend/sự kiện nóng cụ thể theo định vị kênh: độ liên quan, góc vào, hình
  thức, gợi ý tiêu đề, cảnh báo rủi ro. Dùng khi người dùng nói "trend này bắt sao", "bắt trend",
  "đu trend", "trend này có liên quan tới tôi không". skill-trending-topics chỉ tìm và lọc trend.
layer: plan
---

# Phương án bắt trend

> Đưa vào một sự kiện đang nóng, kết hợp định vị của nhà sáng tạo, xuất phương án nội dung bắt trend cụ thể.

## Đầu vào

| Tham số | Bắt buộc | Mô tả |
|------|------|------|
| Sự kiện nóng | Có | Mô tả chủ đề/sự kiện nóng hoặc từ khoá |
| Nền tảng mục tiêu | Không | Nền tảng đăng bài (có Profile thì tự lấy) |
| Ngách của nhà sáng tạo | Không | Ví dụ "công nghệ số", "làm đẹp" (có Profile thì tự lấy) |

## Đầu ra

```markdown
# Phương án bắt trend

## Tổng quan trend
- Sự kiện nóng: {tên sự kiện}
- Mức độ nóng: {hạng S/A/B/C}
- Vòng đời: {bùng nổ/đỉnh/suy giảm/đuôi dài}
- Cửa sổ nóng dự kiến: {còn X giờ/ngày}

## Đánh giá độ liên quan
- Độ liên quan với ngách của nhà sáng tạo: {cao/trung bình/thấp/không}
- Phân tích liên quan: {vì sao liên quan hoặc không liên quan}
- Tính khả thi khi bắt trend: {nên bắt/miễn cưỡng bắt được/không nên bắt}

## Phương án nội dung (3 góc vào)

### Phương án A: {tên góc vào} (mức khuyến nghị: ★★★★★)
- Góc vào: {vào cụ thể thế nào}
- Hình thức nội dung: {ảnh + chữ/video ngắn/livestream/thread}
- Tiêu đề ứng viên:
  1. {tiêu đề A1}
  2. {tiêu đề A2}
  3. {tiêu đề A3}
- Dàn ý nội dung: {3-5 ý chính}
- Thời gian sản xuất: {ước tính}
- Hiệu quả kỳ vọng: {dự kiến lưu lượng và kiểu tương tác}

### Phương án B: {tên góc vào} (mức khuyến nghị: ★★★★☆)
{cấu trúc như trên}

### Phương án C: {tên góc vào} (mức khuyến nghị: ★★★☆☆)
{cấu trúc như trên}

## Chiến lược đăng bài
- Thời điểm đăng tốt nhất: {khung giờ cụ thể}
- Chọn nền tảng: {nền tảng đăng đầu + thứ tự phân phối}
- Chiến lược hashtag: {hashtag chủ đề khuyến nghị}

## Cảnh báo rủi ro
- {rủi ro 1}: {đề xuất né tránh}
- {rủi ro 2}: {đề xuất né tránh}

## Lý do không bắt (xuất khi độ liên quan thấp)
{vì sao không nên bắt + đề xuất thay thế}
```

## Các bước thực hiện

1. **Bóc tách trend**
   - Bóc thông tin cốt lõi của sự kiện: chủ thể, nguyên nhân, diễn biến, điểm gây tranh cãi
   - Xác định loại trend: sự kiện xã hội, chuyện showbiz, tin ngành, thay đổi chính sách, dịp lễ, sự kiện bất ngờ
   - Đánh giá giai đoạn vòng đời của trend:
     - Bùng nổ (0-4 giờ): ưu tiên tốc độ, giành đăng sớm nhất
     - Đỉnh (4-24 giờ): ưu tiên góc vào, làm khác biệt
     - Suy giảm (1-3 ngày): ưu tiên chiều sâu, làm tổng kết/suy ngẫm
     - Đuôi dài (3 ngày+): ưu tiên hậu kiểm, rút ra phương pháp luận
   - Đánh giá mức độ nóng: hạng S (phủ khắp mạng), hạng A (cả ngành bàn tán), hạng B (bàn trong một giới), hạng C (chỉ một nhóm nhỏ quan tâm)

2. **Đánh giá độ liên quan**
   - Phân tích giao điểm giữa trend và ngách của nhà sáng tạo: có liên quan tự nhiên không, có bình luận chuyên môn được không
   - Phân mức độ liên quan:
     - Liên quan cao: trend nằm ngay trong ngách của nhà sáng tạo (như blogger công nghệ đánh giá điện thoại mới ra mắt)
     - Liên quan trung bình: trend có thể nhìn từ góc của nhà sáng tạo (như blogger công sở phân tích tin sa thải)
     - Liên quan thấp: phải gán ghép gượng ép (như blogger ẩm thực bắt trend hàng không vũ trụ)
     - Không liên quan: hoàn toàn không dính, bắt vào còn bị trừ điểm
   - Khi độ liên quan thấp hơn "trung bình", nói rõ là không nên bắt và giải thích lý do

3. **Đào góc vào**
   - Dùng 6 mô hình góc vào khi bắt trend:
     - **Phân tích chuyên môn**: nhìn trend từ góc chuyên môn (hợp nhà sáng tạo kiểu kiến thức)
     - **Nối với trải nghiệm**: kể trải nghiệm thật của mình liên quan tới trend (hợp nhà sáng tạo mạnh về persona)
     - **Công cụ/phương pháp luận**: mượn trend để dẫn ra phương pháp dùng được (hợp nhà sáng tạo kiểu kiến thức thực chiến)
     - **Quan điểm ngược**: nêu quan điểm khác dòng chính (hợp nhà sáng tạo kiểu gây tranh luận, rủi ro cao)
     - **Đồng cảm cảm xúc**: nói lên cảm xúc chung với số đông (hợp nhà sáng tạo kiểu cảm xúc)
     - **Liên tưởng mở rộng**: từ trend mở ra chủ đề lớn hơn (hợp nhà sáng tạo kiểu chiều sâu)
   - Theo định vị của nhà sáng tạo, lọc ra 3 góc vào khớp nhất

4. **Sinh phương án nội dung**
   - Sinh phương án đầy đủ cho từng góc vào:
     - Chọn hình thức nội dung: theo đặc tính nền tảng và góc vào để khớp hình thức tốt nhất
     - Tiêu đề ứng viên: mỗi phương án 3 tiêu đề, phủ các hook cảm xúc khác nhau
     - Dàn ý nội dung: 3-5 ý cốt lõi, bảo đảm logic trọn vẹn
     - Ước tính thời gian sản xuất: dựa vào độ phức tạp của hình thức để đưa con số dự kiến
   - 3 phương án xếp theo mức khuyến nghị, cân nhắc chung độ liên quan, độ khó sản xuất, hiệu quả kỳ vọng

5. **Lập chiến lược đăng bài**
   - Theo vòng đời của trend để chốt khung giờ đăng tốt nhất
   - Chiến lược phân phối đa nền tảng: nền tảng đăng đầu, thứ tự phân phối lại, cách chỉnh nội dung cho từng nền tảng
   - Chiến lược hashtag: hashtag chủ đề chính thức + tổ hợp hashtag đuôi dài

6. **Đánh giá rủi ro**
   - Rà từng điểm rủi ro:
     - Nhạy cảm chính trị: có dính chính sách, quan hệ quốc tế, hệ tư tưởng không
     - Rủi ro pháp lý: có dính sự việc chưa có kết luận, vi phạm bản quyền, quyền riêng tư không
     - Dư luận lật ngược: sự việc có thể lật ngược khiến bài đăng phản tác dụng không
     - Tranh cãi đạo đức: bắt trend này có bị nghi là "ăn theo nỗi đau người khác" không
     - Quy định nền tảng: có chạm lằn ranh đỏ về nội dung của nền tảng không
   - Mỗi điểm rủi ro kèm đề xuất né tránh cụ thể

7. **Bàn giao kết quả**
   - Sinh phương án đầy đủ theo định dạng đầu ra
   - Khi độ liên quan bị chấm là "không", bỏ qua phần sinh phương án, xuất thẳng "Lý do không bắt" và gợi ý hướng thay thế

## Nhận biết Profile

**Khi có Profile:**
- Đọc `identity.md` để lấy định vị ngách, chấm độ liên quan chính xác
- Đọc `audience.md` để lấy hồ sơ (Profile) khán giả, đánh giá mức quan tâm của họ với trend này
- Đọc `style.md` để khớp hình thức nội dung và cách diễn đạt
- Đọc `platforms.md` để chốt nền tảng đăng đầu và chiến lược phân phối
- Đọc `tone.md` (nếu có) để bảo đảm tiêu đề và dàn ý đồng giọng

**Khi không có Profile:**
- Đánh giá độ liên quan lùi về chế độ chung, yêu cầu người dùng tự cung cấp thông tin ngách
- Phương án nội dung không đặc thù hoá theo nền tảng, đưa bản dùng chung
- Nhắc "cung cấp Profile sẽ có đánh giá độ liên quan và khớp góc vào chính xác hơn"

## Quy tắc

1. Khi độ liên quan là "không" thì bắt buộc khuyên không bắt, không được cố sinh phương án
2. Tiêu đề của mỗi phương án phải chứa từ khoá của trend, bảo đảm tìm kiếm thấy được
3. Cảnh báo rủi ro phải trung thực, không được làm nhẹ rủi ro để người dùng chịu bắt trend
4. Trend dính sự việc tiêu cực (thiên tai/tai nạn/người mất), cấm gợi ý góc vào nào ngoài "đồng cảm cảm xúc"
5. Ghi rõ mức gấp về thời gian, trend đang bùng nổ phải nhắc người dùng "làm ngay bây giờ"
6. Các phương án không được trùng góc vào, phải đưa ra những điểm vào thực sự khác nhau

> Nguồn gốc tự phát triển và hướng tham khảo xem `EASEL-META.md` cùng thư mục.
