# Thư mục mẫu Profile

Thư mục này là mẫu cho hồ sơ tài khoản (Profile). Khi tạo hồ sơ mới, sao chép toàn bộ thư mục `_template/` rồi đổi tên, sau đó điền nội dung thay cho phần chú thích trong từng file.

## Danh sách file và ánh xạ tầng

Luồng làm việc của Easel chia thành nhiều tầng (khám phá, lên kế hoạch, sản xuất, đăng bài, quy kết hiệu quả). Mỗi file Profile giữ một vai trò khác nhau ở từng tầng:

| File | Nội dung | Tầng sử dụng |
|------|----------|--------------|
| `identity.md` | Định vị tài khoản, điểm khác biệt, hướng nội dung | Tầng khám phá + tầng kế hoạch của OpenClaw (tham chiếu định vị) |
| `style.md` | Giọng điệu, cấu trúc mở đầu, phong cách hình ảnh, nhịp, yếu tố nhận diện | Tầng sản xuất cô đọng rồi nạp vào (điều khiển tông, nhịp và hình ảnh của thành phẩm) |
| `audience.md` | Nhóm cốt lõi, chủ đề quan tâm, nỗi đau, đặc điểm tương tác | Tầng sản xuất nạp vào + tầng kế hoạch tham chiếu (hiểu viết cho ai, viết gì) |
| `platforms.md` | Thông tin tài khoản từng nền tảng, dạng nội dung, quy tắc riêng | Chỉ tầng đăng bài dùng (thích ứng nền tảng, chuyển định dạng, kiểm tra tuân thủ) |
| `preferences.md` | Việc nên làm, không làm, giới hạn tuân thủ | Mọi tầng (quy tắc cứng và lằn ranh đỏ, bắt buộc tuân thủ suốt quy trình) |
| `memory.md` | Nhận định về nội dung, bài học thất bại, quy luật phản hồi của khán giả | Tầng sản xuất nạp vào + tầng quy kết cập nhật (đúc kết kinh nghiệm, cải tiến liên tục) |

## Mô tả chi tiết từng file

### identity.md — Tôi là ai

Xác định định vị cốt lõi và điểm khác biệt của tài khoản. Tầng khám phá của OpenClaw dùng nó để lọc xu hướng và tư liệu phù hợp; tầng kế hoạch dùng nó để đánh giá đề tài có khớp hướng đi của tài khoản không. Tầng sản xuất không nạp trực tiếp file này — định vị đã được truyền gián tiếp qua đề tài.

### style.md — Nói như thế nào

Điều khiển "cảm giác" của thành phẩm: giọng điệu (hài hước / chỉn chu / sắc sảo), cấu trúc mở đầu (đặt câu hỏi / tạo mâu thuẫn), nhịp nội dung (ngắn gọn / bài dài chuyên sâu), phong cách hình ảnh và yếu tố nhận diện. Tầng sản xuất cô đọng nó làm điểm neo phong cách, bảo đảm thành phẩm nhất quán.

### audience.md — Nói cho ai nghe

Mô tả chân dung và nhu cầu của đối tượng mục tiêu. Tầng sản xuất dựa vào đây để điều chỉnh độ sâu từ ngữ, hướng ví dụ và cách dẫn dắt tương tác; tầng kế hoạch tham chiếu để đánh giá độ khớp giữa đề tài và khán giả.

### platforms.md — Đăng ở đâu

Ghi thông tin tài khoản, dạng nội dung và quy tắc của từng nền tảng đang vận hành. Chỉ dùng ở tầng đăng bài — chuyển thành phẩm của tầng sản xuất sang định dạng từng nền tảng yêu cầu (dọc/ngang, giới hạn ký tự, quy ước hashtag...). Nền tảng không vận hành thì xoá thẳng đoạn tương ứng.

### preferences.md — Được làm gì, không được làm gì

Quy tắc cứng và lằn ranh đỏ xuyên suốt mọi tầng. Tầng khám phá dựa vào đây để lọc tư liệu không phù hợp, tầng kế hoạch để loại đề tài, tầng sản xuất để giới hạn ranh giới nội dung, tầng đăng bài để kiểm tra tuân thủ. Đây là file duy nhất bắt buộc nạp ở tất cả các tầng.

### memory.md — Đã học được gì

Đúc kết kinh nghiệm, không phải nhật ký công việc. Chỉ cập nhật khi có nhận thức thực sự tái sử dụng được (phản hồi của người dùng, quy kết hiệu quả, tổng kết thất bại). Tầng sản xuất cô đọng nó để tránh lặp lại sai lầm; tầng quy kết cập nhật nó sau khi đăng dựa trên dữ liệu phản hồi.

## Cách sử dụng

```bash
# Tạo hồ sơ mới
cp -r profiles/_template profiles/ten-ho-so-cua-ban

# Sửa từng file, điền nội dung thực tế
# Sau đó dùng được ngay trong Easel
easel skill <skill_name> -i "nội dung" -p ten-ho-so-cua-ban
```
