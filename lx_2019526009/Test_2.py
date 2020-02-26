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

fig2 = plt.figure(constrained_layout=True)
spec2 = gridspec.GridSpec(ncols=1, nrows=2, figure=fig2)
f2_ax1 = fig2.add_subplot(spec2[0, 0])
f2_ax2 = fig2.add_subplot(spec2[1, 0])
jd=pd.read_csv('jd.csv',encoding='utf-8',dtype=str)
tb=pd.read_csv('tb.csv',encoding='utf-8',dtype=str)
jd['gross']=jd.apply(get_gross,axis=1)
tb['gross']=tb.apply(get_gross,axis=1)

f2_ax1.set_title("京东")
f2_ax2.set_title("淘宝")
jd['price']=jd['price'].str.replace("¥","").astype(float)
tb['price']=tb['price'].str.replace("¥","").astype(float)
#这儿对价格进行处理
jd = jd.drop(jd[jd.price > 20000].index)
tb = tb.drop(tb[tb.price > 20000].index)
#对价格大于20000的认为是异常值
jd1=jd['price'].value_counts()
tb1=tb['price'].value_counts()

f2_ax1.scatter(jd1.index,jd1.values)
f2_ax2.scatter(tb1.index,tb1.values)
plt.show()