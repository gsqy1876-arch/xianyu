#!/bin/bash
# ============================================
# Ubuntu Server Docker 一键安装脚本
# 支持 Ubuntu 20.04 / 22.04 / 24.04 LTS
# ============================================

set -e

echo "=========================================="
echo "  开始安装 Docker 环境..."
echo "=========================================="

# 1. 更新软件包索引
echo "[1/5] 更新软件包索引..."
sudo apt-get update

# 2. 安装必要的依赖
echo "[2/5] 安装必要依赖..."
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 3. 添加 Docker 官方 GPG 密钥
echo "[3/5] 添加 Docker GPG 密钥..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes

# 4. 设置 Docker 仓库
echo "[4/5] 配置 Docker 仓库..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. 安装 Docker
echo "[5/5] 安装 Docker Engine..."
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动 Docker 并设置开机自启
sudo systemctl enable docker
sudo systemctl start docker

# 将当前用户添加到 docker 组（无需 sudo 运行 docker）
sudo usermod -aG docker $USER

echo ""
echo "=========================================="
echo "  Docker 安装完成！"
echo "=========================================="
echo ""
docker --version
docker compose version
echo ""
echo "注意: 请重新登录以使用户组生效，或执行: newgrp docker"
