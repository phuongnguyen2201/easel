# Easel Skill 能力地图

> 本文档按 Easel 的内容工作流分层介绍当前技能库。每个条目对应 `skills/openclaw/` 中一个可用的 `SKILL.md`。
> 当前共 **112 个 Skill**；这里只说明各 Skill 负责什么，具体输入、输出和执行流程请查看对应目录。

## 🗺️ 分层总览

| 层级 | Skill 数量 | 作用 |
|---|---:|---|
| 🧱 基础能力 | 6 | 贯穿发现、策划、创作、发布与归因的工作台基础能力。 |
| 🔭 发现层 | 9 | 发现热点、趋势、行业变化、竞品动态和内容机会。 |
| 🧭 策划层 | 16 | 把机会转化为定位、选题、结构、排期和可执行方案。 |
| 🎨 创作层 | 50 | 完成文字、视觉、音频、视频和复合内容的实际制作。 |
| 📣 发布层 | 20 | 完成平台适配、质量检查、排期、互动和真实发布。 |
| 📊 归因层 | 11 | 记录内容表现，分析数据与评论，并把结论用于下一轮策略。 |

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
| `ai-image-gen` | 通用 AI 生图：文生图 / 图生图 / 图像变体。 |
| `ai-music` | AI 音乐 / BGM 生成：给短视频、社媒内容生成原创背景音乐 / 配乐 / 纯音乐。通过可插拔 provider（阿里 DashScope / Suno 类第三方 API）文生音乐，异步提交→轮询→下载，产物可再裁剪/归一化或加到视频。 |
| `ai-video-gen` | AI 视频生成：文生视频 / 图生视频 / 数字人首帧驱动。通过可插拔 provider（通义万相 Wan / 火山 Seedance / 快手可灵 / OpenAI 兼容）异步生成视频，需要配置相应生成服务。 |
| `audio-denoise` | 音频降噪：去除录音中的背景噪声、电流声、风噪、嗡嗡声。 |
| `audio-editing` | 通用音频处理：音频剪辑/裁剪、格式转码（mp3/wav/m4a/aac）、音量归一化、从视频提取音轨、多段拼接、淡入淡出、变速（保音高）。 |
| `audio-mix` | 音频混合 / 混音：把旁白口播 + 背景音乐 + 音效混成一轨，BGM 自动循环补足并可闪避（旁白说话时自动压低 BGM 保证人声清晰）。 |
| `audio-visualizer` | 音频可视化视频：把纯音频（播客片段、音乐、口播金句、电台）渲染成带动态波形/频谱的视频，配封面和标题，好发到抖音/B站/视频号等只收视频的平台。 |
| `auto-short-video` | 一句话主题 → 成品短视频：自动串联 文案→配图/AI视频→配音→字幕→BGM→合成，把 Easel 制作层零件编排成一条'一键出片'流水线。单条视频、口播/资讯向，画面默认逐句配图 + Ken Burns 缓动，需要动态时才逐段图生视频。 |
| `auto-subtitle` | 自动字幕 / 语音转字幕：把音频或视频里的语音识别成字幕文件（SRT/ASS/TXT/JSON），可选把字幕烧录进视频。 |
| `beat-sync-video` | 音乐卡点视频 / 踩点视频：检测背景音乐的节拍，让图片或片段在节拍点上切换，配推进/白闪特效，做出燃系'卡点'短视频。 |
| `card-design` | 社媒卡片视觉设计系统：提供配色、中文字体层级、满画幅布局、品类骨架和死空白/密度质检，避免模板化 PPT 与廉价 AI 感。 |
| `card-quote` | 生成适合微博、知乎、公众号或 X/Twitter 分享的 16:9 横版金句卡和数据卡。 |
| `card-xiaohongshu` | 把已有卡片文案渲染为 1080×1440 小红书竖版知识卡片组，并按 card-design 选择视觉风格。 |
| `chart-visualization` | 将数据可视化为图表。当用户需要生成柱状图、折线图、饼图、散点图、雷达图、桑基图、思维导图、流程图等图表时调用此技能，通过 curl 工具调用 AntV API 生成图表图片。产出静态图片 URL（25+ 类型）。 |
| `clipify` | 从长视频中自动提取精彩片段，切成独立短视频，支持 16:9→9:16 竖版转制和逐字字幕烧录。 |
| `comparison-card` | 对比图/一图流：生成 A vs B 参数对比图、优劣势对比表、产品参数一图流。 用 HTML+CSS 渲染成可截图的视觉卡片，适合小红书/微博等平台分享。 |
| `copywriting` | 国内带货转化营销文案：提炼卖点并产出种草、信息流广告、活动促销、电商详情页或落地页的标题、正文和 CTA。 |
| `data-report` | 把 CSV、Excel 或 JSON 数据生成包含 KPI、图表和洞察的完整可视化报告页。 |
| `doc-convert` | 把 Markdown 文稿排版并转换为 HTML、可打印 PDF 或长图 PNG。 |
| `ecom-details-image` | 生成电商商品视觉方案：主图概念、场景图、详情页视觉方向和 AI 生图 Prompt。 |
| `green-screen` | 绿幕抠像 / 换背景 / 合成：把绿幕（或蓝幕/指定色）拍摄的前景人物抠出来，合成到新背景——图片、视频、纯色或前景自身模糊。 |
| `image-editing` | 通用图像处理加工：改尺寸/缩放、裁剪、补边适配平台尺寸、格式转换（png/jpg/webp）、 压缩到目标大小、加文字或图片水印、圆角、多图拼接、生成缩略图、读图片信息。 基于 image_ops.py 确定性处理。 |
| `image-enhance` | 图片增强 / 放大 / 变清晰：高质量放大（Lanczos 2x/4x）+ 去噪 + 锐化 + 自动对比度/饱和度，改善偏糊、偏暗、噪点多的图片。 |
| `infographic` | 将数据或文字内容转化为可视化信息图，支持静态（AntV）和动画 GIF 两种模式。当用户需要制作信息图、数据可视化、流程图、对比图、动画图表、GIF 图表、思维导图、SWOT 分析图时调用。本地渲染信息图/GIF 动画。 |
| `meme-generator` | 表情包 / Meme 生成：给图片加经典上下大字（白字黑边）做梗图，或在图上/下加配文条做反应图（'当…的时候'格式）。中英文都支持，自动换行和字号自适应。 |
| `mindmap` | 思维导图：把 Markdown 大纲（标题层级 + 列表）渲染成可交互思维导图 HTML，可选导出 PNG。适合知识结构、内容框架、SWOT、脑图梳理。 |
| `multi-voice-dubbing` | 多角色对话配音：按 cast 和逐行对白为不同角色分配音色与情绪，合成多声线音轨和带角色名字幕。 |
| `novel-writer` | 长篇小说/网文连载创作：从世界观、人设和三级大纲写到逐章正文，并用文件化状态维护伏笔、前情和跨章一致性。 |
| `paper-explainer` | 科研论文解读：解析 arXiv/PDF 的公式与图表，提炼问题、贡献、方法、关键图和结论，再产出 B站/视频号解读视频或知乎/公众号图文。 |
| `post-formatter` | 用 PAS、AIDA、BAB、STAR、SLAY 等经典框架将主题结构化为社媒帖子。 200-250 字、20 行以内、移动端友好排版。适用于公众号、知乎、微博、LinkedIn 等长文帖子。 |
| `poster-hero` | 生成 1080×1920 竖版营销海报，包含大标题、核心卖点和可选二维码，适合产品发布、活动宣传与朋友圈传播。 |
| `remove-bg` | 图片去背景 / 抠图 / 换背景：用 AI 语义分割把主体从背景抠出，输出透明 PNG，或直接换成纯色（电商白底）/ 新场景背景。无需绿幕。 |
| `short-drama` | 制作多集 AI 微短剧：建立剧集圣经和角色参考，完成分集剧本、逐镜 I2V、对白审计、配音字幕 BGM 与成片，保持跨镜跨集一致性。 |
| `slideshow-video` | 图片相册 → 视频：把一组图片做成带 Ken Burns 缓慢缩放、图间转场、背景音乐和逐图字幕的视频，自动适配平台画幅（竖版/方形/横版）。 |
| `social-content` | 通用多平台社媒内容（单条/兜底）：钩子文案、正文、标签策略和互动引导，主打涨粉/互动/内容运营， 支持微博/抖音/B站/知乎/公众号/X 等；平台不确定或要多平台一次成稿时的默认选择。 |
| `style-transfer` | 文案风格迁移：把一段文案从一种风格改写成另一种风格（严肃→搞笑、书面→口语、文艺→直白、正式→社交媒体感）， 支持风格参考（给一段目标风格的示例文本）。 |
| `subtitle-translate` | 字幕翻译 / 双语字幕：把已有字幕（SRT/VTT/ASS）翻译成目标语言，生成双语（原文+译文）或纯译文字幕，并可软挂载 / 硬烧录进视频。 |
| `text-condenser` | 字数裁剪/摘要：把长文本压缩到指定字数，保留核心信息。支持硬裁剪（严格字数）、 摘要（保留要点）、金句提取（只保留最精华的句子）三种模式。 特别适合从长文生成平台适配的短文。 |
| `text-polisher` | 文本润色打磨：七轮聚焦扫描（清晰度/语气/价值感/证据/具体性/情感/风险） + 去 AI 感改写（砍填充短语、打破公式化结构、主动语态、变化节奏）。 |
| `tts-voiceover` | 文字转语音配音：把文案/脚本合成为 AI 语音口播、旁白、朗读音频。配了 VOICE_PROVIDER 默认走闭源云 TTS（CosyVoice2 等，有情感、像真人），edge 仅无 key 时兜底（edge 偏机械/AI 味）；同步输出分句 SRT 字幕、mp3/wav/m4a。 |
| `video-chapters` | 视频章节 / 时间戳目录：给中长视频自动生成章节划分和时间戳目录，用于 B站分P/YouTube 章节/视频描述区，方便观众跳转、提升完播。 |
| `video-editing` | 用自然语言指令剪辑视频：裁剪、拼接、变速、跳切去静音、文字覆盖、横竖比转换、抽帧封面、转 GIF、压缩、加 BGM/水印。 |
| `video-highlights` | 长视频 / 直播录像高光切片：从一条长视频里找出高光片段，切成多条独立短视频，可选转竖版 9:16 + 加字幕。找点两种方式——音频能量峰值（情绪高涨/欢呼/大声处）或转录后由内容判断挑金句段。 |
| `video-intro-outro` | 视频片头 / 片尾：生成带标题、副标题、logo、关注引导的片头卡片和片尾卡片，并拼接到主视频（硬切或淡入淡出转场）。 |
| `video-reframe` | 智能转换视频画幅，支持 9:16/16:9/1:1、模糊背景填充、焦点裁切和人脸居中裁切。 |
| `video-script` | 生成视频脚本，覆盖短视频（7-60秒）到中长视频（1-30分钟）全时长。 短视频：Hook 变体评分、分秒计时、字幕文案、封面方案。 中长视频：留存率优化、节奏中断点、前向钩子、章节结构。 适用于抖音、视频号、小红书视频、B站、YouTube 等平台。 |
| `video-strategy` | 视频制作策略与工具选型：AI 视频生成模型对比、视频脚本结构设计、制作流程规划，覆盖产品演示/解说/社媒短视频场景。 |
| `video-to-article` | 把口播、讲座、直播或 Vlog 转录并改写成小红书笔记、公众号文章或知乎内容，同时抽帧配图。 |
| `voice-clone` | 上传本人语音样本克隆专属音色，再用它合成口播、旁白或带货语音。 |
| `xhs-note-creator` | 小红书内容总入口：生成标题、正文、caption、hashtags，以及 3-9 张图文卡片或短视频分镜，覆盖素材分析、卖点评估、去 AI 味和质检。 |

## 📣 发布层

完成平台适配、质量检查、排期、互动和真实发布。

| Skill | 功能介绍 |
|---|---|
| `skill-bilibili-upload` | B站视频投稿：把视频投稿到哔哩哔哩，支持标题/简介/分区/标签/封面/转载声明/定时发布。 |
| `skill-channels-upload` | 微信视频号发布：把竖版短视频发布到微信视频号（channels.weixin.qq.com）。 |
| `skill-community-ops` | Vận hành bình luận và ứng phó khủng hoảng sau đăng: mẫu trả lời phân tầng theo 5 loại bình luận kèm quy tắc xử lý theo mức, khai thác đề tài từ bình luận; có sự cố thì phân cấp, dự thảo tuyên bố, thống nhất phát ngôn. |
| `skill-content-repurposing` | Tách một bài gốc (bài viết, kịch bản video, bản ghi livestream) theo tháp trụ cột – phái sinh – vi nội dung rồi viết lại thành nội dung bản địa cho từng nền tảng như Facebook, TikTok, YouTube, Zalo, kèm thứ tự đăng. |
| `skill-cross-platform-publish` | Đăng một chạm lên các nền tảng đã kết nối: thích ứng một nội dung theo số chữ, tỉ lệ, hashtag, loại nội dung của từng nền tảng rồi uỷ quyền cho SKILL đăng tương ứng; publish_dispatch.py kiểm ràng buộc và định tuyến. |
| `skill-douyin-upload` | 将视频/图文内容发布到抖音（creator.douyin.com）。 |
| `skill-kuaishou-upload` | 快手视频发布：把竖版短视频发布到快手创作者中心。 |
| `skill-persona-check` | Kiểm tra nhất quán persona và tone thương hiệu của nội dung so với hồ sơ (Profile) về định vị, ngách, hình thức, khán giả, phong cách, sở thích; chấm điểm, chỉ rõ điểm lệch kèm gợi ý sửa, chỉ cảnh báo không chặn đăng. |
| `skill-publish-checklist` | Kiểm đủ trước khi đăng: rà từng mục tiêu đề, ảnh bìa, hashtag, định dạng, nhãn tuân thủ, link, CTA có đủ chưa, kết luận đăng được hay chưa kèm danh sách mục còn thiếu và cách bổ sung. |
| `skill-publish-notify` | Đẩy thông báo sau khi đăng: thành công hay thất bại đều gửi kết quả (trạng thái, tiêu đề, nền tảng, link) tới Telegram, Slack, webhook bất kỳ hoặc bot nhóm Feishu/DingTalk/WeCom; thuần script, không phụ thuộc ngoài. |
| `skill-publish-scheduler` | Hẹn giờ đăng hàng loạt theo bảng "nội dung × nền tảng × giờ đăng": nhập lịch, xem hàng đợi, tính mục đến hạn, đến giờ giao cho SKILL đăng của từng nền tảng rồi ghi lại trạng thái; lập lịch thuần script, không tự đăng. |
| `skill-quality-gate` | Cổng chất lượng trước khi đăng, một lần kiểm hai cửa: soát rủi ro tuân thủ (từ nhạy cảm, từ tuyệt đối, quy tắc nền tảng) và thẩm định chất lượng sản phẩm (đầy đủ, dễ đọc, hợp nền tảng), chốt đăng được/cần sửa/không đạt. |
| `skill-risk-scanner` | Đánh giá độ nguyên bản và rủi ro bản quyền bằng LLM: dấu hiệu xào bài/đăng lại, bản quyền ảnh và nhạc, chuẩn trích dẫn, thương hiệu; xuất báo cáo rủi ro thấp/trung bình/cao kèm gợi ý sửa, không check trùng kỹ thuật. |
| `skill-seo-quality` | Kiểm và tối ưu để bài hiện trong kết quả tìm kiếm của nền tảng: từ khoá ở tiêu đề, thân bài, hashtag, chữ trên ảnh bìa/khung đầu, cân đối tìm kiếm và đề xuất; xuất báo cáo kèm Top 3 việc sửa, có chế độ SEO web/blog. |
| `skill-short-link` | Gắn tham số UTM (nguồn/kênh/chiến dịch) vào link nội dung hoặc quảng cáo rồi rút gọn qua dịch vụ công khai không cần key, mỗi kênh một link riêng để theo dõi nguồn truy cập và hiệu quả campaign trên từng nền tảng. |
| `skill-wechat-publisher` | 微信公众号文章自动创作与发布工具。给定参考文章、文字或文档，自动搜索整理全网相关信息、生成图文并茂的公众号文章，并发布到微信公众号草稿箱。特别强调反 AI 检测写作。 |
| `skill-xhs-comment-reply` | 小红书评论互动运营：列出我的笔记、抓取某条笔记下的评论、按画像语气逐条回复、以及删除评论 （含自己发的回复）。 |
| `skill-xhs-publisher` | 将图文/视频内容发布到小红书（XHS）。 |
| `skill-zhihu-answer` | 知乎问答回答发布：在知乎问题下发布原创回答——搜热门问题、检查可答性、写内容、 Playwright 发布（绕 header 遮挡 + JS 遍历发布按钮）。 |
| `skill-zhihu-publisher` | 知乎发布：把文章发布到知乎专栏（也可用于回答草稿）。 |

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
| `skill-xhs-analyzer` | 小红书内容分析：搜索笔记、拉取互动数据、分析爆款规律、创作者画像、限流检测，支持 CLI 自动化操作。 |
