import { useState, useRef, useEffect } from 'react';
import {
  createSchedule, executeSkill, runAgent, streamChat,
  fetchAccounts, publishNow, publishStatus, submitPublishSms, fetchOutputs, mediaUrl,
} from '../lib/api';
import type { AccountItem, OutputFile } from '../lib/api';
import { loadPublishDraft, savePublishDraft } from '../lib/store';
import { renderMarkdown } from '../lib/sanitize';
import { IconPublish, IconCopy, IconCheck, IconCalendar, IconSkills, IconEdit, IconStop, IconTrash } from './icons';

interface PublishPageProps {
  persona: string;
}

// 平台列表须与后端 LOGIN_RUNNERS 对齐（有登录/发布链路的才列）——微博/公众号无 publisher，不列
const PLATFORMS: { key: string; label: string; titleLimit?: number; bodyLimit: number; hint: string }[] = [
  { key: 'xiaohongshu', label: 'Xiaohongshu', titleLimit: 20, bodyLimit: 1000, hint: 'Tiêu đề ≤20, nội dung ≤1000, thiên về cảm xúc + hashtag' },
  { key: 'douyin', label: 'Douyin', titleLimit: 55, bodyLimit: 55, hint: 'Caption ≤55, vài chữ đầu là móc câu' },
  { key: 'kuaishou', label: 'Kuaishou', titleLimit: 30, bodyLimit: 1000, hint: 'Video hoặc ảnh (bài ảnh), tiêu đề ≤30, cần kèm media' },
  { key: 'weixin-channels', label: 'WeChat Channels', bodyLimit: 1000, hint: 'Cần kèm video, mô tả ngắn + hashtag, đăng nhập bằng quét mã WeChat' },
  { key: 'zhihu', label: 'Zhihu', bodyLimit: 5000, hint: 'Bài dài/câu trả lời, trình bày rõ logic' },
  { key: 'bilibili', label: 'Bilibili', titleLimit: 80, bodyLimit: 2000, hint: 'Cần kèm video, tiêu đề ≤80, mô tả ≤2000, mặc định đăng vào mục «Kiến thức»' },
];
const LABEL2KEY = Object.fromEntries(PLATFORMS.map((p) => [p.label, p.key]));

// 能一键发布的平台（有后端 publisher）
const PUBLISHABLE = new Set(['xiaohongshu', 'douyin', 'kuaishou', 'weixin-channels', 'zhihu', 'bilibili']);
// 必须附带媒体的平台（无媒体发不了）
const MEDIA_REQUIRED = new Set(['xiaohongshu', 'douyin', 'kuaishou', 'weixin-channels', 'bilibili']);
// 只能发视频的平台（抖音/视频号/B站：图文不走此链路，必须视频）
const VIDEO_ONLY = new Set(['douyin', 'weixin-channels', 'bilibili']);
const VIDEO_RE = /\.(mp4|mov|webm|mkv|avi|m4v|flv|ts)$/i;

function parseSections(text: string): Record<string, string> {
  const parts = text.split(/^\s*={2,}\s*(.+?)\s*={2,}\s*$/m);
  const map: Record<string, string> = {};
  for (let i = 1; i < parts.length; i += 2) map[parts[i].trim()] = (parts[i + 1] || '').trim();
  return map;
}

type PubState = { status: 'publishing' | 'ok' | 'fail'; msg: string };

export default function PublishPage({ persona }: PublishPageProps) {
  const draft0 = loadPublishDraft();
  const [title, setTitle] = useState(draft0.title);
  const [body, setBody] = useState(draft0.body);
  const [platforms, setPlatforms] = useState<string[]>(draft0.platforms);
  const [overrides, setOverrides] = useState<Record<string, string>>(draft0.overrides);
  const [tags, setTags] = useState(draft0.tags || '');
  const [editing, setEditing] = useState<string | null>(null);
  const [copied, setCopied] = useState('');
  const [toast, setToast] = useState('');
  const [adapting, setAdapting] = useState(false);
  const [checking, setChecking] = useState(false);
  const [checkResult, setCheckResult] = useState('');
  const adaptCtl = useRef<AbortController | null>(null);

  // 发布相关
  const [accounts, setAccounts] = useState<AccountItem[]>([]);
  const [mediaFiles, setMediaFiles] = useState<OutputFile[]>([]);
  const [selectedMedia, setSelectedMedia] = useState<string[]>([]);
  const [showPicker, setShowPicker] = useState(false);
  const [pub, setPub] = useState<Record<string, PubState>>({});
  const [publishing, setPublishing] = useState(false);
  // 发布时的短信验证窗口（抖音风控条件触发；没触发就不弹）
  const [pubSms, setPubSms] = useState<{ platform: string; name: string; state: string; message: string } | null>(null);
  const [pubSmsCode, setPubSmsCode] = useState('');
  const [pubSmsBusy, setPubSmsBusy] = useState(false);

  // 草稿持久化：任何改动即写 localStorage，切页/刷新回来都在
  useEffect(() => {
    savePublishDraft({ title, body, platforms, overrides, tags });
  }, [title, body, platforms, overrides, tags]);

  useEffect(() => () => adaptCtl.current?.abort(), []);   // 离开页面中止流

  // 登录态 + 可选媒体列表
  useEffect(() => {
    fetchAccounts().then(setAccounts).catch(() => { /* 忽略 */ });
    fetchOutputs().then((roots) => {
      const files: OutputFile[] = [];
      const walk = (n: OutputFile) => {
        if (n.type === 'file') { if (n.kind === 'image' || n.kind === 'video') files.push(n); return; }
        for (const c of n.children || []) walk(c);
      };
      roots.forEach(walk);
      files.sort((a, b) => (b.mtime || 0) - (a.mtime || 0));
      setMediaFiles(files);
    }).catch(() => { /* 忽略 */ });
  }, []);

  const loginOf = (key: string) => accounts.find((a) => a.platform === key)?.loggedIn ?? false;

  const toggle = (k: string) =>
    setPlatforms((prev) => prev.includes(k) ? prev.filter((x) => x !== k) : [...prev, k]);
  const showToast = (m: string) => { setToast(m); setTimeout(() => setToast(''), 2800); };
  const effective = (k: string) => overrides[k] ?? body;
  const empty = !title.trim() && !body.trim();
  const isVideoPath = (p: string) => /\.(mp4|mov|flv|mkv|avi|webm|m4v|wmv|ts|mpe?g)$/i.test(p);
  const toggleMedia = (path: string) =>
    setSelectedMedia((prev) => {
      if (prev.includes(path)) return prev.filter((x) => x !== path);
      // 通用规则：图片和视频不能同时；视频一次只发一个
      if (isVideoPath(path)) {
        if (prev.length && !prev.every(isVideoPath)) { showToast('Không thể đăng đồng thời ảnh và video, hãy bỏ chọn ảnh trước'); return prev; }
        return [path]; // 视频单选
      }
      if (prev.some(isVideoPath)) { showToast('Không thể đăng đồng thời ảnh và video, hãy bỏ chọn video trước'); return prev; }
      return [...prev, path]; // 图片可多选（图文）
    });

  // A. 智能一稿多改（流式：逐字改写，直接流进每个平台卡片）
  const adapt = () => {
    if (empty || platforms.length === 0 || adapting) return;
    const sel = PLATFORMS.filter((p) => platforms.includes(p.key));
    const prompt =
      `Hãy chạy /skill-content-repurposing: chuyển thể nội dung dưới đây cho các nền tảng: ${sel.map((p) => p.label).join(', ')}.` +
      `Bắt buộc tham khảo platform-specs và công thức chuyển thể của SKILL đó, bám sát định dạng, giọng điệu và số chữ gốc của từng nền tảng.\n` +
      `[YÊU CẦU BẮT BUỘC] Với mỗi nền tảng chỉ xuất "nội dung thuần văn bản có thể sao chép đăng ngay", cấm mọi cú pháp Markdown: không **in đậm**, # tiêu đề, ---, bảng, khối mã, ký hiệu danh sách đánh số;` +
      `có thể dùng emoji và #hashtag, xuống dòng tự nhiên theo thói quen từng nền tảng.\n` +
      `Chỉ xuất đúng theo định dạng dưới đây, giữa các nền tảng dùng dòng phân cách, không thêm bất kỳ giải thích nào:\n` +
      sel.map((p) => `===${p.label}===\n<nội dung thuần văn bản cho nền tảng này>`).join('\n') +
      `\n\nNội dung gốc:\nTiêu đề: ${title}\nNội dung: ${body}`;

    setAdapting(true);
    let acc = '';
    const base = { ...overrides };
    adaptCtl.current = streamChat(
      prompt, persona, `adapt-${Date.now()}`,
      (chunk) => {                       // 逐字：实时解析并流进对应平台卡片
        acc += chunk;
        const map = parseSections(acc);
        const next = { ...base };
        for (const [label, text] of Object.entries(map)) {
          const key = LABEL2KEY[label];
          if (key && platforms.includes(key)) next[key] = text;
        }
        setOverrides(next);
      },
      () => {                            // 完成
        const hit = Object.keys(parseSections(acc)).length;
        setAdapting(false);
        showToast(hit ? `Đã tạo ${hit} phiên bản nền tảng` : 'Không phân tích được, có thể thử lại');
      },
      () => { setAdapting(false); showToast('Chuyển thể thất bại, vui lòng thử lại'); },
    );
  };
  const stopAdapt = () => { adaptCtl.current?.abort(); setAdapting(false); };

  const performPrecheck = async () => {
    const prompt =
      `Bạn là trợ lý kiểm duyệt trước khi đăng mạng xã hội. Với nội dung sắp đăng dưới đây, thực hiện hai kiểm tra, trả lời bằng tiếng Việt ngắn gọn theo từng ý:\n` +
      `1. **Rủi ro tuân thủ**: có chứa từ tuyệt đối/công dụng y tế/biểu đạt nhạy cảm hoặc vi phạm không, liệt kê từ có vấn đề + gợi ý thay thế; nếu không có thì ghi "Không thấy rủi ro rõ ràng".\n` +
      `2. **Tiêu đề/móc câu**: chấm tiêu đề thang 1-10 và đưa 1-2 phương án tốt hơn.\n` +
      `Dòng cuối kết luận «✅ Có thể đăng / ⚠️ Nên sửa».\n\nNội dung cần kiểm tra:\nTiêu đề: ${title}\nNội dung: ${body}`;
    const content = `Nội dung sắp đăng:\nTiêu đề: ${title}\nNội dung: ${body}`;
    const [general, personaResult] = await Promise.all([
      runAgent(prompt),
      persona ? executeSkill('persona-check', content, persona) : Promise.resolve(null),
    ]);
    return `${general.response}\n\n---\n\n## Nhất quán persona\n\n${personaResult?.response || 'Chưa chọn hồ sơ, đã bỏ qua kiểm tra nhất quán persona.'}`;
  };

  // C. 发布前一键预检
  const check = async () => {
    if (empty) return;
    setChecking(true); setCheckResult('');
    try {
      setCheckResult(await performPrecheck());
    } catch (e) {
      setCheckResult(e instanceof Error ? e.message : 'Kiểm tra trước thất bại');
    } finally { setChecking(false); }
  };

  // D. 一键发布（真发布，二次确认）
  const publishAll = async () => {
    if (empty || publishing || checking) return;
    const targets = PLATFORMS.filter((p) => platforms.includes(p.key) && PUBLISHABLE.has(p.key));
    if (targets.length === 0) {
      showToast('Nền tảng đã chọn chưa hỗ trợ đăng một chạm (Bilibili dùng «Sao chép» hoặc biliup trong terminal)');
      return;
    }
    setChecking(true);
    try {
      setCheckResult(await performPrecheck());
    } catch (e) {
      setCheckResult(`Kiểm tra trước thất bại: ${e instanceof Error ? e.message : 'Lỗi không xác định'}\n\nKiểm tra trước chỉ để nhắc, không chặn bạn tiếp tục đăng.`);
    } finally {
      setChecking(false);
    }
    const okToSend = window.confirm(
      `Đã chạy kiểm tra trước khi đăng, kết quả hiển thị trên trang. Điểm persona chỉ để nhắc, không chặn đăng.\n\n` +
      `Sắp [ĐĂNG THẬT] lên: ${targets.map((t) => t.label).join(', ')}.\n` +
      `Nội dung sẽ được đăng công khai lên tài khoản của bạn, tiếp tục?`);
    if (!okToSend) return;

    setPublishing(true);
    for (const t of targets) {
      if (!loginOf(t.key)) {
        setPub((r) => ({ ...r, [t.key]: { status: 'fail', msg: 'Chưa đăng nhập · vào trang Tài khoản để đăng nhập' } }));
        continue;
      }
      if (MEDIA_REQUIRED.has(t.key) && selectedMedia.length === 0) {
        setPub((r) => ({ ...r, [t.key]: { status: 'fail', msg: 'Cần kèm ảnh/video' } }));
        continue;
      }
      if (VIDEO_ONLY.has(t.key) && !selectedMedia.some((p) => VIDEO_RE.test(p))) {
        setPub((r) => ({ ...r, [t.key]: { status: 'fail', msg: `${t.label} chỉ đăng được video, hãy chọn một video từ thư viện nội dung` } }));
        continue;
      }
      setPub((r) => ({ ...r, [t.key]: { status: 'publishing', msg: 'Đang đăng… có thể mất 1-2 phút' } }));
      try {
        const res = await publishNow(t.key, { title, body: effective(t.key), media: selectedMedia, tags });
        if (res.async) {
          // 抖音：异步发布，轮询状态；风控触发短信墙时弹输入框（条件触发，没触发就直接跑完）
          await pollAsyncPublish(t.key, t.label);
        } else {
          setPub((r) => ({
            ...r,
            [t.key]: res.ok
              ? { status: 'ok', msg: 'Đã đăng ✅' }
              : { status: 'fail', msg: res.detail || res.message || 'Đăng bài thất bại' },
          }));
        }
      } catch (e) {
        setPub((r) => ({ ...r, [t.key]: { status: 'fail', msg: e instanceof Error ? e.message : 'Đăng bài thất bại' } }));
      }
    }
    setPublishing(false);
    showToast('Luồng đăng bài đã kết thúc, xem trạng thái trên thẻ từng nền tảng');
  };

  // 异步发布轮询（抖音）：直到 success/error；遇 sms_required/verifying 弹短信窗口
  const pollAsyncPublish = (key: string, label: string) => new Promise<void>((resolve) => {
    const started = Date.now();
    const iv = setInterval(async () => {
      if (Date.now() - started > 15 * 60 * 1000) {   // 15min 兜底
        clearInterval(iv); setPubSms(null);
        setPub((r) => ({ ...r, [key]: { status: 'fail', msg: 'Đăng bài quá thời gian chờ' } }));
        resolve(); return;
      }
      let s;
      try { s = await publishStatus(key); } catch { return; }  // 单次失败忽略
      if (s.state === 'sms_required' || s.state === 'verifying') {
        setPubSms({ platform: key, name: label, state: s.state, message: s.message });
        setPub((r) => ({ ...r, [key]: { status: 'publishing', msg: s.message || 'Cần xác thực SMS' } }));
      } else if (s.state === 'success') {
        clearInterval(iv); setPubSms(null);
        setPub((r) => ({ ...r, [key]: { status: 'ok', msg: 'Đã đăng ✅' } }));
        resolve();
      } else if (s.state === 'error') {
        clearInterval(iv); setPubSms(null);
        setPub((r) => ({ ...r, [key]: { status: 'fail', msg: s.message || 'Đăng bài thất bại' } }));
        resolve();
      } else {
        setPub((r) => ({ ...r, [key]: { status: 'publishing', msg: s.message || 'Đang đăng…' } }));
      }
    }, 2500);
  });

  const submitPubSms = async () => {
    if (!pubSms) return;
    const code = pubSmsCode.replace(/\D/g, '');
    if (code.length < 4) { showToast('Mã xác thực phải gồm 4-6 chữ số'); return; }
    setPubSmsBusy(true);
    try {
      await submitPublishSms(pubSms.platform, code);
      setPubSmsCode('');
      setPubSms((p) => p && ({ ...p, state: 'verifying', message: 'Đang xác thực mã…' }));
    } catch (e) {
      showToast(e instanceof Error ? e.message : 'Gửi thất bại');
    } finally {
      setPubSmsBusy(false);
    }
  };

  const copyFor = (key: string) => {
    const text = (title ? title + '\n\n' : '') + effective(key);
    navigator.clipboard?.writeText(text);
    setCopied(key); setTimeout(() => setCopied(''), 1400);
  };
  const addToCalendar = async (key: string) => {
    if (empty) return;
    const d = new Date();
    await createSchedule({
      title: title.trim() || effective(key).slice(0, 20), date: d.toISOString().slice(0, 10),
      platform: PLATFORMS.find((p) => p.key === key)?.label || '', time: '', status: 'draft', note: effective(key),
    });
    showToast('Đã lưu nháp và thêm vào lịch hôm nay');
  };

  const canPublish = platforms.some((k) => PUBLISHABLE.has(k));

  return (
    <div className="publish-page">
      <div className="publish-editor">
        <h1 className="page-title"><IconPublish size={21} /> Trung tâm đăng bài</h1>
        <p className="page-subtitle">Soạn một lần → AI chuyển thể cho từng nền tảng → kiểm tra trước → kèm media → đăng thật một chạm.</p>

        <label className="field-label">Tiêu đề</label>
        <input className="field" value={title} placeholder="Tiêu đề (một số nền tảng cần)"
          onChange={(e) => setTitle(e.target.value)} />
        <label className="field-label">Nội dung (bản gốc)</label>
        <textarea className="field" style={{ minHeight: 180 }} value={body}
          placeholder="Viết nội dung của bạn, bên phải xem trước theo quy tắc từng nền tảng; bấm «Chuyển thể một chạm» để AI viết lại cho từng nền tảng…"
          onChange={(e) => setBody(e.target.value)} />

        <label className="field-label">Hashtag <span style={{ color: 'var(--text-secondary)', fontWeight: 400, fontSize: 12 }}>(phân cách bằng dấu phẩy, ví dụ «AI,công sở,mẹo hay»)</span></label>
        <input className="field" value={tags} placeholder="AI,công sở,mẹo hay"
          onChange={(e) => setTags(e.target.value)} />

        <label className="field-label">Nền tảng đăng</label>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
          {PLATFORMS.map((p) => (
            <button key={p.key} className={`chip ${platforms.includes(p.key) ? 'active' : ''}`}
              onClick={() => toggle(p.key)}>{p.label}</button>
          ))}
        </div>

        <label className="field-label" style={{ marginTop: 14 }}>
          Media đính kèm {selectedMedia.length > 0 && <span className="pv-badge">{selectedMedia.length} tệp</span>}
          <span style={{ color: 'var(--text-secondary)', fontWeight: 400, fontSize: 12 }}>(Xiaohongshu/Douyin/Kuaishou/WeChat Channels/Bilibili bắt buộc, chọn từ thư viện nội dung; Douyin, WeChat Channels, Bilibili phải là video)</span>
        </label>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
          <button className="btn btn-sm" onClick={() => setShowPicker((v) => !v)}>
            <IconSkills size={13} /> {showPicker ? 'Thu gọn' : 'Chọn media'}
          </button>
          {selectedMedia.map((path) => (
            <div key={path} className="media-chip" onClick={() => toggleMedia(path)} title="Bấm để gỡ">
              {mediaFiles.find((f) => f.path === path)?.kind === 'image'
                ? <img src={mediaUrl(path)} alt="" /> : <span className="media-vid">🎬</span>}
              <span className="media-x">×</span>
            </div>
          ))}
        </div>
        {showPicker && (
          <div className="media-grid">
            {mediaFiles.length === 0 && <div className="dash-empty">Thư viện nội dung chưa có ảnh/video</div>}
            {mediaFiles.slice(0, 40).map((f) => (
              <div key={f.path}
                className={`media-cell ${selectedMedia.includes(f.path) ? 'sel' : ''}`}
                onClick={() => toggleMedia(f.path)} title={f.path}>
                {f.kind === 'image'
                  ? <img src={mediaUrl(f.path)} alt={f.name} loading="lazy" />
                  : <span className="media-vid">🎬<br />{f.name.slice(0, 12)}</span>}
                {selectedMedia.includes(f.path) && <span className="media-check">✓</span>}
              </div>
            ))}
          </div>
        )}

        <div className="publish-actions">
          {adapting ? (
            <button className="btn btn-sm" onClick={stopAdapt}><IconStop size={13} /> Dừng tạo</button>
          ) : (
            <button className="btn btn-sm btn-primary" disabled={empty || platforms.length === 0} onClick={adapt}>
              <IconSkills size={14} /> Chuyển thể một chạm
            </button>
          )}
          <button className="btn btn-sm" disabled={empty || checking || adapting} onClick={check}>
            <IconCheck size={14} /> {checking ? 'Đang kiểm tra…' : 'Kiểm tra trước khi đăng'}
          </button>
          <button className="btn btn-sm" disabled={empty} onClick={() => addToCalendar(platforms[0] || 'xiaohongshu')}>
            <IconCalendar size={14} /> Lưu nháp và lên lịch
          </button>
          <button className="btn btn-sm btn-primary" disabled={empty || publishing || checking || !canPublish}
            title={canPublish ? 'Đăng thật lên các nền tảng đã đăng nhập' : 'Nền tảng đã chọn không có đăng một chạm (Bilibili dùng biliup trong terminal)'}
            onClick={publishAll}>
            <IconPublish size={14} /> {publishing ? 'Đang đăng…' : 'Đăng một chạm'}
          </button>
          <button className="btn btn-sm btn-ghost" disabled={empty || adapting}
            onClick={() => { setTitle(''); setBody(''); setTags(''); setOverrides({}); setCheckResult(''); setPub({}); showToast('Đã xoá trắng'); }}>
            <IconTrash size={13} /> Xoá trắng
          </button>
        </div>
        {adapting && <div className="adapt-hint"><span className="live-pulse" />AI Đang viết lại từng chữ cho các nền tảng… có thể dừng bất cứ lúc nào.</div>}
        <p className="publish-saved-note">Bản nháp tự động lưu, chuyển trang/tải lại vẫn còn. Đăng một chạm chỉ áp dụng cho nền tảng «đã đăng nhập + đủ media».</p>
        {checkResult && (
          <div className="panel" style={{ marginTop: 14 }}>
            <div className="panel-title"><IconCheck size={14} /> Kiểm tra trước khi đăng</div>
            <div className="skill-body-md" dangerouslySetInnerHTML={{ __html: renderMarkdown(checkResult) }} />
          </div>
        )}
      </div>

      <div className="publish-previews">
        {platforms.length === 0 && <div className="dash-empty">Chọn ít nhất một nền tảng để xem trước</div>}
        {PLATFORMS.filter((p) => platforms.includes(p.key)).map((p) => {
          const text = effective(p.key);
          const over = text.length > p.bodyLimit;
          const titleOver = p.titleLimit != null && title.length > p.titleLimit;
          const isEdit = editing === p.key;
          const ps = pub[p.key];
          const publishable = PUBLISHABLE.has(p.key);
          const logged = loginOf(p.key);
          return (
            <div key={p.key} className={`card pv-card pv-${p.key}`}>
              <div className="pv-head">
                <span className="pv-plat">
                  {p.label}
                  {overrides[p.key] != null && <span className="pv-badge">Bản AI</span>}
                  {publishable && (logged
                    ? <span className="pv-badge pv-badge-ok">Đã đăng nhập</span>
                    : <span className="pv-badge">Chưa đăng nhập</span>)}
                </span>
                <span className={`pv-count ${over ? 'over' : ''}`}>{text.length}/{p.bodyLimit}</span>
              </div>
              <div className="pv-body">
                {p.titleLimit != null && (
                  <div className={`pv-title ${titleOver ? 'over' : ''}`}>{title || <span className="pv-ph">Tiêu đề…</span>}</div>
                )}
                {isEdit
                  ? <textarea className="field" style={{ minHeight: 120 }} value={text} autoFocus
                      onChange={(e) => setOverrides((o) => ({ ...o, [p.key]: e.target.value }))} />
                  : <div className="pv-text">{text || <span className="pv-ph">Xem trước nội dung…</span>}{adapting && overrides[p.key] != null && <span className="streaming-cursor" />}</div>}
              </div>
              {ps && (
                <div className={`pv-pubstate ${ps.status}`}>
                  {ps.status === 'publishing' && <span className="live-pulse" />}
                  {ps.status === 'ok' ? '✅ ' : ps.status === 'fail' ? '⚠️ ' : ''}{ps.msg}
                </div>
              )}
              <div className="pv-foot">
                <span className="pv-hint">{p.hint}{over ? ' · vượt số chữ' : ''}</span>
                <div style={{ display: 'flex', gap: 6 }}>
                  <button className="pv-copy" onClick={() => setEditing(isEdit ? null : p.key)}>
                    <IconEdit size={13} />{isEdit ? 'Xong' : 'Sửa'}
                  </button>
                  <button className="pv-copy" onClick={() => copyFor(p.key)}>
                    {copied === p.key ? <IconCheck size={13} /> : <IconCopy size={13} />}{copied === p.key ? 'Đã sao chép' : 'Sao chép'}
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {toast && <div className="toast ok"><span className="toast-icon">✓</span>{toast}</div>}

      {pubSms && (
        <div className="overlay" onClick={(e) => { if (e.target === e.currentTarget) setPubSms(null); }}>
          <div className="modal" onClick={(e) => e.stopPropagation()} style={{ maxWidth: 380 }}>
            <h3 style={{ margin: '0 0 4px' }}>Xác thực đăng bài · {pubSms.name}</h3>
            <p style={{ fontSize: 13, color: /错误|过期|失败|重新|未完成|不正确|失效/.test(pubSms.message || '') ? 'var(--red)' : 'var(--text-secondary)' }}>
              {pubSms.message || 'Nền tảng yêu cầu xác thực SMS, mã đã gửi tới điện thoại của bạn, vui lòng nhập:'}
            </p>
            {pubSms.state === 'verifying' ? (
              <div className="dash-empty" style={{ padding: 16 }}>Đang xác thực mã…</div>
            ) : (
              <>
                <input inputMode="numeric" autoFocus
                  placeholder="Nhập mã xác thực nhận được trên điện thoại" value={pubSmsCode}
                  onChange={(e) => setPubSmsCode(e.target.value.replace(/\D/g, '').slice(0, 8))}
                  onKeyDown={(e) => { if (e.key === 'Enter') submitPubSms(); }}
                  style={{ width: '100%', boxSizing: 'border-box', textAlign: 'center',
                    letterSpacing: 6, fontSize: 20, padding: '10px 12px', margin: '4px 0 10px',
                    border: '1px solid var(--border)', borderRadius: 8 }} />
                <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
                  <button className="btn btn-sm btn-ghost" onClick={() => setPubSms(null)}>Đóng</button>
                  <button className="btn btn-sm btn-primary" disabled={pubSmsBusy} onClick={submitPubSms}>
                    {pubSmsBusy ? 'Đang gửi…' : 'Gửi mã xác thực'}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
