---
name: skill-publish-notify
description: >-
  Đẩy thông báo sau khi đăng: thành công hay thất bại đều gửi kết quả và link tới Telegram, Slack
  hoặc webhook bất kỳ (kèm Feishu/DingTalk/WeCom); thuần script, không phụ thuộc ngoài. Dùng khi
  người dùng nói "báo khi đăng xong", "thông báo Telegram", "gửi webhook", "đăng xong nhắn tôi".
layer: publish
---

# Đẩy thông báo sau khi đăng

> Sau khi đăng nội dung, đẩy kết quả về bot nhóm IM của team hoặc webhook bất kỳ. Đi qua `scripts/notify.py` (thuần thư viện chuẩn, không phụ thuộc).
> Thường nối với các SKILL đăng bài: đăng thành công -> đẩy "đã đăng + link"; thất bại -> đẩy lỗi.

## Kênh hỗ trợ

| Kênh | Cần có | Mô tả |
|------|------|------|
| `feishu` | webhook bot nhóm | Feishu/Lark, hỗ trợ tiêu đề rich text |
| `dingtalk` | webhook (tuỳ chọn thêm secret ký) | Bot nhóm DingTalk |
| `wecom` | webhook bot nhóm | WeCom (WeChat Work) |
| `telegram` | bot token + chat_id | Telegram Bot |
| `slack` | Incoming Webhook | Slack |
| `generic` | webhook bất kỳ | Gửi `{"text": ...}` |

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Kênh | có | Một trong bảng trên |
| webhook / token | có | Địa chỉ bot nhóm (telegram dùng token+chat_id) |
| Nội dung thông báo | có | Phần thân, tiêu đề tuỳ chọn |

## Thực thi

Đường dẫn script (tính từ gốc dự án): `skills/openclaw/skill-publish-notify/scripts/notify.py` (`send -h`).

```bash
# Nhóm Feishu
python <skill>/scripts/notify.py send --channel feishu \
  --webhook "https://open.feishu.cn/open-apis/bot/v2/hook/xxx" \
  --title "Easel đăng thành công" --text "<Chủ đề kỳ này> đã đăng lên TikTok+Facebook\nLink: ..."

# DingTalk (bật ký secret)
python <skill>/scripts/notify.py send --channel dingtalk \
  --webhook "https://oapi.dingtalk.com/robot/send?access_token=xxx" \
  --secret "SECxxx" --text "Đã đăng"

# Telegram
python <skill>/scripts/notify.py send --channel telegram \
  --token "123:ABC" --chat-id "456" --text "Đã đăng"

# Chạy thử trước để xem payload
python <skill>/scripts/notify.py send --channel feishu --webhook URL --text "..." --dry-run
```

## Quy tắc

1. Trước khi gửi hãy dùng `--dry-run` cho người dùng xác nhận nội dung và nhóm đích, rồi mới gửi thật.
2. webhook / token là thông tin nhạy cảm, đọc từ cấu hình người dùng hoặc .env, không hard-code, không để lộ.
3. Nội dung thông báo gọn: trạng thái + tiêu đề + nền tảng + link là đủ.
4. Nhóm DingTalk nếu bật thiết lập bảo mật "ký secret" thì bắt buộc kèm `--secret`.
5. Phải trả HTTP 200 và mã thành công riêng của từng nhà thì mới tính là thành công, nếu không thì nhắc người dùng kiểm tra webhook.

## Nguồn tham khảo

Bot nhóm của các nhà đều theo giao thức chuẩn "POST JSON tới webhook": Feishu msg_type, DingTalk/WeCom msgtype,
Telegram Bot sendMessage, Slack Incoming Webhook. DingTalk ký secret bằng HMAC-SHA256. Thuần urllib,
không cần thư viện bên thứ ba như apprise.
