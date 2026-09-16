---
name: text-polisher
description: >-
  Trau chuốt văn bản: 7 vòng quét tập trung (rõ ràng/giọng/giá trị/bằng chứng/cụ thể/cảm xúc/rủi
  ro) + khử mùi AI (cắt câu đệm, phá cấu trúc công thức, câu chủ động, đổi nhịp), kèm bảng điểm.
  Dùng khi người dùng nói "sửa giúp tôi", "trau chuốt", "nghe AI quá", "cho tự nhiên hơn", "soát
  lỗi".
layer: produce
---

# Trau chuốt văn bản

> Đánh hai đường dao: biên tập có hệ thống để nâng chất lượng + khử mùi AI cho chữ giống người viết.

## Đầu vào

Người dùng đưa vào đoạn nội dung cần biên tập. Thông tin bổ sung tuỳ chọn:
1. **Mục tiêu bài viết** - nhận biết thương hiệu / chuyển đổi / giữ chân
2. **Trọng tâm** - trau chuốt toàn diện / chỉ khử mùi AI / chỉ sửa ngữ pháp và văn phong
3. **Ngôn ngữ** - tiếng Việt / tiếng Anh / song ngữ
4. **Chất liệu bằng chứng** - con số, nhận xét, ca thực tế có thể dùng

## Output

```
=== Bài đã sửa ===
(toàn văn sau khi sửa)

=== Chấm điểm ===
| Tiêu chí | Điểm (1-10) | Diễn giải |
|------|------------|------|
| Độ rõ ràng | X | Có thẳng và dễ hiểu không? |
| Nhịp điệu | X | Câu dài câu ngắn có đổi nhịp không? |
| Độ thật | X | Giống người viết hay giống AI? |
| Mật độ giá trị | X | Còn chỗ nào cắt được nữa không? |
| Khớp giọng | X | Có khớp khán giả mục tiêu và thương hiệu không? |
| Tổng điểm | XX/50 | |

=== Các sửa đổi chính ===
- Điểm sửa 1
- Điểm sửa 2
...
```

**Hai cửa ải (thứ tự cố định, qua cả hai mới giao):**
1. **Tự soát riêng mùi AI (cửa trước)** - văn bản tiếng Trung dùng `references/zh-ai-markers.md` với năm chiều (độ thẳng/nhịp/độ tin cậy/chất người thật/độ tinh gọn), ngưỡng **≥45/50**; chưa qua thì sửa tới khi qua, đừng vội chấm điểm tổng hợp.
2. **Năm chiều trau chuốt chung (cửa chất lượng tổng hợp)** - năm chiều ở bảng trên, ngưỡng **≥35/50**; chưa qua thì sửa tiếp.

Qua cửa mùi AI trước, rồi mới tới cửa tổng hợp - hai cửa cùng thang điểm nhưng gác những chiều khác nhau, đừng trộn lẫn.

## Các bước thực hiện

### Giai đoạn 1: bảy vòng quét tập trung

Mỗi vòng chỉ nhìn một tiêu chí, không sửa dàn trải:

| Vòng | Tiêu chí | Soát cái gì |
|------|------|---------|
| 1 | Độ rõ ràng | Ý chính có nắm được trong 5 giây không? Có câu nào mơ hồ không? |
| 2 | Giọng | Có khớp khán giả mục tiêu không? Có nhất quán với thương hiệu không? |
| 3 | Cảm giác giá trị | Mỗi đoạn có mang giá trị cụ thể không? Thêm được số liệu hoặc ca thực tế không? |
| 4 | Bằng chứng | Luận điểm có gì chống đỡ không? Con số có chuẩn không? |
| 5 | Độ cụ thể | "tiết kiệm thời gian" → "báo cáo tuần rút từ 4 tiếng xuống 15 phút" |
| 6 | Cảm xúc | Có nối được với người đọc không? Có điểm đồng cảm nào không? |
| 7 | Rủi ro | Có chỗ nào gây hiểu lầm, xúc phạm hay rủi ro pháp lý không? |

### Giai đoạn 2: viết lại để khử mùi AI

Nạp danh sách cần xoá → `references/phrases-to-remove.md`
Nạp cấu trúc cần tránh → `references/structures-to-avoid.md`
Văn bản tiếng Trung → `references/zh-ai-markers.md` (từ cấm/dấu câu/cấu trúc câu/chất người thật trong tiếng Trung, kèm phần đặc thù cho nền tảng Xiaohongshu)

**8 quy tắc lõi:**

1. **Chặt câu đệm** - "trước hết/đáng chú ý là/không thể phủ nhận rằng/trong thời đại ngày nay..." xoá hết
2. **Phá cấu trúc công thức** - không dùng lối đối lập nhị nguyên "không phải X, mà là Y"; không dựng bối cảnh tu từ
3. **Câu chủ động** - mỗi câu phải có ai đó đang làm gì. Đừng để vật vô tri thực hiện hành động của con người
4. **Cụ thể hoá** - đừng viết "reasons are structural", hãy nói rõ nguyên nhân cụ thể
5. **Kéo người đọc vào trong** - "bạn" hơn "mọi người", cụ thể hơn trừu tượng
6. **Đổi nhịp** - câu dài câu ngắn xen kẽ. Hai vế hơn ba vế. Không dùng dấu gạch ngang
7. **Tin người đọc** - bỏ phần dạo đầu và biện minh, nói thẳng sự việc
8. **Chặt câu đắt** - câu nào nghe như đang cố tạo trích dẫn thì viết lại

### Giai đoạn 3: tự soát

- [ ] Trạng từ? Xoá
- [ ] Câu bị động? Tìm ra người làm
- [ ] Ba câu liên tiếp dài gần bằng nhau? Ngắt nhịp
- [ ] Mở bài kiểu "here's what/đây là"? Vào thẳng vấn đề
- [ ] Tuyên bố mơ hồ? Nói rõ nghĩa cụ thể
- [ ] Dấu gạch ngang? Xoá

## Quy tắc riêng cho tiếng Trung

Khi xử lý tiếng Trung, quy tắc đầy đủ xem `references/zh-ai-markers.md`. Tra nhanh:

- Xoá cấu trúc thừa kiểu "trong quá trình..."
- "tiến hành/triển khai/thực hiện + danh từ" → dùng thẳng động từ
- "đối với... mà nói" → rút gọn
- "phải thừa nhận rằng/không thể phủ nhận rằng/ai cũng biết rằng" → xoá
- "theo một cách chưa từng có" → nói rõ cách cụ thể

## Nhận biết Profile

- **Có Profile**: đọc style.md để khớp phong cách nhà sáng tạo, không chạy theo cái "giống người" chung chung mà bám thói quen viết của cá nhân đó
- **Không có Profile**: chuyển sang giọng chuyên nghiệp hoặc trò chuyện phổ thông, hướng tới rõ ràng, thẳng thắn, tự nhiên

## Tài liệu tham khảo

- `references/phrases-to-remove.md` - danh sách câu đệm cần xoá
- `references/structures-to-avoid.md` - danh sách cấu trúc công thức cần tránh
- `references/zh-ai-markers.md` - nguồn chuẩn khử mùi AI cho tiếng Trung (từ cấm/dấu câu/cấu trúc câu/chất người thật + phần đặc thù Xiaohongshu)
- `references/checklist.md` - checklist biên tập
- `references/content-refresh.md` - chiến lược làm mới bài cũ
- `references/plain-english-alternatives.md` - bảng từ thay thế gọn hơn
