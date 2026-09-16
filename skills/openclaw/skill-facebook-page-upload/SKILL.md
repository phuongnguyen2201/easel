---
name: skill-facebook-page-upload
description: >-
  Đăng bài lên Trang Facebook qua Meta Graph API: bài chữ, một ảnh, album nhiều ảnh hoặc video,
  kèm hashtag; chạy thử trước rồi mới đăng thật. Dùng khi người dùng nói "đăng lên Facebook",
  "đăng Trang Facebook", "up bài lên fanpage".
layer: publish
---

# Đăng Trang Facebook

> Đăng nội dung đã duyệt lên Trang Facebook bằng Meta Graph API. Không dùng trình duyệt tự động.
> Thiết kế chi tiết: `agent_docs/adapter-facebook-page.md`.

## Điều kiện

- `.env` có `FB_APP_ID` và `FB_CLIENT_TOKEN` (tuỳ chọn `FB_PAGE_ID`, `FB_GRAPH_VERSION`). Kiểm tra bằng Skill Library trên web, **không mở `.env`**.
- Tài khoản Facebook là quản trị viên của Trang và đã cấp quyền `pages_show_list`, `pages_manage_posts`.
- Đã đăng nhập (trang Tài khoản trên web, hoặc lệnh `login` bên dưới). Kiểm tra nhanh bằng `whoami`.

## Quy trình bắt buộc

1. Kiểm tra đăng nhập: `whoami` phải trả `"loggedIn": true`. Nếu `false`, nhờ người dùng đăng nhập ở trang Tài khoản; không tự đăng bài.
2. **Chạy thử (không `--exec`)** với đúng nội dung, tiêu đề, hashtag và media sẽ đăng. Đọc JSON trả về (`kind`, `page`, `message`) và cảnh báo của content_guard.
3. Cho người dùng xem nội dung, Trang đích và loại bài; **chỉ thêm `--exec` khi người dùng xác nhận rõ ràng**.
4. Báo lại `url` từ dòng JSON cuối. Mã thoát khác 0 thì báo lỗi, không thử lại mù quáng.

Không bao giờ tự thêm `--allow-unsafe`. Exit 7 nghĩa là nội dung chứa thông tin nội bộ (khoá, địa chỉ nội bộ…): sửa nội dung rồi chạy thử lại.

## Lệnh

Chạy từ gốc dự án.

```bash
# Kiểm tra đăng nhập và Trang
python skills/shared/scripts/facebook_publish.py whoami
python skills/shared/scripts/facebook_publish.py pages
python skills/shared/scripts/facebook_publish.py pages --set-default 1234567890

# Đăng nhập từ dòng lệnh (in mã thiết bị; QR ở outputs/_login/facebook-page.png)
python skills/shared/scripts/facebook_publish.py login --status-file outputs/_login/facebook-page.json

# Chạy thử (không đăng)
python skills/shared/scripts/facebook_publish.py publish --title "Tiêu đề" --content "Nội dung" --tags "easel,marketing"

# Đăng thật: bài chữ kèm link
python skills/shared/scripts/facebook_publish.py publish --content "Nội dung" --link "https://example.com" --exec

# Đăng thật: một ảnh hoặc album (ảnh phân tách bằng dấu phẩy)
python skills/shared/scripts/facebook_publish.py publish --content "Nội dung" --images outputs/<chủ đề>/anh-1.png,outputs/<chủ đề>/anh-2.png --topic "<chủ đề>" --exec

# Đăng thật: video
python skills/shared/scripts/facebook_publish.py publish --title "Tiêu đề video" --content "Mô tả" --video outputs/<chủ đề>/video.mp4 --topic "<chủ đề>" --exec
```

| Tham số | Ý nghĩa |
|---|---|
| `--title` | Video: tiêu đề video. Bài chữ/ảnh: dòng đầu của bài (bỏ qua nếu nội dung đã mở đầu bằng nó) |
| `--content` | Nội dung bài hoặc mô tả video |
| `--tags` | Hashtag phân tách bằng dấu phẩy, tự thêm `#`, bỏ khoảng trắng |
| `--images` / `--video` | Chọn một trong hai; không kèm media là bài chữ |
| `--link` | Link đính kèm, chỉ cho bài chữ |
| `--page-id` | Trang đích; mặc định Trang mặc định đã lưu |
| `--topic` | Ghi bước đăng vào `outputs/<chủ đề>/.easel.json` |
| `--offline` | Chạy thử không gọi mạng |
| `--exec` | Đăng thật |

## Mã thoát

| Mã | Ý nghĩa | Việc cần làm |
|---|---|---|
| 0 | Thành công (hoặc chạy thử xong) | Báo `url` |
| 3 | Chưa đăng nhập, token hết hạn, mã đăng nhập hết hạn | Nhờ người dùng đăng nhập lại |
| 4 | Thiếu quyền trên Trang | Nhờ người dùng kiểm tra vai trò Trang và quyền đã cấp |
| 5 | Đầu vào sai (thiếu tệp, sai định dạng, vừa ảnh vừa video) | Sửa tham số |
| 6 | Bị Meta giới hạn tần suất | Đợi rồi thử lại sau |
| 7 | content_guard chặn | Xoá thông tin nội bộ khỏi nội dung |

## Ghi nhận

- Chạy từ agent: sau khi đăng thành công, script tự ghi `outputs/_schedule.json` qua `calendar_ops.record_publish`. Đăng từ trang Publish trên web thì web tự ghi, script bỏ qua.
- Token lưu ngoài `outputs/`; đăng xuất ở trang Tài khoản sẽ xoá token.
