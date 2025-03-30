# ECharts 图表示例

这是一个使用 ECharts 创建图表的示例。

## 柱状图示例

```echarts
{
  "title": {
    "text": "月度销售数据"
  },
  "tooltip": {},
  "xAxis": {
    "data": ["一月", "二月", "三月", "四月", "五月", "六月"]
  },
  "yAxis": {},
  "series": [{
    "name": "销售额",
    "type": "bar",
    "data": [12, 19, 3, 5, 2, 3],
    "itemStyle": {
      "color": {
        "type": "linear",
        "x": 0,
        "y": 0,
        "x2": 0,
        "y2": 1,
        "colorStops": [{
          "offset": 0,
          "color": "rgba(255, 99, 132, 0.8)"
        }, {
          "offset": 1,
          "color": "rgba(255, 99, 132, 0.2)"
        }]
      }
    }
  }]
}
```

## 饼图示例

```echarts
{
  "title": {
    "text": "颜色分布"
  },
  "tooltip": {
    "trigger": "item",
    "formatter": "{a} <br/>{b}: {c} ({d}%)"
  },
  "series": [{
    "name": "颜色占比",
    "type": "pie",
    "radius": "60%",
    "data": [
      { "value": 12, "name": "红色" },
      { "value": 19, "name": "蓝色" },
      { "value": 3, "name": "黄色" },
      { "value": 5, "name": "绿色" },
      { "value": 2, "name": "紫色" },
      { "value": 3, "name": "橙色" }
    ],
    "emphasis": {
      "itemStyle": {
        "shadowBlur": 10,
        "shadowOffsetX": 0,
        "shadowColor": "rgba(0, 0, 0, 0.5)"
      }
    }
  }]
}
```

## 折线图示例

```echarts
{
  "title": {
    "text": "网站访问趋势"
  },
  "tooltip": {
    "trigger": "axis"
  },
  "xAxis": {
    "type": "category",
    "data": ["一月", "二月", "三月", "四月", "五月", "六月"]
  },
  "yAxis": {
    "type": "value"
  },
  "series": [{
    "name": "访问量",
    "type": "line",
    "smooth": true,
    "data": [65, 59, 80, 81, 56, 55],
    "lineStyle": {
      "color": "rgb(75, 192, 192)"
    },
    "areaStyle": {
      "color": {
        "type": "linear",
        "x": 0,
        "y": 0,
        "x2": 0,
        "y2": 1,
        "colorStops": [{
          "offset": 0,
          "color": "rgba(75, 192, 192, 0.4)"
        }, {
          "offset": 1,
          "color": "rgba(75, 192, 192, 0.1)"
        }]
      }
    }
  }]
}
```

## 散点图示例

```echarts
{
  "title": {
    "text": "身高体重分布"
  },
  "tooltip": {
    "trigger": "item",
    "formatter": "{c}"
  },
  "xAxis": {
    "name": "身高(cm)",
    "type": "value"
  },
  "yAxis": {
    "name": "体重(kg)",
    "type": "value"
  },
  "series": [{
    "type": "scatter",
    "data": [
      [160, 55],
      [165, 60],
      [170, 65],
      [175, 70],
      [180, 75],
      [185, 80]
    ],
    "symbolSize": 10,
    "itemStyle": {
      "color": "rgba(75, 192, 192, 0.8)"
    }
  }]
}
```

## 雷达图示例

```echarts
{
  "title": {
    "text": "技能评估"
  },
  "tooltip": {},
  "radar": {
    "indicator": [
      { "name": "编程", "max": 100 },
      { "name": "设计", "max": 100 },
      { "name": "分析", "max": 100 },
      { "name": "沟通", "max": 100 },
      { "name": "团队协作", "max": 100 }
    ]
  },
  "series": [{
    "name": "能力值",
    "type": "radar",
    "data": [{
      "value": [85, 70, 90, 80, 88],
      "name": "个人评分",
      "areaStyle": {
        "color": "rgba(75, 192, 192, 0.2)"
      },
      "lineStyle": {
        "color": "rgb(75, 192, 192)"
      },
      "itemStyle": {
        "color": "rgb(75, 192, 192)"
      }
    }]
  }]
}
``` 