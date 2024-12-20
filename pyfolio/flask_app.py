
from flask import Flask  # 导入Flask 类创建Flask应用对象
from flask import render_template
import pandas as pd
import pyfolio as pf
# 文件地址
data_root = pf.__file__.replace("__init__.py","")
target_templates_path = data_root+"/templates/"  
target_static_path = data_root+"/static/" 
# 初始化app    
app = Flask(__name__,template_folder=target_templates_path,static_folder=target_static_path)  # app = application

performance_df = pd.read_excel(target_static_path+"strategy_performance__Out-of-sample months.xlsx",index_col=0)
stress_events_df = pd.read_excel(target_static_path+"strategy_performance__Stress Events.xlsx",index_col=0).astype("str")
long_position_df = pd.read_excel(target_static_path+"strategy_performance__Top 10 long positions of all time.xlsx",index_col=0)
short_position_df = pd.read_excel(target_static_path+"strategy_performance__Top 10 positions of all time.xlsx",index_col=0)
worst_drawdown_df = pd.read_excel(target_static_path+"strategy_performance__Worst drawdown periods.xlsx",index_col=0)

@app.route("/",methods=("POST", "GET"))
def first_page():
    # 绩效统计数据
    return render_template("flask_index.html",
                           name = "pyfolio-策略绩效分析",
                           performance_tables=[performance_df.to_html(classes='data', header="true")],
                           stress_events_tables=[stress_events_df.to_html(classes='data', header="true")],
                           long_position_tables=[long_position_df.to_html(classes='data', header="true")],
                           short_position_tables=[short_position_df.to_html(classes='data', header="true")],
                           worst_drawdown_tables=[worst_drawdown_df.to_html(classes='data', header="true")]
                           
    )

if __name__ == '__main__':  # 当前文件处于脚本状态时运行如下代码
    app.run(port = "2021")  # 启动Flask 应用