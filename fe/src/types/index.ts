export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'tool' | 'unknown';
  content: string;
  timestamp: number;
}

export interface Thread {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
  updatedAt: number;
}

