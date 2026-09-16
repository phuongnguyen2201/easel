---
name: skill-content-matrix
description: >-
  Lập ma trận đề tài: giao trụ cột nội dung với 8 định dạng bài, mỗi ô là một đề tài cụ thể làm
  được ngay, kèm chấm điểm ưu tiên. Dùng khi người dùng nói "ma trận đề tài", "kho đề tài", "cho
  tôi nhiều đề tài một lúc". Khác skill-topic-evaluator: skill đó chỉ đánh giá một đề tài đơn lẻ.
layer: plan
---

# Sinh ma trận đề tài

> Giao trụ cột nội dung của người dùng với 8 định dạng nội dung để sinh ma trận đề tài, mỗi ô cho ra một tiêu đề đề tài cụ thể, làm được ngay.

## Phân vai với các SKILL hoạch định khác

| SKILL | Trách nhiệm | Ranh giới |
|-------|------|------|
| content-strategy | Định nghĩa lý thuyết trụ cột | SKILL này nhận trụ cột từ đó, không định nghĩa lại |
| content-calendar | Ra lịch đăng theo tháng | Có thể lấy đề tài từ ma trận này để lấp lịch |
| **content-matrix (SKILL này)** | Ra **kho tiêu đề đề tài** (trụ cột × định dạng), chấm điểm hàng loạt để chọn Top | Chỉ ra kho tiêu đề, không xếp lịch |
| topic-evaluator | Đánh giá sâu một đề tài đơn | **Dùng chung một bộ chiều chấm điểm** với SKILL này (xem dưới), matrix chấm hàng loạt, evaluator đánh giá sâu |

## Đầu vào

| Tham số | Bắt buộc | Diễn giải |
|------|------|------|
| Trụ cột nội dung | Có | 3-5 từ khoá hoặc cụm từ trụ cột |
| identity.md | Không | Có hồ sơ thì tự đọc, điền sẵn định vị kênh và hỗ trợ gợi ý trụ cột |
| style.md | Không | Có hồ sơ thì dùng để chỉnh phong cách ngôn ngữ của đề tài |

## Đầu ra

File bảng Markdown `content-matrix-YYYY-MM-DD.md`, cấu trúc như sau:

```
| Trụ cột \ Định dạng | Actionable | Motivational | Analytical | Contrarian | Observation | X vs Y | Present vs Future | Listicle |
|-------------|-----------|-------------|-----------|-----------|------------|--------|------------------|---------|
| Trụ cột A   | tiêu đề cụ thể | tiêu đề cụ thể | ... | ... | ... | ... | ... | ... |
| Trụ cột B   | ...       | ...         | ...       | ...       | ...        | ...    | ...              | ...     |
```

Mỗi ô = một tiêu đề đề tài cụ thể (không phải chủ đề chung chung).

Sau bảng đính kèm: đánh dấu các đề tài mạnh nhất + gợi ý bước tiếp theo.

## Các bước thực thi

1. **Kiểm tra file ngữ cảnh**
   - Kiểm tra có hồ sơ `identity.md` không, có thì đọc và điền sẵn định vị kênh
   - Kiểm tra có hồ sơ `style.md` không, có thì đọc lấy phong cách ngôn ngữ ưa dùng

2. **Lấy trụ cột nội dung**
   - Người dùng đưa thẳng: xác nhận số lượng là 3-5
   - Người dùng chưa đưa nhưng có `identity.md`: dựa trên định vị kênh gợi ý 3-5 trụ cột ứng viên, mời người dùng chốt
   - Người dùng chưa đưa và không có ngữ cảnh: hỏi thẳng người dùng

3. **Nạp định nghĩa định dạng nội dung**
   - Tham chiếu 8 định dạng và quy tắc của chúng trong `references/content-formats.md`

4. **Dựng ma trận**
   - Với mỗi trụ cột x mỗi định dạng, sinh một tiêu đề đề tài cụ thể
   - Tiêu đề phải thể hiện đồng thời đặc trưng lĩnh vực của trụ cột đó và cách diễn đạt của định dạng đó
   - Tiêu đề phải là đề bài cụ thể viết được ngay, không phải chủ đề mơ hồ

5. **Xuất ma trận**
   - Render thành bảng Markdown
   - Lưu thành `outputs/<chủ đề>/content-matrix-YYYY-MM-DD.md`

6. **Chấm điểm đề tài (kho hàng loạt)**
   - Theo **bảy chiều thống nhất + thước đo + trọng số khuyến nghị** trong `../../shared/scoring-dimensions.md`, chấm có trọng số cho từng đề tài trong ma trận (thang 100), quy ra điểm tổng rồi xếp hạng.
   - Dùng chung một bộ chiều và thước đo với topic-evaluator, thống nhất cách hiểu - SKILL này chấm nhanh hàng loạt, evaluator đánh giá sâu từng đề tài.
   - Chọn Top 3-5 đề tài mạnh nhất trong ma trận, nêu lý do khuyến nghị (kèm chi tiết điểm ở các chiều then chốt).
   - Đề tài thuộc **ngách nhạy cảm** thì đánh dấu ⚠️ theo danh sách cảnh báo tuân thủ trong scoring-dimensions.md và kèm khuyến nghị tuân thủ.

7. **Đưa bước tiếp theo**
   - Nhắc người dùng có thể chọn bất kỳ ô nào để triển khai thành bài hoàn chỉnh
   - Ví dụ: "Chọn một mã đề tài bất kỳ, tôi sẽ giúp bạn triển khai thành nội dung hoàn chỉnh"

## Nhận biết Profile

**Khi có Profile:**
- Đọc `platforms.md`, chỉnh phong cách đề tài theo đặc tính nền tảng (ví dụ Xiaohongshu thiên nội dung thực dụng, Douyin thiên kích cảm xúc)
- Đọc `audience.md`, bảo đảm đề tài khớp với khán giả mục tiêu
- Đọc `identity.md`, đề tài xoay quanh định vị kênh
- Đọc `style.md`, chỉnh giọng điệu tiêu đề

**Khi không có Profile:**
- Lui về chế độ chung, đề tài không đặc hoá theo nền tảng
- Ghi chú ở cuối đầu ra: "Nếu cung cấp Profile kênh, có thể sinh đề tài bám nền tảng và khán giả sát hơn"

## Quy tắc

1. Số trụ cột bắt buộc nằm trong khoảng 3-5, thiếu 3 thì yêu cầu bổ sung, quá 5 thì yêu cầu tinh giản
2. Mỗi ô bắt buộc là tiêu đề cụ thể, cấm xuất hiện kiểu mô tả chung chung như "nội dung về XX"
3. Tiêu đề bắt buộc khớp đồng thời trụ cột của hàng và định dạng của cột, không được râu ông nọ cắm cằm bà kia
4. Khi có `style.md`, phong cách ngôn ngữ của tiêu đề bắt buộc nhất quán với nó
5. Cấm dùng gạch ngang dài (em dash)
6. Trong cùng một trụ cột, 8 tiêu đề không được trùng góc tiếp cận
7. Trong ma trận không xuất hiện đề tài trùng hoặc giống nhau quá nhiều
