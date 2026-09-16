---
name: skill-comment-insights
description: >-
  Phân tích định lượng bình luận: cảm xúc (tỉ lệ tích cực/trung tính/tiêu cực + bình luận tiêu
  biểu), từ/cụm tần suất cao, nhu cầu/phàn nàn/câu hỏi; dữ liệu cho hậu kiểm, đề tài. Dùng khi
  người dùng nói "phân tích bình luận", "khán giả nói gì", "khách chê gì". Trả lời →
  skill-community-ops.
layer: attribute
---

# Phân tích định lượng khu bình luận (comment-insights)

> Bóc insight định lượng từ bình luận: phân bố cảm xúc, từ và cụm tần suất cao, đào nhu cầu và phàn nàn. Chạy qua
> `scripts/comment_insights.py` (jieba + SnowNLP + từ điển cảm xúc mạng xã hội).

> Phân vai với skill-community-ops: community-ops lo "trả lời bình luận thế nào + xử lý khủng hoảng" (thao tác vận hành);
> SKILL này lo "khu bình luận đang nói gì" (dữ liệu định lượng). Việc lấy bình luận do adapter nền tảng đảm nhiệm (Giai đoạn 5).

## ⚠️ Phụ thuộc

`pip install jieba snownlp` (lần đầu jieba sẽ dựng cache từ điển).

## Đầu vào

Dữ liệu bình luận, ba định dạng:
- `.txt`: mỗi dòng một bình luận
- `.json`: mảng chuỗi, hoặc mảng object (`--column` chỉ định trường, mặc định là content)
- `.csv`: `--column` chỉ định cột bình luận (mặc định cột đầu/content)

## Đầu ra (`outputs/<chủ đề>/`)

- Báo cáo JSON: phân bố và tỉ lệ cảm xúc + bình luận tiêu biểu tích cực lẫn tiêu cực + từ tần suất cao + cụm tần suất cao + số đếm và ví dụ của nhu cầu/phàn nàn/câu hỏi
- Bản tóm tắt đọc được ngay trên terminal

## Thực thi

Đường dẫn script (tính từ gốc dự án): `skills/openclaw/skill-comment-insights/scripts/comment_insights.py`.

```bash
python <skill>/scripts/comment_insights.py analyze -i comments.txt --top 20 \
  -o "outputs/<chủ đề>/report.json"
# CSV thì chỉ định cột
python <skill>/scripts/comment_insights.py analyze -i comments.csv --column "nội dung bình luận"
```

## Dùng kết quả thế nào

1. **Tỉ lệ cảm xúc**: tiêu cực cao → đọc các bình luận tiêu cực tiêu biểu để khoanh vùng vấn đề; phối với skill-community-ops để trả lời và xử lý khủng hoảng.
2. **Từ/cụm tần suất cao**: điểm quan tâm và chủ đề của người xem; có thể đưa sang chart-visualization/infographic để ra word cloud.
3. **Nhu cầu (demands)**: xin link/xin hướng dẫn/hỏi mua đồ giống → biến thẳng thành đề tài cho bài tiếp theo (phối với community-ops để nuôi ngược đề tài).
4. **Phàn nàn (complaints)**: tín hiệu vấn đề của sản phẩm hoặc dịch vụ → hậu kiểm để cải thiện (phối với skill-content-postmortem).

## Quy tắc

1. Cảm xúc là **giá trị xấp xỉ** từ baseline SnowNLP + hiệu chỉnh bằng từ điển mạng xã hội, dùng để xem xu hướng và tỉ lệ, không phải phán chính xác từng bình luận;
   quyết định quan trọng thì phải tự đọc lại các bình luận tiêu biểu, hoặc để LLM đọc kỹ những bình luận còn nghi ngờ.
2. Từ tần suất cao đã lọc theo từ loại (giữ danh/động/tính) + loại bỏ stopword, chỉ giữ những từ có thông tin.
3. Dữ liệu ít (<20 bình luận) thì tỉ lệ ít giá trị tham khảo, phải nói thật cỡ mẫu.
4. Chỉ phân tích, không trả lời; trả lời hay xử lý khủng hoảng thì dùng skill-community-ops.

## Nguồn tham khảo

Dùng lại bộ combo quen thuộc khi phân tích bình luận mạng xã hội: jieba tách từ tiếng Trung (#131 từ tần suất cao) + SnowNLP cảm xúc (#130), rồi chồng thêm
từ điển cảm xúc mạng xã hội (tiếng lóng mạng như juejuezi/yyds/bilei/fanche) để bù sai lệch của SnowNLP trên văn bản mạng xã hội. Phần đào nhu cầu
dùng khớp theo luật (hỏi mua/thắc mắc/phàn nàn), tất định và tái lập được.
