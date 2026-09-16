---
name: paper-explainer
description: >-
  Giải thích bài báo khoa học từ arXiv/PDF (công thức, hình): rút vấn đề, đóng góp, phương pháp,
  hình chính, kết luận → video giải thích hay bài ảnh-chữ. Dùng khi người dùng nói "giải thích
  paper", "tóm tắt bài báo", "paper ra video". video-to-article từ video, doc-convert chỉ đổi định
  dạng.
layer: produce
---

# Giải thích bài báo khoa học (paper → video / bài ảnh-chữ)

> Kể một bài báo thành video hoặc bài ảnh-chữ mà cả người thường lẫn dân trong ngành đều thích xem. Sản phẩm trung gian cốt lõi là một
> **asset library có cấu trúc** (parse + chắt lọc một lần, hai dây chuyền video và ảnh-chữ dùng chung, không gọi LLM lặp lại).
> IO tất định (kéo paper/parse PDF/dựng khung) chạy qua `scripts/paper_ingest.py`; **phần chắt lọc và kịch bản phân cảnh do bạn (LLM) làm** - đó là giá trị cốt lõi của SKILL này.

> Video sang bài ảnh-chữ (chiều ngược) xem **video-to-article**; chỉ đổi định dạng xem **doc-convert**;
> chỉ làm biểu đồ xem **chart-visualization / infographic**; đăng bài giao SKILL đăng của nền tảng đích (adapter VN, Giai đoạn 5).

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Bài báo | Có | arxiv id (2401.12345) / link arxiv / đường dẫn PDF cục bộ (không đưa thì hỏi) |
| Dạng đích | Không | Video (mặc định, Video Channels/Bilibili) / bài ảnh-chữ (Zhihu/WeChat OA) / cả hai |
| Khung hình video | Bắt buộc khi làm video | Khi người dùng hoặc task phía trên chưa nói rõ ngang/dọc (hoặc 16:9/9:16/độ phân giải cụ thể), phải hỏi lại và chờ xác nhận trước khi vào khâu dựng video; không được im lặng suy ra theo nền tảng, Profile hay giá trị mặc định, đã rõ rồi thì đừng hỏi lại |
| Độ sâu cho khán giả | Không | Phổ thông đại chúng (mặc định) / dành cho dân trong ngành (chuyên sâu hơn) |
| Thời lượng | Không | Video mặc định 2-4 phút (video dài trung bình trên Video Channels) |

## Cấu trúc sản phẩm (`outputs/<chủ đề>/`)

```
article.md               bản ảnh-chữ (Zhihu/WeChat OA)
final.mp4                video hoàn chỉnh
assets/                  paper.pdf / parsed/ / asset-library.json / script.md
  slide-plan.json        phân trang có cấu trúc (đầu vào duy nhất của trang, tách lời nói và chữ trên màn hình)
  slides/                PNG + HTML từng trang render ổn định + audit report
  slides-contact-sheet.jpg  ảnh soát lại toàn bộ bộ visual
```

Script (tương đối so với gốc dự án): `paper_ingest.py` (parse) + `render_slides.py` (kiểm tra phân trang/render/audit).

## Các bước thực hiện

### 1. Lấy bản gốc + parse

1. **Tự kiểm môi trường**: `python skills/openclaw/paper-explainer/scripts/paper_ingest.py check`
   (xem pdfplumber / MinerU token / proxy; thiếu pdfplumber thì `pip install pdfplumber`).
2. **Kéo bài báo**: `paper_ingest.py fetch --paper <id/url/pdf> -o "outputs/<chủ đề>/assets/paper.pdf"`.
3. **Parse**: `paper_ingest.py parse -i "outputs/<chủ đề>/assets/paper.pdf" -o "outputs/<chủ đề>/assets/parsed/"`
   (có `MINERU_API_TOKEN` thì đi MinerU, có cấu trúc công thức/biểu đồ; không thì pdfplumber text thuần + cố gắng trích hình).

### 2. Chắt lọc có cấu trúc (bạn làm, phần cốt lõi)

4. Sinh khung: `paper_ingest.py skeleton -o "outputs/<chủ đề>/assets/asset-library.json"`.
5. Đọc `assets/parsed/content.*`, theo `references/paper-distill-schema.md` điền đầy `assets/asset-library.json`:
   `one_liner` (một câu nói rõ paper làm được gì), `problem`/`prior_gap`, `contributions` (tối đa 3 ý),
   `method` (kèm **phép so sánh dễ hiểu** analogy), `key_figures` (chọn 2-4 hình then chốt, mỗi hình viết `plain` giải thích bằng lời thường),
   `results` (kèm số liệu then chốt), `limitations`, `takeaway`, `terms` (bảng thuật ngữ bình dân).
   **Cách diễn giải bình dân** xem `references/explain-methodology.md` (công thức/biểu đồ → lời thường, phép so sánh, tránh chất đống thuật ngữ).
6. **Trung thành với bản gốc**: không thổi phồng, không bịa kết luận; chỗ nào chưa chắc thì ghi chú rõ, đừng đoán bừa (nội dung học thuật sai sẽ bị dân trong ngành bắt lỗi).

### 3A. Dây chuyền video (Video Channels/Bilibili)

7. **Kịch bản phân cảnh**: theo cấu trúc trong `references/video-storyboard.md` (hook → vấn đề → hạn chế hiện có → đóng góp → một hình nói rõ phương pháp → kết quả → ý nghĩa), viết asset-library thành `assets/script.md`.
   Phân cảnh/giữ chân/nhịp video nói **dùng lại phương pháp của video-script** (nạp ngữ cảnh bài báo). Có thể chọn **video nói hai người hỏi đáp** (người dẫn hỏi + người giảng đáp) bắt tai hơn lời dẫn một người - khi dùng hai người thì viết lời nói thành `lines.json` từng dòng (`{speaker,text,emotion}`, speaker=người giảng/người hỏi).
8. **Kiểm kê tư liệu visual + chọn hình**: trước hết liệt kê vai trò visual của từng trang (hình bằng chứng/hình vẽ lại/nét phác khái niệm/typography/motif), rồi mới viết slide-plan. Hình gốc của bài báo lấy từ `assets/parsed/figures/`; hình gốc phức tạp thì cắt lấy vùng then chốt, sơ đồ phương pháp/hình kết quả vẽ lại bằng **infographic / chart-visualization**. Trang bìa/trang khái niệm thiếu hình thì chủ động tìm hoặc làm nét phác, hình cắt cận hay ký hiệu liên quan trực tiếp tới chủ đề, đừng lấy robot/blob ngẫu nhiên lấp chỗ. Chữ trong hình mà không đọc nổi ở độ phân giải đích thì không được dùng thẳng.
9. **Dây chuyền slide ổn định (bắt buộc, không được viết script make_slides tạm trong outputs)**: đọc trước nguyên tắc thiết kế của [card-design](../card-design/SKILL.md) và `references/slide-design.md`, rồi viết script thành `assets/slide-plan.json`. Ghi nguyên văn ý đồ phong cách gốc của người dùng/Profile/ảnh tham chiếu vào `style`, sau đó chọn riêng `base_style`, `treatment`, `theme`, `motif` và tư liệu visual để hiện thực hoá; không được ép phong cách của người dùng vào một preset có sẵn, cũng không được từ chối chỉ vì không có preset trùng tên. Thứ cần chuyển sang là đặc điểm quan sát được (không khí, phối màu, nét, chất liệu, bố cục, tư liệu nhân vật/vật thể), không phải liệt kê tên phong cách. Chưa chỉ định phong cách thì dùng `editorial`, nhưng mặc định cũng phải có lưới biên tập rõ ràng, lớp giấy, mốc neo chương mục và cách đóng khung ảnh, không được giao "nền trơn + chữ". Cả bộ khoá vào một lập trường thiết kế, khung xương trang và cổng audit giữ ổn định. Chạy:
   ```bash
   python skills/openclaw/paper-explainer/scripts/render_slides.py validate --plan "outputs/<chủ đề>/assets/slide-plan.json"
   python skills/openclaw/paper-explainer/scripts/render_slides.py render --plan "outputs/<chủ đề>/assets/slide-plan.json" --out-dir "outputs/<chủ đề>/assets/slides"
   python skills/openclaw/paper-explainer/scripts/render_slides.py audit --plan "outputs/<chủ đề>/assets/slide-plan.json" --slides-dir "outputs/<chủ đề>/assets/slides" --contact-sheet "outputs/<chủ đề>/assets/slides-contact-sheet.jpg"
   ```
   Bất kỳ lần thoát khác 0 nào cũng phải sửa plan rồi render lại; `validate` sẽ theo chức năng từng trang mà chặn các trang nghèo thông tin kiểu "chỉ có khẩu hiệu, thiếu giải thích", đồng thời kiểm tra độ tương phản của mọi màu chữ thân bài trên nền thực tế sau khi gộp theme; accent sáng vẫn dùng để trang trí được, còn chữ sẽ lấy màu nền trước ngữ nghĩa đủ đọc. `render` chặn cứng chữ/phần tử tràn khung, chồng nhau, lệch hàng trong nhóm, chữ trong thẻ trôi lề trái và trang cấu trúc rỗng quá mức. Sau khi mọi script đều qua, Agent hiện tại **bắt buộc nhìn tận mắt contact sheet và ít nhất 3 slide ở kích thước gốc**, kiểm tra khi tạm dừng/tắt tiếng thì trang có tự đọc hiểu được không, hình bài báo có đọc nổi không, chữ có thẳng hàng với phần tử của nó không, khoảng trắng có vai trò kể chuyện không, tư liệu visual có liên quan không, nhịp có bị lặp không; qua script không đồng nghĩa với đạt. Đừng bê nguyên đoạn narration lên màn hình. Chỉ khi chính hình bài báo mang thông tin chính thì mới được đặt `density: visual` cho trang đó, không được coi nó là công tắc để bỏ qua khâu chắt lọc nội dung.
10. **Ra video (lồng tiếng + phụ đề + ghép, thiếu một thứ là hỏng)**: từ narration trong slide-plan sinh lời nói - một người dùng **tts-voiceover**, hai người dùng **multi-voice-dubbing**; đồng bộ SRT, thiếu thì chạy **auto-subtitle**. Ghi `assets/slides/slide_*.png`, tiếng lồng và phụ đề vào storyboard của auto-short-video rồi ghép, bắt buộc đặt `"image_motion": "static"` ở cấp cao nhất; slide/biểu đồ cấm Ken Burns, không được zoom, pan hay cắt mất rìa. Thời gian dừng mỗi trang bám theo đoạn audio/phụ đề narration tương ứng, không chia đều cả track. Không được chỉ giao ảnh tĩnh hay video không tiếng.
11. Dùng `manifest.py meta` đăng ký `final.mp4` hoặc `article.md` là deliverable; phần parse trung gian, slide và audio chỉ để trong `assets/`.
12. **Đăng bài**: giao SKILL đăng của nền tảng đích (adapter VN, Giai đoạn 5).

### 3B. Dây chuyền ảnh-chữ (Zhihu/WeChat OA)

13. Dùng **cùng một asset-library** để viết `article.md`: tiêu đề (hook) + nói rõ bằng lời thường problem → method → results → takeaway, kèm hình trong `assets/`.
    Thích ứng nền tảng xem `references/platform-adapt.md` (chuỗi logic kiểu Zhihu, mạch mở - thân - chuyển - kết kiểu WeChat OA). Dàn trang/ảnh dài giao **doc-convert**; đăng bài giao SKILL đăng của nền tảng đích.

## Nhận biết Profile

- **Có Profile**: `platforms.md` chốt nền tảng chính và gợi ý dạng/khung hình/thời lượng, nhưng khung hình video vẫn phải để người dùng xác nhận; `audience.md` chốt độ sâu cho khán giả (đại chúng vs dân trong ngành); `style.md` chốt giọng giảng giải; `identity.md` chốt ngách lĩnh vực (AI/sinh học/vật liệu... ảnh hưởng tới nguồn lấy phép so sánh).
- **Không có Profile**: mặc định video dài trung bình 2-4 phút, độ sâu phổ thông đại chúng, hỏi trước lĩnh vực và khán giả.

## Quy tắc

1. **Trung thành với bản gốc**: không thổi phồng đóng góp, không bịa số liệu/kết luận; thuật ngữ chưa chắc thì tra lại bản gốc, đừng đoán bừa.
2. **Chắt lọc một lần, dùng lại hai nơi**: asset-library.json là nguồn sự thật duy nhất, cả video lẫn bài ảnh-chữ đều xuất phát từ đó, tránh chắt lọc lặp và lệch cách diễn đạt.
3. **Dễ hiểu nhưng không sai lệch**: dùng phép so sánh để hạ ngưỡng, nhưng so sánh không được bóp méo ý gốc; thuật ngữ then chốt phải có một câu giải thích bình dân chứ không né tránh.
4. **Ưu tiên hình**: bài báo dựa vào hình để nói phương pháp/kết quả, video/bài ảnh-chữ cố gắng dùng hình (hình gốc hoặc infographic vẽ lại) để tải thông tin.
5. **Cố ý không làm**: bài giảng bằng người ảo (quá nặng), phụ thuộc mã nguồn LaTeX (vào từ PDF thì phủ rộng hơn).
6. **Trang không phải bản lời nói, cũng không phải bảng khẩu hiệu**: mỗi trang một kết luận trung tâm, nhưng phải có giải thích, bằng chứng hoặc cách nêu số liệu để trang tự đọc hiểu được khi tạm dừng/tắt tiếng; chi tiết để dành cho narration, không được thu nhỏ cỡ chữ để nhét quá nhiều chữ.

## Nguồn tham khảo

Xem `EASEL-META.md`. Quy trình đúc kết từ QuZhan51496/paper2anything (bản thân nó là Claude Skills: parse_pdf/MinerU + phương pháp chắt lọc tách ra references + fan-out nhiều dạng),
showlab/Paper2Video (cắt đoạn theo khối nội dung, phụ đề đi trước), Paper2Poster (sản phẩm trung gian asset library có cấu trúc),
Azzedde/paper_to_podcast (video nói hai người hỏi đáp), OpenDCAI/Paper2Any (parse một lần, fan-out nhiều dạng).
