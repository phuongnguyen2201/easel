import type { Page } from './Sidebar';
import type { ComponentType } from 'react';
import { IconDashboard, IconFire, IconIdea, IconCalendar, IconPublish, IconSkills } from './icons';

interface SubNavProps {
  current: Page;
  onNavigate: (page: Page) => void;
}

const TOOLS: { page: Page; Icon: ComponentType<{ size?: number }>; label: string }[] = [
  { page: 'trends', Icon: IconFire, label: 'Radar xu hướng' },
  { page: 'ideas', Icon: IconIdea, label: 'Kho ý tưởng' },
  { page: 'calendar', Icon: IconCalendar, label: 'Lịch nội dung' },
  { page: 'publish', Icon: IconPublish, label: 'Trung tâm đăng bài' },
  { page: 'breakdown', Icon: IconSkills, label: 'Mổ xẻ bài viral' },
];

export default function SubNav({ current, onNavigate }: SubNavProps) {
  return (
    <div className="subnav">
      <button className="subnav-back" onClick={() => onNavigate('dashboard')} title="Về bàn làm việc">
        <IconDashboard size={15} /> Bàn làm việc
      </button>
      <span className="subnav-div" />
      <div className="subnav-tabs">
        {TOOLS.map(({ page, Icon, label }) => (
          <button key={page} className={`subnav-tab ${current === page ? 'active' : ''}`}
            onClick={() => onNavigate(page)}>
            <Icon size={14} />{label}
          </button>
        ))}
      </div>
    </div>
  );
}
