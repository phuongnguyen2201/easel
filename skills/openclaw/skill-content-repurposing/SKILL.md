---
name: skill-content-repurposing
description: >-
  Tách một bài rồi viết lại cho Facebook/TikTok/YouTube/Zalo theo định dạng và giọng bản địa từng
  nơi. Dùng khi người dùng nói "một bài đăng nhiều nơi", "chuyển bài này sang TikTok", "tái sử
  dụng nội dung". skill-cross-platform-diff chỉ so khác biệt; skill này viết lại nội dung, không
  đăng.
layer: publish
---

# Chuyển nội dung sang nhiều nền tảng

> Bóc một bài dài thành tư liệu bản địa cho nhiều nền tảng, chỉnh định dạng, độ dài và giọng theo đặc tính từng nơi, để "viết một lần, đăng khắp nơi".

## Đầu vào

Người dùng đưa nội dung nguồn ngay trong prompt, hỗ trợ các dạng sau:

- **Văn bản**: dán thẳng bài mạng xã hội, bài dài trên Facebook hay blog/website, kịch bản video...
- **URL**: đưa link nội dung (dùng WebFetch để lấy về)
- **Bản bóc băng video/audio**: đưa lời video nói của video ngắn hoặc bản chữ của livestream
- **Kết hợp**: nội dung nguồn + chỉ định nền tảng đích

Prompt ví dụ:
```
Execute /skill-content-repurposing
Nội dung nguồn: <kịch bản video YouTube>
Nền tảng đích: Facebook, TikTok, YouTube
```

## Đầu ra

Đầu ra gồm hai phần:

### 1. Kế hoạch chuyển đổi

```json
{
  "source_type": "blog_post",
  "source_word_count": 2000,
  "core_elements": {
    "thesis": "luận điểm cốt lõi",
    "key_points": ["ý chính 1", "ý chính 2", "ý chính 3"],
    "quotable_lines": ["câu đắt 1", "câu đắt 2"],
    "data_points": ["số liệu 1"]
  },
  "target_platforms": ["facebook", "tiktok", "youtube"],
  "total_pieces": 8
}
```

### 2. Nội dung đã chuyển cho từng nền tảng

Mỗi nền tảng ra một bản riêng, đúng định dạng bản địa của nơi đó. Luật chuyển đổi cụ thể xem `references/conversion-recipes.md`.

## Kim tự tháp nội dung

SKILL này theo phương pháp kim tự tháp nội dung ba tầng:

| Tầng | Mô tả | Ví dụ |
|------|------|------|
| **Nội dung trụ cột (Pillar)** | Nội dung dài, chuyên sâu | Video dài trên YouTube, bài dài trên Facebook hay blog, podcast, bản ghi livestream |
| **Nội dung phái sinh (Derivative)** | Độ dài vừa, tách chủ đề con từ nội dung trụ cột | Bài ảnh trên Facebook, bài trả lời trên blog/diễn đàn, kịch bản video nói TikTok |
| **Nội dung vi mô (Micro)** | Ngắn gọn sắc bén, đánh một điểm | Bình luận nổi trên Facebook, TikTok 15 giây, thẻ câu đắt làm ảnh bìa |

Một bài trụ cột có thể đẻ ra 15-25 tư liệu cho các nền tảng. SKILL tự lên phương án bóc tách kim tự tháp theo loại nội dung nguồn.

## Các bước thực thi

1. **Nhận diện loại nội dung nguồn**
   - Xác định nội dung nguồn thuộc loại nào của tầng trụ cột (video YouTube / bài dài trên Facebook, blog / livestream / podcast)
   - Đếm số chữ, số đoạn, đánh giá mật độ nội dung

2. **Rút các yếu tố cốt lõi**
   - Chắt ra luận điểm cốt lõi (thesis)
   - Rút 3-5 ý chính (key points)
   - Đánh dấu các câu đắt trích được (quotable lines)
   - Nhặt số liệu và ví dụ thực tế (data points)

3. **Ánh xạ nền tảng đích**
   - Có Profile: đọc danh sách nền tảng đích từ trường `platforms` của Profile
   - Không có Profile: dùng nền tảng người dùng chỉ định, hoặc mặc định Facebook + TikTok + YouTube
   - Theo `references/platform-specs.md` để chốt yêu cầu định dạng của từng nền tảng

4. **Sinh nội dung chuyển đổi cho từng nền tảng**
   - Làm theo công thức chuyển đổi trong `references/conversion-recipes.md`
   - Mỗi bài phải là **nội dung bản địa** của nền tảng đó - không phải cắt ngắn hay copy-paste
   - Chỉnh theo giới hạn độ dài, giọng điệu, chiến lược hashtag, chuẩn định dạng

5. **Đưa ra gợi ý lịch đăng**
   - Gợi ý thứ tự đăng và khoảng cách thời gian giữa các nền tảng
   - Nguyên tắc: đăng nội dung trụ cột trước → nội dung phái sinh rải dần từ hôm sau → nội dung vi mô chèn vào các khoảng trống

## Nguyên tắc chuyển đổi

- **Bản địa với nền tảng**: mỗi bài đọc lên phải như được viết riêng cho nơi đó, không phải cắt gọt máy móc
- **Cốt lõi thống nhất**: mọi bản chuyển đổi truyền cùng một thông điệp cốt lõi, không lạc đề, không mâu thuẫn
- **Đứng một mình được**: đọc riêng từng bài vẫn trọn vẹn và có giá trị, không cần người đọc đã xem nội dung nguồn
- **Hợp định dạng**: tuân thủ chặt luật độ dài, định dạng và hashtag của từng nền tảng (xem `references/platform-specs.md`)

## Nhận biết Profile

- **Có Profile**:
  - Đọc danh sách nền tảng đích từ trường `platforms`, tự chốt hướng chuyển đổi
  - Đọc giọng điệu từ trường `tone` / `voice`, áp đồng nhất cho mọi bản chuyển đổi
  - Đọc khán giả mục tiêu từ trường `audience`, chỉnh độ sâu và cách diễn đạt
  - Đọc thói quen dùng hashtag từ trường `hashtag_strategy`
- **Không có Profile**:
  - Yêu cầu người dùng chỉ định nền tảng đích (không chỉ định thì mặc định Facebook + TikTok + YouTube)
  - Dùng giọng chuyên nghiệp phổ thông
  - Nhắc: "Nếu đưa Profile của kênh (có thông tin nền tảng và khán giả), bản chuyển đổi sẽ sát hơn nhiều"
