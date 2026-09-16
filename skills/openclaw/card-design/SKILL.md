---
name: card-design
description: >-
  Hệ thiết kế hình ảnh cho thẻ mạng xã hội: màu, phân cấp chữ, bố cục kín khung, khung xương theo
  loại, soát khoảng trống chết; chống PPT mẫu, mùi AI rẻ tiền. Dùng khi người dùng nói "thẻ xấu
  quá", "tối ưu hình ảnh", "màu và bố cục", "nhìn AI quá". Chuẩn cho card-*, poster-hero, không tự
  render.
layer: produce
---

# Hệ thiết kế thẻ (đọc trước khi tạo)

> Đây không phải một "bộ sinh thẻ" mà là một **hệ thiết kế + luật cứng**. Mọi SKILL thẻ/poster kiểu "HTML/CSS → chụp màn hình"
> phải đọc file này trước khi viết dòng HTML đầu tiên. Niềm tin cốt lõi (kết luận thống nhất từ các giải pháp mã nguồn mở thực chiến và nghiên cứu khử mùi AI):
> **Cảm giác cao cấp đến từ "tiết chế + phân cấp + lưới + lấp đầy", không phải chồng đổ bóng/bo góc/gradient lên nhau.**
> "Không ai ra quyết định thiết kế" = AI lấy trung bình thống kê của một vạn tấm ảnh = rẻ tiền. Hệ này chốt sẵn các quyết định thay bạn.

## Quy trình 5 bước (làm đủ, đừng bỏ bước)

1. **Cho người dùng chọn phong cách** (bước đầu tiên, cũng là bước quan trọng nhất): lấy vài lựa chọn từ **thư viện phong cách** trong `references/styles.md` cho người dùng, để họ chọn một:
   - Người dùng đã chỉ định phong cách → dùng luôn.
   - Người dùng không chỉ định → **liệt kê 3-4 ứng viên** (tên phong cách + một câu mô tả + hợp với gì), gợi ý theo loại nội dung/nền tảng/Profile, hỏi họ chọn cái nào; nếu họ gấp thì dùng ứng viên đầu tiên và nói rõ "mặc định đang dùng phong cách X, muốn đổi cứ nói".
   - Thư viện phong cách hiện có 9 kiểu: tối giản Thuỵ Sĩ / tạp chí biên tập / thuỷ mặc tân Á Đông / kem dịu nhẹ / dopamine Y2K / đen vàng cao cấp / sổ tay sticker / geek terminal / xanh cây cỏ. **Thẻ đẹp hay không, trước hết do chọn đúng phong cách**, đừng áp một kiểu cho mọi nội dung.
2. **Chốt spec của phong cách đó**: phong cách được chọn trong `styles.md` đã cho sẵn **font (family + độ đậm) + bảng màu (hex) + tính cách bố cục + hoạ tiết** - **bám sát tuyệt đối**, cả bộ thẻ từ đầu tới cuối chỉ dùng đúng bộ này, không tự phát huy, không đổi màu. (Chi tiết bảng màu xem thêm `palettes.md`)
3. **Định phân cấp chữ**: theo `typography.md` - "**chữ càng lớn càng mảnh**" (bộ font đã cài đủ độ đậm Noto Sans/Serif CJK, tiêu đề lớn dùng Thin/Light). Thân bài trên điện thoại ≥28px.
4. **Áp khung xương**: chọn khung xương theo loại thẻ trong `card-recipes.md` (ảnh bìa/sổ ghi/pipeline/so sánh/ma trận/dữ liệu/câu đắt), rồi đổ nội dung theo **ngưỡng mật độ tối thiểu** của nó.
5. **Tự kiểm sau khi render** (cổng chặn cứng):
   ```bash
   python skills/openclaw/card-design/scripts/card_audit.py audit -f "outputs/<chủ đề>"/card_*.png
   ```
   Bất kỳ FAIL nào (khoảng trống chết/dàn trải không đủ/đầu nặng chân nhẹ) → theo "thang sửa lỗi thiếu nội dung" trong `layout-laws.md` để bổ sung nội dung hoặc đổi khung xương rồi **render lại**, PASS hết mới giao.

## Tra nhanh luật thép (chi tiết xem references)

- **Lấp đầy**: nội dung phủ ≥75% chiều cao khung; bất kỳ dải trắng **không có lý do** nào >15% chiều cao khung = hỏng. Ít nội dung thì **mở rộng nội dung/đổi khung xương tốn ít chiều cao/đổi khung hình 1:1**, **tuyệt đối không** dùng `flex:1` để đẩy nội dung căn giữa theo chiều dọc, **tuyệt đối không** thêm blob trang trí lấp chỗ trống. → `layout-laws.md`
- **Chữ càng lớn càng mảnh**: tiêu đề lớn dùng w200-500, chỉ chữ nhỏ mới in đậm. Dùng toàn bộ 700 đậm = banner rẻ tiền. → `typography.md`
- **Cấm lấy emoji làm icon**: dùng icon nét (Lucide, stroke 1.5, kiểu góc cạnh) hoặc thuần typography. → `anti-ai-slop.md`
- **Cấm gradient xanh tím kiểu công nghệ** (dấu hiệu AI số một), cấm chữ gradient `bg-clip-text`, cấm glassmorphism, cấm "căn giữa mọi thứ". → `anti-ai-slop.md`
- **Thân bài không bao giờ dùng đen tuyền**, dùng xám đậm/mực đậm (#6B6560 / #0a1f3d ...).
- Lập trường Thuỵ Sĩ: **không bo góc, không đổ bóng, cấm gradient**, dựa vào mảng màu + đường mảnh + lưới. Lập trường tạp chí: bo góc nhỏ, chỉ ảnh chụp mới cho bóng cực nhẹ, bắt buộc có lớp nền tạo không khí (vân giấy/loang mực cực nhạt).

## references

- `styles.md` - ⭐ **Thư viện phong cách (9 phong cách có tên, người dùng chọn một)**, mỗi cái gồm font/mã màu hex/tính cách bố cục/hoạ tiết/hợp với gì. **Bước đầu tiên là đọc file này để chọn phong cách.**
- `palettes.md` - chốt chi tiết bảng màu (6 bộ tạp chí + 4 bộ Thuỵ Sĩ + bổ sung Morandi/kem), kèm mã hex.
- `typography.md` - phân cấp chữ, quy tắc "càng lớn càng mảnh", cỡ chữ tối thiểu không được phá, trộn chữ đa ngôn ngữ (Noto Sans/Serif CJK đủ độ đậm).
- `layout-laws.md` - luật lấp đầy khung hình, tự kiểm mật độ theo 4 dải, thang sửa lỗi thiếu/tràn nội dung (trị khoảng trống chết).
- `anti-ai-slop.md` - danh sách phản ví dụ P0/P1/P2 về cảm giác AI rẻ tiền + các thao tác khử mùi AI hiệu quả cao.
- `card-recipes.md` - khung xương theo loại thẻ/phân loại nội dung + ngưỡng mật độ tối thiểu của từng loại.

## Nhận biết Profile

- **Có Profile**: đọc bảng màu thương hiệu/thiên hướng phong cách từ `style.md`; nhưng **ưu tiên giữ ngưỡng cao cấp của hệ này** - nếu Profile không nêu quy chuẩn hình ảnh rõ ràng thì cứ theo hệ này chọn lập trường + khoá màu, đừng lùi về mô tả mơ hồ kiểu "gradient dịu nhẹ". Tên account dùng làm watermark.
- **Không có Profile**: nội dung kiến thức/công nghệ mặc định "Thuỵ Sĩ + xanh Klein" hoặc "tạp chí + Indigo Porcelain"; nội dung đời sống/cảm xúc mặc định "tạp chí + giấy ấm Kraft/Dune".

## Nguồn tham khảo

Xem `EASEL-META.md`. Quy tắc được chắt lọc lại từ op7418/guizang-social-card-skill (lập trường thiết kế/luật lấp đầy/tự kiểm mật độ, AGPL - chỉ tham khảo quy tắc chứ không chép file), comeonzhj/Auto-Redbook-Skills (skin theo chủ đề/tự phân trang), funboy322/avoid-ai-design + yetone/kill-ai-slop (danh sách khử mùi AI), cardplanet/Ant-Card (cách đặt tên phong cách và ý tưởng thư viện template).
