---
name: video-to-article
description: >-
  Bóc băng video nói, bài giảng, livestream, vlog rồi viết lại thành bài Facebook, blog, bài
  ảnh-chữ, kèm trích khung hình làm ảnh minh hoạ. Dùng khi người dùng nói "chuyển video thành bài
  viết", "viết bài từ video", "bóc băng". Chỉ phụ đề → auto-subtitle, dịch phụ đề →
  subtitle-translate.
layer: produce
---

# Chuyển video thành bài viết (video → bài đăng/bài dài)

> Tái dùng video thành nội dung ảnh-chữ: bóc băng → dựng thành bài có cấu trúc → trích khung hình làm ảnh. Bóc băng và trích khung chạy bằng script xác định
> (`asr.py` / `video_ops.py`), **phần dựng thành bài là việc của bạn (LLM)** - đây là giá trị cốt lõi của SKILL này.

> Chỉ cần file phụ đề thì xem **auto-subtitle**; dịch phụ đề thì xem **subtitle-translate**;
> làm bộ card Xiaohongshu thì xem **xhs-note-creator**; chỉ trau chuốt câu chữ thì xem **text-polisher**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| File video | Có | Video nói/bài giảng/livestream/Vlog (chưa đưa thì hỏi) |
| Dạng đích | Không | Bài đăng Facebook (mặc định) / bài dài blog, website / bài trả lời chuyên sâu / ảnh-chữ dạng chung |
| Số ảnh minh hoạ | Không | Trích mấy khung hình từ video (mặc định 3-6, theo mốc nội dung) |

## Đầu ra (`outputs/<chủ đề>/`)

- `article.md` - bài ảnh-chữ hoàn chỉnh (tiêu đề + nội dung + tiêu đề phụ/ý chính + câu đắt + hashtag)
- `assets/frame-*.jpg` - các khung hình đã trích
- `assets/transcript.txt` / `assets/transcript.json` - bản bóc băng gốc và mốc thời gian (để tra lại)

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/asr.py`, `skills/shared/scripts/video_ops.py`.

### 1. Bóc băng giọng nói (kèm mốc thời gian)
```bash
python skills/shared/scripts/asr.py transcribe -i input.mp4 --format json \
  -o "outputs/<chủ đề>/assets/transcript.json"
python skills/shared/scripts/asr.py transcribe -i input.mp4 --format txt \
  -o "outputs/<chủ đề>/assets/transcript.txt"
```
(Lần đầu chạy ASR cần proxy ra ngoài để tải model, xem phần chuẩn bị của auto-subtitle.)

### 2. Dựng thành bài ảnh-chữ (bạn làm)
Đọc bản bóc băng, viết lại thành bài theo dạng đích, **không chép nguyên lời nói**:
- **Rút cấu trúc**: lời kể lan man → tiêu đề rõ ràng + 3-6 tiêu đề phụ/đoạn ý chính.
- **Bỏ từ thừa**: xoá các câu cửa miệng kiểu "rồi thì, kiểu như, cái đó", viết văn hơn nhưng giữ chất riêng.
- **Bắt câu đắt**: nâng quan điểm giá trị nhất trong video thành câu đắt/câu in đậm.
- **Khớp theo dạng đích**: Facebook (emoji, đoạn ngắn, giọng bạn thân, hashtag) / blog, website (văn liền mạch, có mở thân kết) /
  bài trả lời chuyên sâu (chuyên môn, có mạch logic). Độ dài và cách trình bày theo chuẩn của `post-formatter` / `social-content`.
- Ghi vào `article.md`, trong bài đánh dấu "[Ảnh 1: cảnh xx @ 02:15]" để chỉ mốc thời gian video của từng ảnh.

### 3. Trích ảnh minh hoạ
Theo mốc thời gian đã đánh dấu ở bước 2, trích lần lượt từng khung hình:
```bash
python skills/shared/scripts/video_ops.py frame -i input.mp4 \
  -o "outputs/<chủ đề>/assets/frame-01.jpg" --time 00:02:15 --width 1080
```
Chọn mốc có hình rõ nét, nhiều thông tin (tránh khung mờ/khung chuyển cảnh).

### 4. (Tuỳ chọn) bộ card
Khi cần làm thành bộ card Xiaohongshu, đưa `article.md` cho **xhs-note-creator** hoặc **card-xiaohongshu**.

## Nhận biết Profile

- Có Profile: dạng đích mặc định theo nền tảng chính trong `platforms.md`; giọng/xưng hô/mức dùng emoji bám `style.md`;
  hashtag bám ngách của kênh; giới hạn tuân thủ theo `preferences.md`.
- Không có Profile: mặc định dạng bài đăng Facebook + giọng khẩu ngữ trung tính, cuối bài nhắc có thể đưa Profile để tuỳ biến giọng.

## Quy tắc

1. Đây là **viết lại** chứ không phải **bê nguyên bản bóc băng** - lời nói phải chuyển sang văn viết, có cấu trúc, bỏ từ thừa.
2. Ảnh minh hoạ trích từ khung hình thật của video, mốc thời gian do nội dung quyết định, tránh khung mờ.
3. Không bịa thông tin video không có; chỗ bóc băng nghe không rõ thì ghi "[nghe không rõ]" thay vì suy đoán.
4. Giữ quan điểm cốt lõi và chất riêng của người nói, đừng biến thành giọng AI na ná nhau (có thể chạy thêm text-polisher).
5. File `article.md` cuối cùng đặt ở `outputs/<chủ đề>/`, bản bóc băng và khung hình trung gian đặt ở `outputs/<chủ đề>/assets/`.

## Nguồn tham khảo

Video → bài viết là nhu cầu tái dùng nội dung rất phổ biến của nhà sáng tạo (một nguyên liệu nhiều món). Bóc băng dùng faster-whisper (asr.py), ảnh dùng
ffmpeg trích khung (video_ops.py frame), phần dựng bài giao cho LLM - tách lớp IO xác định khỏi phần viết lại sáng tạo.
