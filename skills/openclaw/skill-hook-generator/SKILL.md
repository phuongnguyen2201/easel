---
name: skill-hook-generator
description: >-
  Sinh 6 biến thể Hook mở đầu cho mọi chủ đề theo công thức đã kiểm chứng, mỗi Hook 2 dòng, có
  kiểm tra số chữ. Dùng khi người dùng nói "viết hook", "mở đầu sao cho hút", "3 giây đầu". Bài
  quảng cáo trọn vẹn dùng copywriting, kịch bản video theo giây dùng video-script.
layer: plan
---

# Sinh biến thể Hook

> Với bất kỳ chủ đề nào, sinh 6 biến thể Hook đã kiểm chứng, mỗi Hook có cấu trúc 2 dòng (mở màn + cú lật), dùng để giữ chú ý ngay đầu nội dung mạng xã hội.

## Đầu vào

Đoạn chủ đề người dùng đưa trong prompt. Có thể là từ khoá, cụm từ hoặc một câu mô tả.

## Đầu ra

6 biến thể Hook, mỗi biến thể gồm:

- **Dòng 1 (mở màn)**: ≤40 chữ, câu khẳng định, bất ngờ/cụ thể/có sức va đập
- **Dòng 2 (cú lật)**: ≤40 chữ, mâu thuẫn/dựng lại/lật ngược dòng mở màn

Định dạng đầu ra:

```
### 1. Dẫn bằng con số
> [mở màn]
> [cú lật]

### 2. Lật nhận thức
> [mở màn]
> [cú lật]

### 3. Lột xác cá nhân
> [mở màn]
> [cú lật]

### 4. Mượn uy tín
> [mở màn]
> [cú lật]

### 5. Tự thú
> [mở màn]
> [cú lật]

### 6. Cú sốc tương lai
> [mở màn]
> [cú lật]
```

Xuất xong thì thêm gợi ý bước tiếp theo:

```
---
Chọn một Hook, mình viết tiếp thành bài hoàn chỉnh cho bạn. Chỉ cần trả lời số thứ tự.
```

## Các bước thực hiện

1. **Lấy chủ đề** - trích chủ đề từ prompt của người dùng; đã có sẵn thì dùng luôn, không cần hỏi lại.
2. **Sinh 6 biến thể Hook** - theo 6 công thức trong [hook-formulas.md](references/hook-formulas.md), làm lần lượt từng công thức:
   - Dẫn bằng con số (Number-led)
   - Lật nhận thức (Contrarian)
   - Lột xác cá nhân (Personal transformation)
   - Mượn uy tín (Authority steal)
   - Tự thú (Admission)
   - Cú sốc tương lai (Future shock)
3. **Kiểm từng Hook** - mỗi Hook phải qua các kiểm tra sau:
   - **Mỗi dòng ≤40 chữ**: lấy số chữ bằng script cho chắc, không đếm bằng mắt. Đưa từng dòng vào
     `python3 skills/shared/scripts/wordcount.py count` (truyền qua stdin), đọc
     trường `social_count` (cách đếm kiểu mạng xã hội = ký tự chữ + từ tiếng Anh + chuỗi số + dấu câu).
     Quá 40 thì dựa vào kết quả rút gọn dòng đó rồi đếm lại, tới khi `social_count ≤ 40`.
   - Dòng mở màn không chứa dấu hỏi
   - Ưu tiên góc nhìn ngôi thứ nhất ("tôi") cho dễ nhập vai (công thức về trend/tương lai/uy tín được ngoại lệ)
   - Ưu tiên dùng chữ số Ả Rập
4. **Xuất theo định dạng có cấu trúc** - xem định dạng đầu ra ở trên.
5. **Đưa gợi ý bước tiếp theo** - cho người dùng biết có thể chọn một Hook để viết thành bài hoàn chỉnh.

## Nhận biết Profile

- **Có Profile**: theo các trường `platform`, `tone`, `language` trong Profile mà chỉnh giọng điệu, lối dùng từ và thói quen của nền tảng cho Hook. Ví dụ Facebook thiên khẩu ngữ, TikTok thiên nhịp điệu.
- **Không có Profile**: lùi về chế độ chung, sinh Hook với giọng trung tính, ghi chú "cung cấp Profile của kênh thì có thể khớp phong cách từng nền tảng".

## Quy tắc

1. Mỗi dòng nghiêm ngặt ≤40 chữ, dùng `../../shared/scripts/wordcount.py count` lấy `social_count` từng dòng để xét, quá hạn là sửa
2. Dòng mở màn cấm dùng câu hỏi
3. Cấm dùng dấu gạch ngang dài (em dash)
4. Cấm từ đệm (thật ra, kiểu như, cho nên, rồi thì)
5. Số luôn viết bằng chữ số Ả Rập, không viết thành chữ
6. Không dùng từ ngập ngừng (có thể, chắc là, khoảng chừng)
7. Ưu tiên góc nhìn ngôi thứ nhất cho dễ nhập vai; công thức trend/cú sốc tương lai/mượn uy tín được phép không có "tôi"
8. Bắt đầu ngay, không viết lời mở đầu hay chào hỏi
