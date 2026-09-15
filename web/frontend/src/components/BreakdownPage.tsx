import { useState } from 'react';
import { runAgent, createIdea } from '../lib/api';
import { renderMarkdown } from '../lib/sanitize';
import { IconFire, IconIdea, IconSkills } from './icons';

interface BreakdownPageProps {
  persona: string;
}

export default function BreakdownPage({ persona }: BreakdownPageProps) {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState('');

  const run = async () => {
    if (!input.trim()) return;
    setLoading(true); setResult('');
    const prompt =
      `Bạn là chuyên gia mổ xẻ nội dung viral. Phân tích nội dung dưới đây, trả lời bằng tiếng Việt theo từng ý:\n` +
      `1. **Tóm tắt một câu**\n` +
      `2. **Mổ xẻ móc câu**: vì sao phần mở đầu thu hút\n` +
      `3. **Công thức cấu trúc**: phân đoạn/nhịp/sắp xếp thông tin\n` +
      `4. **Vì sao viral**: cảm xúc/đồng cảm/hữu ích/điểm tranh cãi\n` +
      `5. **Mẫu có thể sao chép**: trừu tượng hoá công thức thành khung cấu trúc tôi áp dụng được ngay\n` +
      `6. **3 ý tưởng có thể làm theo công thức này${persona ? `, kết hợp hồ sơ «${persona}» của tôi` : ''}**\n\n` +
      `Nội dung cần mổ xẻ:\n${input}`;
    try {
      const res = await runAgent(prompt, persona);
      setResult(res.response);
    } catch (e) {
      setResult(e instanceof Error ? e.message : 'Mổ xẻ thất bại, vui lòng thử lại');
    } finally { setLoading(false); }
  };

  const saveToIdeas = async () => {
    if (!result) return;
    const firstLine = input.trim().split('\n')[0].slice(0, 24);
    await createIdea({ title: `Mẫu mổ xẻ: ${firstLine}`, note: result, source: 'Mổ xẻ bài viral', status: 'pending' });
    setToast('Đã lưu vào kho ý tưởng');
    setTimeout(() => setToast(''), 2200);
  };

  return (
    <div className="page-scroll breakdown-page">
      <div className="page-head">
        <div>
          <h1 className="page-title"><IconFire size={21} /> Mổ xẻ bài viral</h1>
          <p className="page-subtitle">Dán một nội dung tham chiếu/viral, AI bóc tách móc câu, cấu trúc, lý do viral và đưa cho bạn mẫu cùng ý tưởng có thể sao chép.</p>
        </div>
      </div>

      <div className="breakdown-body">
        <textarea className="field" style={{ minHeight: 160 }} value={input}
          placeholder="Dán caption viral của tài khoản tham chiếu / nội dung bạn đã lưu vào đây…"
          onChange={(e) => setInput(e.target.value)} />
        <div style={{ marginTop: 12, display: 'flex', gap: 8 }}>
          <button className="btn btn-primary" disabled={loading || !input.trim()} onClick={run}>
            <IconSkills size={15} /> {loading ? 'Đang mổ xẻ…' : 'Bắt đầu mổ xẻ'}
          </button>
          {result && <button className="btn" onClick={saveToIdeas}><IconIdea size={14} /> Lưu vào kho ý tưởng</button>}
          {result && <button className="btn btn-ghost" onClick={() => { setResult(''); setInput(''); }}>Xoá trắng</button>}
        </div>

        {loading && <div className="loading" style={{ padding: 40 }}><div className="spinner" />AI Đang mổ xẻ…</div>}
        {result && !loading && (
          <div className="panel" style={{ marginTop: 18 }}>
            <div className="panel-title"><IconFire size={14} /> Kết quả mổ xẻ</div>
            <div className="skill-body-md" dangerouslySetInnerHTML={{ __html: renderMarkdown(result) }} />
          </div>
        )}
      </div>

      {toast && <div className="toast ok"><span className="toast-icon">✓</span>{toast}</div>}
    </div>
  );
}
