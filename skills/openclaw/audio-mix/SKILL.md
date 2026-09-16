---
name: audio-mix
description: >-
  Trộn lời dẫn + nhạc nền + hiệu ứng thành một track audio: BGM tự lặp cho đủ dài, ducking tự hạ
  nhạc lúc nói. Dùng khi người dùng nói "mix audio", "ghép giọng đọc với nhạc nền", "thêm BGM cho
  voice", "ducking". audio-editing concat nối trước–sau; video-editing bgm gắn nhạc vào video.
layer: produce
---

# Trộn audio (lời dẫn + BGM + hiệu ứng)

> Trộn nhiều đường tiếng **chồng lên nhau cùng lúc** thành một track, năng lực cốt lõi là **ducking (tự hạ nhạc)** - khi lời dẫn cất tiếng thì tự động hạ
> nhạc nền xuống, giọng người rõ, nhạc không lấn. Tất cả chạy qua `skills/shared/scripts/audio_mix.py`,
> **đừng tự ghép tay amix/sidechaincompress**.

> Nối trước sau theo thứ tự (đoạn này tiếp đoạn kia) xem **audio-editing** `concat`; gắn nhạc cho video xem **video-editing** `bgm`;
> khử ồn xem **audio-denoise**.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Lời dẫn | Không | Track chính video nói/lồng tiếng (đưa vào thì thời lượng đầu ra bám theo nó, và kích hoạt ducking) |
| BGM | Không | Nhạc nền (tự lặp cho đủ độ dài lời dẫn) |
| Hiệu ứng | Không | Một hoặc nhiều hiệu ứng, chỉ định được mốc thời gian xuất hiện của từng cái |

(Ít nhất phải có một trong ba. Điển hình nhất: "lời dẫn + BGM".)

## Đầu ra (`outputs/<chủ đề>/`)

- Audio một track sau khi trộn (mp3/wav/m4a, theo đuôi file xuất)
- Báo cáo: số track, thời lượng, có ducking hay không

## Các bước thực hiện

Đường dẫn script (tính từ gốc dự án): `skills/shared/scripts/audio_mix.py` (`mix -h` để xem tham số).

```bash
# Lời dẫn + BGM (mặc định tự ducking, BGM lặp cho đủ độ dài lời dẫn)
python skills/shared/scripts/audio_mix.py mix \
  --voice narration.mp3 --bgm music.mp3 --bgm-volume 0.25 \
  -o outputs/<chủ đề>/final.mp3

# Tắt ducking (chỉ chồng tiếng)
python skills/shared/scripts/audio_mix.py mix --voice v.mp3 --bgm m.mp3 --no-duck -o out.mp3

# Lời dẫn + hiệu ứng theo mốc (giây 3.5 một tiếng ding, giây 8 một tiếng whoosh)
python skills/shared/scripts/audio_mix.py mix --voice v.mp3 \
  --sfx ding.wav --sfx-at 3.5 --sfx whoosh.wav --sfx-at 8 -o out.mp3
```

## Chỉnh tham số

- **Giọng người bị nhạc lấn**: hạ `--bgm-volume` (mặc định 0.25) hoặc kiểm tra ducking đã bật chưa (mặc định bật).
- **Ducking quá gắt / nhạc giật cục**: dùng `--no-duck` rồi tự tay hạ `--bgm-volume`.
- **BGM ngắn hơn lời dẫn**: mặc định tự lặp; không muốn lặp thì dùng `--bgm-loop-off`.
- **Hiệu ứng quá to/quá nhỏ**: `--sfx-volume` (mặc định 0.9).

## Quy tắc

1. Có lời dẫn thì thời lượng đầu ra = độ dài lời dẫn, BGM tự lặp/cắt cho khớp và fade out ở cuối.
2. Lời dẫn + BGM mặc định bật ducking (ưu tiên giọng người); không cần thì ghi rõ `--no-duck`.
3. `--sfx` và `--sfx-at` phải bằng nhau về số lượng (hoặc không đưa --sfx-at thì tất cả mặc định 0s).
4. Trộn audio không chuẩn hoá độ to (giữ nguyên tương quan âm lượng); cần đồng nhất độ to thì dùng audio-editing `normalize` trước.
5. Sản phẩm gom hết vào `outputs/<chủ đề>/`.

## Nguồn tham khảo

Ducking dùng ffmpeg `sidechaincompress` (lấy giọng người làm tín hiệu điều khiển để nén BGM), là cách làm chuẩn của podcast/video nói để giữ giọng
người luôn rõ; chồng nhiều track thì dùng `amix`. Đấu nối sidechain và canh lặp được gói thành script xác định.
