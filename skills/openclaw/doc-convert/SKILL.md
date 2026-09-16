---
name: doc-convert
description: >-
  Dàn trang và chuyển Markdown thành HTML, PDF in được hoặc ảnh dài PNG để lưu trữ, gửi đi hay
  đăng nơi không hỗ trợ Markdown. Dùng khi người dùng nói "chuyển Markdown sang PDF", "xuất bài
  thành ảnh dài", "MD sang HTML", "dàn trang MD". Chỉ Markdown, không DOCX/PPT; sơ đồ tư duy →
  mindmap.
layer: produce
---

# Chuyển đổi định dạng / dàn trang Markdown

> Dàn trang Markdown thành HTML / PDF / ảnh dài PNG. Chạy qua `skills/shared/scripts/doc_convert.py`
> (python-markdown lo dàn trang + Chromium in/chụp màn hình).

> Sơ đồ tư duy: xem mindmap; dàn trang riêng theo nền tảng: xem SKILL đăng tương ứng; card/poster: xem card-*/poster-hero.

## Đầu vào / đầu ra

- Đầu vào: file Markdown (hỗ trợ tiêu đề, danh sách, bảng, khối mã, trích dẫn, hình ảnh...).
- Đầu ra (`outputs/<chủ đề>/`): theo đuôi file `.html` / `.pdf` / `.png` (ảnh dài).

## Thực thi

Đường dẫn script (tương đối gốc dự án): `skills/shared/scripts/doc_convert.py` (`convert -h`).

```bash
# Chuyển sang HTML sạch (dàn trang dễ đọc + font CJK)
python skills/shared/scripts/doc_convert.py convert -i article.md -o "outputs/<chủ đề>/a.html"

# Chuyển sang PDF (khổ A4 in được, hợp để lưu trữ/gửi đi)
python skills/shared/scripts/doc_convert.py convert -i article.md -o "outputs/<chủ đề>/a.pdf"

# Chuyển sang ảnh dài PNG (hợp để đăng nơi không hỗ trợ MD / lưu lại story)
python skills/shared/scripts/doc_convert.py convert -i article.md -o "outputs/<chủ đề>/a.png" --width 800
```

## Yêu cầu trước

- MD sang HTML: cần `pip install markdown`.
- MD sang PDF/PNG: cần playwright + chromium (`playwright install chromium`).

## Quy tắc

1. Chiều rộng ảnh dài `--width` chỉnh theo nền tảng (story/feed, Xiaohongshu ~750-1080); chiều rộng phần thân `--page-width` kiểm soát vùng chữ của HTML/PDF.
2. Ảnh dùng đường dẫn tương đối/tuyệt đối truy cập được, lúc render phải tải lên được.
3. Cần DOCX/PPT hoặc dàn trang tương tác phức tạp thì SKILL này không làm (gợi ý dùng pandoc hoặc công cụ của nền tảng tương ứng).
4. Sản phẩm đều đưa vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

python-markdown (kèm các extension extra/tables/fenced_code/toc) lo phần MD sang HTML, Chromium headless
dùng `page.pdf()`/`screenshot(full_page)` xuất PDF/ảnh dài, thay pandoc cho các nhu cầu dàn trang và phân phối MD thông dụng nhất.
