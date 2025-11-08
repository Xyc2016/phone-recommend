import { Thread, Message } from '../types';

// Mock数据存储
let threads: Thread[] = [];
let threadIdCounter = 1;
let messageIdCounter = 1;

// 初始化一些mock数据
const initMockData = () => {
  const now = Date.now();
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  threads = [
    {
      id: '1',
      title: '我想买一款性价比高的手机',
      messages: [
        {
          id: 'm1',
          role: 'user',
          content: '我想买一款性价比高的手机',
          timestamp: now - 3600000,
        },
        {
          id: 'm2',
          role: 'assistant',
          content: '您好！我可以帮您推荐一些性价比高的手机。请告诉我您的预算范围和使用需求？',
          timestamp: now - 3590000,
        },
      ],
      createdAt: now - 3600000,
      updatedAt: now - 3590000,
    },
    {
      id: '2',
      title: '5000元左右的旗舰手机推荐',
      messages: [
        {
          id: 'm3',
          role: 'user',
          content: '5000元左右的旗舰手机推荐',
          timestamp: now - 7200000,
        },
        {
          id: 'm4',
          role: 'assistant',
          content: '在5000元价位，我推荐以下几款旗舰手机：\n1. 小米14 Pro - 性能强劲，拍照优秀\n2. iPhone 14 - 系统流畅，品牌可靠\n3. 华为 Mate 60 - 国产旗舰，技术先进',
          timestamp: now - 7190000,
        },
      ],
      createdAt: now - 7200000,
      updatedAt: now - 7190000,
    },
  ];
};

initMockData();

// 获取所有对话线程
export const getThreads = (): Promise<Thread[]> => {
  return Promise.resolve([...threads].sort((a, b) => b.updatedAt - a.updatedAt));
};

// 获取单个对话线程
export const getThread = (id: string): Promise<Thread | null> => {
  const thread = threads.find((t) => t.id === id);
  return Promise.resolve(thread ? { ...thread } : null);
};

// 创建新对话线程
export const createThread = (): Promise<Thread> => {
  const thread: Thread = {
    id: `thread-${threadIdCounter++}`,
    title: '新对话',
    messages: [],
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  threads.unshift(thread);
  return Promise.resolve({ ...thread });
};

// 发送消息（Mock响应）
export const sendMessage = async (
  threadId: string,
  content: string
): Promise<Message> => {
  const thread = threads.find((t) => t.id === threadId);
  if (!thread) {
    throw new Error('Thread not found');
  }

  // 添加用户消息
  const userMessage: Message = {
    id: `msg-${messageIdCounter++}`,
    role: 'user',
    content,
    timestamp: Date.now(),
  };
  thread.messages.push(userMessage);
  thread.updatedAt = Date.now();

  // 更新标题（如果这是第一条消息）
  if (thread.messages.length === 1) {
    thread.title = content.length > 20 ? content.substring(0, 20) + '...' : content;
  }

  // 模拟AI响应延迟
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // 生成Mock响应
  const assistantMessage: Message = {
    id: `msg-${messageIdCounter++}`,
    role: 'assistant',
    content: generateMockResponse(content),
    timestamp: Date.now(),
  };
  thread.messages.push(assistantMessage);
  thread.updatedAt = Date.now();

  return assistantMessage;
};

// 生成Mock响应
const generateMockResponse = (userMessage: string): string => {
  const lowerMessage = userMessage.toLowerCase();
  
  if (lowerMessage.includes('性价比') || lowerMessage.includes('便宜')) {
    return '根据您的需求，我推荐以下几款性价比高的手机：\n\n1. **Redmi Note 13 Pro** - 约2000元\n   - 天玑7200-Ultra处理器\n   - 1.5K屏幕，120Hz刷新率\n   - 2亿像素主摄\n\n2. **realme GT Neo6** - 约2500元\n   - 骁龙8s Gen 3\n   - 144Hz电竞屏\n   - 5500mAh大电池\n\n您更关注哪个方面？比如拍照、性能、续航等？';
  }
  
  if (lowerMessage.includes('5000') || lowerMessage.includes('旗舰')) {
    return '在5000元价位，我为您推荐：\n\n1. **小米14 Pro** - 约4999元\n   - 骁龙8 Gen 3\n   - 徕卡影像系统\n   - 120W快充\n\n2. **iPhone 14** - 约5299元\n   - A15芯片\n   - iOS系统\n   - 优秀拍摄能力\n\n3. **华为 Mate 60** - 约5499元\n   - 麒麟9000S\n   - 鸿蒙系统\n   - 卫星通信\n\n您更偏好哪个品牌或系统？';
  }
  
  if (lowerMessage.includes('拍照') || lowerMessage.includes('相机')) {
    return '如果您重视拍照功能，我推荐：\n\n1. **vivo X100 Pro** - 约5999元\n   - 蔡司影像系统\n   - 1英寸大底主摄\n   - 长焦微距\n\n2. **OPPO Find X7 Ultra** - 约5999元\n   - 哈苏影像\n   - 双潜望长焦\n   - 专业人像模式\n\n3. **小米14 Ultra** - 约6499元\n   - 徕卡四摄\n   - 1英寸可变光圈\n   - 专业摄影模式\n\n您的预算范围是多少？';
  }
  
  if (lowerMessage.includes('游戏') || lowerMessage.includes('性能')) {
    return '对于游戏和性能需求，推荐：\n\n1. **iQOO 12 Pro** - 约4999元\n   - 骁龙8 Gen 3\n   - 144Hz E6屏幕\n   - 游戏专用芯片\n\n2. **ROG Phone 7** - 约5999元\n   - 专为游戏设计\n   - 165Hz刷新率\n   - 6000mAh大电池\n\n3. **Redmi K70 Pro** - 约3299元\n   - 骁龙8 Gen 3\n   - 2K屏幕\n   - 性价比之选\n\n您主要玩什么类型的游戏？';
  }
  
  // 默认响应
  return '感谢您的咨询！我是手机推荐AI助手，可以帮助您：\n\n1. **根据预算推荐手机** - 告诉我您的预算范围\n2. **根据需求推荐** - 拍照、游戏、续航等\n3. **对比不同机型** - 我可以帮您对比多款手机\n4. **了解最新机型** - 2024年最新发布的手机\n\n请告诉我您的具体需求，我会为您推荐最适合的手机！';
};

// 删除对话线程
export const deleteThread = (id: string): Promise<void> => {
  threads = threads.filter((t) => t.id !== id);
  return Promise.resolve();
};

// 更新对话标题
export const updateThreadTitle = (id: string, title: string): Promise<void> => {
  const thread = threads.find((t) => t.id === id);
  if (thread) {
    thread.title = title;
  }
  return Promise.resolve();
};

