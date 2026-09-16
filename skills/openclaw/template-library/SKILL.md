---
name: template-library
description: >-
  Lưu, tái dùng, quản lý mẫu nội dung riêng: đúc bài thành công thành mẫu có biến, điền là ra bài;
  có phân loại, phiên bản. Dùng khi người dùng nói "lưu làm mẫu", "dùng mẫu", "danh sách mẫu",
  "dùng lại cấu trúc cũ". post-formatter là khung PAS/AIDA/BAB chung, social-content viết từ đầu.
layer: general
---

# Thư viện mẫu

> Lưu, tái dùng, quản lý mẫu nội dung - biến kinh nghiệm thành công thành cấu trúc lặp lại được

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| action | Có | Loại thao tác: `save` / `use` / `list` / `edit` / `delete` / `get` |
| template_name | Tuỳ thao tác | Tên mẫu (bắt buộc với save / use / edit / delete / get) |
| source_file | Không | Đường dẫn file nguồn cần lưu thành mẫu (dùng khi save) |
| source_text | Không | Nội dung văn bản cần lưu thành mẫu (khi save, chọn một trong hai với source_file) |
| category | Không | Phân loại mẫu: `xiaohongshu` / `weibo` / `douyin` / `zhihu` / `wechat` / `x` / `general` |
| variables | Không | Giá trị điền cho biến của mẫu, dạng JSON (dùng khi use) |
| topic | Không | Chủ đề/đề tài khi dùng mẫu (dùng khi use) |
| profile_name | Không | Tên hồ sơ (Profile) được gắn (tự điền khi có ngữ cảnh Profile) |

## Đầu ra

### Thao tác save

```markdown
## Đã lưu mẫu

**Tên**: {template_name}
**Phân loại**: {category}
**Nơi lưu**: templates/{category}/{template_name}.md

### Cấu trúc mẫu đã trích
| Phần | Mô tả cấu trúc | Vùng thay đổi được |
|------|----------|----------|
| Tiêu đề | Con số + câu hỏi chạm nỗi đau | {{title_number}}, {{pain_point}} |
| Mở đầu | Hook ngược lẽ thường | {{hook_statement}} |
| Thân bài | Ba đoạn (vấn đề - giải pháp - bằng chứng) | {{problem}}, {{solution}}, {{evidence}} |
| Kết | Kêu gọi hành động + dẫn tương tác | {{cta}}, {{question}} |

### Biến của mẫu
Trích được {n} biến, lần sau dùng chỉ cần điền nội dung cụ thể.
```

### Thao tác use

```markdown
## Kết quả áp mẫu

**Mẫu dùng**: {template_name}
**Chủ đề**: {topic}

---

{nội dung sinh ra từ cấu trúc mẫu + các biến đã điền}

---

> Sinh từ mẫu `{template_name}`, có thể chỉnh tiếp.
```

### Thao tác list

```markdown
## Thư viện mẫu

**Tổng số**: {n} mẫu

### Theo phân loại

#### Xiaohongshu ({n1} mẫu)
| Tên mẫu | Mô tả | Số biến | Lượt dùng | Ngày tạo |
|--------|------|--------|----------|----------|
| seeding so sánh | Cấu trúc seeding so sánh hai sản phẩm | 8 | 5 | 2026-07-10 |
| các bước hướng dẫn | Cấu trúc thẻ hướng dẫn N bước | 6 | 3 | 2026-07-08 |

#### Weibo ({n2} mẫu)
| Tên mẫu | Mô tả | Số biến | Lượt dùng | Ngày tạo |
|--------|------|--------|----------|----------|
| bình luận trend | Cấu trúc bình luận chủ đề đang hot | 5 | 7 | 2026-07-12 |

#### Chung ({n3} mẫu)
| ... | ... | ... | ... | ... |
```

## Các bước thực hiện

> Đọc ghi file mẫu, bảo trì INDEX.json, tự tăng usage_count, trích và thay `{{var}}` đều đã cố định trong
> `scripts/templates.py` (thuần stdlib, subcommand argparse). **LLM chỉ định tuyến ý định, phân tích cấu trúc nội dung
> (viết lại nội dung thành công thành thân mẫu có placeholder `{{var}}`) và trình bày kết quả, không tự viết JSON, không tự tay
> thêm xoá file.** Chỉ mục và file mẫu đều ghi nguyên tử (file tạm + rename), thêm xoá mẫu là cập nhật INDEX.json cùng lúc.

### Định tuyến thao tác

1. **Phân tích ý định người dùng**, ánh xạ sang subcommand của script:
   - "lưu mẫu" / "lưu thành mẫu" -> `save`
   - "dùng mẫu" / "áp mẫu" / "dùng lại cấu trúc lần trước" -> `use`
   - "danh sách mẫu" / "có những mẫu nào" / "mẫu hay dùng" -> `list`
   - "sửa mẫu" / "chỉnh mẫu" -> `edit`
   - "xoá mẫu" -> `delete`
   - "xem trước mẫu" / "coi thử mẫu" -> `get`

### Việc của LLM (phân tích trước save/use)

2. **Trước save**: LLM đọc nội dung nguồn, nhận ra phần cấu trúc cố định và vùng thay đổi được, viết lại giá trị cụ thể thành placeholder
   `{{ten_bien}}` (như tên sản phẩm -> `{{product_name}}`, nỗi đau -> `{{pain_point}}`), rồi đưa thân bài đã viết lại
   cho script qua `--text` hoặc `--file`. Script lo trích danh sách biến, ghi file, đăng ký chỉ mục.
3. **Trước use**: LLM dựa vào topic/Profile suy ra giá trị điền cho từng biến, truyền vào qua `--var`/`--vars`.
   Script lo thay thế, tự tăng usage_count, ghi lại chỉ mục nguyên tử.

### Gọi script

4. Một cửa vào duy nhất (mặc định `--root templates`):
   ```bash
   S=skills/openclaw/template-library/scripts/templates.py
   python3 $S save "seeding so sánh" --category xiaohongshu --description "so sánh hai sản phẩm" \
           --text "Tiêu đề: {{title}} A={{product_a}} vs B={{product_b}} CTA={{cta}}"
   python3 $S list --category xiaohongshu                  # liệt kê theo phân loại, giảm dần theo lượt dùng
   python3 $S get "seeding so sánh"                        # xem trước nội dung + thông tin meta
   python3 $S use "seeding so sánh" --var title="chống nắng mùa hè" --var product_a="Anessa"
   python3 $S use "seeding so sánh" --vars '{"title":"chống nắng mùa hè","cta":"thả tim và lưu bài"}'
   python3 $S edit "seeding so sánh" --category general --description "đổi mô tả" --text "thân bài mới {{x}}"
   python3 $S delete "seeding so sánh"                      # xem trước (dry-run)
   python3 $S delete "seeding so sánh" --apply              # xác nhận xong mới xoá thật
   ```

5. **Bảo đảm sẵn trong script (LLM không phải tự phán)**:
   - `save` trùng tên thì mặc định báo lỗi, cần `--force` để ghi đè; `edit` đổi phân loại sẽ chuyển file và dọn file cũ
   - `use` gặp biến chưa điền thì giữ nguyên `{{placeholder}}` và cảnh báo ra stderr, không lỗi âm thầm
   - `delete` mặc định **dry-run**, chỉ in ra mẫu sắp xoá, thêm `--apply` mới xoá thật và dọn chỉ mục
   - Mọi thao tác ghi đều nguyên tử, thêm xoá mẫu luôn khớp với INDEX.json

6. **Trình bày kết quả**: sắp xếp output của script thành Markdown theo mục "Đầu ra" rồi trả cho người dùng.

## Nhận biết Profile

- **Khi có ngữ cảnh Profile**:
  - Thao tác save tự gắn mẫu vào hồ sơ (Profile) hiện tại
  - Thao tác list ưu tiên hiện mẫu của hồ sơ hiện tại, mẫu của hồ sơ khác đánh dấu "dùng chung"
  - Thao tác use tự nạp style.md của hồ sơ để chỉnh giọng
  - Frontmatter của file mẫu ghi `profile: {ten_ho_so}`
- **Khi không có ngữ cảnh Profile**:
  - Mọi mẫu đánh dấu `profile: shared` (mẫu dùng chung)
  - Thao tác list hiện toàn bộ mẫu, không lọc theo hồ sơ
  - Thao tác use không chỉnh giọng, xuất thẳng kết quả điền mẫu

> Nguồn gốc tự phát triển và dự án tham khảo xem `EASEL-META.md` cùng thư mục.
