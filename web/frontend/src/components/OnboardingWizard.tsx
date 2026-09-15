import { useState, useEffect } from 'react';
import { buildProfile, profileBuildStatus } from '../lib/api';

const PLATFORMS = ['小红书', '抖音', 'B站', '视频号', '公众号', '微博', '知乎'];
const TONES = ['Chuyên nghiệp nghiêm túc', 'Nhẹ nhàng hài hước', 'Gần gũi đời thường', 'Sắc sảo châm biếm', 'Ấm áp chữa lành', 'Thực dụng hữu ích'];

interface OnboardingWizardProps {
  onClose: () => void;
  onCreated: (name: string) => void;
}

interface FormState {
  name: string;
  platforms: string[];
  accountStage: string;
  links: Record<string, string>;
  direction: string;
  reason: string;
  goal: string;
  formats: string;
  likes: string;
  tone: string;
  avoid: string;
}

const EMPTY: FormState = {
  name: '', platforms: [], accountStage: 'Tài khoản mới', links: {},
  direction: '', reason: '', goal: '', formats: '', likes: '', tone: '', avoid: '',
};

const STEPS = ['Thông tin cơ bản', 'Liên kết MXH', 'Mục tiêu vận hành', 'Ưu tiên và lằn ranh đỏ'];

export default function OnboardingWizard({ onClose, onCreated }: OnboardingWizardProps) {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<FormState>(EMPTY);
  const [submitting, setSubmitting] = useState(false);
  const [phase, setPhase] = useState<'form' | 'enhancing'>('form');
  const [error, setError] = useState('');

  const set = <K extends keyof FormState>(k: K, v: FormState[K]) =>
    setForm((f) => ({ ...f, [k]: v }));

  const togglePlatform = (p: string) =>
    setForm((f) => ({
      ...f,
      platforms: f.platforms.includes(p)
        ? f.platforms.filter((x) => x !== p)
        : [...f.platforms, p],
    }));

  const canNext =
    (step === 0 && form.name.trim() !== '') ||
    (step === 2 && form.direction.trim() !== '') ||
    step === 1 || step === 3;

  const submit = async () => {
    setSubmitting(true);
    setError('');
    try {
      // 后端异步：立即返回（基线已写、画像可用），不再长阻塞被代理超时掐断
      const res = await buildProfile(form.name.trim(), form as unknown as Record<string, unknown>);
      if (res.created) {
        setSubmitting(false);
        setPhase('enhancing'); // 进入后台增强等待（可跳过）
      } else {
        setError('Tạo hồ sơ thất bại, vui lòng thử lại');
        setSubmitting(false);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Tạo thất bại');
      setSubmitting(false);
    }
  };

  // 增强阶段：轮询后台 AI 增强进度；完成/失败即进入画像（基线已可用）
  useEffect(() => {
    if (phase !== 'enhancing') return;
    let alive = true;
    const name = form.name.trim();
    const tick = async () => {
      try {
        const st = await profileBuildStatus(name);
        if (!alive) return;
        if (st.state === 'done' || st.state === 'failed' || st.state === 'unknown') {
          onCreated(name);
          return;
        }
      } catch {
        /* 轮询失败忽略，继续 */
      }
      if (alive) setTimeout(tick, 5000);
    };
    const t = setTimeout(tick, 4000);
    return () => { alive = false; clearTimeout(t); };
  }, [phase]); // eslint-disable-line react-hooks/exhaustive-deps

  const box: React.CSSProperties = {
    width: '100%', padding: '10px 12px', marginTop: 6, borderRadius: 'var(--radius)',
    border: '1px solid var(--border)', background: 'var(--bg-elev)', color: 'var(--text)',
    fontSize: 14, fontFamily: 'inherit',
  };
  const label: React.CSSProperties = { display: 'block', marginTop: 16, fontSize: 13, color: 'var(--text-secondary)' };

  const chip = (active: boolean): React.CSSProperties => ({
    padding: '6px 13px', borderRadius: 999, fontSize: 13, cursor: 'pointer',
    border: '1px solid var(--border)',
    background: active ? 'var(--accent-gradient)' : 'var(--bg-elev)',
    color: active ? '#fff' : 'var(--text)',
  });

  return (
    <div className="overlay">
      <div className="modal" style={{ width: 560, maxWidth: '100%', maxHeight: '90vh', overflowY: 'auto' }}>
        {/* 头部 + 进度 */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0, fontSize: 20 }}>Thiết lập hồ sơ tài khoản</h2>
          <button onClick={onClose} disabled={submitting}
            style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', fontSize: 22, cursor: 'pointer' }}>×</button>
        </div>
        <div style={{ display: 'flex', gap: 6, margin: '16px 0 4px' }}>
          {STEPS.map((s, i) => (
            <div key={s} style={{ flex: 1 }}>
              <div style={{ height: 4, borderRadius: 2, background: i <= step ? 'var(--accent-start)' : 'var(--border)' }} />
              <div style={{ fontSize: 11, color: i === step ? 'var(--text)' : 'var(--text-secondary)', marginTop: 4 }}>{s}</div>
            </div>
          ))}
        </div>

        {submitting ? (
          <div style={{ padding: '48px 0', textAlign: 'center', color: 'var(--text-secondary)' }}>
            <div className="spinner" style={{ margin: '0 auto 16px' }} />
            Đang tạo hồ sơ cơ bản…
          </div>
        ) : phase === 'enhancing' ? (
          <div style={{ padding: '40px 0', textAlign: 'center', color: 'var(--text-secondary)' }}>
            <div className="spinner" style={{ margin: '0 auto 16px' }} />
            <div style={{ color: 'var(--text)', fontSize: 15, marginBottom: 6 }}>Đã tạo hồ sơ ✓  AI đang bổ sung ở nền…</div>
            <span style={{ fontSize: 12 }}>
              Đang thử thu thập liên kết MXH và hoàn thiện từng khía cạnh, có thể mất 1-2 phút.<br />
              Bạn có thể dùng ngay, việc bổ sung sẽ tiếp tục ở nền.
            </span>
            <div style={{ marginTop: 20 }}>
              <button className="btn btn-primary" onClick={() => onCreated(form.name.trim())}>Dùng ngay</button>
            </div>
          </div>
        ) : (
          <div style={{ minHeight: 240 }}>
            {step === 0 && (
              <>
                <label style={label}>Tên hồ sơ * (một persona = một hồ sơ, dùng được trên nhiều nền tảng)</label>
                <input style={box} value={form.name} placeholder="VD: reviewer công nghệ"
                  onChange={(e) => set('name', e.target.value)} />
                <label style={label}>Nền tảng vận hành (chọn nhiều)</label>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 6 }}>
                  {PLATFORMS.map((p) => (
                    <button key={p} onClick={() => togglePlatform(p)} style={chip(form.platforms.includes(p))}>{p}</button>
                  ))}
                </div>
                <label style={label}>Giai đoạn tài khoản</label>
                <div style={{ display: 'flex', gap: 8, marginTop: 6 }}>
                  {['Tài khoản mới', 'Đã có tài khoản'].map((s) => (
                    <button key={s} onClick={() => set('accountStage', s)} style={chip(form.accountStage === s)}>{s}</button>
                  ))}
                </div>
              </>
            )}

            {step === 1 && (
              <>
                <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 12 }}>
                  Dán liên kết trang chủ từng nền tảng, AI sẽ cố gắng phân tích nội dung và phong cách bạn đã đăng (không lấy được sẽ bỏ qua, có thể để trống).
                </p>
                {form.platforms.length === 0 && (
                  <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>(Chưa chọn nền tảng, có thể sang bước tiếp)</p>
                )}
                {form.platforms.map((p) => (
                  <div key={p}>
                    <label style={label}>{p} liên kết trang chủ</label>
                    <input style={box} value={form.links[p] || ''} placeholder={`https://…`}
                      onChange={(e) => set('links', { ...form.links, [p]: e.target.value })} />
                  </div>
                ))}
              </>
            )}

            {step === 2 && (
              <>
                <label style={label}>Muốn làm nội dung hướng nào * (càng cụ thể càng tốt)</label>
                <input style={box} value={form.direction} placeholder="VD: review skincare bình dân"
                  onChange={(e) => set('direction', e.target.value)} />
                <label style={label}>Vì sao làm hướng này / thế mạnh·trải nghiệm riêng của bạn</label>
                <textarea style={{ ...box, minHeight: 60, resize: 'vertical' }} value={form.reason}
                  onChange={(e) => set('reason', e.target.value)} />
                <label style={label}>Mục tiêu vận hành</label>
                <input style={box} value={form.goal} placeholder="Tăng follow / kiếm tiền / thương hiệu cá nhân / kéo khách về kênh riêng"
                  onChange={(e) => set('goal', e.target.value)} />
                <label style={label}>Dạng nội dung muốn sản xuất</label>
                <input style={box} value={form.formats} placeholder="Bài ảnh / video ngắn / video dài / bài dài"
                  onChange={(e) => set('formats', e.target.value)} />
              </>
            )}

            {step === 3 && (
              <>
                <label style={label}>Nội dung yêu thích / tài khoản tham chiếu</label>
                <textarea style={{ ...box, minHeight: 60, resize: 'vertical' }} value={form.likes}
                  onChange={(e) => set('likes', e.target.value)} />
                <label style={label}>Giọng điệu mong muốn</label>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 6 }}>
                  {TONES.map((t) => (
                    <button key={t} onClick={() => set('tone', form.tone === t ? '' : t)} style={chip(form.tone === t)}>{t}</button>
                  ))}
                </div>
                <label style={label}>Nội dung không làm / lằn ranh tuân thủ</label>
                <textarea style={{ ...box, minHeight: 60, resize: 'vertical' }} value={form.avoid}
                  placeholder="VD: không nhận công dụng y tế, không quảng cáo sai sự thật"
                  onChange={(e) => set('avoid', e.target.value)} />
              </>
            )}

            {error && <div style={{ color: 'var(--red)', fontSize: 13, marginTop: 12 }}>{error}</div>}
          </div>
        )}

        {/* 底部按钮 */}
        {phase === 'form' && !submitting && (
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 20 }}>
            <button className="btn" onClick={() => (step === 0 ? onClose() : setStep(step - 1))}>
              {step === 0 ? 'Huỷ' : 'Quay lại'}
            </button>
            {step < STEPS.length - 1 ? (
              <button className="btn btn-primary" onClick={() => canNext && setStep(step + 1)} disabled={!canNext}>
                Tiếp theo
              </button>
            ) : (
              <button className="btn btn-primary" onClick={submit} disabled={!form.name.trim() || !form.direction.trim()}>
                Tạo hồ sơ
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
