---
name: social-content
description: >-
  Viết bài mạng xã hội cho Facebook, TikTok, YouTube, Zalo, mặc định khi chưa rõ nền tảng: hook,
  thân, hashtag, CTA tương tác. Dùng khi người dùng nói "viết bài đăng", "viết caption", "bài tăng
  follow". Bài ảnh-chữ trọn bộ → xhs-note-creator, bán hàng → copywriting, ép khung →
  post-formatter.
layer: produce
---

# Sáng tạo nội dung mạng xã hội

> Bộ sinh nội dung mạng xã hội dùng chung/dự phòng cho mọi nền tảng. Chủ yếu phục vụ nền tảng phổ biến ở Việt Nam (Facebook / TikTok / YouTube / Zalo / blog), phụ thêm nền tảng quốc tế (X, LinkedIn), sinh hook, thân bài, chiến lược hashtag và dẫn dắt tương tác theo đúng format bản địa.

## Ranh giới trách nhiệm

SKILL này định vị là **dùng chung/dự phòng cho mọi nền tảng**: viết một lần ra nhiều nền tảng, nháp nhanh, lựa chọn mặc định khi chưa rõ nền tảng. Gặp các tình huống chuyên sâu dưới đây thì giao cho SKILL hạ nguồn làm bản tinh:

| Tình huống | Giao cho |
|------|------|
| Bài note trọn bộ kiểu Xiaohongshu (nhiều card + khử mùi AI + caption + hashtags, trọn quy trình) | `xhs-note-creator` |
| Phân cảnh/kịch bản video nói cho một video cụ thể (chấm điểm Hook, bấm giờ theo giây, tối ưu giữ chân) | `video-script` |
| Nội dung bán hàng chuyển đổi cho landing page / trang sản phẩm / trang chi tiết / feed quảng cáo (điểm bán để seeding, tiêu đề/thân bài/CTA + phương án dự phòng) | `copywriting` |
| Bài đăng có cấu trúc, ép chặt khung PAS/AIDA/BAB | `post-formatter` |

SKILL này vẫn giữ đủ năng lực tổng quát: người dùng gọi thẳng nó để làm nội dung cho nền tảng bất kỳ đều được, không bắt buộc chuyển xuống hạ nguồn.

## Đầu vào

Người dùng cung cấp các thông tin sau trong prompt (có thể bỏ bớt, SKILL tự điền giá trị mặc định):

| Trường | Mô tả | Ví dụ |
|------|------|------|
| Nền tảng | Nền tảng đích, chọn nhiều được | Facebook, TikTok, YouTube, Zalo, blog/website (dự phòng quốc tế: X, LinkedIn) |
| Loại nội dung | Bài ảnh-chữ, kịch bản video ngắn, bài dài, status ngắn, thread, carousel | Bài ảnh-chữ |
| Chủ đề | Chủ đề bài đăng hoặc tư liệu | Một đoạn văn bản hoặc URL của một bài viết |
| Mục tiêu | Tương tác, kéo traffic, thương hiệu, tìm khách, seeding, cộng đồng | Tương tác |
| Khán giả | Hồ sơ người theo dõi | Phụ nữ đi làm ở thành phố lớn |
| Tông giọng | Chuyên nghiệp, nhẹ nhàng, sắc sảo, seeding, giáo dục, truyền cảm hứng | Seeding |
| Tư liệu | Ảnh, video, số liệu có sẵn | Không có |

## Đầu ra

Với mỗi nền tảng đích, xuất theo cấu trúc sau:

### 1. Thân bài đăng theo nền tảng

```
[hook dòng đầu]

[nội dung thân bài]

[CTA dẫn dắt hành động]

[hashtag]

Số ký tự: N / giới hạn nền tảng
```

### 2. Chiến lược tương tác

- Giờ đăng tốt nhất
- Việc cần làm sau khi đăng (trả lời bình luận, chia sẻ lại...)
- Kế hoạch liên kết đa nền tảng

### 3. Hướng hình ảnh

- Mô tả ảnh minh hoạ/ảnh bìa/video kèm theo
- Dàn ý bộ card ảnh-chữ kiểu Xiaohongshu (nếu áp dụng)
- Hook kịch bản video ngắn (nếu áp dụng)

### 4. Biến thể

- Mỗi nền tảng 2-3 biến thể bài đăng, dùng cho A/B test hoặc đăng rải theo ngày.

## Các bước thực hiện

1. **Thu thập yêu cầu** - trích các trường đầu vào ở trên từ prompt của người dùng. Trường nào thiếu: có Profile thì lấy từ đó bù vào, không có Profile thì dùng giá trị mặc định chung.

2. **Nạp quy chuẩn nền tảng** - theo nền tảng đích, tham chiếu [platform-specs.md](references/platform-specs.md) để lấy giới hạn ký tự, kích thước ảnh, giờ đăng, quy định nền tảng.

3. **Viết hook** - tham chiếu nguồn dùng chung `skills/shared/references/hook-title-formulas.md`, chọn công thức hook hợp với từng nền tảng rồi viết dòng đầu. Hook quyết định 90% hiệu quả.

4. **Sắp định dạng nội dung** - tham chiếu [content-formats.md](references/content-formats.md), tổ chức thân bài theo loại nội dung:
   - Bài note ảnh-chữ kiểu Xiaohongshu -> hook ảnh bìa + dàn ý bộ card + thân bài
   - Kịch bản video ngắn (TikTok/YouTube Shorts/Reels) -> hook + thân bài + CTA
   - Bài dài trên Facebook, blog/website -> tiêu đề + mở bài + thân chia đoạn + kết
   - Status ngắn kiểu Weibo -> 140 chữ tinh gọn + hashtag chủ đề
   - Tái dùng nội dung -> tách một bản thảo thành tư liệu cho nhiều nền tảng
   - (dự phòng quốc tế) X thread / LinkedIn carousel

5. **Thêm hashtag** - tham chiếu [hashtag-strategy.md](references/hashtag-strategy.md), chọn tầng chủ đề và số lượng theo quy định từng nền tảng.

6. **Kiểm tra tuân thủ** - **đếm chữ bằng script, không đếm bằng mắt**: đưa thân bài của từng nền tảng vào
   `python3 skills/shared/scripts/wordcount.py count` (truyền qua stdin), đọc `social_count`
   (cách đếm cho mạng xã hội = ký tự CJK + từ tiếng Anh + chuỗi số + dấu câu), đối chiếu với [platform-specs.md](references/platform-specs.md)
   về giới hạn ký tự, vượt thì nén theo kết quả rồi đếm lại (có thể giao cho `text-condenser`). Sau đó né từ cấm/từ gây bóp tương tác
   (Facebook/TikTok đặc biệt quan trọng), xác nhận số hashtag đúng quy chuẩn nền tảng, vị trí đặt link ngoài hợp thói quen nền tảng.

7. **Khử mùi AI + cổng chất lượng (bắt buộc, không được bỏ)** - thân bài mỗi nền tảng phải qua hai cổng theo nguồn thẩm quyền text-polisher, chưa đạt thì sửa rồi mới giao:
   - **Khử mùi AI**: quét và viết lại theo `../text-polisher/references/zh-ai-markers.md` (tiếng Trung, có phần đặc thù Xiaohongshu) + `../text-polisher/references/phrases-to-remove.md` + `structures-to-avoid.md`; tự chấm mùi AI **>=45/50**.
   - **Chất lượng tổng thể**: tự chấm theo năm chiều chung của text-polisher (rõ ràng/nhịp/chân thực/mật độ giá trị/khớp giọng) **>=35/50**.
   - Qua cả hai cổng mới sang bước tiếp; đây là cổng chất lượng nội dung duy nhất của SKILL này, đừng bỏ.

8. **Sinh biến thể** - xuất 2-3 biến thể bài đăng cho mỗi nền tảng.

9. **Xuất kết quả** - giao toàn bộ nội dung theo định dạng ở mục "Đầu ra", ghi vào thư mục `outputs/`.

## Nhận biết Profile

### Khi có Profile

Trích từ ngữ cảnh `=== EASEL ACCOUNT PROFILE ===`:

- **platform** - khoá nền tảng đích, nạp quy chuẩn tương ứng
- **audience** - dùng để chỉnh cách dùng từ và độ sâu
- **tone / style** - khớp phong cách nhất quán của kênh
- **hashtag_sets** - ưu tiên dùng hashtag quen thuộc của kênh
- **posting_schedule** - dùng để gợi ý giờ đăng

### Khi không có Profile

- Lùi về chế độ chung: hỏi người dùng nền tảng đích, dùng best practice phổ quát
- Ghi chú ở cuối đầu ra: "Nếu cung cấp Profile kênh sẽ có mức thích ứng nền tảng và khớp phong cách chính xác hơn"
