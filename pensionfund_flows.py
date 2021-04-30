import pandas as pd
import pyodbc as sql
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.artist import setp;  

df = pd.read_excel("afp_data.xlsx", index_col = 0, header = 0)

plt.close("all")

usd = 705

df["fondo_afp"]=df["fondo"]+df["afp"]

NAV = pd.pivot_table(df,values='cuota',columns=['fondo_afp'],index=['Fecha'],aggfunc=np.sum)
AUM = pd.pivot_table(df,values='valorfondo',columns=['fondo_afp'],index=['Fecha'],aggfunc=np.sum)
R = NAV.pct_change().fillna(0)
dAUM = AUM.diff().fillna(0)
AUMp = AUM.shift(1)*(1+R)
dAUMp = (AUMp-AUM.shift(1)).fillna(0)

dAUMs = dAUM - dAUMp

cumdAUM = dAUM.cumsum().fillna(0)
cumdAUMp = dAUMp.cumsum().fillna(0)
cumdAUMs = dAUMs.cumsum().fillna(0)

M = pd.DataFrame(cumdAUMs.sum(axis=1),columns=["Savings"])
M["Profitability"]=cumdAUMp.sum(axis=1)

M=M/usd/10**6

M.index.name = 'Date'
df_neg, df_pos = M.clip(upper=0), M.clip(lower=0)
df_pos.columns=["Savings","Profitability"]
df_neg.columns=["Savings","Profitability"]
fig, ax = plt.subplots()
ax.plot(M.sum(axis=1),'k')
ax.set_ylabel('USD (1000)')
ax.set_title('Chilean Pension Funds Growth Breakdown')
df_pos.plot.area(ax=ax, stacked=True, linewidth=0.)
ax.set_prop_cycle(None)
df_neg.rename(columns=lambda x: '_' + x).plot.area(ax=ax, stacked=True, linewidth=0.)
ax.set_ylim([df_neg.sum(axis=1).min(), df_pos.sum(axis=1).max()])
plt.tight_layout()

