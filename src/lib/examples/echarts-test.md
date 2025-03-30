# ECharts 测试

下面是一个简单的柱状图：

```echarts
{
  "title": {
    "text": "测试图表"
  },
  "tooltip": {},
  "xAxis": {
    "data": ["A", "B", "C", "D", "E"]
  },
  "yAxis": {},
  "series": [{
    "name": "数值",
    "type": "bar",
    "data": [10, 20, 30, 40, 50]
  }]
}
```

这应该会被正确地渲染为图表。 