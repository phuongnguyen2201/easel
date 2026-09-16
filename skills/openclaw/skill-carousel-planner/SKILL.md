---
name: skill-carousel-planner
description: >-
  Lên cấu trúc từng trang cho bài nhiều ảnh (carousel): Hook trang bìa, nhịp nội dung, chữ và hình
  mỗi trang, CTA, caption, chấm điểm tương tác. Dùng khi người dùng nói "lên carousel", "bài nhiều
  ảnh", "mỗi trang viết gì". Render thẻ ảnh thật dùng card-xiaohongshu / xhs-note-creator.
layer: plan
---

# Lên kế hoạch carousel

> Lên cấu trúc từng trang cho bài nhiều ảnh/carousel: Hook trang bìa, nhịp nội dung, chữ và hướng hình mỗi trang, thiết kế CTA, kèm điểm tiềm năng tương tác.

**Nạp xong là bắt đầu quy trình lên kế hoạch ngay, không tóm tắt, không chờ xác nhận.**

**File tham khảo chính:**
- `references/format-specs.md` -- chuẩn kích thước, giới hạn số trang, cỡ chữ
- `references/hook-library.md` -- công thức Hook trang bìa đã kiểm chứng kèm dữ liệu tương tác
- `references/scoring-system.md` -- các tiêu chí chấm điểm tương tác và ngưỡng đạt

## Đầu vào

Chủ đề và mục tiêu người dùng đưa trong prompt. Có thể là từ khoá, một câu mô tả, hoặc brief chi tiết.

## Đầu ra

Tài liệu kế hoạch carousel có cấu trúc, gồm: chữ trang bìa, bóc tách từng trang, caption, bảng điểm, ghi chú sản xuất.

Lưu vào `outputs/<chủ đề>/carousel-brief.md`.

## Các bước thực hiện

### Bước 1: Xác nhận bối cảnh

1. Trích chủ đề và mục tiêu từ prompt của người dùng (giáo dục, chuyển đổi, xây uy tín, giải trí).
2. Xác định khán giả mục tiêu.
3. Nạp toàn bộ file tham khảo chính.
4. Tra `references/hook-library.md`, tìm kiểu Hook tương tác cao khớp chủ đề nhất.

### Bước 2: Hook trang bìa

Trang bìa theo đúng luật mở đầu của video ngắn: phải chặn được ngón tay lướt trong 1 giây.

#### Quy tắc Hook trang bìa

- Chữ trang bìa không quá 12 chữ
- Phải tạo được khoảng trống tò mò hoặc cú chạm cảm xúc
- Dùng 6 công thức đã kiểm chứng trong `references/hook-library.md`:
  - **Ngược lẽ thường:** "Đừng XX nữa"
  - **Danh sách số:** "5 sai lầm phá hỏng XX"
  - **Đối lập gây sốc:** kịch tính thị giác trước - sau
  - **Đánh thẳng nỗi đau:** "Vì sao bạn XX mãi vẫn thất bại" (dạng khẳng định, không thêm dấu hỏi)
  - **Tuyên bố lật ngược:** "Điều này sẽ thay đổi tất cả"
  - **Gắn danh tính:** "Dân XX nhất định phải xem" (tỉ lệ lưu + chia sẻ cao)
- Font phải to, in đậm, ở cỡ thumbnail vẫn đọc rõ
- Trang bìa không đặt logo hay nhận diện thương hiệu (làm giảm tò mò)

Ghi lại công thức Hook đã chọn và chữ trang bìa.

### Bước 3: Cấu trúc từng trang

Sắp theo cung **Hook > dẫn dắt nội dung > hé lộ > kêu gọi hành động**:

| Trang | Vai trò | Quy tắc |
|------|------|------|
| 1 | Hook / trang bìa | Không quá 12 chữ, tạo khoảng trống tò mò, xem Bước 2 |
| 2-3 | Vấn đề / dẫn dắt | Dựng nỗi đau hoặc đặt câu hỏi |
| 4-7 | Nội dung / giá trị | Mỗi trang một ý, chữ trên trang không quá 20 chữ |
| 8-9 | Hé lộ / thu hoạch | Trao insight cốt lõi hoặc sự thay đổi |
| Trang cuối | Kêu gọi hành động | Dẫn lưu bài/chia sẻ/theo dõi |

#### Quy tắc nội dung mỗi trang

- **Mỗi trang chỉ nói một ý.** Cần tới dấu phẩy là tách trang.
- **Chữ mỗi trang không quá 20 chữ** (lớp chữ đè lên hình). Càng ít càng tốt.
- **Đồng nhất thị giác:** cả bài dùng chung một kiểu nền, một font và một bảng màu.
- **Đường đọc:** từ trên xuống, từ trái sang phải. Không bày lộn xộn.
- **Lực kéo lật trang:** mỗi trang phải tạo lý do để người đọc lật sang trang sau.

Xuất theo từng trang:
1. Số trang
2. Chữ trên trang (lớp chữ đè, không quá 20 chữ)
3. Mô tả hình ảnh
4. Giải thích lực kéo lật trang (vì sao người đọc lật sang trang sau)

### Bước 4: Kêu gọi hành động ở trang cuối

Trang cuối quyết định bài có được lưu và chia sẻ hay không. Chọn theo loại nội dung:

| Loại CTA | Tình huống dùng | Ví dụ |
|----------|----------|------|
| Dẫn lưu bài | Nội dung kiến thức, hướng dẫn | "Lưu lại dùng dần" / "Cất vào đây đã" |
| Dẫn chia sẻ | Nội dung đồng cảm, hữu dụng | "@ đứa bạn XX của bạn" / "Gửi cho người đang cần" |
| Dẫn theo dõi | Nội dung dạng series | "Theo dõi để xem tiếp" / "Số sau nói về XX" |
| Dẫn bình luận | Nội dung bàn luận quan điểm | "Bạn thuộc kiểu nào? Kể cho mình ở bình luận" |
| Dẫn nhắn riêng | Nội dung kéo chuyển đổi | "Bình luận 'giải pháp' để nhận bản đầy đủ" |

CTA phải cụ thể. Cấm dùng kiểu chung chung "bấm vào trang chủ" làm CTA chính.

### Bước 5: Caption

Viết caption bổ trợ cho carousel (không lặp lại nội dung trong ảnh):

- Câu đầu: một Hook tách khỏi carousel vẫn đủ ăn
- Thân bài: khai triển một ý trong carousel, thêm góc nhìn cá nhân
- Kết: hô ứng với CTA ở trang cuối
- Hashtag: 3-5 tag đúng ngách, cấm tag chung chung (#doisong #hangngay kiểu này vô dụng)
- Độ dài caption: 300-800 chữ (khoảng tối ưu của Xiaohongshu)

### Bước 6: Chấm điểm tương tác

Chấm theo chuẩn trong `references/scoring-system.md`:

| Tiêu chí | Trọng số | Điểm (1-10) |
|------|------|-------------|
| Độ mạnh Hook | 25% | |
| Nhịp lật trang / lực kéo lật trang | 20% | |
| Mật độ giá trị | 20% | |
| Hiệu quả CTA | 15% | |
| Đồng nhất thị giác | 10% | |
| Chất lượng caption | 10% | |

**Điểm đạt tối thiểu: 7.0 trung bình có trọng số.**

Dưới 7.0 thì tìm tiêu chí yếu nhất, sửa rồi chấm lại.

### Bước 7: Xuất kết quả

Lưu nội dung sau vào `outputs/<chủ đề>/carousel-brief.md`:

```
## Kế hoạch carousel

**Chủ đề:** [chủ đề]
**Mục tiêu:** [mục tiêu]
**Số trang:** [số lượng]
**Công thức Hook:** [tên công thức lấy từ hook-library.md]
**Điểm:** [X.X / 10]

### Bóc tách từng trang

#### Trang 1 (bìa)
- Chữ: "[chữ trang bìa]"
- Hình: [mô tả]

#### Trang 2
- Chữ: "[chữ trên trang]"
- Hình: [mô tả]
- Lực kéo lật trang: [vì sao người đọc lật sang trang sau]

...

### Caption
[caption đầy đủ]

### Ghi chú sản xuất
- [hướng dẫn thiết kế, tư liệu cần chuẩn bị, gợi ý font/bảng màu]
```

## Nhận biết Profile

### Có Profile

- Đọc trường `platform`, chỉnh kích thước và chuẩn dàn trang theo nền tảng (Xiaohongshu 3:4 / 1:1; Instagram 4:5 / 1:1 là tuỳ chọn cho thị trường ngoài)
- Đọc trường `tone` / `voice`, chỉnh giọng điệu cho chữ trang bìa và caption
- Đọc trường `audience`, bảo đảm Hook và góc vào nội dung khớp khán giả mục tiêu
- Đọc trường `positioning`, bảo đảm nội dung bám định vị của kênh
- Đọc trường `visual_style` (nếu có), áp vào phần mô tả hình

### Không có Profile

- Lùi về chế độ chung, mặc định kích thước 3:4 theo chuẩn Xiaohongshu
- Sinh nội dung với giọng trung tính
- Cuối phần đầu ra ghi chú: "Nếu cung cấp Profile của kênh, có thể bám phong cách nền tảng và tông thị giác"
