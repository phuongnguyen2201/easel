---
name: xhs-note-creator
description: >-
  Sinh trọn bộ bài ảnh-chữ: tiêu đề, thân, caption, hashtag + 3-9 thẻ dọc hay phân cảnh video
  ngắn; có phân tích tư liệu, chấm điểm bán, kiểm chất lượng. Dùng khi người dùng nói "bài
  ảnh-chữ", "ra bộ thẻ", "seeding có ảnh". Chỉ render thẻ → card-xiaohongshu, văn bản chung →
  social-content.
layer: produce
---

# Tạo bài đăng ảnh-chữ

Từ một chủ đề + tư liệu tuỳ chọn, sinh ra **bộ thẻ ảnh-chữ** hoặc **kịch bản phân cảnh video ngắn**, xuất đúng quy chuẩn vào `outputs/`.

## Tư tưởng cốt lõi

Người xem bài ảnh-chữ không đọc bài dài, họ xem **bộ thẻ** hoặc **video ngắn**. Bản thảo bài dài chỉ là sản phẩm trung gian.

- **Bài ảnh-chữ**: 3-9 thẻ dọc 3:4 (cover + content x N + ending), mỗi thẻ <= 80 chữ
- **Bài video**: phân cảnh video dọc 15-90 giây + thẻ ảnh bìa

### 5 nguyên tắc làm bài viral

1. **Ưu tiên tư liệu thật**: ảnh chụp màn hình, ảnh so sánh > ảnh AI thuần
2. **Tập trung vào điểm bán cốt lõi**: xét ưu tiên theo công thức (độ hiếm x tính hữu dụng x mức cảm nhận được)
3. **Thị giác sang (đi qua card-design, đừng làm thẻ thô)**: hình ảnh thẻ **thống nhất đi qua hệ thống thiết kế [card-design](../card-design/SKILL.md)** (chọn phong cách rồi khoá spec, chữ to chữ mảnh, lấp đầy khung, cấm emoji cỡ lớn gây cảm giác rẻ tiền). Bài viết phải khẩu ngữ, có cảm giác thật, nhưng **hình ảnh thì không được thô** - muốn chất "người thường / sổ tay" thì chọn phong cách **sticker sổ tay / kem dịu dàng** của card-design (vẫn là HTML render chất lượng cao, không phải t2i thô với emoji cỡ lớn).
4. **Hướng vào điểm đau**: "giải quyết được vấn đề gì" > liệt kê một đống tính năng
5. **Lặp nhanh**: V1 (60 điểm) -> người dùng phản hồi -> V2 (70 điểm)

Phương pháp luận chi tiết: `references/xiaohongshu-viral-methodology.md`

## Quy trình

Thực hiện tuần tự, **không bỏ bước**.

### Step 0 - Intake (bắt buộc hỏi, hỏi gọn một lần)

1. **Chủ đề / người đọc mục tiêu / luận điểm cốt lõi**
2. **Dạng đầu ra**: ảnh-chữ hay video? (mặc định ảnh-chữ)
3. **Tư liệu**: có sẵn chữ/ảnh/video không?
4. **Phong cách**: phong cách thị giác lấy từ **thư viện phong cách của card-design** (9 kiểu: tối giản Thuỵ Sĩ / biên tập tạp chí / mực Á Đông hiện đại / kem dịu dàng / dopamine Y2K / đen vàng xa xỉ / sticker sổ tay / terminal geek / thực vật tươi mát) - tới Step 5A khi ra thẻ thì card-xiaohongshu sẽ dẫn chọn, ở đây chưa chốt.
5. **Số thẻ / độ dài video**: ảnh-chữ mặc định 5-7 thẻ; video mặc định 30-60 giây

### Step 0.5 - Phân tích điểm bán/điểm sáng (bắt buộc với bài quảng bá/chia sẻ/review)

1. Liệt kê mọi chức năng/đặc tính/điểm sáng
2. Cho người dùng chấm điểm từng ý:
   - Độ hiếm (1-5): người khác có không?
   - Tính hữu dụng (1-5): giải quyết vấn đề lớn cỡ nào?
   - Mức cảm nhận được (1-5): người dùng có thấy ngay không?
3. Điểm = độ hiếm x tính hữu dụng x mức cảm nhận được
4. Chọn Top 1-2 làm điểm bán cốt lõi

### Step 1 - Kiểm kê tư liệu (chỉ làm khi có tư liệu)

Nếu người dùng đưa tư liệu, chạy script sinh danh sách trước:

```bash
python3 skills/openclaw/xhs-note-creator/scripts/analyze_material.py <path>... \
  --out <work-dir>/reference/materials.json \
  --frames-dir <work-dir>/reference/frames
```

Thứ tự giá trị tư liệu: ảnh so sánh > demo chức năng > biểu đồ số liệu > tư liệu thương hiệu

### Step 2 - Thu thập tham khảo bên ngoài (bắt buộc với bài quan điểm/tin tức)

Làm theo `references/reference-search.md`, số liệu cốt lõi phải đối chiếu chéo từ >= 2 nguồn.

### Step 3 - Viết bản thảo bài dài (2000-4000 chữ)

Bắt đầu từ H2 (không viết H1), viết xong **đưa người dùng xác nhận** rồi mới đi tiếp.

### Step 4 - Khử mùi AI (bắt buộc)

Quy tắc khử mùi AI dùng thống nhất nguồn chuẩn text-polisher, SKILL này không giữ bản sao:

- Quy tắc tiếng Trung (gồm phần đặc thù: chất người thường trên Xiaohongshu / giọng bạn thân / nhịp emoji) -> `../text-polisher/references/zh-ai-markers.md`
- Cụm từ đệm phổ biến -> `../text-polisher/references/phrases-to-remove.md`
- Cấu trúc công thức -> `../text-polisher/references/structures-to-avoid.md`

Quét và viết lại đầy đủ theo 5 tầng nguyên tắc của nó, điểm chất lượng thang 50.

### Step 5 - Phân nhánh: ảnh-chữ hay video

#### 5A. Bài ảnh-chữ: tách thành 3-9 thẻ

- cover (thẻ 1) + content (ở giữa) + ending (thẻ cuối)
- Mỗi thẻ <= 80 chữ
- Mỗi thẻ chỉ nói một luận điểm
- Cả bộ giữ nguyên bảng màu/font/phong cách (bộ đã chọn ở card-design chạy xuyên suốt cả nhóm thẻ)

**Hình ảnh thẻ luôn đi qua pipeline chất lượng cao card-design, đừng dùng t2i thô hay thẻ kiểu người thường đầy emoji cỡ lớn.** Chia hai đường render theo việc có ảnh thật hay không (ghi chiến lược vào `meta.json`, tập giá trị khớp với `references/meta-schema.md`):

| Chiến lược | Dùng cho | Đường render |
|------|------|----------|
| `html_card` | Thẻ chữ thuần / thẻ khái niệm / thẻ số liệu (**mặc định, dùng nhiều nhất**) | **Đi qua [card-xiaohongshu](../card-xiaohongshu/SKILL.md)**: đọc [card-design](../card-design/SKILL.md) chọn phong cách rồi khoá spec -> viết HTML -> `render_card.py` ra ảnh -> `card_audit.py` chặn cứng |
| `text_on_photo` | Có ảnh thật + chữ hook (tư liệu thật là tốt nhất) | Pillow `scripts/text_on_image.py` (đường tư liệu thật của Xiaohongshu, giữ lại) |
| `collage` | Có 2-4 ảnh bổ trợ nhau | Pillow `scripts/collage_3x4.py` |

> Thẻ chữ thuần/khái niệm/số liệu **không còn đi qua t2i tự chuẩn bị** - thống nhất để card-xiaohongshu render, đảm bảo chất lượng thị giác; chỉ "thẻ ảnh thật" mới đi đường Pillow.

#### 5B. Bài video: viết kịch bản phân cảnh

- 6-12 phân cảnh, mỗi cảnh 2-8 giây
- Mỗi cảnh gồm: narration (<= 30 chữ), on_screen_text (<= 15 chữ), visual, material_ref
- Ra một thẻ cover làm ảnh bìa

### Step 6 - caption + hashtags + tiêu đề

**Tiêu đề**: chọn công thức tiêu đề từ nguồn chung `skills/shared/references/hook-title-formulas.md` (điểm đau + giải pháp / dạng câu hỏi / dạng phát hiện / từ khoá trend / đồng cảm danh tính...), ra 2-3 phương án.

**caption**: 100-300 chữ, mở bằng hook -> thông tin then chốt -> CTA, giọng bạn thân + ít emoji (điểm nhịp, không dùng như icon)

**hashtags**: 5-8 thẻ, 4 thẻ cốt lõi (từ khoá trend + chức năng cốt lõi + khác biệt + nhóm đối tượng) + 4 thẻ phụ trợ (bối cảnh + ngành hàng)

### Step 7 - Ghi xuống đĩa

```
outputs/<chủ đề>/{YYYY-MM-DD}/{tiêu đề ngắn}_{timestamp}/
├── {tiêu đề đầy đủ}.md   # bản thảo bài dài
├── meta.json             # metadata (thẻ/phân cảnh/caption/hashtags)
├── images/               # ảnh thẻ cuối / ảnh bìa
└── reference/            # materials.json / kết quả tìm kiếm
```

Tên thư mục chuẩn hoá bằng script: `python3 skills/openclaw/xhs-note-creator/scripts/normalize_slug.py "tiêu đề" --with-ts`

### Step 8 - Kiểm tra (bắt buộc, hai cửa)

**① Cửa văn bản/cấu trúc** (tiêu đề/caption/hashtag/số chữ và cấu trúc thẻ):

```bash
python3 skills/openclaw/xhs-note-creator/scripts/validate_meta.py "outputs/<chủ đề>/meta.json"
```

**② Cửa thị giác** (chỉ với đường `html_card`, chạy sau khi render; chặn cứng khoảng trắng chết/mật độ):

```bash
python skills/openclaw/card-design/scripts/card_audit.py audit -f "outputs/<chủ đề>/card_*.png"
```

Bất kỳ cửa nào thoát khác 0 -> sửa rồi chạy lại tới khi qua. Không bàn giao sản phẩm chưa kiểm.

## Những việc không được làm

- Không viết H1; tiêu đề chỉ đặt trong `meta.json.title`
- Không ghi nguồn tham khảo ở cuối thân bài
- Không để placeholder `[chèn ảnh]` trong file `.md`
- Không bỏ qua Step 4 (khử mùi AI) và Step 8 (validate)
- Không tự đặt tên thư mục bằng tay, luôn dùng `normalize_slug.py`

## Nhận biết Profile

- **Có Profile**: đọc mảng nội dung, khán giả mục tiêu, phong cách nội dung để canh giọng bài và chiến lược hashtag
- **Không có Profile**: hỏi thông tin cơ bản rồi xuất theo phong cách seeding phổ thông

## Phụ thuộc công cụ

- Python 3.8+, Pillow (bắt buộc, cho đường thẻ ảnh thật)
- playwright + chromium (render thẻ cho đường `html_card`, đi qua card-xiaohongshu; lần đầu chạy `pip install playwright && playwright install chromium`)

## Tài liệu tham khảo

- **Hình ảnh thẻ** -> [card-design](../card-design/SKILL.md) (hệ thống thiết kế/thư viện phong cách, đọc trước khi ra ảnh) + [card-xiaohongshu](../card-xiaohongshu/SKILL.md) (pipeline render HTML -> ảnh chụp)
- `references/xiaohongshu-viral-methodology.md` - phương pháp luận bài viết/điểm bán/tiêu đề/cảm xúc (phần thị giác đã giao cho card-design)
- Khử mùi AI -> `../text-polisher/references/zh-ai-markers.md` (nguồn chuẩn, có phần đặc thù Xiaohongshu)
- Hook/công thức tiêu đề -> `skills/shared/references/hook-title-formulas.md` (nguồn chung)
- `references/material-intake.md` - quy trình xử lý tư liệu
- `references/image-sourcing.md` - xử lý nguồn ảnh
- `references/meta-schema.md` - định nghĩa trường metadata
- `references/output-spec.md` - quy chuẩn thư mục đầu ra
