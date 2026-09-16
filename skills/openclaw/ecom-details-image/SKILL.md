---
name: ecom-details-image
description: >-
  Lập phương án ảnh sản phẩm thương mại điện tử: ý tưởng ảnh chính, ảnh bối cảnh, hướng ảnh trang
  chi tiết và Prompt sinh ảnh AI. Dùng khi người dùng nói "ảnh chính sản phẩm", "ảnh trang chi
  tiết", "phương án ảnh bán hàng". Chỉ lập kế hoạch; tách nền → remove-bg, sinh ảnh →
  ai-image-gen.
layer: produce
---

# ecom-details-image Skill

Dùng Skill này khi người dùng cần chiến lược hình ảnh, Prompt ảnh, ảnh chính sản phẩm, ảnh marketing, ảnh mạng xã hội, ảnh quảng cáo, visual PDP thương mại điện tử, hoặc yêu cầu sinh ảnh AI trực tiếp.

Hai chế độ:

1. **Chế độ Brief / Prompt**: chỉ xuất brief hình ảnh và Prompt ảnh chạy được.
2. **Chế độ Generate**: khi người dùng yêu cầu rõ "sinh ảnh, tạo ảnh, ra ảnh, render image", xuất Prompt cuối trước, rồi gọi `scripts/generate_image.py`.

> **Đồng bộ hướng thẩm mỹ với [card-design](../card-design/SKILL.md)**: ảnh infographic trang chi tiết / ảnh marketing theo cùng một bộ nguyên tắc khử cảm giác AI rẻ tiền - cấm gradient xanh tím kiểu công nghệ, cấm dùng emoji làm icon, chữ to nét mảnh, chừa khoảng trắng có tiết chế, lấp đầy chứ không để trống hoác. Viết các ràng buộc này vào phần thuận và phần phủ định của Prompt (SKILL này ra Prompt t2i, không render HTML, nên chỉ đồng bộ ở mức "hướng thẩm mỹ", không đi qua render_card).

Không để lộ, không hỏi xin, không ghi, không commit và không in lại API key thật. Người dùng phải tự cấu hình API bằng biến môi trường của mình.

## References (nạp khi cần, đừng đọc hết một lượt)

| File | Nội dung | Khi nào đọc |
|---|---|---|
| `references/templates.md` | Bảng khớp 25 mẫu bối cảnh, cách dùng, tra nhanh biến thể phong cách | Khi xác định loại bối cảnh và khớp mẫu |
| `references/templates/*.json` | Mẫu bối cảnh cụ thể (`prompt_template`/`variants`/`category_tips`/`anti_ai_tips`) | Chỉ đọc đúng cái đã khớp |
| `references/image-gen-rules.md` | Cấu trúc Prompt chung, luật thép text-to-image, nguyên tắc tinh gọn, mẹo Anti-AI, chặn điểm dễ hỏng | Khi viết từng Prompt |
| `references/campaign-style-lock.md` | Quy tắc Campaign Style Lock và mẫu mặc định cho task nhiều ảnh | Khi task có nhiều ảnh |
| `references/pdp-sequences.md` | Chẩn đoán động lực chuyển đổi, chuỗi ảnh chính/trang chi tiết, góc máy đa chiều, cấu trúc infographic trang chi tiết, phối font | Khi làm ảnh sản phẩm/trang chi tiết/PDP |

## Quy trình lõi

1. Xác định loại task hình ảnh và bối cảnh → đọc `references/templates.md` để khớp mẫu.
2. Từ `references/templates/` đọc **đúng một** file JSON đã khớp, lấy `prompt_template`, `variants`, `category_tips` làm cấu trúc nền cho Prompt.
3. Chỉ hỏi thêm thông tin còn thiếu mà thực sự ảnh hưởng tới kết quả ảnh (xem **Đầu vào tối thiểu** bên dưới).
4. Dựng brief hình ảnh.
5. Task nhiều ảnh: trước hết theo `references/campaign-style-lock.md` lập **Campaign Style Lock**, khoá bảng màu, tông nóng lạnh, font, nền, ánh sáng, bố cục và phong cách icon cho cả bộ ảnh.
6. Theo `references/image-gen-rules.md` viết Prompt ảnh chạy được (giữ gọn, đối chiếu từng luật thép); task nhiều ảnh bắt buộc chép nguyên đoạn Campaign Style Lock vào mọi Prompt.
7. Ảnh sản phẩm/trang chi tiết/ảnh marketing: theo `references/pdp-sequences.md` chẩn đoán động lực chuyển đổi trước, rồi mới xếp chuỗi ảnh.
8. Khi người dùng yêu cầu trang chi tiết thương mại điện tử / PDP / bộ ảnh chính / trọn bộ ảnh sản phẩm, mặc định xuất gói **5 ảnh chính + 7-9 ảnh trang chi tiết** (mỗi màn trang chi tiết bắt buộc theo định dạng infographic thương mại điện tử, xem `references/pdp-sequences.md`).
9. Người dùng yêu cầu ra ảnh ngay → gọi `scripts/generate_image.py`; khi người dùng đưa ảnh sản phẩm tham chiếu thì truyền `--image`.
10. Trả về Prompt, đường dẫn file đã sinh và các giả định quan trọng.

## Đầu vào tối thiểu

Mọi task hình ảnh đều ưu tiên xác nhận: mục tiêu, mục đích dùng (ảnh chính/ảnh quảng cáo/ảnh mạng xã hội/Banner/module PDP/thumbnail...), chủ thể, khán giả và ngữ cảnh, phong cách, bố cục và tỉ lệ, có cần chữ trong ảnh không, ràng buộc phủ định. Thiếu trường không quan trọng thì nêu rõ giả định rồi làm tiếp, đừng chặn vô ích.

## Gọi script sinh ảnh (scripts/generate_image.py)

Sinh ảnh trực tiếp đi qua API tạo ảnh của apimart.ai (model do `IMG_MODEL` chỉ định, model-agnostic, polling bất đồng bộ); cũng có thể chuyển sang skill cổng sinh ảnh chung `ai-image-gen`. Ưu tiên đặt `.env` trong `.claude/skills/ecom-details-image/`, đừng ghi API key thật vào repo:

```dotenv
IMG_BASE_URL=https://api.apimart.ai/v1
IMG_MODEL=gpt-image-2
IMG_API_KEY=your-api-key
```

Script chấp nhận các alias: `OPENAI_BASE_URL`, `OPENAI_API_BASE`, `OPENAI_IMAGE_MODEL`, `OPENAI_MODEL`, `OPENAI_API_KEY`.

Dạng lệnh gọi:

```bash
python3 skills/openclaw/ecom-details-image/scripts/generate_image.py --prompt "..." --size 1:1 --resolution 2k
python3 skills/openclaw/ecom-details-image/scripts/generate_image.py --prompt-file prompt.txt --output-dir outputs
python3 skills/openclaw/ecom-details-image/scripts/generate_image.py --env-file .env --image product.jpg --prompt-file prompt.txt
```

Tham số: `--prompt` / `--prompt-file`; `--output-dir` (chỉ dùng khi người dùng chỉ định, nếu không thì `generated-images/`); `--size` (dạng tỉ lệ, 14 kiểu, ví dụ `1:1`/`16:9`/`2:3`/`4:5`, mặc định `1:1`); `--resolution` (`1k`/`2k`/`4k`, mặc định `2k`, 4K chỉ áp dụng cho 6 tỉ lệ khổ rộng); `--image` (đường dẫn ảnh sản phẩm tham chiếu, rất hiệu quả để giữ đúng ngoại hình sản phẩm); `--poll-interval` (mặc định `5`); `--timeout` (mặc định `180`); `--format` (mặc định `png`).

Quy tắc sinh ảnh:

1. Xuất Prompt cuối trước, rồi mới gọi script. Prompt ngắn dùng `--prompt`, Prompt dài dùng `--prompt-file`.
2. Chọn `--size` theo nền tảng, không có yêu cầu thì mặc định `1:1`.
3. Thiếu cấu hình như `IMG_API_KEY` thì **không gọi script**, chỉ xuất trọn gói Prompt cùng ví dụ lệnh cấu hình, nói rõ cần khai báo gì trong `.env`, để người dùng tự chạy.
4. Nếu API hoặc model không hỗ trợ một kích thước nào đó, đổi sang kích thước được hỗ trợ gần nhất và nói rõ.

## Kiểm tra QA (xác nhận từng mục trước khi xuất)

- Prompt đúng mục tiêu thật của người dùng, đã khớp đúng mẫu bối cảnh và ráp dựa trên `prompt_template` của mẫu đó.
- Prompt gọn, chỉ giữ thông tin cốt lõi, rõ chủ thể/bố cục/phong cách/mục đích dùng.
- Task sản phẩm hoặc marketing có chẩn đoán động lực chuyển đổi; thiếu bằng chứng thì không bịa công dụng, chứng nhận, số liệu, điểm đánh giá, doanh số, nhận xét hay giấy uỷ quyền.
- Đã áp dụng luật thép text-to-image: mã màu hex, tỉ lệ bằng số, khoảng trắng nêu rõ, danh sách phủ định, chừa chỗ cho giao diện nền tảng (chi tiết xem `references/image-gen-rules.md`).
- Bối cảnh UGC/livestream/mạng xã hội đã áp dụng mẹo anti-AI (trường `anti_ai_tips` của mẫu).
- Task nhiều ảnh: mỗi ảnh mở đầu bằng cùng một đoạn Campaign Style Lock; đã phân bổ góc máy và cỡ cảnh khác nhau, không có 3 ảnh liên tiếp cùng góc, ảnh toàn cảnh chiếm không quá 40%.
- **Ảnh trang chi tiết bắt buộc theo định dạng infographic thương mại điện tử** (có tiêu đề, icon, nhãn, lợi ích, bước làm hoặc huy hiệu tin cậy), mỗi Prompt trang chi tiết mở đầu bằng `E-commerce infographic`, không phải chỉ là ảnh sản phẩm chụp nhiều góc.
- Chữ trong ảnh ngắn và cần thiết; có ảnh tham chiếu của người dùng thì đã truyền `--image`; ràng buộc phủ định bao được các lỗi thường gặp.
- Trong output và trong file không có API key hay thông tin xác thực riêng tư.
- Nhắc người dùng sau khi ra ảnh hãy phóng to 200% soát lại từng chữ, nhất là dấu tiếng Việt.

## Định dạng output

Chế độ Brief / Prompt trả về:

1. **Mẫu đã khớp** (tên file mẫu + loại bối cảnh)
2. **Visual Brief**
3. **Final Image Prompt**
4. **Negative Constraints**
5. **Assumptions**

Task sản phẩm hoặc marketing bổ sung: **Conversion Driver Diagnosis**, **Campaign Style Lock** (khi nhiều ảnh), **Hero Image Sequence** (ghi rõ từng ảnh theo mẫu nào), **PDP Detail Image Sequence** (khi đụng tới trang chi tiết/PDP/trọn bộ ảnh sản phẩm), **Copy Lines** (khi cần chữ), **Test Priorities**.

Chế độ Generate trả về:

1. **Mẫu đã khớp** (tên file mẫu + loại bối cảnh)
2. **Final Image Prompt**
3. **Campaign Style Lock** (task nhiều ảnh bắt buộc trả về)
4. **Image Pack Plan** (số thứ tự, mục đích, kích thước, mẫu tương ứng và câu chữ ngắn của từng ảnh)
5. **Generated Files**
6. **Assumptions / Notes**
