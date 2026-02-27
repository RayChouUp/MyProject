# FastAPI Demo

Python3 + FastAPI 学习项目。

## 1. 初始化环境

Windows PowerShell:

1) 创建虚拟环境（若不存在）

python -m venv .venv

2) 激活虚拟环境

.\.venv\Scripts\Activate.ps1

3) 安装依赖

pip install -r requirements.txt

## 2. 启动项目

uvicorn main:app --reload

默认访问地址：

- http://127.0.0.1:8000/
- Swagger 文档：http://127.0.0.1:8000/docs

## 3. 依赖管理

新增依赖后，可更新依赖文件：

pip freeze > requirements.txt
