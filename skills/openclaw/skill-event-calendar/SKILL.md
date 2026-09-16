---
name: skill-event-calendar
description: >-
  Tra N ngày tới có ngày lễ, kỷ niệm, mốc sale, sự kiện ngành, thể thao (Tết, 11.11) để bắt điểm
  rơi nội dung, kèm điểm bắt trend. Dùng khi người dùng nói "sắp tới có lễ gì", "tháng sau bắt
  trend gì", "lịch marketing", "khi nào có sale". Đầu vào cho skill-content-calendar (xếp lịch
  đăng).
layer: discover
---

# Lịch ngày lễ / mốc sự kiện

> Tra ngày lễ, ngày kỷ niệm, mốc sale thương mại điện tử, sự kiện ngành trong N ngày tới, cho nhà sáng tạo điểm bắt trend và cửa sổ thời gian chuẩn bị trước.

## Đầu vào

| Tham số | Bắt buộc | Mô tả |
|------|------|------|
| Khoảng thời gian | Không | N ngày tới (mặc định 30 ngày) |
| Ngách/lĩnh vực | Không | Lọc các mốc liên quan tới một ngách cụ thể (có Profile thì tự trích) |
| Loại mốc | Không | Lọc theo loại: ngày lễ/thương mại điện tử/ngành/thi cử/thể thao (mặc định lấy tất cả) |

## Đầu ra

```markdown
# Lịch mốc nội dung

Khoảng thời gian: {start_date} - {end_date}
Lọc theo ngách: {ngách hoặc "tất cả"}
Thời điểm tạo: {date}

## Mốc trọng điểm sắp tới (trong 7 ngày)

| Ngày | Tên mốc | Loại | Giá trị bắt trend | Số ngày chuẩn bị trước | Ngách gợi ý |
|------|---------|------|---------|------------|---------|
| {date} | {name} | {type} | ★★★★★ | {N ngày} | {ngách} |

## Tổng quan mốc trong 30 ngày tới

### {tháng}

| Ngày | Tên mốc | Loại | Giá trị bắt trend | Hướng nội dung gợi ý |
|------|---------|------|---------|------------|
| {date} | {name} | {type} | ★★★★☆ | {gợi ý một câu} |

## Giải thích chi tiết các mốc giá trị cao (Top 3-5)

### {tên mốc} ({ngày})
- Loại: {ngày lễ/thương mại điện tử/ngành/thi cử/thể thao}
- Giá trị bắt trend: ★★★★★
- Chuẩn bị trước: {nên bắt đầu chuẩn bị trước X ngày}
- Hướng nội dung:
  1. {hướng A}: {mô tả một câu}
  2. {hướng B}: {mô tả một câu}
  3. {hướng C}: {mô tả một câu}
- Hợp ngách: {nhà sáng tạo ở ngách nào hợp để bắt}
- Nhắc tránh hố: {điều cần lưu ý}
- Tham chiếu bài viral năm ngoái: {loại nội dung hot ở cùng mốc năm ngoái}

## Gợi ý nhịp nội dung tháng này

{dựa trên mật độ mốc và phân bố loại, đưa gợi ý nhịp nội dung cho tháng này}
```

## Các bước thực hiện

1. **Phân tích khoảng thời gian**
   - Mặc định tra 30 ngày tới
   - Người dùng chỉ định khoảng nào thì tra theo khoảng đó
   - Tính ngày đầu ngày cuối, xác định các tháng phải phủ

2. **Nạp dữ liệu mốc**
   - Đọc [events-china.md](references/events-china.md) để lấy dữ liệu ngày lễ cả năm và mốc sale của Trung Quốc (kho này theo lịch Trung Quốc)
   - Theo khoảng thời gian, lọc ra mọi mốc rơi vào khoảng đó
   - Bổ sung sự kiện đặc biệt của năm (như Olympic, World Cup, những sự kiện không cố định)
   - **Ngày dương lịch của các ngày lễ âm lịch đều quy đổi bằng `scripts/lunar.py`, không ước lượng**:
     - Tra ngày lễ: `python3 skills/openclaw/skill-event-calendar/scripts/lunar.py festival "Trung thu" 2026` (nhận tên tiếng Việt, không phân biệt dấu/hoa thường)
     - Quy đổi tổng quát: `python3 skills/openclaw/skill-event-calendar/scripts/lunar.py l2s 2026 8 15`
     - Danh sách ngày lễ hỗ trợ xem `python3 skills/openclaw/skill-event-calendar/scripts/lunar.py festival --list` (Tết Nguyên đán/Nguyên tiêu/Đoan ngọ/Thất tịch/Trung thu/Trùng cửu/Lạp bát - lễ Trung Quốc/Tết ông Táo/Giao thừa...)

3. **Khớp liên quan với ngách**
   - Nếu có thông tin ngách (người dùng chỉ định hoặc trích từ Profile), đánh giá độ liên quan của từng mốc
   - Ghi rõ mỗi mốc hợp với nhà sáng tạo ở ngách nào
   - Độ liên quan với ngách ảnh hưởng tới điểm "giá trị bắt trend"

4. **Đánh giá giá trị bắt trend**
   - Chấm điểm từng mốc theo các chiều sau (1-5 sao):
     - Độ quan tâm toàn dân: có phải cả nước cùng tham gia không (Tết Nguyên đán 5 sao, Ngày Sách thế giới 2 sao)
     - Không gian sáng tạo nội dung: làm ra được bao nhiêu nội dung khác biệt
     - Giá trị thương mại: nhãn hàng có nhu cầu chạy quảng cáo không
     - Độ bền thời gian: chủ đề còn hot trong bao lâu
     - Độ liên quan với ngách (khi có thông tin ngách)

   ### Thang chấm giá trị bắt trend

   | Số sao | Tiêu chuẩn |
   |------|------|
   | ⭐ | Mốc mờ nhạt, chỉ nhóm nhỏ quan tâm, không gian sáng tạo hạn chế |
   | ⭐⭐ | Có mức quan tâm nhất định, nhưng góc nội dung bị bó hoặc cạnh tranh quá gắt |
   | ⭐⭐⭐ | Mức quan tâm toàn dân trung bình, có 2-3 góc nội dung rõ ràng để vào |
   | ⭐⭐⭐⭐ | Quan tâm cao, nhiều góc để vào, lại liên quan tới nhiều ngách dọc |
   | ⭐⭐⭐⭐⭐ | Mốc cấp toàn dân (như Tết Nguyên đán/11.11/12.12), không gian sáng tạo cực lớn, giá trị thương mại cao |

5. **Gợi ý hướng nội dung**
   - Với mốc giá trị cao (4-5 sao), sinh 3 hướng nội dung cụ thể
   - Hướng nội dung phải cân nhắc: đặc tính nền tảng, dạng bài viral các năm trước, định vị của nhà sáng tạo
   - Ghi rõ số ngày chuẩn bị trước:
     - Video ngắn/livestream: trước 3-5 ngày
     - Nội dung ảnh-chữ: trước 1-3 ngày
     - Kế hoạch theo series: trước 7-14 ngày

6. **Gợi ý hoạch định nhịp**
   - Phân tích mật độ mốc trong khoảng thời gian
   - Nhận ra giai đoạn dày mốc và giai đoạn trống
   - Gợi ý nhịp nội dung: giai đoạn dày thì dồn vào mốc giá trị cao, giai đoạn trống thì bù nội dung thường xanh
   - Nhắc xung đột thời gian: cùng một ngày có nhiều mốc thì gợi ý chọn bỏ

7. **Giao đầu ra**
   - Sinh lịch hoàn chỉnh theo định dạng đầu ra
   - Mốc trong 7 ngày tới làm nổi bật riêng, nhắc mức gấp
   - Mốc giá trị cao thì phân tích chi tiết

8. **Lưu vào lịch nội dung (tuỳ chọn)**
   - Khi người dùng muốn lưu các mốc đã tra vào lịch để theo dõi lâu dài, gom các mốc thành mảng JSON (`title`/`date`/tuỳ chọn `event_type`/`end_date`/`platform`) rồi giao `skill-content-calendar-log` nhập hàng loạt (trùng tên trùng ngày thì tự khử trùng lặp, chạy lại không đổi kết quả):

   ```bash
   python skills/shared/scripts/calendar_ops.py import-events --file events.json
   ```

## Nhận biết Profile

**Khi có Profile:**
- Đọc `identity.md` lấy ngách, tự lọc các mốc liên quan cao
- Đọc `platforms.md` lấy nền tảng đang hoạt động, chỉnh dạng thức của gợi ý hướng nội dung
- Đọc `audience.md` lấy hồ sơ khán giả, đánh giá mức quan tâm của khán giả với từng mốc
- Trích sở thích thương mại hoá từ `identity.md`/`preferences.md`, đánh giá mốc nào có cơ hội hợp tác thương mại

**Khi không có Profile:**
- Hiện toàn bộ mốc, không lọc theo ngách
- Giá trị bắt trend chấm theo độ quan tâm toàn dân, không có chiều khớp ngách
- Hướng nội dung đưa gợi ý phổ thông
- Ghi chú "cung cấp Profile hoặc chỉ định ngách sẽ lọc mốc chính xác hơn"

## Quy tắc

1. Dữ liệu mốc phải chính xác, ngày không được sai (tham chiếu references/events-china.md, kho theo lịch Trung Quốc)
2. Ngày dương lịch của ngày lễ âm lịch đều gọi `scripts/lunar.py` để quy đổi, cấm dựa vào trí nhớ hay ước lượng (script phủ 1900-2100, đã tự kiểm bằng mốc neo)
3. Thời điểm các đợt sale lớn của sàn lấy theo công bố chính thức của năm đó, chưa công bố thì dùng thông lệ các năm trước
4. Điểm giá trị bắt trend phải có căn cứ, không chấm theo cảm tính
5. Số ngày chuẩn bị trước phải thực tế, tính tới chu kỳ sản xuất thật
6. Khi đụng ngày kỷ niệm mang tính chính trị, chỉ gợi ý hướng nội dung tích cực
7. Dữ liệu ngày lễ mỗi năm cần cập nhật lại phần quy đổi âm lịch và các mốc sale mới

> Nguồn gốc tự phát triển, phả hệ thuật toán quy đổi âm lịch và dự án mã nguồn mở tham khảo xem `EASEL-META.md` cùng thư mục.
