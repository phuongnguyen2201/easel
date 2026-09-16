---
name: skill-cross-platform-diff
description: >-
  Phân tích sâu cùng một chủ đề khác nhau thế nào trên Facebook/TikTok/YouTube/Zalo: hình thức, gu
  khán giả, ngôn ngữ, phân phối, kiếm tiền. Dùng khi người dùng nói "Facebook với TikTok khác gì",
  "lên YouTube thì làm sao", "nền tảng nào hợp". Viết lại bài dùng skill-content-repurposing.
layer: discover
---

# Phân tích khác biệt nội dung giữa các nền tảng

> Phân tích cùng một chủ đề được thể hiện khác nhau ra sao trên từng nền tảng mạng xã hội, xuất chiến lược thích ứng cho từng nền tảng.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Chủ đề/đề tài nội dung | Có | Chủ đề, từ khoá hoặc một đoạn nội dung cần phân tích |
| Nền tảng mục tiêu | Nên có | Danh sách nền tảng cần so sánh (mặc định quét toàn bộ nền tảng) |
| Mục đích phân tích | Nên có | "tôi muốn đăng nội dung này lên các nền tảng" / "muốn hiểu khác biệt giữa các nền tảng" / "chọn nền tảng chủ lực" |
| Nội dung sẵn có | Tuỳ chọn | Nếu người dùng đã có nội dung trên một nền tảng, dùng làm mốc so sánh |
| Ngách / ngành | Tuỳ chọn | Ngách khác nhau thì khác biệt giữa các nền tảng cũng khác nhau |

Các nền tảng hỗ trợ: Facebook, TikTok, YouTube (Shorts), Zalo, Threads, blog/website, X/Twitter.

## Đầu ra

```markdown
# Phân tích khác biệt giữa các nền tảng: [chủ đề/đề tài]

## Tóm tắt phân tích
- Chủ đề phân tích: [chủ đề]
- Nền tảng so sánh: [danh sách nền tảng]
- Thời điểm phân tích: [ngày]

## Toàn cảnh khác biệt giữa các nền tảng

### Ma trận so sánh
| Chiều | Facebook | TikTok | YouTube | Zalo | Threads | Blog/Website |
|------|--------|------|-----|------|------|--------|
| Hình thức nội dung chủ lực | | | | | | |
| Chân dung khán giả cốt lõi | | | | | | |
| Hệ ngôn ngữ/giọng điệu | | | | | | |
| Logic phân phối traffic | | | | | | |
| Vòng đời nội dung | | | | | | |
| Đường kiếm tiền | | | | | | |
| Độ hợp của chủ đề này | | | | | | |

### Phân tích từng nền tảng

#### [tên nền tảng]
- **Chủ đề này thường xuất hiện thế nào trên nền tảng này**: hình thức, phong cách, góc nhìn
- **Kỳ vọng của khán giả**: người dùng nền tảng này mong gì khi thấy chủ đề đó
- **Hệ ngôn ngữ**: thói quen dùng từ, giọng điệu, cách diễn đạt
- **Logic traffic**: chủ đề này lấy lượt xem bằng cách nào (tìm kiếm / đề xuất / lan truyền xã hội)
- **Đặc điểm ca thành công**: nội dung về chủ đề này chạy tốt trên nền tảng này có gì giống nhau
- **Cẩm nang tránh hố**: những hố dễ sụp khi làm chủ đề này trên nền tảng này
- **Khả năng kiếm tiền**: đường thương mại hoá của chủ đề này trên nền tảng này

(mỗi nền tảng mục tiêu một mục)

## Insight khác biệt cốt lõi
1. [phát hiện khác biệt quan trọng nhất giữa các nền tảng]
2. [phát hiện quan trọng thứ hai]
3. ...

## Gợi ý chọn nền tảng
- **Nên làm chủ lực**: [1-2 nền tảng hợp nhất + lý do]
- **Bố trí hỗ trợ**: [nền tảng đáng vận hành song song + chiến lược]
- **Không nên**: [nền tảng không hợp + lý do]

## Chiến lược thích ứng
Với mỗi nền tảng được đề xuất, nêu các điểm chuyển đổi từ "nội dung gốc" sang "nội dung đã thích ứng nền tảng":
- Hướng viết lại tiêu đề
- Điều chỉnh cấu trúc nội dung
- Chuyển đổi giọng điệu và từ ngữ
- Yêu cầu định dạng và độ dài
- Chiến lược tag/hashtag
- Gợi ý thời điểm đăng

## Lưu ý
- Ghi chú về tính thời điểm: luật và thuật toán nền tảng thay đổi liên tục
- Căn cứ phân tích (thông tin công khai của nền tảng + hiểu biết ngành)
```

## Các bước thực hiện

1. **Xác định phạm vi phân tích**
   - Xác nhận chủ đề/đề tài và nền tảng mục tiêu
   - Nếu người dùng không chỉ định nền tảng, mặc định phân tích 6 nền tảng chính: Facebook, TikTok, YouTube, Zalo, Threads, blog/website
   - Xác nhận mục đích phân tích (hiểu khác biệt / chọn nền tảng / làm thích ứng)

2. **Nạp kiến thức nền tảng**
   - Đọc `references/platform-traits.md` để lấy đặc điểm cơ bản của từng nền tảng
   - Đây là kiến thức nền, không xuất trực tiếp, chỉ dùng để chống lưng cho phân tích

3. **Phân tích giao chủ đề - nền tảng**
   - Với mỗi nền tảng mục tiêu, phân tích mức độ thích ứng của chủ đề trên nền tảng đó:
     - Hình thức nội dung: chủ đề này thường xuất hiện dưới dạng gì (bài ảnh / video ngắn / video dài / hỏi đáp / bài viết)
     - Kỳ vọng khán giả: người dùng nền tảng này muốn nhận được gì (kiến thức / giải trí / seeding / thảo luận / đồng cảm)
     - Hệ ngôn ngữ: từ ngữ, giọng điệu, phong cách khi bàn chủ đề này trên nền tảng đó
     - Nguồn traffic: trên nền tảng này, chủ đề đó lấy lượt xem chủ yếu qua kênh nào

4. **Rút khác biệt**
   - So sánh ngang giữa các nền tảng, chỉ ra điểm khác biệt then chốt
   - Tập trung vào "khác biệt nhu cầu thông tin" của cùng một chủ đề trên các nền tảng (cùng một từ khoá, mục đích khi tìm trên YouTube và khi tìm trên TikTok hoàn toàn khác nhau)
   - Đúc ra quy luật khác biệt (ví dụ "nền tảng càng chuyên sâu càng cần luận cứ, nền tảng càng vụn càng cần cảm xúc")

5. **Đánh giá độ thích ứng**
   - Kết hợp đặc tính chủ đề và đặc điểm nền tảng để chấm mức thích ứng của từng nền tảng
   - Các chiều đánh giá: độ khớp tự nhiên của nội dung, độ bão hoà cạnh tranh, khả năng kiếm tiền, chi phí vận hành
   - Đưa gợi ý phân tầng chủ lực/hỗ trợ/không nên

   ### Chấm điểm độ thích ứng (mỗi mục 1-5 điểm)

   | Chiều | 1 điểm | 3 điểm | 5 điểm |
   |------|------|------|------|
   | Độ khớp nội dung | Chủ đề gần như không ai quan tâm trên nền tảng này | Có khán giả nhất định nhưng không phải dòng chính | Nội dung loại này có lượt xem lớn, tương tác cao |
   | Bão hoà cạnh tranh | Các kênh top độc chiếm, người mới gần như hết cửa | Có cạnh tranh nhưng vẫn khác biệt hoá được | Nội dung khan hiếm, cung không đủ cầu |
   | Kiếm tiền khả thi | Loại nội dung này trên nền tảng chưa có mô hình kinh doanh | Nhận booking quảng cáo được nhưng ít nhãn hàng | Nhãn hàng hoạt động mạnh, đường kiếm tiền rõ ràng |
   | Chi phí vận hành | Phải đăng đều tần suất cao + chăm tương tác liên tục | Mức đầu tư vận hành trung bình | Nội dung có đuôi dài mạnh, ít áp lực vận hành |

6. **Sinh chiến lược thích ứng**
   - Với các nền tảng được đề xuất, đưa chiến lược thích ứng nội dung cụ thể
   - Không viết lại nội dung (đó là việc của repurposing), chỉ đưa "chỉ dẫn hướng chuyển đổi"
   - Gồm hướng tiêu đề, điều chỉnh cấu trúc, chuyển giọng điệu, yêu cầu định dạng, chiến lược tag

7. **Xuất báo cáo**
   - Dựng báo cáo phân tích đầy đủ theo mẫu
   - Lưu vào `outputs/`

## Nhận biết Profile

**Khi có Profile:**
- Đọc identity.md (định vị ngách), platforms.md (nền tảng chủ lực hiện tại), audience.md (hồ sơ khán giả)
- Gợi ý chọn nền tảng bám theo năng lực sẵn có của kênh ("bạn mạnh bài dài nhiều ảnh, YouTube và blog/website hợp với bạn hơn TikTok")
- Chiến lược thích ứng có tính tới tài sản nội dung sẵn có ("bài phân tích sâu trên blog/website của bạn có thể tách thành bộ carousel cho Facebook")
- Gợi ý đường kiếm tiền gắn với mục tiêu thương mại hoá trong Profile

**Khi không có Profile:**
- Lùi về chế độ chung, phân tích khách quan khác biệt giữa các nền tảng
- Gợi ý chọn nền tảng dựa trên đặc tính chủ đề chứ không dựa trên đặc tính kênh
- Không phán "bạn hợp cái gì" theo cá nhân, chỉ phán "chủ đề này hợp nền tảng nào"

> Nguồn gốc tự phát triển và các nghiên cứu/dự án mã nguồn mở tham khảo xem `EASEL-META.md` cùng thư mục.
