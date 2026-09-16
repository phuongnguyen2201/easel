---
name: video-script
description: >-
  Viết kịch bản video ngắn 7-60 giây (Hook chấm điểm, bấm giờ theo giây, phụ đề, bìa) hay dài 1-30
  phút (giữ chân, ngắt nhịp, hook dẫn tiếp, chương) cho TikTok, Reels, YouTube. Dùng khi người
  dùng nói "kịch bản video", "kịch bản TikTok", "viết lời video". Kế hoạch series →
  video-strategy.
layer: produce
---

# Sinh kịch bản video

> Tự khớp chế độ video ngắn hay video trung/dài theo thời lượng mục tiêu, sinh kịch bản có cấu trúc tối ưu cho tỉ lệ giữ chân.

## Đầu vào

| Trường | Bắt buộc | Diễn giải | Ví dụ |
|------|------|------|------|
| Chủ đề | Có | Chủ đề video | "Vì sao Rust đang thay thế C++" |
| Thời lượng mục tiêu | Có | Số giây hoặc số phút | 30 giây / 10 phút |
| Nền tảng | Không | TikTok/Reels/Facebook/YouTube (mặc định suy từ thời lượng)| TikTok |
| Loại nội dung | Không | Khoa học thường thức/hướng dẫn/đánh giá/seeding/bình luận/tạp đàm | Khoa học thường thức |
| Ý chính cốt lõi | Có | Thông tin then chốt phải phủ | An toàn bộ nhớ, hiệu năng... |
| Tông giọng | Không | Chuyên nghiệp/nhẹ nhàng/sắc sảo/như đang trò chuyện (mặc định: như đang trò chuyện)| Nhẹ nhàng |

## Tự xác định chế độ

| Thời lượng | Chế độ | Nền tảng điển hình | Chỉ số then chốt |
|------|------|----------|----------|
| 7-15 giây | Video ngắn - siêu tốc | TikTok/Reels | Tỉ lệ xem hết ở 3 giây |
| 15-60 giây | Video ngắn - chuẩn | TikTok/Reels/Facebook | Tỉ lệ xem hết, chia sẻ DM, lưu |
| 1-5 phút | Video trung | Facebook/TikTok/YouTube | Giữ chân 5 giây, tỉ lệ tương tác |
| 5-30 phút | Video dài | YouTube | Giữ chân 30 giây, tỉ lệ xem trọn |

**Chuẩn tốc độ nói**: khoảng 250 chữ/phút.

---

## Chế độ video ngắn (≤60 giây)

### Step 1 - Thiết kế Hook (3 biến thể)

Chọn 3 trong 5 kiểu Hook, mỗi kiểu sinh một biến thể:

| Kiểu | Hợp cảnh nào | Ví dụ |
|------|---------|------|
| Khoảng trống tò mò | Kiến thức lạ, phản trực giác | "Việc bạn làm mỗi ngày thật ra đang hại bạn" |
| Phá vỡ khuôn mẫu | Trái lệ thường, thách thức nhận thức | "Quên hết những gì bạn từng học về XX đi" |
| Kích hoạt danh tính | Khán giả đúng tệp | "Nếu bạn là XX, clip này nhất định phải xem hết" |
| Chạm nỗi đau | Vướng mắc có thật | "Rõ ràng đã rất cố gắng mà vẫn không hiệu quả?" |
| Bảo chứng uy tín | Có số liệu/nghiên cứu đỡ | "Nghiên cứu mới nhất phát hiện: XX hoá ra là sai" |

Mỗi Hook chấm theo 4 chiều (mỗi mục 1-5, thang 20): độ tò mò, hiệu quả phá vỡ, kích hoạt danh tính, độ rõ trong 3 giây. Chọn điểm cao nhất làm Hook chính.

### Step 2 - Kịch bản bấm giờ theo giây

Nén cấu trúc theo thời lượng:

| Thời lượng | Cấu trúc |
|------|------|
| 7-15 giây | Hook(0-2s) + Giá trị cốt lõi(2-10s) + Chốt(10-15s) |
| 15-30 giây | Hook(0-3s) + Nỗi đau(3-8s) + Giải pháp(8-20s) + Chốt CTA(20-30s) |
| 30-60 giây | Hook(0-3s) + Nỗi đau(3-8s) + Giải pháp(8-40s) + Insight+CTA(40-60s) |

Định dạng kịch bản:
```
[0-3s] HOOK
Lời thoại: "..."
Phụ đề: "..."
Hình ảnh: [mô tả]

[3-8s] Nỗi đau
Lời thoại: "..."
Hình ảnh: [mô tả]
```

Mỗi câu ≤15 chữ, văn nói, thêm chú thích trong ngoặc (ngắt/nhấn/biểu cảm).

### Step 3 - caption + ảnh bìa

**caption**: 100-300 chữ, mở đầu bằng biến thể Hook (không lặp lại Hook trong video), chia sẻ DM > lưu > thích.
**hashtags**: 3-5 tag đúng ngách, không dùng tag chung chung.
**Ảnh bìa**: tiêu đề lớn 3-5 chữ + mô tả hình ảnh + biểu cảm.

### Step 4 - Chấm điểm chất lượng (thang 100)

| Chiều | Trọng số | Điểm kiểm |
|------|------|--------|
| Độ mạnh của Hook | 25 | Khoảng trống tò mò, hiệu quả phá vỡ, độ rõ trong 3 giây |
| Chất lượng nội dung | 25 | Mật độ giá trị, cấu trúc, độ rõ của nỗi đau - giải pháp |
| caption+CTA | 20 | Dài 100+ chữ, CTA hướng chia sẻ, biến thể Hook |
| Đúng chuẩn định dạng | 15 | Vùng an toàn 9:16, khớp thời lượng, ảnh bìa |
| Tín hiệu thuật toán | 15 | Tối ưu lưu/chia sẻ, tính nguyên bản |

≥80 điểm thì giao, <60 điểm thì làm lại rồi chấm lại.

---

## Chế độ video trung/dài (>60 giây)

> Phương pháp chi tiết để tối ưu tỉ lệ giữ chân (điểm ngắt nhịp / hook dẫn tiếp / cấu trúc chương / đường cong giữ chân) xem `references/retention-scripting-guide.md`.

### Step 1 - Tính cấu trúc

Chia các đoạn theo thời lượng mục tiêu:
- **Hook**: 0:00-0:30 (video ngắn rút còn 0:00-0:10)
- **Mở đầu**: 0:30-2:00
- **CTA lần đầu**: khoảng mốc 25%
- **Kéo giữ chân trở lại**: khoảng mốc 60%
- **Kết**: 60 giây cuối
- **Số chữ mục tiêu** = thời lượng (phút) × 250

### Step 2 - Viết Hook (ba đoạn)

| Giai đoạn | Thời gian | Mục tiêu |
|------|------|------|
| Bắt mắt | 0-5s | Câu quan trọng nhất cả clip, không để intro |
| Hứa hẹn | 5-15s | Xem hết thì được gì, cụ thể cảm nhận được |
| Treo | 15-30s | Không xem thì mất gì |

### Step 3 - Các đoạn nội dung

Cấu trúc mỗi đoạn: ngắt nhịp -> phần chính -> tóm nhỏ -> hook dẫn tiếp.
**Ngắt nhịp** mỗi 60-90 giây một lần (video ngắn mỗi 15-30 giây), các kiểu: [cắt cảnh] [hình ảnh] [hiệu ứng âm thanh] [cú sốc số liệu].

### Step 4 - CTA và phần kết

- CTA lần đầu (mốc 25%): mềm, kiểu trò chuyện, 10-15 giây
- Kéo giữ chân trở lại (mốc 60%): "Tiếp theo mới là phần then chốt nhất"
- CTA kết: kêu gọi dứt khoát + hé lộ số sau, **không nói "cảm ơn đã xem"**

### Step 5 - Đánh dấu rủi ro giữ chân

Quét toàn bản thảo, đánh dấu cảnh báo ⚠️ ở vùng nguy hiểm (ít nhất 3 chỗ) + phương án xử lý.

## Định dạng đầu ra

Sản phẩm ghi vào `outputs/<chủ đề>/`. Bao gồm:
- Metadata kịch bản (chủ đề/thời lượng/nền tảng/số chữ)
- Kịch bản phân đoạn đầy đủ (có timecode, lời thoại, phụ đề, gợi ý hình ảnh)
- Nhật ký ngắt nhịp (timestamp/kiểu/diễn giải)
- Bản đồ rủi ro giữ chân (video trung/dài) / chấm điểm chất lượng (video ngắn)
- Ghi chú dựng phim

## Kiểm chất lượng

- [ ] Số chữ khớp thời lượng (250 chữ/phút, ±10%): **dùng script để phán, không ước lượng**. Đưa toàn bộ lời thoại (bỏ timecode, gợi ý hình ảnh và các dòng không phải lời thoại) vào
  `python3 skills/shared/scripts/wordcount.py check --target <số phút x 250> --tolerance 0.1` (truyền qua stdin), mã thoát 0 = đạt; khác 0 thì script báo "còn cần thêm/bớt X chữ", theo đó tăng giảm lời thoại rồi chạy lại đến khi qua.
- [ ] Hook đầy đủ (video ngắn: 3 biến thể có chấm điểm; video trung/dài: ba đoạn)
- [ ] Tần suất ngắt nhịp đạt chuẩn
- [ ] CTA đặt đúng vị trí
- [ ] Toàn bản thảo là văn nói, câu ngắn, không giống văn viết
- [ ] Phần kết có năng lượng, không có lời chốt thừa

## Nhận biết Profile

- **Có Profile**: đọc platform để khoá nền tảng, audience để chỉnh cách dùng từ, tone để khớp phong cách, cta_style để dùng câu quen thuộc
- **Không có Profile**: mặc định suy nền tảng từ thời lượng, tông giọng như đang trò chuyện
