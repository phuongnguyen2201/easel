---
name: ai-image-gen
description: >-
  Sinh ảnh AI mọi chủ đề: chữ thành ảnh, ảnh thành ảnh, biến thể ảnh qua API tương thích OpenAI
  hay API bất đồng bộ apimart, người dùng tự có API key. Dùng khi người dùng nói "tạo ảnh AI", "vẽ
  giúp tôi một tấm", "sinh ảnh minh hoạ", "sửa ảnh bằng AI". Ảnh sản phẩm e-com →
  ecom-details-image.
layer: produce
---

# ai-image-gen Skill

> Sinh ảnh AI đa dụng: chữ thành ảnh / ảnh thành ảnh / biến thể ảnh. Người dùng tự có API key sinh ảnh (OpenAI tương thích hoặc apimart bất đồng bộ), sản phẩm ghi vào `outputs/`.

Gọi script dùng chung `skills/shared/scripts/ai_image.py` (thuần thư viện chuẩn, không phụ thuộc bên thứ ba).
SKILL này không hỏi xin, không in lại, không ghi, không commit bất kỳ API key thật nào -- key chỉ nằm trong `.env` của chính người dùng.

## Ranh giới (phân biệt với các SKILL lân cận)

- **ai-image-gen (SKILL này)**: sinh ảnh AI đa dụng, mọi đề tài, chữ thành ảnh / ảnh thành ảnh / biến thể.
- **ecom-details-image**: chuyên xuất ảnh trang chi tiết e-com / ảnh chính của sản phẩm (25 mẫu bối cảnh, chuỗi PDP). Cần ảnh sản phẩm e-com thì dùng nó.
- **card-\* / poster-\***: chụp ảnh render HTML+CSS (thẻ câu đắt, thẻ Xiaohongshu, poster), **không phải sinh bằng AI**, là xuất ảnh thiết kế tất định.
- **image-editing**: xử lý tất định ảnh có sẵn (đổi kích thước/cắt/đóng watermark/nén), không sinh khung hình mới.

## Cấu hình (bắt buộc đọc trước khi chạy)

> **Luật sắt về đường dẫn kiểm tra cấu hình**: trước hết `cd` tới thư mục gốc dự án Easel ghi ở cuối `AGENTS.md`, xác nhận thư mục hiện tại có `.env` và `skills/shared/scripts/ai_image.py`, rồi mới chạy các lệnh dưới. Không được kiểm tra bằng `./shared/scripts/...` trong workspace OpenClaw, cũng không được dùng `env` / `printenv` thay cho việc đọc `.env` của dự án; nếu không sẽ báo nhầm `IMG_BASE_URL`/Key đã cấu hình thành thiếu.

Cần đặt ba mục trong `.env` ở thư mục gốc dự án (script tự dò ngược lên từ thư mục hiện tại để tìm `.env`):

| Biến | Mô tả | Tên thay thế tương thích |
|---|---|---|
| `IMG_BASE_URL` | Địa chỉ gốc của API | `OPENAI_BASE_URL` / `OPENAI_API_BASE` / `BASE_URL` |
| `IMG_MODEL` | Tên model ảnh | `OPENAI_IMAGE_MODEL` / `IMAGE_MODEL` / `OPENAI_MODEL` |
| `IMG_API_KEY` | API key | `OPENAI_API_KEY` / `API_KEY` |

Hỗ trợ hai loại dịch vụ, script tự nhận diện theo `base_url` (cũng có thể ép bằng `--mode sync|async`):

- **OpenAI tương thích (đồng bộ)**: `base_url` không chứa apimart. Đi qua `/images/generations`, `/images/edits`, `/images/variations`.
  Ví dụ: `IMG_BASE_URL=https://api.openai.com/v1`, `IMG_MODEL=gpt-image-1`.
- **apimart (bất đồng bộ, poll)**: `base_url` có chứa `apimart`. Gửi tác vụ -> poll `/tasks/<id>` -> tải về.
  Ví dụ: `IMG_BASE_URL=https://api.apimart.ai/v1`.

## Các bước thực hiện

### 1. Xác nhận cấu hình trước (offline, không gửi request)

```bash
python skills/shared/scripts/ai_image.py check
```

In trạng thái ba mục cấu hình (key hiển thị dạng che), tên thay thế trúng được và chế độ tự nhận diện. Thiếu mục nào thì đưa ví dụ điền `.env` rồi kết thúc với mã thoát 2. **Cấu hình chưa sẵn sàng thì không đi tiếp**, nói thẳng cho người dùng thiếu gì và cấu hình thế nào.

### 2. Chữ thành ảnh text2img

Trước hết viết nhu cầu của người dùng thành một Prompt ảnh rõ ràng (chủ thể + phong cách + bố cục + ánh sáng + chất lượng), rồi chạy:

```bash
python skills/shared/scripts/ai_image.py text2img \
  --prompt "một chú chó Shiba đeo kính râm, phong cách minh hoạ phẳng, nền màu tương phản rực rỡ, nhiều chi tiết" \
  --size 1024x1024 --n 1 \
  --output "outputs/<chủ đề>/ai-image"
```

- `--size`: chế độ đồng bộ dùng pixel (`1024x1024` / `1536x1024` / `1024x1536`...); chế độ bất đồng bộ dùng tỉ lệ (`1:1` / `16:9` / `9:16`...).
- `--n`: số ảnh sinh ra (nhiều ảnh thì tự đánh số theo thứ tự).
- `--output`: thư mục (nhiều ảnh tự đánh số) hoặc một file có đuôi mở rộng; tất cả đặt trong `outputs/<chủ đề>/`.
- Đồng bộ có thể thêm `--quality low|medium|high`; bất đồng bộ có thể thêm `--resolution 1k|2k|4k`.

### 3. Ảnh thành ảnh / chỉnh ảnh img2img

Dựa trên một ảnh đầu vào + câu lệnh để sinh ảnh mới (OpenAI đi `/images/edits` multipart, tuỳ chọn `--mask` để sửa cục bộ; apimart lấy ảnh đầu vào làm ảnh tham chiếu rồi đi endpoint sinh ảnh):

```bash
python skills/shared/scripts/ai_image.py img2img \
  --prompt "đổi nền thành phố đêm đèn neon, giữ nguyên chủ thể" \
  --image path/to/input.png \
  --output "outputs/<chủ đề>/edited.png"
```

### 4. Biến thể ảnh variations

Từ một ảnh sinh ra nhiều biến thể:

```bash
python skills/shared/scripts/ai_image.py variations \
  --image path/to/input.png --n 3 \
  --output "outputs/<chủ đề>/variations"
```

### 5. Bàn giao

Báo cho người dùng đường dẫn sản phẩm và tham số sinh ảnh (chế độ/model/kích thước/số lượng). Nếu cần đổi kích thước/đóng watermark/nén nữa thì chuyển sang `image-editing`.

## Sản phẩm

Xuất thống nhất vào `outputs/<chủ đề>/`. Script tự tạo thư mục, nhiều ảnh đặt tên theo timestamp + số thứ tự.

## Nhận biết Profile

Khi có Profile của kênh (`=== EASEL ACCOUNT PROFILE ===`), hãy đưa phong cách hình ảnh thương hiệu (bảng màu / tông điệu / yếu tố ưa dùng) vào Prompt để giữ bộ ảnh đồng nhất; không có Profile thì sinh ảnh theo mô tả của người dùng.

## Câu hỏi thường gặp

- **Thiếu key / thiếu cấu hình**: `check` sẽ chỉ rõ thiếu mục nào kèm ví dụ `.env`; thông báo lỗi dễ hiểu, không ném traceback.
- **Dùng sai định dạng kích thước giữa đồng bộ và bất đồng bộ**: đồng bộ dùng pixel, bất đồng bộ dùng tỉ lệ. Dùng `--mode` để ép chế độ.
- **Không được ghi key thật vào bất kỳ sản phẩm nào hay commit lên repo**.
