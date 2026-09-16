---
name: ai-video-gen
description: >-
  Sinh video AI từ 0: chữ→video, ảnh→video, người ảo từ khung đầu; bất đồng bộ qua provider cắm
  được (VIDEO_PROVIDER), người dùng tự có API key. Dùng khi người dùng nói "AI tạo video", "làm
  ảnh động", "video người ảo". video-strategy chọn chiến lược, video-editing dựng, clipify cắt
  clip.
layer: produce
---

# Sinh video AI

> Chữ sinh video / ảnh sinh video / người ảo dẫn từ khung đầu. Bọc `shared/scripts/ai_video.py`, nhiều provider cắm được, gửi bất đồng bộ→poll→tải về. **Người dùng tự có API key** (cấu hình trong `.env`).

## Trước khi chạy: cấu hình API key

> **Luật sắt về đường dẫn kiểm tra cấu hình**: trước tiên `cd` vào thư mục gốc dự án Easel ghi ở cuối `AGENTS.md`, xác nhận thư mục hiện tại có `.env` và `skills/shared/scripts/`, rồi mới chạy registry, `check` hay lệnh sinh nội dung. Không được đổi sang `./shared/scripts/...` của workspace, cũng không được kết luận là chưa cấu hình chỉ vì `env` / `printenv` không hiện biến.

Chọn provider trước và điền key tương ứng vào `.env`, rồi chạy `check` để kiểm tra offline:

```bash
python skills/shared/scripts/ai_video.py check --provider dashscope
```

| provider | Dịch vụ | Cần cấu hình trong .env |
|----------|------|-------------|
| `dashscope` | Alibaba Tongyi Wanxiang Wan | `DASHSCOPE_API_KEY` (tuỳ chọn `DASHSCOPE_VIDEO_MODEL`/`DASHSCOPE_BASE_URL`; tương thích tên cũ `DASHSCOPE_MODEL`) |
| `ark` | Volcengine Seedance | `ARK_API_KEY` (tuỳ chọn `ARK_MODEL`/`ARK_BASE_URL`) |
| `kling` | Kuaishou Kling | `KLING_ACCESS_KEY` + `KLING_SECRET_KEY` (xác thực JWT) |
| `openai-compatible` | Endpoint /videos dùng chung | `VIDEO_API_KEY` + `VIDEO_BASE_URL` (tuỳ chọn `VIDEO_MODEL`) |
| `xhs-maas` | MaaS nội bộ Xiaohongshu (happyhorse chữ/ảnh sinh video)| `XHS_MAAS_API_KEY` (tuỳ chọn `XHS_MAAS_VIDEO_BASE`/`XHS_MAAS_T2V_MODEL`/`XHS_MAAS_I2V_MODEL`). Bất đồng bộ kiểu DashScope + header api-key, nối thẳng mạng nội bộ |
| `agnes` | Agnes (agnes-video-2.5-flash)| `AGNES_API_KEY` (tuỳ chọn `AGNES_BASE_URL`/`AGNES_MODEL`/`AGNES_SIZE`). Tạo theo chuẩn OpenAI Videos + poll ở endpoint riêng; **mặc định có audio gốc** (mô tả âm thanh ngay trong prompt); ra mạng ngoài qua proxy |

Cũng có thể đặt `VIDEO_PROVIDER` để khỏi truyền `--provider` mỗi lần.

Trước khi chạy hãy gọi `model_registry.py configured --group video --env-file .env`: chỉ có một provider khả dụng thì chọn thẳng nó; nhiều provider khả dụng mà người dùng chưa chỉ định thì liệt kê provider/model để hỏi lần này dùng cái nào, không tự ý lấy giá trị mặc định.

## Đầu vào

> **Chốt chặn xác nhận khung hình**: khi người dùng hoặc task phía trên chưa nói rõ ngang/dọc (hoặc 16:9 / 9:16 / tỉ lệ cụ thể), phải hỏi lại và chờ xác nhận trước mọi lệnh sinh nội dung hay lệnh tốn tiền; không được suy ngầm từ nền tảng, Profile hay giá trị mặc định của script. Đã rõ rồi thì không hỏi lại.

- Chữ sinh video: mô tả khung hình/góc máy/phong cách (prompt)
- Ảnh sinh video: một ảnh đầu vào (đường dẫn local hoặc URL) + mô tả chuyển động tuỳ chọn
- Tuỳ chọn: thời lượng `--duration`, khung hình `--ratio` (16:9 / 9:16 / 1:1), model `--model`, audio gốc `--audio auto|on|off`

## Đầu ra

File video sinh ra; bắt buộc dùng `-o` để chỉ vào `outputs/<chủ đề>/`. Tác vụ bất đồng bộ tự poll đến khi xong rồi mới tải về.

## Các bước thực hiện

1. **Xác nhận cấu hình và năng lực**: chạy `check` trước, rồi chạy `capabilities --provider <p> --model <m>`. short-drama không được đoán model có hỗ trợ audio gốc hay không theo tên thương hiệu; model mới thì đăng ký năng lực và trường request bằng `VIDEO_CAPABILITIES_JSON`, không cần sửa luồng gọi.
   - **`probe-dialogue`** (dùng cho short-drama): gửi thật 1 lần sinh + ASR, đo xem model có nói **đúng từng chữ** lời thoại chỉ định không, kết luận `dialogue_faithful` rồi cache lại - short-drama dựa vào đó để chọn đối thoại gốc, hay "sinh không lời thoại + lồng tiếng hậu kỳ". Cách dùng `probe-dialogue --provider <p> --model <m>`.
2. **Viết prompt cho chuẩn**: video AI rất nhạy với prompt, theo [Chuẩn viết prompt video AI](../video-strategy/references/ai-video-prompting.md) mà mô tả khung hình, chuyển động máy, phong cách và thời lượng. Video ngắn dọc dùng `--ratio 9:16`.
3. **Chữ sinh video**:
   ```bash
   python skills/shared/scripts/ai_video.py text2video --provider dashscope \
     --prompt "hoàng hôn bên biển, máy tiến chậm, tông màu ấm, chất điện ảnh" --ratio 9:16 --duration 5 \
     --audio auto \
     -o outputs/<chủ đề>/clip.mp4
   ```
4. **Ảnh sinh video / làm ảnh chuyển động / khung đầu người ảo**:
   ```bash
   python skills/shared/scripts/ai_video.py image2video --provider kling \
     --image outputs/<chủ đề>/cover.png --prompt "nhân vật mỉm cười vẫy tay, tóc bay nhẹ" \
     -o outputs/<chủ đề>/clip.mp4
   ```
5. **Gia công tiếp**: đoạn video sinh ra có thể đưa cho `video_ops.py` (nối/gắn phụ đề/gắn BGM/đổi ngang dọc), `auto-subtitle` (phụ đề), `tts-voiceover` (lồng tiếng) để ráp thành phim hoàn chỉnh, hoặc đưa thẳng vào luồng end-to-end `auto-short-video`.

## Nhận biết Profile

- Có Profile: lấy thiên hướng phong cách hình ảnh từ `style.md` bơm vào prompt; `platforms.md` chỉ dùng để gợi ý khung hình, không thay được xác nhận của người dùng.
- Không có Profile: xác nhận ngang/dọc trước, rồi sinh theo tỉ lệ đã chốt.

## Lưu ý

- API sinh video đều chạy bất đồng bộ và **tốn khá nhiều thời gian** (vài chục giây tới vài phút) + **tính tiền theo lượng dùng**, phải xác nhận với người dùng trước.
- Tên model/trường dữ liệu của từng provider khác nhau theo phiên bản, đều ghi đè được bằng `--model` hoặc env; nếu báo lỗi thì đối chiếu tài liệu chính thức mới nhất mà chỉnh.
- `--audio auto` chỉ ánh xạ các trường đã biết theo capability profile; khai báo năng lực không đảm bảo chất lượng, tải về vẫn phải kiểm bằng ffprobe/ASR/soát hình. Gateway mặc định có tiếng nhưng chưa rõ trường bật/tắt thì đừng đoán mà bơm tham số.
