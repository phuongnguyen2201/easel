---
name: skill-cross-platform-publish
description: >-
  Đăng một nội dung lên nhiều nền tảng trong một lượt: thích ứng số chữ, tỉ lệ, hashtag, loại
  nội dung theo từng nền tảng rồi giao cho script đăng tương ứng. Dùng khi người dùng nói "đăng
  lên nhiều nền tảng", "đăng cùng lúc Facebook và TikTok", "phân phối đa nền tảng".
layer: publish
---

# Đăng đa nền tảng

> Một bản gốc → nhiều nền tảng. `scripts/publish_dispatch.py` kiểm tra ràng buộc, định tuyến
> nền tảng → SKILL đăng và in lệnh chạy thử. **Thích ứng nội dung do bạn (LLM) làm; đăng thật do
> script đăng của từng nền tảng làm.**

## Nền tảng → SKILL đăng

| Nền tảng | Trạng thái | SKILL đăng |
|---|---|---|
| `facebook-page` | ✅ Đã có adapter | `skill-facebook-page-upload` |
| `youtube` | ⏳ Chưa có | — |
| `tiktok` | ⏳ Chưa có | — |
| `zalo-oa` | ⏳ Chưa có | — |
| `instagram` | ⏳ Chưa có | — |
| `threads` | ⏳ Chưa có | — |

Nền tảng chưa có adapter: chỉ soạn bản thích ứng để người dùng đăng tay, **không giả vờ đã đăng**.

## Đầu vào

Manifest nội dung (JSON), `media_type` ∈ `text | image | video | article`:
```json
{
  "content": {"title": "...", "body": "...", "tags": ["...", "..."], "media_type": "image", "topic": "<chủ đề>"},
  "platforms": ["facebook-page", "tiktok"]
}
```

## Quy trình

Chạy từ gốc dự án.

```bash
# Xem toàn bộ nền tảng và ràng buộc
python skills/openclaw/skill-cross-platform-publish/scripts/publish_dispatch.py platforms

# 1) Lập kế hoạch: kiểm tra vượt giới hạn + nền tảng nào đăng được
python skills/openclaw/skill-cross-platform-publish/scripts/publish_dispatch.py plan --manifest outputs/<chủ đề>/assets/publish-plan.json
```

2. **Thích ứng nội dung cho từng nền tảng** (bạn làm), theo `constraints_note` và `warnings`:
   rút gọn tiêu đề/nội dung, bớt hashtag, đổi giọng theo nền tảng. Cần đổi tỉ lệ video thì dùng
   **video-reframe**. Có thể dùng **skill-content-repurposing** cho bản viết lại.
3. **Kiểm tra persona trước khi đăng** (khi có Profile): chạy **skill-persona-check** cho từng bản
   thích ứng, rồi `python skills/shared/scripts/persona_gate.py check --score 85`. Dưới ngưỡng thì
   báo điểm, điểm lệch và gợi ý sửa, nhưng không chặn nếu người dùng đã quyết đăng.
4. **Chạy thử từng nền tảng `publishable`** bằng `dry_run_command` trong kế hoạch, ví dụ Facebook:
   ```bash
   python skills/shared/scripts/facebook_publish.py whoami
   python skills/shared/scripts/facebook_publish.py publish --title "Tiêu đề" --content "Bản cho Facebook" --tags "vimo,fomc" --images outputs/<chủ đề>/anh-1.png --topic "<chủ đề>"
   ```
5. **Cho người dùng xem toàn bộ bản thích ứng + nền tảng đích, chờ xác nhận rõ ràng**, rồi mới
   chạy lại đúng lệnh đó kèm `--exec`. Không bao giờ tự thêm `--allow-unsafe`; exit 7 là
   content_guard chặn, sửa nội dung rồi chạy thử lại.
6. **Sau khi đăng**: báo `url` từng nền tảng; nền tảng `manual_only` thì đưa bản thích ứng để đăng
   tay. Có thể dùng **skill-publish-notify** để đẩy kết quả, **skill-short-link** để tạo link UTM.
   Ghi bước tổng hợp vào manifest chủ đề:
   ```bash
   python skills/shared/scripts/manifest.py record --topic "<chủ đề>" --layer publish --skill skill-cross-platform-publish --summary "Đã đăng: Facebook Page; đăng tay: TikTok"
   ```
   > Script đăng đã tự ghi `_schedule.json` và nhật ký đăng khi `--exec` thành công; không ghi tay
   > thêm (sẽ bị trùng). Chỉ gọi **skill-publish-log** khi cần bổ sung điểm persona.

## Profile

- Có Profile: nền tảng đích mặc định lấy từ `platforms.md`; giọng và hashtag theo `style.md`;
  giới hạn tuân thủ theo `preferences.md`.
- Không có Profile: hỏi người dùng muốn đăng lên nền tảng nào.

## Quy tắc

1. **Không đăng nguyên một bản lên mọi nền tảng** — mỗi nền tảng thích ứng theo ràng buộc và thói quen riêng.
2. Luôn chạy `plan` trước và xử lý hết `warnings`.
3. Luôn chạy thử trước; chỉ `--exec` sau khi người dùng xác nhận.
4. Một nền tảng lỗi thì báo lỗi nền tảng đó và tiếp tục các nền tảng còn lại; không thử lại mù quáng.
5. Đăng theo lịch dùng **skill-publish-scheduler**.
