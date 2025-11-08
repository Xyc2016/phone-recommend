# 手机推荐 AI Agent

一个基于AI的手机推荐助手，帮助用户找到最适合的手机。

## 项目结构

```
phone-recommend/
├── fe/              # 前端项目 (React + TypeScript + Ant Design)
│   ├── src/         # 源代码
│   ├── package.json # 前端依赖
│   ├── .gitignore   # 前端 Git 忽略文件
│   └── README.md    # 前端文档
├── be/              # 后端项目 (Python + asyncio + MongoDB + LangChain) [待开发]
│   ├── .gitignore   # 后端 Git 忽略文件
│   └── ...
└── README.md       # 项目总文档
```

## Git 仓库说明

本项目使用**单一 Git 仓库**（Monorepo）管理前后端代码：

- ✅ 统一版本控制，前后端代码同步
- ✅ 便于代码审查和协作
- ✅ 统一的 CI/CD 配置
- ✅ 便于共享工具和配置

### 初始化 Git 仓库

```bash
# 在项目根目录初始化
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Add frontend and backend structure"
```

### 分支策略建议

- `main/master`: 主分支，生产环境代码
- `develop`: 开发分支
- `feat/*`: 功能分支
- `fix/*`: 修复分支

## 前端

详见 [fe/README.md](./fe/README.md)

### 快速开始

```bash
cd fe
pnpm install
pnpm run dev
```

## 后端

待开发...

## 技术栈

### 前端
- React 19
- TypeScript
- rsbuild
- Ant Design
- Tailwind CSS
- SASS

### 后端 (计划)
- Python
- asyncio
- MongoDB
- LangChain

## 开发规范

### 提交信息规范

建议使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

### 目录规范

- `fe/`: 前端相关代码，包含自己的 `.gitignore` 和配置文件
- `be/`: 后端相关代码，包含自己的 `.gitignore` 和配置文件
- 每个子项目独立管理自己的依赖和构建产物

