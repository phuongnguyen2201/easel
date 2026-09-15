import { useState, useEffect } from 'react';
import {
  fetchTrends, fetchSchedule, fetchOutputs, fetchAccounts, fetchIdeas,
  fetchAnalyticsPlatforms, fetchAccountAnalytics,
} from '../lib/api';
import type {
  TrendGroup, ScheduleItem, OutputNode, AccountItem, Idea,
  AnalyticsPlatform, AccountAnalytics, AccountWhoami,
} from '../lib/api';
import type { Page } from './Sidebar';
import { getWhoamiCache, verifyStale } from '../lib/whoami';
import {
  IconFire, IconCalendar, IconOutputs, IconChat, IconSkills, IconAccounts,
  IconIdea, IconPublish,
} from './icons';

/** 大数格式化：12000 → 1.2万。 */
function fmtNum(n: number | null): string {
  if (n == null) return '—';
  const a = Math.abs(n);
  if (a >= 1000000) return (n / 1000000).toFixed(1) + 'M';
  if (a >= 1000) return (n / 1000).toFixed(a >= 100000 ? 0 : 1) + 'K';
  return String(n);
}
/** 增长量渲染信息：正=绿↑，负=红↓，0/缺失=不显示。 */
function growthInfo(n: number | null): { text: string; color: string } | null {
  if (n == null || n === 0) return null;
  return n > 0
    ? { text: `▲+${fmtNum(n)}`, color: 'var(--trend-up)' }
    : { text: `▼${fmtNum(Math.abs(n))}`, color: 'var(--trend-down)' };
}

interface DashboardProps {
  persona: string;
  gatewayStatus: string;
  onNavigate: (page: Page) => void;
  onUseTopic: (title: string) => void;
}

const STATUS_LABEL: Record<string, string> = { idea: 'Ý tưởng', draft: 'Nháp', scheduled: 'Chờ đăng', published: 'Đã đăng' };

export default function DashboardPage({ persona, gatewayStatus, onNavigate, onUseTopic }: DashboardProps) {
  const [trends, setTrends] = useState<TrendGroup[]>([]);
  const [schedule, setSchedule] = useState<ScheduleItem[]>([]);
  const [outputs, setOutputs] = useState<OutputNode[]>([]);
  const [accounts, setAccounts] = useState<AccountItem[]>([]);
  const [ideas, setIdeas] = useState<Idea[]>([]);
  // 归因层：账号创作数据
  const [anaPlats, setAnaPlats] = useState<AnalyticsPlatform[]>([]);
  const [anaSel, setAnaSel] = useState('');
  const [anaData, setAnaData] = useState<Record<string, AccountAnalytics | 'loading' | 'error'>>(() => {
    try { return JSON.parse(localStorage.getItem('easel_analytics') || '{}'); } catch { return {}; }
  });
  const [anaWin, setAnaWin] = useState<'last' | 'day' | 'week' | 'month' | 'year'>('week');
  // whoami 自愈：登录态以真实 profile 为准（与账号页共享 localStorage 缓存）
  const [whoamiMap, setWhoamiMap] = useState<Record<string, AccountWhoami>>(() => getWhoamiCache());

  useEffect(() => {
    fetchTrends('weibo,douyin', 6).then((d) => setTrends(d.trends)).catch(() => {});
    fetchSchedule().then(setSchedule).catch(() => {});
    fetchOutputs().then(setOutputs).catch(() => {});
    fetchAccounts().then(setAccounts).catch(() => {});
    fetchIdeas().then(setIdeas).catch(() => {});
    fetchAnalyticsPlatforms().then((ps) => {
      setAnaPlats(ps);
      const cache = getWhoamiCache();
      const isLog = (p: AnalyticsPlatform) => p.loggedIn || !!cache[p.platform]?.loggedIn;
      const first = ps.find(isLog);
      if (first) setAnaSel((s) => s || first.platform);
      // 开页后台自愈：对非 B 站的归因平台真校验（whoami），刷新登录态；B 站走 cookie 判定不必。
      verifyStale(ps.filter((p) => p.platform !== 'bilibili').map((p) => p.platform), {
        onUpdate: (platform, r) => {
          setWhoamiMap((m) => ({ ...m, [platform]: r }));
          if (r.loggedIn) setAnaSel((s) => s || platform);
        },
      });
    }).catch(() => {});
  }, []);

  const runAna = (platform: string) => {
    setAnaSel(platform);
    setAnaData((d) => ({ ...d, [platform]: 'loading' }));
    fetchAccountAnalytics(platform)
      .then((r) => setAnaData((d) => {
        const next = { ...d, [platform]: r };
        try { localStorage.setItem('easel_analytics', JSON.stringify(next)); } catch { /* quota */ }
        return next;
      }))
      .catch(() => setAnaData((d) => ({ ...d, [platform]: 'error' as const })));
  };

  const hour = new Date().getHours();
  const greet = hour < 6 ? 'Khuya rồi' : hour < 12 ? 'Chào buổi sáng' : hour < 14 ? 'Chào buổi trưa' : hour < 18 ? 'Chào buổi chiều' : 'Chào buổi tối';
  const todayStr = new Date().toISOString().slice(0, 10);
  const upcoming = [...schedule]
    .filter((s) => s.date >= todayStr && s.status !== 'published')
    .sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time)).slice(0, 5);
  const recent = outputs.slice(0, 5);
  const pendingIdeas = ideas.filter((i) => i.status === 'pending');
  const loggedIn = accounts.filter((a) => a.loggedIn).length;

  const quick: { label: string; page: Page; Icon: typeof IconChat }[] = [
    { label: 'Bắt đầu trò chuyện', page: 'chat', Icon: IconChat },
    { label: 'Xem xu hướng', page: 'trends', Icon: IconFire },
    { label: 'Mổ xẻ bài viral', page: 'breakdown', Icon: IconSkills },
    { label: 'Ghi ý tưởng', page: 'ideas', Icon: IconIdea },
    { label: 'Lên lịch', page: 'calendar', Icon: IconCalendar },
    { label: 'Đi đăng bài', page: 'publish', Icon: IconPublish },
  ];

  const stats: { label: string; value: string; page: Page; Icon: typeof IconChat }[] = [
    { label: 'Ý tưởng chờ làm', value: String(pendingIdeas.length), page: 'ideas', Icon: IconIdea },
    { label: 'Lịch chờ đăng', value: String(upcoming.length), page: 'calendar', Icon: IconCalendar },
    { label: 'Dự án nội dung', value: String(outputs.length), page: 'outputs', Icon: IconOutputs },
    { label: 'Tài khoản đã đăng nhập', value: `${loggedIn}/${accounts.length}`, page: 'accounts', Icon: IconAccounts },
  ];

  return (
    <div className="page-scroll dash-page">
      <div className="dash-hero">
        <h1 className="page-title" style={{ fontSize: 26 }}>{greet} 👋</h1>
        <p className="page-subtitle">
          {gatewayStatus === 'connected' ? 'Mọi thứ sẵn sàng.' : '⚠ Gateway chưa kết nối.'}
          {persona ? ` Hồ sơ hiện tại «${persona}».` : ' Chế độ chung — chọn hồ sơ sẽ cho kết quả tốt hơn.'}
          Từ xu hướng đến đăng bài, xử lý trọn nội dung hôm nay ở một nơi.
        </p>
        <div className="dash-quick">
          {quick.map((q) => (
            <button key={q.page} className="dash-quick-btn" onClick={() => onNavigate(q.page)}>
              <q.Icon size={16} /><span>{q.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* 概览数字 */}
      <div className="dash-stats">
        {stats.map((s) => (
          <button key={s.label} className="card card-hover dash-stat" onClick={() => onNavigate(s.page)}>
            <span className="dash-stat-ic"><s.Icon size={18} /></span>
            <span className="dash-stat-val">{s.value}</span>
            <span className="dash-stat-label">{s.label}</span>
          </button>
        ))}
      </div>

      <div className="dash-grid">
        {/* 今日热点 */}
        <div className="card dash-card">
          <div className="dash-card-head">
            <span><IconFire size={16} /> Xu hướng hôm nay</span>
            <button className="dash-more" onClick={() => onNavigate('trends')}>Radar xu hướng →</button>
          </div>
          {trends.length === 0 && <div className="dash-empty">Đang tải xu hướng / cần cấu hình proxy</div>}
          {trends.map((g) => (
            <div key={g.platform} className="dash-trend-group">
              <div className="dash-trend-plat">{g.label}</div>
              {g.items.slice(0, 3).map((it, i) => (
                <div key={i} className="dash-trend-item" title={`${it.title}(bấm để làm thành nội dung)`}>
                  <span className="dash-trend-title" onClick={() => onUseTopic(it.title)}>{it.title}</span>
                </div>
              ))}
            </div>
          ))}
        </div>

        {/* 选题库 */}
        <div className="card dash-card">
          <div className="dash-card-head">
            <span><IconIdea size={16} /> Kho ý tưởng · chờ làm</span>
            <button className="dash-more" onClick={() => onNavigate('ideas')}>Tất cả →</button>
          </div>
          {pendingIdeas.length === 0 && <div className="dash-empty">Chưa có ý tưởng nào, vào Radar xu hướng lưu vài cái nhé</div>}
          {pendingIdeas.slice(0, 5).map((it) => (
            <div key={it.id} className="dash-idea" onClick={() => onUseTopic(it.title)} title="Bấm để làm thành nội dung">
              <span className="dash-idea-title">{it.title}</span>
              {it.source && <span className="badge">{it.source}</span>}
            </div>
          ))}
        </div>

        {/* 近期排期 */}
        <div className="card dash-card">
          <div className="dash-card-head">
            <span><IconCalendar size={16} /> Lịch sắp tới</span>
            <button className="dash-more" onClick={() => onNavigate('calendar')}>Lịch →</button>
          </div>
          {upcoming.length === 0 && <div className="dash-empty">Chưa có lịch đăng, vào Lịch sắp xếp một mục nhé</div>}
          {upcoming.map((s) => (
            <div key={s.id} className="dash-sched" onClick={() => onNavigate('calendar')}>
              <span className="dash-sched-date">{s.date.slice(5)}</span>
              <span className="dash-sched-title">{s.platform ? `[${s.platform}] ` : ''}{s.title}</span>
              <span className="badge">{STATUS_LABEL[s.status] || s.status}</span>
            </div>
          ))}
        </div>

        {/* 最近产物 */}
        <div className="card dash-card dash-card-top">
          <div className="dash-card-head">
            <span><IconOutputs size={16} /> Sản phẩm gần đây</span>
            <button className="dash-more" onClick={() => onNavigate('outputs')}>Thư viện nội dung →</button>
          </div>
          {recent.length === 0 && <div className="dash-empty">Chưa có sản phẩm nào, vào Trò chuyện tạo cái đầu tiên nhé</div>}
          {recent.map((g) => (
            <div key={g.name} className="dash-output" onClick={() => onNavigate('outputs')}>
              <span className="dash-output-name">{g.meta?.title || g.name}</span>
              <span className="badge">{g.meta?.platform || (g.type === 'dir' ? `${g.fileCount ?? 0} tệp` : 'Một tệp')}</span>
            </div>
          ))}
        </div>

        {/* 创作数据（归因层）：选平台自动拉取登录账号的粉丝/获赞/关注 + 多窗口增长 + 近7日环比 + 最新笔记 */}
        <div className="card dash-card dash-card-wide">
          <div className="dash-card-head">
            <span><IconAccounts size={16} /> Dữ liệu sáng tạo</span>
            {anaSel && anaData[anaSel] && anaData[anaSel] !== 'loading' && (
              <button className="dash-more" onClick={() => runAna(anaSel)}>Làm mới →</button>
            )}
          </div>
          {(() => {
            const logged = anaPlats.filter((p) => p.loggedIn || whoamiMap[p.platform]?.loggedIn);
            if (anaPlats.length === 0) return <div className="dash-empty">Đang tải / cần cấu hình proxy</div>;
            if (logged.length === 0) {
              return (
                <div className="dash-empty" onClick={() => onNavigate('accounts')} style={{ cursor: 'pointer' }}>
                  Đăng nhập ở trang Tài khoản rồi xem ở đây người theo dõi / lượt thích / đang theo dõi của từng nền tảng, xu hướng tăng trưởng và bài mới nhất →
                </div>
              );
            }
            const d = anaSel ? anaData[anaSel] : undefined;
            const WIN: [typeof anaWin, string][] = [
              ['last', 'so với lần trước'], ['day', 'so với hôm qua'], ['week', 'so với tuần trước'], ['month', 'so với tháng trước'], ['year', 'so với năm trước'],
            ];
            return (
              <>
                <div className="ana-plats">
                  {logged.map((p) => (
                    <button key={p.platform} className={`chip ${anaSel === p.platform ? 'active' : ''}`}
                      onClick={() => runAna(p.platform)}>{p.name}</button>
                  ))}
                </div>
                {!d && <div className="dash-empty">Bấm nền tảng phía trên để xem dữ liệu tài khoản</div>}
                {d === 'loading' && (
                  <div className="loading" style={{ padding: '28px 0' }}><div className="spinner" />Đang thu thập… (khởi động trình duyệt, vài giây)</div>
                )}
                {d === 'error' && (
                  <div className="dash-empty" style={{ color: 'var(--red)' }}>Thu thập thất bại (chưa đăng nhập / cần kiểm tra trên máy thật), bấm nền tảng để thử lại</div>
                )}
                {d && d !== 'loading' && d !== 'error' && (!d.loggedIn ? (
                  <div className="dash-empty" onClick={() => onNavigate('accounts')} style={{ cursor: 'pointer' }}>
                    Trạng thái đăng nhập nền tảng này đã hết hiệu lực, vào trang Tài khoản đăng nhập lại →
                  </div>
                ) : (
                  <div className="ana-body">
                    {/* 概览 + 增长对比 */}
                    <div className="ana-col ana-col-main">
                      <div className="ana-id">{d.nickname ? `@${d.nickname}` : d.name}</div>
                      <div className="ana-overview">
                        {([['Người theo dõi', 'followers'], ['Lượt thích', 'likes'], ['Đang theo dõi', 'following']] as const).map(([label, key]) => {
                          const w = d.growth?.[anaWin] ?? null;
                          const g = w ? growthInfo(w[key as 'followers' | 'likes']) : null;
                          return (
                            <div key={key} className="ana-stat">
                              <div className="ana-stat-val">{fmtNum(d[key])}</div>
                              <div className="ana-stat-label">{label}</div>
                              {g ? <div className="ana-stat-delta" style={{ color: g.color }}>{g.text}</div>
                                 : <div className="ana-stat-delta ana-muted">—</div>}
                            </div>
                          );
                        })}
                      </div>
                      <div className="ana-wins">
                        {WIN.map(([k, lab]) => (
                          <button key={k} className={`ana-win ${anaWin === k ? 'on' : ''}`}
                            onClick={() => setAnaWin(k)}>{lab}</button>
                        ))}
                      </div>
                      <div className="ana-wins-note">
                        {d.growth?.[anaWin]?.since_days != null
                          ? `So với ảnh chụp ${d.growth[anaWin]!.since_days} ngày trước`
                          : 'Chưa có ảnh chụp lịch sử cho khoảng này, làm mới vài lần để tích luỹ dữ liệu so sánh'}
                      </div>
                    </div>

                    {/* 近7日平台指标 + 环比 */}
                    <div className="ana-col ana-col-metrics">
                      <div className="ana-sub">7 ngày gần nhất · so kỳ trước</div>
                      {(d.metrics ?? []).length === 0 ? (
                        <div className="dash-empty">Nền tảng này không cung cấp chỉ số 7 ngày</div>
                      ) : (
                        <div className="ana-metrics">
                          {(d.metrics ?? []).map((m) => {
                            const vs = m.vs ?? '';
                            const up = vs.startsWith('+');
                            const has = vs && vs !== '-';
                            return (
                              <div key={m.label} className="ana-metric">
                                <div className="ana-metric-val">{m.value}</div>
                                <div className="ana-metric-label">{m.label}</div>
                                {has && <div className="ana-metric-vs" style={{ color: up ? 'var(--trend-up)' : 'var(--trend-down)' }}>so kỳ trước {vs}</div>}
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>

                    {/* 最新笔记（可点进原文） */}
                    <div className="ana-col ana-col-notes">
                      <div className="ana-sub">Bài mới nhất</div>
                      {(d.notes ?? []).length === 0 ? (
                        <div className="dash-empty">Tài khoản này chưa có bài đã đăng đọc được</div>
                      ) : (
                        <div className="ana-notes">
                          {(d.notes ?? []).slice(0, 6).map((n, i) => (
                            <a key={i} className="ana-note" href={n.url} target="_blank" rel="noreferrer" title={n.title}>
                              {n.cover
                                ? <img className="ana-note-cover" src={n.cover} alt="" referrerPolicy="no-referrer" />
                                : <span className="ana-note-cover ana-note-cover-ph">📝</span>}
                              <span className="ana-note-main">
                                <span className="ana-note-title">{n.title || '(Không tiêu đề)'}</span>
                                {n.stat && <span className="ana-note-stat">{n.stat}</span>}
                              </span>
                              <span className="ana-note-go">↗</span>
                            </a>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </>
            );
          })()}
        </div>
      </div>
    </div>
  );
}
