# Easel Skill 能力地图

> 本文档按 Easel 的内容工作流分层介绍当前技能库。每个条目对应 `skills/openclaw/` 中一个可用的 `SKILL.md`。
> 当前共 **102 个 Skill**；这里只说明各 Skill 负责什么，具体输入、输出和执行流程请查看对应目录。

## 🗺️ 分层总览

| 层级 | Skill 数量 | 作用 |
|---|---:|---|
| 🧱 基础能力 | 6 | 贯穿发现、策划、创作、发布与归因的工作台基础能力。 |
| 🔭 发现层 | 9 | 发现热点、趋势、行业变化、竞品动态和内容机会。 |
| 🧭 策划层 | 16 | 把机会转化为定位、选题、结构、排期和可执行方案。 |
| 🎨 创作层 | 50 | 完成文字、视觉、音频、视频和复合内容的实际制作。 |
| 📣 发布层 | 11 | 完成平台适配、质量检查、排期、互动和真实发布。 |
| 📊 归因层 | 10 | 记录内容表现，分析数据与评论，并把结论用于下一轮策略。 |

## 🧱 基础能力

贯穿发现、策划、创作、发布与归因的工作台基础能力。

| Skill | 功能介绍 |
|---|---|
| `asset-manager` | Quản lý sản phẩm đã tạo trong outputs/: lưu trữ theo ngày/nền tảng/loại, gắn tag, tìm lại nội dung cũ, lập danh sách và thống kê tư liệu. |
| `batch-process` | Áp một thao tác cho cả thư mục ảnh/video/audio qua batch_process.py: nén, gắn watermark, đổi định dạng, scale, đổi tỉ lệ, chuẩn hoá âm lượng; xuất ra batch_out/, không ghi đè bản gốc. |
| `skill-my-account` | Tra tài khoản đã đăng nhập trong Easel (Facebook, TikTok, YouTube, Zalo) từ trạng thái đăng nhập cục bộ: danh tính, người theo dõi, lượt thích, đang theo dõi và danh sách bài, không cần hỏi tên tài khoản hay link. |
| `skill-profile-builder` | Hướng dẫn lần đầu dùng Easel: thu thập link mạng xã hội và ý định vận hành, phân tích nội dung đã đăng cùng gu lưu/thích để sinh hồ sơ tài khoản (Profile) 6 chiều từ đầu, đánh dấu phần còn thiếu để hỏi bổ sung. |
| `skill-profile-manager` | Quản lý vòng đời hồ sơ tài khoản (Profile): tạo hồ sơ trống, sửa 6 trường, ghi thêm memory, chuyển hồ sơ đang kích hoạt, xuất ra outputs/ và so sánh hai hồ sơ theo từng chiều. |
| `template-library` | Lưu, tái dùng và quản lý mẫu nội dung riêng của nhà sáng tạo: đúc bài thành công thành mẫu có biến, lần sau điền chủ đề là ra bài, có phân loại và quản lý phiên bản. |

## 🔭 发现层

发现热点、趋势、行业变化、竞品动态和内容机会。

| Skill | 功能介绍 |
|---|---|
| `skill-algorithm-updates` | Theo dõi thay đổi thuật toán, phân phối đề xuất, kiểm duyệt và quy tắc kiếm tiền của các nền tảng như Facebook, TikTok, YouTube, Zalo, phân tích tác động tới nhà sáng tạo và xuất bản tin có nguồn kèm gợi ý ứng phó. |
| `skill-competitor-analysis` | Mổ xẻ toàn diện chiến lược nội dung của kênh đối thủ cùng ngách: phân bố đề tài, định dạng, nhịp đăng, quy luật viral, cách tương tác, SWOT, từ đó chỉ ra cơ hội khác biệt và hành động ưu tiên có dữ liệu chứng minh. |
| `skill-content-gap-analysis` | Quét cung–cầu nội dung của một ngách trên mạng xã hội, đối chiếu tín hiệu tìm kiếm, trend và câu hỏi ở bình luận để tìm đề tài nhu cầu cao nhưng ít cạnh tranh, xuất danh sách đề tài xếp ưu tiên kèm 3-5 việc làm ngay. |
| `skill-cross-platform-diff` | Phân tích sâu cùng một chủ đề khác nhau thế nào giữa các nền tảng (hình thức, gu khán giả, ngôn ngữ, logic phân phối, đường kiếm tiền), chấm độ hợp từng nền tảng và gợi ý nền tảng chủ lực kèm hướng thích ứng. |
| `skill-event-calendar` | Tra N ngày tới có ngày lễ, ngày kỷ niệm, mốc sale, sự kiện ngành và thể thao để bắt điểm rơi nội dung, chấm giá trị bắt trend từng mốc, số ngày cần chuẩn bị và gợi ý hướng nội dung cho nhà sáng tạo. |
| `skill-news-intelligence` | Gom tin từ báo và trang tin ngành, tin chuyên ngành và động thái thương mại của nền tảng, lọc theo ngách của nhà sáng tạo để ra bản tin tình báo có cấu trúc kèm 3-5 đề tài làm được ngay. |
| `skill-rss-aggregator` | Tổng hợp feed RSS/Atom đã đăng ký của blogger, báo, newsletter: kéo bài mới, lọc theo từ khoá và khung thời gian, bỏ trùng lặp, xếp theo thời gian rồi ra tóm tắt đề tài/tin; thuần thư viện chuẩn, không phụ thuộc ngoài. |
| `skill-trending-topics` | Lấy bảng xếp hạng trend theo thời gian thực từ các nguồn đã cấu hình, lọc trend liên quan ngách của nhà sáng tạo, gợi ý 3-5 đề tài phái sinh kèm góc vào, định dạng, thời điểm đăng và nhận định xu hướng. |
| `skill-ugc-discovery` | Tìm nội dung do người dùng tạo (UGC) về thương hiệu/kênh: bài của fan, review, nhắc tên, thảo luận cộng đồng; phân loại cảm xúc, tách phản hồi tiêu cực, xuất danh sách UGC giá trị kèm link nguồn và gợi ý tương tác. |

## 🧭 策划层

把机会转化为定位、选题、结构、排期和可执行方案。

| Skill | 功能介绍 |
|---|---|
| `skill-account-diagnosis` | Chẩn đoán sức khỏe kênh từ hồ sơ tài khoản và dữ liệu nội dung gần đây, chỉ ra vấn đề theo cấu trúc bệnh → bằng chứng → đơn thuốc, kèm ý kiến xây kênh theo giai đoạn và gợi ý đăng bài. |
| `skill-article-outline` | Phân tích kết quả tìm kiếm rồi lập dàn ý bài dài gồm cấu trúc tiêu đề H2/H3, số chữ mục tiêu từng đoạn, vị trí biểu đồ và kế hoạch FAQ cho bài blog/website hoặc bài dài trên Facebook. |
| `skill-audience-profiler` | Phân tích đặc điểm, nỗi đau, nhu cầu, sở thích nội dung và kênh tiếp cận của người theo dõi để dựng 2-4 thẻ chân dung khán giả mục tiêu có thể hành động ngay. |
| `skill-brand-onboarding` | Thu thập thông tin công khai và phỏng vấn có cấu trúc về phong cách hình ảnh, tone nội dung, chân dung khán giả và mục tiêu vận hành để sinh bộ hồ sơ tài khoản (Profile) đầy đủ nhiều chiều. |
| `skill-campaign-planner` | Lập kế hoạch campaign marketing trọn gói cho Tết, đợt sale lớn, ra mắt sản phẩm hay sự kiện: mục tiêu, nhịp khởi động – bùng nổ – kéo dài, ma trận nội dung đa kênh, minigame, phân tầng KOL, ngân sách, rủi ro và KPI. |
| `skill-carousel-planner` | Lên cấu trúc từng trang cho bài nhiều ảnh (carousel): Hook trang bìa, nhịp nội dung, chữ và hướng hình ảnh mỗi trang, CTA trang cuối, caption đi kèm và điểm tương tác dự kiến. |
| `skill-collab-proposal` | Soạn đề xuất hợp tác theo hai chế độ: booking quảng cáo (báo giá theo bảng giá KOL, hình thức nội dung, lịch, KPI dự kiến) và collab với nhà sáng tạo/thương hiệu khác (thế mạnh bổ trợ, chia việc, quảng bá chéo). |
| `skill-content-calendar` | Lập lịch đăng theo tháng cho Facebook/TikTok/YouTube/Zalo: từng bài có đề tài cụ thể, góc khai thác và hướng hình ảnh, xếp theo trụ cột nội dung và tần suất chuẩn. |
| `skill-content-matrix` | Lập ma trận đề tài bằng cách giao trụ cột nội dung với 8 định dạng bài, mỗi ô là một đề tài cụ thể làm được ngay, kèm chấm điểm chọn ra các đề tài mạnh nhất. |
| `skill-content-strategy` | Lập chiến lược nội dung tổng thể gồm trụ cột nội dung, hành trình khán giả, nguyên tắc nhịp 90 ngày, kênh phân phối và hệ KPI, gộp thành một tài liệu chiến lược thực thi được. |
| `skill-hook-generator` | Sinh 6 biến thể Hook mở đầu cho mọi chủ đề theo các công thức đã kiểm chứng, mỗi Hook gồm 2 dòng mở màn và lật ngược, có kiểm tra số chữ từng dòng. |
| `skill-livestream` | Lập kế hoạch livestream trọn bộ gồm chủ đề, timeline, lời mở màn, câu chuyển đoạn, lời chốt đơn, cảm ơn, tương tác và checklist trước giờ live cho livestream bán hàng, chia sẻ kiến thức, giải trí. |
| `skill-positioning-analysis` | Tìm định vị khác biệt cho kênh/thương hiệu: quét ngách, vẽ toạ độ đối thủ, tìm khoảng trống, chọn điểm khác biệt về khán giả, bối cảnh, giá trị, hình thức, persona rồi chốt một câu định vị kèm gợi ý triển khai. |
| `skill-topic-evaluator` | Chấm một đề tài chưa làm theo 7 tiêu chí (lưu lượng, khớp kênh, khác biệt, thời sự, kiếm tiền, chi phí, rủi ro tuân thủ), kết luận làm, không làm hay đổi hướng kèm gợi ý sửa hoặc đề tài thay thế. |
| `skill-trend-rider` | Từ một trend hoặc sự kiện nóng cụ thể và định vị kênh, lên phương án bắt trend gồm đánh giá độ liên quan, góc vào, hình thức, gợi ý tiêu đề, thời điểm đăng và cảnh báo rủi ro. |
| `skill-voice-builder` | Dựng hồ sơ giọng văn (voice/tone: giọng điệu, từ ngữ, nhịp, phong cách) của nhà sáng tạo qua phỏng vấn có cấu trúc và phân tích mẫu viết để nội dung về sau giữ được sự nhất quán. |

## 🎨 创作层

完成文字、视觉、音频、视频和复合内容的实际制作。

| Skill | 功能介绍 |
|---|---|
| `ai-image-gen` | Sinh ảnh AI mọi chủ đề: chữ thành ảnh, ảnh thành ảnh theo lệnh chỉnh sửa và biến thể từ một ảnh, qua API tương thích OpenAI hoặc API bất đồng bộ apimart với API key của người dùng, xuất vào outputs/. |
| `ai-music` | Sinh nhạc nền/BGM gốc (không lời hoặc có hát) cho video ngắn và nội dung mạng xã hội từ mô tả phong cách qua provider cắm được (MUSIC_PROVIDER): gửi bất đồng bộ, poll rồi tải về, sau đó cắt, chuẩn hoá hay gắn vào video. |
| `ai-video-gen` | Sinh video mới bằng AI từ 0: chữ→video, ảnh→video (làm ảnh động), người ảo dẫn từ khung đầu; gọi bất đồng bộ qua provider cắm được (VIDEO_PROVIDER trong .env) với API key của người dùng, xuất video vào outputs/. |
| `audio-denoise` | Khử ồn bản ghi âm: lọc tiếng nền, tiếng rè điện, gió, ù bằng chuỗi filter ffmpeg (afftdn/highpass/lowpass, tuỳ chọn RNNoise) theo 3 mức, xử lý cả audio lẫn track tiếng của video, kèm báo cáo trước–sau. |
| `audio-editing` | Xử lý âm thanh chung qua audio_ops.py: cắt đoạn, đổi định dạng mp3/wav/m4a/aac, chuẩn hoá âm lượng, tách audio từ video, nối nhiều đoạn, fade in/out, đổi tốc độ giữ cao độ; xuất file mới vào outputs/, giữ bản gốc. |
| `audio-mix` | Trộn lời dẫn, nhạc nền và hiệu ứng thành một track audio thuần qua audio_mix.py: BGM tự lặp cho đủ dài lời dẫn, ducking tự hạ nhạc khi có giọng nói, hiệu ứng đặt theo mốc giây, xuất mp3/wav/m4a. |
| `audio-visualizer` | Render audio thuần (podcast, nhạc, câu nói hay, radio) thành video mp4 có sóng/phổ động (cqt/bars/waves/spectrum) kèm ảnh bìa và tiêu đề qua audio_viz.py để đăng lên các nền tảng chỉ nhận video. |
| `auto-short-video` | Từ một câu chủ đề tự nối lời → ảnh minh hoạ/AI video → giọng đọc → phụ đề → BGM → ghép thành một video ngắn hoàn chỉnh dạng nói/tin tức; hình mặc định ảnh theo từng câu + Ken Burns, chỉ ảnh→video ở cảnh cần chuyển động. |
| `auto-subtitle` | Nhận dạng giọng nói trong file audio hoặc video thành file phụ đề SRT/ASS/TXT/JSON qua asr.py (faster-whisper), tự tách âm thanh từ video, tuỳ chọn đốt phụ đề cứng vào video bằng ffmpeg. |
| `beat-sync-video` | Dựng video bắt nhịp nhạc qua beatsync.py (librosa): phát hiện beat của nhạc nền, chuyển ảnh hoặc clip đúng điểm nhịp kèm hiệu ứng zoom/nháy trắng, tự lặp tư liệu khi thiếu, xuất video kèm báo cáo BPM và số đoạn. |
| `card-design` | Hệ thiết kế hình ảnh cho thẻ mạng xã hội: bảng màu, phân cấp chữ, bố cục kín khung, khung xương theo loại thẻ, kiểm khoảng trống chết/mật độ; tránh PPT mẫu và mùi AI rẻ tiền, là quy chuẩn chung cho card-* và poster-hero. |
| `card-quote` | Sinh thẻ trích dẫn hoặc thẻ số liệu ngang 16:9 (một câu hero hay một cụm số liệu chính) để chia sẻ trên Facebook, Threads/X, LinkedIn, render từ HTML thành ảnh theo phong cách đã chọn trong card-design. |
| `card-xiaohongshu` | Render văn bản thẻ có sẵn thành bộ thẻ kiến thức dọc 1080×1440 dạng lướt (thẻ bìa, thẻ thân, thẻ chốt; 3-9 thẻ, mỗi thẻ một ý), chọn phong cách theo card-design và kiểm khoảng trống chết sau khi render. |
| `chart-visualization` | Vẽ biểu đồ từ dữ liệu đầu vào với 25+ loại (cột, đường, tròn, phân tán, radar, sankey, sơ đồ tư duy, lưu đồ, bảng) bằng cách gọi AntV API qua mạng với curl, trả về URL ảnh tĩnh chèn ngay dạng Markdown. |
| `clipify` | Tự tìm điểm gây cười trong video nói tiếng Anh, cắt thành các video ngắn độc lập, chuyển 16:9→9:16 bằng pan bám mặt người đang nói hoặc chia đôi màn hình, rồi đốt phụ đề theo từng chữ kiểu opus/karaoke/minimal. |
| `comparison-card` | Làm ảnh so sánh A vs B kiểu "một ảnh nói hết" cho 2-4 đối tượng: bảng thông số, ưu–nhược, thông số sản phẩm với bố cục table/versus/pros_cons, render HTML+CSS thành thẻ chụp được, chia sẻ Facebook/Threads. |
| `copywriting` | Viết văn bản bán hàng chuyển đổi: chắt lọc điểm bán theo FAB rồi ra tiêu đề, thân bài, CTA kèm phương án thay thế cho bài seeding, quảng cáo feed, khuyến mãi, trang chi tiết sản phẩm và landing page. |
| `data-report` | Sinh trang báo cáo trực quan hoàn chỉnh từ CSV/Excel/JSON gồm thẻ KPI, 2-4 biểu đồ, bảng dữ liệu và 3-5 insight; report.py tính mọi số liệu từ dữ liệu thật, xuất HTML tự chứa và render được thành ảnh dài chia sẻ. |
| `doc-convert` | Dàn trang và chuyển bản thảo Markdown thành HTML sạch, PDF A4 in được hoặc ảnh dài PNG chỉnh được bề rộng bằng doc_convert.py (python-markdown + Chromium) để lưu trữ, gửi đi hay đăng nơi không hỗ trợ Markdown. |
| `ecom-details-image` | Lập phương án hình ảnh sản phẩm thương mại điện tử: ý tưởng ảnh chính, ảnh bối cảnh, hướng hình ảnh trang chi tiết và Prompt sinh ảnh AI, mặc định 5 ảnh chính + 7-9 ảnh trang chi tiết cùng một phong cách khoá chung. |
| `green-screen` | Tách nhân vật quay trên phông xanh (hoặc xanh dương/màu chỉ định) rồi ghép vào nền mới là ảnh, video, màu đơn hay chính tiền cảnh làm mờ qua chromakey.py (ffmpeg chromakey + despill), giữ nguyên âm thanh gốc. |
| `image-editing` | Gia công ảnh có sẵn một cách tất định bằng image_ops.py: resize, cắt, pad theo tỉ lệ nền tảng, đổi định dạng png/jpg/webp, nén về dung lượng đích, watermark chữ/ảnh, bo góc, ghép nhiều ảnh, thu nhỏ, đọc thông tin ảnh. |
| `image-enhance` | Nâng chất lượng ảnh mờ, tối, nhiễu bằng img_enhance.py (Pillow + OpenCV): phóng to Lanczos 2x/4x, khử nhiễu, làm nét, tự động tương phản và bão hoà; tăng cường truyền thống, không phải AI siêu phân giải. |
| `infographic` | Biến dữ liệu/văn bản thành infographic render cục bộ theo hai chế độ: tĩnh AntV với 50+ mẫu danh sách, lưu đồ, so sánh, SWOT xuất được SVG; hoặc GIF động kiểu đua cột, số chạy, tiến độ, đường mọc qua gif_chart.py. |
| `meme-generator` | Làm meme/ảnh chế từ ảnh có sẵn bằng meme_ops.py (Pillow): chữ lớn trắng viền đen trên/dưới kiểu kinh điển, hoặc thêm dải chữ trên/dưới kiểu ảnh phản ứng, tự xuống dòng và chỉnh cỡ chữ, xuất jpg/png. |
| `mindmap` | Render dàn ý Markdown (cấp tiêu đề + danh sách) thành sơ đồ tư duy HTML tương tác bằng mindmap.py (markmap, một file HTML), tuỳ chọn xuất PNG qua Chromium; hợp cấu trúc kiến thức, khung nội dung, SWOT. |
| `multi-voice-dubbing` | Lồng tiếng hội thoại nhiều vai: theo dàn nhân vật (cast) và từng dòng thoại gán giọng cùng cảm xúc cho mỗi vai, tổng hợp một track nhiều giọng kèm phụ đề có tên vai, làm lời dẫn cho video hoặc trộn thêm BGM. |
| `novel-writer` | Viết tiểu thuyết/truyện dài kỳ từ thế giới quan, nhân vật, dàn ý 3 cấp tới từng chương, chú trọng ba chương đầu giữ chân; trạng thái lưu thành file để giữ mạch ngầm, tiền truyện và nhất quán giữa các chương. |
| `paper-explainer` | Giải thích bài báo khoa học: đọc arXiv/PDF kể cả công thức và hình, rút vấn đề, đóng góp, phương pháp, hình chính, kết luận rồi làm video giải thích (slide, lồng tiếng, phụ đề) hoặc bài ảnh-chữ, trung thành với bản gốc. |
| `post-formatter` | Cấu trúc chủ đề theo khung kinh điển (PAS, AIDA, BAB, STAR, SLAY) thành bài đăng ngắn tối đa 20 dòng, dễ đọc trên mobile: hook mở đầu, dòng lật ngược, thân theo từng giai đoạn của khung, câu kêu gọi tương tác cuối bài. |
| `poster-hero` | Sinh poster marketing dọc 1080×1920 gồm tiêu đề lớn, 3-5 điểm bán chính, CTA và mã QR tuỳ chọn, nền có gu theo phong cách card-design, phục vụ ra mắt sản phẩm, quảng bá sự kiện và chia sẻ story/feed. |
| `remove-bg` | Tách chủ thể khỏi nền ảnh bằng phân đoạn AI (rembg, remove_bg.py) mà không cần phông xanh: xuất PNG trong suốt, thay nền trắng cho ảnh sản phẩm thương mại điện tử, nền màu hoặc ghép vào cảnh nền mới. |
| `short-drama` | Làm phim ngắn AI nhiều tập: dựng kinh thánh phim và ảnh tham chiếu nhân vật, viết kịch bản từng tập, ảnh→video từng cảnh, kiểm thoại, lồng tiếng + phụ đề + BGM, ra thành phẩm, giữ nhất quán giữa các cảnh và các tập. |
| `slideshow-video` | Ghép một bộ ảnh có sẵn thành video với hiệu ứng Ken Burns, chuyển cảnh giữa ảnh, nhạc nền và phụ đề từng ảnh, tự khớp khung hình dọc/vuông/ngang; dựa trên slideshow.py (ffmpeg tất định), xuất video vào outputs/. |
| `social-content` | Viết nội dung mạng xã hội theo định dạng gốc của Facebook, TikTok, YouTube, Zalo: hook, thân bài, chiến lược hashtag, kêu gọi tương tác kèm 2-3 biến thể, thiên về tăng follow; mặc định khi chưa rõ nền tảng. |
| `style-transfer` | Đổi phong cách một đoạn văn bản mà giữ nguyên ý cốt lõi (nghiêm túc → hài, văn viết → văn nói, văn hoa → thẳng, trang trọng → giọng mạng xã hội), có thể học từ mẫu phong cách đích, kèm tóm tắt thay đổi. |
| `subtitle-translate` | Dịch phụ đề có sẵn (SRT/VTT/ASS) sang ngôn ngữ đích, xuất bản song ngữ (gốc + dịch) hoặc chỉ bản dịch, gắn mềm hoặc đốt cứng vào video; LLM dịch từng dòng, subtitle_ops.py xử lý timeline, định dạng và đốt. |
| `text-condenser` | Nén văn bản dài về số chữ chỉ định mà vẫn giữ ý cốt lõi theo ba chế độ: cắt cứng đúng số chữ (script kiểm đếm), tóm tắt giữ ý chính, trích câu đắt nhất; kèm báo cáo nén và danh sách ý đã giữ. |
| `text-polisher` | Trau chuốt văn bản qua 7 vòng quét tập trung (rõ ràng, giọng, giá trị, bằng chứng, cụ thể, cảm xúc, rủi ro) và khử mùi AI (cắt câu đệm, phá cấu trúc công thức, câu chủ động, đổi nhịp), xuất bản sửa kèm bảng điểm. |
| `tts-voiceover` | Chuyển văn bản thành giọng đọc AI cho lời dẫn, thuyết minh, đọc bài: có VOICE_PROVIDER thì đi TTS đám mây giọng tự nhiên có cảm xúc, không key thì edge-tts dự phòng (giọng máy hơn); xuất mp3/wav/m4a kèm SRT tách câu. |
| `video-chapters` | Tự chia chương và lập mục lục timestamp cho video trung/dài (chương YouTube, phần mô tả video) để người xem nhảy nhanh, tăng tỉ lệ xem hết; asr.py bóc băng có timeline, LLM chia và đặt tên chương theo chuyển đề tài. |
| `video-editing` | Dựng một video bằng lệnh ngôn ngữ tự nhiên qua video_ops.py (ffmpeg): cắt, ghép, đổi tốc độ, jump-cut bỏ khoảng lặng, chèn chữ, đổi tỉ lệ ngang/dọc, trích khung làm bìa, ra GIF, nén, thêm BGM/watermark. |
| `video-highlights` | Tìm highlight trong video dài hoặc bản ghi livestream theo đỉnh năng lượng âm thanh hoặc bóc băng rồi chọn câu đắt, cắt thành nhiều video ngắn qua highlight_cut.py (librosa), tuỳ chọn chuyển dọc 9:16 và thêm phụ đề. |
| `video-intro-outro` | Tạo thẻ mở đầu và kết thúc cho video (tiêu đề, tiêu đề phụ, logo, kêu gọi theo dõi/đăng ký) rồi nối vào video chính bằng cắt cứng hoặc chuyển cảnh fade, toàn bộ qua intro_outro.py (ffmpeg). |
| `video-reframe` | Đổi khung hình video thông minh sang 9:16/16:9/1:1 qua reframe.py theo ba cách: nền mờ lấp không viền đen, cắt theo tiêu điểm, cắt giữ mặt ở giữa nhờ nhận diện khuôn mặt; xuất video kèm báo cáo chiến lược đã dùng. |
| `video-script` | Viết kịch bản video từ ngắn 7-60 giây (biến thể Hook có chấm điểm, bấm giờ theo giây, lời phụ đề, phương án bìa) tới trung/dài 1-30 phút (tối ưu giữ chân, điểm ngắt nhịp, hook dẫn tiếp, cấu trúc chương). |
| `video-strategy` | Lập chiến lược sản xuất video và chọn công cụ: so sánh model AI tạo video, thiết kế cấu trúc kịch bản, quy cách từng nền tảng và quy trình sản xuất cho demo sản phẩm, video giải thích, video ngắn mạng xã hội. |
| `video-to-article` | Bóc băng video nói, bài giảng, livestream, vlog rồi viết lại có cấu trúc thành bài Facebook, blog hay bài ảnh-chữ (tiêu đề, đề mục, câu đắt, hashtag), kèm trích khung hình tại mốc thời gian phù hợp làm ảnh minh hoạ. |
| `voice-clone` | Tải mẫu giọng của chính người dùng lên provider đám mây (tự có key) để nhân bản giọng riêng, rồi tổng hợp lời dẫn, thuyết minh hay giọng bán hàng bằng giọng đó; chỉ nhân bản giọng mà người dùng có quyền sử dụng. |
| `xhs-note-creator` | Sinh trọn bộ bài đăng ảnh-chữ từ chủ đề và tư liệu: tiêu đề, thân bài, caption, hashtag cùng 3-9 thẻ ảnh dọc hoặc phân cảnh video ngắn, có phân tích tư liệu, đánh giá điểm bán, khử mùi AI và kiểm chất lượng. |

## 📣 发布层

完成平台适配、质量检查、排期、互动和真实发布。

| Skill | 功能介绍 |
|---|---|
| `skill-community-ops` | Vận hành bình luận và ứng phó khủng hoảng sau đăng: mẫu trả lời phân tầng theo 5 loại bình luận kèm quy tắc xử lý theo mức, khai thác đề tài từ bình luận; có sự cố thì phân cấp, dự thảo tuyên bố, thống nhất phát ngôn. |
| `skill-content-repurposing` | Tách một bài gốc (bài viết, kịch bản video, bản ghi livestream) theo tháp trụ cột – phái sinh – vi nội dung rồi viết lại thành nội dung bản địa cho từng nền tảng như Facebook, TikTok, YouTube, Zalo, kèm thứ tự đăng. |
| `skill-facebook-page-upload` | Đăng bài lên Trang Facebook qua Meta Graph API (bài chữ, một ảnh, album, video, hashtag): đăng nhập thiết bị bằng mã QR, chạy thử trước rồi mới `--exec`, qua content_guard, ghi lịch và manifest sau khi đăng. |
| `skill-persona-check` | Kiểm tra nhất quán persona và tone thương hiệu của nội dung so với hồ sơ (Profile) về định vị, ngách, hình thức, khán giả, phong cách, sở thích; chấm điểm, chỉ rõ điểm lệch kèm gợi ý sửa, chỉ cảnh báo không chặn đăng. |
| `skill-publish-checklist` | Kiểm đủ trước khi đăng: rà từng mục tiêu đề, ảnh bìa, hashtag, định dạng, nhãn tuân thủ, link, CTA có đủ chưa, kết luận đăng được hay chưa kèm danh sách mục còn thiếu và cách bổ sung. |
| `skill-publish-notify` | Đẩy thông báo sau khi đăng: thành công hay thất bại đều gửi kết quả (trạng thái, tiêu đề, nền tảng, link) tới Telegram, Slack, webhook bất kỳ hoặc bot nhóm Feishu/DingTalk/WeCom; thuần script, không phụ thuộc ngoài. |
| `skill-publish-scheduler` | Hẹn giờ đăng hàng loạt theo bảng "nội dung × nền tảng × giờ đăng": nhập lịch, xem hàng đợi, tính mục đến hạn, đến giờ giao cho SKILL đăng của từng nền tảng rồi ghi lại trạng thái; lập lịch thuần script, không tự đăng. |
| `skill-quality-gate` | Cổng chất lượng trước khi đăng, một lần kiểm hai cửa: soát rủi ro tuân thủ (từ nhạy cảm, từ tuyệt đối, quy tắc nền tảng) và thẩm định chất lượng sản phẩm (đầy đủ, dễ đọc, hợp nền tảng), chốt đăng được/cần sửa/không đạt. |
| `skill-risk-scanner` | Đánh giá độ nguyên bản và rủi ro bản quyền bằng LLM: dấu hiệu xào bài/đăng lại, bản quyền ảnh và nhạc, chuẩn trích dẫn, thương hiệu; xuất báo cáo rủi ro thấp/trung bình/cao kèm gợi ý sửa, không check trùng kỹ thuật. |
| `skill-seo-quality` | Kiểm và tối ưu để bài hiện trong kết quả tìm kiếm của nền tảng: từ khoá ở tiêu đề, thân bài, hashtag, chữ trên ảnh bìa/khung đầu, cân đối tìm kiếm và đề xuất; xuất báo cáo kèm Top 3 việc sửa, có chế độ SEO web/blog. |
| `skill-short-link` | Gắn tham số UTM (nguồn/kênh/chiến dịch) vào link nội dung hoặc quảng cáo rồi rút gọn qua dịch vụ công khai không cần key, mỗi kênh một link riêng để theo dõi nguồn truy cập và hiệu quả campaign trên từng nền tảng. |

## 📊 归因层

记录内容表现，分析数据与评论，并把结论用于下一轮策略。

| Skill | 功能介绍 |
|---|---|
| `roi-calculator` | Tính ROI content marketing từ dữ liệu chạy quảng cáo: CTR/CPC/CPM/ROAS, CPA, lợi nhuận, đối chiếu chuẩn ngành; phân tích một chiến dịch hoặc so sánh nhiều chiến dịch xếp theo ROI kèm gợi ý phân bổ ngân sách. |
| `skill-comment-insights` | Phân tích định lượng bình luận: tỉ lệ cảm xúc tích cực/trung tính/tiêu cực kèm bình luận tiêu biểu, từ và cụm từ tần suất cao, khai thác nhu cầu/phàn nàn/câu hỏi làm dữ liệu cho hậu kiểm nội dung và gợi đề tài. |
| `skill-content-calendar-log` | Nền lịch nội dung thống nhất: tự ghi mọi lần đăng từ trang đăng/chat, lịch người dùng xếp và sự kiện nền tảng/lễ/ngày đặc biệt vào một timeline để Agent đọc lại trước khi lập kế hoạch đề tài, lịch đăng. |
| `skill-content-postmortem` | Hậu kiểm nội dung hai chế độ: mổ xẻ một bài đã đăng vì sao viral hay xịt theo Hook, cấu trúc, đề tài, thời điểm, nền tảng kèm 3 việc cải thiện; hoặc từ nhiều bài rút quy luật viral thành công thức lặp lại được. |
| `skill-data-tracker` | Ghi snapshot chỉ số kênh theo ngày (follower, tương tác), phân tích xu hướng tăng trưởng (tốc độ, đổi nhịp, dự báo mốc) và theo dõi vòng đời một bài từ đăng tới suy giảm, phân loại bùng nổ nhanh, tăng đều hay đuôi dài. |
| `skill-post-scorer` | Chấm tiềm năng tương tác của bản nháp bài đăng trước khi đăng theo 5 chiều (Hook, khớp giọng văn, mật độ giá trị, cấu trúc, sẵn sàng đăng), đối chiếu hiệu quả lịch sử, xuất thẻ điểm kèm gợi ý sửa phần yếu nhất. |
| `skill-publish-analytics` | Phân tích nhật ký đăng theo 4 chiều (thời điểm đăng, hiệu quả hashtag, loại nội dung, tăng trưởng follower) để quy kết hiệu quả nội dung, xuất báo cáo có phát hiện chính, phương pháp, hạn chế và đề xuất tối ưu. |
| `skill-publish-log` | Quản lý nhật ký đăng bài: ghi từng lần đăng (nền tảng, tiêu đề, link, thời gian, số liệu ban đầu, tag), tra cứu theo thời gian, nền tảng, từ khoá và thống kê số bài, tổng tương tác để hậu kiểm và quy kết. |
| `skill-social-performance-review` | Phân tích hiệu quả nội dung tháng trước trên Facebook, TikTok, YouTube, Zalo từ CSV, ảnh chụp hoặc mô tả, tìm mô hình hiệu quả và nguyên nhân thất bại, xuất báo cáo hậu kiểm tháng kèm đề xuất thực thi cho tháng sau. |
| `skill-strategy-advisor` | Phân tích hiệu quả nội dung gần đây, hồ sơ tài khoản và xu hướng ngành để tối ưu lặp chiến lược: khuyến nghị giai đoạn tới về hướng nội dung, ngách mới, hình thức, nhịp đăng, tinh chỉnh hồ sơ, kèm danh sách hành động. |
