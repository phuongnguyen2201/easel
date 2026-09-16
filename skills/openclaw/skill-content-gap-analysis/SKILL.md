---
name: skill-content-gap-analysis
description: >-
  Tìm khoảng trống nội dung trong ngách: đề tài nhu cầu cao, ít cạnh tranh, kiểm chứng qua tìm
  kiếm, trend, bình luận; xuất danh sách đề tài ưu tiên. Dùng khi người dùng nói "đề tài chưa ai
  làm", "khoảng trống nội dung", "ngách còn gì để làm". skill-competitor-analysis mổ xẻ kênh đối
  thủ.
layer: discover
---

# Tìm đề tài đại dương xanh

> Quét nguồn cung nội dung và nhu cầu người dùng của ngách mục tiêu trên các nền tảng mạng xã hội, tìm ra đề tài đại dương xanh "nhu cầu cao mà ít nội dung tốt", xuất danh sách đề tài có ưu tiên.

## Đầu vào

Người dùng cung cấp các thông tin sau trong prompt (một số là tuỳ chọn):

- **Bắt buộc**: ngách/lĩnh vực (ví dụ "sắp xếp nhà cửa", "dạy Python", "ăn dặm cho bé")
- **Tuỳ chọn**: nền tảng mục tiêu (Facebook, TikTok, YouTube, Zalo..., mặc định quét toàn bộ nền tảng)
- **Tuỳ chọn**: danh sách kênh đối thủ (2-5 nhà sáng tạo cùng ngách)
- **Tuỳ chọn**: các hướng nội dung mình đã đăng (để đối chiếu khoảng trống)

## Đầu ra

```markdown
# Tìm đề tài đại dương xanh: {ngách}
Ngày: {date}
Nền tảng mục tiêu: {danh sách nền tảng}
Đối thủ đã quét: {danh sách kênh}
Số đề tài đại dương xanh tìm được: {count}

## Tóm tắt
{2-3 câu khái quát hướng cơ hội lớn nhất}

## Danh sách đề tài đại dương xanh

### 🔵 Ưu tiên cao (nhu cầu mạnh + cạnh tranh yếu)
| Hướng đề tài | Tín hiệu nhu cầu | Mức cạnh tranh | Nền tảng gợi ý | Dạng nội dung gợi ý | Tính thời sự |
|---------|---------|---------|---------|-------------|--------|

### 🟢 Ưu tiên vừa (nhu cầu rõ + cạnh tranh trung bình)
| Hướng đề tài | Tín hiệu nhu cầu | Mức cạnh tranh | Nền tảng gợi ý | Dạng nội dung gợi ý | Tính thời sự |

### ⚪ Hồ quan sát (trend tiềm năng + còn phải kiểm chứng)
| Hướng đề tài | Tín hiệu nhu cầu | Mức cạnh tranh | Nền tảng gợi ý | Dạng nội dung gợi ý | Tính thời sự |

## Nguồn tín hiệu nhu cầu
{Bằng chứng nhu cầu của từng đề tài: từ khoá trending, từ gợi ý tìm kiếm, câu hỏi lặp nhiều ở phần bình luận...}

## Điểm mù của đối thủ
{Những hướng kênh đối thủ chưa phủ nhưng người dùng có nhu cầu}

## Gợi ý dạng nội dung
{Dạng nội dung tốt nhất cho từng đề tài: bài viết kèm ảnh, video ngắn, video trung/dài, livestream, tuyển tập...}

## Danh sách thắng nhanh
{3-5 đề tài có thể bắt tay làm ngay trong tuần này + góc nội dung cụ thể}
```

## Các bước thực hiện

> Ba nguồn tín hiệu nhu cầu (từ gợi ý tìm kiếm trên nền tảng / bảng trending của nền tảng / nhu cầu chưa được đáp ứng ở phần bình luận) cùng cách thu thập và phương án dự phòng, xem [demand-signals.md](references/demand-signals.md). Ba loại tín hiệu phải đối chiếu chéo, thiếu một là không được.

### 1. Thu thập trend thời gian thực của nền tảng

Dùng web_fetch gọi API bảng trending (xem [hotlist-apis.md](../../shared/hotlist-apis.md)) để lấy chủ đề đang nóng trên từng nền tảng:

- Trending Douyin: `web_fetch https://60s.viki.moe/v2/douyin`
- Nội dung nóng Bilibili: `web_fetch https://60s.viki.moe/v2/bili` (⚠️ hay lỗi 500, không ổn định; khi hỏng thì đổi sang nguồn dự phòng `web_fetch https://v2.xxapi.cn/api/bilibilihot`)
- Trending Weibo: `web_fetch https://60s.viki.moe/v2/weibo`
- Bảng nóng Zhihu: `web_fetch https://60s.viki.moe/v2/zhihu`
- Bảng nóng Toutiao: `web_fetch https://60s.viki.moe/v2/toutiao`

Lọc từ danh sách trending ra các chủ đề liên quan tới ngách của người dùng, ghi lại chỉ số độ nóng, dùng làm hồ ứng viên cho đề tài mang tính thời sự.

### 2. Đào từ gợi ý tìm kiếm

Dùng web_search tìm từ khoá cốt lõi của ngách, thu thập từ gợi ý của công cụ tìm kiếm và của nền tảng (nhu cầu đuôi dài):

- Tìm `{ngách} site:xiaohongshu.com`, `{ngách} site:bilibili.com`..., quan sát các gợi ý tìm kiếm
- Tìm `{ngách} + cách/làm sao/gợi ý/tránh lỗi/so sánh/hướng dẫn` và các từ thể hiện nhu cầu khác, để lộ ra câu hỏi cụ thể của người dùng
- Thu thập các từ đuôi dài xuất hiện ở mục "tìm kiếm liên quan" - đây là nhu cầu thật của người dùng

Phân loại từ gợi ý tìm kiếm theo ý định: học hỏi, ra quyết định, giải quyết vấn đề, seeding mua sắm.

### 3. Quét nhu cầu chưa được đáp ứng ở phần bình luận

Dùng web_search tìm nội dung đang hot trong ngách, dùng web_fetch lấy trang về, tập trung phân tích phần bình luận:

- Câu hỏi lặp đi lặp lại trong các bình luận nhiều like ("xin một video hướng dẫn XX", "nói kỹ về XX được không")
- Điểm đau người dùng than phiền về nội dung hiện có ("nói như không nói", "chẳng vào trọng tâm gì cả")
- Số like của các bình luận dạng hỏi - càng nhiều like thì nhu cầu càng phổ biến
- Nội dung có lượt lưu/chia sẻ cao hơn hẳn lượt like - tức là hữu ích nhưng trình bày chưa tốt, mình làm tốt hơn được

### 4. Phân tích độ phủ của kênh đối thủ

Nếu người dùng đã cung cấp kênh đối thủ:

- Dùng web_search tìm `site:xiaohongshu.com {tên đối thủ}` hoặc `{tên đối thủ} {nền tảng}` để lấy danh sách nội dung của họ
- Phân loại nội dung đối thủ đã đăng theo chủ đề, vẽ ra bản đồ độ phủ
- Tìm điểm mù: hướng đối thủ chưa làm nhưng người dùng có nhu cầu
- Tìm vùng trũng chất lượng: hướng đối thủ đã làm nhưng chất lượng kém (bình luận phản hồi tiêu cực nhiều)

Nếu người dùng không cung cấp kênh đối thủ:

- Dùng web_search tìm `{ngách} nhà sáng tạo nên theo dõi` hoặc `{ngách} kênh` để ra các kênh top đầu
- Lấy mẫu phân tích độ phủ nội dung của 2-3 kênh top đầu

### 5. Đánh giá mức cạnh tranh

Với mỗi đề tài ứng viên, đánh giá tình hình nguồn cung nội dung:

- Dùng web_search tìm đề tài đó, xem số lượng và chất lượng kết quả
- **Tín hiệu đại dương xanh**: kết quả tìm kiếm có dưới 10 nội dung liên quan, chất lượng không đồng đều, chưa có nhà sáng tạo top đầu nào phủ, nội dung cũ kỹ (trên nửa năm chưa cập nhật)
- **Tín hiệu đại dương đỏ**: rất nhiều nội dung chất lượng cao, nhiều nhà sáng tạo top đầu đã phủ, nội dung cập nhật liên tục
- **Đại dương xanh giả**: kết quả tìm kiếm ít nhưng nhu cầu người dùng cũng yếu - cần đối chiếu chéo tín hiệu nhu cầu

### 6. Ghép dạng nội dung

Dựa vào đặc điểm đề tài và tính chất nền tảng để gợi ý dạng nội dung tốt nhất:

| Loại đề tài | Xiaohongshu | Douyin | Bilibili | Weibo |
|---------|--------|------|-----|------|
| Hướng dẫn/cẩm nang | Tuyển tập bài ảnh | Video ngắn | Video trung/dài | Bài dài kèm ảnh |
| Đánh giá/so sánh | Bài viết kèm ảnh | Video ngắn | Video trung/dài | Bình chọn + bài ảnh |
| Tránh lỗi/kinh nghiệm | Bài viết kèm ảnh | Video ngắn dạng nói | Video trung/dài | Bài theo chủ đề hashtag |
| Seeding/gợi ý mua | Bài viết kèm ảnh | Chia sẻ đồ hay | Video tuyển tập | Bài ảnh lưới 9 ô |
| Bình luận tin nóng | Bài viết kèm ảnh | Video ngắn | Video bình luận thời sự | Bình luận/chia sẻ lại |

### 7. Xếp thứ tự ưu tiên

Xếp hạng từng đề tài theo điểm có trọng số, xem [scoring-model.md](references/scoring-model.md):

| Yếu tố | Trọng số | Cách đánh giá |
|------|------|---------|
| Độ mạnh nhu cầu | 30% | Tần suất từ gợi ý tìm kiếm, số câu hỏi ở bình luận, độ liên quan với trend |
| Khoảng trống cạnh tranh | 25% | Nội dung hiện có ít, chất lượng kém, cập nhật chậm |
| Khớp với ngách | 20% | Mức khớp với định vị và khán giả của người dùng |
| Chi phí sản xuất | 15% | Có dùng tư liệu và năng lực sẵn có để làm nhanh được không |
| Giá trị thời sự | 10% | Có cửa sổ bắt trend hay cơ hội theo mùa không |

### 8. Sinh danh sách đề tài

Xuất danh sách đề tài đại dương xanh phân theo mức ưu tiên + 3-5 việc thắng nhanh. Mỗi việc thắng nhanh bắt buộc phải có: đề tài cụ thể, nền tảng mục tiêu, dạng nội dung, góc tiếp cận cốt lõi.

## Nguyên tắc quan trọng

- **Kiểm chứng nhu cầu trước** - đề tài đại dương xanh phải có tín hiệu nhu cầu thật chống lưng, "chưa ai làm" không đồng nghĩa với "đại dương xanh"
- **Cạnh tranh yếu ≠ chưa ai làm** - có người làm nhưng làm dở còn tốt hơn hoàn toàn chưa ai làm, vì nhu cầu đã được kiểm chứng
- **Khác biệt theo nền tảng** - cùng một đề tài, mức cạnh tranh ở các nền tảng có thể khác hẳn nhau, phải đánh giá từng nền tảng
- **Tránh đại dương xanh giả** - kết quả tìm kiếm ít + bình luận không ai bàn tới = có thể chẳng có nhu cầu nào cả
- **Thắng nhanh trước, cày sâu sau** - ưu tiên đề tài chi phí sản xuất thấp, thấy kết quả nhanh, để tạo phản hồi tích cực
- **Không đu mọi trend** - trend chỉ có giá trị khi khớp với ngách, bắt trend gượng ép thì không bền

## Nhận biết Profile

- **Khi có Profile**:
  - Đọc `platforms.md`, tập trung vào nền tảng người dùng thực sự đang làm, ưu tiên phân tích khoảng trống nội dung trên các nền tảng đó
  - Đọc `identity.md`, khớp với định vị nội dung và thế mạnh chuyên môn của người dùng, lọc bỏ đề tài vượt quá khả năng
  - Đọc `audience.md`, khoá vào bối cảnh nhu cầu của khán giả mục tiêu, khi phân tích bình luận thì chú ý các câu hỏi của nhóm này
  - Kết hợp thiên hướng phong cách nội dung trong Profile, khi gợi ý dạng nội dung thì ưu tiên dạng người dùng làm tốt
- **Khi không có Profile**:
  - Lùi về chế độ chung, yêu cầu người dùng cung cấp thông tin ngách
  - Quét toàn bộ nền tảng, không phân tích chuyên biệt theo nền tảng
  - Ghi chú thêm "nếu cung cấp Profile kênh thì sẽ nhận được hướng đề tài và gợi ý nền tảng chính xác hơn"
