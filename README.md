# AI Workflow Demo 🚀

> 一个基于workflow的RAG系统，使用Haystack2框架，使用FastAPI作为web框架，使用uv作为包管理器。

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com/)
[![Haystack](https://img.shields.io/badge/Haystack-2.0+-purple.svg)](https://haystack.deepset.ai/)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

## 📋 项目概述

本项目实现了一个基于workflow的RAG系统，使用Haystack2框架，使用FastAPI作为web框架，使用uv作为包管理器。

### ✨ 核心特性

- 🤖 **workflow** - 基于Haystack2框架的workflow系统,可自由编排


## 系统架构

主要这几个服务
api_server
- 通过fastapi实现的，接收创建workflow的请求，并返回workflow的id，查看workflow的运行状态，查看workflow的结果，删除workflow

MQ
- 使用rabbitmq作为消息队列，api_server和worker之间通过rabbitmq通信
- 解耦，并发控制，用户优先级控制，幂等

worker
- 单纯worker，业务无关，只做workflow的执行
- 订阅MQ，获取workflow的请求
- 执行workflow，并记录结果




## 快速开始

### 🔧 环境要求
- 🐍 **Python**: 3.12+
- 📦 **包管理器**: uv

### 📦 安装步骤

#### 1. 克隆项目
```bash
git clone git@github.com:kelvin-lc/ai-workflow.git
cd ai-workflow
```

#### 2. 安装依赖

```bash
uv sync
```

#### 3. 设置环境变量
```bash

```

### 🚀 启动服务

#### 方式一：IDE 启动
在 Cursor IDE 中直接运行，使用 `.vscode/launch.json` 配置启动

#### 方式二：命令行启动
```bash
uv run python src/main.py
```

#### 服务访问地址
- 🌐 **服务地址**: http://localhost:8001
- 📚 **API文档**: http://localhost:8001/docs
- 💚 **健康检查**: http://localhost:8001/ping

### 🚀 发送请求

#### 方式一：Web UI 界面
访问 [API文档界面]() 直接点击发送

#### 方式二：命令行请求
```bash

```

#### 示例响应

```

## 开发路线图

### 计划功能
- [ ] 支持用户选择不同模型
- [ ] Docker容器化
- [ ] 数据持久化层
- [ ] 性能、评估等框架
- [ ] 综合日志系统
- [ ] 指标监控和告警
- [ ] 单元和集成测试
- [ ] CI/CD流水线实现

## 贡献指南

[待实现：贡献指南]

## 许可证

[待实现：许可证信息]