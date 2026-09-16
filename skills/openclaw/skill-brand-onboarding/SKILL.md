---
name: skill-brand-onboarding
description: >-
  Onboarding kênh/thương hiệu: phỏng vấn bài bản về hình ảnh, tone, khán giả, mục tiêu; sinh hồ sơ
  (Profile) đầy đủ. Dùng khi người dùng nói "onboarding", "tạo hồ sơ kênh", "hồ sơ thương hiệu",
  "xây kênh từ đầu". Chỉ giọng văn → skill-voice-builder, chỉ khán giả → skill-audience-profiler.
layer: plan
---

# Onboarding thương hiệu

> Qua phỏng vấn bài bản + thu thập thông tin công khai, sinh hồ sơ kênh Easel (Profile) đầy đủ cho nhà sáng tạo/thương hiệu.

## Đầu vào

Người dùng cung cấp tên thương hiệu/kênh, kèm tuỳ chọn: link mạng xã hội, ảnh chụp màn hình, tài liệu thương hiệu.

## Đầu ra

Thư mục `profiles/<name>/`, gồm:

| File | Nội dung |
|------|------|
| `identity.md` | Tên thương hiệu, định vị, sứ mệnh, điểm khác biệt, sản phẩm/dịch vụ cốt lõi |
| `style.md` | Phong cách hình ảnh, voice/tone, nhịp nội dung, quy tắc Do/Don't |
| `audience.md` | Hồ sơ khán giả mục tiêu, ngôn ngữ người dùng, nỗi đau và nhu cầu |
| `platforms.md` | Nền tảng đang hoạt động, thông tin kênh, tần suất đăng, chiến lược hashtag |
| `preferences.md` | Trụ cột nội dung, sản phẩm chủ lực, chủ đề cấm, lằn ranh tuân thủ |
| `memory.md` | Ban đầu để trống, lớp quy kết cập nhật sau |

---

## Phase 0 - Chuẩn bị môi trường

1. Hỏi tên hồ sơ (chữ thường tiếng Anh, dùng làm tên thư mục, ví dụ `my-brand`)
2. Kiểm tra `profiles/<name>/` đã tồn tại chưa:
   - Đã có → tóm tắt nội dung hiện tại, hỏi: cập nhật hay dựng lại?
   - Chưa có → tiếp tục
3. Bảo đảm thư mục `profiles/<name>/` tồn tại

---

## Phase 1 - Thu thập thông tin

**Thu thập thông tin công khai trước, rồi mới hỏi người dùng bù chỗ thiếu.**

### Bước 1: Thu thập link mạng xã hội

Hỏi người dùng (có cái nào đưa cái đó):
- Link trang chủ hoặc ID trên Facebook / TikTok / YouTube / Zalo
- Website cá nhân / tên fanpage hoặc blog
- Brand guideline, file VI, ảnh chụp màn hình đã có (có thể đưa đường dẫn file)

### Bước 2: Trích xuất thông tin công khai

Với mỗi link, dùng WebFetch lấy trang công khai và trích:

**Dữ kiện xác nhận được (ghi rõ nguồn):**
- Tên thương hiệu, nickname kênh, mô tả/chữ ký
- Địa bàn, phạm vi phục vụ
- Nhóm sản phẩm hoặc dịch vụ
- Giá trị thương hiệu (nếu phần mô tả có nêu)
- Số liệu mạng xã hội: người theo dõi, lượt thích và lưu, số bài/video
- Quan sát hình ảnh: phong cách ảnh bìa, gu filter, thói quen dàn trang, tông màu chủ đạo

Thông tin WebFetch không lấy được thì đánh dấu là chỗ thiếu cần xác nhận.

**Chỗ thiếu chỉ người dùng trả lời được:**
- Màu thương hiệu chính xác (mã hex), tên font
- Mô tả nhóm khán giả mục tiêu (ICP)
- Sản phẩm/dịch vụ chủ lực, điểm khác biệt cốt lõi
- Mục tiêu vận hành mạng xã hội, hiện trạng đang chạy
- Định dạng nội dung đặc trưng và ví dụ bài viết thật
- Những điều tuyệt đối không làm

---

## Phase 2 - Soạn sẵn tài liệu phỏng vấn

Sinh tài liệu phỏng vấn gửi người dùng, ghi vào `outputs/<chủ đề>/onboarding-thuong-hieu.md`.

**Tài liệu gồm bốn phần:**

**Phần một - Những gì chúng ta đã nắm được**
Trình bày các dữ kiện đã xác nhận ở Phase 1 dưới dạng khẳng định để người dùng đối chiếu và sửa.
> "Thông tin trên đã chính xác chưa? Có gì thiếu hoặc cần sửa không?"

**Phần hai - Những câu bạn cần trả lời** (chỉ hỏi chỗ thiếu thật sự)
1. Khán giả mục tiêu là ai? (ICP)
2. Sản phẩm/dịch vụ chủ lực?
3. Khác biệt lớn nhất so với các kênh cùng loại?
4. Mục tiêu cốt lõi trên mạng xã hội? (tăng người theo dõi / bán hàng / nhận diện thương hiệu / cộng đồng - chọn 1-2)
5. Nhịp vận hành hiện tại? Cái gì hiệu quả, cái gì không?

**Phần ba - Danh sách tư liệu**
Bắt buộc: mã màu thương hiệu, Logo, ảnh chụp thật sản phẩm (ảnh gốc độ phân giải cao)
Có thì tốt: ảnh bối cảnh, brand guideline, ảnh chụp bài tiêu biểu, kênh bạn thích/muốn tránh

**Phần bốn - Chi tiết thương hiệu và nội dung**
- Gu trình bày chữ, định dạng nội dung đặc trưng
- 3-5 ví dụ bài viết thật (ghi chú "đầu vào giá trị nhất")
- Trụ cột nội dung (tick chọn + tự thêm)
- Nội dung tuyệt đối không đăng, tỉ lệ các dạng nội dung, mốc quan trọng sắp tới

Điều chỉnh giọng tài liệu theo tone thương hiệu.

---

## Phase 3 - Rà tư liệu và câu trả lời

Sau khi người dùng gửi lại tài liệu đã điền và tư liệu:

1. **Xử lý tư liệu** - Logo → `profiles/<name>/assets/logo.png`; ảnh sản phẩm → `assets/products/`; ảnh bối cảnh → `assets/lifestyle/`; bài mẫu → `assets/examples/`
2. **Gộp câu trả lời** - hợp nhất câu trả lời của người dùng với dữ liệu thu ở Phase 1, xác định chỗ còn thiếu
3. **Hỏi bù** - nếu còn chỗ thiếu quan trọng thì hỏi thẳng vào đó (không quá 3 câu)

---

## Phase 4 - Sinh hồ sơ Profile

Tổng hợp mọi thông tin rồi ghi vào các file trong `profiles/<name>/`.

Sinh sáu file theo cấu trúc mẫu trong [profile-templates.md](references/profile-templates.md):
- `identity.md` - thông tin cơ bản, sản phẩm cốt lõi, điểm khác biệt, hướng nội dung
- `style.md` - voice/tone, phong cách hình ảnh, định dạng đặc trưng, ví dụ bài viết, Do/Don't
- `audience.md` - ICP, ngôn ngữ người dùng, nỗi đau và nhu cầu, đặc điểm tương tác
- `platforms.md` - số liệu kênh trên từng nền tảng, dạng nội dung, tần suất đăng, hashtag
- `preferences.md` - trụ cột nội dung, sản phẩm chủ lực, vùng cấm, lằn ranh tuân thủ, mục tiêu vận hành
- `memory.md` - mẫu trống ban đầu

Thông tin chưa có thì đánh dấu `[chờ bổ sung]`, không bịa. Ước lượng từ ảnh chụp thì ghi `(ước lượng)`.

---

## Phase 5 - Chốt bản cuối

Trình bày hồ sơ hoàn chỉnh cho người dùng, xác nhận từng file:

1. Có sai sót dữ kiện nào không?
2. Có phần nào không phù hợp cần xoá không?
3. Có chỗ nào thiếu cần bổ sung không?

Sửa xong thì xác nhận:

> "Hồ sơ đã lưu tại `profiles/<name>/`. Mọi SKILL của Easel sẽ tự đọc hồ sơ này."

---

## Ghi chú vận hành

- **Bắt buộc thu thập thông tin công khai trước khi sinh tài liệu phỏng vấn** - điền sẵn thứ đã biết cho thấy sự chuyên nghiệp, người dùng cũng hoàn thành nhanh hơn
- **Định dạng nội dung đặc trưng và ví dụ bài viết thật là đầu vào quan trọng nhất** - đây là thứ giúp nội dung sinh ra giống chính chủ chứ không phải AI chung chung
- **Màu thương hiệu là đầu vào hình ảnh quan trọng thứ hai** - sai mã màu thì mọi sản phẩm hình ảnh đều sai, cái nào ước lượng thì ghi "(ước lượng)"
- **Không bịa chi tiết thương hiệu** - thông tin chưa có thì ghi `[chờ bổ sung]`
- **Không được bỏ qua khán giả và mục tiêu vận hành** - không có ICP và mục tiêu thì mọi khâu lên kế hoạch nội dung về sau đều chung chung
