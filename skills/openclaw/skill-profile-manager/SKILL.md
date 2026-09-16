---
name: skill-profile-manager
description: >-
  Quản lý vòng đời hồ sơ (Profile): tạo trống, sửa 6 trường, ghi memory, chuyển, xuất, so sánh.
  Dùng khi người dùng nói "tạo hồ sơ mới", "sửa hồ sơ", "ghi memory", "đổi hồ sơ". Sinh từ mạng xã
  hội → skill-profile-builder, giọng văn → skill-voice-builder, onboarding →
  skill-brand-onboarding.
layer: general
---

# Trình quản lý hồ sơ kênh

> Tạo, sửa, cập nhật memory, xuất, so sánh - quản lý trọn vòng đời hồ sơ

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| action | Có | Loại thao tác: `create` / `edit` / `memory-update` / `export` / `diff` / `list` / `switch` |
| profile_name | Tuỳ thao tác | Tên hồ sơ (bắt buộc khi create, không cần khi list) |
| field | Không | File cần sửa: `identity` / `style` / `audience` / `platforms` / `preferences` / `memory` |
| content | Không | Nội dung cần ghi (dùng khi edit / memory-update) |
| profile_b | Không | Tên hồ sơ thứ hai (bắt buộc khi thao tác diff) |
| data_source | Không | Nguồn dữ liệu cho cập nhật memory: người dùng kể / báo cáo số liệu / phản hồi bài đăng |

## Đầu ra

### Thao tác create

Xuất xác nhận cấu trúc thư mục hồ sơ mới:

```markdown
## Đã tạo xong hồ sơ

**Tên hồ sơ**: {profile_name}
**Thư mục**: profiles/{profile_name}/

### File đã tạo
| File | Trạng thái | Mô tả |
|------|------|------|
| identity.md | ✅ Đã điền | Định vị, khác biệt hoá, hướng nội dung |
| style.md | ✅ Đã điền | Tone giọng, cấu trúc mở đầu, phong cách hình ảnh |
| audience.md | ✅ Đã điền | Nhân khẩu học, sở thích, điểm đau |
| platforms.md | ⬜ Chờ bổ sung | Tài khoản nền tảng, định dạng nội dung |
| preferences.md | ⬜ Chờ bổ sung | Quy tắc tuân thủ, lằn ranh đỏ |
| memory.md | ⬜ Trống | Sẽ tích luỹ dần khi dùng |
```

### Thao tác diff

Xuất bảng đối chiếu từng file của hai hồ sơ:

```markdown
## Đối chiếu hồ sơ: {profile_a} vs {profile_b}

| Chiều | {profile_a} | {profile_b} | Tóm tắt khác biệt |
|------|-------------|-------------|----------|
| Định vị | ... | ... | ... |
| Phong cách | ... | ... | ... |
| Khán giả | ... | ... | ... |
| Nền tảng | ... | ... | ... |
| Sở thích | ... | ... | ... |
```

### Thao tác list

```markdown
## Danh sách hồ sơ hiện có

| Hồ sơ | Độ đầy đủ | Cập nhật cuối | Số mục memory |
|------|--------|----------|----------|
| Chuyên gia công nghệ số | 85% | 2026-07-15 | 12 |
| Nhà sáng tạo hài hước | 60% | 2026-07-10 | 3 |
```

## Các bước thực hiện

### Định tuyến thao tác

1. **Phân tích ý định người dùng**: nhận diện loại action từ câu người dùng nhập
   - "tạo hồ sơ" / "thêm kênh mới" → `create`
   - "sửa hồ sơ" / "chỉnh lại hồ sơ" → `edit`
   - "ghi vào hồ sơ" / "memory hồ sơ" / "nhớ cái này" → `memory-update`
   - "xuất hồ sơ" → `export`
   - "so sánh hồ sơ" / "đối chiếu hai hồ sơ" → `diff`
   - "có những hồ sơ nào" / "danh sách hồ sơ" → `list`
   - "đổi hồ sơ" / "dùng hồ sơ khác" → `switch`

### Luồng create

2. **Kiểm tra hồ sơ đã tồn tại chưa**: đọc thư mục `profiles/`, xác nhận chưa có hồ sơ trùng tên
3. **Copy template**: copy `profiles/_template/` thành `profiles/{profile_name}/`
4. **Hướng dẫn điền thông tin lõi**: hỏi người dùng lần lượt, thu thập các thông tin sau
   - **identity.md**: bạn là ai? làm nội dung gì? khác người khác ở chỗ nào?
   - **style.md**: phong cách ngôn ngữ của bạn thế nào? trang trọng/nhẹ nhàng/hài hước? câu cửa miệng hay dùng?
   - **audience.md**: khán giả mục tiêu của bạn là ai? tuổi, sở thích, điểm đau?
5. **Ghi file**: ghi thông tin đã thu thập vào đúng file theo định dạng template
6. **Nhắc việc tiếp theo**: cho người dùng biết có thể bổ sung platforms.md và preferences.md sau

### Luồng edit

7. **Xác định file**: dựa vào tham số field để suy ra đường dẫn file cần sửa `profiles/{profile_name}/{field}.md`
8. **Đọc nội dung hiện tại**: hiện nội dung hiện có của file đó cho người dùng xác nhận
9. **Áp thay đổi**: sửa trường được chỉ định theo yêu cầu người dùng, giữ nguyên phần còn lại của file
10. **Xác nhận thay đổi**: xuất tóm tắt diff trước và sau khi sửa

### Luồng memory-update

11. **Đọc memory hiện có**: đọc `profiles/{profile_name}/memory.md`
12. **Định dạng mục memory mới**: ghi thêm theo định dạng sau
    ```
    ### {ngày} - {nhãn nguồn}
    - Phát hiện: {phát hiện cụ thể}
    - Đề xuất hành động: {gợi ý làm được ngay}
    ```
13. **Kiểm tra trùng**: đối chiếu với các mục memory đã có, tránh ghi lặp
14. **Ghi nối tiếp**: thêm mục mới vào cuối memory.md

### Luồng export

15. **Tổng hợp hồ sơ**: đọc mọi file .md trong thư mục hồ sơ
16. **Sinh thẻ tóm tắt**: gộp thành một bản tóm tắt hồ sơ có cấu trúc (định dạng Markdown)
17. **Xuất ra outputs/**: lưu thành `outputs/<tên hồ sơ-ngày xuất>/profile-export.md`

### Luồng diff

18. **Đọc hai hồ sơ**: đọc lần lượt mọi file trong `profiles/{profile_a}/` và `profiles/{profile_b}/`
19. **Đối chiếu từng chiều**: đối chiếu theo năm chiều identity / style / audience / platforms / preferences
20. **Sinh bảng khác biệt**: xuất bảng đối chiếu có cấu trúc, làm nổi các điểm khác biệt then chốt

### Luồng list

21. **Quét thư mục profiles/**: liệt kê mọi thư mục con (trừ `_template`)
22. **Tính độ đầy đủ**: kiểm tra 6 file của từng hồ sơ có nội dung thực chất không (không rỗng, không còn là template)
23. **Xuất danh sách**: xuất theo thứ tự độ đầy đủ

## Nhận biết Profile

Bản thân SKILL này chính là công cụ quản lý Profile:

- **Khi có ngữ cảnh Profile**: mặc định thao tác trên hồ sơ đang kích hoạt, edit / memory-update không cần chỉ định lại profile_name
- **Khi không có ngữ cảnh Profile**: thao tác list hiện mọi hồ sơ khả dụng, các thao tác khác bắt buộc chỉ định rõ profile_name
- **Khi dùng lần đầu**: nếu trong thư mục profiles/ chưa có hồ sơ nào (chỉ có _template), tự động vào luồng create

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
