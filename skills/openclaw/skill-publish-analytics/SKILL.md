---
name: skill-publish-analytics
description: >-
  Phân tích nhật ký đăng theo 4 chiều (thời điểm đăng, hashtag, loại nội dung, tăng trưởng
  follower), quy kết hiệu quả, gợi ý tối ưu. Dùng khi người dùng nói "đăng giờ nào tốt", "hashtag
  nào hiệu quả", "phân tích dữ liệu đăng". skill-social-performance-review hậu kiểm đa nền tảng
  theo tháng.
layer: attribute
---

# Phân tích quy kết dữ liệu đăng bài

> Đọc publish-log.json, phân tích hiệu quả nội dung theo bốn chiều thời gian, hashtag, loại nội dung và tăng trưởng; xuất báo cáo quy kết có cấu trúc.

## Vị trí trong tầng dữ liệu

SKILL này là **tầng tiêu thụ** của chuỗi quy kết: chỉ đọc nền dữ liệu, không tạo kho mới, không ghi ngược:

| Dữ liệu | Nền chuẩn | Bên duy trì | SKILL này dùng để |
|------|----------|--------|----------------|
| Sự kiện đăng bài | `outputs/_analytics/publish-log.json` | skill-publish-log | Chế độ A/B/C |
| Người theo dõi / snapshot theo thời gian | `outputs/_analytics/snapshots/{profile}/{platform}/{date}.json` | skill-data-tracker | Chế độ D quy kết tăng trưởng |

**Nguồn chuẩn của chuỗi thời gian người theo dõi là nền snapshot của `skill-data-tracker`.** File `outputs/_analytics/follower-log.json` mà chế độ D đọc được `track.py export-followers` xuất ra một cách xác định, không sửa tay. Ánh xạ trường xem `references/follower-log-schema.md`.

## Đầu vào

Người dùng chọn chế độ phân tích (có thể kết hợp):

- **Chế độ A - Khung giờ đăng tốt nhất**: phân tích quan hệ giữa khung giờ đăng và dữ liệu tương tác
- **Chế độ B - Hiệu quả hashtag**: đánh giá ảnh hưởng của hashtag lên hiệu quả nội dung
- **Chế độ C - So sánh loại nội dung**: so sánh các chỉ số theo từng loại nội dung
- **Chế độ D - Quy kết tăng trưởng**: nối sự kiện đăng bài với tăng trưởng người theo dõi

Không chỉ định chế độ thì mặc định chạy A + B + C. Trước chế độ D hãy chạy `python3 skills/openclaw/skill-data-tracker/scripts/track.py export-followers`.

## Nguồn dữ liệu

### Cấu trúc publish-log.json

```json
{
  "version": "1.0",
  "entries": [{
    "id": "định danh duy nhất",
    "platform": "xiaohongshu|douyin|bilibili|weibo",
    "title": "tiêu đề",
    "url": "link bài đăng",
    "type": "image-text|video|livestream|article",
    "published_at": "dấu thời gian ISO 8601",
    "logged_at": "thời điểm ghi nhận",
    "initial_metrics": {
      "views": null | number,
      "likes": null | number,
      "comments": null | number,
      "shares": null | number
    },
    "skill_source": "SKILL đã tạo nội dung này",
    "profile": "tên hồ sơ kênh",
    "tags": ["danh sách hashtag"],
    "notes": "ghi chú"
  }]
}
```

### Quy tắc xử lý dữ liệu

- **Chỉ số null**: loại khỏi phép tính trung bình của chính chỉ số đó, báo cáo phần trăm độ phủ
- **Cảnh báo cỡ mẫu**: một nhóm < 5 bản ghi thì ghi `⚠ mẫu chưa đủ`; toàn bộ < 10 bản ghi thì cảnh báo ngay đầu báo cáo rằng kết quả có thể không có ý nghĩa thống kê
- **Múi giờ**: có Profile thì dùng múi giờ trong Profile, không có Profile thì mặc định Asia/Shanghai

## Các bước thực hiện

Toàn bộ phép tính của bốn chế độ (chia nhóm khung giờ, gộp hashtag, so sánh loại nội dung, quy kết tăng trưởng, cảnh báo cỡ mẫu,
độ phủ) do `scripts/analyze.py` làm một cách xác định. **Đừng nhẩm bằng Python nội tuyến, gọi thẳng script.**
LLM chỉ lo chọn chế độ, lọc theo Profile, đọc hiểu JSON, viết phát hiện chính/phương pháp/giới hạn.

1. Kiểm tra ngữ cảnh Profile (dấu `=== EASEL ACCOUNT PROFILE ===`), có thì lấy tên profile.
2. Gọi script (`--profile` phải đặt trước subcommand; publish-log.json không tồn tại thì script báo lỗi thân thiện):

```bash
python3 skills/openclaw/skill-publish-analytics/scripts/analyze.py all
python3 skills/openclaw/skill-publish-analytics/scripts/analyze.py --profile "<tên profile>" time
python3 skills/openclaw/skill-publish-analytics/scripts/analyze.py --profile "<tên profile>" tags
python3 skills/openclaw/skill-publish-analytics/scripts/analyze.py --profile "<tên profile>" types
python3 skills/openclaw/skill-publish-analytics/scripts/analyze.py --profile "<tên profile>" growth
```

3. Script xuất JSON có cấu trúc: `summary` (tổng số/khoảng ngày/nền tảng/độ phủ từng chỉ số/cảnh báo cỡ mẫu toàn bộ) +
   kết quả từng chế độ. Mỗi nhóm phân tích có `count` và `warning` (nhóm <5 bản ghi thì ghi mẫu chưa đủ).
4. **Đọc hiểu kết quả**: theo mô tả từng chế độ bên dưới và mục "Định dạng đầu ra", chuyển JSON thành bảng Markdown ->
   phát hiện chính (3 ý) -> phương pháp -> giới hạn. Phần giới hạn bắt buộc có "tương quan không phải nhân quả".

## Chế độ A - Khung giờ đăng tốt nhất

**Các bước:**
1. Phân tích `published_at` để lấy giờ và thứ trong tuần
2. Chia thành 6 nhóm khung giờ: sáng sớm(6-9) / buổi sáng(9-12) / trưa(12-14) / chiều(14-18) / tối(18-22) / đêm khuya(22-6)
3. Đối chiếu initial_metrics để tính tương tác trung bình của mỗi nhóm (views, likes, comments, shares)
4. Thống kê riêng theo từng nền tảng

**Đầu ra:**
- Bảng heatmap (thứ trong tuần x khung giờ), mỗi ô là điểm tương tác tổng hợp trung bình
- Gợi ý Top 3 khung giờ đăng (kèm thứ và khoảng giờ cụ thể)
- Khung giờ tốt nhất của từng nền tảng

**Cách tính điểm tương tác tổng hợp:**
`engagement_score = views * 0.1 + likes * 1.0 + comments * 2.0 + shares * 3.0`

## Chế độ B - Hiệu quả hashtag

**Các bước:**
1. Lấy `tags[]` của từng bản ghi, đếm tần suất dùng của mỗi hashtag
2. Với mỗi hashtag, tính views, likes, comments, shares trung bình của các bài có gắn nó
3. Dựng ma trận đồng xuất hiện: số lần hashtag A và hashtag B cùng xuất hiện
4. Nhận diện hashtag hiệu quả (tương tác trung bình cao hơn mức trung bình chung) và hashtag kém

**Đầu ra:**
- Bảng xếp hạng hiệu quả hashtag: hashtag / số lần dùng / lượt xem TB / lượt thích TB / bình luận TB / chia sẻ TB
- So sánh Top 5 với Bottom 5 hashtag
- Ma trận đồng xuất hiện (chỉ hiện các cặp xuất hiện chung >= 2 lần)

## Chế độ C - So sánh loại nội dung

**Các bước:**
1. Gom nhóm theo trường `type` (image-text / video / livestream / article)
2. Tính số bài đăng, views, likes, comments, shares trung bình của mỗi loại
3. Chéo nền tảng với loại nội dung thành bảng hai chiều

**Đầu ra:**
- Bảng so sánh loại: loại / số lượng / lượt xem TB / lượt thích TB / bình luận TB / chia sẻ TB
- Mỗi chỉ số đánh dấu "winner" (loại có giá trị cao nhất)
- Bảng chéo nền tảng x loại nội dung

## Chế độ D - Quy kết tăng trưởng

**Điều kiện trước:** `outputs/_analytics/follower-log.json` (view phái sinh xuất từ nền snapshot của `skill-data-tracker`, schema và ánh xạ trường xem `references/follower-log-schema.md`)

**Các bước:**
1. Đọc follower-log.json, nếu không có thì báo một dòng và bỏ qua chế độ này
2. Nối mỗi sự kiện đăng bài với biến động người theo dõi sau 24h / 48h / 7d
3. Tính mức tăng người theo dõi của từng bài (snapshot sau khi đăng - snapshot gần nhất trước khi đăng)
4. Xếp hạng theo mức tác động lên người theo dõi

**Đầu ra:**
- Bảng xếp hạng tác động của bài đăng: tiêu đề / nền tảng / thời điểm đăng / tăng 24h / tăng 48h / tăng 7d
- Phân tích điểm chung của các bài tăng mạnh (loại nội dung, hashtag, khung giờ)
- Nếu follower-log.json không tồn tại, xuất:
  > "Chế độ D cần dữ liệu người theo dõi. Hãy ghi snapshot người theo dõi vào outputs/_analytics/follower-log.json, schema xem skill-publish-analytics/references/follower-log-schema.md"

## Định dạng đầu ra

Đầu ra của mỗi chế độ đều gồm các phần sau:

```markdown
## Tóm tắt dữ liệu
- Tổng số bản ghi / khoảng ngày / nền tảng liên quan
- Độ phủ từng chỉ số (tỉ lệ không null)

## Kết quả phân tích
(bảng và biểu đồ tương ứng với chế độ)

## Phát hiện chính
1. (insight quan trọng nhất, làm được ngay)
2. (quan trọng thứ hai)
3. (quan trọng thứ ba)

## Phương pháp
- Công thức tính điểm tương tác tổng hợp
- Cách gộp số liệu (trung bình / trung vị)
- Tiêu chí chia khung giờ

## Giới hạn
- Ghi chú về cỡ mẫu
- Độ phủ dữ liệu null
- "Tương quan không phải nhân quả - phân tích khung giờ/hashtag chỉ cho thấy liên hệ, không suy ra nhân quả"
```

## Nhận biết Profile

- **Có Profile**:
  - Lọc theo trường `profile`, chỉ phân tích dữ liệu của kênh hiện tại
  - Dùng trường platform và timezone trong Profile
  - Đầu ra ghi rõ "Phạm vi phân tích: {profile_name} @ {platform}"
- **Không có Profile**:
  - Phân tích toàn bộ bản ghi, hiển thị theo nhóm nền tảng
  - Ghi chú trong báo cáo: "Cung cấp Profile để lọc dữ liệu theo kênh và dùng múi giờ riêng của nền tảng"

## Quy tắc

1. **Không bịa số liệu** - mọi con số phải lấy từ publish-log.json, không suy đoán hay điền thêm
2. **Báo cáo cỡ mẫu** - mỗi nhóm phân tích bắt buộc ghi số bản ghi
3. **Tương quan không phải nhân quả** - phần khung giờ và hashtag bắt buộc ghi chú "tương quan không phải nhân quả"
4. **Cảnh báo thiếu mẫu** - toàn bộ < 10 bản ghi thì in đậm cảnh báo ở đầu báo cáo
5. **Minh bạch cách tính** - trình bày công thức và cách gộp của từng chỉ số

## Ghi chú tự phát triển

Sản phẩm tham khảo: Metricool analytics, Iconosquare insights, SocialBee performance reports, Later analytics.
SKILL này tập trung phân tích nhịp đăng và quy luật tương tác trên các nền tảng mạng xã hội Trung Quốc (Xiaohongshu, Douyin, Bilibili, Weibo).
