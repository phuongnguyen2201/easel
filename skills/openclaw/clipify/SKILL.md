---
name: clipify
description: >-
  Tự trích clip hay (điểm gây cười) từ video dài nói tiếng Anh, chuyển dọc 9:16 với pan bám mặt,
  đốt phụ đề từng chữ. Dùng khi người dùng nói "cắt clip từ video dài", "trích đoạn hay", "phụ đề
  từng chữ". video-highlights tổng quát hơn (mọi ngôn ngữ/livestream), chuyển dọc tĩnh ổn hơn.
layer: produce
---

# Clipify

Tìm những khoảnh khắc hài nhất trong một video, cắt ra thành các clip đứng riêng, tuỳ chọn chuyển khung 16:9 → 9:16 (pan bám mặt hoặc split-screen), rồi đốt phụ đề từng chữ kiểu opus.

## Đầu vào

- Đường dẫn file video (người dùng đưa; chưa có thì hỏi)
- Tuỳ chọn: khung hình muốn ra (9:16, 16:9, 1:1) - chưa nói thì hỏi sau khi đã chốt danh sách clip ứng viên
- Tuỳ chọn: kiểu phụ đề - chưa nói thì hỏi trước khi làm phụ đề

## Công cụ (chỉ đi đường nhanh nhất)

- **Whisper:** `whisper --model tiny.en --word_timestamps True --output_format json` (nhanh gấp ~10 lần `small.en`; chất lượng đủ tốt cho tiếng Anh). Với video không phải tiếng Anh: `--model base` (bỏ `--language`).
- **ffmpeg:** giải mã bằng phần cứng là tuỳ chọn và tuỳ nền tảng - dùng `-hwaccel auto`, hoặc bỏ luôn (macOS: `videotoolbox`; Linux: `vaapi`/`cuda`/không có). Thêm `-preset ultrafast` cho các bản render nháp. Dùng `-c:v libx264 -crf 20` cho bản master cuối.
- **Numpy** để căn tiếng (FFT cross-correlation). Không cần scipy/cv2.
- **Scripts:** `<skill-dir>/scripts/` (`<skill-dir>` là thư mục chứa file SKILL.md này - thường là `~/.claude/skills/clipify/`)
  - `analyze.py` - dựng dòng thời gian người nói từ hai file chuyển động ROI
  - `build_pan.py` - sinh biểu thức crop theo x cho ffmpeg, cắt cứng
  - `build_ass.py` - sinh phụ đề ASS kiểu opus từ JSON của whisper
  - `audio_align.py` - tìm offset của một clip con trong file nguồn dài

Thư mục làm việc: `/tmp/clipify/` (mkdir lúc bắt đầu, giữ lại file trung gian để debug).

---

## Quy trình

### Bước 1 - Tìm các đoạn hài nhất

```bash
mkdir -p /tmp/clipify
ffmpeg -y -i "$VIDEO" -vn -ac 1 -ar 16000 /tmp/clipify/audio.wav
whisper /tmp/clipify/audio.wav --model tiny.en --word_timestamps True --output_format json --output_dir /tmp/clipify --language en
```

Đọc file JSON vừa ra (hoặc bản `.txt`) rồi chọn 3-5 clip ứng viên. Các tín hiệu hài cần quét:

- **Câu chốt và phản ứng:** những từ như "what", "wait", "no way", tiếng cười, "haha", chửi thề
- **Khoảnh khắc lật kèo:** câu hỏi dẫn dắt → câu trả lời bất ngờ
- **Khoảng lặng ngượng:** segment Whisper có khoảng trống dài, hoặc từ đệm ("uh", "um")
- **Tự trào / câu một dòng đáng trích:** câu khẳng định ngắn, tách ra vẫn đứng được
- **Đỉnh âm lượng:** dò bằng `ffmpeg -af volumedetect`, hoặc tìm đoạn đối đáp qua lại nhanh (các segment Whisper ngắn xen kẽ)

Với mỗi ứng viên, đề xuất: `[start, end, why-it's-funny, suggested title]`. Nhắm clip dài 10-25 giây. Đưa danh sách ra cho người dùng xác nhận/chọn.

### Bước 2 - Cắt từng clip đã chọn

```bash
ffmpeg -y -ss "$START" -t "$DURATION" -i "$VIDEO" -c copy /tmp/clipify/clip_$N.mp4
```

(Dùng `-c copy` để cắt tức thì. Chỉ encode lại khi cần cắt chính xác tới từng frame.)

### Bước 3 - Chốt khung hình đầu ra

Hỏi người dùng (bỏ qua nếu họ đã nói rõ): "9:16 (TikTok / Reels), 16:9 (YouTube), hay 1:1 (feed Instagram)?"

### Bước 4 - Nếu 16:9 → 9:16: pan giữa hai mặt hay split-screen

Dò tỉ lệ nguồn bằng `ffprobe`. Nếu nguồn là 16:9 mà đích là 9:16, hãy hỏi:

> "Có hai hướng: **(a) pan cắt cứng** bám theo người đang nói (mỗi lúc chỉ một mặt trên khung), hoặc **(b) split-screen** xếp chồng, thấy cả hai mặt. Bạn chọn hướng nào?"

Bỏ qua câu hỏi này nếu chỉ có một mặt (clip một người nói). Clip một người thì chỉ cần crop giữa.

#### Bước 4a - Pan giữa hai mặt (nên dùng cho hội thoại talking-head cắt nhanh)

1. **Xác định hai vùng ROI của mặt.** Lấy một frame mẫu: `ffmpeg -ss <middle> -i <clip> -frames:v 1 /tmp/clipify/probe.jpg`. Đọc ảnh đó. Ước lượng vùng miệng + cằm của từng mặt theo `x,y,w,h` trong hệ pixel của nguồn. (Không cần cv2 - camera đứng yên trong một clip; một frame là đủ.) Kiểm lại bằng cách vẽ khung:

   ```bash
   ffmpeg -i probe.jpg -vf "drawbox=x=$LX:y=$LY:w=$LW:h=$LH:color=cyan@0.9:t=4,drawbox=x=$RX:y=$RY:w=$RW:h=$RH:color=magenta@0.9:t=4" verify.jpg
   ```

   Lặp **tối đa hai lần**. Khung nên phủ miệng + cằm và tránh tay/micro. Đừng chỉnh quá kỹ - phép so sai khác frame rất dễ tính.

2. **Trích năng lượng chuyển động từng frame trong mỗi ROI:**

   ```bash
   ffmpeg -y -i clip.mp4 -filter_complex "
   [0:v]split=2[a][b];
   [a]crop=$LW:$LH:$LX:$LY,format=gray,tblend=all_mode=difference,signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG:file=/tmp/clipify/L.txt[la];
   [b]crop=$RW:$RH:$RX:$RY,format=gray,tblend=all_mode=difference,signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG:file=/tmp/clipify/R.txt[ra]
   " -map "[la]" -f null - -map "[ra]" -f null -
   ```

3. **Dựng dòng thời gian người nói** (thời gian bám tối thiểu 1.0s - câu chen ngắn sẽ nhập vào người nói trước đó):

   ```bash
   python3 <skill-dir>/scripts/analyze.py /tmp/clipify/L.txt /tmp/clipify/R.txt 1.0 > /tmp/clipify/segments.json
   ```

4. **Chọn toạ độ x để pan** cho dải dọc 9:16 lấy từ nguồn. Với nguồn W=1920 và đích W=1080, dải crop rộng 608.
   - LEFT_X = `face_left_center_x - 304` (kẹp ≥ 0)
   - RIGHT_X = `face_right_center_x - 304` (kẹp ≤ source_W - 608)

5. **Sinh biểu thức x cắt cứng rồi render:**

   ```bash
   EXPR=$(python3 <skill-dir>/scripts/build_pan.py /tmp/clipify/segments.json $LEFT_X $RIGHT_X)
   ffmpeg -y -i clip.mp4 -filter_complex \
     "[0:v]crop=608:1080:x='$EXPR':y=0,scale=1080:1920:flags=lanczos[v]" \
     -map "[v]" -map 0:a -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
     -c:a aac -b:a 192k /tmp/clipify/clip_panned.mp4
   ```

   Mặc định coi nguồn là 1920×1080; nguồn 4K thì hoặc downscale trước, hoặc nhân đôi toàn bộ toạ độ.

#### Bước 4b - Split-screen (lúc nào cũng thấy cả hai mặt)

Hai ô xếp chồng, mỗi ô 1080×960. Ô của người đang nói nằm trên - lớp overlay đảo mỗi lần đổi người nói.

```
[0:v]split=2[a0][a1];
[a0]crop=Wcrop:Hcrop:LX_tile:LY_tile,scale=1080:960,split=2[lt0][lt1];
[a1]crop=Wcrop:Hcrop:RX_tile:RY_tile,scale=1080:960,split=2[rt0][rt1];
[lt0][rt0]vstack[layoutL];
[rt1][lt1]vstack[layoutR];
[layoutL][layoutR]overlay=0:0:enable='<RIGHT_SPEAKER_ENABLE>'[v]
```

Dựng `<RIGHT_SPEAKER_ENABLE>` từ `segments.json` theo dạng `between(t,a,b)+between(t,a,b)+...` trên các đoạn của người bên phải. Ô crop nên nhắm khoảng 720×640 quanh mỗi mặt (tỉ lệ 1.125:1 để khớp 1080×960).

### Bước 5 - Thêm phụ đề

Hỏi một lần (chỉ khi người dùng chưa chọn kiểu):

> "Có ba kiểu phụ đề: **opus** (chữ trắng to đậm, tô vàng từ đang đọc), **karaoke** (cụm 4 chữ, tô xanh lá), **minimal** (Helvetica gọn, không tô). Hoặc gửi một mẫu bạn thích."

Nếu họ gửi ảnh/mẫu tham chiếu: bám sát font, cỡ chữ, độ đậm, màu, vị trí và hiệu ứng hết mức có thể - viết tay một file ASS riêng hoặc mở rộng `build_ass.py`.

Không thì dùng preset:

```bash
# Chạy lại whisper trên clip đã cắt để mốc thời gian tính đúng từ đầu clip
whisper /tmp/clipify/clip_panned.mp4 --model tiny.en --word_timestamps True --output_format json --output_dir /tmp/clipify --language en
python3 <skill-dir>/scripts/build_ass.py /tmp/clipify/clip_panned.json /tmp/clipify/captions.ass opus
```

Đốt phụ đề vào hình:

```bash
ffmpeg -y -i /tmp/clipify/clip_panned.mp4 -vf "subtitles=/tmp/clipify/captions.ass" \
  -c:v libx264 -preset fast -crf 20 -c:a copy "$OUTPUT.mp4"
```

### Bước 6 - Bàn giao

- Lưu mỗi file thành phẩm vào `<source_dir>/clipify_out/` (mkdir nếu chưa có)
- In một dòng cho mỗi clip: tên, độ dài, chỗ nào hài, đường dẫn đầu ra
- In đường dẫn đầu ra đầu tiên (hoặc mở luôn - Linux `xdg-open <path>`, macOS `open <path>`) để người dùng xem thử
- Mời người dùng chỉnh tiếp (đổi kiểu phụ đề, đổi ROI, chuyển sang split-screen, canh lại thời gian phụ đề)

---

## Lỗi hay gặp (rút từ các lần chạy trước - đừng lặp lại)

- **Đừng chỉnh ROI quá kỹ.** Tối đa hai vòng. Phép so sai khác chuyển động rất dễ tính - ROI rộng phủ miệng + cằm vẫn chạy tốt dù không canh đúng tâm miệng.
- **Coi chừng cắt cảnh nằm trong clip.** Chạy `ffmpeg -filter:v "select='gt(scene,0.3)',showinfo" -f null -` để đếm số cú cắt. Nếu clip 16:9→9:16 có nhiều cú cắt, ROI mặt cố định chỉ đúng với cảnh chủ đạo; báo trước cho người dùng, rồi mời họ hoặc chọn clip quay một mạch, hoặc chấp nhận khung lệch ở các đoạn cắt.
- **Độ phân giải nguồn rất quan trọng.** Nguồn 4K thì hoặc downscale về 1920×1080 trước (nhanh hơn, đủ đẹp cho đầu ra 9:16), hoặc nhân đôi mọi toạ độ ROI/pan.
- **Phụ đề đã đốt sẵn trong nguồn.** Một số clip "raw" vẫn dính phụ đề. Gặp vậy thì tìm bản master không phụ đề bằng cross-correlation âm thanh (`audio_align.py`) rồi cắt từ bản đó.
- **Đừng chạy whisper trên cả file nguồn dài nếu một clip ngắn là đủ.** Chạy whisper trên clip đã cắt sau Bước 2; chỉ whisper toàn bộ nguồn ở Bước 1 khi cần transcript để tìm đoạn hài.
- **Nói kế hoạch trong một dòng rồi làm.** Đừng tường thuật từng vòng lặp.
