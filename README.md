### pyfolio

#### 介绍

pyfolio原本是zipline的绩效分析模块，有大名鼎鼎的量化平台quantopian开发并开源出来。但是，quantopian倒闭之后，pyfolio慢慢缺乏维护，已经很久没有更新了，在使用过程中经常会碰到各种小bug，另一个原因是pyfolio做绩效分析的效率并不高，数据非常多的时候处理速度会比较慢，还有pyfolio对notebook支持比较好，对于其他的开发环境支持较弱，本模块尝试在pyfolio的基础上，结合其他绩效分析模块的优点，做出一个更好用的绩效分析模块，供大家使用。

本模块主要基于python语言，使用numpy、pandas、scipy、plotly、dash、flask和pyqt6等对原来的pyfolio进行改进优化。


#### 安装教程


1.  pip install git+https://gitee.com/yunjinqi/pyfolio.git
2.  如果第一种方法失败，可以手动进入下载包的工作目录，然后git clone，或者直接下载下来文件，然后放到包的工作目录.
```
cd C:\ProgramData\Anaconda3\Lib\site-packages
git clone https://gitee.com/yunjinqi/pyfolio.git
```


#### 使用说明

```python

import pandas as pd
import pyfolio as pf
import os
import warnings
warnings.filterwarnings("ignore")
# 加载数据
pf_path = os.path.dirname(pf.__file__)
df = pd.read_csv(pf_path+"/datas/基准收益率和日收益率序列.csv",index_col = 0)
df.index = pd.to_datetime(df.index)
positions = pd.read_csv(pf_path+"/datas/positions.csv",index_col = 0)
positions.index = pd.to_datetime(positions.index)
pf.create_full_tear_sheet(df['returns'],benchmark_rets=df['benchmark_rets'],positions= positions)

```

#### 绩效分析结果展示

##### 绩效指标分析

![绩效统计指标1](https://gitee.com/yunjinqi/pyfolio/tree/master/img/image-20211218133956274.png)

![绩效统计指标2](https://gitee.com/yunjinqi/pyfolio/tree/master/img/image-20211218134015808.png)








