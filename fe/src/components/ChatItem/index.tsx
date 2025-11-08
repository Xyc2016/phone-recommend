import React from 'react';
import { Avatar } from 'antd';
import { UserOutlined, RobotOutlined } from '@ant-design/icons';
import { Message } from '../../types';

interface ChatItemProps {
  message: Message;
}

export const ChatItem: React.FC<ChatItemProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <Avatar
        icon={isUser ? <UserOutlined /> : <RobotOutlined />}
        className={isUser ? 'bg-blue-500' : 'bg-purple-500'}
      />
      <div className={`flex-1 ${isUser ? 'items-end' : 'items-start'} flex flex-col max-w-[70%]`}>
        <div
          className={`rounded-lg px-4 py-2 ${
            isUser
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 text-gray-900'
          }`}
        >
          <div className="whitespace-pre-wrap break-words">{message.content}</div>
        </div>
      </div>
    </div>
  );
};

