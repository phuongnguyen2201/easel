---
name: skill-algorithm-updates
description: >-
  Theo dõi thay đổi cơ chế nền tảng: thuật toán, phân phối, kiểm duyệt, kiếm tiền của Facebook,
  TikTok, YouTube, Zalo, tác động tới nhà sáng tạo. Dùng khi người dùng nói "thuật toán đổi à",
  "nền tảng đổi luật", "sao view tụt". Trend: skill-trending-topics; tin ngành:
  skill-news-intelligence.
layer: discover
---

# Theo dõi biến động thuật toán nền tảng

> Tổng hợp cập nhật thuật toán, thay đổi cơ chế đề xuất và điều chỉnh quy tắc phân phối của các nền tảng mạng xã hội Trung Quốc, xuất bản tin có cấu trúc.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| platforms | Không | Danh sách nền tảng cần theo dõi (mặc định đủ 6: Douyin/Xiaohongshu/Bilibili/Weibo/Zhihu/Video Channels) |
| time_range | Không | Khoảng thời gian: "1 tuần gần đây" / "1 tháng gần đây" / "3 tháng gần đây" (mặc định "1 tháng gần đây") |
| focus | Không | Hướng quan tâm: "phân phối traffic" / "kiểm duyệt nội dung" / "quy tắc kiếm tiền" / "tất cả" (mặc định "tất cả") |

## Đầu ra

```markdown
# Bản tin biến động thuật toán nền tảng
Ngày cập nhật: {date}
Nền tảng bao phủ: {platforms}
Khoảng thời gian: {time_range}
Hướng quan tâm: {focus}

## {tên nền tảng}
### Thay đổi gần đây
- **{tiêu đề thay đổi}**: {mô tả cụ thể} (nguồn: {source}, thời gian: {date})
- ...

### Tác động tới nhà sáng tạo
- {mô tả tác động}

### Khuyến nghị ứng phó
- {khuyến nghị làm được ngay}

(mỗi nền tảng một mục, cấu trúc giống nhau)

## Xu hướng xuyên nền tảng
- {hướng thay đổi quy tắc xuất hiện ở nhiều nền tảng cùng lúc}

## Nguồn thông tin
- [{tiêu đề nguồn}]({URL})
- ...
```

## Các bước thực hiện

### Bước 1: Xác định phạm vi

- Phân tích tham số đầu vào, chốt danh sách nền tảng, khoảng thời gian và hướng quan tâm
- Có Profile thì đọc `profiles/<hồ sơ>/platforms.md`, ưu tiên phủ các nền tảng nhà sáng tạo đang hoạt động
- Không có Profile thì phủ đủ 6 nền tảng

### Bước 2: Tìm kiếm đa chiều - kênh chính thức của nền tảng và cộng đồng nhà sáng tạo

Với mỗi nền tảng, chạy 2-3 nhóm truy vấn web_search:

- `"{tên nền tảng} thuật toán cập nhật {năm hiện tại}"`
- `"{tên nền tảng} cơ chế đề xuất thay đổi nhà sáng tạo"`
- `"{tên nền tảng} quy tắc phân phối mới nhất"`

Nếu focus khác "tất cả", thêm truy vấn định hướng:
- Phân phối traffic: `"{tên nền tảng} vòng phân phối điều chỉnh"`
- Kiểm duyệt nội dung: `"{tên nền tảng} quy tắc kiểm duyệt nội dung thay đổi"`
- Quy tắc kiếm tiền: `"{tên nền tảng} chính sách kiếm tiền cập nhật"`

Đọc `references/platform-sources.md` để lấy URL nguồn chính thức của từng nền tảng và mẫu truy vấn.

### Bước 3: Tìm kiếm nguồn tin bên thứ ba

Bổ sung góc nhìn ngành, chạy các truy vấn sau:

- `"nền tảng mạng xã hội thuật toán thay đổi {năm hiện tại}"` giới hạn trong newrank.cn / woshipm.com / 36kr.com
- `"{tên nền tảng} nhà sáng tạo than phiền thuật toán"` - bắt cảm nhận thực tế trong thảo luận cộng đồng
- `"mạng xã hội Trung Quốc thuật toán đề xuất xu hướng"` - lấy phân tích tổng hợp xuyên nền tảng

### Bước 4: Thu thập và trích xuất

Với 3-5 kết quả liên quan nhất ở bước 2 và bước 3 (mỗi nền tảng), chạy web_fetch:

- Trích mô tả cụ thể của thay đổi thuật toán, thời điểm hiệu lực, nguyên văn thông báo chính thức
- Đọc `references/algorithm-vocabulary.md` để hiểu thuật ngữ riêng của từng nền tảng
- Phân tầng nguồn thông tin:
  - **Xác nhận chính thức**: thông báo chính thức của nền tảng, thông báo trong trung tâm nhà sáng tạo
  - **Báo ngành**: bài đưa tin của Newrank, 36kr và các trang tương tự
  - **Cảm nhận cộng đồng**: thảo luận trong cộng đồng nhà sáng tạo, quan sát cá nhân (ghi rõ là chưa kiểm chứng)

### Bước 5: Tổng hợp bản tin

Gom thông tin đã trích theo từng nền tảng thành bản tin có cấu trúc:

1. **Sắp theo từng nền tảng**: liệt kê từng thay đổi theo thời gian giảm dần, kèm URL nguồn và ngày
2. **Phân tích tác động**: mỗi thay đổi ảnh hưởng cụ thể gì tới nhà sáng tạo (lượt tiếp cận, chiến lược nội dung, kiếm tiền)
3. **Khuyến nghị ứng phó**: với mỗi thay đổi, đưa ra điều chỉnh làm được ngay
4. **Xu hướng xuyên nền tảng**: nhận diện hướng thay đổi quy tắc xuất hiện ở nhiều nền tảng (ví dụ "các nền tảng video ngắn đồng loạt tăng trọng số tỉ lệ xem hết")
5. **Tổng hợp nguồn**: liệt kê toàn bộ URL đã trích dẫn

### Bước 6: Xuất kết quả

Lưu bản tin vào thư mục `outputs/<chủ đề>/`.

## Quy tắc

1. **Mỗi khẳng định phải kèm URL nguồn** - thông tin không có nguồn thì không đưa vào bản tin
2. **Tách xác nhận khỏi tin đồn** - thông báo chính thức ghi "đã xác nhận", thảo luận cộng đồng ghi "chưa kiểm chứng / phản hồi cộng đồng"
3. **Ghi mốc thời gian** - mỗi thay đổi ghi rõ thời điểm xảy ra; thay đổi cũ hơn 6 tháng xếp vào "thông tin nền" chứ không phải "thay đổi gần đây"
4. **Không dự đoán tương lai** - chỉ báo cáo thay đổi đã xảy ra, không suy đoán nền tảng sẽ điều chỉnh tiếp thế nào
5. **Báo trung thực khi không có kết quả** - nền tảng nào không thấy thay đổi gần đây thì ghi rõ "không thấy thay đổi thuật toán gần đây", không bịa

## Nhận biết Profile

**Khi có Profile:**
- Đọc `profiles/<hồ sơ>/platforms.md` để xác định nền tảng nhà sáng tạo đang hoạt động, ưu tiên phủ các nền tảng này
- Phân tích tác động gắn với loại nội dung của nhà sáng tạo (ví dụ "bạn làm nội dung kiến thức, trọng số tỉ lệ xem hết tăng là có lợi cho bạn")
- Khuyến nghị ứng phó may đo theo tình huống cụ thể của nhà sáng tạo
- Nền tảng không hoạt động thì chỉ đưa thông tin mức tóm tắt

**Khi không có Profile:**
- Phủ đều cả 6 nền tảng
- Phân tích tác động hướng tới nhóm nhà sáng tạo nói chung
- Khuyến nghị ứng phó giữ tính tổng quát, không phán đoán cá nhân hoá

## Ghi chú tự phát triển

> Khác với skill-cross-platform-diff: cross-platform-diff phân tích khác biệt **đặc điểm tĩnh** giữa các nền tảng, SKILL này theo dõi thay đổi **quy tắc động**.
> Nguồn gốc tự phát triển và khác biệt cốt lõi xem `EASEL-META.md` cùng thư mục.
