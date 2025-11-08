import { Thread, Message } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// 获取所有对话线程
export const getThreads = async (): Promise<Thread[]> => {
  const response = await fetch(`${API_BASE_URL}/api/threads`);
  if (!response.ok) {
    throw new Error('Failed to fetch threads');
  }
  const data = await response.json();
  return data.map((thread: any) => ({
    ...thread,
    messages: thread.messages || [],
    createdAt: new Date(thread.created_at).getTime(),
    updatedAt: new Date(thread.updated_at).getTime(),
  }));
};

// 获取单个对话线程
export const getThread = async (id: string): Promise<Thread | null> => {
  const response = await fetch(`${API_BASE_URL}/api/threads/${id}`);
  if (!response.ok) {
    if (response.status === 404) {
      return null;
    }
    throw new Error('Failed to fetch thread');
  }
  const thread = await response.json();
  return {
    ...thread,
    messages: (thread.messages || []).map((msg: any) => ({
      ...msg,
      timestamp: new Date(msg.created_at).getTime(),
    })),
    createdAt: new Date(thread.created_at).getTime(),
    updatedAt: new Date(thread.updated_at).getTime(),
  };
};

// 创建新对话线程
export const createThread = async (): Promise<Thread> => {
  const response = await fetch(`${API_BASE_URL}/api/threads`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
  });
  if (!response.ok) {
    throw new Error('Failed to create thread');
  }
  const thread = await response.json();
  return {
    ...thread,
    messages: [],
    createdAt: new Date(thread.created_at).getTime(),
    updatedAt: new Date(thread.updated_at).getTime(),
  };
};

// 删除对话线程
export const deleteThread = async (id: string): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/api/threads/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete thread');
  }
};

// 重命名对话线程
export const renameThread = async (id: string, title: string): Promise<Thread> => {
  const response = await fetch(`${API_BASE_URL}/api/threads/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    throw new Error('Failed to rename thread');
  }

  const thread = await response.json();

  return {
    ...thread,
    messages: (thread.messages || []).map((msg: any) => ({
      ...msg,
      timestamp: new Date(msg.created_at).getTime(),
    })),
    createdAt: new Date(thread.created_at).getTime(),
    updatedAt: new Date(thread.updated_at).getTime(),
  };
};

// 发送消息（SSE 流式响应）
export const sendMessage = async (
  threadId: string,
  content: string,
  onChunk: (chunk: string) => void,
  onDone: () => void,
  onError: (error: Error) => void
): Promise<void> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/threads/${threadId}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('No response body');
    }

    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          try {
            const json = JSON.parse(data);
            if (json.done) {
              onDone();
              return;
            }
            if (json.content) {
              onChunk(json.content);
            }
            if (json.error) {
              onError(new Error(json.error));
              return;
            }
          } catch (e) {
            // 忽略解析错误
          }
        }
      }
    }

    onDone();
  } catch (error) {
    onError(error instanceof Error ? error : new Error('Unknown error'));
  }
};

