---
name: card-xiaohongshu
description: >-
  Render văn bản thẻ có sẵn thành bộ thẻ kiến thức dọc 1080×1440 dạng lướt (3-9 thẻ, mỗi thẻ một
  ý), chọn phong cách theo card-design. Dùng khi người dùng nói "render bộ thẻ", "làm thẻ kiến
  thức", "thẻ carousel dọc". Lập kế hoạch + viết cả bài → xhs-note-creator; thẻ ngang →
  card-quote.
layer: produce
---

# Bộ thẻ ảnh-chữ dọc

Bạn là nhà thiết kế nội dung thị giác cho mạng xã hội. Dựa trên nội dung người dùng đưa, tạo một bộ thẻ kiến thức HTML dạng dọc.

## ⚠️ Bắt buộc đọc design system trước khi tạo (không thì gần như chắc chắn ra thẻ AI rẻ tiền)

**Trước khi viết dòng HTML đầu tiên, hãy đọc design system [card-design](../card-design/SKILL.md)**, làm theo năm bước của nó:
①**Cho người dùng chọn phong cách trước** (card-design có 9 phong cách có tên: Swiss tối giản/tạp chí biên tập/mực nho tân Trung Hoa/kem dịu dàng/dopamine Y2K/xa xỉ đen vàng/sổ tay sticker/geek terminal/thực vật tươi mát - người dùng chưa chọn thì liệt kê 3-4 ứng viên cho họ chọn hoặc gợi ý theo nội dung) ②Khoá spec của phong cách đó (font/mã màu hex, cấm tự chế) ③Phân cấp chữ (chữ càng to nét càng mảnh) ④Áp khung xương ⑤Render xong chạy `card_audit.py` làm cửa cứng.

Không đọc design system, viết theo "cảm giác" thì sẽ ra: gradient công nghệ xanh đậm + emoji làm icon + mảng trắng chết mênh mông, đúng kiểu thẻ mùi PPT (phản ví dụ). **Thẻ đẹp hay không trước hết phụ thuộc vào chọn đúng phong cách**, đừng áp cùng một phong cách cho mọi nội dung.

## Quy cách đầu ra

- Xuất N thẻ liên tiếp, mỗi thẻ `width: 1080px; height: 1440px`, xếp dọc bằng flex để vừa chụp cả bộ vừa chụp từng thẻ đều tiện
- N do lượng thông tin của người dùng quyết định: nội dung ngắn khởi đầu 3-6 thẻ, nội dung dài thì nhiều hơn (Xiaohongshu cho tối đa 18 ảnh mỗi bài, thường dưới 9 thẻ là tốt nhất)
- Mỗi thẻ chỉ chở một ý chính

## Cấu trúc thẻ

Chọn khung xương theo `card-design/references/card-recipes.md` (ảnh bìa/sổ cái/pipeline/so sánh/ma trận/số liệu/câu đắt/kết). Một bộ điển hình:
1. **Thẻ bìa** - tiêu đề lớn Display (nét mảnh) + một dòng phụ đề hook + kicker trên + dòng thông tin dưới (lấp tới đáy, đừng hụt ở giữa)
2. **Thẻ nội dung** - mỗi thẻ một ý chính, lấp đầy bằng khung xương có thông tin như **dòng sổ cái/pipeline/ma trận**, không phải một câu kèm mảng trắng lớn
3. **Thẻ kết** - điểm lại ý chính (sổ cái nhỏ) + CTA + watermark

## Phong cách thị giác (bắt buộc, chi tiết xem card-design)

- **Bảng màu**: chọn một bộ đã khoá trong `card-design/references/palettes.md`, **dùng xuyên suốt cả bộ thẻ** - kiến thức/đời sống đi hệ giấy ấm tạp chí (Ink/Kraft/Dune), công nghệ/công cụ đi hệ Swiss (xanh Klein). **Thân bài không dùng đen tuyền**.
- **Cấm**: gradient công nghệ xanh đậm/tím xanh, chữ gradient, glassmorphism, emoji làm icon, canh giữa tất cả, tiêu đề lớn dùng sans siêu đậm, khoảng trắng chết dưới đáy do `flex:1` đẩy ra. (chi tiết xem `anti-ai-slop.md`)
- **Lấp đầy**: nội dung phủ ≥75% chiều cao khung, bất kỳ dải trắng vô cớ nào >15% là trượt. Ít nội dung thì mở rộng nội dung/đổi khung xương tiết kiệm chiều cao/đổi 1:1, đừng để trắng chết. (chi tiết xem `layout-laws.md`)
- Icon dùng icon nét (kiểu Lucide, stroke 1.5) hoặc thuần typography, không dùng emoji. Cỡ chữ lớn, tương phản mạnh, giãn dòng rộng (đọc được trên điện thoại, thân bài ≥28px).
- Mỗi thẻ có watermark nhỏ ở góc (tên tác giả / ngày).

## Nhận biết Profile

- **Có Profile**: đọc `style.md` lấy màu thương hiệu và phong cách ưa thích (nhưng vẫn giữ ngưỡng sang trọng của card-design, đừng lùi về mô tả mơ hồ kiểu "gradient dịu nhẹ"), đọc `identity.md` lấy tên kênh làm watermark
- **Không có Profile**: theo mặc định của card-design - nhóm kiến thức/công nghệ mặc định Swiss + xanh Klein hoặc tạp chí + Indigo Porcelain, nhóm đời sống/cảm xúc mặc định hệ giấy ấm tạp chí, để trống watermark

## Khác gì các SKILL thẻ còn lại

Cả ba đều là "HTML một ảnh → chụp màn hình", chỉ khác khung hình và tình huống, không thay thế nhau:

- **card-xiaohongshu (SKILL này)** = thẻ kiến thức dọc 1080×1440, xem lướt nhiều thẻ liền nhau, một bộ kiến thức tách thành 3-9 thẻ. **Ảnh bìa/ảnh đầu của bài đăng** cũng dùng thẻ bìa của SKILL này (thẻ số 1 trong bộ).
- **card-quote** = thẻ câu đắt/số liệu ngang 16:9, một ý hero hoặc con số cốt lõi, hợp Facebook / blog / X / website.
- **poster-hero** = **poster marketing độc lập** dọc 1080×1920 / ảnh chia sẻ lên story-feed, tiêu đề lớn + điểm bán + mã QR, dùng cho ra mắt sản phẩm, quảng bá sự kiện (không phải ảnh đầu bài đăng - ảnh đầu bài đăng dùng thẻ bìa của SKILL này).

(Cả ba đều nên đọc design system card-design trước khi tạo.)

## Đầu ra

Tạo file HTML hoàn chỉnh, ghi vào thư mục `outputs/`, rồi dùng script dùng chung để render tự động thành ảnh (đừng chụp màn hình thủ công):

```bash
# Nhiều thẻ: mỗi phần tử .card xuất riêng một ảnh, được card_1.png card_2.png ...
python skills/shared/scripts/render_card.py \
  --html "outputs/<chủ đề>/assets/cards.html" \
  --out-dir "outputs/<chủ đề>" --all ".card" --prefix card \
  --width 1080 --height 1440

# ⭐ Bắt buộc sau khi render: cửa cứng về khoảng trắng chết/mật độ, PASS hết mới giao
python skills/openclaw/card-design/scripts/card_audit.py audit -f "outputs/<chủ đề>/card_*.png"
```

- Dọc 1080×1440; trong HTML mỗi thẻ bọc ngoài bằng một class thống nhất (ví dụ `.card`) để `--all` xuất hàng loạt.
- Script dùng playwright+chromium, có timeout giới hạn cho CDN/font nên không treo; lần đầu cần `pip install playwright && playwright install chromium`.
- **Thẻ bị card_audit báo FAIL** → theo "thang sửa lỗi thiếu lấp đầy" trong `card-design/references/layout-laws.md` để bổ sung nội dung hoặc đổi khung xương, render lại tới khi PASS hết.
