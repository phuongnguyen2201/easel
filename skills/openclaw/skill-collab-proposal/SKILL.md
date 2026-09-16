---
name: skill-collab-proposal
description: >-
  Soạn đề xuất hợp tác hai chế độ: booking quảng cáo (thương hiệu tìm đến: báo giá theo bảng giá
  KOL, hình thức nội dung, lịch, KPI dự kiến) và collab với nhà sáng tạo/thương hiệu (chia việc,
  quảng bá chéo). Dùng khi người dùng nói "báo giá booking", "nhãn hàng hỏi hợp tác", "làm
  collab".
layer: plan
---

# Sinh phương án booking quảng cáo / collab

> Theo nhu cầu hợp tác, tra bảng giá KOL để tính khoảng báo giá, dùng công thức hệ số nền tảng để ước lượng KPI, xuất đề xuất có cấu trúc gửi thẳng được cho nhãn hàng hoặc đối tác.

## Đầu vào

| Tham số | Bắt buộc | Mô tả |
|------|------|------|
| Thông tin đối tác | Có | Tên thương hiệu/tên đối tác, mô tả sản phẩm hoặc dịch vụ |
| Chế độ hợp tác | Không | Chỉ định rõ A (booking quảng cáo) hoặc B (collab), không chỉ định thì tự nhận diện |
| Khoảng ngân sách | Không | Trần ngân sách của nhãn hàng, dùng để suy ngược ra hình thức nội dung |
| Tài liệu bổ sung | Không | Brief thương hiệu, case của đối thủ, dữ liệu hợp tác trước đây |

**Quy tắc tự nhận diện:** có "báo giá" "booking quảng cáo" "cài cắm thương hiệu" "nhận quảng cáo" thì đi chế độ A; có "collab" "phối hợp" "hợp tác nhà sáng tạo" "quảng bá chéo" thì đi chế độ B.

## Đầu ra

Tài liệu phương án dạng Markdown, lưu vào `outputs/<chủ đề>/collab-proposal.md`. Mẫu cấu trúc đầu ra đầy đủ của hai chế độ xem `references/proposal-templates.md`:
- **Chế độ A (booking quảng cáo)**: tổng quan kênh / hình thức hợp tác và báo giá / ý tưởng nội dung / KPI dự kiến / lịch / đề xuất điều khoản
- **Chế độ B (collab)**: so tổng quan hai bên / khán giả bổ trợ nhau / phương án nội dung chung / chiến lược quảng bá chéo / lịch triển khai / hiệu quả kỳ vọng

## Các bước thực hiện

### 1. Đọc ý định và trích thông tin
- Đọc đầu vào để quyết định đi chế độ A (booking quảng cáo) hay chế độ B (collab)
- Trích thông tin then chốt: tên thương hiệu/đối tác, hướng sản phẩm, nhu cầu hợp tác, ngân sách
- **Thiếu thông tin then chốt thì chủ động hỏi lại**, không bịa tên thương hiệu hay thông tin sản phẩm

### 2. Đọc dữ liệu Profile
- `identity.md`: tên kênh, số người theo dõi, ngách nội dung, kinh nghiệm booking quảng cáo trước đây
- `platforms.md`: số người theo dõi từng nền tảng, tỉ lệ tương tác 30 ngày gần nhất, nền tảng chủ lực
- `audience.md`: hồ sơ khán giả (tuổi, giới tính, khu vực, sức chi tiêu)
- Không có Profile thì để placeholder, nhắc người dùng bổ sung (xem mục "Nhận biết Profile")

### 3. Xác định cấp KOL
Theo số người theo dõi trong `identity.md`, tra bảng cấp ở mục 1 của `references/kol-pricing-guide.md` (người thường / KOC / tầm trung / top đầu / siêu sao). Các bước sau đều dựa trên cấp này.

### 4. Tính khoảng báo giá (chế độ A)
1. Tra mục 2 của `references/kol-pricing-guide.md`, lấy **khoảng báo giá gốc** theo cấp + nền tảng + hình thức nội dung (số liệu CNY, chuẩn thị trường Trung Quốc)
2. Theo **hệ số điều chỉnh** ở mục 3 (độ khớp ngách/tính thời điểm dịp lễ/độc quyền/tái sáng tạo/đa nền tảng...) cộng dồn phần cộng thêm
3. Tính: báo giá sau điều chỉnh = báo giá gốc x (1 + tổng các phần cộng thêm)
4. Dùng **công thức CPE** ở mục 4 để kiểm ngược tính hợp lý, vượt khoảng hợp lý thì gắn cảnh báo

### 5. Ước lượng KPI
Tính theo từng tầng bằng công thức ở mục 5 của `references/kol-pricing-guide.md`, mỗi con số ghi kèm cách tính:
1. **Lượt hiển thị dự kiến** = số người theo dõi x hệ số hiển thị nền tảng x hệ số loại nội dung (tra hệ số ở mục 5.1)
2. **Lượt tương tác dự kiến** = lượt hiển thị dự kiến x tỉ lệ tương tác mốc của nền tảng (tra mục 5.2)
3. **Chuyển đổi dự kiến** = lượt tương tác dự kiến x tỉ lệ chuyển đổi nội dung (tra mục 5.3; loại chỉ chạy hiển thị mà không có đường dẫn chuyển đổi thì đừng ép ước, ghi "chủ yếu lấy hiển thị")
4. Xuất **khoảng** (mức thận trọng/mức lạc quan), không đưa một con số duy nhất

### 6. Thiết kế phương án nội dung
- Gợi ý 2-3 hình thức nội dung, mỗi hình thức ghi rõ: dạng (ảnh-chữ/video ngắn/video dài/livestream/kết hợp), thời lượng hoặc độ dài, hướng sáng tạo và cách cài cắm (cài mềm/quảng cáo trực diện/video nói/cài vào bối cảnh), tóm tắt kịch bản (3-5 câu)
- Xếp thứ tự ưu tiên gợi ý theo sở thích khán giả trong `audience.md`

### 7. Lên lịch
- Chu kỳ sản xuất: chốt kịch bản → quay/dựng → nhãn hàng duyệt → đăng
- Thời điểm đăng nên chọn: tránh lúc đối thủ dồn dập, khớp dịp lễ/trend
- Ghi rõ thời gian chừa cho khâu duyệt (thường 3-5 ngày làm việc)

### 8. Các bước bổ sung khi lập kế hoạch collab (chế độ B)
- So dữ liệu hai kênh (người theo dõi/tỉ lệ tương tác/hồ sơ khán giả), trình bày bằng bảng
- Ước mức trùng khán giả: cùng nền tảng cùng ngách thì trùng cao (40-60%), khác nền tảng hoặc khác ngách thì trùng thấp (10-25%)
- Thiết kế ma trận chia việc nội dung: ai lên hình/ai dựng/đăng đầu ở kênh nào/kịch bản tương tác dưới bình luận
- Ước lượng KPI riêng cho từng bên (dùng lại công thức ở bước 5)

### 9. Lưu kết quả
- Lưu vào `outputs/<chủ đề>/collab-proposal.md`
- Đầu file ghi thời điểm tạo, chế độ áp dụng, nguồn dữ liệu

## Nhận biết Profile

### Khi có Profile
- Đọc từ `identity.md`: tên kênh, số người theo dõi, định vị ngách, kinh nghiệm booking quảng cáo trước đây
- Đọc từ `platforms.md`: số người theo dõi và tỉ lệ tương tác từng nền tảng, xác định nền tảng chủ lực
- Đọc từ `audience.md`: tuổi/giới tính/khu vực/sức chi tiêu của khán giả, dùng để khớp hướng nội dung
- Báo giá tính bằng cách tra bảng theo số người theo dõi thực, KPI suy ra từ công thức dựa trên tỉ lệ tương tác thực
- Hình thức nội dung gợi ý phải khớp thể loại mà kênh làm tốt

### Khi không có Profile
- Tổng quan kênh để placeholder `[bổ sung: nền tảng/số người theo dõi/tỉ lệ tương tác]`
- Báo giá đưa khoảng chung cho mọi cấp ở hình thức nội dung đó, ghi "chỉ để tham khảo, cần chỉnh theo dữ liệu thực"
- KPI dự kiến dùng trung vị ngành, ghi "dựa trên mức trung bình ngành, thực tế có thể lệch khá nhiều"
- Cuối bài ghi chú: "Nếu cung cấp Profile của kênh (gồm identity.md / platforms.md / audience.md), có thể sinh báo giá và KPI dự kiến chính xác hơn"

## Quy tắc

1. **Báo giá phải truy được nguồn** - mỗi con số báo giá phải lần về được bảng cấp + hệ số điều chỉnh trong `references/kol-pricing-guide.md`, cấm bịa ra
2. **KPI phải ghi công thức** - mỗi giá trị dự kiến ghi kèm cách tính (ví dụ "100 nghìn người theo dõi x hệ số 0.3 = 30 nghìn lượt hiển thị")
3. **Khoảng tốt hơn một số** - báo giá và KPI đều đưa khoảng từ mức thận trọng tới mức lạc quan
4. **Thiếu thông tin thì hỏi, không bịa** - thiếu tên thương hiệu, thông tin sản phẩm, ngân sách thì bắt buộc hỏi lại
5. **Bắt buộc kiểm CPE** - tính xong báo giá phải dùng công thức CPE kiểm ngược, thấy vô lý thì gắn cảnh báo
6. **Ít nhất 2 hình thức nội dung** - mỗi hình thức ghi rõ ưu nhược
7. **Ước chuyển đổi phải thận trọng** - hợp tác không có đường dẫn chuyển đổi trực tiếp thì đừng ép ước tỉ lệ chuyển đổi
8. **Cấm dùng dấu gạch ngang dài (em dash)**
