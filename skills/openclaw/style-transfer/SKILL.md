---
name: style-transfer
description: >-
  Đổi phong cách đoạn văn, giữ ý: nghiêm túc → hài, văn viết → văn nói, văn hoa → thẳng, trang
  trọng → giọng mạng xã hội; nhận mẫu phong cách đích. Dùng khi người dùng nói "đổi giọng hài",
  "viết dân dã hơn", "viết giống XX", "đổi phong cách". text-polisher nâng chất lượng, giữ phong
  cách.
layer: produce
---

# Chuyển phong cách bài viết

> Viết lại bài từ phong cách này sang phong cách khác, giữ nguyên ý cốt lõi, chỉ đổi cách diễn đạt.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| `text` | Có | Bài gốc cần viết lại |
| `target_style` | Có | Phong cách đích (xem danh sách phong cách dựng sẵn, hoặc mô tả tự do) |
| `style_reference` | Không | Một đoạn mẫu của phong cách đích, dùng để học đặc trưng phong cách |
| `preserve_keywords` | Không | Danh sách từ khoá/thuật ngữ bắt buộc giữ nguyên |
| `intensity` | Không | Mức chuyển: `light` (chỉnh nhẹ giọng) / `medium` (mặc định) / `full` (viết lại hẳn) |

### Phong cách dựng sẵn

> Chi tiết ở `references/style-rules.md`, có checklist thực thi đầy đủ.

| key phong cách | Tên | Quy tắc cốt lõi | Đặc trưng câu | Điều cấm |
|----------|------|---------|---------|---------|
| `humorous` | Hài hước | Cứ 3-4 câu ít nhất một cú meme/phóng đại/tự trào | Chủ yếu câu ngắn, nhịp bẻ lái | Không viết "haha", không giải thích meme |
| `colloquial` | Văn nói | Bỏ hết liên từ văn viết, dùng "ừ thì", "kiểu", "nói chung" | <=15 chữ/câu, nhiều câu hỏi và cảm thán | Không dùng "tóm lại", "ngoài ra", "do đó" |
| `literary` | Văn hoa | Diễn đạt bằng hình ảnh, dùng ví von thay cho nói thẳng | Câu dài ngắn xen kẽ, có khoảng lặng | Không chất đống tính từ |
| `sharp` | Sắc bén | Kết luận thẳng, không chừa đường lùi | Ngắn gọn dứt khoát, nhiều dấu chấm | Không dùng "có thể", "chắc là", "mình nghĩ" |
| `professional` | Chuyên môn | Thuật ngữ chính xác, chuỗi logic đầy đủ | Cấu trúc song song/tăng tiến rõ ràng | Không dùng lối nói văn nói |
| `healing` | Chữa lành | Ấm áp đồng cảm, nhiều câu mở đầu bằng "bạn" | Câu dài vừa, nhịp chậm rãi | Không mỉa mai/phê phán |
| `sarcastic` | Đanh đá | Chỉ trúng vấn đề, không giữ thể diện | Câu cực ngắn + câu hỏi tu từ | Không công kích cá nhân |
| `social_media` | Chất mạng xã hội | emoji + văn nói + câu kéo tương tác | Xuống dòng nhiều, mỗi dòng <=20 chữ | Không viết đoạn dài |
| `custom` | Tự định nghĩa | Cần cung cấp `style_reference` | - | - |

## Đầu ra

- Bài đã viết lại (văn bản thuần)
- Tóm tắt thay đổi phong cách (đã đổi những chiều nào: từ ngữ, kiểu câu, giọng điệu, tu từ, nhịp)
- Ghi vào `outputs/<chủ đề>/`, tên file có ký hiệu phong cách gốc và phong cách đích

## Các bước thực hiện

### Step 1 - Phân tích phong cách

Phân tích đặc trưng phong cách của bài gốc, nhận diện các chiều sau:
- **Tầng từ ngữ**: trang trọng/văn nói, trừu tượng/cụ thể, mật độ thuật ngữ
- **Tầng kiểu câu**: tỉ lệ câu dài/câu ngắn, chủ động/bị động, câu phức/câu đơn
- **Tầng giọng điệu**: khách quan/chủ quan, lạnh lùng/nhiệt tình, khoảng cách với người đọc
- **Tầng tu từ**: tần suất dùng ví von, điệp cấu trúc, câu hỏi tu từ, phóng đại
- **Tầng nhịp**: độ dài đoạn, cảm giác ngắt nghỉ, mật độ thông tin

### Step 2 - Dựng mô hình phong cách đích

Nếu có `style_reference`:
- Phân tích văn bản mẫu theo cùng các chiều đó, rút ra vector đặc trưng phong cách
- Nhận diện thủ pháp đặc trưng của văn bản mẫu (kiểu câu riêng, câu cửa miệng, mẫu nhịp)

Nếu dùng phong cách dựng sẵn:
- Nạp định nghĩa đặc trưng của phong cách đó

### Step 3 - Viết lại theo phong cách mới

Viết lại theo mức chuyển đã chọn:
1. Xử lý từng đoạn, bảo đảm trọn ý
2. Chỉnh theo thứ tự ưu tiên: giọng điệu -> từ ngữ -> kiểu câu -> tu từ -> nhịp
3. Giữ nguyên các từ khoá liệt kê trong `preserve_keywords`
4. Giữ đủ lượng thông tin của bài gốc (không thêm không bớt ý cốt lõi)

### Step 4 - Kiểm tra nhất quán

- Kiểm tra phong cách toàn bài có đồng nhất không (tránh đầu một kiểu cuối một kiểu)
- Kiểm tra thông tin cốt lõi có còn đủ không
- Kiểm tra `preserve_keywords` đã giữ đủ chưa
- Nếu ý bị lệch quá ngưỡng sau khi chuyển, quay lại viết lại đoạn đó

### Step 5 - Xuất tóm tắt thay đổi

Liệt kê các chiều phong cách đã thay đổi để người dùng biết đã sửa những gì:
```
Chuyển phong cách: trang trọng -> văn nói
- Từ ngữ: thay từ văn viết bằng từ đời thường (12 chỗ)
- Kiểu câu: tách câu phức dài thành câu ngắn (8 chỗ)
- Giọng điệu: thêm từ đệm và cảm giác tương tác (6 chỗ)
- Tu từ: bỏ điệp cấu trúc, thêm ví von kiểu nói chuyện (3 chỗ)
```

## Nhận biết Profile

- **Có Profile**: đọc `style.md` để lấy phong cách quen dùng của kênh, làm mốc tinh chỉnh phong cách đích; đọc `identity.md` để lấy tông thương hiệu, bảo đảm bài viết lại vẫn nằm trong ranh giới thương hiệu
- **Không có Profile**: viết lại thẳng theo phong cách đích người dùng chỉ định, không ràng buộc thương hiệu

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
