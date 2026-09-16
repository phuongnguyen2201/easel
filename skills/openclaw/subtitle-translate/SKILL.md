---
name: subtitle-translate
description: >-
  Dịch phụ đề có sẵn (SRT/VTT/ASS) sang ngôn ngữ đích, ra song ngữ (gốc + dịch) hoặc chỉ bản dịch,
  gắn mềm hoặc đốt cứng vào video. Dùng khi người dùng nói "dịch phụ đề", "phụ đề song ngữ", "dịch
  SRT sang tiếng Việt/Anh". auto-subtitle tạo phụ đề từ giọng nói, skill này chỉ dịch bản có sẵn.
layer: produce
---

# Dịch phụ đề / phụ đề song ngữ

> Dịch phụ đề có sẵn sang ngôn ngữ đích, cho ra phụ đề **song ngữ** (bản gốc + bản dịch) hoặc **chỉ bản dịch**, tuỳ chọn đốt cứng vào video.
> Phần dịch giao cho LLM (chính bạn), phần xác định (parse/gộp/định dạng/timeline/đốt phụ đề) giao hết cho
> `skills/shared/scripts/subtitle_ops.py`. **Đừng tự ghép lệnh ffmpeg, cũng đừng sửa tay timeline.**

> Chỉ làm "phụ đề có sẵn -> dịch/song ngữ/đốt cứng". Nhận dạng giọng nói để tạo phụ đề xem **auto-subtitle**;
> Dựng video nói chung xem **video-editing**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| File phụ đề | Có | Đường dẫn `.srt` / `.vtt` / `.ass` (không đưa thì hỏi) |
| Ngôn ngữ đích | Có | Dịch sang ngôn ngữ nào (vd Tiếng Việt / English / Tiếng Nhật) |
| Dạng đầu ra | Không | `song ngữ` (mặc định) / `chỉ bản dịch` |
| Thứ tự gốc-dịch | Không | Khi song ngữ: bản gốc ở trên (mặc định) hoặc bản dịch ở trên |
| File video | Không | Có thì đốt được phụ đề; gắn mềm (bật/tắt được) hoặc đốt cứng (in thẳng vào hình) |

## Đầu ra (`outputs/<chủ đề>/`)

- File phụ đề song ngữ / chỉ bản dịch (`.srt` hoặc `.ass`)
- Nếu đốt phụ đề: video có phụ đề (`*-sub.mp4`)
- Báo cáo: số dòng phụ đề, ngôn ngữ đích, dạng đầu ra, đường dẫn xuất

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/subtitle_ops.py` (mỗi subcommand đều hỗ trợ `-h`).

### 1. Trích văn bản cần dịch
```bash
python skills/shared/scripts/subtitle_ops.py extract -i "<phụ đề>" -o /tmp/st_lines.txt
```
Mỗi dòng phụ đề nằm trên một dòng, số dòng và thứ tự cố định. **Nhớ tổng số dòng N.**

### 2. Dịch từng dòng (bạn tự làm)
Đọc `/tmp/st_lines.txt`, dịch từng dòng sang ngôn ngữ đích, ghi vào `/tmp/st_trans.txt`:
- **Số dòng phải đúng bằng N, thứ tự khớp một-một, không thêm bớt dòng trống, không gộp, không tách dòng** (script sẽ kiểm, lệch là báo lỗi ngay).
- Một dòng gốc có nhiều câu thì gộp thành một dòng dịch, đừng tách ra nhiều dòng.
- Giọng và thuật ngữ bám theo lĩnh vực nội dung; nội dung nói thì dịch tự nhiên như nói, nội dung văn viết thì dịch trang trọng.
- Dòng gốc trống thì dòng dịch cũng để trống (giữ chỗ).

### 3. Gộp thành phụ đề song ngữ / chỉ bản dịch
```bash
# SRT song ngữ (bản gốc ở trên, bản dịch ở dưới)
python skills/shared/scripts/subtitle_ops.py merge -i "<phụ đề>" --trans /tmp/st_trans.txt \
  -o "outputs/<chủ đề>/<tên>-bilingual.srt"

# ASS song ngữ (bản gốc chữ trắng to hơn / bản dịch chữ vàng nhỏ hơn, kiểu đẹp hơn, nên dùng khi đốt cứng)
python skills/shared/scripts/subtitle_ops.py merge -i "<phụ đề>" --trans /tmp/st_trans.txt \
  -o "outputs/<chủ đề>/<tên>-bilingual.ass" --format ass

# Chỉ bản dịch (không giữ bản gốc)
python skills/shared/scripts/subtitle_ops.py merge -i "<phụ đề>" --trans /tmp/st_trans.txt \
  -o "outputs/<chủ đề>/<tên>-<lang>.srt" --trans-only
```
`--order trans-top` để đưa bản dịch lên trên.

### 4. (Tuỳ chọn) Đốt phụ đề vào video
```bash
# Đốt cứng (in thẳng vào hình, nên dùng .ass để giữ kiểu song ngữ)
python skills/shared/scripts/subtitle_ops.py burn -i "<video>" \
  --sub "outputs/<chủ đề>/<tên>-bilingual.ass" \
  -o "outputs/<chủ đề>/<tên>-sub.mp4"

# Gắn mềm (bật/tắt trong trình phát, không đổi hình; mp4 -> mov_text, mkv -> srt)
python skills/shared/scripts/subtitle_ops.py burn -i "<video>" \
  --sub "outputs/<chủ đề>/<tên>-bilingual.srt" \
  -o "outputs/<chủ đề>/<tên>-sub.mp4" --soft
```

## Các subcommand khác

- `parse -i "<phụ đề>" [-o out.json]` - parse thành JSON (kèm timeline), để xử lý bằng chương trình hoặc đối chiếu.
- `build --json <cues.json> -o "<phụ đề>"` - dựng từ JSON (cue có `text` và `trans` tuỳ chọn), hợp cho dịch hàng loạt/cả đoạn rồi điền ngược.
- `convert -i a.srt -o b.vtt` - chuyển đổi định dạng (srt <-> vtt <-> ass).

## Quy tắc

1. Dịch theo ba bước extract -> dịch từng dòng -> merge, **giữ đúng số dòng**, tuyệt đối không để script phải "đoán dòng nào khớp dòng nào".
2. Timeline, số dòng phụ đề và định dạng đều do script sinh ra, cấm sửa tay dấu thời gian.
3. Đốt cứng nên ưu tiên `.ass` (có sẵn style Noto Sans CJK); nếu đốt cứng bằng srt mà chữ tiếng Việt có dấu thành ô vuông, thêm `--font-dir` cho `burn` trỏ tới thư mục có font Unicode đầy đủ.
4. Song ngữ mặc định bản gốc ở trên, bản dịch ở dưới (chỉnh bằng `--order`); chỉ bản dịch thì dùng `--trans-only`.
5. Sản phẩm đều vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Hình thái công cụ dịch phụ đề tham khảo các dự án mã nguồn mở: rockbenben/subtitle-translator (song ngữ hàng loạt, canh trên dưới bản dịch),
bonigarcia/dualsub (gộp song ngữ), innovationmech/video-translate (nhúng phụ đề mềm/cứng).
SKILL này giao phần "dịch" cho LLM, chỉ biến các khâu dễ sai là parse/timeline/gộp/đốt phụ đề thành script xác định.
