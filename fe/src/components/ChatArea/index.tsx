import React, { useState, useEffect, useRef } from 'react';
import { Empty, Input, Button, message as antdMessage } from 'antd';
import { SendOutlined, AudioOutlined, MobileOutlined } from '@ant-design/icons';
import { Thread, Message } from '../../types';
import { sendMessage, createThread } from '../../services/api';
import { ChatItem } from '../ChatItem';

const { TextArea } = Input;

interface ChatAreaProps {
  thread: Thread | null;
  onMessageSent: (message: Message) => void;
  onThreadCreated?: (thread: Thread) => void;
}

export const ChatArea: React.FC<ChatAreaProps> = ({ thread, onMessageSent, onThreadCreated }) => {
  const [inputValue, setInputValue] = useState('');
  const [sending, setSending] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState<Message | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [thread?.messages, streamingMessage]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!inputValue.trim() || sending) return;

    const content = inputValue.trim();
    setInputValue('');
    setSending(true);

    try {
      let currentThread = thread;
      
      // 如果没有对话，先创建一个
      if (!currentThread) {
        currentThread = await createThread();
        onThreadCreated?.(currentThread);
      }

      // 创建流式消息占位符
      const tempAssistantMessage: Message = {
        id: `temp-${Date.now()}`,
        role: 'assistant',
        content: '',
        timestamp: Date.now(),
      };
      setStreamingMessage(tempAssistantMessage);

      // 发送消息并接收 SSE 流式响应
      let fullContent = '';
      await sendMessage(
        currentThread.id,
        content,
        (chunk: string) => {
          // 接收流式数据块
          fullContent += chunk;
          setStreamingMessage({
            ...tempAssistantMessage,
            content: fullContent,
          });
        },
        () => {
          // 流式响应完成
          setStreamingMessage(null);
          setSending(false);
          // 刷新线程以获取最新消息
          onMessageSent({
            ...tempAssistantMessage,
            content: fullContent,
          });
        },
        (error: Error) => {
          // 错误处理
          setStreamingMessage(null);
          setSending(false);
          antdMessage.error(`发送失败: ${error.message}`);
          console.error('Failed to send message:', error);
        }
      );
    } catch (error) {
      setStreamingMessage(null);
      setSending(false);
      antdMessage.error('发送失败，请稍后重试');
      console.error('Failed to send message:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // 空状态
  if (!thread || thread.messages.length === 0) {
    return (
      <div className="h-full flex flex-col bg-white">
        <div className="flex-1 flex items-center justify-center">
          <Empty
            image={<MobileOutlined style={{ fontSize: 64, color: '#d9d9d9' }} />}
            description={
              <span className="text-gray-500">
                开始对话吧！告诉我您的手机需求，我会为您推荐合适的手机。
              </span>
            }
          />
        </div>
        <div className="border-t border-gray-200 p-4">
          <div className="max-w-4xl mx-auto">
            <div className="flex gap-2 mb-2">
              <Button size="small" type="text">
                了解推荐
              </Button>
              <Button size="small" type="text">
                热门机型
              </Button>
              <Button size="small" type="text">
                购买指南
              </Button>
              <Button size="small" type="text">
                对比分析
              </Button>
            </div>
            <div className="flex gap-2">
              <TextArea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="例如：我想买一款5000元左右的拍照手机"
                autoSize={{ minRows: 1, maxRows: 4 }}
                className="flex-1"
              />
              <Button
                type="primary"
                icon={<SendOutlined />}
                onClick={handleSend}
                loading={sending}
                disabled={!inputValue.trim()}
              >
                发送
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Messages */}
      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto p-4 space-y-4"
        style={{ scrollBehavior: 'smooth' }}
      >
        {thread.messages.map((message) => (
          <ChatItem key={message.id} message={message} />
        ))}
        {streamingMessage && (
          <ChatItem key={streamingMessage.id} message={streamingMessage} />
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-2 mb-2">
            <Button size="small" type="text">
              了解推荐
            </Button>
            <Button size="small" type="text">
              热门机型
            </Button>
            <Button size="small" type="text">
              购买指南
            </Button>
            <Button size="small" type="text">
              对比分析
            </Button>
          </div>
          <div className="flex gap-2">
            <TextArea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="输入您的问题..."
              autoSize={{ minRows: 1, maxRows: 4 }}
              className="flex-1"
            />
            <Button
              type="text"
              icon={<AudioOutlined />}
              onClick={() => {
                // TODO: 语音输入
              }}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={handleSend}
              loading={sending}
              disabled={!inputValue.trim()}
            >
              发送
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

