import pandas as pd
import pyfolio as pf
import os
import warnings

warnings.filterwarnings("ignore")
# 加载数据
pf_path = os.path.dirname(pf.__file__)
df = pd.read_csv(pf_path + "/datas/基准收益率和日收益率序列.csv", index_col=0)
df.index = pd.to_datetime(df.index)
positions = pd.read_csv(pf_path + "/datas/positions.csv", index_col=0)
positions.index = pd.to_datetime(positions.index)
pf.create_full_tear_sheet_by_flask(df['returns'],
                                   benchmark_rets=df['benchmark_rets'],
                                   positions=positions,
                                   live_start_date='2019-01-01',
                                   run_flask_app=True
                                   )
