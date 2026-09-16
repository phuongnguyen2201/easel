---
name: skill-content-calendar-log
description: >-
  Nền lịch nội dung thống nhất: tự ghi mọi lần đăng (trang đăng/chat), lịch đã xếp, sự kiện nền
  tảng/ngày lễ vào một timeline; Agent đọc lại trước khi lập kế hoạch. Dùng khi người dùng nói
  "trong lịch có gì", "tiếp theo đăng gì", "ghi sự kiện vào lịch". Hiệu quả từng bài →
  skill-publish-log.
layer: attribute
---

# Nền lịch nội dung thống nhất

> Ghi lần đăng + lịch đã xếp + sự kiện nền tảng vào một dòng thời gian, để khâu lập kế hoạch đọc lại. Sản phẩm chính là những gì thấy ở trang "Lịch nội dung" trên Web.

## Định vị tầng dữ liệu

Kho lưu trữ có thẩm quyền duy nhất là `outputs/_schedule.json` (**cùng một file** với `/api/schedule` của trang lịch trên Web). Mỗi bản ghi:

| Trường | Mô tả |
|------|------|
| `kind` | `content` (nội dung/bài đăng) \| `event` (sự kiện nền tảng/ngày lễ/ngày đặc biệt) |
| `status` | riêng cho content: `idea`/`draft`/`scheduled`/`published` |
| `platform` `title` `date` `time` `note` `url` | dùng chung |
| `source` | `manual`/`publish-page`/`chat`/`scheduler` (truy được nguồn) |
| `event_type` `end_date` | riêng cho event |

- **Đăng bài tự vào kho, không cần làm tay**: trang đăng bài và trang chat cuối cùng đều gọi script publisher (`xhs_publish`/`douyin_publish`/`web_publisher`/`bili_upload`), script tự ghi một bản ghi `published` khi `--exec` chạy thành công (và đồng thời chuyển tiếp sang `skill-publish-log`). Đừng ghi bù thủ công nữa, tránh trùng.
- **Phân vai với publish-log**: nền này quản dòng thời gian (khi nào đăng gì, lịch chờ đăng, mốc của nền tảng, nhắc chỗ cần bù nội dung); `skill-publish-log` quản chỉ số của từng bài (lượt đọc/lượt thích/hậu kiểm). Một lần gọi record-publish ghi cả hai kho, không lệch nhau.

## Tình huống kích hoạt

- **Đọc lại để lập kế hoạch** (hay dùng nhất): trước khi chọn đề tài/xếp lịch thì xem lịch trước - nhịp đăng từng nền tảng, khoảng trống bị đứt bài, lịch chờ đăng, sự kiện nền tảng sắp tới có thể bắt trend.
- **Ghi sự kiện nền tảng**: đưa ngày lễ/đợt sale lớn/sự kiện nền tảng vào đúng ngày (thường đi kèm `skill-event-calendar` để tra ra mốc rồi nhập hàng loạt).
- **Xếp lịch/ghi bù thủ công**: lịch người dùng nói miệng hoặc nội dung đã đăng ngoài hệ thống.

## Lệnh

```bash
# Đọc lại tóm tắt để lập kế hoạch (Agent bắt buộc đọc trước khi lên kế hoạch): nhịp đăng/khoảng đứt bài từng nền tảng + lịch chờ đăng + mốc sắp tới + gợi ý
python skills/shared/scripts/calendar_ops.py context --days 14 --gap 5

# Lịch đã xếp + sự kiện trong N ngày tới (--kind để chỉ xem content hoặc event)
python skills/shared/scripts/calendar_ops.py upcoming --days 14 [--kind event]

# Rải một lượt các ngày lễ cố định của một năm (ngày dương cố định + âm lịch quy đổi qua lunar.py + kiểu "thứ mấy của tuần thứ N" như Ngày của Mẹ/Black Friday; idempotent, chạy lại nhiều lần được)
python skills/shared/scripts/calendar_ops.py seed-holidays --year 2026

# Ghi một sự kiện nền tảng/ngày lễ/ngày đặc biệt
python skills/shared/scripts/calendar_ops.py add-event --title "11.11" --date 2026-11-11 \
  --event-type "thương mại điện tử" [--end-date 2026-11-12] [--platform TikTok] [--note "ghi chú"]

# Nhập hàng loạt sự kiện từ JSON của skill-event-calendar (trùng tên trùng ngày thì khử trùng, idempotent; stdin hoặc --file)
python skills/shared/scripts/calendar_ops.py import-events --file events.json

# Lọc và tra cứu
python skills/shared/scripts/calendar_ops.py list [--kind content] [--platform Facebook] \
  [--since 2026-08-01] [--until 2026-08-31]

# Ghi bù thủ công một bài đã đăng (chỉ dùng khi bài không đăng qua script publisher, cần nhập tay)
python skills/shared/scripts/calendar_ops.py record-publish --platform Facebook --title "Tiêu đề" \
  --type "ảnh + chữ" [--url ...] [--tags "AI,hướng dẫn"] [--note ...] [--source manual]
```

`suggestions` mà `context` in ra (nhắc đứt bài / mốc sắp tới chưa có lịch) nên chuyển nguyên văn cho người dùng, làm căn cứ cho "tiếp theo làm gì".

## Phân vai với các SKILL khác

| SKILL | Quan hệ |
|-------|------|
| `skill-content-calendar` (plan) | Sinh bảng lịch đăng theo tháng; trước khi xếp thì đọc `context` của nền này, xếp xong ghi kế hoạch trở lại (`add-event`/hoặc xếp lịch ở frontend) |
| `skill-event-calendar` (discover) | Tra ngày lễ/mốc sắp tới; tra xong dùng `import-events` ghi vào lịch |
| `skill-publish-log` (attribute) | Nền chỉ số; bản ghi đăng bài đã được script tự đồng bộ, không cần gọi lại |

## Nhận biết Profile

- Có Profile: `platform` suy được từ nền tảng chính trong `platforms.md`; nhắc đứt bài của `context` kết hợp nền tảng chính của kênh sẽ có ý nghĩa hơn.
- Không có Profile: bao phủ toàn bộ bản ghi, không lọc theo kênh.

> Nguồn gốc tự phát triển và tài liệu tham khảo xem `EASEL-META.md` cùng thư mục.
