---
name: skill-news-intelligence
description: >-
  Gom tin báo/trang tin ngành, tin chuyên ngành, động thái thương mại nền tảng, lọc theo ngách, ra
  bản tin tình báo có cấu trúc kèm đề tài làm được. Dùng khi người dùng nói "tin ngành hôm nay",
  "bản tin ngày", "ngành có gì mới". Tin sâu theo ngày; trend theo phút → skill-trending-topics.
layer: discover
---

# Tổng hợp tình báo tin tức

> Lấy nội dung chuyên sâu từ báo ngành tiếng Trung và các nguồn tin chuyên ngành, lọc theo ngách của nhà sáng tạo,
> sinh bản tin tình báo tiếng Việt có cấu trúc, kèm hướng đề tài làm được ngay.

## Phân vai với skill-trending-topics

| | skill-trending-topics | skill-news-intelligence (SKILL này) |
|---|---|---|
| Lấy gì | **Bảng hot search realtime** của Weibo/Douyin/Zhihu/Toutiao/Bilibili | **Bài chuyên sâu / tin nhanh** của báo ngành tiếng Trung |
| Độ tươi | Theo phút, đuổi trend | Theo ngày, nhìn xu hướng ngành |
| Dùng để | Bắt trend, ra đề tài làm lại nhanh | Đề tài chuyên sâu, quan sát ngành, tích trữ nội dung |
| Đầu ra | Xếp hạng hot search + góc làm lại | Bản tin tình báo + hướng đề tài |

**Quy tắc ranh giới**: SKILL này không lấy bảng hot search (đó là việc của trending-topics).
Nếu người dùng hỏi "hôm nay có gì hot/đang trend gì", định tuyến sang skill-trending-topics.
SKILL này lo chuyện "ngành gần đây có gì mới, có đề tài nào đáng đào sâu".

## Đầu vào

Người dùng đưa các thông tin sau trong prompt (đều không bắt buộc):

- **Ngách/lĩnh vực**: vận hành kênh cá nhân / công nghệ đồ số / kinh doanh tài chính / AI / chủ đề thời sự (có Profile thì tự rút ra)
- **Từ khoá**: ví dụ "AI", "gọi vốn", "tiêu dùng mới" (dùng để lọc tiêu đề)
- **Độ sâu**: lướt nhanh / phân tích sâu (chế độ sâu sẽ tải cả nội dung bài, mặc định là nhanh)
- **Số lượng**: mỗi nguồn 5-15 mục (mặc định 10)

## Đầu ra

```markdown
# Bản tin tình báo ngành
Ngày: {date} | Ngách: {track} | Nguồn tin: {sources}

## Điểm tin nhanh
#### 1. [tiêu đề](url)
- **Nguồn**: tên nguồn (nhãn lĩnh vực) | **Thời gian**: thời điểm đăng
- **Tóm tắt**: tóm tắt một câu bằng tiếng Việt
- **Insight**: 💡 bối cảnh / tác động / liên quan gì tới nhà sáng tạo

## Hướng đề tài
Dựa trên tin hôm nay, gợi ý 3-5 đề tài làm được ngay:
1. {đề tài} - góc tiếp cận + nền tảng/định dạng gợi ý
```

## Quy trình

### Step 1 - Chọn nguồn tin

Chọn bộ nguồn theo ngách (key của nguồn xem bảng dưới, hoặc gõ `--list-sources` để liệt kê):

| Ngách | Nguồn nên dùng |
|------|--------|
| Kênh cá nhân/vận hành nội dung | `woshipm,huxiu,aihot` |
| Công nghệ, đồ số | `sspai,geekpark,infoq_cn,36kr` |
| Kinh doanh, tài chính | `wallstreetcn,huxiu,tmtpost,36kr` |
| AI | `aihot,infoq_cn` |
| Thời sự/chất liệu chủ đề | `thepaper,tencent,huxiu` |

### Step 2 - Lấy dữ liệu

```bash
python3 skills/openclaw/skill-news-intelligence/scripts/fetch_news.py --source rss --limit 20 --keyword AI --no-save
```

Tham số: `--source` là key nguồn (ngăn bằng dấu phẩy, `all` là lấy hết); `--limit` số mục mỗi nguồn;
`--keyword` lọc theo từ khoá (khớp chuỗi con, chạy được với chữ có dấu); `--deep` tải cả nội dung bài; `--no-save` chỉ in ra stdout.

### Step 3 - Sinh bản tin

Đọc JSON, sinh bản tin tiếng Việt theo đúng định dạng ở mục "Đầu ra". Quy tắc:

1. **Ngôn ngữ**: toàn bộ tiếng Việt có dấu, giữ nguyên danh từ riêng tiếng Anh quen thuộc
2. **Chống bịa**: chỉ dùng dữ liệu có trong JSON, không tự nghĩ ra tin; thiếu thời gian thì ghi "không rõ thời gian"
3. **Lọc theo ngách**: khi có Profile/ngách, ưu tiên các mục liên quan tới ngách đó
4. **Hướng đề tài**: cuối bản tin, dựa trên tin mà đưa 3-5 đề tài làm được (góc tiếp cận + nền tảng/định dạng gợi ý)
5. **Nhãn smart_fill**: mục gắn `smart_fill` là phần bù rộng khi từ khoá không đủ, phải ghi chú "độ liên quan thấp"

### Step 4 - Lưu sản phẩm

Bản tin lưu vào `outputs/<chủ đề>/news-briefing-{date}.md`.

## Chế độ bản tin hằng ngày

Một lệnh là ra bản tin cho ngách đã cài sẵn:

```bash
python3 skills/openclaw/skill-news-intelligence/scripts/daily_briefing.py --profile tech_digital --no-save
```

| Profile | Dùng cho | Nguồn gồm |
|---------|------|--------|
| `creator` | Nhật báo tình báo cho nhà sáng tạo | Woshipm + Huxiu + 36Kr + AIHOT |
| `tech_digital` | Nhật báo công nghệ, đồ số | Sspai + GeekPark + 36Kr + TMTPost + InfoQ |
| `business` | Nhật báo kinh doanh, tài chính | Wallstreetcn + Huxiu + TMTPost + 36Kr |
| `ai` | Nhật báo tin AI | AIHOT + InfoQ |
| `topics` | Nhật báo chất liệu chủ đề | The Paper + Tencent News + Huxiu |

## Nguồn tin có sẵn

| Key | Tên nguồn | Lĩnh vực |
|-----|------|------|
| `woshipm` | Woshipm | Kênh cá nhân, vận hành, nội dung |
| `huxiu` | Huxiu | Kinh doanh, công nghệ, tiêu dùng |
| `tmtpost` | TMTPost | Công nghệ, kinh doanh |
| `geekpark` | GeekPark | Công nghệ, đồ số, tiêu dùng |
| `sspai` | Sspai | Đồ số, hiệu suất, lối sống |
| `infoq_cn` | InfoQ bản tiếng Trung | Kỹ thuật, lập trình |
| `aihot` | AIHOT | Tin AI (tuyển chọn tiếng Trung, cập nhật hằng ngày) |
| `36kr` | 36Kr | Đầu tư khởi nghiệp, công nghệ, tin nhanh kinh doanh |
| `wallstreetcn` | Wallstreetcn | Tài chính, vĩ mô |
| `tencent` | Tencent News | Thời sự tổng hợp (chất liệu làm lại) |
| `thepaper` | The Paper | Thời sự, xã hội (chất liệu làm lại) |

## Nhận biết Profile

- **Có Profile**: đọc ngách trong `identity.md` để tự chọn nguồn và từ khoá; đọc `platforms.md` để khớp nền tảng, định dạng cho đề tài gợi ý
- **Không có Profile**: dùng chế độ chung (`--source all` hoặc hỏi người dùng đang quan tâm ngách nào)

## Xử lý riêng theo nguồn

| Nguồn | Lưu ý |
|----|---------|
| AIHOT | Đã là bản biên tập sẵn, trích thẳng rồi chuyển sang tiếng Việt; mặc định lấy 24h |
| The Paper | Đi vòng qua feedx, mặc định lấy 48h |
| InfoQ / Sspai | RSS có khi chỉ cho tiêu đề/tóm tắt, cần phân tích sâu thì thêm `--deep` |
| 36Kr / Wallstreetcn / Tencent | Có bộ thu riêng (không phải RSS chung) |

Nguồn nào lấy lỗi thì trả về rỗng và bỏ qua, không chặn cả bản tin (fail-open).

## Phụ thuộc

- Python 3.8+
- `requests`, `beautifulsoup4`
