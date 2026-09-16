---
name: skill-quality-gate
description: >-
  Kiểm tra trước khi đăng qua hai cửa: tuân thủ (từ nhạy cảm, từ tuyệt đối, quy tắc nền tảng) và
  chất lượng (đầy đủ, dễ đọc, hợp nền tảng); chốt đăng được/cần sửa/không đạt. Dùng khi người dùng
  nói "kiểm tra tuân thủ", "có từ nhạy cảm không", "duyệt trước khi đăng", "chất lượng đủ chưa".
layer: publish
---

# Cửa chất lượng trước khi đăng

> Một SKILL lo trọn hai cửa kiểm: dò rủi ro tuân thủ + soát chất lượng sản phẩm.

## Đầu vào

Người dùng đưa nội dung cần kiểm: văn bản, đường dẫn ảnh, đường dẫn video, hoặc trộn lẫn.
Tuỳ chọn: nền tảng định đăng.

## Đầu ra

```json
{
  "overall_verdict": "✅ đăng được | ⚠️ cần sửa | ❌ không đạt",
  "platform": "tên nền tảng hoặc generic",
  "compliance": {
    "risk_level": "low|medium|high",
    "issues": [{ "type": "", "severity": "", "text": "", "reason": "", "suggestion": "" }],
    "passed_checks": []
  },
  "quality": {
    "score": "✅|⚠️|❌",
    "dimensions": [{ "name": "", "score": "", "note": "" }]
  },
  "top_fixes": ["đề xuất sửa 1", "đề xuất sửa 2", "đề xuất sửa 3"]
}
```

## Các bước thực hiện

### Cửa một: dò tuân thủ

1. Đọc nội dung (văn bản và/hoặc ảnh)
2. Nạp bộ quy tắc tuân thủ chung → `references/general-rules.md`
3. Theo Profile hoặc nền tảng người dùng chỉ định mà nạp bộ quy tắc tương ứng (các bộ hiện có đều là quy định của nền tảng Trung Quốc):
   - Xiaohongshu → `references/platform-xiaohongshu.md`
   - Douyin → `references/platform-douyin.md`
   - Bilibili → `references/platform-bilibili.md`
   - Không có nền tảng → chỉ dùng quy tắc chung
4. Dò từng mục: từ tuyệt đối, vi phạm quy định y tế, nội dung cấm, hạn chế riêng của nền tảng (danh sách từ nhạy cảm và luật quảng cáo trong references là của Trung Quốc)
5. Tổng hợp kết quả tuân thủ

### Cửa hai: soát chất lượng

1. Nhận diện loại sản phẩm (văn bản/ảnh/video)
2. Kiểm từng chiều → `references/review-dimensions.md`
3. Đưa kết luận ba mức → `references/review-levels.md`
   - ✅ Đạt: đăng được luôn
   - ⚠️ Có tì vết: nên chỉnh nhẹ rồi đăng
   - ❌ Không đạt: phải làm lại
4. Nếu kết luận là ❌, theo `references/rework-rules.md` mà đưa hướng dẫn làm lại

### Phán định tổng hợp

- Tuân thủ rủi ro cao → tổng thể ❌ không đạt
- Soát chất lượng ra ❌ (mức phải làm lại) → tổng thể ❌ không đạt
- Tuân thủ rủi ro thấp + chất lượng ✅ → tổng thể ✅ đăng được
- Các tổ hợp còn lại → tổng thể ⚠️ cần sửa
- Xuất Top 3 đề xuất sửa ưu tiên

## Nhận biết Profile

- **Có Profile**: đọc platform để nạp quy tắc nền tảng, kiểm mức hợp phong cách
- **Không có Profile**: chỉ kiểm tuân thủ chung + tiêu chuẩn chất lượng chung
