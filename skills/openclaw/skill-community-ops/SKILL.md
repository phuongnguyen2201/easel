---
name: skill-community-ops
description: >-
  Vận hành bình luận, xử lý khủng hoảng sau đăng: mẫu trả lời, mức xử lý cho khen/hỏi/muốn mua/cà
  khịa/anti-fan, đào đề tài từ bình luận; có sự cố: phân cấp, soạn tuyên bố và phát ngôn chung.
  Dùng khi người dùng nói "trả lời bình luận", "bị chửi", "khủng hoảng truyền thông", "thư xin
  lỗi".
layer: publish
---

# Vận hành bình luận và ứng phó khủng hoảng truyền thông

> Năng lực tầng vận hành sau khi đăng: trả lời bình luận, đào đề tài từ bình luận, phân cấp ứng phó khi có sự cố tiêu cực. Ba chế độ, trúng cái nào làm cái đó.

## Ba chế độ

| Chế độ | Tình huống kích hoạt | Sản phẩm chính |
|------|----------|----------|
| A Chiến lược trả lời bình luận | Có một loạt bình luận cần trả lời / hỏi "bình luận này trả lời sao" | Mẫu trả lời theo nhóm + quy tắc xử lý theo mức |
| B Đào đề tài từ bình luận | Hỏi "bình luận đào được đề tài gì" / đưa một đống bình luận | 3-5 gợi ý đề tài cho bước tiếp theo |
| C Ứng phó khủng hoảng truyền thông | Có sự cố tiêu cực, làn sóng đánh giá xấu, bị dìm | Phân cấp khủng hoảng + nháp tuyên bố + phát ngôn chung + lằn ranh đỏ + thời hạn phản hồi |

Một yêu cầu có thể trúng nhiều chế độ (kiểu "bình luận đang cãi nhau, trả lời giúp mình rồi xem có cần ra tuyên bố không"). Xác định chế độ trước, rồi chạy đúng quy trình tương ứng. Nếu đầu vào mơ hồ, hỏi rõ "cần trả lời bình luận, đào đề tài, hay xử lý tiêu cực".

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Nội dung bình luận | Bắt buộc với chế độ A/B | Một loạt bình luận thật, hoặc mô tả tình huống kiểu "nội dung của mình hay nhận bình luận dạng XX" |
| Mô tả sự cố tiêu cực | Bắt buộc với chế độ C | Chuyện gì đã xảy ra, trên nền tảng nào, lan tới mức nào, có bằng chứng xác thực không |
| Nền tảng mục tiêu | Nên có | Xiaohongshu / Douyin / Bilibili / Weibo / WeChat OA / Zhihu, quyết định tông giọng |
| Persona thương hiệu/lằn ranh đỏ | Tuỳ chọn | Không có Profile thì cấp tay, dùng để chốt giọng và phát ngôn |

## Chế độ A: Chiến lược trả lời bình luận

1. Đọc `references/reply-playbook.md` mục "I. Kho lời thoại phân tầng cho 5 nhóm bình luận", xếp bình luận người dùng đưa vào 5 nhóm: khen thường / hỏi chuyên môn / muốn mua xin link / cà khịa bắt bẻ / anti-fan chê ác ý.
2. Mỗi nhóm cho 2-3 mẫu trả lời dùng được ngay (dùng `[placeholder]` cho tên thương hiệu, sản phẩm, link..., không viết cứng case cụ thể).
3. Theo `references/reply-playbook.md` mục "II. Quy tắc xử lý theo mức", đưa ra mức xử lý: phải trả lời / dẫn sang nhắn riêng / ghim lên đầu / để nguội / xoá và chặn, kèm giải thích mỗi bình luận rơi vào mức nào, vì sao.
4. Chỉnh giọng theo nền tảng mục tiêu: đọc đoạn nền tảng tương ứng trong `references/platform-comment-ecology.md` (Xiaohongshu thân thiện, Bilibili nhiều meme, Zhihu chuyên sâu, Douyin ngắn gọn, Weibo nhịp nhanh, WeChat OA tiết chế).
5. Đầu ra: bảng mẫu trả lời theo nhóm + danh sách xử lý theo mức + gợi ý giọng theo nền tảng.

## Chế độ B: Đào đề tài từ bình luận

1. Đọc hết bình luận, theo `references/topic-mining.md` mục "I. Các chiều gom cụm bình luận" gom ra nhu cầu lặp nhiều, câu hỏi lặp lại, điểm tranh cãi, lời xin nội dung, lời than phiền.
2. Thống kê độ mạnh tín hiệu của từng cụm (tần suất cao / trung bình / lác đác nhưng gắt).
3. Theo `references/topic-mining.md` mục "II. Công thức biến bình luận thành đề tài", chuyển các cụm giá trị cao thành 3-5 gợi ý đề tài cụ thể.
4. Mỗi đề tài cần: hướng tiêu đề + lấy từ bình luận nào/nhóm nào + vì sao đáng làm + dạng thể hiện gợi ý (bài ảnh/video/tuyển tập).
5. Đầu ra: tóm tắt các cụm bình luận + 3-5 thẻ gợi ý đề tài.

## Chế độ C: Ứng phó dư luận / khủng hoảng

1. Đọc `references/crisis-grading.md` mục "I. Chuẩn phân ba cấp khủng hoảng", căn theo tính chất sự việc, mức lan toả, có bằng chứng xác thực không, có chạm đáy an toàn/pháp lý/đạo đức không, để kết luận: 🟢 bỏ qua được / 🟡 cần phản hồi / 🔴 cần tuyên bố chính thức. Nêu căn cứ kết luận (trúng những tiêu chí nào).
2. Theo cấp đã kết luận mà lấy sản phẩm tương ứng:
   - 🟢 Bỏ qua được -> nêu lý do chọn "không phản hồi/phản hồi nhẹ" + gợi ý theo dõi nội bộ (canh tín hiệu nào là sẽ leo thang).
   - 🟡 Cần phản hồi -> theo `references/crisis-grading.md` mục "III. Khung lời thoại phản hồi", soạn nháp lời thoại trả lời ở bình luận/tin nhắn riêng.
   - 🔴 Cần tuyên bố chính thức -> theo mục "IV. Cấu trúc tuyên bố chính thức", soạn nháp tuyên bố (gồm bốn đoạn: trình bày sự thật, nhận trách nhiệm, biện pháp, cam kết).
3. Ra "phát ngôn chung đối ngoại": một câu lập trường cốt lõi + 3-5 cặp Q&A, bảo đảm cả nhóm nói ra ngoài giống nhau (`references/crisis-grading.md` mục "V. Phát ngôn chung").
4. Ra "danh sách lằn ranh đỏ": những việc lần này tuyệt đối không làm (`references/crisis-grading.md` mục "VI. Lằn ranh đỏ khủng hoảng", như xoá bình luận chặn bình luận, đổ lỗi, cãi tay đôi theo cảm xúc, chặn hàng loạt).
5. Ra "gợi ý thời hạn phản hồi": theo từng cấp mà đưa khung giờ vàng để lên tiếng (`references/crisis-grading.md` mục "VII. Thời hạn phản hồi").
6. Đầu ra: kết luận phân cấp khủng hoảng + nháp lời thoại/tuyên bố + phát ngôn chung + danh sách lằn ranh đỏ + gợi ý thời hạn.

## Nhận biết Profile

**Khi có Profile:**
- Đọc `preferences.md` (việc làm/việc không làm/đáy tuân thủ) -> giọng trả lời và phát ngôn khủng hoảng bám persona thương hiệu, không vượt lằn ranh đỏ.
- Đọc `style.md` / `identity.md` -> từ ngữ, cách xưng hô, liều lượng meme trong mẫu trả lời khớp phong cách kênh.
- Đọc `platforms.md` -> tự chốt tông bình luận của nền tảng chủ lực, khỏi hỏi lại.
- Phát ngôn khủng hoảng tuân theo mục "đáy tuân thủ" trong `preferences.md`, tuyên bố không hứa điều không làm được.

**Khi không có Profile:**
- Lùi về chế độ chung, mẫu trả lời dùng giọng trung tính thân thiện, để placeholder cho người dùng điền thông tin thương hiệu.
- Hỏi hoặc mặc định nền tảng mục tiêu, đi theo tông chung của nền tảng đó.
- Ứng phó khủng hoảng dùng phát ngôn an toàn chuẩn ngành, cuối bài nhắc "cung cấp Profile để phát ngôn bám persona thương hiệu và lằn ranh đỏ".

## Quy tắc

1. Mẫu luôn dùng `[placeholder]`, không viết cứng case có tên thương hiệu/sản phẩm/người cụ thể.
2. Phân cấp khủng hoảng bắt buộc nêu căn cứ, không được chỉ đưa kết luận.
3. Nháp tuyên bố chỉ hứa những biện pháp làm được, không viết sáo rỗng, không hứa hão.
4. Không gợi ý bất kỳ hành vi xoá bình luận chặn bình luận, seeding ảo spam, cãi vã ác ý hay động tác vi phạm, làm hỏng niềm tin dài hạn.
5. Câu trả lời và phát ngôn hợp với hệ sinh thái bình luận của nền tảng mục tiêu, không bê nguyên tông của nền tảng khác.
