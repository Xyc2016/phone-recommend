# 手机推荐 AI Agent - 前端

## 技术栈

- **React 18** - UI框架
- **TypeScript** - 类型安全
- **rsbuild** - 构建工具
- **Ant Design** - UI组件库
- **Ant Design X** - AI组件库
- **Tailwind CSS** - 样式工具
- **dayjs** - 日期处理

## 项目结构

```
fe/
├── src/
│   ├── components/       # 组件
│   │   ├── Sidebar/     # 左侧边栏
│   │   ├── ChatArea/    # 聊天区域
│   │   └── ChatItem/    # 消息项
│   ├── hooks/           # 自定义Hooks
│   │   └── useThreads.ts
│   ├── services/        # 服务层
│   │   └── mockService.ts  # Mock数据服务
│   ├── types/           # 类型定义
│   │   └── index.ts
│   ├── App.tsx          # 主应用组件
│   ├── index.tsx        # 入口文件
│   └── index.css        # 全局样式
├── package.json
├── tsconfig.json
├── rsbuild.config.ts
└── tailwind.config.js
```

## 功能特性

- ✅ 多对话线程管理
- ✅ 对话列表（按日期分组：今天、昨天、更早）
- ✅ 新建对话
- ✅ 删除对话
- ✅ 消息发送和接收（Mock）
- ✅ 空状态展示
- ✅ 响应式布局

## 安装依赖

```bash
cd fe
npm install
```

## 开发运行

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动

## 构建

```bash
npm run build
```

构建产物将输出到 `dist/` 目录

## 预览构建结果

```bash
npm run preview
```

## Mock数据

当前使用Mock服务模拟AI响应，支持以下场景：

- 性价比/便宜手机推荐
- 5000元/旗舰手机推荐
- 拍照/相机需求
- 游戏/性能需求
- 通用咨询

## 下一步

- [ ] 连接后端API
- [ ] 用户认证
- [ ] 消息历史持久化
- [ ] 语音输入
- [ ] 图片上传
- [ ] 消息搜索

