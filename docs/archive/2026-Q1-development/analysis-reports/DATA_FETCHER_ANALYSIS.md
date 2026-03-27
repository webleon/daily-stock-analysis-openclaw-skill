# 原项目数据获取模块深度分析

**分析日期**: 2026-03-25  
**分析范围**: data_provider/ 目录（9342 行代码）  
**状态**: ✅ 分析完成

---

## 📊 数据源架构总览

### 数据源列表

| 数据源 | 优先级 | 特点 | 状态 |
|--------|--------|------|------|
| **TushareFetcher** | -1 (最高) | 需要 Token，数据质量高 | ✅ 完整实现 |
| **EfinanceFetcher** | 0 | 免费，稳定 | ✅ 完整实现 |
| **AkshareFetcher** | 1 | 免费，数据全 | ✅ 完整实现 |
| **BaostockFetcher** | 2 | 免费，历史数据 | ✅ 完整实现 |
| **PytdxFetcher** | 3 | 实时行情 | ✅ 完整实现 |
| **YFinanceFetcher** | 4 | 美股/港股 | ✅ 完整实现 |
| **LongbridgeFetcher** | 5 | 港股备用 | ✅ 完整实现 |
| **EastmoneyFetcher** | 6 | 补充数据 | ✅ 完整实现 |

### 核心设计模式

```
策略模式 (Strategy Pattern) + 责任链模式 (Chain of Responsibility)

┌─────────────────────────────────────────┐
│     DataFetcherManager                  │
│  - 管理多个数据源                        │
│  - 自动故障切换                          │
│  - 统一接口                             │
└─────────────┬───────────────────────────┘
              │
    ┌─────────▼─────────┐
    │  BaseFetcher      │
    │  (抽象基类)       │
    └─────────┬─────────┘
              │
    ┌─────────┼─────────┬─────────┬─────────┐
    │         │         │         │         │
┌───▼───┐ ┌──▼───┐ ┌──▼───┐ ┌──▼───┐ ┌──▼───┐
│Tushare│ │Efinance│ │Akshare│ │Baostock│ │...   │
└───────┘ └───────┘ └───────┘ └────────┘ └──────┘
```

---

## 🔑 核心机制分析

### 1. 防封禁策略

#### 1.1 速率限制（Rate Limiting）

```python
# AkShare 实现示例
class AkshareFetcher(BaseFetcher):
    def __init__(self):
        self._min_request_interval = 3.0  # 最小请求间隔（秒）
        self._max_request_interval = 8.0  # 最大请求间隔（秒）
        self._last_request_time: Optional[float] = None
    
    def _rate_limit(self):
        """速率限制 - 随机间隔"""
        if self._last_request_time is None:
            return
        
        elapsed = time.time() - self._last_request_time
        random_interval = random.uniform(
            self._min_request_interval,
            self._max_request_interval
        )
        
        if elapsed < random_interval:
            sleep_time = random_interval - elapsed
            logger.debug(f"[AkShare] 速率限制：休眠 {sleep_time:.2f} 秒")
            time.sleep(sleep_time)
        
        self._last_request_time = time.time()
```

**关键参数**:
- 最小间隔：3 秒
- 最大间隔：8 秒
- 随机化：防止被识别为爬虫

#### 1.2 Tushare 配额管理

```python
class TushareFetcher(BaseFetcher):
    def __init__(self, rate_limit_per_minute: int = 80):
        self.rate_limit_per_minute = rate_limit_per_minute
        self._call_count = 0  # 当前分钟内的调用次数
        self._minute_start: Optional[float] = None
    
    def _check_rate_limit(self):
        """检查并执行速率限制"""
        now = time.time()
        
        # 检查是否需要重置计数器（新的一分钟）
        if self._minute_start is None or (now - self._minute_start) >= 60:
            self._minute_start = now
            self._call_count = 0
            logger.debug("[Tushare] 重置调用计数器")
        
        # 检查是否超出配额
        if self._call_count >= self.rate_limit_per_minute:
            wait_time = 60 - (now - self._minute_start)
            if wait_time > 0:
                logger.warning(f"[Tushare] 超出配额，强制休眠 {wait_time:.2f} 秒")
                time.sleep(wait_time)
                self._minute_start = time.time()
                self._call_count = 0
        
        self._call_count += 1
```

**配额说明**（Tushare 免费用户）:
- 每分钟最多 80 次请求
- 每天最多 500 次请求
- 超过配额强制休眠

---

### 2. 重试策略（Retry Strategy）

#### 2.1 Tenacity 重试装饰器

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result,
    before_sleep_log,
)

class AkshareFetcher(BaseFetcher):
    @retry(
        stop=stop_after_attempt(5),  # 最多重试 5 次
        wait=wait_exponential(multiplier=2, min=3, max=60),  # 指数退避：3, 6, 12, 24, 48... 最大 60 秒
        retry=(
            retry_if_exception_type((ConnectionError, TimeoutError, requests.exceptions.RequestException)) |
            retry_if_result(lambda r: r is None or (hasattr(r, 'status_code') and r.status_code >= 500))
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _fetch_with_retry(self, url: str, params: Dict = None, headers: Dict = None, 
                          is_json: bool = True) -> Optional[requests.Response]:
        """带重试的 HTTP 请求"""
        self._rate_limit()
        
        # ... 实现细节
```

**重试策略详解**:
- **最大重试次数**: 5 次
- **退避策略**: 指数退避（3s → 6s → 12s → 24s → 48s，最大 60s）
- **触发条件**:
  - 连接错误（ConnectionError）
  - 超时（TimeoutError）
  - HTTP 5xx 错误
  - 返回 None
  - 收到 HTML 而非 JSON

#### 2.2 重试日志

```python
# 每次重试都会记录日志
before_sleep=before_sleep_log(logger, logging.WARNING)

# 日志示例:
# [WARNING] Retrying in 3 seconds...
# [WARNING] Retrying in 6 seconds...
# [WARNING] Retrying in 12 seconds...
```

---

### 3. 故障切换（Failover）

#### 3.1 数据源管理器

```python
class DataFetcherManager:
    """
    数据源策略管理器
    
    职责：
    1. 管理多个数据源（按优先级排序）
    2. 自动故障切换（Failover）
    3. 提供统一的数据获取接口
    
    切换策略：
    - 优先使用高优先级数据源
    - 失败后自动切换到下一个
    - 所有数据源都失败时抛出异常
    """
    
    def __init__(self, fetchers: Optional[List[BaseFetcher]] = None):
        self._fetchers: List[BaseFetcher] = []
        
        if fetchers:
            # 按优先级排序
            self._fetchers = sorted(fetchers, key=lambda f: f.priority)
        else:
            # 默认数据源将在首次使用时延迟加载
            self._init_default_fetchers()
    
    def get_daily_data(self, stock_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        获取日线数据（自动切换数据源）
        
        策略：
        1. 按优先级尝试每个数据源
        2. 捕获异常后自动切换到下一个
        3. 所有数据源失败时返回 None
        """
        errors = []
        
        for fetcher in self._fetchers:
            try:
                logger.info(f"[DataFetcherManager] 尝试使用 {fetcher.name} (Priority {fetcher.priority})")
                data = fetcher.get_daily_data(stock_code, start_date, end_date)
                
                if data is not None and not data.empty:
                    logger.info(f"[DataFetcherManager] {fetcher.name} 成功获取数据")
                    return data
                
            except Exception as e:
                error_msg = f"{fetcher.name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"[DataFetcherManager] {fetcher.name} 失败：{e}")
                continue
        
        # 所有数据源都失败
        logger.error(f"[DataFetcherManager] 所有数据源均失败：{'; '.join(errors)}")
        return None
```

#### 3.2 切换流程

```
获取数据请求
      │
      ▼
┌─────────────────┐
│ TushareFetcher  │ Priority -1
│ (最高优先级)     │
└────────┬────────┘
         │ 失败
         ▼
┌─────────────────┐
│ EfinanceFetcher │ Priority 0
└────────┬────────┘
         │ 失败
         ▼
┌─────────────────┐
│ AkshareFetcher  │ Priority 1
└────────┬────────┘
         │ 失败
         ▼
┌─────────────────┐
│ BaostockFetcher │ Priority 2
└────────┬────────┘
         │ 失败
         ▼
       ...
         │
         ▼
    返回 None (降级兜底)
```

---

### 4. 错误处理（Error Handling）

#### 4.1 异常分类

```python
class DataFetchError(Exception):
    """数据获取异常基类"""
    pass

class RateLimitError(DataFetchError):
    """速率限制异常"""
    pass

class DataFormatError(DataFetchError):
    """数据格式异常"""
    pass
```

#### 4.2 HTML 响应检测

```python
def _is_html_response(response: requests.Response) -> bool:
    """检测响应是否为 HTML（而非预期的 JSON）"""
    content_type = response.headers.get('Content-Type', '').lower()
    return 'text/html' in content_type

def _is_valid_json_response(response: requests.Response) -> bool:
    """检测响应是否为有效的 JSON"""
    try:
        response.json()
        return True
    except (json.JSONDecodeError, ValueError):
        return False

# 在重试策略中使用
if _is_html_response(response):
    logger.warning(f"[AkShare] 收到 HTML 响应：{response.status_code}")
    raise DataFetchError(f"收到 HTML 响应而非 JSON: {response.status_code}")
```

---

### 5. 缓存策略（Caching）

#### 5.1 基本面数据缓存

```python
class DataFetcherManager:
    def __init__(self):
        self._fundamental_cache: Dict[str, Dict[str, Any]] = {}
        self._fundamental_cache_lock = RLock()
        self._fundamental_timeout_worker_limit = 8
        self._fundamental_timeout_slots = BoundedSemaphore(self._fundamental_timeout_worker_limit)
    
    def _get_fundamental_cache_key(self, stock_code: str, budget_seconds: Optional[float] = None) -> str:
        """生成基本面缓存 key（包含预算分桶以避免低预算结果污染高预算请求）"""
        normalized_code = normalize_stock_code(stock_code)
        if budget_seconds is None:
            return f"{normalized_code}|budget=default"
        
        try:
            budget = max(0.0, float(budget_seconds))
        except (TypeError, ValueError):
            budget = 0.0
        
        # 100ms bucket to balance cache reuse and scenario isolation
        budget_bucket = int(round(budget * 10))
        return f"{normalized_code}|budget={budget_bucket}"
    
    def _prune_fundamental_cache(self, ttl_seconds: int, max_entries: int) -> None:
        """修剪过期和溢出的基本面缓存项"""
        with self._fundamental_cache_lock:
            if not self._fundamental_cache:
                return
            
            now_ts = time.time()
            if ttl_seconds > 0:
                # 删除过期项
                cache_items = list(self._fundamental_cache.items())
                expired_keys = [
                    key
                    for key, value in cache_items
                    if now_ts - float(value.get("ts", 0)) > ttl_seconds
                ]
                for key in expired_keys:
                    self._fundamental_cache.pop(key, None)
            
            # 限制最大条目数
            if len(self._fundamental_cache) > max_entries:
                # 删除最旧的项
                sorted_items = sorted(
                    self._fundamental_cache.items(),
                    key=lambda x: float(x[1].get("ts", 0))
                )
                for key, _ in sorted_items[:len(sorted_items) - max_entries]:
                    self._fundamental_cache.pop(key, None)
```

**缓存参数**:
- TTL: 可配置（默认根据预算分桶）
- 最大条目数：可配置
- 预算分桶：100ms 粒度

---

## 📈 性能优化策略

### 1. 并发控制

```python
# 使用信号量限制并发 worker 数量
self._fundamental_timeout_worker_limit = 8
self._fundamental_timeout_slots = BoundedSemaphore(self._fundamental_timeout_worker_limit)

# 使用时
with self._fundamental_timeout_slots:
    # 执行请求
    pass
```

### 2. 线程安全

```python
# 使用 RLock 保证线程安全
self._fundamental_cache_lock = RLock()

with self._fundamental_cache_lock:
    # 访问缓存
    pass
```

### 3. 延迟加载

```python
def _init_default_fetchers(self):
    """延迟加载默认数据源"""
    # 只在首次使用时初始化
    pass
```

---

## 🎯 关键最佳实践总结

### 1. 多层防护策略

| 层级 | 策略 | 目的 |
|------|------|------|
| **L1** | 速率限制 | 防止被封禁 |
| **L2** | 重试机制 | 应对临时故障 |
| **L3** | 故障切换 | 应对数据源故障 |
| **L4** | 缓存 | 减少请求次数 |
| **L5** | 降级兜底 | 保证系统可用性 |

### 2. 请求间隔策略

```python
# 最佳实践：随机间隔
random_interval = random.uniform(3.0, 8.0)
time.sleep(random_interval)

# 避免固定间隔被识别为爬虫
```

### 3. 重试策略

```python
# 最佳实践：指数退避
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=3, max=60),
)
def fetch():
    pass

# 重试间隔：3s → 6s → 12s → 24s → 48s (max 60s)
```

### 4. 故障切换策略

```python
# 最佳实践：优先级链
fetchers = sorted(fetchers, key=lambda f: f.priority)

for fetcher in fetchers:
    try:
        return fetcher.fetch()
    except Exception as e:
        logger.warning(f"{fetcher.name} failed: {e}")
        continue

return None  # 降级兜底
```

---

## 📋 新实现建议

基于原项目的最佳实践，新实现应该包含：

### 必需功能

1. ✅ **多数据源支持**（至少 3 个）
2. ✅ **优先级管理**（可配置）
3. ✅ **自动故障切换**
4. ✅ **指数退避重试**（5 次，3-60 秒）
5. ✅ **速率限制**（随机间隔 3-8 秒）
6. ✅ **HTML 响应检测**
7. ✅ **线程安全缓存**
8. ✅ **并发控制**（信号量）

### 可选功能

1. ⬜ **配额管理**（Tushare 风格）
2. ⬜ **预算分桶缓存**
3. ⬜ **详细日志记录**
4. ⬜ **指标监控**

---

**分析完成日期**: 2026-03-25  
**分析师**: 研究分析师 🔬  
**代码行数**: 9342 行  
**状态**: ✅ 分析完成，可以开始实现
