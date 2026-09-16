---
name: text-condenser
description: >-
  Cắt/tóm tắt văn bản về số chữ chỉ định, giữ ý cốt lõi, 3 chế độ: cắt cứng (đúng số chữ), tóm tắt
  (giữ ý), trích câu đắt; ra bản ngắn vừa giới hạn nền tảng. Dùng khi người dùng nói "cắt còn 200
  chữ", "dài quá", "rút gọn", "tóm tắt", "lọc ý chính". text-polisher trau chuốt không đổi độ dài.
layer: produce
---

# Cắt chữ / tóm tắt

> Nén văn bản dài về số chữ chỉ định, giữ thông tin cốt lõi, khớp giới hạn độ dài của từng nền tảng.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| `text` | Có | Bản gốc cần nén |
| `target_length` | Không | Số chữ đích (ví dụ `140`, `280`, `500`); không chỉ định thì tự nén còn 30%-50% bản gốc |
| `mode` | Không | Chế độ nén: `strict` / `summary` / `extract` (mặc định `summary`) |
| `platform` | Không | Nền tảng đích (tự đặt giới hạn số chữ): `weibo`(140) / `twitter`(280) / `xiaohongshu`(1000) / `zhihu_answer`(tự do) |
| `preserve` | Không | Danh sách thông tin/từ khoá bắt buộc giữ |
| `tone` | Không | Thiên hướng giọng sau khi nén: `neutral` (mặc định) / `punchy` (mạnh) / `soft` (mềm) |

### Giải thích các chế độ nén

| Chế độ | Hành vi | Dùng khi nào |
|------|------|----------|
| `strict` | Siết đúng số chữ đích ±5%, cân từng chữ | Nền tảng có giới hạn độ dài cứng (Weibo, Twitter) |
| `summary` | Giữ hết ý chính, cho phép số chữ xê dịch ±15% | Làm tóm tắt, sapo bài viết |
| `extract` | Chỉ trích nguyên câu đắt nhất trong bản gốc, không viết lại | Trích câu đắt, lọc tinh hoa |

## Đầu ra

- Nội dung sau khi nén
- Báo cáo nén: số chữ bản gốc, số chữ đích, số chữ thực tế, tỉ lệ nén, danh sách ý cốt lõi đã giữ
- Ghi vào thư mục `outputs/`

## Các bước thực hiện

> **Số chữ lấy theo script**: đếm chữ và phán định đạt/chưa đạt đều dùng `skills/shared/scripts/wordcount.py`,
> không tự đếm. LLM lo viết lại, script lo phán định.
> Cách đếm cho mạng xã hội (`social_count`) = ký tự CJK + từ tiếng Anh + chuỗi số + dấu câu.

### Step 1 - Phân tích bản gốc

1. Đếm số chữ bản gốc: `python3 skills/shared/scripts/wordcount.py count -f <bản-gốc>` (hoặc truyền qua stdin)
2. Trích cấu trúc thông tin cốt lõi:
   - Luận điểm trung tâm / dữ kiện cốt lõi
   - Luận cứ then chốt / số liệu chống lưng
   - Thông tin thứ yếu / phần bổ sung
   - Nội dung tô điểm / câu chuyển ý
3. Gắn mức ưu tiên cho từng thông tin (P0 bắt buộc giữ / P1 cố giữ / P2 có thể bỏ)

### Step 2 - Chiến lược cắt

Chọn chiến lược theo tỉ lệ giữ lại (số chữ đích / số chữ bản gốc):

| Tỉ lệ giữ | Chiến lược | Mô tả |
|--------|------|------|
| > 70% | Cắt nhẹ | Bỏ tô điểm thừa, gộp cách nói lặp |
| 40%-70% | Nén vừa | Bỏ thông tin P2, gọn câu cú, gộp đoạn giống nhau |
| 20%-40% | Nén mạnh | Chỉ giữ P0/P1, viết lại theo lối mật độ cao |
| < 20% | Nén tối đa | Chỉ giữ P0, gói trong một câu |

### Step 3 - Thực hiện nén

Chạy theo `mode`:

**Chế độ strict (script làm chốt chặn, chỉnh theo vòng khép kín):**
1. Cắt trước về 120% số chữ đích
2. Gọn từng câu, bỏ những từ có thể bỏ trong mỗi câu
3. **Gọi script kiểm tra**: `python3 skills/shared/scripts/wordcount.py check --target <N> -f <file>` (hoặc truyền qua stdin)
   - Mã thoát 0 = đạt; khác 0 = chưa đạt, script sẽ báo "còn cần thêm/bớt X chữ"
   - Giới hạn cứng của nền tảng mặc định ±5%, chỉnh bằng `--tolerance` (ví dụ `--tolerance 0.1`)
4. **Chưa đạt thì viết lại rồi check lại, tới khi script phán pass (mã thoát 0)**, không được kết thúc theo cảm tính
5. Xác nhận không có câu đứt, không có câu cụt

**Chế độ summary:**
1. Lọc nội dung theo mức ưu tiên thông tin
2. Viết lại bằng lời của mình, không bị ràng buộc bởi cú pháp bản gốc
3. Bảo đảm mạch logic liền lạc, đọc độc lập được

**Chế độ extract:**
1. Chấm điểm từng câu (mật độ thông tin x chất lượng diễn đạt)
2. Chọn câu theo điểm giảm dần, tới khi gần số chữ đích
3. Chỉnh thứ tự câu cho liền mạch
4. Không viết lại câu gốc (nhiều nhất là thêm câu nối)

### Step 4 - Kiểm tra chất lượng

- Số chữ đạt chưa: **chế độ strict bắt buộc lấy mã thoát 0 của `wordcount.py check` làm chuẩn**; chế độ khác dùng `wordcount.py count` đối chiếu xem có nằm trong dung sai không
- Thông tin then chốt trong `preserve` đã giữ đủ chưa
- Bản nén có đọc độc lập được không (không cần xem bản gốc vẫn hiểu)
- Có sai lệch thông tin không (nén làm đổi nghĩa)
- Câu có trọn vẹn không (không câu cụt, không đại từ lửng)

### Step 5 - Xuất báo cáo nén

```
Báo cáo nén:
- Bản gốc: 2.350 chữ
- Đích: 500 chữ
- Thực tế: 487 chữ (tỉ lệ nén 79.3%, tỉ lệ nén = phần đã cắt = 1 - thực tế/bản gốc)
- Chế độ: summary
- Ý đã giữ:
  1. [P0] Luận điểm cốt lõi - đã giữ
  2. [P0] Số liệu then chốt - đã giữ
  3. [P1] Phần ví dụ - đã rút gọn
  4. [P2] Phần bối cảnh - đã bỏ
```

## Nhận biết Profile

- **Có Profile**: đọc tông giọng thương hiệu từ `style.md`, giữ phong cách ngôn ngữ nhất quán khi nén; tham chiếu ưu tiên nền tảng trong `platforms.md`, tự khớp quy chuẩn số chữ của nền tảng hay dùng nhất
- **Không có Profile**: nén theo tham số người dùng chỉ định; chưa chỉ định nền tảng thì mặc định chế độ `summary`, nén còn 30%-50% bản gốc

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
