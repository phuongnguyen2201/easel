---
name: short-drama
description: >-
  Làm phim ngắn AI nhiều tập: kinh thánh phim, kịch bản, ảnh→video từng cảnh, lồng tiếng + phụ đề,
  nhất quán nhân vật xuyên tập. Dùng khi người dùng nói "phim ngắn AI", "kịch bản từng tập", "phim
  nhiều tập". Video đơn → auto-short-video, chỉ kịch bản → video-script, một đoạn → ai-video-gen.
layer: produce
---

# Làm phim ngắn AI (micro-drama ngang/dọc, nhiều tập)
> **Luật sắt về đường dẫn kiểm tra cấu hình**: trước khi chạy cả pipeline, `cd` tới thư mục gốc dự án Easel ghi ở cuối `AGENTS.md`, xác nhận `.env` và `skills/shared/scripts/` tồn tại. Cấu hình sinh ảnh, video, lồng tiếng bắt buộc chạy registry/`check` từ đây; không dùng `./shared/scripts/...` trong OpenClaw workspace, không dùng `env` / `printenv` để kết luận thiếu `IMG_BASE_URL`, `VOICE_BASE_URL` hay Key. Thấy thiếu thì đối chiếu `pwd` trước, quay về gốc dự án và truyền tường minh `--env-file .env` để kiểm lại.
## ⛔ Ba luật sắt (dễ hỏng nhất, thuộc lòng trước khi bắt tay)

1. **Mỗi cảnh bắt buộc "image to video" thành clip động - tuyệt đối không lấy ảnh tĩnh thế vào.** Ảnh khung chính (frame) chỉ là **khung đầu** của I2V, phải dùng **ai-video-gen `image2video`** để biến thành `clip` chuyển động. Bỏ qua bước này = một đống ảnh tĩnh ghép tiếng, rác. Trước khi ghép, `storyboard` sẽ **chặn cứng** cảnh chỉ có frame mà thiếu clip.
2. **Lồng tiếng bắt buộc dùng provider cloud closed-source (có cảm xúc, như người thật) - tuyệt đối không dùng edge (đọc phẳng, đậm mùi AI).** Trước hết cấu hình `VOICE_PROVIDER` trong `.env` + `voice_clone.py check` để kiểm key; có key rồi thì `dubbing align/dub` **chặn cứng ngay trước khi ghép** với edge, bất kỳ nhân vật nào (kể cả người dẫn) rơi xuống edge là fail ngay. Chỉ khi hoàn toàn không có key mới dùng `--allow-edge` để chống cháy.
3. **Ưu tiên audio gốc, mỗi cảnh phải giữ tiếng nền, thoại bắt buộc đưa vào model.** Audio gốc của model video (tiếng nền/bước chân/hiệu ứng vật lý) chất lượng tốt, **mặc định dùng trọn track tiếng nền**. **Điểm số một: khi sinh video phải viết thoại vào `generation_prompt` (do `prepare` sinh) rồi đưa cho model**, nếu không model không biết nói gì, thoại sai hết. Mặc định **native-first** (để model nói từng chữ, nói được là dùng, không mặc định vứt sang TTS) → `audit` kiểm ASR từng cảnh: khớp thì dùng thoại gốc (thường gặp), nói sai thì chuyển `dub` sang TTS, cảnh dẫn/cảnh hành động thì đi TTS/tiếng nền. Chi tiết quyết định và probe xem bước 16/18 và `references/native-audio-workflow.md`.
4. **Hình/tiếng/phụ đề khớp theo timeline, phát tự nhiên.** Hình dùng trọn độ dài clip thật (thoại chỉ chiếm một đoạn, đặt đúng thời điểm nói thực tế), **tuyệt đối không làm chậm/lặp/đóng băng**; clip không phủ hết thoại thì sinh lại hoặc tách cảnh (`align` chặn cứng).

> **⚠️ Cấm đi đường tắt (kỷ luật thực thi, hay hỏng nhất)**: `prepare → drama_ops.py generate (sinh video) → audit → align` là **chuỗi không được bỏ bước**, script đã gắn **cổng cứng theo chuỗi**: ① sinh video **bắt buộc qua `drama_ops.py generate`** (nó tự đọc `generation_prompt` từng cảnh rồi gọi model video, agent không thể truyền thành prompt chỉ có hình ảnh) - đừng gọi tay ai-video-gen từng cảnh nữa; ② `generate`/`audit` thấy cảnh có thoại mà thiếu `generation_prompt` → kết luận "chưa chạy prepare" và fail ngay; ③ `align` thấy thiếu `clip-audit.json` → kết luận "chưa chạy audit" và fail ngay (không còn âm thầm hạ toàn bộ thoại xuống TTS). Đường tắt sai kiểu "gọi tay sinh video chỉ truyền prompt hình ảnh + TTS thẳng" sẽ bị chặn lại - nhờ vậy mới có "thoại đưa vào model + dùng tiếng gốc của video".

> SKILL lớp điều phối: phần sáng tạo (kinh thánh phim/kịch bản/phân cảnh/lines) do bạn - LLM - viết, mọi thao tác sinh đều uỷ quyền cho SKILL sẵn có (ai-image-gen/ai-video-gen/ai-music), IO xác định đi qua `scripts/drama_ops.py` + `scripts/dubbing.py`; nhất quán nhân vật dựa vào "chốt ảnh tham chiếu trước rồi mới I2V" + kinh thánh phim khoá tất cả thành cùng một bộ.

## Đầu vào

| Trường | Bắt buộc | Mô tả |
|------|------|------|
| Thể loại/tóm tắt | Có | Một câu cốt truyện hoặc nguồn chuyển thể (không có thì hỏi) |
| Số tập | Không | Tuỳ thể loại/nhu cầu, **không ép** (micro-drama hay có 10-30 tập, chỉ là con số phổ biến; xây kênh thử nghiệm có thể làm 1-3 tập để kiểm chuỗi) |
| Thời lượng mỗi tập | Không | **Không ép số phút cố định** - tuỳ thể loại/nền tảng/nhịp truyện, vài chục giây tới vài phút đều được; tổng thời lượng bản dựng = tổng thời lượng clip của các cảnh (script không đặt trần, người dùng muốn dài bao nhiêu thì bấy nhiêu) |
| Khung hình | Có | Khi người dùng hoặc task phía trên chưa nêu rõ ngang/dọc (hoặc 16:9/9:16/độ phân giải cụ thể), trước khi làm phải hỏi lại và chờ xác nhận; không được suy đoán âm thầm theo nền tảng, Profile hay giá trị mặc định, đã rõ rồi thì đừng hỏi lại |
| Phong cách hình ảnh | Không | Đô thị kiểu Hong Kong/cổ trang/học đường/trinh thám... (chốt một tiền tố phong cách thống nhất)|

## Cấu trúc sản phẩm (`outputs/<chủ đề>/` - lấy theo tên phim)

```
series-bible.md         Kinh thánh phim (lời hứa kịch + bảng nhân vật [mô hình hành động+want/need/wound/flaw+bốn câu hỏi đáng theo dõi+hồ sơ chất giọng] + tuyến truyện + đường cong cảm xúc/nhịp điểm sướng + thang phản diện + twist từng tập + hook + tiền tố phong cách)
cast.json               Bảng chọn giọng (nhân vật → chất giọng: giọng edge + pitch/rate, hoặc giọng clone)
ref_index.json          Chỉ mục ảnh tham chiếu (C nhân vật / S bối cảnh / P đạo cụ, tái dùng xuyên cảnh xuyên tập)
refs/                   Ảnh tham chiếu (C01_LamSach.png ...)
episodes/ep01/
  script.md             Kịch bản tập này (bốn hồi theo nhịp nhân quả + thoại + hook cuối tập)
  lines.json            Thoại từng dòng của tập ({speaker,text,emotion,shot,at?}, shot=cảnh chứa nó, at=giây bắt đầu trong cảnh/khớp thời điểm nói, dùng cho lồng tiếng theo timeline)
  shots.json            Phân cảnh của tập (từng cảnh: prompt theo trục thời gian + @tham chiếu + mô tả khung cuối + sfx tuỳ chọn [hiệu ứng hẹn giờ]; align ghi ngược duration mỗi cảnh)
  shots/                Ảnh khung chính từng cảnh + clip đã sinh
  voice.mp3 / voice.srt Lồng tiếng nhiều nhân vật (mỗi nhân vật một giọng riêng, khớp cảnh) + phụ đề cùng trục
  timing.json           Thời lượng từng cảnh + mốc đầu/cuối từng dòng (align sinh ra, lưu hồ sơ/đối chiếu)
  clip-audit.json       Track audio gốc, ASR, ngôn ngữ, thời điểm nói và quyết định native/dub/regenerate
  final.mp4             Bản dựng hoàn chỉnh của tập
progress.json           Tiến độ sinh theo tập/theo cảnh (kiểm soát chi phí, chạy tiếp từ điểm dừng)
```

Script (tính từ gốc dự án): `skills/openclaw/short-drama/scripts/drama_ops.py` (tài sản/phân cảnh/tiến độ),
`skills/openclaw/short-drama/scripts/dubbing.py` (lồng tiếng nhiều nhân vật);
bộ ghép dùng lại: `skills/openclaw/auto-short-video/scripts/assemble.py`.

## Các bước thực hiện

> ⚠️ Sinh ảnh/sinh video/lồng tiếng đều **chạy bất đồng bộ + tính tiền theo lượng dùng**. **Ra Plan trước** (mấy tập, mỗi tập mấy cảnh, gọi API trả phí nào,
> thời gian/chi phí ước tính), xác nhận xong mới chạy. Khi xây kênh thử nghiệm nên chạy **1 tập** để kiểm toàn chuỗi rồi mới làm nhiều.

### 0. Hoạch định bộ phim (đầu óc mới, bắt buộc làm)

1. **Chọn thể loại + chốt điểm sướng**: đọc `references/genre-hooks-handbook.md` trước để chọn một thể loại chính (lật kèo/chiến thần/trùng sinh báo thù/ngôn tình ngọt/giấu thân phận...) + điểm sướng cốt lõi của nó, tránh "cốt truyện quá đơn giản/quá rời rạc".
2. **Dựng khung**: `python skills/openclaw/short-drama/scripts/drama_ops.py scaffold --series "<tên phim>"`.
3. **Chạy qua story engine** (trị "cốt đơn giản/nhân vật phẳng", bắt buộc làm trước khi viết bible): đọc `references/story-engine.md` -
   - Viết **lời hứa kịch** trong một câu rồi tự kiểm (chủ thể/mục tiêu theo đuổi/trở lực đắt giá/phần thưởng lặp lại; đổi tên vẫn độc đáo, trở lực có giá phải trả, nhân vật chính có quyền chủ động, khúc giữa có phần thưởng);
   - Mỗi nhân vật chính dựng **mô hình hành động 8 trường + want/need/wound/flaw/vòng cung + bốn câu hỏi đáng theo dõi (ep1 phải thấy được ít nhất một)**;
   - Phản diện xếp **4 tầng thang** theo `references/satisfaction-and-villain.md` (trị nhân vật công cụ/lạm phát điểm sướng).
4. Viết `series-bible.md` (đọc `references/series-bible-schema.md`, đã có sẵn các trường chiều sâu nói trên): điểm bán trong một câu, **lời hứa kịch**, thế giới quan, **bảng nhân vật (mô hình hành động + chiều sâu)**, tuyến truyện chính, **đường cong cảm xúc + bảng nhịp điểm sướng + thang phản diện**, **dàn ý từng tập (mỗi tập: cốt truyện + điểm lật theo nhân quả + nút thắt cuối tập)**, **tiền tố phong cách hình ảnh thống nhất**.
5. **Qua cổng A/B**: theo `references/drama-review-rubric.md`, tự chấm **có dẫn chứng** từng mục ở A (cổng story engine) + B (cổng nhân vật đáng theo dõi), bất kỳ lỗi nặng ⛔ nào cũng phải sửa xong mới đi tiếp.

### 1. Kịch bản từng tập (nhịp nhân quả + tay nghề viết thoại, đừng kể lể lan man)

6. Mỗi tập đọc `references/four-act-drama.md`, `references/causal-beats.md`, `references/vertical-pacing.md` và **`references/dialogue-craft.md`**, rồi viết `episodes/epNN/script.md` theo **nhịp nhân quả**:
   Mục tiêu (hook 3 giây) → trở ngại → bước ngoặt (điểm bùng nổ sướng/ngược) → hook cuối tập, các nhịp liền nhau nối bằng "bởi vì/cho nên"; **mật độ điểm sướng** cứ 15-30s một sự kiện cảm xúc.
   - **Twist sinh ra từ nhân quả**: mỗi twist phải qua "bài test một câu về lật kèo nhân quả" + 5 câu hỏi tiết lộ công bằng trong `genre-hooks-handbook.md`, điền không nổi = twist trên trời rơi xuống, làm lại.
   - **Thoại theo `dialogue-craft.md`**: cấm nói thẳng tuột/cấm cả dàn cùng một giọng (qua swap-test)/biến phần giải thích thành xung đột/ai cũng có thứ muốn + thứ muốn giấu/mỗi tập ≥1 câu đắt/mỗi dòng ≤15 chữ.
   - **Mỗi câu thoại phải ghi rõ người nói**: trong kịch bản, thoại luôn viết dạng **`Tên nhân vật: thoại`** (tên nhân vật lấy đúng như trong cast/bible, đừng viết "anh ta/cô ta/mọi người") - khi rút ra lines.json thì chép nguyên speaker, tránh lồng tiếng sai nhân vật.
7. **Viết xong thì qua cổng C/D/E**: theo `references/drama-review-rubric.md`, tự chấm từng mục C (tiết lộ twist) + D (nhịp) + E (thoại) và **dẫn nhịp/câu thoại cụ thể**, bất kỳ lỗi nặng ⛔ nào (thiếu hook ep1/giọng điệu na ná nhau/twist trên trời rơi xuống) đều phải sửa, đừng làm cho có.

### 2. Chốt tạo hình nhân vật / bối cảnh (nền móng của tính nhất quán)

8. Dùng **ai-image-gen** sinh **ảnh tham chiếu tạo hình** cho từng nhân vật (chính diện/nhiều góc, đưa vào từ khoá ngoại hình + tiền tố phong cách thống nhất); bối cảnh/đạo cụ quan trọng làm tương tự.
9. Đăng ký lần lượt vào chỉ mục (tự động cấp mã C/S/P):
   ```bash
   python skills/openclaw/short-drama/scripts/drama_ops.py ref add --series "<tên phim>" \
     --kind character --name "Lâm Sách" --image refs/C01_LamSach.png --desc "nam chính, vest lạnh lùng" --style "đô thị kiểu Hong Kong"
   ```
   Đọc `references/character-consistency.md` để hiểu vì sao phải chốt ảnh tham chiếu trước.
9.5 **⛔ Ảnh tạo hình bắt buộc soi bằng mắt (làm xong ảnh tuyệt đối không bỏ qua)**: dùng công cụ xem ảnh **xem từng ảnh tạo hình của từng nhân vật**, xác nhận tóc/tuổi/trang phục/khí chất **khớp thiết định nhân vật**, ghi nhận lần lượt:
   ```bash
   python skills/openclaw/short-drama/scripts/drama_ops.py ref review --series "<tên phim>" \
     --code C01 --observation "Nhìn thấy: nam tóc ngắn mặc vest, vẻ lạnh lùng, khớp thiết định nam chính"
   ```
   Hình tượng lệch (nam chính thành ông chú, bé gái thành người lớn) → sinh lại ảnh tạo hình rồi soi lại, **đừng lấy hình tượng lệch đi sinh video** (khuôn mặt vỡ trận xuyên cảnh). Ảnh tạo hình nhân vật chưa soi thì `generate` sau đó sẽ **chặn cứng**.

### 2.5 Chọn giọng (nhân vật → chất giọng, mấu chốt của nhiều tuyến giọng, **ưu tiên closed-source + giọng khớp nhân vật**)

10. Đọc `skills/shared/references/voice-casting.md`. **Chất giọng do chính hình tượng trong ảnh tham chiếu tạo hình quyết định** - xem ảnh tạo hình sinh ra ở §2 trông thế nào, rồi đối chiếu bảng "nguyên mẫu hình tượng → tra nhanh chất giọng" ở voice-casting.md §0.6: trong ảnh là **bé gái thì ghép giọng bé gái (giọng trẻ em nữ, cao và nhanh)**, chị đại ghép giọng trưởng thành, ông chú ghép giọng trầm già dặn, tổng tài ghép giọng dày... **tuyệt đối không để hình tượng lệch chất giọng** (nữ chính gán giọng bà thím, trẻ con gán giọng người lớn = mất nhập tâm). **Mỗi nhân vật dùng `--archetype` ghi nguyên mẫu hình tượng, `--ref` gắn mã C của ảnh tạo hình** (`cast check` sẽ đối chiếu: mọi nhân vật có ảnh tạo hình trong ref_index đều phải được gán giọng, thiếu là chặn ngay). Người dẫn tách riêng và khác mọi nhân vật.
   - **Bắt buộc ưu tiên closed-source (luật sắt ②, gồm cả người dẫn/lồng tiếng thường)**: trước hết cấu hình `VOICE_PROVIDER` trong `.env` + `python skills/shared/scripts/voice_clone.py check --provider <..> --env-file .env` để **kiểm key dùng được**; `cast init` cho người dẫn và `cast add` đều mặc định `clone` và tự lấy `VOICE_PROVIDER`. **Có key rồi thì: `cast check` chặn edge trong cấu hình tĩnh, `align/dub` chặn thêm một lớp trước khi ghép** - bất kỳ nhân vật nào (kể cả người dẫn) rơi xuống edge là fail ngay (clone thiếu voice_id / gọi clone lỗi đều tính), ép bạn sửa xong closed-source rồi mới ra phim. Chỉ khi hoàn toàn không có key mới dùng `--allow-edge` chống cháy. Giọng dựng sẵn xem voice-casting.md §0.5.
   ```bash
   python skills/openclaw/short-drama/scripts/dubbing.py cast init --series "<tên phim>"   # tạo template (người dẫn mặc định closed-source)
   # Theo hình tượng trong ảnh tạo hình, chọn giọng dựng sẵn closed-source cho khớp, rồi ghi archetype/ref
   python skills/openclaw/short-drama/scripts/dubbing.py cast add --series "tên phim" --name "Lâm Sách" --role male_lead \
     --engine clone --provider openai-compatible --voice-id FunAudioLLM/CosyVoice2-0.5B:benjamin \
     --archetype "nam chính lạnh lùng" --ref C01 --note "trầm, từ tính, khớp ảnh tạo hình C01"
   python skills/openclaw/short-drama/scripts/dubbing.py cast add --series "tên phim" --name "Đóa Đóa" --role child \
     --engine clone --provider openai-compatible --voice-id FunAudioLLM/CosyVoice2-0.5B:bella \
     --pitch=+6Hz --rate=+5% --archetype "bé gái nhỏ" --ref C03 --note "giọng trẻ em, khớp ảnh tạo hình non nớt C03"
   python skills/openclaw/short-drama/scripts/dubbing.py cast check --series "tên phim"
   ```
   Cần **giọng clone riêng** (không phải giọng dựng sẵn) → `--provider minimax/dashscope` + chạy `voice_clone.py enroll` trước để lấy `--voice-id`.
   Chỉ khi chưa cấu hình bất kỳ key closed-source nào mới lùi về edge (`cast check` sẽ hiện 💡 nhắc nâng cấp). Phân tầng và cấu hình xem voice-casting.md §0 và SKILL `multi-voice-dubbing`.

### 3. Kịch bản phân cảnh + thoại từng dòng + **hoạch định thời lượng** (mấu chốt của sự tự nhiên: chốt mỗi cảnh giữ bao lâu rồi mới đi sinh video)

11. **Tách cảnh** theo thời lượng và nhịp của tập (số cảnh không ép - tập ngắn thì vài cảnh, tập dài thì nhiều cảnh hơn, bám theo cốt truyện), viết `episodes/epNN/shots.json` (định dạng xem `references/shot-prompt-format.md`):
   Mỗi cảnh gồm `idx / desc / prompt (đầu phong cách + nhịp hình theo từng giây + [âm thanh]) / refs (trỏ tới C/S/P) / tail (mô tả khung cuối)`.
12. **Đồng thời rút thoại từng dòng của tập ra `episodes/epNN/lines.json`** (có thứ tự `[{speaker, text, emotion, shot}]`; quy tắc trường xem bước 17) - **viết xong trước khi sinh video**, vì mỗi cảnh giữ bao lâu là do thoại của nó quyết định.
13. **Hoạch định thời lượng từng cảnh + kiểm tra có nhét vừa clip không** (gốc rễ trị chuyện "hình đứng im/quá gấp"):
   ```bash
   python skills/openclaw/short-drama/scripts/dubbing.py plan --series "<tên phim>" --episode N
   ```
   ⚠️ **Ràng buộc thực tế: video AI chỉ sinh được các mốc thời lượng cố định (thường là 5s, đôi khi 5/10s), không xuất theo số giây tuỳ ý.** Nên `plan` có tác dụng: ① ước lượng thời lượng thoại mỗi cảnh (= thời gian hình nên giữ, ghi ngược vào `target_duration`) ② **kiểm tra thoại mỗi cảnh có nhét vừa một mốc clip không** - **không vừa (thoại > ~5s) thì tách thành nhiều cảnh hoặc rút gọn thoại** (`plan` sẽ đánh dấu ⚠️), đừng cố sinh rồi kéo giãn ở hậu kỳ ③ đề xuất mốc thời lượng clip nên sinh cho từng cảnh `gen_duration` (5 hoặc 10). **Giữ thoại mỗi cảnh gọn trong một mốc clip chính là mấu chốt để hình trông tự nhiên.**
14. **Kiểm tra phân cảnh**: `drama_ops.py shots validate --series "<tên phim>" --episode N` (tiền tố phong cách/ảnh tham chiếu được trỏ tới/mã đã đăng ký/idx liên tục).

### 4. Sinh khung chính (chỉ là khung đầu của I2V, chưa phải bản dựng)

15. Dùng **ai-image-gen** sinh ảnh khung đầu theo prompt từng cảnh (**image to image và trỏ tới ảnh tham chiếu trong refs của cảnh đó**, giữ nhân vật nhất quán), lưu vào `episodes/epNN/shots/`, ghi đường dẫn ngược vào trường `frame` của shots.json. ⚠️ Tới đây vẫn chỉ là **ảnh tĩnh**, bước sau bắt buộc phải biến nó thành video.

### 5. Sinh video từng cảnh (I2V, **luật sắt ①: cảnh nào cũng phải làm, tuyệt đối không bỏ**)

16. **Sinh giao ước audio và prompt (đưa thoại vào model)**: chạy `model_registry.py configured --group video --env-file .env` trước; nếu có nhiều lựa chọn khả dụng mà người dùng chưa chỉ định thì hỏi, chọn xong cho tập này thì khoá suốt cả chuỗi.
    ```bash
    python skills/openclaw/short-drama/scripts/dubbing.py prepare --series "<tên phim>" --episode N --language vi-VN --provider "$VIDEO_PROVIDER"
    ```
    `prepare` đọc `lines.json` rồi ghi giao ước thoại vào `generation_prompt` của từng cảnh: mặc định **native-first** (yêu cầu model **nói thoại từng chữ**, bản dựng dùng thoại gốc); cảnh dẫn/cảnh thuần hành động thì không đưa thoại.
    - **Một cảnh có thể có nhiều câu thoại trong khung hình**: model video nói liền được, `prepare` sẽ ghi hết các câu của cảnh đó vào `generation_prompt` theo thứ tự thời gian (mỗi câu định vị bằng `at`, thiếu thì xếp tuần tự, tổng cộng phải nhét vừa mốc clip). **Không cần vì "nhiều câu" mà tách cứng mỗi câu một cảnh** - chỉ có lời dẫn và thoại trong khung vẫn phải khác cảnh (tránh giọng gốc chồng lên lời dẫn).
    - **Đừng dùng dub để né native-first**: `prepare --dialogue-mode dub` (cả phim không đưa thoại, hậu kỳ TTS toàn bộ) **đã có cổng cứng** - khi chưa có `ai_video.py probe-dialogue` đo thực tế cho thấy model không trung thực, và cũng không truyền tường minh `--force-dub`, thì sẽ bị từ chối. Vướng ràng buộc nhiều câu/một câu **không phải** lý do đổi sang dub (nhiều câu cứ nhét chung vào prompt). Mặc định để model thử tiếng gốc, `audit` chỉ đổi sang TTS ở đúng những cảnh nói sai.
17. **Sinh video từng cảnh (script điều khiển, ép đưa thoại vào model)**:
    ```bash
    python skills/openclaw/short-drama/scripts/drama_ops.py generate --series "<tên phim>" --episode N --ratio "<9:16 hoặc 16:9>"
    ```
    `prepare` sẽ khoá provider/model cuối cùng vào shots.json; `generate` bắt buộc dùng lại, truyền tường minh giá trị xung đột sẽ bị chặn cứng. Sau khi qua cổng cứng về prompt, nó gọi ai-video-gen từng cảnh (tự kèm `--audio auto --ratio <khung hình đã xác nhận> --duration gen_duration`), ghi clip ngược lại và ghi tiến độ; cảnh đã có clip thì tự bỏ qua, `--dry-run` để xem kế hoạch, `--only 1,3` để sinh lại một cảnh, `--force` để ép sinh lại.
    - **Mốc clip bắt buộc ≥ thời lượng thoại của cảnh đó** (bước 13 `plan` đã chọn mốc, cảnh quá dài đã tách): thời lượng hình do clip thật quyết định, bản dựng chỉ **cắt tự nhiên**, tuyệt đối không làm chậm/lặp/đóng băng. Clip còn ngắn hơn thoại → `align` fail cứng, phải sinh lại hoặc tách cảnh.
    - Liền mạch xuyên cảnh/xuyên tập thì dùng "khung cuối → khung đầu của cảnh kế" trong `references/character-consistency.md` (khi sinh lại một cảnh bằng `--only`, điền khung cuối của cảnh trước vào frame của cảnh đó).

### 6. Lồng tiếng nhiều nhân vật + phụ đề + hiệu ứng + BGM (khớp timeline)

> lines.json đã viết ở bước 12; ở đây làm lồng tiếng thật và **khớp theo timeline**.
> **Mô hình cốt lõi (timeline/dạng track)**: mỗi cảnh = một timeline của trọn clip, **thoại chỉ chiếm một đoạn**, thời gian còn lại là
> hành động/khoảng lặng/hiệu ứng - **thời lượng clip thường > tổng độ dài thoại**. Lồng tiếng không phải nối đuôi thoại cho kín clip, mà là đặt từng dòng
> **lệch theo `at`** lên timeline của clip (khớp thời điểm nói/mấp máy môi), chỗ trống để dành cho hành động và hiệu ứng.

18. **Kiểm tra track audio gốc của từng clip đã sinh** (ưu tiên tiếng nền, quyết định xem `references/native-audio-workflow.md`):
    ```bash
    python skills/openclaw/short-drama/scripts/dubbing.py audit --series "<tên phim>" --episode N
    ```
    Xuất `clip-audit.json`, quyết định từng cảnh `native / dub / regenerate`: `native` = có thoại (**có thể nhiều câu**) + đúng ngôn ngữ + độ tương đồng ASR cả đoạn ≥ ngưỡng (mặc định 0.6), hoặc cảnh thuần hành động không có tiếng nói bất ngờ → cho trọn track tiếng gốc đi thẳng + có phụ đề mà không lồng tiếng; `dub` = giọng người hỏng thật (sai ngôn ngữ/nội dung) hoặc hoàn toàn không có tiếng gốc → đổi sang TTS, **bỏ track gốc của cảnh đó** (không tách được giọng người thì giữ lại sẽ trùng với lồng tiếng); `regenerate` = thiếu clip/ASR không đọc ra/cảnh hành động có tiếng nói bất ngờ → sinh lại kèm phản hồi, lấy được tiếng gốc tốt thì chuyển `native` (ưu tiên, vừa dùng tiếng gốc của model vừa giữ tiếng nền), tối đa hai lần. Đúng ngôn ngữ là cổng bắt buộc đi trước; ngưỡng chỉnh bằng `--threshold`; khẩu hình/nhân vật lệch rõ thì soi bằng mắt rồi sinh lại.
19. **Quy tắc trường của `lines.json` thoại từng dòng** (viết ở bước 12, soi lại ở đây) - có thứ tự `[{speaker, text, emotion, shot, at?}]`:
    - `speaker` **phải trùng khít tên nhân vật trong cast.json** (chép nguyên phần "Tên nhân vật:" trong kịch bản, đừng viết chung chung "anh ta/cô ta") - `align` kiểm rất chặt, speaker không có trong cast là chặn và báo lỗi ngay (**trị chuyện "lồng tiếng sai nhân vật"**), không còn âm thầm lấy giọng người dẫn thế vào.
    - `emotion` là **kênh cảm xúc** gửi cho engine lồng tiếng (không phải bắt nhân vật đọc tên cảm xúc ra), viết cụ thể: giận dữ/cười khẩy/nén nhịn/khóc vỡ oà/run rẩy/hoảng sợ/đắc ý/dịu dàng/thất vọng/mỉa mai/gấp gáp/đau đớn/nũng nịu... - provider cloud closed-source sẽ đổi thành "nói bằng giọng <cảm xúc>" để dẫn dắt diễn xuất. **⚠️ Chất giọng không đổi theo cảm xúc**: `emotion` chỉ chỉnh ngữ điệu/tốc độ/cảm xúc (`emotion_prosody` cộng thêm phần chênh rate/pitch/volume), danh tính chất giọng của nhân vật luôn là đúng một `voice_id` đã gắn trong cast.json - cùng một nhân vật thì chất giọng cố định xuyên cảnh xuyên tập, chỉ ngữ điệu cảm xúc thay đổi.
    - **`shot` = idx của cảnh chứa câu thoại này (bắt buộc)**: để mỗi câu lồng tiếng/phụ đề rơi đúng vào clip hình tương ứng; một cảnh có thể nhiều câu; cảnh thuần hành động không có thoại thì không xuất hiện trong lines.
    - **`at` = giây bắt đầu của câu thoại này **trong clip của cảnh** (tuỳ chọn, đơn vị giây)**: khớp thời điểm nhân vật **bắt đầu nói/mấp máy môi** trên hình (ví dụ nhân vật đi lại trong 1.5s đầu, sau đó mới mở lời → `at: 1.5`). Không ghi thì xếp tuần tự từ đầu. **Đây là mấu chốt để "thời điểm nói khớp với hình"**; khoảng trống giữa các câu thoại chính là thời gian cho hành động/khoảng lặng/hiệu ứng.
20. **Lồng tiếng khớp timeline** (bắt buộc chạy sau khi đã sinh và kiểm từng cảnh):
    ```bash
    python skills/openclaw/short-drama/scripts/dubbing.py align --series "<tên phim>" --episode N
    ```
    Sau khi đọc `clip-audit.json`, thoại trong khung thuộc `native` thì **không tổng hợp TTS, dùng thẳng tiếng gốc của model**, mốc đầu/cuối từ ASR gốc được ghi vào phụ đề; lời dẫn và thoại `dub` đi vào track lồng tiếng riêng (track gốc của cảnh `dub` bị bỏ khi ghép, chỉ còn TTS, tránh chồng hai giọng người). Sinh ra `voice.mp3`, `voice.srt` cùng trục, `timing.json`, và ghi thời lượng clip thật ngược vào shots.json.
    - **Thời lượng hình = thời lượng clip thật (luật sắt ③)**: `align` dò thời lượng clip thật của từng cảnh làm thời lượng hình, thoại xếp chồng lên theo `at`, phần còn lại để cho hành động/khoảng lặng/hiệu ứng - bản dựng chính là **clip phát nguyên trạng, tuyệt đối không đóng băng/kéo giãn/lặp**.
    - **Chặn cứng theo timeline**: cảnh có thoại mà thiếu clip, `at` âm, thoại trong cùng cảnh chồng nhau, hoặc `at` + thời lượng lồng tiếng thật vượt quá clip - gặp trường hợp nào cũng fail; phải sinh lại, tách cảnh, rút gọn thoại hoặc sửa `at`, cấm để phụ đề/tiếng kéo lấn sang cảnh sau.
    - lines không ghi `shot` hoặc speaker sai → `align` chặn/cảnh báo, theo hướng dẫn sửa lines.json rồi chạy lại.
21. **Hiệu ứng âm thanh + BGM** (chiếm phần thời gian không có thoại, tạo lớp lang âm thanh cho hình):
    - **Hiệu ứng** (tiếng súng/kéo ghế/bước chân/mở cửa/tát...): thêm mảng `sfx` vào cảnh đó trong `shots.json`: `[{"file": "sfx/gun.wav", "at": 1.2, "volume": 0.9}]` (`at` = giây **trong cảnh**). File hiệu ứng có thể dùng **ai-music** sinh đoạn ngắn (hoặc lấy từ thư viện), rồi điền đường dẫn vào `file`. `storyboard` sẽ quy đổi `at` trong cảnh sang thời gian toàn cục, `assemble` chèn đúng điểm vào track âm thanh của bản dựng.
    - **BGM**: dùng **ai-music** sinh theo không khí truyện (căng thẳng/ngọt/trinh thám), lưu vào `episodes/epNN/bgm.mp3` (khi trộn, assemble tự hạ nhạc để né lời dẫn).
    (Phụ đề đã được `align` xuất ra `voice.srt`, không cần chạy riêng auto-subtitle nữa.)

### 7. Ghép từng tập + bàn giao

22. Chuyển phân cảnh của tập thành đầu vào ghép rồi ghép. `storyboard` tự đọc kết quả kiểm: cảnh `native` thì **cho trọn track tiếng gốc (tiếng model + tiếng nền) đi thẳng**; cảnh `dub` thì **bỏ track gốc, dùng track TTS riêng** (không tách được giọng người thì giữ lại sẽ thành hai giọng chồng nhau); cảnh hoàn toàn không có tiếng gốc thì chèn khoảng lặng cùng độ dài; ducking sidechain chỉ để lời dẫn/lồng tiếng phủ sạch lên tiếng nền của cảnh native; bộ ghép chuẩn hoá AAC 48 kHz stereo rồi mới nối:
    ```bash
    python skills/openclaw/short-drama/scripts/drama_ops.py storyboard --series "<tên phim>" --episode N --size "<1080x1920 hoặc 1920x1080>" \
      -o episodes/epNN/storyboard.json --narration episodes/epNN/voice.mp3 --bgm episodes/epNN/bgm.mp3 --subtitle episodes/epNN/voice.srt
    python skills/openclaw/auto-short-video/scripts/assemble.py assemble \
      --storyboard episodes/epNN/storyboard.json -o episodes/epNN/final.mp4
    ```
    Phụ đề được assemble tự khắc theo kiểu **canh giữa dưới, cỡ chữ vừa phải** (mặc định theo độ phân giải, chỉnh tinh bằng `--sub-size/--sub-margin-v/--sub-font`).
23. Cuối mỗi tập có thể thêm "teaser tập sau/thẻ hook" để giữ khán giả theo dõi tiếp. **Dựng xong thì chấm theo mục "lồng tiếng/chọn giọng" và "bản dựng" trong `references/drama-review-rubric.md`** (nhất là xác nhận **không phải cả phim một giọng**, giọng khớp nhân vật, **phụ đề/lồng tiếng khớp hình**). Nhiều tập thì lặp bước 6-22 cho từng tập (kịch bản → phân cảnh → sinh video → lồng tiếng → ghép); dùng `progress show` để xem tiến độ cả bộ.
24. **Đăng bài**: theo khung hình/nền tảng đã xác nhận, bàn giao cho SKILL lớp đăng bài tương ứng (ví dụ dọc thì TikTok/YouTube Shorts, ngang thì YouTube).

## Nguyên tắc điều phối (kế thừa auto-short-video)

- **Hạ cấp là ngoại lệ, không phải mặc định** (khớp ba luật sắt): video cảnh nào cũng phải I2V, lồng tiếng mặc định chặn cứng edge, bản dựng mặc định chặn cứng ảnh tĩnh; chỉ khi người dùng nói rõ muốn phim ngắn bằng ảnh tĩnh mới dùng `storyboard --allow-static`, hoàn toàn không có key closed-source mới dùng `--allow-edge`; mọi lần hạ cấp đều phải **báo thật, báo rõ** cho người dùng biết hạ cái gì và vì sao. **Lưu hồ sơ sản phẩm trung gian + chạy tiếp từ điểm dừng**: ảnh tham chiếu/phân cảnh/clip/tiến độ đều ghi ra file, cảnh nào chưa ưng thì sinh lại riêng cảnh đó, progress chống đốt tiền lặp lại.

## Nhận biết Profile

- **Có Profile**: `platforms.md` chỉ dùng để gợi ý khung hình, vẫn phải hỏi người dùng xác nhận; `style.md` hoà vào tiền tố phong cách hình ảnh và bảng màu thống nhất; `identity.md` chốt tông thể loại; `preferences.md` lọc lằn ranh đỏ (bạo lực/gợi dục/giá trị quan).
- **Không có Profile**: hỏi trước ngang/dọc, thể loại/số tập/thời lượng mỗi tập và phong cách ưa thích; **không đặt sẵn thời lượng cố định** (người dùng không chỉ định thì theo nhịp thể loại mà chốt, đừng áp cứng một con số phút nào).

> Nguồn gốc phương pháp luận mã nguồn mở xem `EASEL-META.md`.
