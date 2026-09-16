---
name: video-strategy
description: >-
  Lập chiến lược sản xuất video, chọn công cụ: so sánh model AI tạo video, cấu trúc kịch bản, quy
  trình sản xuất cho demo sản phẩm, video giải thích, video ngắn mạng xã hội. Dùng khi người dùng
  nói "làm video thế nào", "làm video bằng gì", "lên series video". Kịch bản cụ thể →
  video-script.
layer: produce
---

# Chiến lược sản xuất video

Chiến lược sản xuất video và chọn công cụ. Bao gồm so sánh model AI tạo video, chọn framework video lập trình, thiết kế cấu trúc kịch bản, lên quy trình sản xuất.

> Skill này lo **hoạch định chiến lược và chọn công cụ**. Skill `video-editing` đã triển khai sẽ chạy thao tác dựng bằng ffmpeg thật (cắt, jump cut, chèn chữ, đổi tốc độ...).

## Đầu vào

- Mục tiêu video (demo sản phẩm / video giải thích / video ngắn mạng xã hội / quảng cáo / hướng dẫn)
- Nền tảng mục tiêu (Douyin / Bilibili / Kuaishou / Video Channels / YouTube / Instagram)
- Tư liệu sẵn có (ảnh chụp màn hình, video quay màn hình, kịch bản, tư liệu thương hiệu)
- Ràng buộc ngân sách và tech stack

## Đầu ra

- Phương án sản xuất đề xuất (chọn công cụ + lý do)
- Thông số khớp nền tảng (độ phân giải, thời lượng, tỉ lệ khung hình)
- Các bước trong quy trình sản xuất
- Cấu trúc kịch bản video (nếu cần)

## Các bước thực hiện

### 1. Thu thập bối cảnh

Xác nhận các thông tin sau (chưa có thì chủ động hỏi):
- **Loại video**: demo sản phẩm, video giải thích, video ngắn mạng xã hội, quảng cáo, hướng dẫn
- **Nền tảng mục tiêu**: quyết định tỉ lệ khung hình và giới hạn thời lượng (xem bảng thông số nền tảng bên dưới)
- **Cách thể hiện**: người ảo AI / lời dẫn + hình / thuần lập trình / quay màn hình
- **Tình trạng tư liệu**: đã có sẵn gì chưa (ảnh chụp màn hình, video quay màn hình, logo)
- **Nhu cầu tái sử dụng**: làm một lần hay dựng mẫu để sản xuất hàng loạt
- **Ngân sách**: một số công cụ tính phí theo thời lượng video

### 2. Chọn phương án sản xuất

| Phương án | Tình huống phù hợp | Công cụ | Khả dụng |
|------|---------|------|--------|
| **Video lập trình** | Theo mẫu, chạy bằng dữ liệu, số lượng lớn | Hyperframes, Remotion | ✅ Node.js dùng được |
| **AI tạo video** | Hình ảnh gốc, B-roll | Veo 3, Sora 2, Runway, Kling, Seedance | ⚠️ Cần API key |
| **Người ảo AI** | Có người xuất hiện, đa ngôn ngữ | HeyGen, Synthesia | ⚠️ Cần API key |
| **Dựng lại/chế lại** | Cắt video dài thành video ngắn | ffmpeg (skill video-editing), CapCut | ✅ ffmpeg dùng được |

### 3. So sánh model AI tạo video

Nếu người dùng cần AI tạo hình cho video, chọn theo bảng này:

| Model | Độ phân giải | Thời lượng tối đa | Thế mạnh | Chi phí |
|------|--------|---------|------|------|
| **Veo 3** (Google) | Tối đa 1080p | Linh hoạt | Chất lượng hình cao nhất + âm thanh đồng bộ | Tính phí API |
| **Sora 2** (OpenAI) | Tối đa 1080p | ~20s | Chất điện ảnh + âm thanh đồng bộ | API + ChatGPT |
| **Runway Gen-4** | Tối đa 4K | ~10s/lần | Kiểm soát chuyển động, nhất quán theo thời gian | Thuê bao |
| **Kling 2.5/3.0** (Kuaishou) | Tối đa 1080p | Tối đa 2 phút | Cảnh dài, chi phí đơn vị thấp | Tính phí theo giây (đơn giá thấp) |
| **Seedance** (ByteDance) | Tối đa 1080p | Đoạn ngắn | Tạo nhanh, chuyển động bám sát, hợp làm hàng loạt | Tính theo credit |
| **Hailuo / MiniMax** (MiniMax) | Tối đa 1080p | Đoạn ngắn | Nhân vật nhất quán qua nhiều cảnh | Tính theo credit |
| **Pika 2.x** | 1080p | Đoạn ngắn | Hiệu ứng nhanh, ảnh thành video | Tính theo credit |
| **Hunyuan Video / Wan 2** (Tencent) | 720p-1080p | Linh hoạt | Mã nguồn mở tự host, kiểm soát hoàn toàn, không phí API | Miễn phí (cần GPU) |

**Chọn nhanh**:
- **Chất lượng hình cao nhất + âm thanh**: Veo 3 hoặc Sora 2
- **Hàng loạt / chi phí thấp**: Kling, Seedance
- **Nhân vật nhất quán qua nhiều cảnh**: Hailuo
- **Tự host / kiểm soát thương hiệu**: Hunyuan Video hoặc Wan 2 (trọng số mở)
- **Ảnh thành video**: Kling, Pika, Runway

> Số hiệu phiên bản và giá trong bảng trên thay đổi rất nhanh theo từng hãng, chỉ để tham khảo khi chọn, **lấy công bố mới nhất của từng hãng làm chuẩn**.

> Cách viết prompt cho AI video xem [references/ai-video-prompting.md](references/ai-video-prompting.md)

### 4. Thông số nền tảng mục tiêu

#### Nền tảng Trung Quốc

| Nền tảng | Tỉ lệ khung hình | Độ phân giải khuyến nghị | Giới hạn thời lượng | Ghi chú |
|------|--------|-----------|---------|------|
| **Douyin** | 9:16 | 1080x1920 | 15s / 60s / 15min | Dưới 15s thì trọng số tỉ lệ xem hết cao nhất |
| **Bilibili** | 16:9 | 1920x1080 | Không giới hạn cứng | Chủ yếu khung ngang, khung dọc vẫn hỗ trợ |
| **Kuaishou** | 9:16 | 1080x1920 | 11min | Chủ yếu khung dọc |
| **Video Channels** | 9:16 / 16:9 | 1080x1920 | 30min | Video ngắn < 1min được ưu tiên đề xuất |
| **Xiaohongshu** | 9:16 / 3:4 | 1080x1920 | 15min | 3:4 cũng hay dùng |

#### Nền tảng quốc tế

| Nền tảng | Tỉ lệ khung hình | Độ phân giải khuyến nghị | Giới hạn thời lượng |
|------|--------|-----------|---------|
| **YouTube** | 16:9 | 1920x1080 / 3840x2160 | Không giới hạn |
| **YouTube Shorts** | 9:16 | 1080x1920 | 60s |
| **TikTok** | 9:16 | 1080x1920 | 10min |
| **Instagram Reels** | 9:16 | 1080x1920 | 90s |
| **Instagram Feed** | 1:1 / 4:5 | 1080x1080 / 1080x1350 | 60s |

### 5. Framework video lập trình

Dùng code sinh video, hợp cho sản xuất hàng loạt lặp lại được, theo mẫu, chạy bằng dữ liệu.

**Hyperframes** (HTML/CSS, khuyến nghị) - mã nguồn mở, Apache 2.0, mỗi khung hình là một tài liệu HTML, thân thiện nhất với agent.
**Remotion** (React) - khả năng animation mạnh hơn, hợp hiệu ứng phức tạp và render hàng loạt trên Lambda.

| Yếu tố | Hyperframes | Remotion |
|------|-------------|----------|
| Mức thân thiện với agent | Tốt hơn (thuần HTML) | Tốt (React) |
| Khả năng animation | Cơ bản (CSS transition) | Nâng cao (Spring, interpolate) |
| Render hàng loạt | Tại máy | Lambda (AWS) |
| Giấy phép | Apache 2.0 | Dùng thương mại cần mua bản quyền |

### 6. Mẫu quy trình sản xuất

**Video demo sản phẩm**: kịch bản → quay màn hình → chèn lớp lập trình (tiêu đề, chú thích) → B-roll AI → lồng tiếng → xuất theo thông số nền tảng

**Video giải thích**: kịch bản (vấn đề→giải pháp→CTA) → chọn cách thể hiện (người ảo AI / lời dẫn) → làm hình → thêm phụ đề → xuất

**Video ngắn mạng xã hội hàng loạt**: dựng mẫu bằng Hyperframes/Remotion → đổ dữ liệu → render hàng loạt → thêm phụ đề theo nền tảng → phân phối

**Nhân bản cách dựng video viral**: lấy video tham chiếu → bóc nhịp dựng theo từng nhịp → xuất beat sheet → làm lại bằng tư liệu của mình. Xem [references/edit-anatomy.md](references/edit-anatomy.md)

### 7. Pipeline agent điều khiển trực tiếp được

```
Agent viết kịch bản (kết hợp Profile)
    ↓
Hyperframes: HTML → MP4 (video lập trình)
    và/hoặc
AI video API: tạo B-roll
    ↓
ffmpeg (skill video-editing): cắt ghép
    ↓
sản phẩm → outputs/<chủ đề>/
```

## Lỗi thường gặp

1. **Chọn công cụ trước rồi mới nghĩ chiến lược** - chốt mục tiêu video trước, rồi mới chọn công cụ
2. **Bắt AI tạo chữ ngay trong video** - model không render nổi chữ đọc được một cách ổn định, hãy chèn lớp chữ bằng lập trình
3. **Bỏ qua phụ đề** - 85% video mạng xã hội được xem ở chế độ tắt tiếng, bắt buộc phải có phụ đề
4. **Sai tỉ lệ khung hình** - dọc 9:16 cho mạng xã hội, ngang 16:9 cho YouTube/website
5. **Làm quá kỹ** - trên mạng xã hội, cảm giác chân thật thường thắng cảm giác trau chuốt

## Nhận biết Profile

Phát hiện dấu hiệu `=== EASEL ACCOUNT PROFILE ===`.

**Khi có Profile**:
- Đọc phong cách hình ảnh thương hiệu từ Profile (màu, font, logo) để áp vào mẫu video
- Đọc nền tảng ưa dùng, ưu tiên đề xuất thông số của nền tảng đó
- Đọc hồ sơ khán giả để chỉnh phong cách video (chuyên nghiệp/nhẹ nhàng/bắt trend)
- Đọc thông tin sản phẩm, dùng thẳng khi viết kịch bản

**Khi không có Profile**:
- Lùi về chế độ tổng quát, chủ động hỏi phong cách thương hiệu và nền tảng mục tiêu
- Đề xuất phương án theo best practice chung
