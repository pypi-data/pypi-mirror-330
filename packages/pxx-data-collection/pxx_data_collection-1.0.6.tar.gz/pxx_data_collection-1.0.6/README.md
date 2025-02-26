# pxx-data-collection
拼夕夕商家后台数据采集工具

![Version](https://img.shields.io/badge/Version-v1.0.4-green)

## 安装
```bash
pip install pxx-data-collection
```

## 使用方法
### 连接浏览器
```python
from PxxDataCollection import Collector

collector = Collector()
collector.connect_browser(port=9527)
collector.login(username='your_username', password='your_password')
```

### 获取商家后台数据
```python
# 获取 商家后台-数据中心-流量看板概览 数据
result = collector.mms.data_center.get__flow_plate__overview(date='2025-01-18')

# ... 其他数据获取方法与上面类似
```

### 获取推广中心数据
```python
# 获取 推广中心-账户管理-财务流水日账单 数据
result = collector.marketing.account.get__report__daily(
    begin_date='2025-01-16', end_date='2025-01-16'
)

# ... 其他数据获取方法与上面类似
```