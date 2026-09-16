---
name: video-highlights
description: >-
  Cắt highlight từ video dài/livestream ra nhiều clip, tuỳ chọn 9:16 + phụ đề; tìm điểm theo đỉnh
  âm thanh (hò reo) hoặc bóc băng chọn câu đắt. Dùng khi người dùng nói "cắt highlight", "cắt live
  thành clip", "lọc điểm nhấn". clipify chuyên tiếng Anh + pan bám mặt; skill này tổng quát hơn.
layer: produce
---

# Cắt highlight từ video dài / bản ghi livestream

> Tìm đoạn highlight trong video dài -> cắt thành nhiều clip ngắn (có thể chuyển khung dọc + thêm phụ đề). Việc cắt chạy qua
> `skills/shared/scripts/highlight_cut.py`, **đừng tự ghép lệnh cắt** - script đã lo cắt chính xác,
> chừa khoảng trước/sau, xuất hàng loạt, chuyển khung dọc và sinh danh sách clip.

> Video nói tiếng Anh cần tìm điểm cười + pan bám mặt theo từng đoạn thì xem **clipify**; chỉ đổi khung hình thì xem **video-reframe**;
> dịch phụ đề thì xem **subtitle-translate**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Video dài | Có | Bản ghi livestream / video dài (chưa có thì hỏi) |
| Cách tìm điểm | Không | `energy` (mặc định, chỗ cảm xúc lên cao) / `content` (bóc băng rồi chọn theo câu đắt/điểm bùng) |
| Số clip | Không | Cắt mấy clip (mặc định 5) |
| Độ dài mỗi clip | Không | Mỗi clip dài khoảng bao nhiêu (mặc định 20s) |
| Chuyển khung dọc | Không | Có chuyển 9:16 để đăng TikTok/YouTube Shorts không |

## Đầu ra (`outputs/<chủ đề>/`)

- Nhiều clip (`highlight_01.mp4` ...) + danh sách `highlights.json`

## Các bước thực hiện

Đường dẫn script (so với gốc dự án): `skills/shared/scripts/highlight_cut.py` (`energy -h` / `cut -h`).

### Cách A: tìm điểm theo năng lượng âm thanh (nhanh, hợp livestream có hò reo/cảm xúc lên xuống)
```bash
# 1) Tìm các đoạn ứng viên
python skills/shared/scripts/highlight_cut.py energy -i "<video dài>" \
  --top 5 --clip-len 20 -o /tmp/hl_cand.json
# 2) Cắt clip (có thể chuyển khung dọc luôn)
python skills/shared/scripts/highlight_cut.py cut -i "<video dài>" \
  --segments /tmp/hl_cand.json -o "outputs/<chủ đề>" \
  --reframe 9:16 --reframe-mode blur
```

### Cách B: tìm điểm theo nội dung (chuẩn, hợp video nói/kiến thức/bán hàng, chọn câu đắt và điểm bùng)
1. Bóc băng trước (dùng lại `asr.py` của auto-subtitle, có timeline):
   ```bash
   python skills/shared/scripts/asr.py transcribe -i "<video dài>" --format json -o /tmp/hl.json
   ```
2. **Bạn** đọc bản bóc băng, chọn ra 3-5 đoạn giá trị nhất/cuốn nhất (trọn ý, đừng cắt nửa câu),
   ghi thành danh sách clip `/tmp/hl_segs.json`:
   ```json
   {"segments": [{"start": 73.2, "end": 95.0, "label": "câu đắt: xxx"}, ...]}
   ```
3. Cắt clip:
   ```bash
   python skills/shared/scripts/highlight_cut.py cut -i "<video dài>" \
     --segments /tmp/hl_segs.json -o "outputs/<chủ đề>" --reframe 9:16
   ```

`--pad 0.3` chừa khoảng trước/sau mỗi đoạn để không cắt quá sát; không chuyển khung dọc thì bỏ `--reframe`.

## Nhận biết Profile

- Có Profile: tỉ lệ khung dọc theo nền tảng chính trong `platforms.md`; tìm điểm bám theo định vị kênh (bán hàng thì nhắm điểm bùng,
  kiến thức thì nhắm câu đắt, giải trí thì nhắm cao trào cảm xúc); độ dài clip bám theo nền tảng (Douyin 15-30s, Video Channels 30-60s).
- Không có Profile: mặc định tìm điểm theo năng lượng top5, mỗi đoạn 20s, hỏi xem có chuyển khung dọc không.

## Quy tắc

1. Tìm điểm theo nội dung thì bắt buộc cắt **trọn ý**, đừng vào/ra giữa nửa câu.
2. Tìm điểm theo năng lượng hợp với tư liệu có cảm xúc lên xuống rõ; video nói đều đều thì ưu tiên tìm theo nội dung (cách B).
3. Clip mặc định chừa 0.3s ở đầu và cuối để không bị cắt mất đoạn mở/kết.
4. Chuyển khung dọc cho video nói thì nên dùng `--reframe-mode smart` (canh giữa khuôn mặt), còn lại dùng `blur` (không mất hình).
5. Sản phẩm để hết vào `outputs/<chủ đề>/`, kèm danh sách `highlights.json`.

## Nguồn tham khảo

Chọn đoạn theo năng lượng âm thanh dùng đỉnh RMS của librosa (lọc tham lam để giữ khoảng cách giữa các đỉnh); chọn đoạn theo nội dung theo lối opus-clip "bóc băng -> chọn câu đắt"
nhưng để LLM phán đoán. Việc cắt và chuyển khung dọc dùng lại script xác định, đảm bảo timeline và khung hình không sai.
