import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
from matplotlib import gridspec

plt.rcParams['font.sans-serif'] = ['SimHei']
jd=pd.read_csv('jd.csv',encoding='utf-8',dtype=str)
tb=pd.read_csv('tb.csv',encoding='utf-8',dtype=str)
jd['price']=jd['price'].str.replace("¥","").astype(float)
tb['price']=tb['price'].str.replace("¥","").astype(float)
jd1=jd["华为荣耀9X"==jd.name]
tb1=tb["honor/荣耀 荣耀9x"==tb.name]
jd2=jd["华为荣耀畅玩8A"==jd.name]
tb2=tb["honor/荣耀 荣耀畅玩8A"==tb.name]
jd3=jd["小米Redmi Note8"==jd.name]
tb3=tb["Xiaomi/小米 Redmi Note 8"==tb.name]
jd4=jd["Apple iPhone 8"==jd.name]
tb4=tb["Apple/苹果 iPhone 8"==tb.name]
jd5=jd["华为畅享9"==jd.name]
tb5=tb["HUAWEI 畅享9"==tb.name]

fig = plt.figure(constrained_layout=True)
spec2 = gridspec.GridSpec(ncols=5, nrows=1, figure=fig)
f1 = fig.add_subplot(spec2[0, 0])
f2 = fig.add_subplot(spec2[0, 1])
f3 = fig.add_subplot(spec2[0, 2])
f4 = fig.add_subplot(spec2[0, 3])
f5 = fig.add_subplot(spec2[0, 4])

f1.boxplot([jd1['price'],tb1['price']],labels=['京东','淘宝'])
f1.set_title("荣耀9X")
f2.boxplot([jd2['price'],tb2['price']],labels=['京东','淘宝'])
f2.set_title("荣耀畅玩8A")
f3.boxplot([jd3['price'],tb3['price']],labels=['京东','淘宝'])
f3.set_title("红米Note8")
f4.boxplot([jd4['price'],tb4['price']],labels=['京东','淘宝'])
f4.set_title("iPhone 8")
f5.boxplot([jd5['price'],tb5['price']],labels=['京东','淘宝'])
f5.set_title("华为畅享9")
plt.show()