# 个人知识文档问答系统

一个极简的**本地知识节点管理系统**：单文件后端 + 单文件前端 + SQLite 数据库，零配置一键启动。项目名个人知识文档问答系统，为个人知识整理与灵感沉淀而设计。该系统可接入任意大模型。

支持：

- 📝 **知识节点管理**（增删改查、分类、标签、搜索）
- 🧠 **智能问答**（召回相关节点 + 大模型生成推理链回答）
- 💬 **自由对话**（多会话管理，支持上下文历史）
- 📥 **文档导入**（支持 TXT、DOCX、Markdown、PDF 文件）

***

## 🛠 技术栈

- **后端**：Python 3.10+ · FastAPI · SQLAlchemy 2.x · Pydantic 2
- **语义向量**：sentence-transformers（中文 `bge-small-zh-v1.5`，首次使用会自动下载约 100MB）
- **大模型**：兼容 **OpenAI 协议**（可接入 OpenAI / DeepSeek / 通义千问 / Qwen 等），也兼容本地 **Ollama**
- **数据库**：SQLite（本地文件 `knowledge.db`，首次运行自动创建）
- **前端**：单文件 `index.html` · 原生 JavaScript · 极简 CSS（无任何构建工具）

***

## 📁 项目结构

```
个性化知识神经网络/
├── main.py              # 后端全部逻辑（单文件）
├── requirements.txt     # 依赖列表
├── README.md            # 说明文档
├── Dockerfile           # Docker 镜像构建文件
├── .dockerignore        # Docker 构建忽略文件
├── .gitignore           # 忽略规则（数据库/缓存/大模型缓存等）
├── run_tests.py         # 测试验证脚本
├── static/
│   └── index.html       # 前端页面（单文件，四个 Tab）
├── tests/               # 单元测试目录
│   ├── __init__.py
│   ├── test_file_parsing.py    # 文件解析测试
│   ├── test_embedding.py       # 向量生成测试
│   ├── test_database.py        # 数据库操作测试
│   ├── test_import.py          # 导入功能测试
│   ├── test_api.py             # API接口测试
│   └── test_data/
│       ├── test.txt            # 测试用纯文本文件
│       └── test.md             # 测试用Markdown文件
├── knowledge.db         # 首次运行后自动生成（不会被提交到 Git）
└── settings.json        # 首次配置后自动生成（不会被提交到 Git，里面含 API Key）
```

> 注：`knowledge.db`、`settings.json`、`.hf_models/`、`__pycache__/`、`debug_*.py`、`test_*.py` 已在 `.gitignore` 中被忽略，不会被上传到 GitHub。

***

## 🚀 启动步骤

### 方式一：直接运行（推荐）

#### 1. 克隆 / 下载项目

```bash
git clone https://github.com/你的用户名/binruan-doc-mind.git
cd binruan-doc-mind
```

或直接在 GitHub 上点 **Download ZIP**，解压到本地。

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

首次安装可能较慢（`sentence-transformers` 会连带安装 `torch`）。

#### 3. 启动服务

```bash
python main.py
```

终端会打印：

```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

首次启动会在当前目录自动创建：

- `knowledge.db`（数据库，含节点表 + 会话表 + 消息表）
- 首次使用**智能问答**时，会下载 `bge-small-zh-v1.5` 模型（约 100MB，后续会缓存到本地）

### 方式二：Docker 部署

#### 1. 构建 Docker 镜像

```bash
docker build -t siyuan-knowledge-network .
```

#### 2. 运行容器

**Windows PowerShell:**
```powershell
docker run -d -p 8000:8000 -v ${PWD}\data:/app/data -v ${PWD}\models:/app/.hf_models siyuan-knowledge-network
```

**Linux/Mac:**
```bash
docker run -d -p 8000:8000 -v $(pwd)/data:/app/data -v $(pwd)/models:/app/.hf_models siyuan-knowledge-network
```

**参数说明：**
- `-d`: 后台运行容器
- `-p 8000:8000`: 将容器端口8000映射到宿主机端口8000
- `-v ${PWD}\data:/app/data`: 将数据库文件持久化到宿主机的 `data` 目录
- `-v ${PWD}\models:/app/.hf_models`: 将向量模型缓存持久化到宿主机的 `models` 目录

#### 3. 访问应用

打开浏览器访问：`http://localhost:8000`

#### 4. 常用 Docker 命令

```bash
# 查看运行状态
docker ps

# 查看日志
docker logs -f <容器ID或容器名称>

# 停止容器
docker stop <容器ID或容器名称>

# 删除容器
docker rm <容器ID或容器名称>

# 重新构建镜像
docker build -t siyuan-knowledge-network .
```

**注意事项：**
- 首次运行会下载向量模型（约100MB），可能需要几分钟
- 如果模型下载失败，请检查网络连接或手动下载模型到 `models` 目录
- 数据库和模型缓存会持久化到宿主机，删除容器不会丢失数据

***

## 🌐 访问地址

| 页面                 | 地址                            |
| ------------------ | ----------------------------- |
| 前端主页面（四个 Tab）      | <http://127.0.0.1:8000/>      |
| FastAPI Swagger 文档 | <http://127.0.0.1:8000/docs>  |
| FastAPI Redoc 文档   | <http://127.0.0.1:8000/redoc> |

***

## 🧩 四个 Tab 的作用

### 📝 列表管理

- 新建/编辑/删除节点；标题、内容、分类、标签
- 顶部关键字实时搜索；按分类下拉过滤
- 数据持久化到本地 SQLite

### 🧠 智能问答

- 输入问题，系统先召回语义最相关的若干节点
- 然后把「问题 + 参考节点内容」发给你配置的大模型，生成带推理链的回答
- 右侧显示参考节点与相似度；下方显示 AI 画出的逻辑链路

### 💬 自由对话

- 左侧可新建 / 切换 / 删除对话
- 右侧是纯聊天界面，支持多轮上下文（默认取最近 20 条作为历史）
- 完全独立于知识库，只与大模型对话

### 📥 文档导入

- 支持导入 TXT、DOCX、Markdown、PDF 文件
- 自动解析文档内容，提取候选知识节点
- 预览候选节点后，确认写入知识库

***

## 🔑 配置大模型（LLM）

打开页面后，点击右上角 **「⚙ 大模型配置」**（或在智能问答 / 自由对话页首次触发时会提示）填写：

| 字段              | 含义                                                                                    |
| --------------- | ------------------------------------------------------------------------------------- |
| **Base URL**    | 大模型 API 地址。OpenAI 协议写 `https://api.openai.com/v1`；Ollama 本地写 `http://localhost:11434` |
| **API Key**     | 对应服务商的 Key。Ollama 可留空                                                                 |
| **Model Name**  | 模型名，如 `gpt-4o-mini`、`deepseek-chat`、`qwen-plus`、Ollama 的 `llama3:8b` 等                |
| **Temperature** | 0\~1 之间；越大越发散，默认 0.2                                                                  |
| **Timeout**     | 请求超时秒数，默认 30                                                                          |

配置保存在本地 `settings.json`（**不会被提交到 Git**）。

> **未配置 LLM 会发生什么？** 智能问答与自由对话会友好提示"请先配置大模型"；列表管理与文档导入仍可正常使用。

***

## 📡 RESTful API 列表

| 方法       | 路径                                        | 说明                         |
| -------- | ----------------------------------------- | -------------------------- |
| `POST`   | `/api/nodes`                              | 新建节点                       |
| `GET`    | `/api/nodes?keyword=xxx&category=xxx`     | 查询节点列表                     |
| `GET`    | `/api/nodes/{id}`                         | 获取单个节点详情                   |
| `PUT`    | `/api/nodes/{id}`                         | 更新节点（会同步更新向量）              |
| `DELETE` | `/api/nodes/{id}`                         | 删除节点                       |
| `GET`    | `/api/categories`                         | 获取所有分类（去重）                 |
| `GET`    | `/api/nodes/all-relations?threshold=0.60` | 返回节点两两相似度关系（图谱用）           |
| `POST`   | `/api/nodes/batch-embed`                  | 为所有缺失向量的节点批量编码             |
| `POST`   | `/api/qa`                                 | 智能问答（带参考节点 + 推理链）          |
| `GET`    | `/api/freechat/sessions`                  | 获取自由对话会话列表                 |
| `POST`   | `/api/freechat/sessions`                  | 新建自由对话会话                   |
| `DELETE` | `/api/freechat/sessions/{id}`             | 删除会话（含所有消息）                |
| `GET`    | `/api/freechat/sessions/{id}/messages`    | 拉取该会话的消息历史                 |
| `POST`   | `/api/freechat/sessions/{id}/messages`    | 发一条消息，返回 AI 回复（会附带最近历史上下文） |
| `GET`    | `/api/settings/llm`                       | 获取当前 LLM 配置（Key 不回显）       |
| `PUT`    | `/api/settings/llm`                       | 更新 LLM 配置                  |

> 更详细的请求/响应示例可在启动后打开 <http://127.0.0.1:8000/docs>（Swagger 交互文档）查看与调试。

***

## 💡 特色

- ✅ **零配置**：数据库、表结构自动创建，无需手动执行 SQL
- ✅ **极简结构**：核心文件只有 `main.py` + `static/index.html` + `requirements.txt`
- ✅ **无前端构建**：原生 JS，双击即运行
- ✅ **可插拔大模型**：OpenAI 协议 / Ollama 本地都支持
- ✅ **隐私本地化**：所有数据与配置都在本地，不会上传到任何服务器
- ✅ **文档导入**：支持 TXT、DOCX、Markdown、PDF 多种格式

***

## ⚠️ 注意

- 本项目设计为**本地个人使用**，未引入任何认证/鉴权，请勿直接暴露到公网
- 停止服务：在终端按 `Ctrl + C` 即可
- 清空所有数据：直接删除 `knowledge.db` 文件，下次启动会重建空数据库
- `settings.json` 中可能含有真实 API Key，**已在** **`.gitignore`** **中被忽略**，但在本机仍要妥善保管
- 首次使用智能问答会下载 `bge-small-zh-v1.5`（约 100MB），请保持网络可用

***

## 🧪 单元测试

项目包含完整的单元测试，覆盖主要功能模块。

### 测试覆盖范围

| 测试模块 | 测试内容 | 测试用例数 |
|---------|---------|-----------|
| `test_file_parsing.py` | TXT、Markdown、PDF 文件解析 | 6个 |
| `test_embedding.py` | 向量生成、批量处理、空文本处理 | 8个 |
| `test_database.py` | CRUD操作、默认值、向量存储 | 7个 |
| `test_import.py` | 导入会话管理、候选节点处理 | 4个 |
| `test_api.py` | REST API接口测试 | 11个 |
| **总计** | | **36个** |

### 运行测试

#### 方式一：使用 unittest（推荐）

```bash
# 运行所有测试
python -m unittest discover -s tests -v

# 运行特定测试文件
python -m unittest tests.test_database -v
python -m unittest tests.test_file_parsing -v
```

#### 方式二：使用 pytest

```bash
# 安装 pytest
pip install pytest

# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_database.py -v
```

### 测试文件结构

```
tests/
├── __init__.py
├── test_data/
│   ├── test.txt      # 测试用纯文本文件
│   └── test.md       # 测试用Markdown文件
├── test_file_parsing.py    # 文件解析测试
├── test_embedding.py       # 向量生成测试
├── test_database.py        # 数据库操作测试
├── test_import.py          # 导入功能测试
└── test_api.py             # API接口测试
```

### 测试验证脚本

项目包含 `run_tests.py` 脚本，用于验证测试代码的完整性：

```bash
python run_tests.py
```

该脚本会检查：
- 所有测试文件是否存在
- 测试代码语法是否正确
- 测试用例数量统计
- 测试覆盖范围

### 注意事项

- 向量测试首次运行会下载向量模型（约100MB），建议提前下载
- API测试使用内存数据库，不会影响实际数据
- PDF测试需要安装pypdf依赖
- 部分测试需要配置大模型API才能完整运行



