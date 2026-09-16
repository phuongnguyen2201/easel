---
name: skill-persona-check
description: >-
  Kiểm tra nhất quán persona và tone thương hiệu so với hồ sơ về định vị, ngách, hình thức, khán
  giả, phong cách, sở thích; chấm điểm, chỉ điểm lệch. Dùng khi người dùng nói "có đúng persona
  của tôi không", "giống tôi viết không", "kiểm tra tone". Bắt buộc có Profile, chưa có thì nhắc
  tạo.
layer: publish
---

# Kiểm tra nhất quán persona

> Kiểm tra nội dung có khớp persona của nhà sáng tạo và tone thương hiệu không, xuất điểm nhất quán và chẩn đoán điểm lệch.

## Khác biệt với các SKILL khác

| SKILL | Định vị | Điểm tập trung |
|---|---|---|
| **persona-check** (SKILL này) | Nhất quán persona/thương hiệu | Định vị kênh, đề tài, hình thức, khán giả, phong cách có khớp hồ sơ không |
| skill-quality-gate | Tuân thủ chuyên sâu + duyệt chất lượng | Quy tắc nền tảng, chất lượng nội dung |
| skill-publish-checklist | Kiểm tra đầy đủ | Có sót tiêu đề, sót ảnh bìa hay không |

## Điều kiện tiên quyết

SKILL này **bắt buộc có Profile mới chạy được**. Profile nên chứa các thông tin sau (một phần hoặc toàn bộ):

- `identity.md`: định vị kênh, ngách chủ đạo, hướng nội dung
- `style.md`: tone giọng, cách kể, hình ảnh và hình thức nội dung
- `audience.md`: khán giả mục tiêu và nhu cầu của họ
- `preferences.md`: điều nên làm, không làm và các lằn ranh đỏ
- `memory.md`: kinh nghiệm đã kiểm chứng và các lần vấp của hồ sơ hiện tại

Nếu không có Profile, trả về lời nhắc ngay, không kiểm tra.

## Đầu vào

- **Nội dung cần kiểm tra**: văn bản bài viết hoặc đường dẫn sản phẩm
- **Profile**: được nạp qua dấu hiệu `=== EASEL ACCOUNT PROFILE ===`, hoặc chỉ định tên hồ sơ

## Đầu ra

Xuất báo cáo nhất quán có cấu trúc, định dạng JSON:

```json
{
  "overall_score": 85,
  "verdict": "consistent | minor_drift | major_drift",
  "publish_allowed": true,
  "warning": "",
  "dimensions": [
    {
      "dimension": "tên chiều kiểm tra",
      "score": 90,
      "status": "aligned | drifted",
      "evidence": "văn bản bằng chứng cụ thể",
      "suggestion": "gợi ý điều chỉnh"
    }
  ],
  "drift_summary": ["danh sách tóm tắt các điểm lệch"],
  "rewrite_hints": ["gợi ý sửa cụ thể"],
  "summary": "tóm tắt một câu"
}
```

Chuẩn chấm điểm:
- 80-100: nhất quán (consistent), không cần cảnh báo persona
- 60-79: lệch nhẹ (minor_drift), cảnh báo rõ và đưa gợi ý sửa
- 0-59: lệch rõ (major_drift), cảnh báo nổi bật về lệch định vị kênh/đề tài/hình thức

**Điểm persona chỉ để nhắc, không phải quyền đăng bài.** `publish_allowed` luôn là `true`; điểm thấp không được chặn đăng,
không được bắt người dùng sửa bài chỉ để qua điểm. Khi người dùng đã nói rõ muốn đăng, hiện cảnh báo rồi đăng tiếp. An toàn nội dung,
tuân thủ nền tảng, thông tin nhạy cảm là các cổng chặn cứng độc lập, không thuộc phạm vi SKILL này, vẫn xử lý theo quy tắc tương ứng.

## Các bước thực hiện

### Step 1 - Đọc hiểu hồ sơ Profile

1. Kiểm tra có ngữ cảnh Profile không (dấu hiệu `=== EASEL ACCOUNT PROFILE ===`)
2. **Không có Profile** → xuất thẳng lời nhắc rồi dừng:
   ```
   Không phát hiện Profile của kênh, không thể kiểm tra nhất quán persona.
   Hãy tạo Profile trước: dùng skill-profile-builder để tạo có hướng dẫn, hoặc copy profiles/_template/ rồi điền tay.
   File style.md của Profile nên có: phong cách viết, tone giọng nền, nét tính cách, cách nói đặc trưng.
   ```
3. **Có Profile** → bắt buộc đọc `identity.md`, `style.md`, `audience.md`,
   `preferences.md`, `memory.md` của hồ sơ hiện tại; tình huống đăng bài thì đọc thêm `platforms.md`. Trích trước ngách chủ đạo, đề tài được phép,
   hình thức nội dung và khán giả, rồi mới trích tone giọng, cách dùng từ và thói quen nền tảng. Không được chỉ đọc `style.md` rồi chấm theo độ giống về ngôn ngữ.

### Step 2 - Phân tích nội dung cần kiểm tra

Phân tích ngôn ngữ đa chiều với nội dung đầu vào:

1. **Đề tài và ý đồ**: nội dung này nói gì, có thuộc ngách chủ đạo của kênh hoặc mở rộng hợp lý không
2. **Hình thức nội dung**: truyện, hoạt hình, video nói, review, bài ảnh... có khớp định vị kênh không
3. **Khán giả mục tiêu**: vấn đề nội dung giải quyết, giá trị cảm xúc và độ khó đọc có hướng tới khán giả trong hồ sơ không
4. **Phong cách ngôn ngữ**: tone giọng, cách dùng từ, kiểu câu, góc kể và sắc thái cảm xúc
5. **Nền tảng và sở thích**: có hợp nền tảng đích không, có chạm vào mục "không làm" đã ghi rõ trong hồ sơ không

### Step 3 - Đối chiếu từng chiều

Đối chiếu đặc trưng nội dung với đặc trưng Profile theo từng chiều, mỗi chiều chấm điểm độc lập:

| Chiều | Nội dung đối chiếu | Trọng số |
|---|---|---|
| **Định vị kênh và ngách nội dung** | Đề tài/chủ đề vs ngách chủ đạo, hướng nội dung, kho đề tài trong `identity.md` | 30% |
| **Nhất quán hình thức nội dung** | Truyện/hoạt hình/bài ảnh/video nói vs hình thức nội dung chính mà hồ sơ quy định | 15% |
| **Khớp khán giả mục tiêu** | Giá trị nội dung và nhóm người đọc/xem vs `audience.md` | 15% |
| **Tone giọng và phong cách kể** | Tone giọng, nhịp, góc nhìn vs `style.md` | 15% |
| **Tính cách và cách dùng từ** | Tính cách trong diễn đạt, vốn từ, cách nói đặc trưng vs hồ sơ | 10% |
| **Thích ứng nền tảng** | Dạng nội dung và cách diễn đạt vs `platforms.md` (không có nền tảng đích thì chấm điểm trung tính) | 10% |
| **Sở thích và kinh nghiệm** | `preferences.md` và `memory.md` của hồ sơ hiện tại | 5% |

Mỗi chiều chấm 0-100, tính tổng điểm theo trọng số.

Để tránh việc giống nhau về ngôn ngữ che lấp sai lệch căn bản, sau khi tính hãy áp các mức trần sau:

- **Định vị kênh và ngách nội dung < 40**: tổng điểm tối đa 59, bắt buộc kết luận `major_drift`.
- **Nhất quán hình thức nội dung < 40**: tổng điểm tối đa 69, ít nhất phải kết luận `minor_drift`.
- Chạm vào mục "không làm" hoặc lằn ranh đỏ đã chốt trong hồ sơ: tổng điểm tối đa 39, và phải chỉ rõ bằng chứng; nhưng vẫn chỉ cảnh báo, không quyết thay người dùng chuyện đăng hay không.
- Người dùng chủ động muốn lấn ngách chỉ có nghĩa đó là lựa chọn có ý thức, không vì thế mà thổi điểm nhất quán lên; chỉ cần ghi trong báo cáo "người dùng chủ động lấn ngách".

Ví dụ: `nhà sáng tạo hoạt hình hài 2D` đăng truyện chữ thuần kinh dị, dù vẫn khẩu ngữ, giàu hình ảnh, có twist,
ngách kênh và hình thức nội dung vẫn lệch nặng, tổng điểm bắt buộc dưới 60, không được vì kỹ thuật ngôn ngữ mà cho 80+.

### Step 4 - Khoanh vùng điểm lệch

Với các chiều có score < 80, đưa bằng chứng lệch cụ thể:

1. **Trích nguyên văn**: chỉ ra đoạn hoặc câu cụ thể trong nội dung bị lệch persona
2. **Giải thích đối chiếu**: nói rõ cách diễn đạt mà Profile kỳ vọng vs cách diễn đạt thực tế
3. **Mức nghiêm trọng**: đánh dấu điểm lệch đó có ảnh hưởng cảm nhận persona tổng thể không

### Step 5 - Sinh gợi ý chỉnh sửa

Với mỗi điểm lệch, đưa gợi ý sửa có thể làm được ngay:

- Cụ thể tới mức từ: từ ngữ nên thay
- Cụ thể tới mức câu: kiểu câu nên điều chỉnh
- Cụ thể tới mức đoạn: hướng nên viết lại

### Step 6 - Xuất báo cáo

Tổng hợp điểm của mọi chiều, sinh báo cáo có cấu trúc:

1. Tính tổng điểm theo trọng số và áp mức trần cho lệch nghiêm trọng
2. Kết luận verdict (consistent / minor_drift / major_drift)
3. Liệt kê tóm tắt toàn bộ điểm lệch
4. Đưa gợi ý sửa đã sắp theo thứ tự ưu tiên
5. `publish_allowed` luôn xuất `true`; dưới 80 điểm thì điền `warning` thật nổi bật
6. Sinh tóm tắt một câu, nói rõ "đây là nhắc nhở về persona, không chặn người dùng đăng bài"

## Nhận biết Profile

- **Có Profile**: trích đầy đủ đặc trưng persona từ Profile, đối chiếu trên mọi chiều. Đây là chế độ làm việc chuẩn của SKILL này.
- **Không có Profile**: **không chạy được**. Nhắc thẳng người dùng tạo Profile, nói rõ cần những gì (style, tone, personality), rồi dừng thực thi. Đây là SKILL duy nhất trong Easel bắt buộc phải có Profile.

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
