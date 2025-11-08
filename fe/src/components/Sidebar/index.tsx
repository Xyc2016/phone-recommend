import React from 'react';
import { Button, Dropdown, Empty } from 'antd';
import { PlusOutlined, MoreOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Thread } from '../../types';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import 'dayjs/locale/zh-cn';

dayjs.extend(relativeTime);
dayjs.locale('zh-cn');

interface SidebarProps {
  threads: Thread[];
  currentThreadId: string | null;
  onThreadSelect: (threadId: string) => void;
  onNewThread: () => void;
  onDeleteThread: (threadId: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  threads,
  currentThreadId,
  onThreadSelect,
  onNewThread,
  onDeleteThread,
}) => {
  // 按日期分组
  const groupThreadsByDate = (threads: Thread[]) => {
    const today = dayjs().startOf('day');
    const yesterday = today.subtract(1, 'day');

    const groups: { label: string; threads: Thread[] }[] = [
      { label: '今天', threads: [] },
      { label: '昨天', threads: [] },
      { label: '更早', threads: [] },
    ];

    threads.forEach((thread) => {
      const threadDate = dayjs(thread.updatedAt);
      if (threadDate.isAfter(today)) {
        groups[0].threads.push(thread);
      } else if (threadDate.isAfter(yesterday)) {
        groups[1].threads.push(thread);
      } else {
        groups[2].threads.push(thread);
      }
    });

    return groups.filter((group) => group.threads.length > 0);
  };

  const groups = groupThreadsByDate(threads);

  const getMenuItems = (threadId: string): MenuProps['items'] => [
    {
      key: 'delete',
      label: '删除',
      danger: true,
      onClick: () => onDeleteThread(threadId),
    },
  ];

  return (
    <div className="h-full flex flex-col bg-white border-r border-gray-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold">
            📱
          </div>
          <span className="text-lg font-semibold">手机推荐</span>
        </div>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          block
          onClick={onNewThread}
          className="h-10"
        >
          开启新对话
        </Button>
      </div>

      {/* Thread List */}
      <div className="flex-1 overflow-y-auto">
        {threads.length === 0 ? (
          <div className="p-4">
            <Empty description="暂无对话" />
          </div>
        ) : (
          groups.map((group) => (
            <div key={group.label} className="mb-4">
              <div className="px-4 py-2 text-sm text-gray-500 font-medium">
                {group.label}
              </div>
              <div>
                {group.threads.map((thread) => (
                  <div
                    key={thread.id}
                    className={`cursor-pointer px-4 py-3 hover:bg-gray-50 flex items-center gap-2 ${
                      currentThreadId === thread.id ? 'bg-blue-50 border-l-2 border-blue-500' : ''
                    }`}
                    onClick={() => onThreadSelect(thread.id)}
                  >
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-gray-900 truncate">
                        {thread.title}
                      </div>
                      {thread.messages.length > 0 && (
                        <div className="text-xs text-gray-500 mt-1 truncate">
                          {thread.messages[thread.messages.length - 1].content}
                        </div>
                      )}
                    </div>
                    <Dropdown
                      menu={{ items: getMenuItems(thread.id) }}
                      trigger={['click']}
                      onClick={(e) => e.stopPropagation()}
                    >
                      <Button
                        type="text"
                        icon={<MoreOutlined />}
                        size="small"
                        onClick={(e) => e.stopPropagation()}
                      />
                    </Dropdown>
                  </div>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

