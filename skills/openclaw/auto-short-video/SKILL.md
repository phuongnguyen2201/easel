---
name: auto-short-video
description: >-
  Một câu chủ đề → video ngắn hoàn chỉnh dạng nói/tin: tự nối lời → ảnh/AI video → giọng đọc → phụ
  đề → BGM → ghép. Dùng khi người dùng nói "video một chạm", "làm video từ chủ đề", "làm giúp một
  video". Cốt truyện/nhiều tập → short-drama, chỉ kịch bản → video-script, một đoạn →
  ai-video-gen.
layer: produce
---

# Video ngắn một chạm (điều phối đầu-cuối)

> Nhập một chủ đề, tự động ra một video ngắn. SKILL này là **lớp điều phối**: nối các mảnh sản xuất có sẵn thành một dây chuyền -
> nội dung (video-script) → ảnh cho từng câu (ai-image-gen) hoặc clip (ai-video-gen) → giọng đọc (tts-voiceover) →
> phụ đề (auto-subtitle) → BGM (ai-music) → **ghép (scripts/assemble.py)**.
> Đúc kết từ cách làm engine video ngắn tự động của Pixelle-Video / MoneyPrinterTurbo.

## Đầu vào

- Chủ đề / nội dung (bắt buộc)
- Tuỳ chọn: thời lượng mục tiêu, phong cách, có cần giọng đọc/phụ đề/BGM, ảnh do AI sinh hay tư liệu của người dùng
- **Chốt cứng khung hình**: khi người dùng hoặc task phía trên chưa nói rõ ngang/dọc (hoặc 16:9/9:16/độ phân giải cụ thể), phải hỏi lại và chờ xác nhận trước khi sản xuất hay gọi API tốn phí; không được im lặng suy ra từ nền tảng, Profile hay giá trị mặc định, đã rõ rồi thì đừng hỏi lại

## Đầu ra

Video thành phẩm ghi vào `outputs/<chủ đề>/final.mp4`; ảnh phân cảnh, giọng đọc, phụ đề và storyboard ghi vào `outputs/<chủ đề>/assets/`.

## Các bước thực thi (cắt bớt theo nhu cầu, khâu nào thiếu API key thì tự hạ cấp hoặc hỏi lại)

1. **Viết kịch bản phân cảnh**: dùng [video-script](../video-script/SKILL.md) viết chủ đề thành lời video nói, tách thành N câu (mỗi câu một phân cảnh), mỗi câu kèm một mô tả hình ảnh.

2. **Sinh hình ảnh** (mỗi phân cảnh một ảnh/một clip):
   - Có API key ảnh → [ai-image-gen](../ai-image-gen/SKILL.md) chạy text2img từng câu (theo khung hình đã chốt)
   - Cần chuyển động → [ai-video-gen](../ai-video-gen/SKILL.md) text2video/image2video
   - Người dùng có tư liệu riêng → dùng [image-editing](../image-editing/SKILL.md) `pad` về khung hình đã chốt
   - Không có gì cả → theo khung hình đã chốt mà chọn thẻ ảnh (dọc dùng card-xiaohongshu/poster-hero, ngang dùng card-quote) rồi pad, tránh lệch khung hình.

3. **Giọng đọc**: [tts-voiceover](../tts-voiceover/SKILL.md) tổng hợp nội dung thành lời video nói (ra kèm SRT). **Có cấu hình `VOICE_PROVIDER` thì mặc định dùng giọng hay của bản đóng** (có cảm xúc, như người thật), thiếu key mới lùi về edge (máy móc) - muốn giọng đọc không "cứng" thì nhất định phải cấu hình key bản đóng. Không cần giọng đọc thì mới bỏ qua.

4. **Phụ đề**: dùng SRT đi kèm TTS, hoặc chạy [auto-subtitle](../auto-subtitle/SKILL.md) trên file giọng đọc; cũng có thể để assemble tự sinh từ caption của từng phân cảnh.

5. **BGM**: [ai-music](../ai-music/SKILL.md) sinh nhạc, hoặc dùng nhạc người dùng đưa. Tuỳ chọn.

6. **Ghép thành phẩm**: viết đống tư liệu ở trên thành storyboard JSON rồi gọi bộ ghép:
   ```bash
   python skills/openclaw/auto-short-video/scripts/assemble.py assemble \
     --storyboard "outputs/<chủ đề>/assets/storyboard.json" \
     -o "outputs/<chủ đề>/final.mp4"
   ```
   Cấu trúc storyboard (ảnh/clip chọn một, narration/bgm/subtitle tuỳ chọn, thiếu duration thì chia đều theo giọng đọc):
   ```json
   {
     "size": "<kích thước đã chốt, ví dụ 1080x1920 hoặc 1920x1080>",
     "image_motion": "ken-burns",
     "shots": [
       {"image": "outputs/<chủ đề>/assets/shot1.png", "duration": 3, "caption": "câu thứ nhất", "motion": "static"},
       {"video": "outputs/<chủ đề>/assets/clip2.mp4", "caption": "câu thứ hai"}
     ],
     "narration": "outputs/<chủ đề>/assets/voice.mp3",
     "bgm": "outputs/<chủ đề>/assets/bgm.mp3",
     "subtitle": "outputs/<chủ đề>/assets/voice.srt"
   }
   ```
   `image_motion` đặt chuyển động mặc định cho toàn bộ ảnh, từng cảnh có thể ghi đè bằng `motion`: ảnh chụp dùng `ken-burns`, slide/biểu đồ/giao diện có chữ bắt buộc dùng
   `static` (thu phóng đúng tỉ lệ + bù viền, không cắt, không trượt).
   Bộ ghép tự lo: sinh khung tĩnh hay Ken Burns theo `image_motion`, bù viền cho vừa khung hình, nối cảnh, trộn giọng đọc + BGM (BGM tự hạ nhỏ), khắc phụ đề.

7. **Bàn giao**: ra final.mp4, kèm một câu ghi chú sản xuất (đã dùng những khâu nào, khâu nào bị hạ cấp).

## Nguyên tắc điều phối

- **Thiếu mảnh vẫn chạy**: khâu nào thiếu API key ảnh/video/TTS thì tự hạ cấp (thẻ ảnh đỡ lưng / bỏ giọng đọc), không chặn cả dây chuyền, và nói thật với người dùng là đã hạ cấp cái gì.
- **Ra Plan trước**: khi đụng nhiều API tốn phí (sinh ảnh/sinh video/sinh nhạc), phải nói trước sẽ gọi những gì, ước lượng thời gian và chi phí, người dùng xác nhận rồi mới chạy.
- **Lưu lại sản phẩm trung gian**: ảnh phân cảnh, giọng đọc, phụ đề và storyboard đều ghi vào `outputs/<chủ đề>/assets/`, tiện thay riêng một món rồi ghép lại.

## Nhận biết Profile

- Có Profile: lấy tông giọng và phong cách hình ảnh từ `style.md` xuyên suốt nội dung lẫn prompt sinh ảnh; `platforms.md` chỉ dùng để gợi ý khung hình/thời lượng, khung hình vẫn phải chốt lại; `preferences.md` lọc lằn ranh đỏ.
- Không có Profile: chốt ngang/dọc trước, rồi dùng phong cách video nói phổ thông.
