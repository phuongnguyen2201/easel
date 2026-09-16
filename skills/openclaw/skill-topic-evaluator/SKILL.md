---
name: skill-topic-evaluator
description: >-
  Chấm một đề tài theo 7 tiêu chí (lưu lượng, khớp kênh, khác biệt, thời sự, kiếm tiền, chi phí,
  tuân thủ), chốt làm/bỏ/đổi hướng. Dùng khi người dùng nói "đề tài này nên làm không", "có viral
  không", "đánh giá đề tài". skill-content-matrix sinh hàng loạt, skill-post-scorer chấm bài đã
  làm.
layer: plan
---

# Đánh giá tính khả thi của đề tài

> Người dùng đưa một đề tài, chấm điểm nhiều chiều xem có đáng làm không, xuất khuyến nghị "làm / bỏ / đổi hướng".

> **Chuẩn chấm điểm**: SKILL này và `skill-content-matrix` dùng chung **bộ 7 tiêu chí + thang đo + trọng số** trong `../../shared/scoring-dimensions.md`. matrix chấm nhanh cả rổ đề tài, SKILL này **chấm sâu từng đề tài** (mổ xẻ chi tiết theo từng tiêu chí). Tiêu chí, thang đo và ngưỡng điểm tổng của hai bên hoàn toàn giống nhau.

## Đầu vào

| Tham số | Bắt buộc | Mô tả |
|------|------|------|
| Đề tài | Có | Tiêu đề hoặc mô tả đề tài người dùng muốn làm |
| Nền tảng mục tiêu | Không | Facebook / TikTok / YouTube (Shorts) / Zalo / blog-website (tự lấy khi có Profile) |
| Bối cảnh bổ sung | Không | Nguồn đề tài, cảm hứng, tham khảo đối thủ... |

## Đầu ra

```markdown
# Báo cáo đánh giá đề tài

## Đề tài: {đề tài người dùng đưa ra}
Nền tảng mục tiêu: {platform}
Thời điểm đánh giá: {date}

## Chấm điểm 7 tiêu chí

Chấm theo bộ tiêu chí và thang đo thống nhất trong `../../shared/scoring-dimensions.md`, mỗi tiêu chí kèm căn cứ chi tiết:

| Tiêu chí | Điểm | Diễn giải |
|------|------|------|
| Tiềm năng lưu lượng | X/10 | {mức độ đau + độ nóng của chủ đề trên nền tảng + nhu cầu tìm kiếm} |
| Khớp kênh | X/10 | {độ ăn khớp với định vị, khán giả và hệ thống nội dung} |
| Khác biệt cạnh tranh | X/10 | {độ bão hoà của mảng + có cắt được góc khác biệt không; điểm cao = cạnh tranh thấp} |
| Giá trị thời sự | X/10 | {thường xanh vs trend một lần; điểm cao = thường xanh} |
| Dư địa kiếm tiền | X/10 | {có nhận booking quảng cáo/bán hàng/kéo traffic một cách tự nhiên được không} |
| Chi phí sản xuất | X/10 | {rào cản nguồn lực và kỹ năng; đảo chiều, điểm cao = dễ làm} |
| Rủi ro tuân thủ | X/10 | {mức nhạy cảm; đảo chiều, điểm cao = rủi ro thấp} |

Điểm tổng: XX/100 (quy đổi theo trọng số khuyến nghị trong scoring-dimensions.md)

## Kết luận: {làm / bỏ / đổi hướng}

{một câu tóm tắt lý do của phán quyết}

## Phân tích chi tiết

### Phân tích tiềm năng lưu lượng
{độ nóng tìm kiếm, lượng thảo luận và tình hình bài viral cùng mảng của đề tài này trên nền tảng mục tiêu}

### Khác biệt cạnh tranh
{nhóm top đã chiếm chỗ chưa, dư địa bứt lên của nhóm giữa, điểm cắt khác biệt}

### Giá trị thời sự
{thường xanh hay trend ngắn hạn, thời điểm đăng tốt nhất}

### Đường kiếm tiền
{các dạng hợp tác thương mại có thể nhận, chuỗi kéo traffic và chuyển đổi}

### Tính khả thi khi sản xuất
{tư liệu/thiết bị/kiến thức chuyên môn/thời gian phải bỏ ra}

### Độ hợp với kênh
{mức khớp với hệ thống nội dung của nhà sáng tạo và hồ sơ người theo dõi}

### Rủi ro tuân thủ
{gắn nhãn ⚠️ cho mảng nhạy cảm và khuyến nghị tuân thủ}

## Gợi ý tối ưu (đưa ra khi kết luận là đổi hướng)

1. {gợi ý chỉnh góc tiếp cận}
2. {gợi ý chỉnh hình thức}
3. {gợi ý chỉnh thời điểm}

## Đề tài thay thế (đưa ra khi kết luận là bỏ)

1. {đề tài thay thế A} - {lý do đề xuất}
2. {đề tài thay thế B} - {lý do đề xuất}
```

### Thang chấm điểm

Thang 7 tiêu chí thống nhất (các bậc 1-3 / 4-6 / 7-8 / 9-10) xem `../../shared/scoring-dimensions.md`; SKILL này áp dụng thẳng, không tự đặt chuẩn riêng.

## Các bước thực hiện

1. **Phân tích ý đồ của đề tài**
   - Rút từ khoá cốt lõi và hướng chủ đề từ đề tài người dùng đưa
   - Nhận diện loại đề tài: kiến thức hữu ích, đồng cảm cảm xúc, bắt trend, thể hiện persona, bán hàng/seeding, tranh luận gây tranh cãi
   - Nếu chưa chỉ định nền tảng, suy ra nền tảng hợp nhất theo loại đề tài, hoặc hỏi người dùng

2. **Đánh giá sâu từng tiêu chí**

   Triển khai lần lượt 7 tiêu chí theo `../../shared/scoring-dimensions.md`, mỗi tiêu chí cho điểm kèm căn cứ cụ thể:
   - **Tiềm năng lưu lượng** - độ nóng của chủ đề trên nền tảng, nhu cầu tìm kiếm, thành tích lịch sử của mảng, khả năng lan truyền, thiên hướng thuật toán
   - **Khớp kênh** - so với định vị/persona/mảng nội dung, nối tiếp nội dung đã có, sở thích trong hồ sơ người theo dõi, ảnh hưởng tới tăng trưởng dài hạn
   - **Khác biệt cạnh tranh** - độ bão hoà của mảng, nhóm top đã chiếm chỗ chưa, dư địa bứt lên của nhóm giữa, góc mới có thể cắt vào
   - **Giá trị thời sự** - thường xanh vs thời vụ; thường xanh thì xét giá trị tìm kiếm dài hạn, thời vụ thì xét tốc độ nguội và thời điểm đăng tốt nhất
   - **Dư địa kiếm tiền** - giá trị thương mại (thương hiệu/bán hàng/khoá học trả phí/kéo traffic), mức sẵn sàng chi tiền của khán giả, đường kiếm tiền có tự nhiên không
   - **Chi phí sản xuất** (đảo chiều) - tư liệu/thiết bị/kiến thức chuyên môn/thời gian cần có, năng lực hiện tại của nhà sáng tạo có kham nổi không
   - **Rủi ro tuân thủ** (đảo chiều) - gắn nhãn ⚠️ cho mảng nhạy cảm và khuyến nghị tuân thủ

3. **Phán quyết tổng hợp và xuất báo cáo**
   - Tính điểm tổng theo trọng số khuyến nghị trong scoring-dimensions.md (thang 100)
   - Kết luận theo ngưỡng thống nhất:
     - **>= 70**: làm, lên lịch đăng ngay
     - **50-69**: đổi hướng, chỉnh xong đánh giá lại (kèm ít nhất 2 gợi ý tối ưu)
     - **< 50**: bỏ, kèm ít nhất 2 đề tài thay thế
   - Xuất báo cáo đánh giá đầy đủ

## Nhận biết Profile

**Khi có Profile:**
- Đọc `identity.md` để lấy định vị mảng nội dung, đánh giá chính xác mức khớp kênh
- Đọc `audience.md` để lấy hồ sơ người theo dõi, đánh giá mức khớp về sở thích của khán giả
- Đọc `platforms.md` để lấy các nền tảng đang hoạt động, đánh giá tiềm năng lưu lượng theo từng nền tảng
- Đọc `style.md` để xét độ tương thích giữa đề tài và phong cách nội dung
- Lấy thông tin kiếm tiền từ `identity.md`/`preferences.md`, đánh giá tính khả thi của đường kiếm tiền

**Khi không có Profile:**
- Chấm 7 tiêu chí theo chuẩn chung, không đánh giá chi tiết mức khớp kênh
- Ở tiêu chí khớp kênh, nhắc "cung cấp Profile để có đánh giá độ khớp chính xác hơn"
- Tiềm năng lưu lượng dựa trên dữ liệu chung của nền tảng thay vì thành tích lịch sử của kênh

## Quy tắc

1. Chấm điểm phải dựa trên phân tích cụ thể, cấm chấm theo cảm tính
2. Phần diễn giải của mỗi tiêu chí phải có căn cứ cụ thể, không được nói chung chung
3. Kết luận "đổi hướng" bắt buộc kèm ít nhất 2 gợi ý tối ưu
4. Kết luận "bỏ" bắt buộc kèm ít nhất 2 đề tài thay thế
5. Đánh giá phải tính tới năng lực thực tế của nhà sáng tạo, không đề xuất đề tài vượt quá khả năng
6. Đề tài dính mảng nhạy cảm (thẩm mỹ, tài chính, mẹ và bé, sức khoẻ) phải gắn nhãn rủi ro tuân thủ

> Nguồn gốc tự phát triển và hướng tham khảo xem `EASEL-META.md` cùng thư mục.
