#!/bin/bash

# MediaSync115 自动部署脚本
# 功能：自动提交代码到 Git 并部署 Docker 镜像

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 获取当前时间
BUILD_TIME=$(date '+%Y-%m-%d %H:%M:%S')
GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  MediaSync115 自动部署脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# ==================== 步骤 1: Git 提交 ====================
echo -e "${YELLOW}[1/4] 检查 Git 变更...${NC}"

# 检查是否有变更
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo -e "${GREEN}  没有检测到代码变更，跳过 Git 提交${NC}"
else
    echo -e "${YELLOW}  检测到代码变更，准备提交...${NC}"

    # 显示变更文件
    echo -e "${BLUE}  变更文件列表：${NC}"
    git status --short

    # 添加所有变更
    git add -A

    # 生成提交信息
    COMMIT_MSG="自动部署: ${BUILD_TIME}

变更内容：
$(git status --short)

构建时间: ${BUILD_TIME}
Git SHA: ${GIT_SHA}"

    # 提交代码
    git commit -m "$COMMIT_MSG"

    # 推送到 master 分支
    echo -e "${YELLOW}  推送到 master 分支...${NC}"
    git push origin master

    echo -e "${GREEN}  ✓ Git 提交完成${NC}"
fi

echo ""

# ==================== 步骤 2: 停止旧容器 ====================
echo -e "${YELLOW}[2/4] 停止旧容器...${NC}"

# 停止并删除旧容器（如果存在）
docker-compose -f docker-compose.single.yml down 2>/dev/null || true

# 清理旧镜像（可选，保留最近3个版本）
echo -e "${BLUE}  清理旧镜像...${NC}"
docker images wangsy1007/mediasync115 --format "{{.ID}} {{.CreatedAt}}" | \
    sort -k2,3 -r | \
    tail -n +4 | \
    awk '{print $1}' | \
    xargs -r docker rmi -f 2>/dev/null || true

echo -e "${GREEN}  ✓ 旧容器已清理${NC}"
echo ""

# ==================== 步骤 3: 构建镜像 ====================
echo -e "${YELLOW}[3/4] 构建 Docker 镜像...${NC}"

# 获取版本号（从 package.json 或默认）
VERSION=$(cat frontend/package.json | grep '"version"' | head -1 | sed 's/.*: "\(.*\)".*/\1/')
if [ -z "$VERSION" ]; then
    VERSION="1.0.0"
fi

# 构建镜像
docker build \
    --build-arg APP_BUILD_VERSION="$VERSION" \
    --build-arg APP_BUILD_TAG="latest" \
    --build-arg APP_BUILD_GIT_SHA="$GIT_SHA" \
    --build-arg APP_BUILD_TIME="$BUILD_TIME" \
    -t wangsy1007/mediasync115:latest \
    -t "wangsy1007/mediasync115:$VERSION" \
    -f Dockerfile \
    .

echo -e "${GREEN}  ✓ 镜像构建完成${NC}"
echo ""

# ==================== 步骤 4: 启动容器 ====================
echo -e "${YELLOW}[4/4] 启动容器...${NC}"

docker-compose -f docker-compose.single.yml up -d

# 等待服务启动
echo -e "${BLUE}  等待服务启动...${NC}"
sleep 5

# 检查健康状态
MAX_RETRIES=30
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:5173/healthz > /dev/null 2>&1; then
        echo -e "${GREEN}  ✓ 服务健康检查通过${NC}"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -e "${BLUE}  等待服务就绪... ($RETRY_COUNT/$MAX_RETRIES)${NC}"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}  ✗ 服务启动超时，请检查日志${NC}"
    echo -e "${YELLOW}  查看日志: docker logs mediasync115${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  部署成功！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}访问地址:${NC}"
echo -e "  应用: http://localhost:5173"
echo ""
echo -e "${BLUE}常用命令:${NC}"
echo -e "  查看日志: docker logs -f mediasync115"
echo -e "  停止服务: docker-compose -f docker-compose.single.yml down"
echo -e "  重启服务: docker-compose -f docker-compose.single.yml restart"
echo ""
echo -e "${BLUE}构建信息:${NC}"
echo -e "  版本: $VERSION"
echo -e "  Git SHA: $GIT_SHA"
echo -e "  构建时间: $BUILD_TIME"
echo ""
