### pyfolio

#### 介绍

pyfolio原本是zipline的绩效分析模块，由大名鼎鼎的量化平台quantopian开发并开源出来。但是，quantopian倒闭之后，pyfolio慢慢缺乏维护，已经很久没有更新了，在使用过程中经常会碰到各种小bug，另一个原因是pyfolio做绩效分析的效率并不高，数据非常多的时候处理速度会比较慢，还有pyfolio对notebook支持比较好，对于其他的开发环境支持较弱，本模块尝试在pyfolio的基础上，结合其他绩效分析模块的优点，做出一个更好用的绩效分析模块，供大家使用。

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

#### 一些付费文章

1. [如何使用analyzer及创建新的analyzer(4)---策略绩效评价模块pyfolio的使用](https://yunjinqi.blog.csdn.net/article/details/110842730)
2. [【答读者问37】如何使用pyfolio对比基准收益率和策略收益率？](https://yunjinqi.blog.csdn.net/article/details/122012247)
3. [使用flask给pyfolio做一个界面,可以在spyder\pycharm\vscode中呈现策略绩效分析结果(2021-10-29更新)](https://yunjinqi.blog.csdn.net/article/details/121025639)




#### 绩效分析结果展示

##### 绩效指标分析

![绩效统计指标1](https://img-blog.csdnimg.cn/aa15defc2c11403f9590c5cca2ed2e83.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

![绩效统计指标2](https://img-blog.csdnimg.cn/77c50796bc704f35935e8c8703935cac.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

![累计收益率](https://img-blog.csdnimg.cn/0e09ad44096c4336a0ef750aa4d4e403.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![累计收益率在对数坐标轴上](https://img-blog.csdnimg.cn/51a0010aa2cb406e8edd875ebfed753e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![累计收益率的波动率](https://img-blog.csdnimg.cn/51a0010aa2cb406e8edd875ebfed753e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![日收益率](https://img-blog.csdnimg.cn/18710ef4d9964cc29c8f1b34d9deed94.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![滚动夏普率](https://img-blog.csdnimg.cn/cd1ffa71138f4fe08793637f6b726676.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![滚动贝塔值](https://img-blog.csdnimg.cn/18710ef4d9964cc29c8f1b34d9deed94.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![滚动波动率](https://img-blog.csdnimg.cn/cd1ffa71138f4fe08793637f6b726676.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![最大回撤](https://img-blog.csdnimg.cn/b208313bfb614b46ac0a17560383b167.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![5次最大回撤](https://img-blog.csdnimg.cn/b208313bfb614b46ac0a17560383b167.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![收益率分析](https://img-blog.csdnimg.cn/5bf3808296c8466aaee3709573666c26.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![总的持仓](https://img-blog.csdnimg.cn/c325397edef343ed93e58503afdacbe2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![持仓集中度](https://img-blog.csdnimg.cn/c325397edef343ed93e58503afdacbe2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![10个最大持仓的分布](https://img-blog.csdnimg.cn/c37248b7257942e59c66b3045a15f339.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![多空持仓](https://img-blog.csdnimg.cn/7d68517645674f8097791d98d57d806c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![总的杠杆](https://img-blog.csdnimg.cn/7d68517645674f8097791d98d57d806c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
![exposure](https://img-blog.csdnimg.cn/c37248b7257942e59c66b3045a15f339.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5LqR6YeR5p2e,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)





