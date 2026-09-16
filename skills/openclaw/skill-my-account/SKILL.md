---
name: skill-my-account
description: >-
  Tra tài khoản đã đăng nhập trong Easel (Facebook, TikTok, YouTube, Zalo): danh tính, follower,
  bài đăng; không hỏi tên/link. Dùng khi người dùng hỏi "tôi đã đăng nhập kênh nào", "tôi là ai",
  "follower của tôi", "tôi đăng gì gần đây". Phân tích bình luận → skill-comment-insights.
layer: general
---

# Tài khoản của tôi (my-account)

Bạn là "trợ lý tự tra tài khoản". Khi người dùng hỏi về **tài khoản hoặc nội dung của chính họ** (tôi là ai / đã đăng nhập kênh nào / bao nhiêu người theo dõi /
gần đây đăng gì / có những bài nào), **hãy dùng công cụ ở đây tra trạng thái đăng nhập và dữ liệu trong hệ thống trước, đừng vội hỏi người dùng tên kênh hay link trang cá nhân**
- những thông tin này hệ thống đã có sẵn (người dùng đã quét mã ở trang "Tài khoản", trạng thái đăng nhập được lưu ngay trên máy).

## Nguyên tắc cốt lõi

- **Tra trước, đừng hỏi**: người dùng nói "tài khoản của tôi / bài của tôi / người theo dõi của tôi / gần đây đăng gì", chạy thẳng script tra tài khoản đang đăng nhập.
- **Tra không ra mới nói**: chỉ khi thực sự **chưa đăng nhập nền tảng đó**, hoặc nền tảng không trả về mục dữ liệu đó, mới nói thật với người dùng "bạn chưa đăng nhập X, vào trang 'Tài khoản' quét mã là xem được" - chứ không mặc định là người dùng chưa cung cấp thì không làm được.
- **Nhận diện nền tảng theo ngữ cảnh**: hội thoại đang nói nền tảng nào thì tra nền tảng đó; người dùng không nói rõ mà chỉ đăng nhập một nền tảng thì tra nền tảng đó; đăng nhập nhiều nơi mà không chỉ định thì chạy whoami tra hết một lượt rồi hỏi muốn xem cái nào.

## Cách chạy (Playwright, chạy được headless)

Thống nhất đi qua script xác định (CWD = gốc dự án). Thứ được đọc là **trạng thái đăng nhập ở máy** (`~/.easel-browser-profiles/<nền tảng>Profile`),
không phải hồ sơ (Profile); đăng nhập một lần dùng lâu dài, đăng nhập/đăng xuất thao tác ở trang "Tài khoản" trên Web, SKILL này chỉ đọc chứ không đổi trạng thái đăng nhập.

| Phụ thuộc | Mô tả |
|------|------|
| playwright + nhân chromium | `account_stats.py check` để kiểm tra |
| Đã quét mã đăng nhập | Khi chưa đăng nhập script trả về `logged_in/loggedIn=false`, dựa vào đó nhắc vào trang tài khoản |
| Mạng | Proxy được xử lý **tự động theo nền tảng** (Xiaohongshu đi thẳng, còn lại đi qua env), không cần chỉ định tay |

## Phạm vi năng lực

- **Tra danh tính đăng nhập `whoami`** (nhẹ, vài giây): nền tảng đó đã đăng nhập chưa + biệt danh + ảnh đại diện. Trả lời "tôi là ai / đã đăng nhập chưa / tên kênh của tôi".
- **Tra dữ liệu sáng tạo `account_stats fetch`**: người theo dõi / lượt thích / đang theo dõi / số bài đăng + **danh sách bài đăng (tiêu đề + link + dữ liệu từng bài)**. Trả lời "tôi có bao nhiêu người theo dõi / gần đây đăng gì / tôi có những bài nào / được bao nhiêu lượt thích".
- **Bình luận**: lấy và phân tích bình luận của một bài đăng không thuộc SKILL này - dùng adapter nền tảng để lấy bình luận + **skill-comment-insights** (phân tích cảm xúc/nhu cầu).

## Nền tảng hỗ trợ

whoami: Xiaohongshu / Douyin / Zhihu / Kuaishou / Video Channels.
account_stats fetch `--platform`: `xiaohongshu` / `douyin` / `kuaishou` / `zhihu` / `weixin-channels`.

> Mức đầy đủ dữ liệu mỗi nền tảng mỗi khác (hiện trạng trên máy thật): **Xiaohongshu** đủ nhất (người theo dõi/lượt thích/đang theo dõi/biến động 7 ngày gần nhất + bài viết kèm link và ảnh bìa);
> **Zhihu** (người theo dõi = người quan tâm, lượt thích = tổng lượt tán thành + danh sách bài viết); **Kuaishou** trung tâm sáng tạo không cho tổng người theo dõi/lượt thích, chỉ có tương tác 7 ngày gần nhất + danh sách bài đăng;
> **Douyin/Video Channels** sau khi đăng nhập thì lấy theo trang sáng tạo của từng bên. Mục nào không lấy được thì hiển thị đúng "-", không bịa không chắp vá.

## Quy trình thực thi

```
Xác định người dùng hỏi về "danh tính" hay "dữ liệu"
  ├ Danh tính (tôi là ai/đã đăng nhập kênh nào) → whoami (chạy một lượt cho từng nền tảng)
  └ Dữ liệu (người theo dõi/bài đăng/lượt thích/gần đây đăng gì) → account_stats.py fetch --platform <nền tảng>
        ├ logged_in=true  → trích trường tương ứng với câu hỏi để trả lời (số người theo dõi / tiêu đề + link N bài gần nhất ...)
        └ logged_in=false → nhắc "bạn chưa đăng nhập X, vào trang 'Tài khoản' quét mã"
```

## Phân vai với các SKILL khác

- **SKILL này (my-account)** = tra nhanh "tài khoản/dữ liệu/bài đăng của tôi", đọc trạng thái đăng nhập là trả lời ngay.
- **skill-publish-analytics / skill-social-performance-review** = **phân tích hiệu quả chuyên sâu** sau khi đăng (so chuẩn, hậu kiểm).
- **skill-content-postmortem** = **quy luật viral/hậu kiểm nội dung** sau khi đã đăng.
- **skill-account-diagnosis** = **chẩn đoán kênh/khám sức khoẻ xây kênh** (bệnh gì → thuốc nấy).
- **skill-comment-insights** = phân tích cảm xúc/nhu cầu từ bình luận đã thu thập.
- Khi cần **chiều sâu**, dữ liệu của SKILL này có thể làm đầu vào cho chúng.

## Ràng buộc

- Chỉ đọc trạng thái đăng nhập, không sửa; đăng nhập/đăng xuất để người dùng vào trang "Tài khoản" trên Web.
- Chưa đăng nhập thì đừng kết thúc bằng lỗi, hãy nói rõ vào đâu để đăng nhập.
- Đưa link bài đăng nguyên trạng (link explore của Xiaohongshu, link zhuanlan/p của Zhihu; Kuaishou không có link công khai thì nói rõ).
- Khi nền tảng đổi giao diện khiến trường lấy về rỗng, nói thật "lần này không lấy được mục này", có thể bật `EASEL_STATS_DEBUG=1` để dump nội dung mà dò (xem commands).

## Câu lệnh mẫu

Toàn bộ câu lệnh (whoami từng nền tảng, account_stats fetch, xử lý chưa đăng nhập, phân tích trường, debug dump) xem
**[references/commands.md](references/commands.md)**.
