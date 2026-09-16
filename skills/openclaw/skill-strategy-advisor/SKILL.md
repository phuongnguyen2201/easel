---
name: skill-strategy-advisor
description: >-
  Đề xuất điều chỉnh chiến lược giai đoạn tới từ hiệu quả nội dung, hồ sơ (Profile), xu hướng
  ngành: hướng nội dung, ngách mới, hình thức, nhịp đăng, chỉnh hồ sơ. Dùng khi người dùng nói
  "bước tiếp theo làm gì", "điều chỉnh thế nào", "chiến lược tháng sau". skill-content-strategy
  lập từ đầu.
layer: attribute
---

# Gợi ý điều chỉnh chiến lược

> Dựa trên dữ liệu nội dung hiện có và hồ sơ (Profile), đưa ra gợi ý tối ưu chiến lược nội dung cho giai đoạn tiếp theo.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Tóm tắt dữ liệu nội dung | Có | Dữ liệu hiệu quả nội dung của giai đoạn vừa qua (ít nhất có tiêu đề, nền tảng, chỉ số cốt lõi), hoặc báo cáo hậu kiểm |
| Khoảng thời gian | Nên có | Giai đoạn mà dữ liệu bao phủ (ví dụ "30 ngày gần nhất", "tháng 6") |
| Mô tả chiến lược hiện tại | Nên có | Hướng nội dung, ngách, nhịp đăng, hình thức chính đang chạy |
| Thay đổi mục tiêu | Tuỳ chọn | Mục tiêu gần đây có đổi không (ví dụ từ tăng người theo dõi chuyển sang kiếm tiền, từ một nền tảng sang đa nền tảng) |
| Thông tin ngành/ngách | Tuỳ chọn | Biến động gần đây của ngành, động thái đối thủ |
| Báo cáo hậu kiểm | Tuỳ chọn | Nếu đã chạy skill-content-postmortem, có thể trích thẳng đầu ra của nó |

Nếu người dùng chỉ đưa mô tả mơ hồ (ví dụ "dạo này số liệu không tốt lắm"), hãy dẫn dắt họ bổ sung dữ liệu cụ thể, nhưng đừng chặn quy trình. Dựa trên thông tin sẵn có mà đưa gợi ý, kèm ghi chú mức độ tin cậy.

## Đầu ra

```markdown
# Gợi ý điều chỉnh chiến lược: [kênh/chủ đề] - [giai đoạn]

## Chẩn đoán hiện trạng

### Tổng quan số liệu
| Chỉ số | Giá trị hiện tại | Xu hướng (↑↓→) | Độ khoẻ |
|------|--------|-------------|--------|
| Tần suất đăng | | | |
| Lượt đọc/xem trung bình | | | |
| Tỉ lệ tương tác trung bình | | | |
| Tăng trưởng người theo dõi | | | |
| Tỉ lệ viral | | | |

### Nhận diện vấn đề cốt lõi
- Vấn đề 1: [vấn đề cụ thể + dữ liệu chứng minh]
- Vấn đề 2: ...
- Tín hiệu tích cực: [những mặt làm tốt, không được chỉ nói vấn đề]

## Gợi ý chiến lược (xếp theo mức ưu tiên)

### 1. [tiêu đề gợi ý ưu tiên cao nhất]
- **Hiện trạng**: đang làm thế nào
- **Vấn đề**: dữ liệu nói lên điều gì
- **Gợi ý**: chỉnh cụ thể ra sao
- **Hiệu quả kỳ vọng**: thay đổi dự kiến sau khi chỉnh
- **Điểm then chốt khi thực thi**: lưu ý lúc triển khai

### 2. [tiêu đề gợi ý ưu tiên kế tiếp]
...

(tổng cộng 3-5 gợi ý)

## Điều chỉnh hướng nội dung

### Hướng giữ nguyên
- [hướng đang chạy tốt + lý do]

### Hướng cần đẩy mạnh
- [hướng có tiềm năng nhưng đầu tư chưa đủ + căn cứ]

### Hướng giảm bớt hoặc bỏ
- [hướng hiệu quả kém hoặc ROI thấp + phương án thay thế]

### Gợi ý thăm dò ngách mới
- [hướng mới gợi ý từ dữ liệu và xu hướng + phương án thử nước]

## Tối ưu hình thức nội dung
- Gợi ý định dạng (bài ảnh-chữ / video / livestream / kết hợp)
- Gợi ý độ dài
- Gợi ý nhịp đăng (tần suất + khung giờ tốt nhất)

## Gợi ý tinh chỉnh hồ sơ (khi có Profile)
- Mô tả định vị có cần cập nhật không
- Khán giả mục tiêu có cần chỉnh không
- Phong cách nội dung có cần đổi mới không
- Gợi ý sửa cụ thể (đưa đối chiếu trước và sau khi sửa)

## Danh sách hành động tiếp theo
1. Làm ngay tuần này: [1-2 hành động]
2. Hoàn tất trong hai tuần: [2-3 điều chỉnh]
3. Theo dõi liên tục: [chỉ số cần bám để kiểm chứng]

## Giới hạn dữ liệu và giả định
- Thuyết minh phạm vi và chất lượng dữ liệu dùng để phân tích
- Giả định then chốt (ví dụ thuật toán nền tảng không thay đổi lớn)
```

## Các bước thực hiện

1. **Nạp và làm sạch dữ liệu**
   - Nhận dữ liệu nội dung người dùng đưa (CSV, ảnh chụp màn hình, mô tả bằng chữ, báo cáo hậu kiểm đều được)
   - Chuẩn hoá về một định dạng thống nhất: tiêu đề nội dung, nền tảng, thời gian đăng, chỉ số cốt lõi
   - Nếu đã trích đầu ra của skill-content-postmortem thì dùng lại luôn kết luận phân tích của nó

2. **Chẩn đoán hiện trạng**
   - Tính giá trị trung bình, xu hướng, biên độ dao động của các chỉ số cốt lõi
   - Nhận diện điểm bất thường (tăng vọt, tụt mạnh)
   - Đối chiếu references/platform-benchmarks.md để đánh giá độ khoẻ của kênh
   - Đánh dấu tín hiệu tích cực và tín hiệu có vấn đề

3. **Phân tích quy nguyên**
   - Phân tích chéo: tổ hợp hướng nội dung x hình thức nội dung nào chạy tốt nhất/tệ nhất
   - Chiều thời gian: xu hướng đang tốt lên hay xấu đi
   - Yếu tố bên ngoài: có chịu ảnh hưởng từ thay đổi quy tắc nền tảng, trend ngành, yếu tố mùa vụ không

4. **Quét xu hướng và cơ hội**
   - Dựa trên thông tin ngách, nhận định thay đổi xu hướng nội dung của ngành
   - Nhận diện hướng tăng trưởng tiềm năng trong dữ liệu người dùng (tín hiệu đã nhú nhưng chưa được khuếch đại)
   - Kết hợp hướng ưu tiên phân phối mới nhất của nền tảng (ví dụ nền tảng đang đẩy định dạng nào)

5. **Sinh chiến lược**
   - Sinh 3-5 gợi ý chiến lược, mỗi gợi ý gồm: hiện trạng, vấn đề, gợi ý, hiệu quả kỳ vọng, điểm then chốt khi thực thi
   - Xếp theo mức tác động kỳ vọng (tác động cao + dễ thực thi được ưu tiên)
   - Bảo đảm gợi ý cụ thể, làm được ngay, không viết câu sáo rỗng kiểu "nâng cao chất lượng nội dung"

6. **Ma trận điều chỉnh hướng**
   - Chia các hướng nội dung hiện có thành bốn ô: giữ / đẩy mạnh / giảm / thêm mới
   - Mỗi điều chỉnh hướng đều phải có dữ liệu chống lưng
   - Gợi ý ngách mới phải kèm phương án thử nước chi phí thấp (ví dụ "đăng trước 3 bài để đo phản hồi")

7. **Tinh chỉnh hồ sơ (khi có Profile)**
   - Đối chiếu hiệu quả dữ liệu với mô tả định vị trong Profile
   - Nếu dữ liệu cho thấy khán giả/phong cách/hướng lệch với Profile, hãy đưa gợi ý tinh chỉnh
   - Đưa đối chiếu trước và sau khi sửa, chứ không chỉ nói "cần điều chỉnh"

8. **Xuất và bàn giao**
   - Sinh báo cáo đầy đủ theo mẫu đầu ra
   - Sinh danh sách hành động (tuần này / trong hai tuần / theo dõi liên tục)
   - Lưu vào `outputs/<chủ đề>/`

## Nhận biết Profile

**Khi có Profile:**
- Đọc identity.md (định vị ngách), platforms.md (nền tảng đang tập trung), audience.md (hồ sơ khán giả), preferences.md (thiên hướng kiếm tiền/thương mại hoá)
- Gợi ý chiến lược bám mục tiêu dài hạn trong Profile (không vì số liệu ngắn hạn mà khuyên chệch khỏi định vị kênh)
- Tinh chỉnh hồ sơ: khi hiệu quả dữ liệu lệch với định nghĩa trong Profile thì chỉ rõ và đưa gợi ý sửa
- Gợi ý theo giai đoạn: giai đoạn xây kênh nghiêng về "tìm hướng hiệu quả", giai đoạn tăng trưởng nghiêng về "khuếch đại lợi thế", giai đoạn kiếm tiền nghiêng về "hiệu suất chuyển đổi"

**Khi không có Profile:**
- Lui về chế độ chung, chẩn đoán và gợi ý dựa trên chính dữ liệu
- Không phán "có chệch định vị hay không" (vì chưa biết định vị là gì)
- Không xuất phần tinh chỉnh hồ sơ
- Khuyên người dùng tạo Profile để có gợi ý chiến lược chính xác hơn

> Nguồn gốc tự phát triển và các dự án tham khảo xem `EASEL-META.md` trong cùng thư mục.
