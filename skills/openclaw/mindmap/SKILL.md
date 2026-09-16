---
name: mindmap
description: >-
  Render dàn ý Markdown thành sơ đồ tư duy HTML tương tác (markmap), tuỳ chọn xuất PNG (Chromium);
  hợp cấu trúc kiến thức, khung nội dung, SWOT. Dùng khi người dùng nói "sơ đồ tư duy", "mindmap",
  "sơ đồ cây", "vẽ sơ đồ ý chính". Biểu đồ số liệu/infographic → chart-visualization/infographic.
layer: produce
---

# Sơ đồ tư duy (Markdown -> mindmap)

> Render dàn ý Markdown thành HTML sơ đồ tư duy tương tác, tuỳ chọn xuất PNG. Chạy qua `skills/shared/scripts/mindmap.py`
> (markmap).

> Biểu đồ số liệu xem chart-visualization; infographic/sơ đồ quy trình xem infographic; SKILL này chuyên làm **mindmap dàn ý phân cấp**.

## Đầu vào

Dàn ý Markdown (dùng tiêu đề `#`/`##`/`###` để phân cấp, danh sách `-` là nút lá):
```markdown
# Chủ đề trung tâm
## Nhánh một
- Ý chính A
- Ý chính B
## Nhánh hai
- Ý chính C
```

## Đầu ra (`outputs/<chủ đề>/`)

- HTML sơ đồ tư duy (một file duy nhất; markmap JS lấy từ CDN, có mạng thì bung/gập được, mở offline thì không tương tác)
- Ảnh PNG tuỳ chọn (`--png`)

## Thực thi

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/mindmap.py` (`make -h`).

```bash
# Trước hết sắp nội dung thành dàn ý Markdown (bạn làm), lưu thành outline.md, rồi:
python skills/shared/scripts/mindmap.py make -i outline.md \
  -o "outputs/<chủ đề>/mm.html" --png
```
`-i -` đọc được từ stdin; `--title` tự đặt tiêu đề; `--bg` màu nền.

## Điểm mấu chốt khi dùng

1. **Trước hết tổ chức nội dung thành dàn ý Markdown rõ ràng** (phân cấp mạch lạc, mỗi nút thật ngắn) - đây là chìa khoá chất lượng mindmap,
   do bạn (LLM) làm: từ bài viết/chủ đề rút ra trung tâm -> nhánh -> ý chính.
2. Nên để 2-4 cấp, chữ trong nút cô đọng (vài chữ), đừng nhét cả câu dài vào một nút.
3. HTML tương tác được (bung/gập, phóng to thu nhỏ), hợp để chia sẻ hoặc nhúng; PNG hợp để đăng ảnh trực tiếp.

## Điều kiện trước (PNG)

Render PNG cần playwright + chromium + mạng ngoài (markmap JS lấy từ CDN). Chỉ cần HTML thì không phụ thuộc gì thêm.

## Quy tắc

1. Nội dung phải thành dàn ý Markdown rồi mới render, đừng ném thẳng bài dài không có cấu trúc vào.
2. Nút gọn; đừng phân cấp quá sâu (quá 4 cấp là khó đọc).
3. Sản phẩm đều nằm trong `outputs/<chủ đề>/`.

## Nguồn tham khảo

markmap (Markdown -> sơ đồ tư duy tương tác) là giải pháp mã nguồn mở chuẩn mực; SKILL này sinh HTML tự chứa (nạp
markmap qua CDN), và dùng Chromium headless render để xuất PNG.
