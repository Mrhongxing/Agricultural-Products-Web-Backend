# 使用官方 Python 运行时作为基础镜像
FROM python:3.11-alpine

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装系统依赖和 Python 包
RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev && \
    apk add --no-cache --virtual .build-deps build-base mariadb-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

# 复制应用代码
COPY . .

# 创建 images 目录（如果不存在）
RUN mkdir -p images

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "-m", "uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]