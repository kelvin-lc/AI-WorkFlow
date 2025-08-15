# AI WorkFlow 🚀

> 一个基于Haystack2的智能工作流管理系统，使用FastAPI构建RESTful API，支持工作流定义和任务管理。

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com/)
[![Haystack](https://img.shields.io/badge/Haystack-2.0+-purple.svg)](https://haystack.deepset.ai/)
[![uv](https://img.shields.io/badge/uv-package%20manager-yellow.svg)](https://github.com/astral-sh/uv)

## 📋 项目概述

AI WorkFlow 是一个现代化的工作流管理平台，专为AI应用场景设计。基于Haystack2框架构建，提供完整的工作流定义、任务管理和执行功能。

### ✨ 核心特性

- 🤖 **智能工作流** - 基于Haystack2的可视化工作流编排
- 🚀 **高性能API** - FastAPI构建的异步RESTful服务
- 📊 **任务管理** - 完整的任务生命周期管理
- 🔍 **高级过滤** - 支持多维度过滤、分页和排序
- 🛡️ **类型安全** - 基于Pydantic的数据验证
- 📱 **交互友好** - 自动生成Swagger文档
- 🔧 **灵活配置** - 支持多种数据库和环境配置

## 🏗️ 系统架构

```mermaid
graph TB
    %% 用户交互层
    subgraph "客户端层"
        UI[Web UI<br/>Swagger Docs]
        CLI[命令行工具<br/>curl/HTTPie]
        SDK[Python SDK<br/>第三方集成]
    end

    %% API网关层
    subgraph "API服务层"
        API[FastAPI Server<br/>端口: 8001]
        AUTH[认证中间件<br/>JWT/Token]
        CORS[CORS中间件<br/>跨域支持]
        LOG[日志中间件<br/>请求追踪]
    end

    %% 业务逻辑层
    subgraph "核心业务层"
        WF_DEF[AI Workflow 定义<br/>CRUD API]
        WF_JOB[AI Workflow 任务<br/>CRUD API]
        DEBUG[调试接口<br/>数据库管理]
    end

    %% 数据访问层
    subgraph "数据访问层"
        CRUD_DEF[Workflow Def<br/>CRUD操作]
        CRUD_JOB[Workflow Job<br/>CRUD操作]
        BASE[Base CRUD<br/>通用操作]
    end

    %% 数据存储层
    subgraph "数据存储层"
        DB[(SQLite/MySQL<br/>MatrixOne)]
        SCHEMA[数据模型<br/>SQLModel]
    end

    %% 未来扩展 - 分布式处理
    subgraph "未来规划 - 分布式处理"
        MQ[消息队列<br/>RabbitMQ/Redis]
        
        subgraph "并发执行集群"
            WORKER1[Workflow Worker 1<br/>Haystack2执行器]
            WORKER2[Workflow Worker 2<br/>Haystack2执行器]
        end
    end
    
    %% 未来扩展 - 监控体系
    subgraph "未来规划 - 可观测性"
        OTEL[OpenTelemetry<br/>链路追踪]
        PROMETHEUS[Prometheus<br/>指标收集]
        GRAFANA[Grafana<br/>可视化监控]
        JAEGER[Jaeger<br/>分布式追踪]
        ALERT[AlertManager<br/>告警系统]
    end

    %% 连接关系
    UI --> API
    CLI --> API
    SDK --> API
    
    API --> AUTH
    API --> CORS
    API --> LOG
    
    AUTH --> WF_DEF
    AUTH --> WF_JOB
    AUTH --> DEBUG
    
    WF_DEF --> CRUD_DEF
    WF_JOB --> CRUD_JOB
    DEBUG --> BASE
    
    CRUD_DEF --> SCHEMA
    CRUD_JOB --> SCHEMA
    BASE --> SCHEMA
    
    SCHEMA --> DB
    
    %% 未来连接（虚线）
    WF_JOB -.-> MQ
    MQ -.-> WORKER1
    MQ -.-> WORKER2
    
    %% 监控连接
    API -.-> OTEL
    WORKER1 -.-> OTEL
    WORKER2 -.-> OTEL
    OTEL -.-> JAEGER
    OTEL -.-> PROMETHEUS
    PROMETHEUS -.-> GRAFANA
    PROMETHEUS -.-> ALERT

    %% 样式
    classDef primary fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef secondary fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef storage fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef future fill:#fff3e0,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5
    classDef monitor fill:#fce4ec,stroke:#880e4f,stroke-width:2px,stroke-dasharray: 5 5

    class UI,CLI,SDK primary
    class API,AUTH,CORS,LOG secondary
    class WF_DEF,WF_JOB,DEBUG,CRUD_DEF,CRUD_JOB,BASE secondary
    class DB,SCHEMA storage
    class MQ,WORKER1,WORKER2 future
    class OTEL,PROMETHEUS,GRAFANA,JAEGER,ALERT monitor
```

### 主要术语

- ai_workflow_def: 定义AI pipeline，相当于Class
- ai_workflow_job: 执行AI pipeline，相当于Instance

### 🏢 架构组件说明

#### 当前已实现
- **API服务层**: FastAPI应用，提供异步HTTP服务
- **业务逻辑层**: 工作流定义和任务管理的核心API
- **数据访问层**: ORM操作
- **数据存储层**: 支持Postgres、Elasticsearch、MatrixOne等数据库

#### 未来规划 - 分布式处理
- **消息队列**: 使用RabbitMQ/Redis实现异步任务分发
- **并发执行集群**: 多个Workflow Worker并行处理，支持水平扩展
- **负载均衡**: 消息队列自动分发任务到可用的Worker节点

#### 未来规划 - 可观测性体系
- **OpenTelemetry**: 统一的链路追踪和指标收集标准
- **Jaeger**: 分布式追踪系统，跟踪请求在微服务间的调用链路
- **Prometheus**: 时序数据库，收集系统和业务指标
- **Grafana**: 可视化仪表盘，实时监控系统状态
- **AlertManager**: 智能告警系统，基于规则进行异常通知

## 🚀 快速开始

### 🔧 环境要求

- 🐍 **Python**: 3.12+
- 📦 **包管理器**: [uv](https://github.com/astral-sh/uv)
- 💾 **数据库**: SQLite (默认) / MySQL / MatrixOne

### 📦 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/your-org/ai-workflow.git
cd ai-workflow
```

#### 2. 安装依赖
```bash
# 安装uv (如果未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步依赖
uv sync
```

#### 3. 配置环境变量
```bash
# 复制环境配置文件
cp .env.example .env

# 编辑配置 (可选)
# DATABASE_URI=sqlite+aiosqlite:///app.db  # SQLite (默认)
# DATABASE_URI=mysql+asyncmy://user:pass@host:port/db  # MySQL
# LOG_LEVEL=INFO
# SECRET_KEY=your-secret-key
```

### 🚀 启动服务

#### 方式一：IDE 启动 (推荐)
在 VS Code/Cursor 中使用调试配置启动：
- 按 `F5` 或选择 "Python Debugger: FastAPI"
- 自动启动并支持断点调试

#### 方式二：命令行启动
```bash
# 开发模式 (热重载)
uv run uvicorn src.api_server.main:app --reload --host 0.0.0.0 --port 8001

# 生产模式
uv run uvicorn src.api_server.main:app --host 0.0.0.0 --port 8001 --workers 4
```

#### 🌐 服务访问地址
- **API服务**: http://localhost:8001
- **交互文档**: http://localhost:8001/docs
- **健康检查**: http://localhost:8001/health
- **Ping检测**: http://localhost:8001/ping

## 📖 API 使用指南

### 🔍 核心接口

#### AI Workflow 定义管理
```bash
# 创建工作流定义
POST /api/v1/ai_workflow_def
{
  "name_str": "智能问答工作流",
  "description_text": "基于RAG的智能问答系统",
  "hs_yaml_content": "# Haystack YAML配置...",
  "version_str": "1.0.0",
  "is_active_flag": true,
  "tags_str": "RAG,问答,AI"
}

# 获取工作流列表 (支持高级过滤)
GET /api/v1/ai_workflow_def/list?limit=20&offset=0&order_by=updated_at_time&order=desc&is_active=true&name=智能

# 获取单个工作流
GET /api/v1/ai_workflow_def/{workflow_def_id}
```

#### AI Workflow 任务管理
```bash
# 创建任务
POST /api/v1/ai_workflow_job
{
  "ai_workflow_def_id": "workflow-uuid",
  "job_name_str": "问答任务001",
  "trigger_data_json": {"query": "什么是人工智能？", "top_k": 5},
  "status_str": "pending"
}

# 获取任务列表 (支持多维度过滤)
GET /api/v1/ai_workflow_job?status=completed&limit=10&created_after=2024-01-01T00:00:00

# 获取单个任务
GET /api/v1/ai_workflow_job/{job_id}
```

### 🔧 高级过滤功能

支持以下过滤参数：

**通用过滤**:
- `limit`: 返回数量 (1-1000, 默认100)
- `offset`: 偏移量 (默认0)
- `order_by`: 排序字段
- `order`: 排序方向 (asc/desc)

**时间过滤**:
- `created_after/before`: 创建时间范围
- `updated_after/before`: 更新时间范围
- `started_after/before`: 开始时间范围 (仅任务)
- `completed_after/before`: 完成时间范围 (仅任务)

**业务过滤**:
- 工作流定义: `name`, `version`, `tags`, `is_active`
- 工作流任务: `job_name`, `status`, `ai_workflow_def_id`

### 🛠️ 调试接口 (开发环境)

```bash
# 创建数据库表
POST /api/v1/debug/create-tables

# 删除数据库表 (危险操作)
DELETE /api/v1/debug/drop-tables

# 查看表结构信息
GET /api/v1/debug/table-info

# 数据库连接测试
GET /api/v1/debug/health-check
```

## 📁 项目结构

```
AI-WorkFlow/
├── src/
│   ├── api_server/          # FastAPI应用主目录
│   │   ├── api/            # API路由层
│   │   │   ├── api_v1/     # API v1版本
│   │   │   │   ├── ai_workflow_def.py    # 工作流定义API
│   │   │   │   ├── ai_workflow_job.py    # 工作流任务API
│   │   │   │   └── debug.py              # 调试接口
│   │   │   ├── deps.py     # 依赖注入
│   │   │   └── errors.py   # 异常处理
│   │   ├── crud/           # 数据访问层
│   │   │   ├── crud_ai_workflow_def.py
│   │   │   ├── crud_ai_workflow_job.py
│   │   │   └── base.py     # 基础CRUD
│   │   ├── models/         # 数据模型
│   │   │   ├── ai_workflow_def.py
│   │   │   ├── ai_workflow_job.py
│   │   │   └── base.py     # 基础模型
│   │   ├── utils/          # 工具模块
│   │   │   ├── logging_config.py
│   │   │   └── middleware.py
│   │   ├── config.py       # 配置管理
│   │   └── main.py         # 应用入口
│   └── worker/             # 工作流执行器 (规划中)
├── tests/                  # 测试代码
├── .vscode/               # VS Code配置
├── pyproject.toml         # 项目配置
└── README.md              # 项目文档
```

## 🧪 开发和测试

### 🔍 代码风格
```bash
# 代码格式化
uv run black src/
uv run isort src/

# 类型检查
uv run mypy src/

# 代码质量检查
uv run flake8 src/
```

### 🧪 运行测试
```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/test_api.py

# 生成覆盖率报告
uv run pytest --cov=src --cov-report=html
```

## 📈 开发路线图

### ✅ 已完成功能
- [x] 基础FastAPI应用架构
- [x] AI工作流定义CRUD接口
- [x] AI工作流任务CRUD接口
- [x] 高级过滤、分页、排序功能
- [x] 数据库抽象层和模型设计
- [x] 异常处理和日志记录
- [x] API文档自动生成
- [x] 调试和开发工具接口

### 🚧 进行中
- [ ] 用户认证和权限管理
- [ ] Haystack2工作流执行引擎集成
- [ ] 消息队列异步任务处理

### 📋 计划功能
- [ ] 工作流可视化编辑器
- [ ] 实时执行状态监控
- [ ] 工作流模板市场
- [ ] 多租户支持
- [ ] Docker容器化部署
- [ ] K8s集群部署支持
- [ ] 分布式Worker集群
- [ ] 可观测性体系集成
  - [ ] OpenTelemetry链路追踪
  - [ ] Prometheus指标监控
  - [ ] Grafana可视化仪表盘
  - [ ] Jaeger分布式追踪
  - [ ] AlertManager智能告警
- [ ] 自动化测试覆盖
- [ ] CI/CD流水线

## 🤝 贡献指南

我们欢迎任何形式的贡献！

### 🔧 开发流程
1. Fork 本项目
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送分支: `git push origin feature/amazing-feature`
5. 提交 Pull Request

### 📝 代码规范
- 遵循 PEP 8 代码规范
- 使用类型注解
- 编写完善的文档字符串
- 确保测试覆盖率 > 80%

## 📄 许可证

本项目采用 [Apache 2.0](LICENSE) 许可证。

## 📧 联系我们

- **Issues**: [GitHub Issues](https://github.com/your-org/ai-workflow/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/ai-workflow/discussions)
- **Email**: your-email@example.com

---

⭐ 如果这个项目对你有帮助，请给我们一个 Star！