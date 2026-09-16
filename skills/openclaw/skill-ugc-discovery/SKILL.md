---
name: skill-ugc-discovery
description: >-
  Tìm nội dung do người dùng tạo (UGC) về thương hiệu/kênh: bài của fan, review, nhắc tên, thảo
  luận cộng đồng; xuất danh sách UGC giá trị kèm link nguồn, phản hồi tiêu cực và gợi ý tương tác.
  Dùng khi người dùng nói "ai nhắc tới tôi", "tìm UGC", "fan đăng gì về tôi", "khách nói gì về
  mình".
layer: discover
---

# Phát hiện nội dung UGC

> Tìm nội dung do người dùng tạo liên quan tới thương hiệu/kênh của nhà sáng tạo, phát hiện bài của người theo dõi, review, nhắc tên và thảo luận cộng đồng, xuất ra danh sách UGC có thể tương tác.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| brand_keywords | có | Tên thương hiệu/tên kênh, có thể nhiều (phân tách bằng dấu phẩy) |
| platforms | không | Nền tảng tập trung (Xiaohongshu/Bilibili/Weibo/Zhihu/Douyin), mặc định toàn nền tảng |
| content_type | không | reviews / mentions / fan_art / complaints / all (mặc định all) |
| time_range | không | recent / this_month / this_quarter (mặc định recent) |

## Đầu ra

```markdown
# Báo cáo phát hiện nội dung UGC

## Tổng quan phát hiện
- Từ khoá tìm kiếm: {keywords}
- Nền tảng tìm kiếm: {platforms}
- Nội dung UGC tìm được: {count} mục
- Tích cực/trung tính/tiêu cực: {positive}/{neutral}/{negative}

## UGC giá trị cao (nên tương tác/chia sẻ)
| # | Nền tảng | Tóm tắt nội dung | Link nguồn | Ước lượng tương tác | Cảm xúc | Hành động đề xuất |
|---|------|---------|---------|-----------|------|---------|

## Phản hồi tiêu cực (cần lưu ý)
| # | Nền tảng | Tóm tắt nội dung | Link nguồn | Mức nghiêm trọng | Phản hồi đề xuất |
|---|------|---------|---------|---------|---------|

## Gợi ý tương tác
- {gợi ý cụ thể: chia sẻ/bình luận/collab/cảm ơn}
```

## Ba lộ trình phát hiện

### Lộ trình 1 - Tìm trên nền tảng (lộ trình chính)

Dùng WebSearch tìm nội dung liên quan tới tên nhà sáng tạo/thương hiệu:

**Các tổ hợp từ khoá tìm kiếm:**
- `"{tên kênh} review"` / `"{tên kênh} đánh giá"` / `"{tên thương hiệu} trải nghiệm"`
- `"{tên kênh} site:xiaohongshu.com"` / `"site:bilibili.com"`
- `"{tên kênh} đồ tốt"` / `"{tên kênh} mẫu tương tự"`

Tập trung nền tảng theo tham số platforms, không chỉ định thì tìm lần lượt từng nền tảng.

### Lộ trình 2 - Theo dõi chủ đề/hashtag

Tìm chủ đề thương hiệu của nhà sáng tạo và các hashtag liên quan:

- `"#{tên kênh}# site:weibo.com"` - chủ đề trên Weibo
- `"#{chủ đề thương hiệu}#"` - chủ đề thương hiệu xuyên nền tảng
- `"{tên kênh} chủ đề"` / `"{tên thương hiệu} hashtag"`

### Lộ trình 3 - Quét thảo luận cộng đồng

Tìm diễn đàn, cộng đồng hỏi đáp, bài thảo luận:

- `"{tên thương hiệu} thế nào"` / `"{tên sản phẩm} có tốt không"` - Zhihu/Tieba
- `"{tên thương hiệu} có đáng mua không"` / `"{tên kênh} có uy tín không"` - thảo luận quyết định mua
- `"{tên thương hiệu} chê"` / `"{tên thương hiệu} tránh hố"` - tìm có hướng phản hồi tiêu cực

## Các bước thực hiện

1. **Xác nhận từ khoá**: lấy brand_keywords từ đầu vào của người dùng. Nếu có Profile, bổ sung tên kênh, tên thương hiệu, tên sản phẩm... từ `identity.md`.
2. **Xác định phạm vi tìm kiếm**: theo tham số platforms xác định nền tảng đích; theo content_type điều chỉnh trọng tâm từ khoá (reviews nghiêng về "đánh giá/review", complaints nghiêng về "chê/tránh hố").
3. **Chạy ba lộ trình**:
   - Lộ trình 1: mỗi nền tảng chạy 2-3 nhóm từ khoá (WebSearch)
   - Lộ trình 2: tìm chủ đề và hashtag thương hiệu
   - Lộ trình 3: tìm thảo luận cộng đồng
4. **Thu thập nội dung**: với các link liên quan cao trong kết quả tìm kiếm, dùng WebFetch lấy tóm tắt nội dung và số liệu tương tác.
5. **Khử trùng lặp và phân loại**: bỏ kết quả trùng, phân loại theo sắc thái cảm xúc (tích cực/trung tính/tiêu cực).
6. **Đánh giá cảm xúc**: dựa trên văn bản nội dung để xác định sắc thái, phân biệt nhắc tên mang tính sự kiện và nội dung mang tính đánh giá.
7. **Xếp hạng giá trị**: sắp theo lượng tương tác và chất lượng nội dung, lọc ra UGC giá trị cao (đáng tương tác/chia sẻ).
8. **Đánh dấu tiêu cực**: liệt kê riêng phản hồi tiêu cực, sắp theo mức nghiêm trọng, đưa ra chiến lược phản hồi đề xuất.
9. **Gợi ý tương tác**: với UGC giá trị cao, đưa ra gợi ý tương tác cụ thể (chia sẻ kèm lời cảm ơn / tương tác dưới bình luận / mời collab).
10. **Xuất báo cáo**: sinh báo cáo đầy đủ theo mẫu đầu ra, lưu vào `outputs/`.

## Nhận biết Profile

**Khi có Profile:**
- Đọc `identity.md` lấy tên kênh, tên thương hiệu, từ khoá dòng sản phẩm để tự mở rộng từ khoá tìm kiếm
- Đọc `platforms.md` xác định nền tảng đang hoạt động, ưu tiên tìm trên các nền tảng này
- Đọc `audience.md` để biết UGC nào đến từ nhóm khán giả mục tiêu (giá trị tương tác cao hơn)
- Đọc `style.md` để khớp giọng điệu và cách tương tác trong gợi ý

**Khi không có Profile:**
- Người dùng bắt buộc cung cấp brand_keywords, nếu không thì nhắc người dùng bổ sung
- Tìm toàn nền tảng, không xếp ưu tiên nền tảng
- Gợi ý tương tác đưa ra chiến lược chung
- Ghi chú "Cung cấp Profile sẽ giúp phát hiện UGC và gợi ý tương tác chính xác hơn"

## Quy tắc

1. **Tách sự kiện và phân tích** - nội dung tìm được là sự kiện, đánh giá cảm xúc là phân tích, ghi chú tách bạch hai phần
2. **Bắt buộc kèm link nguồn** - mỗi UGC phát hiện được phải kèm URL nguồn
3. **Không bịa UGC** - tìm không ra thì báo trung thực "không phát hiện UGC liên quan", không bịa nội dung
4. **Ưu tiên nội dung hành động được** - khi sắp xếp, ưu tiên hiển thị UGC có lượng tương tác cao, đáng phản hồi
5. **Không né nội dung tiêu cực** - phản hồi tiêu cực liệt kê riêng, đưa gợi ý phản hồi mang tính xây dựng
6. **Ghi rõ giới hạn dữ liệu** - kết quả WebSearch có giới hạn về thời gian và độ phủ, phải ghi rõ phạm vi và giới hạn tìm kiếm

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
