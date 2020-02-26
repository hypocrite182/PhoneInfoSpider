import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import re

plt.rcParams['font.sans-serif'] = ['SimHei']
def get_gross(x):
    gross=0
    try:
        gross=float(re.search("\d+\.?\d*",x.gross).group())
        if "万" in x.gross:
            gross*=10000
    except:
        pass
    return gross

def get_name(x):
    temp=x['name'].split()
    result=list()
    for each in temp:
        if "/" not in each and "HUAWEI" not in each and "尊享" not in each and not each.endswith("G"):
            if "Apple" in each:
                each=each.replace("Apple","")
            result.append(each)
    return "".join(result)

fig2 = plt.figure(constrained_layout=True)
spec2 = gridspec.GridSpec(ncols=1, nrows=2, figure=fig2)
f2_ax1 = fig2.add_subplot(spec2[0, 0])
f2_ax2 = fig2.add_subplot(spec2[1, 0])
jd=pd.read_csv('jd.csv',encoding='utf-8',dtype=str)
jd['gross']=jd.apply(get_gross,axis=1)
jd['name']=jd.apply(get_name,axis=1)
new_table=jd.groupby('name').sum()
data=new_table.gross.sort_values(ascending=False)
f2_ax1.tick_params(labelsize=7)
f2_ax1.bar(data.index[0:20],data.values[0:20])
f2_ax1.set_title("京东（总评论量）")
tb=pd.read_csv('tb.csv',encoding='utf-8',dtype=str)
tb['gross']=tb.apply(get_gross,axis=1)
tb['name']=tb.apply(get_name,axis=1)
new_table=tb.groupby('name').sum()
data=new_table.gross.sort_values(ascending=False)
f2_ax2.tick_params(labelsize=7)
f2_ax2.bar(data.index[0:20],data.values[0:20])
f2_ax2.set_title("淘宝（总月销量）")
plt.show()