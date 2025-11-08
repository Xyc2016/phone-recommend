# 手机搜索工具使用指南

## 概述

手机搜索工具（`search_phones`）是一个 LangChain Tool，让 AI Agent 能够从 MongoDB 数据库中搜索手机信息。当用户询问手机推荐、手机参数、手机对比等问题时，AI 会自动调用这个工具来获取相关数据。

## 功能特性

### 支持的搜索条件

1. **关键词搜索**：匹配品牌、型号、描述、特色、标签等
2. **品牌筛选**：精确匹配品牌名称
3. **价格区间**：指定最低价格和最高价格
4. **硬件配置**：
   - 运行内存（RAM）
   - 存储容量（Storage）
5. **标签筛选**：如"旗舰机"、"游戏手机"、"拍照手机"等
6. **结果数量**：可指定返回结果数量（1-20，默认5）

### 返回信息

工具会返回格式化的手机信息，包括：
- 品牌和型号
- 简介描述
- 芯片处理器
- 屏幕信息
- 电池和充电
- 相机配置
- 特色功能
- SKU 配置（内存、存储、颜色、价格）

## 技术实现

### 文件结构

```
be/app/
├── tools/
│   ├── __init__.py              # 工具模块导出
│   └── search_phones.py     # 手机搜索工具实现
├── services/
│   ├── llm_service.py           # LLM 服务（支持工具调用）
│   └── phone_service.py         # 手机数据服务
└── main.py                      # 应用启动（绑定工具）
```

### 核心组件

#### 1. PhoneSearchInput (Pydantic Schema)

定义了工具的输入参数结构，LangChain 使用这个 schema 来告诉 LLM 如何调用工具。

```python
class PhoneSearchInput(BaseModel):
    keyword: Optional[str]
    brand: Optional[str]
    tags: Optional[List[str]]
    min_price: Optional[float]
    max_price: Optional[float]
    ram: Optional[str]
    storage: Optional[str]
    limit: Optional[int]
```

#### 2. search_phones 函数

异步函数，执行实际的搜索逻辑：

```python
async def search_phones(...) -> str:
    # 构建搜索参数
    params = PhoneSearchParams(...)
    
    # 调用 PhoneService 搜索
    phones = await phone_service.search_phones(params)
    
    # 格式化结果返回给 AI
    return formatted_result
```

#### 3. LangChain Tool

使用 `Tool.from_function` 创建工具：

```python
search_phones = Tool.from_function(
    func=search_phones,
    name="search_phones",
    description="搜索手机数据库...",
    args_schema=PhoneSearchInput,
    coroutine=search_phones,  # 支持异步
)
```

### LLM 服务集成

`llm_service.py` 已更新以支持工具调用：

1. **绑定工具**：`bind_tools(tools)` 方法将工具绑定到 LLM
2. **工具调用流程**：
   - LLM 决定是否需要调用工具
   - 如果需要，返回工具调用请求
   - 系统执行工具并获取结果
   - 将结果返回给 LLM
   - LLM 基于工具结果生成最终回答

### 启动流程

在 `main.py` 的 `startup_event` 中：

```python
from app.tools import search_phones

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    
    # 绑定工具到 LLM 服务
    llm_service.bind_tools([search_phones])
```

## 使用示例

### 1. 添加示例数据

首先，运行数据填充脚本添加示例手机数据：

```bash
cd be
uv run python scripts/seed_phones.py
```

这会添加以下品牌的旗舰手机：
- 小米14 Pro
- 华为 Mate 60 Pro
- OPPO Find X7 Ultra
- vivo X100 Pro
- 一加12
- Redmi K70 Pro
- 荣耀 Magic6 Pro
- 真我 GT5 Pro

### 2. 用户查询示例

用户可以这样提问，AI 会自动调用工具：

#### 示例 1：关键词搜索
**用户**：推荐一款小米的手机

**AI 行为**：
1. 调用 `search_phones(brand="小米")`
2. 获取小米手机列表
3. 基于结果生成推荐回答

#### 示例 2：价格区间搜索
**用户**：5000元左右有什么好的手机？

**AI 行为**：
1. 调用 `search_phones(min_price=4500, max_price=5500)`
2. 获取该价格区间的手机
3. 分析并推荐

#### 示例 3：配置搜索
**用户**：我想要16GB内存512GB存储的手机

**AI 行为**：
1. 调用 `search_phones(ram="16GB", storage="512GB")`
2. 找到符合配置的手机
3. 提供选项

#### 示例 4：综合搜索
**用户**：5000以下的骁龙8 Gen3手机有哪些？

**AI 行为**：
1. 调用 `search_phones(keyword="骁龙8 Gen3", max_price=5000)`
2. 获取结果
3. 对比分析各款手机优缺点

#### 示例 5：标签搜索
**用户**：推荐一款拍照手机

**AI 行为**：
1. 调用 `search_phones(tags=["拍照手机"])`
2. 获取拍照手机列表
3. 重点介绍相机配置

## 数据库 Schema

### phones 集合结构

```javascript
{
  "_id": ObjectId,
  "brand": "小米",
  "model": "小米14 Pro",
  "description": "徕卡光学全焦段三摄...",
  "os": "HyperOS",
  "chipset": "骁龙8 Gen3",
  "display": "6.73英寸 3200×1440 AMOLED 120Hz",
  "battery": "4880mAh，120W有线快充...",
  "camera": "徕卡Summilux镜头...",
  "tags": ["旗舰机", "拍照手机", "游戏手机"],
  "features": ["徕卡影像", "骁龙8 Gen3", ...],
  "specs": {
    "weight": "223g",
    "thickness": "8.49mm",
    "5G": true,
    "NFC": true,
    "IR": true
  },
  "skus": [
    {
      "sku_id": "mi14pro_12_256_black",
      "name": "12GB+256GB 黑色",
      "ram": "12GB",
      "storage": "256GB",
      "color": "黑色",
      "price": 4999,
      "currency": "CNY",
      "availability": "有货",
      "extra": {}
    },
    ...
  ],
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### 索引

为提高查询性能，已创建以下索引：
- `brand`: 品牌索引
- `model`: 型号索引
- `tags`: 标签索引
- `updated_at`: 更新时间索引

## 扩展工具

### 添加更多手机数据

编辑 `scripts/seed_phones.py`，添加更多手机到 `SAMPLE_PHONES` 列表。

### 添加新的搜索条件

1. 在 `PhoneSearchInput` 中添加新参数
2. 在 `search_phones` 函数中处理新参数
3. 在 `PhoneService._build_search_query` 中添加查询逻辑

### 添加更多工具

1. 在 `app/tools/` 目录创建新工具文件
2. 定义工具的输入 schema 和执行函数
3. 在 `app/tools/__init__.py` 中导出
4. 在 `main.py` 中绑定新工具：

```python
from app.tools import search_phones, new_tool

llm_service.bind_tools([search_phones, new_tool])
```

## 调试和日志

### 启用详细日志

工具已配置完整的日志记录：

```python
logger.info("Searching phones with params: ...")
logger.error("Error searching phones: %s", e, exc_info=True)
```

启动服务器时会看到工具调用的详细信息：
- 工具绑定信息
- 搜索参数
- 搜索结果
- 错误信息

### 查看工具调用

LLM 服务会记录：
```
INFO: LLM requested tool calls: [...]
INFO: Executing tool: search_phones with args: {...}
INFO: Tool search_phones result: ...
```

## 常见问题

### Q: 为什么 AI 没有调用工具？

A: 可能的原因：
1. 用户问题不需要搜索手机数据
2. LLM 认为已有的信息足够回答
3. 工具描述不够清晰，LLM 没有意识到应该使用

解决方案：优化工具的 `description`，使其更明确。

### Q: 如何提高搜索准确性？

A: 
1. 确保数据库中的手机数据完整、准确
2. 为手机添加更多标签和关键词
3. 优化 `PhoneService._build_search_query` 的查询逻辑

### Q: 工具返回结果太多怎么办？

A: 
1. 减少默认的 `limit` 值（当前为 5）
2. 在工具描述中引导 AI 使用更精确的搜索条件
3. 优化搜索结果的排序逻辑

## 性能优化

1. **数据库索引**：确保关键字段有索引
2. **结果限制**：默认返回 5 条结果，最多 20 条
3. **缓存**：可以考虑添加 Redis 缓存热门查询
4. **异步执行**：所有数据库操作都是异步的

## 安全考虑

1. **参数验证**：使用 Pydantic 自动验证输入
2. **查询限制**：限制返回结果数量，防止数据库过载
3. **错误处理**：捕获异常并返回友好的错误信息
4. **注入防护**：使用 MongoDB 的参数化查询，防止注入攻击

## 总结

手机搜索工具为 AI Agent 提供了强大的数据查询能力，使其能够基于真实的数据库数据为用户提供准确的手机推荐。通过 LangChain 的工具系统，AI 可以智能地决定何时需要搜索数据，并将搜索结果融入自然的对话中。

