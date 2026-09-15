import { useState, useEffect } from 'react';
import { fetchPersonaFiles, savePersonaFile, deletePersona } from '../lib/api';
import type { PersonaFile } from '../lib/api';
import { renderMarkdown } from '../lib/sanitize';

interface ProfilePageProps {
  persona: string;
  onNewProfile: () => void;
  onDeleted: (name: string) => void;
}

/** Bỏ dòng H1 đầu file khi hiển thị — thẻ đã có nhãn, tránh lặp tiêu đề. Chế độ sửa giữ nguyên văn. */
function stripLeadingH1(md: string): string {
  return md.replace(/^\s*# [^\n]*\n?/, '');
}

const DIM_META: Record<string, { label: string; icon: string }> = {
  'identity.md': { label: 'Định vị tài khoản', icon: '🪪' },
  'style.md': { label: 'Phong cách nội dung', icon: '🎨' },
  'audience.md': { label: 'Đối tượng mục tiêu', icon: '👥' },
  'platforms.md': { label: 'Nền tảng vận hành', icon: '📱' },
  'preferences.md': { label: 'Ưu tiên và lằn ranh đỏ', icon: '⚖️' },
  'memory.md': { label: 'Kinh nghiệm tích luỹ', icon: '🧠' },
};

export default function ProfilePage({ persona, onNewProfile, onDeleted }: ProfilePageProps) {
  const [files, setFiles] = useState<PersonaFile[]>([]);
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [savingFile, setSavingFile] = useState('');
  const [deleting, setDeleting] = useState(false);
  const [toast, setToast] = useState('');

  useEffect(() => {
    if (!persona) { setFiles([]); return; }
    let ignore = false;   // 切 persona 丢弃旧请求（F2）
    setLoading(true);
    setError('');
    setEditing(false);
    fetchPersonaFiles(persona)
      .then((d) => {
        if (ignore) return;
        setFiles(d.files);
        setDrafts(Object.fromEntries(d.files.map((f) => [f.filename, f.content])));
      })
      .catch(() => { if (!ignore) setError('Tải hồ sơ thất bại'); })
      .finally(() => { if (!ignore) setLoading(false); });
    return () => { ignore = true; };
  }, [persona]);

  const showToast = (msg: string) => { setToast(msg); setTimeout(() => setToast(''), 2500); };

  const handleSave = async (filename: string) => {
    setSavingFile(filename);
    try {
      await savePersonaFile(persona, filename, drafts[filename] ?? '');
      setFiles((prev) => prev.map((f) => f.filename === filename ? { ...f, content: drafts[filename] ?? '' } : f));
      showToast(`Đã lưu ${DIM_META[filename]?.label || filename} ✓`);
    } catch (e) {
      showToast(e instanceof Error ? e.message : 'Lưu thất bại');
    } finally {
      setSavingFile('');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`Xoá hồ sơ «${persona}»?\nThao tác này không thể hoàn tác, toàn bộ 6 file của hồ sơ sẽ bị xoá.`)) return;
    setDeleting(true);
    try {
      await deletePersona(persona);
      onDeleted(persona);
      showToast(`Đã xoá hồ sơ «${persona}»`);
    } catch (e) {
      showToast(e instanceof Error ? e.message : 'Xoá thất bại');
    } finally {
      setDeleting(false);
    }
  };

  if (!persona) {
    return (
      <div className="profile-page">
        <h1 className="page-title">Hồ sơ người dùng Profile</h1>
        <div className="empty-state" style={{ height: '70%' }}>
          <div className="empty-icon">👤</div>
          <h3>Chưa chọn hồ sơ</h3>
          <p>Hồ sơ lưu định vị, phong cách, khán giả và lằn ranh đỏ của bạn để nội dung tạo ra sát persona hơn.</p>
          <button className="btn btn-primary" onClick={onNewProfile}>+ Hồ sơ mới</button>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="profile-head">
        <div>
          <h1 className="page-title">{persona}</h1>
          <p className="page-subtitle">Sáu khía cạnh tạo nên một persona hoàn chỉnh, có thể sửa và lưu bất cứ lúc nào.</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className={`btn ${editing ? 'btn-primary' : ''}`} onClick={() => setEditing((v) => !v)}>
            {editing ? 'Xong' : '✏️ Sửa hồ sơ'}
          </button>
          <button className="btn" style={{ color: 'var(--red)', borderColor: 'var(--red)' }}
            disabled={deleting} onClick={handleDelete}>
            {deleting ? 'Đang xoá…' : '🗑 Xoá hồ sơ'}
          </button>
        </div>
      </div>

      {error && <div style={{ color: 'var(--red)', fontSize: 14, marginTop: 12 }}>{error}</div>}

      {loading ? (
        <div className="loading"><div className="spinner" />Đang tải…</div>
      ) : (
        files.map((f) => {
          const meta = DIM_META[f.filename] || { label: f.filename, icon: '📄' };
          const dirty = editing && (drafts[f.filename] ?? '') !== f.content;
          return (
            <div key={f.filename} className="profile-dim">
              <div className="profile-dim-head">
                <div className="profile-dim-title">{meta.icon} {meta.label}</div>
                {editing && (
                  <button className="btn btn-sm btn-primary" disabled={!dirty || savingFile === f.filename}
                    onClick={() => handleSave(f.filename)}>
                    {savingFile === f.filename ? 'Đang lưu…' : dirty ? 'Lưu' : 'Đã lưu'}
                  </button>
                )}
              </div>
              {editing ? (
                <textarea
                  className="field"
                  style={{ minHeight: 150, fontFamily: "'SF Mono','Consolas',monospace", fontSize: 13 }}
                  value={drafts[f.filename] ?? ''}
                  onChange={(e) => setDrafts((p) => ({ ...p, [f.filename]: e.target.value }))}
                />
              ) : (
                <div className="card" style={{ padding: '14px 18px' }}>
                  <div className="profile-content"
                    dangerouslySetInnerHTML={{ __html: renderMarkdown(stripLeadingH1(f.content || '') || '_(trống)_') }} />
                </div>
              )}
            </div>
          );
        })
      )}

      {toast && <div className="toast ok"><span className="toast-icon">✓</span>{toast}</div>}
    </div>
  );
}
