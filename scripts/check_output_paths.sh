#!/bin/bash
#
# 输出路径规范检查脚本
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

PROJECT_DIR="/Users/webleon/.openclaw/workspace/skills/daily-stock-analysis-openclaw-skill"
OUTPUT_DIR="/Users/webleon/.openclaw/workspace/output"

echo "========================================"
echo "📁 输出路径规范检查"
echo "========================================"
echo ""

cd "$PROJECT_DIR"

ERRORS=0

# 检查根目录的备份文件
echo "🔍 检查项目根目录..."
if ls *.tar.gz 2>/dev/null; then
    echo -e "${RED}❌ 错误：备份文件在项目根目录${NC}"
    echo "   请移动到：output/backups/"
    for file in *.tar.gz; do
        mv "$file" "$OUTPUT_DIR/backups/" 2>/dev/null && echo "   ✅ 已移动 $file"
    done
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ 根目录干净${NC}"
fi

# 检查源码目录的数据文件
echo ""
echo "🔍 检查源码目录..."
if find core src data_provider -name "*.db" 2>/dev/null | grep -q .; then
    echo -e "${RED}❌ 错误：数据库文件在源码目录${NC}"
    find core src data_provider -name "*.db"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ 源码目录干净${NC}"
fi

# 检查输出目录结构
echo ""
echo "🔍 检查输出目录结构..."
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"/{daily-stock-analysis,backups,cache,accuracy,logs}
    echo -e "${GREEN}✅ 已创建输出目录结构${NC}"
fi

for subdir in daily-stock-analysis backups cache accuracy logs; do
    [ ! -d "$OUTPUT_DIR/$subdir" ] && mkdir -p "$OUTPUT_DIR/$subdir"
done

echo -e "${GREEN}✅ 输出目录结构完整${NC}"

# 检查备份文件位置
echo ""
echo "🔍 检查备份文件..."
if [ -d "$OUTPUT_DIR/backups" ]; then
    BACKUP_COUNT=$(ls -1 "$OUTPUT_DIR/backups"/*.tar.gz 2>/dev/null | wc -l)
    echo -e "${GREEN}✅ 备份文件位置正确：$BACKUP_COUNT 个文件${NC}"
fi

echo ""
echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 输出路径检查通过${NC}"
    echo "========================================"
    exit 0
else
    echo -e "${RED}❌ 发现 $ERRORS 个问题${NC}"
    echo "========================================"
    exit 1
fi
