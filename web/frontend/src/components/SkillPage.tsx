import { useState, useEffect, useMemo } from 'react';
import type { ComponentType } from 'react';
import { fetchSkills } from '../lib/api';
import type { SkillItem } from '../lib/api';
import SkillDrawer from './SkillDrawer';
import {
  IconSearch, IconCompass, IconSkills, IconSend, IconChart, IconLayers,
  IconVideo, IconImage, IconMusic, IconMic, IconText, IconLayout, IconProfile, IconOutputs,
} from './icons';

interface SkillPageProps {
  persona: string;
}

type IconC = ComponentType<{ size?: number }>;
type LayerMeta = { key: string; label: string; Icon: IconC; color: string };

const LAYERS: LayerMeta[] = [
  { key: 'discover', label: 'Khám phá', Icon: IconSearch, color: 'var(--layer-discover)' },
  { key: 'plan', label: 'Lên kế hoạch', Icon: IconCompass, color: 'var(--layer-plan)' },
  { key: 'produce', label: 'Sản xuất', Icon: IconSkills, color: 'var(--layer-produce)' },
  { key: 'publish', label: 'Đăng bài', Icon: IconSend, color: 'var(--layer-publish)' },
  { key: 'attribute', label: 'Đo lường', Icon: IconChart, color: 'var(--layer-attribute)' },
  { key: 'general', label: 'Chung', Icon: IconLayers, color: 'var(--layer-general)' },
];
const LAYER_META: Record<string, LayerMeta> = Object.fromEntries(LAYERS.map((l) => [l.key, l]));
const OTHER: LayerMeta = { key: 'other', label: 'Khác', Icon: IconLayers, color: 'var(--layer-general)' };

// 按 skill 名关键词映射线性图标（无匹配退回层图标）
function iconFor(name: string, LayerIcon: IconC): IconC {
  const n = name.toLowerCase();
  const map: [RegExp, IconC][] = [
    [/video|clip|reframe|highlight|beat|slideshow|intro|chapter/, IconVideo],
    [/image|img|photo|poster|infographic|comparison|meme|remove-bg|green-screen|enhance/, IconImage],
    [/music|audio|bgm|mix|denoise/, IconMusic],
    [/voice|tts|clone|subtitle/, IconMic],
    [/card|xhs|xiaohongshu|note/, IconLayout],
    [/copy|writ|text|polish|condens|style|format|content/, IconText],
    [/chart|data|report|roi|analy|insight|scor/, IconChart],
    [/publish|upload|wechat|zhihu|bilibili|douyin|kuaishou|channel/, IconSend],
    [/rss|trend|news|discover|ugc|competitor|hot/, IconSearch],
    [/profile|persona|brand|position|audience/, IconProfile],
    [/schedul|calendar|plan|strategy|campaign|matrix/, IconCompass],
    [/asset|template|batch|doc|mindmap|link/, IconOutputs],
  ];
  for (const [re, C] of map) if (re.test(n)) return C;
  return LayerIcon;
}

const LAYER_DESC: Record<string, string> = {
  discover: 'Kỹ năng lớp Khám phá', plan: 'Kỹ năng lớp Lên kế hoạch', produce: 'Kỹ năng lớp Sản xuất',
  publish: 'Kỹ năng lớp Đăng bài', attribute: 'Kỹ năng lớp Đo lường', general: 'Kỹ năng chung', other: 'Kỹ năng',
};

export default function SkillPage({ persona }: SkillPageProps) {
  const [skills, setSkills] = useState<SkillItem[]>([]);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState<string | null>(null);

  const load = () => {
    fetchSkills().then(setSkills).catch(() => setError('Tải danh sách SKILL thất bại'));
  };
  useEffect(load, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return skills;
    return skills.filter((s) =>
      s.name.toLowerCase().includes(q) || (s.description || '').toLowerCase().includes(q));
  }, [skills, query]);

  const grouped = useMemo(() => {
    const g: Record<string, SkillItem[]> = {};
    for (const s of filtered) {
      const key = LAYER_META[s.layer] ? s.layer : 'other';
      (g[key] ||= []).push(s);
    }
    return g;
  }, [filtered]);

  const orderedLayers = [...LAYERS, OTHER].filter((l) => grouped[l.key]?.length);
  const needApiCount = skills.filter((s) => s.needsApi && !s.apiConfigured).length;

  return (
    <div className="skills-page">
      <div className="skills-page-head">
        <h1 className="page-title">Thư viện kỹ năng</h1>
        <p className="page-subtitle">
          Tổng cộng {skills.length} kỹ năng, xem theo từng lớp của quy trình. Bấm thẻ để xem mô tả và chạy tại chỗ;
          kỹ năng gắn nhãn <span className="badge badge-warn" style={{ padding: '1px 7px' }}>Cần API</span> phải cấu hình khoá trước
          {needApiCount > 0 && ` (hiện còn ${needApiCount} kỹ năng chờ cấu hình)`}.
        </p>
        <div className="skill-search">
          <span className="skill-search-ic"><IconSearch size={16} /></span>
          <input
            className="field"
            placeholder="Tìm theo tên hoặc mô tả kỹ năng…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          {query && <button className="btn btn-ghost btn-sm" onClick={() => setQuery('')}>Xoá</button>}
        </div>
      </div>

      {error && <div style={{ color: 'var(--red)', maxWidth: 1100, margin: '16px auto' }}>{error}</div>}

      <div className="skills-body">
        {orderedLayers.length === 0 && !error && (
          <div className="empty-state" style={{ height: 240 }}>
            <div className="empty-icon"><IconSearch size={40} /></div>
            <p>Không có kỹ năng nào khớp «{query}»</p>
          </div>
        )}

        {orderedLayers.map((layer) => (
          <section key={layer.key}>
            <div className="section-title">
              <span className="section-ic" style={{ color: layer.color }}><layer.Icon size={15} /></span>
              {layer.label}
              <span style={{ color: 'var(--text-tertiary)', fontWeight: 500 }}>· {grouped[layer.key].length}</span>
            </div>
            <div className="skill-grid">
              {grouped[layer.key].map((s) => {
                const meta = LAYER_META[s.layer] || OTHER;
                const Icon = iconFor(s.name, meta.Icon);
                const alert = s.needsApi && !s.apiConfigured;
                return (
                  <div
                    key={s.name}
                    className="card card-hover skill-card"
                    style={{ ['--layer-color' as string]: meta.color }}
                    onClick={() => setSelected(s.name)}
                  >
                    {alert && <div className="skill-card-alert" title="Cần cấu hình API key">!</div>}
                    <div className="skill-card-icon" style={{ color: meta.color }}><Icon size={19} /></div>
                    <div className="skill-card-name">{s.name}</div>
                    <div className="skill-card-desc">{s.description?.trim() || LAYER_DESC[layer.key]}</div>
                    <div className="skill-card-foot">
                      {s.needsApi && (s.apiConfigured
                        ? <span className="badge badge-ok">Đã cấu hình</span>
                        : <span className="badge badge-warn">Cần API</span>)}
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        ))}
      </div>

      {selected && (
        <SkillDrawer
          skillName={selected}
          persona={persona}
          onClose={() => setSelected(null)}
          onConfigured={load}
        />
      )}
    </div>
  );
}
