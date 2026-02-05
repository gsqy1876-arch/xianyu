# 闲鱼自动回复系统 Docker 镜像
# 基于 Python 3.9-slim，适用于 Ubuntu Server 部署
# 注: login_helper.py 在本地运行，不需要在 Docker 中安装 Playwright

FROM python:3.9-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    LANG=C.UTF-8

# 设置工作目录
WORKDIR /app

# 安装系统依赖
# 更换 APT 为清华源以便在国内环境快速构建
# 兼容 Debian 11 (Bullseye) 和 Debian 12 (Bookworm) 的源文件格式
RUN if [ -f /etc/apt/sources.list ]; then \
        sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
        sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list; \
    fi && \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
        sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources; \
    fi && \
    apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    curl \
    ca-certificates \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 包（使用清华源，排除 Playwright）
# 增加 --trusted-host 以防证书问题，并先升级 pip
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn pip -U && \
    grep -v "playwright" requirements.txt > requirements_prod.txt && \
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements_prod.txt

# 复制项目代码
COPY . .

# 创建日志目录
RUN mkdir -p logs

# 健康检查
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('logs') else 1)"

# 启动命令
CMD ["python", "Start.py"]

