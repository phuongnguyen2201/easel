---
name: skill-seo-quality
description: >-
  Kiểm và tối ưu để bài hiện trong kết quả tìm kiếm trên Facebook/TikTok/YouTube: từ khoá ở tiêu
  đề, thân bài, hashtag, ảnh bìa/khung đầu; cân đối tìm kiếm vs đề xuất; có chế độ web/blog. Dùng
  khi người dùng nói "SEO", "sao không tìm thấy bài tôi", "chọn hashtag thế nào", "tối ưu tìm
  kiếm".
layer: publish
---

# Tối ưu tìm kiếm nội sàn

> Làm cho nội dung được nền tảng tìm ra và xếp hạng cao. Lấy cơ chế tìm kiếm nội sàn của các nền tảng nội dung Trung Quốc làm chủ thể, web SEO cho trang/blog là chế độ tuỳ chọn.

## Định vị

Lưu lượng trên các nền tảng này chia hai nhánh: **lưu lượng đề xuất** (thuật toán chủ động phân phối) và **lưu lượng tìm kiếm** (người dùng chủ động gõ từ khoá và trúng bài). Đa số nhà sáng tạo chỉ tối ưu đề xuất, bỏ quên tìm kiếm - trong khi lưu lượng tìm kiếm thì trúng đích, dài hạn, tích luỹ được. SKILL này chuyên trị nhánh tìm kiếm: làm cho tiêu đề, thân bài, hashtag, chữ trên ảnh bìa đều trúng từ mà người dùng sẽ tìm.

Việc tối ưu hook/tỉ lệ xem hết/tương tác cho lưu lượng đề xuất không thuộc đây, giao cho `social-content` / `video-script`.

## Đầu vào

- Nội dung cần kiểm (đường dẫn file, văn bản, hoặc link bài đã đăng)
- Nền tảng mục tiêu (Xiaohongshu / Douyin / Zhihu / WeChat OA / Bilibili / Weibo; thiếu thì hỏi hoặc lấy theo Profile)
- Tuỳ chọn: từ khoá mục tiêu / tình huống tìm kiếm muốn phủ, trọng tâm kiểm (soát trước khi đăng / bổ sung từ khoá / tối ưu toàn diện)

## Đầu ra

```markdown
# Báo cáo tối ưu tìm kiếm - [nền tảng]

## Rà soát mức trúng từ khoá mục tiêu
| Từ khoá/tình huống tìm | Vị trí xuất hiện (tiêu đề/thân bài/hashtag/ảnh bìa) | Trọng số | Trạng thái |

## Soát từng mục (theo tín hiệu tìm kiếm của nền tảng đó)
| Mục kiểm | Trạng thái ✅/⚠️/❌ | Giải thích | Đề xuất sửa |

## Chẩn đoán đánh đổi giữa tìm kiếm và đề xuất
(nội dung hiện nghiêng về nhánh nào, có cần nhường một phần hook đề xuất cho tìm kiếm không)

## Đánh giá tổng: ✅ đăng được / ⚠️ cần sửa / ❌ diện tìm kiếm quá hẹp
## Mục cần sửa ưu tiên (Top 3, xếp theo mức tăng hiển thị tìm kiếm dự kiến)
```

## Các bước thực hiện

1. **Đọc nội dung** - lấy toàn văn, tiêu đề, hashtag/chủ đề, chữ trên ảnh bìa hoặc khung đầu (video thì lấy tiêu đề + mô tả + khung phụ đề chính).
2. **Chốt nền tảng và từ khoá mục tiêu** - không có từ mục tiêu thì suy ngược từ chủ đề nội dung ra từ khoá và từ khoá đuôi dài người dùng có thể tìm (ai tìm, tìm gì, nói bằng cách nào).
3. **Nạp quy tắc nền tảng** - đọc trong `references/platform-search.md` phần tín hiệu tìm kiếm và cách bố trí từ khoá của nền tảng tương ứng.
4. **Soát từng mục** - chấm theo quy tắc của nền tảng đó: từ khoá có đặt lên trước không, mật độ có tự nhiên không, hashtag có trúng từ hot trong tìm kiếm không, ảnh bìa/khung đầu có chữ tìm được không.
5. **Chẩn đoán đánh đổi lưu lượng** - xác định nội dung đang nghiêng về đề xuất hay tìm kiếm, đưa cách bổ sung cho tìm kiếm mà không hy sinh độ dễ đọc.
6. **(Tuỳ chọn) chế độ trang web/blog** - khi nội dung là bài dài trên WeChat OA được Baidu lập chỉ mục, câu trả lời Zhihu muốn lên công cụ tìm kiếm, hoặc website/blog riêng, đọc `references/web-blog-seo.md` để soát thêm phần web SEO.
7. **Xếp ưu tiên và ghi sản phẩm** - chọn Top 3 tăng ích nhiều nhất, lưu vào `outputs/<chủ đề>/seo-report.md`.

## Nhìn nhanh theo nền tảng

Cơ chế tìm kiếm của các nền tảng khác nhau rất nhiều, quy tắc chi tiết xem `references/platform-search.md`. Khác biệt cốt lõi:

| Nền tảng | Cửa tìm kiếm | Tín hiệu tìm kiếm quan trọng nhất |
|------|----------|------------------|
| Xiaohongshu | Ô tìm kiếm nội sàn | Từ khoá tiêu đề + thân bài, hashtag chủ đề, chữ ảnh bìa, lượt lưu |
| Douyin | Tìm kiếm + ô tìm kiếm chèn trong luồng đề xuất video | Từ khoá tiêu đề/nội dung, từ chủ đề, tỉ lệ xem hết và tương tác |
| Zhihu | Tìm kiếm nội sàn + được Baidu/Google lập chỉ mục | Khớp câu hỏi, tín hiệu chất lượng câu trả lời; **web SEO áp dụng ở đây** |
| WeChat OA | WeChat Search | Từ khoá tiêu đề, nhãn bài nguyên gốc, trọng số kênh, lịch sử được tìm |
| Bilibili | Tìm kiếm nội sàn | Từ khoá tiêu đề/tag/mô tả, lượt xem và tỉ lệ xem hết |
| Weibo | Chủ đề/super topic/bảng tìm kiếm nóng | Từ chủ đề #, tính thời sự, lượng tương tác |

**Ranh giới áp dụng**: Meta description, Open Graph, URL/Slug, phân cấp H1/H2, E-E-A-T - nhóm web SEO này chỉ có tác dụng với nội dung "bị công cụ tìm kiếm (Baidu/Google) thu thập": câu trả lời Zhihu, website/blog riêng, bài WeChat OA được lập chỉ mục ra ngoài. Nội dung thuần nội sàn (Xiaohongshu/Douyin/Bilibili/Weibo) không ăn bộ này, đừng áp.

## Nguyên tắc kiểm

- **Đặt từ khoá lên trước** - khi người dùng tìm, hệ thống ưu tiên khớp các từ nằm ở đầu; để từ khoá chính ở đầu tiêu đề và câu đầu thân bài.
- **Dùng từ người thật hay nói** - trúng đúng cách nói người dùng thật sự gõ, không phải tiếng lóng ngành hay từ tự chế.
- **Mật độ tự nhiên** - từ khoá phủ đủ là được, nhồi nhét còn bị chấm kém chất lượng và bị bóp tương tác.
- **Hashtag là trọng số tìm kiếm, không phải trang trí** - hashtag chủ đề vào thẳng chỉ mục tìm kiếm, chọn loại có lượng tìm cao và liên quan.
- **Ảnh bìa/khung đầu cũng tìm được** - một số nền tảng OCR chữ trên ảnh bìa để đưa vào chỉ mục, chữ trên bìa cũng phải có từ khoá.
- **Tìm kiếm và đề xuất có thể cùng đạt** - ưu tiên bổ sung từ khoá mà không hy sinh hook và độ dễ đọc, xung đột thì chọn theo mục tiêu nội dung.

## Nhận biết Profile

- **Có Profile**: đọc `platform` để khoá quy tắc nền tảng; đọc `audience` để suy ra cách tìm kiếm của nhóm khán giả đó; đọc `hashtag_sets` quen dùng của kênh để tái dùng hashtag trọng số cao; đọc `preferences` để né từ cấm.
- **Không có Profile**: hỏi nền tảng mục tiêu và tình huống tìm kiếm muốn phủ, soát theo quy tắc chung trong `references/platform-search.md`, cuối bài ghi chú "cung cấp Profile của kênh sẽ nhận được gợi ý từ khoá bám sát thói quen tìm kiếm của khán giả hơn".
