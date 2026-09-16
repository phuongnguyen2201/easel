---
name: skill-content-postmortem
description: >-
  Hậu kiểm nội dung hai chế độ: (A) một bài: mổ xẻ vì sao viral hay xịt theo Hook, cấu trúc, đề
  tài, thời điểm, nền tảng; (B) nhiều bài: rút quy luật viral thành công thức lặp lại được. Dùng
  khi người dùng nói "bài này sao viral", "sao xịt vậy", "hậu kiểm", "công thức viral".
layer: attribute
---

# Hậu kiểm nội dung và rút quy luật viral

> Mổ xẻ nguyên nhân thành/bại của một bài, hoặc rút từ nhiều bài ra công thức viral lặp lại được.

## Đầu vào

### Chế độ A - hậu kiểm một bài

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Nội dung gốc hoặc link | Có | Toàn văn bài đã đăng (tiêu đề + nội dung + tag) |
| Nền tảng | Có | Facebook / TikTok / YouTube / Zalo / Threads / blog-website / X, v.v. |
| Chỉ số dữ liệu | Nên có | Lượt đọc/xem, thích, lưu, bình luận, chia sẻ, tỉ lệ xem hết, v.v. |
| Thời điểm đăng | Nên có | Ngày và giờ cụ thể |
| Đối chiếu cùng kỳ | Tuỳ chọn | Số liệu trung bình của các bài gần đây cùng kênh, dùng làm baseline so sánh |

### Chế độ B - rút quy luật

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Dữ liệu nhiều bài | Có | Ít nhất 5 bài kèm tiêu đề, tóm tắt nội dung, nền tảng, chỉ số cốt lõi |
| Khoảng thời gian | Nên có | Mốc đầu và mốc cuối của dữ liệu |
| Tiêu chí lọc | Tuỳ chọn | Ngưỡng "viral" và "xịt" do người dùng định nghĩa (ví dụ lưu > 500 là viral) |

Nếu người dùng không đưa chỉ số, hãy phân tích định tính dựa trên chính nội dung và ghi rõ "không có dữ liệu hỗ trợ, chỉ là nhận định về cấu trúc".

## Đầu ra

### Chế độ A - báo cáo hậu kiểm một bài

```markdown
# Hậu kiểm nội dung: [tóm tắt tiêu đề]

## Kết luận nhanh
- Phán định: viral / trung bình / xịt (kèm căn cứ phán định)
- Nguyên nhân cốt lõi: tóm tắt trong một câu

## Mổ xẻ đa chiều

### 1. Phân tích Hook
- Kiểu mở đầu (đặt câu hỏi / xung đột / con số / câu chuyện / gây tò mò)
- Điểm hấp dẫn của 3 giây đầu / 2 dòng đầu (1-10)
- Gợi ý cải thiện

### 2. Cấu trúc nội dung
- Kiểu cấu trúc (tổng - phân - tổng / tăng tiến / song song / cung truyện)
- Mật độ thông tin và nhịp
- Điểm sáng và điểm đứt mạch

### 3. Đánh giá đề tài
- Độ nóng của đề tài (theo trend / thường xanh / ngách hẹp)
- Mức khớp với nỗi đau của khán giả
- Góc nhìn khác biệt

### 4. Thích ứng nền tảng
- Có hợp gu nội dung của nền tảng không
- Thích ứng định dạng (bài ảnh / video / độ dài / chiến lược tag)
- Mức tận dụng cơ chế phân phối

### 5. Thời điểm và nhịp
- Giờ đăng có rơi vào khung giờ khán giả hoạt động không
- Có bắt trend trúng cửa sổ thời gian không
- Nhịp tương tác (vận hành phần bình luận)

### 6. Hình ảnh / ảnh bìa (nếu có)
- Độ hút mắt của ảnh bìa
- Phong cách hình ảnh có khớp tông của nền tảng không

## Đơn thuốc cải thiện
- 3 gợi ý tối ưu cụ thể, làm được ngay (xếp theo thứ tự ưu tiên)

## Ghi chú dữ liệu
- Nguồn dữ liệu và mức tin cậy
```

### Thang điểm các chiều

`references/postmortem-dimensions.md` cung cấp thang điểm 1-10 cho 6 chiều: sức Hook / cấu trúc nội dung / mật độ thông tin / dẫn dắt tương tác / trình bày hình ảnh / thích ứng nền tảng; đề tài và nhịp thời gian là chiều định tính (không chấm điểm).

| Điểm | Ý nghĩa |
|------|------|
| 1-3 | Chiều này có vấn đề rõ, là điểm yếu kéo tụt hiệu quả chung |
| 4-6 | Mức đạt, không lỗi nặng nhưng thiếu điểm nhấn |
| 7-8 | Trên mức trung bình của nội dung cùng loại, có cách làm dùng lại được |
| 9-10 | Chiều này là lợi thế cạnh tranh cốt lõi của bài |

### Chế độ B - báo cáo rút quy luật

```markdown
# Rút quy luật viral: [kênh/chủ đề]

## Tổng quan dữ liệu
- Phạm vi phân tích: X bài, thời gian Y-Z
- Chuẩn viral: [ngưỡng do người dùng đặt hoặc hệ thống suy ra]
- Tỉ lệ viral: X%

## Đặc điểm chung của bài viral
| Chiều | Điểm chung bài viral | Điểm chung bài xịt | Mức khác biệt |
|------|----------|----------|------------|
| Kiểu Hook | | | |
| Hướng đề tài | | | |
| Cấu trúc nội dung | | | |
| Thời điểm đăng | | | |
| Độ dài nội dung | | | |
| Chiến lược tag | | | |
| Phong cách hình ảnh | | | |

## Công thức viral
- Công thức 1: [kiểu đề tài] + [mẫu Hook] + [cấu trúc] = xác suất viral cao
- Công thức 2: ...
- Công thức ngược: [tổ hợp cần tránh]

## Danh sách hành động lặp lại được
1. 3 chiến lược dùng được ngay cho bài tiếp theo
2. Hướng tối ưu trung hạn (điều chỉnh trong 1-2 tuần)

## Giới hạn dữ liệu
- Nêu giới hạn về cỡ mẫu, độ đầy đủ dữ liệu, thay đổi thuật toán nền tảng
```

### Mẫu công thức viral

**[Công thức tiêu đề]** Từ cảm xúc + con số + gây tò mò/tương phản
**[Công thức cấu trúc]** Hook (3 giây đầu) -> chạm nỗi đau -> giải pháp -> kêu gọi hành động
**[Công thức đề tài]** Sự kiện đang nóng x lĩnh vực ngách x góc nhìn phản trực giác

Mỗi lần mổ xẻ cần xuất ra:
- Tên công thức (<=8 chữ, dễ dùng lại)
- Cấu trúc công thức (dùng -> để nối các mắt xích)
- Điều kiện áp dụng được (loại nội dung nào dùng lại được công thức)
- Ví dụ áp dụng (lấy một ví dụ ngay trong lĩnh vực của nhà sáng tạo)

## Các bước thực hiện

### Chế độ A - hậu kiểm một bài

1. **Xác nhận chế độ**: dựa vào đầu vào của người dùng để biết là hậu kiểm một bài hay rút quy luật. Nếu chỉ có một bài, vào chế độ A.
2. **Thu thập bối cảnh**: xác nhận nền tảng, thời điểm đăng, chỉ số dữ liệu. Thiếu dữ liệu thì chủ động hỏi một lần, người dùng không bổ sung thì cứ tiếp tục.
3. **Dựng baseline**: có dữ liệu đối chiếu cùng kỳ thì tính độ lệch; không có thì dùng baseline chung của nền tảng (tham khảo dữ liệu đặc điểm nền tảng trong `references/`).
4. **Mổ xẻ đa chiều**: các chiều chấm điểm được (sức Hook/cấu trúc nội dung/mật độ thông tin/dẫn dắt tương tác/trình bày hình ảnh/thích ứng nền tảng) dùng thang 1-10 trong `references/postmortem-dimensions.md`; đề tài và nhịp thời gian thì nhận định định tính. Mỗi chiều đều phải có nhận định kèm bằng chứng.
5. **Xếp hạng nguyên nhân**: chỉ ra 1-2 yếu tố quyết định thành/bại, tách bạch "yếu tố nội dung" và "yếu tố may mắn" (như được nền tảng đề xuất, trúng cửa sổ trend).
6. **Kê đơn**: xuất 3 gợi ý cải thiện cụ thể, làm được, có thứ tự ưu tiên.
7. **Xuất báo cáo**: dựng báo cáo đầy đủ theo mẫu đầu ra, lưu vào `outputs/`.

### Chế độ B - rút quy luật

> **Thống kê tổng hợp giao cho script, LLM chỉ lo rút quy luật.** Chia ngưỡng top20%, so nhóm viral vs nhóm thường, giao nhiều chiều, đồng xuất hiện của tag đều do [`scripts/aggregate.py`](scripts/aggregate.py) làm (dùng lại `engagement_score`/`engagement_rate`/`cooccurrence`/`pct_change`/`sample_warning` của `../../shared/scripts/social_stats.py`).

1. **Nạp dữ liệu**: nhận dữ liệu nhiều bài, chuẩn hoá thành một mảng JSON thống nhất (mỗi bài gồm tiêu đề, nền tảng, chỉ số số học likes/collects/comments/shares/views, và các trường chiều hook_type/topic/structure/length_bucket/time_bucket/tags), ghi ra file tạm.
2. **Gọi script để tổng hợp**:
   ```bash
   python3 skills/openclaw/skill-content-postmortem/scripts/aggregate.py --input contents.json
   python3 skills/openclaw/skill-content-postmortem/scripts/aggregate.py --input contents.json \
     --metric collects --threshold 500 --cross "hook_type,topic"  # chỉ định trường xếp hạng/ngưỡng tuyệt đối/giao 2 chiều
   ```
   Script tự làm: chia ngưỡng (`--threshold` ưu tiên, không có thì lấy phân vị `--top-pct`), so nhóm viral/nhóm thường (mỗi chiều có count/top_count/top_rate_pct/avg_score/lift_vs_global), giao 2 chiều, đồng xuất hiện của tag, cảnh báo cỡ mẫu.
3. **Nhận diện mẫu + sinh công thức (LLM diễn giải)**: từ `by_dimension`/`cross` đọc ra các tổ hợp giá trị xuất hiện nhiều và có lift cao ở nhóm viral, đúc thành "công thức viral" lặp lại được (đề tài + Hook + cấu trúc).
4. **Tổng kết mặt trái + danh sách hành động (LLM diễn giải)**: từ các giá trị có top_rate thấp / lift âm, đúc ra "danh sách tránh hố", xuất gợi ý phân tầng (dùng ngay / điều chỉnh trung hạn), và chuyển tiếp `warning` về cỡ mẫu của script.
5. **Xuất báo cáo**: dựng theo mẫu, lưu vào `outputs/`.

## Nhận biết Profile

**Khi có Profile:**
- Đọc `identity.md` (định vị kênh, phong cách nội dung, thông tin ngách)
- Đọc `audience.md` (hồ sơ khán giả mục tiêu, nỗi đau và sở thích)
- Đọc `platforms.md` (chiến lược vận hành và kết quả trong quá khứ trên từng nền tảng)
- Khi hậu kiểm, kết hợp định vị kênh để xét độ hợp của đề tài ("đề tài này quá chung so với khán giả của bạn")
- Khi rút quy luật, đưa gợi ý theo giai đoạn của kênh (giai đoạn khởi động vs tăng trưởng vs kiếm tiền)
- Đối chiếu với mục "nội dung có kết quả tốt" trong Profile để so sánh theo thời gian

**Khi không có Profile:**
- Lùi về chế độ chung, phân tích theo quy luật chung của nền tảng
- Không nhận định độ hợp liên quan tới định vị kênh
- Nhắc người dùng bổ sung Profile (`identity.md` / `audience.md` / `platforms.md`) để hậu kiểm chính xác hơn

> Nguồn gốc tự phát triển và các dự án tham khảo xem `EASEL-META.md` cùng thư mục.
