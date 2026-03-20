#!/bin/bash

# Daily Stock Analysis - OpenClaw Skill 入口
# 用法：./run.sh [股票代码] 或 ./run.sh --market-review

set -e

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/log"
ENV_FILE="$SCRIPT_DIR/.env"

# 确保目录存在
mkdir -p "$LOG_DIR"

# 日志文件
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 日志函数
log() {
    echo "[$TIMESTAMP] $*" | tee -a "$LOG_FILE"
}

# 加载环境变量
if [[ -f "$ENV_FILE" ]]; then
    log "📄 加载环境变量：$ENV_FILE"
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# 检查 Python 依赖
check_dependencies() {
    log "🔍 检查依赖..."
    
    if ! command -v python3 &> /dev/null; then
        log "❌ 错误：未找到 python3"
        exit 1
    fi
    
    # 检查关键依赖
    python3 -c "import akshare" 2>/dev/null || {
        log "⚠️  警告：akshare 未安装，A 股数据可能不可用"
    }
    
    python3 -c "import yfinance" 2>/dev/null || {
        log "⚠️  警告：yfinance 未安装，美股/港股数据可能不可用"
    }
    
    log "✅ 依赖检查完成"
}

# 解析参数
MARKET_REVIEW=false
MARKET_TYPE="all"
STOCK_CODES=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --market-review)
            MARKET_REVIEW=true
            shift
            ;;
        --market)
            MARKET_TYPE="$2"
            shift 2
            ;;
        *)
            STOCK_CODES="$1"
            shift
            ;;
    esac
done

# 主函数
main() {
    log "=== Daily Stock Analysis 开始 ==="
    
    # 检查依赖
    check_dependencies
    
    # 大盘复盘模式
    if [[ "$MARKET_REVIEW" == true ]]; then
        log "📊 执行大盘复盘 (市场：$MARKET_TYPE)"
        cd "$SCRIPT_DIR" && PYTHONPATH="$SCRIPT_DIR" python3 "$SCRIPT_DIR/src/core/market_review.py" \
            --market "$MARKET_TYPE" \
            2>&1 | tee -a "$LOG_FILE"
        
        log "=== 大盘复盘完成 ==="
        return
    fi
    
    # 单股/多股分析模式
    if [[ -n "$STOCK_CODES" ]]; then
        log "📈 分析股票：$STOCK_CODES"
        python3 "$SCRIPT_DIR/analyzer_service.py" \
            --stocks "$STOCK_CODES" \
            2>&1 | tee -a "$LOG_FILE"
        
        log "=== 股票分析完成 ==="
        return
    fi
    
    # 默认：分析配置中的自选股
    if [[ -n "$STOCK_LIST" ]]; then
        log "📈 分析自选股：$STOCK_LIST"
        python3 "$SCRIPT_DIR/main.py" \
            --stocks "$STOCK_LIST" \
            2>&1 | tee -a "$LOG_FILE"
        
        log "=== 自选股分析完成 ==="
        return
    fi
    
    # 无参数：显示帮助
    echo "用法：$0 [股票代码] 或 $0 --market-review"
    echo ""
    echo "示例:"
    echo "  $0 AAPL              # 分析单只股票"
    echo "  $0 AAPL,MSFT,GOOGL   # 分析多只股票"
    echo "  $0 --market-review   # 大盘复盘"
    echo "  $0 --market us       # 美股复盘"
    echo ""
    echo "环境变量:"
    echo "  STOCK_LIST           # 自选股代码列表"
    echo "  GEMINI_API_KEY       # Gemini API Key"
    echo "  TELEGRAM_BOT_TOKEN   # Telegram Bot Token"
}

# 执行
main "$@"
