---
name: asset-manager
description: >-
  Quản lý sản phẩm trong outputs/: lưu trữ theo ngày/nền tảng/loại, gắn tag, tìm lại nội dung cũ,
  lập danh sách tư liệu. Dùng khi người dùng nói "sắp xếp tư liệu", "dọn outputs", "tìm lại bài
  cũ", "hôm trước làm gì". Lớp produce tạo nội dung, asset-manager quản lý sản phẩm sau khi tạo.
layer: general
---

# Trình quản lý tư liệu

> Lưu trữ, gắn tag, tìm kiếm sản phẩm trong outputs/ - để nội dung cũ lúc nào cũng tra được và dùng lại được

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| action | có | Loại thao tác: `scan` / `search` / `archive` / `tag` / `list` / `report` |
| query | không | Từ khoá tìm kiếm (dùng khi thao tác search) |
| path | không | File hoặc thư mục cần thao tác (mặc định `outputs/`) |
| tags | không | Danh sách tag cần thêm, phân tách bằng dấu phẩy (dùng khi thao tác tag) |
| filter_platform | không | Lọc theo nền tảng: `xiaohongshu` / `weibo` / `douyin` / `zhihu` / `wechat` / `x` |
| filter_type | không | Lọc theo loại: `image` / `video` / `text` / `card` / `poster` / `script` |
| filter_date | không | Lọc theo ngày: `today` / `this-week` / `this-month` / `2026-07` / `2026-07-15` |
| profile_name | không | Lọc theo hồ sơ (Profile) (tự điền khi có ngữ cảnh Profile) |

## Đầu ra

### Thao tác list

```markdown
## Danh sách tư liệu

**Thư mục**: outputs/
**Thống kê**: tổng {n} file, {size} MB

| Tên file | Loại | SKILL nguồn | Ngày tạo | Tag |
|--------|------|-----------|----------|------|
| hero-poster-congnghe-sanphammoi-20260715.png | poster | poster-hero | 2026-07-15 | #congnghe #ramatsanpham |
| xhs-card-chamsocda-01.png | thẻ | card-xiaohongshu | 2026-07-14 | #chamsocda #xiaohongshu |
| ... | ... | ... | ... | ... |
```

### Thao tác search

```markdown
## Kết quả tìm kiếm: "{query}"

Tìm thấy {n} mục khớp:

| File | Vị trí khớp | Độ liên quan | Ngày tạo |
|------|----------|--------|----------|
| outputs/<chủ đề>/congnghe-so-sanh-danh-gia.md | tên file+nội dung | *** | 2026-07-12 |
| outputs/<chủ đề>/sanpham-congnghe-mo-hop.md | nội dung | ** | 2026-07-10 |
```

### Thao tác report

```markdown
## Thống kê tư liệu

### Phân bố theo loại
| Loại | Số lượng | Tỉ lệ |
|------|------|------|
| Ảnh | 45 | 38% |
| Bài viết | 32 | 27% |
| Kịch bản video | 20 | 17% |
| Thẻ | 15 | 13% |
| Poster | 6 | 5% |

### Phân bố theo nền tảng
| Nền tảng | Số lượng | Sản phẩm gần nhất |
|------|------|----------|
| Xiaohongshu | 30 | 2026-07-15 |
| Weibo | 25 | 2026-07-14 |
| Douyin | 20 | 2026-07-13 |

### Xu hướng sản lượng (30 ngày gần đây)
| Tuần | Số sản phẩm | Trung bình ngày |
|----|----------|------|
| Tuần này | 12 | 1.7 |
| Tuần trước | 18 | 2.6 |
| Hai tuần trước | 8 | 1.1 |
```

## Các bước thực hiện

> Mọi thao tác file có tác dụng phụ và cần nhất quán trạng thái (quét chỉ mục, di chuyển lưu trữ, bảo trì tags.json) đã cố định trong
> `scripts/assets.py` (thuần stdlib, subcommand argparse). **LLM chỉ định tuyến ý định và trình bày kết quả, không tự tay
> find/grep/mv hay viết JSON.** Chỉ mục và tags dùng ghi nguyên tử (file tạm + rename).

### Định tuyến thao tác

1. **Phân tích ý định người dùng**, ánh xạ sang subcommand của script:
   - "sắp xếp tư liệu" / "lưu trữ" / "dọn outputs" -> `archive`
   - "gắn tag" / "đánh dấu" -> `tag`
   - "tìm cái trước đây" / "tìm lại lịch sử" / "hôm trước làm gì" -> `search`
   - "danh sách tư liệu" / "xem có những gì" -> `list`
   - "thống kê tư liệu" / "báo cáo sản lượng" -> `report`
   - (nếu chỉ mục có thể đã cũ thì chạy `scan` một lần trước khi tra; search/list sẽ tự quét khi thiếu chỉ mục)

### Gọi script

2. Điểm vào thống nhất (mặc định `--root outputs`):
   ```bash
   S=skills/openclaw/asset-manager/scripts/assets.py
   python3 $S scan                                    # tạo/cập nhật INDEX.json
   python3 $S search "từ khoá" --platform xiaohongshu --type card --date this-week
   python3 $S search --tag "chăm sóc da,seeding"      # tag phải trúng hết
   python3 $S list --platform weibo                    # danh sách tư liệu
   python3 $S report                                   # phân bố loại/nền tảng/ngày
   python3 $S tag "bai-tuyen-dung/card_1.png" --add "chăm sóc da,xiaohongshu" --remove "nháp"
   python3 $S archive                                  # xem trước kế hoạch lưu trữ (dry-run)
   python3 $S archive --apply                          # xác nhận xong mới thật sự di chuyển
   python3 $S archive bai-tuyen-dung --apply           # chỉ lưu trữ một thư mục/file
   ```

3. **Quy tắc lưu trữ**: file được chuyển vào `outputs/{ngày}/{nền tảng}/{loại}/`. Ngày lấy từ
   `YYYYMMDD`/`YYYY-MM-DD` trong tên file, không có thì lấy mtime; nền tảng/loại suy ra từ tên file và đuôi mở rộng.

4. **Bảo đảm an toàn (script lo sẵn, LLM không phải phán đoán)**:
   - `archive` mặc định **dry-run**, chỉ in kế hoạch `MOVE`/`CONFLICT`/`skip`; thêm `--apply` mới di chuyển
   - **Idempotent**: source==target thì bỏ qua; đích đã có và nội dung giống nhau thì bỏ qua; thứ đã nằm trong cấu trúc `ngày/nền tảng/...` thì không lưu trữ lại
   - Đích đã có nhưng nội dung khác -> đánh dấu `CONFLICT` rồi bỏ qua, **tuyệt đối không ghi đè**
   - Khi di chuyển, key trong tags.json tự đi theo đường dẫn mới

5. **Trình bày kết quả**: gom output của script thành bảng Markdown như chương "Đầu ra" rồi trả cho người dùng.
   Trước khi lưu trữ nhất định phải cho xem kế hoạch dry-run, có xác nhận rồi mới `--apply`.

## Nhận biết Profile

- **Khi có ngữ cảnh Profile**:
  - Đọc `identity.md` / `platforms.md` lấy tên kênh và nền tảng, truyền cho script qua `--tag` (tên hồ sơ) hoặc
    `--platform` để thu hẹp phạm vi search/list
  - Nếu tư liệu để theo thư mục từng hồ sơ, `archive <thư mục hồ sơ> --apply` chỉ lưu trữ sản phẩm của hồ sơ đó
- **Khi không có ngữ cảnh Profile**:
  - Hiện toàn bộ tư liệu trong outputs/, không lọc theo hồ sơ
  - Ghi chú: "Nếu cung cấp Profile của kênh (gồm identity.md / platforms.md), có thể quản lý tư liệu theo chiều kênh và nền tảng"

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
