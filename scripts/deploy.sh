#!/bin/bash
# ============================================
# 闲鱼自动回复系统 Docker 部署脚本
# ============================================

set -e

echo "=========================================="
echo "  闲鱼自动回复系统 - Docker 部署"
echo "=========================================="

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装，请先运行 install_docker.sh"
    exit 1
fi

# 检查配置文件
if [ ! -f "global_config.yml" ]; then
    echo "警告: global_config.yml 不存在"
    echo "请确保已正确配置 Cookie 信息"
    exit 1
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "提示: 从 .env.example 创建 .env 文件..."
        cp .env.example .env
        echo "请编辑 .env 文件配置必要的环境变量"
    fi
fi

# 创建日志目录
mkdir -p logs

echo ""
echo "[1/2] 构建 Docker 镜像..."
docker compose build

echo ""
echo "[2/2] 启动容器..."
docker compose up -d

echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "常用命令:"
echo "  查看日志: docker compose logs -f xianyu-app"
echo "  停止服务: docker compose down"
echo "  重启服务: docker compose restart"
echo ""
docker compose ps
