---
name: skill-competitor-analysis
description: >-
  Mổ xẻ chiến lược nội dung kênh đối thủ: đề tài, định dạng, nhịp đăng, quy luật viral, cách tương
  tác; chỉ ra cơ hội khác biệt, việc cần làm. Dùng khi người dùng nói "phân tích đối thủ", "đối
  thủ đang làm gì", "mổ xẻ bài viral". skill-content-gap-analysis tìm khoảng trống đề tài cả
  ngách.
layer: discover
---

# Phân tích nội dung đối thủ

> Mổ xẻ nội dung kênh đối thủ cùng ngách trên mọi khía cạnh: phân bố đề tài, nhịp đăng, quy luật viral, định dạng ưa dùng, cách tương tác; tìm cơ hội khác biệt và đưa ra việc làm được ngay.

## Đầu vào

Người dùng cung cấp các thông tin sau trong prompt (một phần là tuỳ chọn):

- **Bắt buộc**: tên hoặc link kênh đối thủ (1-5 kênh), ngách/lĩnh vực của người dùng
- **Tuỳ chọn**: nền tảng mục tiêu (Facebook/TikTok/YouTube/Zalo...), trọng tâm phân tích (đề tài/định dạng/tăng người theo dõi/kiếm tiền...), tên kênh của chính mình (để đối chiếu)

## Đầu ra

```markdown
# Báo cáo phân tích nội dung đối thủ
Ngày: {date}
Ngách: {niche}
Nền tảng phân tích: {platforms}
Số đối thủ: {N}

## Thẻ hồ sơ kênh đối thủ
(mỗi đối thủ một thẻ)
- Tên kênh / nền tảng / quy mô người theo dõi / định vị trong phần giới thiệu
- Từ khoá hướng nội dung / tần suất đăng / định dạng chủ lực
- Top 3 bài tiêu biểu (tiêu đề + số liệu + mổ xẻ)

## Phân bố đề tài
Phân loại chủ đề nội dung và tỉ trọng của từng đối thủ

## Định dạng và nhịp đăng
Tỉ trọng hình thức nội dung (bài ảnh/video ngắn/livestream/carousel/tuyển tập) + tần suất và quy luật giờ đăng

## Mổ xẻ bài viral
Phân tích điểm chung của nội dung tương tác cao gần đây: mẫu tiêu đề, đặc điểm ảnh bìa, cấu trúc nội dung, hook cảm xúc

## Cách tương tác
Đặc điểm tỉ lệ bình luận/thích/lưu/chia sẻ + chiến lược vận hành phần bình luận

## Phân tích bắt trend
Đối thủ bắt trend thế nào, tần suất bắt trend, đánh giá hiệu quả

## Phân tích SWOT
SWOT ở tầng nội dung cho từng đối thủ chính

## Cơ hội khác biệt
Đề tài, định dạng, persona, khoảng trống khán giả mà đối thủ chưa phủ hoặc làm còn yếu

## Việc cần làm
Các việc cụ thể xếp theo độ ưu tiên, mỗi việc dẫn số liệu làm căn cứ
```

## Các bước thực hiện

### 1. Thu thập bối cảnh

Xác nhận các thông tin sau, thiếu gì thì chủ động hỏi:
- Danh sách kênh đối thủ (tên hoặc link)
- Ngách / lĩnh vực nhỏ của người dùng
- Nền tảng mục tiêu (mặc định phủ mọi nền tảng đối thủ đang có mặt)
- Trọng tâm phân tích (mặc định đủ mọi khía cạnh)

### 2. Hồ sơ kênh đối thủ

Lập hồ sơ cơ bản cho từng kênh đối thủ. Cách thu thập dữ liệu và phương án dự phòng khi bị chặn crawl ở từng nền tảng xem [data-collection.md](references/data-collection.md):
- Dùng `web_fetch` lấy thông tin trang kênh (giới thiệu, quy mô người theo dõi, số bài đăng); bị chặn crawl thì lùi về `web_search` để lấy thông tin công khai
- Trích từ khoá định vị, hướng nội dung, đặc điểm persona
- Ghi khoảng quy mô người theo dõi, mức độ hoạt động của kênh
- Dữ liệu không lấy được (lượt xem/tỉ lệ xem hết/mức tăng người theo dõi và các số liệu trong trang quản trị nhà sáng tạo) thì ghi thẳng "không có dữ liệu công khai", không bịa con số chính xác

### 3. Phân tích đề tài và chủ đề

Rà nội dung gần đây của đối thủ (cố gắng phủ 30-90 ngày gần nhất):
- Gom theo chủ đề, tính tỉ trọng từng chủ đề
- Nhận diện hướng đề tài cốt lõi (đề tài thường xanh vs đề tài bắt trend vs trải nghiệm cá nhân)
- Đánh dấu từ khoá và hashtag xuất hiện nhiều

### 4. Định dạng nội dung và nhịp đăng

Phân tích định dạng ưa dùng và quy luật đăng của đối thủ (chỉ số tần suất đăng và cách suy ra nhịp tăng người theo dõi xem [viral-patterns.md](references/viral-patterns.md)):
- Phân bố định dạng: bài ảnh / video ngắn / video dài vừa / livestream / carousel ảnh / tuyển tập
- Tần suất đăng: hằng ngày / vài lần mỗi tuần / không đều
- Khung giờ đăng: dồn vào những khung nào
- Thích ứng nền tảng: cùng một nội dung được xử lý khác nhau ra sao trên từng nền tảng

### 5. Mổ xẻ nội dung viral

Cách xác định bài viral, các chiều mổ xẻ và cách truy ngược "công thức viral" xem [viral-patterns.md](references/viral-patterns.md). Lọc nội dung có tương tác vượt hẳn mức trung bình (>= 3-5 lần trung vị của kênh), mổ xẻ từng bài:
- **Tiêu đề/ảnh bìa**: dùng hook gì? (con số, gợi tò mò, điểm đau, phản trực giác, từ ngữ cảm xúc)
- **Cấu trúc nội dung**: cách giữ chân ở đoạn mở, nhịp ở giữa, cách dẫn dắt tương tác ở đoạn kết
- **Thời điểm chọn đề tài**: có trúng trend, dịp lễ, chiến dịch của nền tảng không
- **Đặc điểm định dạng**: thời lượng, số ảnh, cách trình bày, font chữ, BGM...

### 6. Phân tích cách tương tác

Phân tích đặc điểm tương tác của nội dung đối thủ:
- Cấu trúc tương tác: phân bố tỉ lệ thích/bình luận/lưu/chia sẻ
- Đặc điểm phần bình luận: khán giả bàn chuyện gì là chính, xu hướng cảm xúc ra sao
- Chủ kênh tương tác: có trả lời bình luận không, phong cách trả lời, chiến lược ghim bình luận
- Kiểu được lưu vs kiểu được lan truyền: nội dung nào được lưu nhiều (thiên công cụ), nội dung nào được chia sẻ nhiều (thiên cảm xúc)

### 7. Phân tích bắt trend

Dùng `web_fetch` gọi API bảng tìm kiếm nóng (xem [hotlist-apis.md](../../shared/hotlist-apis.md)) để lấy trend hiện tại của từng nền tảng, rồi:
- So mức trùng khớp giữa nội dung gần đây của đối thủ và các chủ đề đang nóng
- Phân tích tần suất, tốc độ và góc tiếp cận khi đối thủ bắt trend
- Đánh giá chênh lệch tương tác giữa nội dung bắt trend và nội dung thường
- Nhận diện loại trend mà đối thủ bắt tốt (sự kiện xã hội/tin ngành/meme của nền tảng/dịp lễ)

### 8. Phân tích SWOT

Làm SWOT ở tầng nội dung cho từng đối thủ chính:
- **S (điểm mạnh)**: chất lượng nội dung, tần suất đăng, độ nhận diện persona, độ gắn bó của người theo dõi
- **W (điểm yếu)**: định dạng đơn điệu, đề tài hẹp, ít tương tác, đăng không đều
- **O (cơ hội)**: nhu cầu khán giả chưa ai đáp ứng, nền tảng/định dạng mới nổi, khoảng trống trong ngách
- **T (thách thức)**: những điểm đối thủ này gây sức ép cạnh tranh trực tiếp lên người dùng

### 9. Đào cơ hội khác biệt

Dựa trên phân tích trên, tìm hướng khác biệt có thể chen vào:
- Khoảng trống đề tài: chủ đề đối thủ chưa làm nhưng khán giả có nhu cầu
- Khác biệt định dạng: đối thủ dồn vào bài ảnh thì mình dùng video ngắn để phá vây (và ngược lại)
- Khác biệt persona: đối thủ thiên chuyên môn nghiêm túc thì mình đi hướng gần gũi chân thật (và ngược lại)
- Chia nhỏ khán giả: đối thủ phủ đại chúng thì mình đào sâu nhóm hẹp hơn
- Khác biệt nền tảng: đối thủ dồn sức vào một nền tảng thì mình dựng lợi thế ở nền tảng khác

### 10. Xuất việc cần làm

Gom thành danh sách việc làm được ngay:
- Mỗi việc ghi độ ưu tiên (cao/trung bình/thấp) và hiệu quả kỳ vọng
- Dẫn số liệu cụ thể của đối thủ làm căn cứ ("đối thủ A dùng định dạng XX đạt XX tương tác")
- Tách việc thắng nhanh (tuần này làm được) và việc dài hạn (cần tích luỹ liên tục)
- Đề xuất phải khớp với định vị và phong cách của chính người dùng

Xem [analysis-templates.md](references/analysis-templates.md) để xuất ma trận cạnh tranh.

## Nhận biết Profile

- **Khi có Profile**:
  - Đọc `identity.md`: lấy định vị và điểm khác biệt của người dùng, ghép đúng tầm đối thủ
  - Đọc `platforms.md`: tập trung vào nền tảng người dùng đang vận hành thật, phân tích màn thể hiện của đối thủ trên nền tảng đó
  - Đọc `style.md`: khớp việc cần làm với phong cách nội dung và tone người dùng thích
  - Đọc `audience.md` (nếu có): dùng hồ sơ khán giả để tinh chỉnh phần phân tích cơ hội khác biệt
  - Trong kết luận, đối chiếu thẳng với kênh của người dùng, đưa ra bảng so "bạn vs đối thủ"
- **Khi không có Profile**:
  - Lùi về chế độ tổng quát, yêu cầu người dùng tự cung cấp thông tin ngách và đối thủ
  - Phân tích phủ mọi nền tảng, không chuyên biệt hoá theo nền tảng
  - Ghi chú "cung cấp Profile của kênh sẽ có đối chiếu đối thủ và đề xuất khác biệt chính xác hơn"
