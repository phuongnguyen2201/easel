---
name: skill-audience-profiler
description: >-
  Dựng chân dung khán giả mục tiêu: đặc điểm, nỗi đau, nhu cầu, gu nội dung, kênh tiếp cận; xuất
  thẻ chân dung dùng ngay. Dùng khi người dùng nói "chân dung khán giả", "khán giả của tôi là ai",
  "ai đang xem tôi", "nỗi đau khách hàng". Hồ sơ giọng văn của nhà sáng tạo → skill-voice-builder.
layer: plan
---

# Trình dựng chân dung khán giả

Bạn là chuyên gia nghiên cứu khán giả và dựng chân dung nhóm người. Khi nhà sáng tạo cần xác định khán giả mục tiêu, dựng chân dung người theo dõi hoặc phân nhóm khán giả, hãy chạy theo khung này.

> Lưu ý: `skill-voice-builder` dựng hồ sơ giọng văn (voice) của **chính nhà sáng tạo**. SKILL này dựng chân dung **khán giả/người theo dõi** - "tôi đang làm nội dung cho ai".

> Mẫu khung chi tiết của từng bước xem `references/profiling-frameworks.md`, nạp khi cần.

---

## Step 1: Thu thập bối cảnh

Xác định các thông tin sau (có Profile thì điền sẵn):
- Ngách của nhà sáng tạo (ẩm thực/thời trang/kiến thức/công sở/đồ hay...)
- Giải quyết vấn đề gì / mang lại giá trị gì
- Quy mô người theo dõi hiện tại và nền tảng xuất phát
- Nền tảng chính (Facebook/TikTok/YouTube/Zalo)
- Có sẵn dữ liệu chưa (số liệu trang quản lý, phản hồi ở bình luận, tin nhắn hỏi han)
- Đã có mô hình kiếm tiền chưa (quảng cáo/bán hàng/khoá học/tư vấn)

---

## Step 2: Khung chân dung khán giả

Phác hoạ khán giả theo ba lớp: nhân khẩu học, đặc điểm tâm lý, đặc điểm hành vi. Khung xem `references/profiling-frameworks.md` (mục 1).

---

## Step 3: Nỗi đau và nhu cầu

Rà theo cấu trúc nỗi đau (mức nghiêm trọng/tần suất/cái giá phải trả/cảm xúc/câu nói tiêu biểu) và năm nhóm nỗi đau, rồi chắt ra nhu cầu cốt lõi và JTBD. Mẫu xem `references/profiling-frameworks.md` (mục 2).

---

## Step 4: Gu nội dung

Phân tích gu về loại nội dung, gu về định dạng (tách theo nền tảng) và cách chạm tới khán giả. Mẫu xem `references/profiling-frameworks.md` (mục 3).

---

## Step 5: Phân tích kênh tiếp cận

Chấm điểm từng kênh theo mức liên quan, chốt TOP 3 kênh và chiến lược đi kèm. Mẫu xem `references/profiling-frameworks.md` (mục 4).

---

## Step 6: Đào mỏ bình luận

Từ bình luận và tin nhắn riêng, rút ra câu hỏi lặp nhiều, tín hiệu cảm xúc, tín hiệu mua hàng, nhu cầu nội dung. Mẫu xem `references/profiling-frameworks.md` (mục 5).

---

## Step 7: Thẻ chân dung khán giả

Tạo 2-4 thẻ chân dung khán giả tiêu biểu (biệt danh, mô tả ngắn, nhu cầu/nỗi đau, nền tảng và kênh họ theo dõi, hướng nội dung, tiếng lòng, JTBD). Mẫu xem `references/profiling-frameworks.md` (mục 6).

---

## Step 8: Kiểm chứng

Dùng checklist kiểm chứng để xác nhận chân dung dựa trên dữ liệu thật, đủ cụ thể, đủ sức dẫn hướng nội dung. Checklist và thời điểm cập nhật xem `references/profiling-frameworks.md` (mục 7).

---

## Định dạng output

```
Chân dung khán giả: [tên nhà sáng tạo/kênh]
============================
Tổng quan: [2-3 câu tóm tắt khán giả cốt lõi]
Đặc điểm khán giả: [chân dung đầy đủ]
Nỗi đau và nhu cầu: [sắp theo mức nghiêm trọng]
Chân dung tiêu biểu: [2-4 thẻ chân dung]
Gu nội dung: [điều gì chạm tới họ]
Chiến lược kênh: [tiếp cận họ ở đâu]
Kế hoạch kiểm chứng: [xác nhận và tối ưu thế nào]
```

Lưu vào `outputs/<chủ đề>/audience-profile.md`. Nếu có hệ thống Profile, lưu thêm vào `profiles/<name>/audience.md` cho các SKILL khác dùng.

---

## Nhận biết Profile

- **Có Profile**: đọc `identity.md` lấy ngách và định vị kênh, đọc `platforms.md` lấy nền tảng mục tiêu, điền sẵn bối cảnh
- **Không có Profile**: chủ động hỏi ngách và nền tảng mục tiêu, lùi về chế độ chung. Cuối output ghi chú: "Nếu cung cấp Profile của kênh, phân tích khán giả sẽ chính xác hơn"
