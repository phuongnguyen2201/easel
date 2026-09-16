---
name: skill-voice-builder
description: >-
  Dựng hồ sơ giọng văn (voice/tone: giọng điệu, từ ngữ, nhịp, phong cách) của nhà sáng tạo qua
  phỏng vấn và phân tích bài mẫu để nội dung sau nhất quán. Dùng khi người dùng nói "phong cách
  viết của tôi", "thống nhất văn phong", "voice/tone". skill-audience-profiler dựng chân dung khán
  giả.
layer: plan
---

# Dựng hồ sơ giọng văn

> Qua phỏng vấn có cấu trúc + phân tích bài mẫu, dựng hồ sơ giọng văn cá nhân (about-me.md + voice.md), giữ thương hiệu nhất quán cho nội dung về sau.

## Đầu vào

Người dùng trả lời phỏng vấn và đưa 3-5 bài mẫu (bài trên Facebook, kịch bản TikTok, kịch bản YouTube, post Zalo, bài blog/website...).

Nếu người dùng chưa có bài mẫu, gõ `use samples` để nạp bộ mẫu mặc định `references/sample-content.md`.

## Đầu ra

Hai file, ghi ra thư mục gốc dự án (**sản phẩm giọng văn nhẹ và độc lập, không thuộc schema sáu chiều của Profile**; muốn gộp vào Profile thì chép các ý chính ngược lại vào `profiles/<Profile>/style.md`):

1. **about-me.md** (≤300 từ) - định vị cá nhân: danh tính và định vị, khán giả mục tiêu, trụ cột chủ đề, quan điểm ngành, cam kết persona, vùng cấm nội dung
2. **voice.md** (≤500 từ) - hồ sơ giọng văn: tín hiệu dương (viết thế nào) + tín hiệu thiếu vắng (không bao giờ viết kiểu gì), gộp chung một file

## Các bước thực thi

### 1. Tự động mở phỏng vấn

Nạp là chạy, không mở bài, không tóm tắt, không hỏi xác nhận. Tin nhắn đầu tiên bắt buộc là câu hỏi phỏng vấn.

Cấm:
- Tóm tắt chức năng của SKILL này
- Hỏi người dùng đã sẵn sàng chưa
- Giải thích sẽ sinh ra những file nào

### 2. Hỏi thành hai đợt (tổng 6 câu)

Dùng công cụ AskUserQuestion, mỗi đợt tối đa 4 câu.

- **Batch 1** (4 câu): danh tính và định vị, khán giả mục tiêu, trụ cột chủ đề, quan điểm ngành
- **Batch 2** (2 câu): cam kết persona, vùng cấm nội dung

Chi tiết câu hỏi và phương án → [interview-questions.md](references/interview-questions.md)

Trả lời xong Batch 1 thì gửi ngay Batch 2, ở giữa không bình luận. Câu nào bỏ trống thì hỏi lại riêng một lần rồi đi tiếp.

### 3. Sinh about-me.md

Viết dựa trên đáp án của 6 câu, cấu trúc:

```
# Định vị của tôi
## Danh tính và định vị
## Khán giả mục tiêu
## Trụ cột chủ đề nội dung
## Quan điểm ngành
## Cam kết persona
## Vùng cấm nội dung
```

≤300 từ. Mỗi dòng phải là thông tin trích dùng được ngay khi sáng tạo về sau.

### 4. Thu bài mẫu

Nhắc người dùng dán 3-5 bài mẫu. Cho phép dán một lần hoặc gửi từng bài.

- Tối thiểu 3 bài mới được vào bước phân tích, thiếu thì hỏi thêm
- Người dùng gõ `use samples` → nạp `references/sample-content.md`, báo tác giả bài mẫu và nhắc có thể thay bất cứ lúc nào

### 5. Phân tích bài mẫu

Tìm quy luật xuyên suốt mọi bài mẫu, không dựa vào đặc điểm của một bài.

Chi tiết các chiều phân tích → [voice-analysis-dimensions.md](references/voice-analysis-dimensions.md)

Bốn chiều phân tích:
- **Tín hiệu giọng** - độ dài câu, nhịp đoạn, kiểu mở đầu, ngôi xưng, ngữ điệu, cụm từ đặc trưng, phong cách CTA
- **Tín hiệu cấu trúc** - khoảng độ dài, liệt kê vs văn xuôi, mẫu mở/kết, cách chuyển ý
- **Tín hiệu chủ đề** - chủ đề lặp nhiều qua các bài, khán giả ngầm định, lập trường tác giả
- **Tín hiệu thiếu vắng** - từ ngữ/dấu câu chưa từng xuất hiện, kiểu mở đầu chưa từng dùng, ngữ điệu chưa từng chạm tới

### 6. Sinh voice.md

Tổng hợp hồ sơ giọng văn, tín hiệu dương và tín hiệu thiếu vắng gộp chung một file:

```
# Hồ sơ giọng văn của tôi
## Tôi nghe giống ai
## Tông giọng nền
## Nhịp câu
## Hook mở đầu
## Tôi mở đầu thế nào
## Tôi kết bài thế nào
## Cách diễn đạt đặc trưng
## Vùng cấm nội dung
## Những điều giọng này không bao giờ làm
```

≤500 từ. Mỗi mục phải dựa trên bằng chứng từ bài mẫu, không được bịa. `Vùng cấm nội dung` và `Những điều giọng này không bao giờ làm` phải có bằng chứng thiếu vắng trong bài mẫu.

### 7. Xác nhận hoàn tất và gợi bước tiếp theo

Báo người dùng hai file đã sẵn sàng, các bước sáng tạo sau sẽ tự trích dùng. Gợi ý những thao tác tiếp theo.

## Nhận biết Profile

- **Có Profile** - điền sẵn khán giả, nền tảng, tông giọng ưa dùng và các thông tin đã biết từ Profile, khi phỏng vấn thì bỏ qua câu đã có đáp án hoặc dùng để đối chiếu; ghi chú mức khớp với Profile ngay trong voice.md.
- **Không có Profile** - chạy đủ cả 6 câu phỏng vấn, sinh hồ sơ giọng văn dùng chung.

## Quy tắc

1. **Nạp là chạy** - không tóm tắt, không giải thích, vào phỏng vấn luôn
2. **Tối thiểu 3 bài mẫu** - dưới 3 bài thì không khởi động phân tích
3. **Dựa trên bằng chứng** - rút quy luật từ bài mẫu, không bịa đặc điểm không có thật
4. **Giữ mâu thuẫn** - phong cách giữa các bài chỏi nhau thì ghi đúng như vậy, không làm mượt
5. **Giới hạn độ dài** - about-me.md ≤300 từ, voice.md ≤500 từ
6. **Định dạng sản phẩm** - mọi nội dung bài mẫu xuất trong khối mã, giữ nguyên xuống dòng và khoảng trắng
7. **Không lặp** - voice.md không nhắc lại thông tin khán giả và chủ đề đã có trong about-me.md
8. **Ngôn ngữ** - file sản phẩm mặc định viết tiếng Việt (trừ khi bài mẫu rõ ràng là tiếng Anh)
9. **Cấm gạch ngang dài** - file sản phẩm và bản nháp không dùng em dash
