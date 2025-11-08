import React, { useState, useEffect } from 'react';
import { Layout } from 'antd';
import { Sidebar } from './components/Sidebar';
import { ChatArea } from './components/ChatArea';
import { useThreads } from './hooks/useThreads';
import { Thread } from './types';
import { getThread } from './services/api';

const { Sider, Content } = Layout;

function App() {
  const { threads, addThread, removeThread, renameThread, refreshThreads } = useThreads();
  const [currentThreadId, setCurrentThreadId] = useState<string | null>(null);
  const [currentThread, setCurrentThread] = useState<Thread | null>(null);

  // 加载当前线程
  useEffect(() => {
    if (currentThreadId) {
      getThread(currentThreadId).then((thread) => {
        setCurrentThread(thread);
      });
    } else {
      setCurrentThread(null);
    }
  }, [currentThreadId]);

  // 刷新当前线程
  const handleMessageSent = () => {
    refreshThreads();
    if (currentThreadId) {
      getThread(currentThreadId).then((thread) => {
        setCurrentThread(thread);
      });
    }
  };

  const handleThreadCreated = (thread: Thread) => {
    setCurrentThreadId(thread.id);
    setCurrentThread(thread);
    refreshThreads();
  };

  const handleNewThread = async () => {
    try {
      const newThread = await addThread();
      setCurrentThreadId(newThread.id);
      setCurrentThread(newThread);
    } catch (error) {
      console.error('Failed to create thread:', error);
    }
  };

  const handleThreadSelect = (threadId: string) => {
    setCurrentThreadId(threadId);
  };

  const handleDeleteThread = async (threadId: string) => {
    await removeThread(threadId);
    if (currentThreadId === threadId) {
      setCurrentThreadId(null);
      setCurrentThread(null);
    }
  };

  const handleRenameThread = async (threadId: string, newTitle: string) => {
    try {
      const updated = await renameThread(threadId, newTitle);
      if (currentThreadId === threadId) {
        setCurrentThread((prev) =>
          prev
            ? {
                ...prev,
                title: updated.title,
                updatedAt: updated.updatedAt,
              }
            : prev
        );
      }
    } catch (error) {
      console.error('Failed to rename thread:', error);
    }
  };

  return (
    <Layout className="h-screen">
      <Sider width={320} className="h-screen" theme="light">
        <Sidebar
          threads={threads}
          currentThreadId={currentThreadId}
          onThreadSelect={handleThreadSelect}
          onNewThread={handleNewThread}
          onDeleteThread={handleDeleteThread}
          onRenameThread={handleRenameThread}
        />
      </Sider>
      <Content className="h-screen">
        <ChatArea 
          thread={currentThread} 
          onMessageSent={handleMessageSent}
          onThreadCreated={handleThreadCreated}
        />
      </Content>
    </Layout>
  );
}

export default App;

