---
name: skill-account-diagnosis
description: >-
  Chẩn đoán kênh từ hồ sơ (Profile) + dữ liệu nội dung: độ tập trung ngách, định vị, dấu hiệu bóp
  tương tác, vòng phân phối; gợi ý xây kênh dạng bệnh → bằng chứng → đơn thuốc. Dùng khi người
  dùng nói "chẩn đoán kênh", "kênh tôi sao không lên", "có bị bóp tương tác không", "xây kênh thế
  nào".
layer: plan
---

# Chẩn đoán kênh / khám sức khoẻ khi xây kênh

> Khám và kê đơn theo lối truy nguyên cho **một kênh cụ thể**. Đọc hồ sơ do [profile-builder](../skill-profile-builder/SKILL.md) sinh ra + nội dung/dữ liệu gần đây của người dùng -> chẩn đoán sức khoẻ kênh -> đưa ý kiến xây kênh theo từng giai đoạn và gợi ý đăng bài. **Gắn chặt với hồ sơ**: chưa có Profile hoàn chỉnh thì đi chạy profile-builder trước.

## Điều kiện trước

- Bắt buộc có Profile **đã hoàn chỉnh** (`profiles/<tên>/` điền cơ bản đủ sáu chiều). Nếu Profile thiếu hoặc còn `[cần bổ sung]` trên diện rộng, **bảo người dùng chạy `skill-profile-builder` trước**, đừng cố chẩn đoán khi thông tin chưa đủ.

## Đầu vào

| Mục | Bắt buộc | Diễn giải |
|----|------|------|
| Tên hồ sơ | Có | Trỏ tới `profiles/<tên>/` |
| Dữ liệu nội dung gần đây | Không | Tiêu đề/đề tài/lượt hiển thị/tương tác của 10-30 nội dung gần nhất (có thì chẩn đoán chuẩn hơn; không có thì dựa vào Profile + hỏi thêm) |
| Vướng mắc cụ thể | Không | Ví dụ "lượt xem không lên", "có phải bị bóp tương tác không" |

## Đầu ra

Một báo cáo chẩn đoán + danh sách hành động theo từng giai đoạn:

1. **Chẩn đoán năm chiều** (mỗi chiều: hiện trạng -> bằng chứng -> kết luận), xem [diagnosis-framework.md](references/diagnosis-framework.md):
   độ tập trung ngách / độ rõ của định vị / tín hiệu bị bóp tương tác / giai đoạn vòng phân phối / độ khớp nội dung - khán giả.
2. **Bệnh -> bằng chứng -> đơn thuốc**: mọi vấn đề đều phải đủ ba đoạn, không đưa lời khuyên chung chung.
3. **Ý kiến xây kênh theo giai đoạn**: theo bậc đang đứng (0-500 / 500-5k / 5k-10k / 10k+) mà nói bậc đó cần làm gì.
4. **Gợi ý đăng bài**: ưu tiên hướng nội dung, nhịp đăng, năng lực cần bồi thêm (có thể trỏ sang SKILL phía sau: đề tài -> content-matrix, kịch bản -> video-script, tuân thủ -> quality-gate...).
5. **Khoảng trống thông tin -> Plan**: thông tin cần cho chẩn đoán mà đang thiếu (ví dụ không có dữ liệu gần đây), **liệt thành plan để hỏi người dùng**, đừng bịa dữ liệu rồi kết luận.

## Các bước thực thi

1. **Đọc sáu chiều của Profile** (identity/style/audience/platforms/preferences/memory), đánh giá độ đầy đủ. Thiếu quá nhiều -> khuyên chạy profile-builder trước rồi dừng.
2. **Thu thập dữ liệu gần đây**: người dùng đưa thì dùng; không có thì nói rõ "thiếu dữ liệu sẽ ảnh hưởng độ chính xác của chẩn đoán", và hỏi thêm ở chỗ cần (đề tài và tương tác của vài nội dung gần đây).
3. **Chẩn đoán từng chiều**: theo thước đo trong diagnosis-framework.md mà chấm hiện trạng + tìm bằng chứng + hạ kết luận cho mỗi chiều. Tín hiệu bóp tương tác thì tự soát theo từng mục trong danh sách.
4. **Xác định giai đoạn vòng phân phối**: kết hợp lượng người theo dõi + tỉ lệ tương tác gần đây để định vị bậc hiện tại.
5. **Kê đơn**: sắp các vấn đề đã chẩn ra theo "bệnh -> bằng chứng -> đơn thuốc", đơn thuốc phải cụ thể làm được ngay (không phải kiểu nói suông "tương tác nhiều lên").
6. **Đưa danh sách hành động theo giai đoạn**: các việc then chốt của bậc hiện tại + bậc kế tiếp.
7. **Liệt plan cho khoảng trống thông tin**: gom các điểm chưa chắc, cần người dùng xác nhận hoặc bổ sung dữ liệu thành một danh sách, chờ họ trả lời rồi mới làm mịn.
8. **Gợi ý hồi lưu**: các insight dùng lại được phát hiện trong lúc chẩn đoán, khuyên người dùng xác nhận rồi ghi vào `profiles/<tên>/memory.md` (SKILL này không tự sửa Profile, chỉ gợi ý).

## Nhận biết Profile

- **Có Profile**: suốt quá trình lấy định vị/phong cách/khán giả/lằn ranh đỏ của hồ sơ đó làm chuẩn để chẩn đoán - độ tập trung ngách là "lệch bao xa so với định vị ấy", chứ không phải chuẩn chung chung.
- **Profile chưa hoàn chỉnh**: dẫn sang profile-builder trước, không cố chẩn đoán.
- Kết luận chẩn đoán chỉ **gợi ý** ghi ngược vào memory, do người dùng xác nhận, tránh làm nhiễu hồ sơ.
