# qianchuan-data-collection
巨量千川数据采集工具

## 安装
```bash
pip install qianchuan-data-collection
```

## 使用方法
### 连接浏览器
```python
from QianchuanDataCollection import Collector

collector = Collector()
collector.connect_browser(port=9527)
```

### 获取全域推广数据
```python
# 获取全域推广-推商品 视频表格数据
r = collector.data.site_promotion.get__push_product__material__detail(
    begin_date='2025-01-20', end_date='2025-01-20'
)
```

## 支持采集的数据
- 数据
    - 全域推广数据
        - 推直播-概览
        - 推直播-素材-视频
        - 推商品-概览
        - 推商品-素材-视频