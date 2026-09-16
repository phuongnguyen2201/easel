---
name: skill-profile-builder
description: >-
  Sinh hồ sơ (Profile) 6 chiều từ đầu khi mới dùng Easel: từ link kênh và ý định vận hành, phân
  tích bài đã đăng, gu lưu/thích. Dùng khi người dùng nói "tạo hồ sơ từ link", "lần đầu dùng",
  "phân tích kênh ra hồ sơ". Hồ sơ có sẵn (sửa, memory, xuất, so sánh, chuyển) →
  skill-profile-manager.
layer: general
---

# Bộ dựng Profile (dẫn dắt lần đầu)

> Biến "hồ sơ trống/nửa vời" thành "Profile 6 chiều dùng được". Người dùng chạy skill này đầu tiên khi mới dùng Easel: thu link mạng xã hội + ý định vận hành -> phân tích bài đã đăng/gu lưu-thích -> sinh 6 file chiều trong `profiles/<tên>/`. Sinh xong thì giao cho [account-diagnosis](../skill-account-diagnosis/SKILL.md) chẩn đoán xây kênh.

## Khác gì so với profile-manager

- **profile-builder (SKILL này)** = **sinh** hồ sơ từ 0 tới 1 (dẫn dắt khai báo + phân tích mạng xã hội + tổng hợp thành bản).
- **profile-manager** = CRUD, chuyển đổi, thêm/xoá/sửa trường của hồ sơ đã có.

## Đầu vào

Người dùng cung cấp theo nhu cầu (thiếu thì hỏi thêm để bù, không bịa):

| Mục | Mô tả |
|----|----|
| Tên hồ sơ | Một persona = một hồ sơ (không phải một nền tảng), ví dụ "chuyên gia công nghệ - đồ số" |
| Link mạng xã hội | URL trang chủ ở từng nền tảng (Facebook/TikTok/YouTube/Zalo/Threads/blog-website), dùng để phân tích bài đã đăng và gu lưu-thích |
| Ý định vận hành | Muốn làm hướng nào, vì sao làm, đặc điểm/thế mạnh/nguồn lực của bản thân |
| Gu nội dung | Thích xem loại nào, muốn làm ra loại nào, kênh tham khảo/đối chuẩn |
| Lằn ranh đỏ | Nội dung nhất định không làm, đáy tuân thủ |

## Đầu ra

Sinh 6 file trong `profiles/<tên hồ sơ>/` (cấu trúc xem `profiles/_template/`):
`identity.md` / `style.md` / `audience.md` / `platforms.md` / `preferences.md` / `memory.md`.
Mỗi trường ghi rõ nguồn: `[người dùng tự khai]` / `[phân tích link]` / `[cần bổ sung]`.

## Các bước thực hiện

1. **Chốt tên hồ sơ**, kiểm tra `profiles/<tên>/` đã tồn tại chưa (có rồi thì hỏi ghi đè hay bổ sung). Chưa có thì copy `profiles/_template/` làm khung.

2. **Thu link mạng xã hội**. Theo danh sách trong [onboarding-questions.md](references/onboarding-questions.md), dẫn người dùng đưa link trang chủ và thông tin cơ bản.

3. **Phân tích link mạng xã hội**. Theo [social-link-analysis.md](references/social-link-analysis.md), dùng web_fetch lấy phần nội dung công khai lấy được (tiêu đề/đề tài/tương tác của bài gần đây, mục lưu/thích công khai), rồi suy ra: đề tài hay đăng, phong cách giọng điệu, hồ sơ khán giả, đặc điểm nội dung tương tác cao.
   - Khi bị chặn thu thập (đa số nền tảng chống bot) thì **hạ cấp**: nói rõ cái nào không lấy được, chuyển sang để người dùng kể + hỏi thêm cho đủ, **không bịa dữ liệu**.

4. **Thu ý định vận hành và gu**. Theo onboarding-questions.md, hỏi lần lượt từng chiều: hướng muốn làm, lý do, đặc điểm/nguồn lực của bản thân, gu nội dung, kênh đối chuẩn, lằn ranh đỏ.

5. **Tổng hợp sinh 6 chiều**. Trộn [phân tích link] với [người dùng tự khai], điền theo các trường của từng file trong `profiles/_template/`:
   - identity <- định vị/khác biệt hoá/hướng nội dung
   - style <- giọng điệu/cấu trúc mở đầu/hình ảnh/nhịp/yếu tố nhận diện (ưu tiên phong cách xuất hiện nhiều trong phân tích link)
   - audience <- nhóm cốt lõi/sở thích/nỗi đau/đặc điểm tương tác
   - platforms <- tên tài khoản từng nền tảng/quy mô người theo dõi/hình thức nội dung (lấy từ link)
   - preferences <- làm gì/không làm gì/đáy tuân thủ
   - memory <- lần đầu để trống hoặc chỉ ghi insight sơ bộ rút từ phân tích link

6. **Đánh dấu chỗ thiếu + hỏi thêm**. Chiều nào thiếu thông tin thì ghi ngay `[cần bổ sung]` tại chỗ đó và **liệt kê các câu hỏi cụ thể cần người dùng trả lời** (làm thành plan để người dùng bù từng mục), không lấp đầy bằng câu chữ sáo rỗng.

7. **Ghi file và báo lại**. Ghi các file trong `profiles/<tên>/`, xuất một bản tóm tắt "đã sinh hồ sơ": mức hoàn thiện từng chiều, phần nào từ phân tích link, phần nào còn thiếu, và gợi ý bước tiếp theo là chạy account-diagnosis.

## Nhận biết Profile

SKILL này **sinh** Profile chứ không tiêu thụ. Chất lượng sinh ra phụ thuộc vào mức lấy được dữ liệu từ link người dùng đưa và độ đầy đủ của phần tự khai - thông tin càng đủ thì account-diagnosis sau đó càng chuẩn.
