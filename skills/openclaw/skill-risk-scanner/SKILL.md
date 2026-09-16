---
name: skill-risk-scanner
description: >-
  Đánh giá độ nguyên bản, rủi ro bản quyền: dấu hiệu xào bài/đăng lại, nguồn ảnh/nhạc, chuẩn trích
  dẫn; dựa trên LLM, không check trùng kỹ thuật. Dùng khi người dùng nói "có đạo văn không", "dùng
  ảnh này được không", "bản quyền nhạc", "có bị kiện không". Từ nhạy cảm → skill-quality-gate.
layer: publish
---

# Đánh giá độ nguyên bản và rủi ro bản quyền của nội dung

> Dựa trên khả năng phân tích văn bản của LLM, đánh giá rủi ro về độ nguyên bản và rủi ro bản quyền tư liệu, xuất báo cáo rủi ro định tính kèm đề xuất cải thiện.

## Tuyên bố giới hạn năng lực

SKILL này dựa trên phân tích văn bản của LLM, **không bao gồm** các năng lực kỹ thuật sau:

- **Không check trùng kỹ thuật** - không tính được độ tương đồng cosine hay tỉ lệ trùng lặp chính xác, việc đó cần API ngoài như Copyleaks / Originality.ai
- **Không xuất điểm tương đồng** - mọi kết luận rủi ro đều là mức định tính (thấp/trung bình/cao), không bịa phần trăm hay số thập phân
- **Không nhận diện nội dung ảnh** - không đọc được EXIF, không dò watermark, không truy ra nguồn ảnh; rủi ro ảnh được đánh giá dựa trên mô tả nguồn do người dùng cung cấp
- **Không đối chiếu vân tay âm thanh** - không nhận ra được bản nhạc BGM, chỉ kết luận rủi ro dựa trên nguồn nhạc người dùng ghi chú

## Khác gì các SKILL còn lại

| SKILL | Định vị | Trọng tâm kiểm tra |
|---|---|---|
| **risk-scanner** (SKILL này) | Độ nguyên bản + rủi ro bản quyền | Nhận diện mẫu xào bài, rủi ro bản quyền tư liệu, tuân thủ khi trích dẫn |
| skill-quality-gate | Tuân thủ nền tảng + chất lượng nội dung | Từ nhạy cảm, quy tắc nền tảng, luật quảng cáo, từ tuyệt đối, vi phạm về y tế |
| skill-publish-checklist | Kiểm tính đầy đủ | Có sót tiêu đề, sót ảnh bìa hay không |

## Đầu vào

| Tham số | Bắt buộc | Mô tả |
|------|------|------|
| Nội dung cần kiểm | Có | Thân bài viết, kịch bản, bản thảo bài dài |
| Mô tả nguồn tư liệu | Không | Người dùng mô tả nguồn ảnh/audio/video (ví dụ "ảnh lấy từ Unsplash", "BGM dùng nhạc có sẵn của TikTok") |
| Văn bản nguồn tham khảo | Không | Văn bản hoặc URL của bài gốc đã tham khảo, dùng để đối chiếu mức độ viết lại |
| Nền tảng đích | Không | Tên nền tảng sẽ đăng, dùng để khớp quy tắc bản quyền của nền tảng |

## Đầu ra

Báo cáo đánh giá rủi ro dạng Markdown, cấu trúc như sau:

```markdown
# Báo cáo đánh giá rủi ro

## Mức rủi ro tổng thể: 🟢 thấp / 🟡 trung bình / 🔴 cao

## 1. Đánh giá độ nguyên bản của văn bản

### Quét mẫu xào bài
- [kết quả quét và phát hiện cụ thể]

### Đánh giá tính độc nhất của nội dung
- [có trải nghiệm cá nhân/dữ liệu độc quyền/quan điểm nguyên bản hay không]

### Kiểm chuẩn trích dẫn
- [trích dẫn có ghi nguồn không, số liệu có ghi xuất xứ không]

## 2. Rủi ro bản quyền tư liệu (chỉ xuất khi người dùng có mô tả nguồn tư liệu)

### Tư liệu ảnh
- [kết luận dựa trên nguồn người dùng mô tả]

### Audio/BGM
- [kết luận dựa trên nguồn người dùng mô tả]

## 3. Rủi ro thương hiệu và nhãn hiệu
- [rủi ro khi dùng tên thương hiệu/nhãn hiệu được nhắc trong bài]

## 4. Danh sách rủi ro

### Bắt buộc xử lý (chặn đăng)
- [mục rủi ro cao]

### Nên xử lý (không chặn nhưng có nguy cơ)
- [mục rủi ro trung bình]

## 5. Đề xuất cải thiện
- [đề xuất thao tác cụ thể cho từng mục rủi ro]
```

Định nghĩa mức rủi ro:
- **Rủi ro thấp** - nội dung có phần nguyên bản rõ rệt, trích dẫn đúng chuẩn, nguồn tư liệu rõ ràng
- **Rủi ro trung bình** - có phần nghi xào bài hoặc nguồn tư liệu không rõ, nên sửa rồi mới đăng
- **Rủi ro cao** - có dấu hiệu bê bài/sao chép rõ ràng hoặc nguy cơ xâm phạm bản quyền, không nên đăng thẳng

## Các bước thực hiện

### Step 1 - Chốt đầu vào và phạm vi kiểm tra

1. Đọc nội dung cần kiểm mà người dùng đưa
2. Xác nhận có mô tả nguồn tư liệu hay không (nguồn ảnh, audio, video)
3. Xác nhận có văn bản nguồn tham khảo hay không (để đối chiếu mức độ viết lại)
4. Xác nhận nền tảng đích (để khớp quy tắc bản quyền riêng của nền tảng)
5. Không có mô tả nguồn tư liệu thì bỏ phần đánh giá bản quyền tư liệu, ghi rõ trong báo cáo "người dùng chưa cung cấp thông tin nguồn tư liệu, không đánh giá được rủi ro bản quyền tư liệu"

### Step 2 - Quét mẫu xào bài trong văn bản

Quét từng đoạn, theo phần "1. Nhận diện mẫu xào bài" trong `references/washing-patterns.md` để bắt ba nhóm dấu hiệu: thay từ đồng nghĩa một cách máy móc, đổi cấu trúc câu nhưng sao y luận điểm, bê nguyên đoạn rồi xáo thứ tự. Mỗi dấu hiệu tìm được phải trích đúng đoạn văn và nêu lý do; không thấy gì thì nói rõ "không phát hiện mẫu xào bài rõ rệt".

### Step 3 - Đánh giá tính độc nhất của nội dung

Theo phần "2. Đánh giá tính độc nhất của nội dung" trong `references/washing-patterns.md`, xét bài có trải nghiệm cá nhân, dữ liệu độc quyền, quan điểm nguyên bản, chi tiết cụ thể hay không, rồi kết luận độ nguyên bản cao/trung bình/thấp.

### Step 4 - Kiểm chuẩn trích dẫn

Theo phần "3. Kiểm chuẩn trích dẫn" trong `references/washing-patterns.md`, soát việc ghi nguồn cho trích dẫn quan điểm, trích dẫn số liệu, ảnh chụp màn hình; nếu người dùng có đưa văn bản nguồn tham khảo thì đối chiếu mức độ diễn đạt lại (chỉ đổi từ mà không đổi ý, có thêm phân tích riêng không, có đổi cấu trúc và mạch lập luận không).

### Step 5 - Đánh giá rủi ro bản quyền tư liệu (dựa trên mô tả của người dùng)

**Chỉ chạy bước này khi người dùng có mô tả nguồn tư liệu.**

Dựa trên nguồn tư liệu người dùng mô tả, tham chiếu phần "7. Bảng tra nhanh rủi ro nguồn tư liệu" trong `references/copyright-guide.md` (ảnh 7.1 / audio BGM 7.2) để định mức rủi ro, và với tư liệu rủi ro cao thì gợi ý nguồn thay thế từ kho ảnh và kho nhạc miễn phí trong `references/copyright-guide.md`.

### Step 6 - Quét rủi ro thương hiệu và nhãn hiệu

Quét tên thương hiệu, nhãn hiệu, tên sản phẩm xuất hiện trong bài:

1. **Nhắc tên thương hiệu đối thủ** - dìm đối thủ trong nội dung quảng bá là rủi ro cạnh tranh không lành mạnh
2. **Dùng tên thương hiệu khi chưa được phép** - đặt nổi tên thương hiệu của người khác ở tiêu đề/ảnh bìa có thể thành xâm phạm nhãn hiệu
3. **Ám chỉ liên kết sai sự thật** - các cách nói gán ghép chưa được phép như "thương hiệu XX khuyên dùng/hàng giống thương hiệu XX"
4. Liệt kê mọi tên thương hiệu bắt được kèm ngữ cảnh sử dụng, rồi kết luận mức rủi ro

### Step 7 - Tổng hợp báo cáo rủi ro

1. Gom toàn bộ phát hiện từ Step 2-6
2. Chốt mức rủi ro tổng thể (lấy mức cao nhất trong tất cả các chiều)
3. Tách rủi ro thành hai nhóm "bắt buộc xử lý" và "nên xử lý":
   - **Bắt buộc xử lý**: đoạn xào bài rõ rệt, nguồn tư liệu rủi ro cao, dùng thương hiệu khi chưa được phép
   - **Nên xử lý**: thiếu ghi nguồn trích dẫn, phần nguyên bản hơi ít, thiếu nhãn ghi nội dung do AI tạo
4. Với từng mục rủi ro, đưa đề xuất cải thiện cụ thể:
   - Đoạn xào bài → chỉ đúng đoạn và nêu hướng viết lại (bổ sung trải nghiệm cá nhân, đổi góc lập luận)
   - Tư liệu không rõ nguồn → gợi ý nguồn miễn phí thay thế cụ thể
   - Thiếu trích dẫn → chỉ đúng vị trí cần bổ sung trích dẫn
5. Xuất báo cáo rủi ro đầy đủ dạng Markdown

## Nhận biết Profile

**Khi có Profile:**
- Đọc trường `platform`, bật quy tắc bản quyền của nền tảng đó (tham chiếu `references/copyright-guide.md`):
  - Xiaohongshu: yêu cầu gắn nhãn nội dung do AI tạo, cơ chế phát hiện ảnh bê nguyên
  - Douyin: giới hạn bản quyền BGM, chuẩn dùng âm thanh gốc
  - Bilibili: chuẩn ghi nhãn khi đăng lại, yêu cầu trích dẫn tư liệu
  - WeChat OA: quy tắc khai báo bài nguyên bản, cơ chế đăng lại theo whitelist
- Đọc trường `positioning`, xét độ khớp giữa nội dung và định vị kênh (lệch định vị tự nó không phải rủi ro bản quyền, nhưng vẫn nhắc trong báo cáo)
- Đọc phong cách nội dung cũ, xét lần này có hợp phong cách trước không (phong cách đổi đột ngột có thể là dấu hiệu bê bài)

**Khi không có Profile:**
- Kiểm độ nguyên bản và bản quyền ở mức tổng quát, không đặc thù hoá theo nền tảng
- Ghi chú ở cuối báo cáo: "nếu cung cấp Profile của kênh (kèm thông tin nền tảng), có thể bật phần kiểm quy tắc bản quyền riêng của nền tảng"

## Quy tắc

1. **Không bịa chỉ số định lượng** - cấm xuất phần trăm tương đồng, điểm nguyên bản, tỉ lệ khớp; mọi kết luận diễn đạt bằng mức định tính
2. **Không tuyên bố có khả năng check trùng kỹ thuật** - báo cáo không được ám chỉ đã đối chiếu cơ sở dữ liệu, tìm kiếm vector hay so vân tay
3. **Đánh giá tư liệu phải dựa trên mô tả của người dùng** - người dùng không mô tả nguồn thì không đoán, ghi rõ "chưa có nguồn, không đánh giá được"
4. **Phát hiện phải trích nguyên văn** - khi đánh dấu nghi xào bài, bắt buộc trích đúng đoạn văn, không kết luận chung chung
5. **Đề xuất phải làm được ngay** - mỗi đề xuất cải thiện phải nói rõ người dùng làm gì (sửa đoạn nào, đổi tư liệu nào, bổ sung trích dẫn nào)
6. **Trung thực về giới hạn** - ghi chú cuối báo cáo "đánh giá này dựa trên phân tích văn bản của LLM, nếu cần check trùng chính xác hãy dùng công cụ chuyên dụng như Copyleaks, Originality.ai"
7. Cấm dùng dấu gạch ngang dài (em dash)
