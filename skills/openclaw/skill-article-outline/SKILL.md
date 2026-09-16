---
name: skill-article-outline
description: >-
  Lập dàn ý bài dài từ phân tích kết quả tìm kiếm: cấu trúc tiêu đề H2/H3, số chữ từng đoạn, vị
  trí biểu đồ và kế hoạch FAQ, cho bài blog/website hay bài dài trên Facebook. Dùng khi người dùng
  nói "dàn ý bài viết", "cấu trúc bài dài", "dàn ý blog", "khung bài viết", "cấu trúc H2/H3".
layer: plan
---

# Sinh dàn ý bài dài

> Dựa trên phân tích tìm kiếm, sinh dàn ý bài dài có cấu trúc (cấp tiêu đề, số chữ từng đoạn, vị trí biểu đồ, FAQ), dùng cho bài dài trên Facebook, blog/website và tương tự.

## Đầu vào

Người dùng cung cấp trong prompt:
- **Chủ đề hoặc từ khoá mục tiêu** (bắt buộc)
- **Từ khoá mục tiêu** - cụm chính xác cần tối ưu (nếu khác chủ đề)
- **Ý định tìm kiếm** - phổ biến kiến thức/thương mại/hướng dẫn (tuỳ chọn, không cho thì suy từ ngữ cảnh)
- **Nền tảng mục tiêu** - Facebook/blog/website (tuỳ chọn, có Profile thì tự nhận diện)

## Đầu ra

File dàn ý Markdown gồm: gợi ý tiêu đề, tham số mục tiêu, cấu trúc phân cấp H2/H3 (kèm số chữ mục tiêu từng đoạn), đánh dấu vị trí biểu đồ, kế hoạch FAQ, phân tích khác biệt nội dung.

Lưu vào `outputs/<chủ đề>/outline.md`.

## Các bước thực thi

### 1. Xác nhận chủ đề và ý định

Trích từ đầu vào của người dùng:
1. **Chủ đề hoặc từ khoá mục tiêu** (bắt buộc)
2. **Từ khoá mục tiêu** - cụm chính xác cần lên hạng/phủ sóng (nếu khác chủ đề)
3. **Ý định tìm kiếm** - phổ biến kiến thức, thương mại, hướng dẫn

Chỉ có chủ đề thì suy từ khoá và ý định theo ngữ cảnh.

### 2. Phân tích tìm kiếm

Dùng WebSearch phân tích 5 kết quả đầu của từ khoá mục tiêu:

1. Tìm từ khoá mục tiêu
2. Với mỗi kết quả, ghi lại:
   - **Cấu trúc tiêu đề** - đã phủ những chủ đề H2/H3 nào
   - **Độ dài nội dung** - khoảng bao nhiêu chữ
   - **Yếu tố hình ảnh** - biểu đồ, ảnh minh hoạ, infographic
   - **FAQ** - có mục câu hỏi thường gặp không
   - **Góc nhìn riêng** - điểm khác biệt của từng kết quả
   - **Thiếu sót** - mặt nào còn yếu hoặc bỏ sót
3. Với 2-3 kết quả xếp hạng đầu, dùng WebFetch trích cấu trúc tiêu đề chi tiết (khi tóm tắt tìm kiếm chưa đủ)
4. Tổng hợp mẫu hình chung và khoảng trống cơ hội

### 3. Sinh dàn ý

Sinh dàn ý có cấu trúc theo mẫu sau:

```
# Dàn ý: [chủ đề]

## Gợi ý tiêu đề
1. [tiêu đề chính - 15-25 chữ, đặt từ khoá lên trước, có lực]
2. [tiêu đề thay thế - góc tiếp cận khác]
3. [tiêu đề thay thế - dạng câu hỏi]

## Tham số mục tiêu
- **Từ khoá lõi**: [từ khoá]
- **Ý định tìm kiếm**: [phổ biến kiến thức/thương mại/hướng dẫn]
- **Số chữ mục tiêu**: [X.XXX] chữ
- **Số đoạn H2**: [6-8]
- **Nền tảng mục tiêu**: [Facebook/blog/website/chung]

---

## Dàn ý thân bài

### H2: [tiêu đề đoạn - nên dùng dạng câu hỏi] (~400-600 chữ)
- **Ý mở đầu**: [dùng sự thật hay số liệu nào để dẫn vào đoạn này?]
- **Ý cần phủ**:
  - [ý 1]
  - [ý 2]
  - [ý 3]
- **H3: [đoạn con]** (nếu cần)
  - [hướng nội dung của đoạn con]
- **Số liệu then chốt**: [cần tìm số liệu gì để tăng sức thuyết phục?]
- **Gợi ý biểu đồ**: [cột/đường/tròn/không] - [trực quan hoá dữ liệu gì]
- **Vị trí ảnh minh hoạ**: [có/không] - [mô tả ảnh gợi ý]

### H2: [tiêu đề đoạn] (~400-600 chữ)
[... lặp lại 6-8 đoạn ...]

### Mục FAQ (3-5 câu)
1. [câu hỏi từ gợi ý tìm kiếm] - [hướng trả lời]
2. [câu hỏi từ gợi ý tìm kiếm] - [hướng trả lời]
3. [câu hỏi từ gợi ý tìm kiếm] - [hướng trả lời]
4. [câu hỏi từ phân tích tìm kiếm] - [hướng trả lời]

### Kết (~100-200 chữ)
- Tóm tắt các ý cốt lõi
- Hướng kêu gọi hành động

---

## Kế hoạch link nội bộ
- **Bài này nên dẫn tới**: [bài liên quan đã có, có thể link tới]
- **Nên link về bài này**: [bài đã có nên thêm link trỏ về bài này]

## Khác biệt nội dung
1. [nội dung đối thủ hay bỏ sót mà bài này nên phủ]
2. [góc nhìn riêng hoặc quan điểm gốc có thể đưa vào]
3. [lợi thế định dạng - trực quan tốt hơn, phủ sâu hơn, cấu trúc rõ hơn]
```

Nguyên tắc sinh tiêu đề:
- 60-70% tiêu đề H2 dùng dạng câu hỏi
- Mỗi đoạn H2 đều có gợi ý "ý mở đầu" rõ ràng
- Chỉ dùng đoạn con H3 khi chủ đề thực sự cần chia nhỏ
- Tổng số chữ mục tiêu các đoạn phải xấp xỉ tổng số chữ mục tiêu chung
- Gợi ý loại biểu đồ nên đa dạng (tránh lặp một loại)
- Vị trí ảnh minh hoạ nên rải đều

### 4. Phân tích khác biệt nội dung

Sinh xong dàn ý thì bổ sung phân tích khác biệt:
1. Liệt kê 3-5 chủ đề hoặc góc nhìn mà toàn bộ đối thủ top đầu đều bỏ sót
2. Chỉ ra chỗ có thể thêm số liệu, case hoặc quan điểm gốc
3. Nêu lợi thế định dạng bài này khai thác được (nhiều biểu đồ hơn, cấu trúc tốt hơn, phủ sâu hơn)

### 5. Lưu

Lưu dàn ý vào `outputs/<chủ đề>/outline.md`.
Thư mục `outputs/` hoặc thư mục con chưa có thì tự tạo.

## Nhận biết Profile

- Phát hiện dấu `=== EASEL ACCOUNT PROFILE ===`
- **Khi có Profile**:
  - Theo trường `platform` mà thích ứng đặc điểm nền tảng (thói quen trình bày bài dài trên Facebook, thiên hướng chiều sâu của blog chuyên đề, trọng tâm SEO của website)
  - Theo trường `tone` / `style` mà chỉnh phong cách tiêu đề và cách dùng từ
  - Theo trường `audience` mà khớp mức hiểu biết của khán giả, chỉnh độ sâu và mật độ thuật ngữ
- **Khi không có Profile**:
  - Sinh dàn ý chung, `Nền tảng mục tiêu` đặt là `chung`
  - Ghi chú "cung cấp Profile của kênh sẽ có dàn ý tuỳ biến theo nền tảng"
