# 手机推荐 AI Agent - 前端

## 技术栈

- **React 19** - UI 框架
- **TypeScript** - 类型安全
- **rsbuild** - 构建工具
- **Ant Design** - UI 组件库
- **Tailwind CSS + SASS** - 样式系统
- **dayjs** - 日期处理

## 项目结构

```
fe/
├── src/
│   ├── components/       # 组件
│   │   ├── Sidebar/      # 左侧边栏
│   │   ├── ChatArea/     # 聊天区域
│   │   └── ChatItem/     # 消息项
│   ├── hooks/            # 自定义 Hooks
│   │   └── useThreads.ts
│   ├── services/         # 服务层
│   │   └── api.ts        # 后端 API 封装（SSE 支持）
│   ├── styles/           # SASS 变量等
│   ├── types/            # 类型定义
│   ├── App.tsx           # 主应用组件
│   ├── index.tsx         # 入口文件
│   └── index.scss        # 全局样式
├── package.json
├── tsconfig.json
├── rsbuild.config.ts
├── tailwind.config.js
└── .env.example
```

## 功能特性

- ✅ 多对话线程管理（创建、删除、切换）
- ✅ 对话列表按日期分组（今天、昨天、更早）
- ✅ 空状态与快速入口
- ✅ 与后端 API 对接（FastAPI + MongoDB）
- ✅ SSE 流式 AI 响应，实时渲染
- ✅ Tailwind + SASS 样式体系

## 安装依赖

```bash
cd fe
pnpm install
```

## 环境变量

复制 `.env.example` 为 `.env`，根据实际情况调整：

```bash
cp .env.example .env
# 例如：VITE_API_BASE_URL=http://localhost:8000
```

## 开发运行

```bash
pnpm run dev
```

应用将在 `http://localhost:3000` 启动。

## 构建

```bash
pnpm run build
```

构建产物输出到 `dist/` 目录。

## 预览构建结果

```bash
pnpm run preview
```

## 下一步

- [ ] 用户认证
- [ ] 消息历史搜索
- [ ] 语音输入
- [ ] 图片上传
- [ ] 主题 / 外观自定义

