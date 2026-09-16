---
name: post-formatter
description: >-
  Cấu trúc chủ đề theo khung kinh điển PAS, AIDA, BAB, STAR, SLAY thành bài ngắn tối đa 20 dòng,
  dễ đọc trên mobile, hợp bài chữ trên Facebook, LinkedIn, blog. Dùng khi người dùng nói "viết
  theo PAS", "công thức AIDA", "viết theo khung". Khác social-content: viết tự do, không bó khung.
layer: produce
---

# Đóng khung bài đăng

> Dùng năm khung kinh điển PAS / AIDA / BAB / STAR / SLAY để cấu trúc một chủ đề thành bài dài đăng mạng xã hội bằng tiếng Việt.
> Chỉ lo "áp khung + trình bày", không sáng tác tự do (đó là việc của social-content).

## Đầu vào

Trích các thông tin sau từ prompt của người dùng, thiếu cái nào thì hỏi ngay:

| Trường | Mô tả | Khi thiếu |
|------|------|----------|
| Chủ đề | Chủ đề gói trong một câu, hoặc một đoạn tư liệu/ghi chú/dữ liệu | Bắt buộc, thiếu thì hỏi |
| Khung | Một trong PAS / AIDA / BAB / STAR / SLAY | Thiếu thì tự chọn theo mục đích nội dung |
| Nền tảng | Facebook / TikTok / YouTube (Shorts) / Zalo / blog, website | Thiếu thì viết kiểu mạng xã hội phổ thông |
| Bổ sung | Dữ kiện, số liệu, tông giọng, độc giả mục tiêu | Có thể bỏ trống |

Nếu thiếu cả chủ đề lẫn khung, dùng một lượt AskUserQuestion hỏi gọn cả chủ đề và khung, rồi thêm một câu
"Còn gì tôi cần biết nữa không? Số liệu, tông giọng hay viết cho ai". Đủ thông tin thì viết luôn, không dài dòng.

## Đầu ra

Một bài đăng tiếng Việt đăng được ngay, đặt trong khối mã, không lời mở không lời kết. Cấu trúc:

- Dòng đầu là hook
- Dòng hai là cú lật/đối lập
- Phần thân (chia giai đoạn theo khung đã chọn)
- Kết + một câu kêu gọi tương tác bằng tiếng Việt

## Các bước thực hiện

1. **Chốt khung**: người dùng chỉ định thì dùng đúng cái đó; không chỉ định thì theo `skills/shared/references/copy-frameworks.md`
   phần "quy tắc chọn khung", chọn một cái theo mục đích nội dung. Đã chọn thì chỉ dùng một, không trộn.
2. **Tách chủ đề**: định nghĩa từng giai đoạn của khung xem `skills/shared/references/copy-frameworks.md`, mỗi giai đoạn chiếm mấy dòng xem
   `references/frameworks.md` (phân bổ số dòng); chia chủ đề và tư liệu vào từng giai đoạn.
3. **Viết thân bài**: áp đúng quy tắc trình bày tiếng Việt trong `references/formatting.md` -
   200-250 chữ, tối đa 20 dòng, chừa dòng trống giữa các đoạn, câu ngắn, bỏ gạch ngang dài, khử mùi AI.
4. **Gắn CTA**: kết bằng lời dẫn kiểu mạng xã hội Việt (theo dõi / lưu bài / bình luận cùng bàn), một câu là đủ,
   bám mục đích nội dung, không dùng kiểu tiếng Anh như "Repost if".
5. **Tự kiểm**: rà từng mục theo checklist ở cuối `references/formatting.md` (hook, giọng dịch,
   danh sách, phần kết). **Số chữ, số dòng lấy kết quả chắc chắn bằng script, không đếm bằng mắt**:
   - Số chữ: `python3 skills/shared/scripts/wordcount.py check --target 225 --tolerance 0.12`
     (truyền thân bài qua stdin), mã thoát 0 = nằm trong khoảng 200-250; khác 0 thì script báo "cần thêm/bớt X chữ", chỉnh theo rồi chạy lại.
   - Số dòng: cho thân bài qua `wc -l` đếm một lượt, xác nhận tối đa 20 dòng.
   Vượt giới hạn thì sửa tới khi script chấm đạt.
6. **Xuất kết quả**: chỉ đưa bài đăng cuối, đặt trong khối mã, không giải thích thêm.

## Ranh giới với social-content

- **post-formatter (SKILL này)**: áp chặt một khung marketing, cho ra một bài đăng có cấu trúc cố định.
  Dùng khi người dùng nói rõ "viết theo PAS", "áp AIDA", "bài đăng có cấu trúc".
- **social-content**: sáng tác tự do, định dạng gốc cho nhiều nền tảng, đủ hook/hashtag/chiến lược tương tác, không bó khung.
- Nói gọn: cần khung, cần cấu trúc → SKILL này; cần tự do phát huy, cần trọn bộ nguyên liệu → social-content.

## Nhận biết Profile

- Có Profile: nạp tông giọng, mẫu câu quen dùng, độc giả mục tiêu, từ cấm của kênh vào, để đầu ra theo khung
  bám persona của kênh đó; nền tảng mặc định lấy nền tảng chính trong Profile.
- Không có Profile: lùi về chế độ mạng xã hội phổ thông, viết theo quy tắc mặc định trong `references/formatting.md`.

## Quy tắc cứng

- Chỉ trả về bài đăng thành phẩm, không thêm bình luận ngoài lề.
- Số chữ, số dòng kiểm bằng script: số chữ chạy `skills/shared/scripts/wordcount.py check` (theo chuẩn social_count), số dòng dùng `wc -l`, lấy kết quả script làm chuẩn, vượt là sửa.
- Toàn bài không dùng gạch ngang dài (em dash).
- Danh sách thì đúng ba mục, không thì thôi, không kê cho đủ số.
- Kiến thức chuyên môn (giải thích khung, quy tắc trình bày) nằm hết trong references/, file này chỉ nói quy trình.
