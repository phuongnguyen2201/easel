---
name: skill-trending-topics
description: >-
  Lấy bảng xếp hạng trend thời gian thực từ các nguồn đã cấu hình, lọc theo ngách kênh, gợi ý đề
  tài phái sinh. Dùng khi người dùng nói "hôm nay có trend gì", "mọi người đang bàn gì", "bắt
  trend", "top trending". skill-news-intelligence làm bản tin ngành sâu theo ngày, không lấy bảng
  trend.
layer: discover
---

# Phát hiện trend

> Kéo dữ liệu bảng trend thời gian thực từ nhiều nền tảng, lọc ra trend liên quan tới ngách của nhà sáng tạo, xuất đề tài sáng tạo lại làm được ngay.

## Đầu vào

Người dùng cung cấp các thông tin sau trong prompt (đều là tuỳ chọn):

- **Nền tảng**: Weibo / Douyin / Zhihu / Toutiao / Bilibili (mặc định: Weibo + Douyin)
- **Ngách/lĩnh vực**: ví dụ "công nghệ - đồ số", "làm đẹp", "công sở" (có Profile thì tự động trích ra)
- **Mục đích**: lướt bảng trend / tìm đề tài sáng tạo lại / bắt trend viết nội dung

## Đầu ra

```markdown
# Bản tin trend nhanh
Ngày: {date}
Nền tảng: {platforms}

## 🔥 Top 10 trend toàn nền tảng
| # | Nền tảng | Chủ đề | Độ hot | Mức liên quan tới bạn |

## 🎯 Đề tài sáng tạo lại đề xuất (3-5 đề tài)
### Đề tài 1: {tiêu đề}
- Nguồn trend: {nền tảng + chủ đề gốc}
- Góc sáng tạo lại: {cắt vào thế nào}
- Định dạng gợi ý: {bài ảnh-chữ/video ngắn/thread}
- Tính thời điểm: {cần đăng nhanh cỡ nào}

## 📊 Insight xu hướng
{chủ đề trùng nhau giữa các nền tảng, xu hướng đi lên, trend kế tiếp có thể đoán trước}
```

## Các bước thực hiện

1. **Kéo dữ liệu bảng trend** - dùng web_fetch gọi **những API công ích đã kiểm chứng là dùng được dưới đây** (trả về JSON, không cần key, môi trường đã cấu hình proxy ra ngoài nên tự có hiệu lực). Kéo theo nền tảng mà người dùng chỉ định, không chỉ định thì mặc định kéo Weibo + Douyin.

   🚫 **Tuyệt đối không web_fetch trang chủ nền tảng** (weibo.com / zhihu.com / douyin.com) **hay tophub.today** - chúng chặn crawl theo IP máy chủ, trả về trang đăng nhập / captcha / 403 chứ không phải dữ liệu. Cũng đừng dùng API bên thứ ba không có trong danh sách này (vvhan / tenapi... chưa kiểm chứng, đừng dùng).

   **Nguồn chính 60s (v2, đường dẫn bắt buộc có `/v2/`)** base `https://60s.viki.moe`:
   - Weibo `https://60s.viki.moe/v2/weibo` | Douyin `https://60s.viki.moe/v2/douyin`
   - Zhihu `https://60s.viki.moe/v2/zhihu` | Toutiao `https://60s.viki.moe/v2/toutiao`
   - Xiaohongshu `https://60s.viki.moe/v2/rednote` | Baidu `https://60s.viki.moe/v2/baidu/hot`
   - Trả về `{"code":200,"data":[{"title","hot","url"},...]}` (một số endpoint lồng trong `data.data`, khi parse nhớ kiểm tra cả hai).

   **Nguồn dự phòng xxapi (dùng khi một endpoint của nguồn chính lỗi, nhất là Bilibili)** base `https://v2.xxapi.cn`:
   - Weibo `/api/weibohot` | Douyin `/api/douyinhot` | Bilibili `/api/bilibilihot` | Baidu `/api/baiduhot`

   Thứ tự hạ cấp: 60s → xxapi → nếu tất cả đều lỗi thì báo thật và nhờ người dùng dán ảnh chụp/nội dung bảng trend. **Danh sách đầy đủ và các lưu ý xem `shared/hotlist-apis.md` (tuỳ chọn, các URL ở trên đã đủ dùng)**.
2. **Parse dữ liệu** - trích tiêu đề và giá trị độ hot của từng mục trend, sắp xếp theo độ hot.
3. **Khớp ngách** - nếu có Profile hoặc người dùng đã chỉ định ngách thì lọc ra các chủ đề liên quan tới ngách, ghi mức liên quan (cao/trung bình/thấp). Không có thông tin ngách thì hiển thị nguyên Top 10.
4. **Phân tích sáng tạo lại** - từ các chủ đề liên quan, chọn 3-5 đề tài đáng làm lại:
   - Có tính tranh luận hoặc còn không gian bàn luận
   - Khớp với định vị của nhà sáng tạo
   - Cửa sổ thời điểm còn đủ rộng (không phải trend đã nguội)
   - Làm ra được nội dung khác biệt (không phải bê nguyên xi)
5. **Insight xu hướng** - phân tích chủ đề trùng nhau giữa các nền tảng (cùng lúc lên bảng trend của Weibo và Douyin nghĩa là sự kiện lớn), xu hướng đi lên, trend kế tiếp có thể đoán trước.
6. **Xuất kết quả** - bàn giao theo định dạng đầu ra.

## Nhận biết Profile

- **Khi có Profile**:
  - Đọc `identity.md` để lấy ngách và định vị, tự động lọc trend liên quan
  - Đọc `style.md` để khớp hình thức nội dung cho gợi ý sáng tạo lại
  - Đọc `platforms.md` để ưu tiên kéo bảng trend của nền tảng mà nhà sáng tạo đang hoạt động
  - Đọc `audience.md` để xác định trend nào hấp dẫn với khán giả mục tiêu
- **Khi không có Profile**:
  - Hiển thị Top 10 toàn nền tảng, không lọc theo ngách
  - Gợi ý sáng tạo lại đưa ra góc tiếp cận chung
  - Ghi chú thêm "chỉ định ngách hoặc cung cấp Profile sẽ lọc trend chính xác hơn"
