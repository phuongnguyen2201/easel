---
name: novel-writer
description: >-
  Viết tiểu thuyết/truyện dài kỳ: thế giới, nhân vật, dàn ý 3 cấp, từng chương (3 chương đầu giữ
  chân); trạng thái lưu file giữ mạch ngầm, tiền truyện, nhất quán. Dùng khi người dùng nói "viết
  truyện", "viết tiếp chương", "dàn ý truyện". Bài thường → social-content; một đoạn →
  text-polisher.
layer: produce
---

# Viết tiểu thuyết / truyện mạng dài kỳ bằng AI

> Một câu cảm hứng -> thế giới quan/nhân vật -> dàn ý 3 cấp -> chính văn từng chương. Cốt lõi là **nhất quán truyện dài**:
> dùng "**file là sự thật + nạp theo nhu cầu**" - AI không dựa vào trí nhớ ngữ cảnh, mỗi chương chỉ nạp lát cắt liên quan,
> trạng thái đổ hết ra file, diff được, viết tiếp được. IO xác định (dựng khung/tiến độ/quét mùi AI máy móc) chạy qua
> `scripts/novel_ops.py`, **phần sáng tạo (thiết định/dàn ý/chính văn) do bạn - LLM - làm**.

> Chỉ đổi phong cách một đoạn xem **style-transfer**; chỉ trau chuốt khử mùi AI xem **text-polisher**;
> chỉ viết bài thường xem **social-content**; đăng bài xem SKILL đăng của nền tảng đích.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Cảm hứng/đề tài | Có | Một câu ý tưởng, hoặc thiết định đã có (chưa cho thì hỏi) |
| Nền tảng | Không | Zhihu Yanxuan / Fanqie / Qidian / bài ảnh-chữ Xiaohongshu (mặc định theo Profile hoặc hỏi) |
| Tên sách | Không | Bỏ trống thì đặt theo đề tài, dùng làm tên thư mục sản phẩm |
| Việc lần này | Không | Lập dự án / ra dàn ý / viết chương N / viết tiếp / chuyển bài ảnh-chữ (mặc định suy từ hội thoại) |

## Cấu trúc sản phẩm (`outputs/<tên sách>/`)

```
bible/    world.md characters.md voice.md canon.md   <- sự thật cứng (chương nào cũng phải đọc)
outline/  overview.md volumes.md chapters.md          <- dàn ý 3 cấp
state/    summary.md character-state.md plot-arcs.md progress.json/md  <- trạng thái dài kỳ
chapters/ 001.md 002.md ...                            <- chính văn từng chương
```

Đường dẫn script (tính từ gốc dự án): `skills/openclaw/novel-writer/scripts/novel_ops.py`.
Kiểm số chữ dùng chung: `skills/shared/scripts/wordcount.py`.

## Các bước thực thi (chọn nhánh theo hội thoại, không cần chạy hết mỗi lần)

### A. Lập dự án (lần đầu)

1. **Dựng khung**: `python skills/openclaw/novel-writer/scripts/novel_ops.py scaffold --book "<tên sách>"`
   (sinh mẫu bible/outline/state/chapters, file đã có thì không ghi đè).
2. **Chốt thế giới quan + nhân vật + văn phong**: đọc `references/web-novel-methodology.md` và `references/platform-specs.md`,
   theo đề tài viết đầy `bible/world.md` (hệ thống sức mạnh/luật lệ/ràng buộc cứng), `bible/characters.md` (nhân vật chính + phụ quan trọng: thân phận/ngoại hình/tính cách/mục tiêu/quan hệ),
   `bible/voice.md` (ngôi kể/thì/nhịp câu/từ hay dùng + bảng từ cấm của sách này). Thiết định phải **chạy được** (ràng buộc được chính văn), không viết chung chung.

### B. Dàn ý (3 cấp)

3. **overview -> volumes -> chapters**: viết `outline/overview.md` (một câu bán ý tưởng + xung đột lõi + tuyến chính + hướng kết),
   `outline/volumes.md` (arc từng quyển: mục tiêu/bước ngoặt/cao trào cuối quyển), `outline/chapters.md` (bảng mục lục chương: tiêu đề + một câu hook + phục bút liên quan).
   Nền dàn ý có thể tham khảo `skill-article-outline`, nhưng phải mở rộng thành cấu trúc 3 cấp của truyện mạng + bảng cắm phục bút (ghi vào `bible/canon.md`).

### C. Ba chương vàng (3 chương đầu tăng cường riêng)

4. Theo mẫu ba chương vàng trong `references/web-novel-methodology.md`, đẩy kịch **hook mở đầu, điểm sướng, cảm giác nhập vai, hồi hộp giữ người đọc** của ba chương đầu
   (chương 1 phải cho tín hiệu xung đột/kim thủ chỉ trong 3 giây; cuối mỗi chương để hook mạnh). Ba chương này quyết định tỉ lệ giữ chân, đáng mài riêng.

### D. Viết một chương (vòng lặp chính của truyện dài kỳ)

5. **Chỉ nạp lát cắt liên quan** (đừng nhét cả sách): đọc `bible/` (toàn bộ, là ràng buộc cứng) + đúng dòng của chương này trong `outline/chapters.md` +
   `state/summary.md` (tóm tắt tiền truyện) + các nhân vật liên quan trong `state/character-state.md`.
6. **(Tuỳ chọn) ra thẻ cảnh trước**: chương phức tạp thì theo `references/scene-card-schema.md` liệt kê thẻ cảnh (nhân vật/địa điểm/xung đột/story value lên xuống/cảm xúc/lối ra) rồi mới viết chính văn.
7. **Viết chính văn** vào `chapters/<ba chữ số>.md`: theo văn phong `bible/voice.md`, cuối chương hook mạnh.
8. **Cổng số chữ**: đưa chính văn qua
   `python3 skills/shared/scripts/wordcount.py check --target <số chữ mục tiêu của nền tảng> --tolerance 0.15 -f chapters/<NNN>.md`
   (Zhihu Yanxuan/Fanqie thường 2000-4000 chữ mỗi chương, xem platform-specs), chưa đạt thì thêm bớt theo gợi ý.
9. **Khử mùi AI**: chạy `python skills/openclaw/novel-writer/scripts/novel_ops.py slopcheck -f chapters/<NNN>.md` trước
   để quét máy móc (từ mùi AI/từ nối thừa/lặp đầu câu), chỗ nào dính thì viết lại; rồi cho cả chương qua **text-polisher** (chế độ khử mùi AI).

### E. sync (chốt bản xong thì bảo trì trạng thái, chống vỡ mạch giữa các chương)

10. Cập nhật `state/` và `bible/canon.md`:
    - Dùng **text-condenser** (chế độ tóm tắt) nén cuốn chiếu "diễn biến đã xảy ra" vào `state/summary.md` (chương sau nạp file này, không nạp toàn văn).
    - Cập nhật `state/character-state.md` (vị trí/hoàn cảnh/quan hệ nhân vật thay đổi), `state/plot-arcs.md` (tiến độ từng tuyến), `bible/canon.md` (sự kiện mới/dòng thời gian/trạng thái phục bút: cắm -> thu).
    - Ghi tiến độ: `novel_ops.py record --book "<tên sách>" --chapter N --title "<tiêu đề>" --words <số chữ> --status done --when <ngày hôm nay>`
      (ngày lấy từ ngữ cảnh hội thoại, script không tự lấy giờ để giữ tính xác định).
11. **Tự soát nhất quán**: đối chiếu `bible/canon.md` quét xem chương này có chỏi sự thật/dòng thời gian/nhân vật đã chốt không; có thì sửa chính văn hoặc bổ sung thiết định (xem `references/consistency-rules.md`).

### F. (Tuỳ chọn) next - suy diễn tình tiết

12. Khi bí tình tiết, sinh 2-3 **nhánh** đề cương chương kế (hướng đi/điểm sướng/twist khác nhau), liệt kê hơn kém cho người dùng chọn, chốt rồi mới viết.

### G. (Tuỳ chọn) chuyển thành bài ảnh-chữ dài kỳ trên Xiaohongshu

13. Giao một chương cho **card-xiaohongshu** hoặc **xhs-note-creator**, tách thành 3-9 thẻ dọc đăng dài kỳ (mỗi thẻ một nốt cảm xúc, thẻ cuối để hook).

## Nhận biết Profile

- **Có Profile**: `platforms.md` chốt nền tảng và số chữ/tần suất ra chương; `style.md` hoà vào văn phong `bible/voice.md`;
  `identity.md`/`audience.md` chốt tông đề tài và người đọc mục tiêu; `preferences.md` lọc lằn ranh đỏ (đề tài/nội dung nhạy cảm).
- **Không Profile**: hỏi trước về nền tảng và gu đề tài; mặc định ngôi thứ ba, mỗi chương ~3000 chữ, cuối chương hook mạnh, phong cách truyện mạng phổ thông.

## Quy tắc

1. **File là sự thật**: thiết định/trạng thái lấy theo file `bible/` `state/`, không dựa trí nhớ hội thoại; chỏi nhau thì canon thắng.
2. **Nạp theo nhu cầu**: mỗi chương chỉ đọc lát cắt liên quan, tránh nhét cả sách vào ngữ cảnh gây trôi/quá dài.
3. **Nhất quán trên hết**: nhân vật/thế giới quan/phục bút không vỡ giữa các chương là mạch sống của truyện mạng, thà chậm còn hơn vỡ.
4. **Khử mùi AI**: slopcheck máy móc + text-polisher, hai lớp bảo hiểm; văn phong thống nhất nhờ `bible/voice.md`.
5. **Không ghi đè nội dung đã viết**: scaffold idempotent, record upsert; sửa chính văn/thiết định bằng chỉnh sửa tăng dần, đừng viết lại cả bài xoá mất sửa của người dùng.
6. **Không bịa thiết định**: chi tiết thế giới quan chưa chắc thì hỏi trước hoặc bổ sung định nghĩa vào bible rồi mới viết chính văn.

## Nguồn tham khảo

Xem `EASEL-META.md`. Phương pháp luận đúc từ autonovel (hệ thống mẫu/miễn dịch kép chống slop), Maliang MaliangAINovalWriter
(dàn ý 3 cấp/ba chương vàng/suy diễn tình tiết), AI_NovelGenerator (chốt bản thì cập nhật trạng thái + soát nhất quán), GOAT-Storytelling-Agent
(tách thẻ cảnh thay ngữ cảnh dài) - đều theo tư tưởng "file là sự thật + nạp theo nhu cầu", hợp nhất với Easel thuần công cụ file.
