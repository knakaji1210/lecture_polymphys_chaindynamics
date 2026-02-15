# Animation of Single Chain Dynamics (2d Square Lattice model)
# 重心を奇跡として描画、重心位置の時間変化も描画（240121）
# SAW Chainをモデル化（260128作成開始、260201一旦完了）
# v2 Reptation開発時に見つけた諸々を実装
# 末端以外のセグメントを動かす順番をランダムに変更（260208）
# FuncMを利用する形に変更

import numpy as np
import matplotlib.pyplot as plt
import animatplot as amp
import singleChainDynamicsFuncM_SAW_v1 as scdm

try:
    N = int(input('Degree of polymerization (default=100): '))
except ValueError:
    N = 100

try:
    t_max = int(input('Number of steps (default=100): '))
except ValueError:
    t_max = 100

t = np.linspace(0, t_max-1, t_max)

try:
    initConfig = input('Initial Configuration (Fully Extended (F) or Random Coil (R)): ')
    if initConfig == "":
        raise ValueError
except ValueError:
    initConfig = "F"

try:
    centerConfig = input('with center of gravity (W) or without it (O)): ')
    if centerConfig == "":
        raise ValueError
except ValueError:
    centerConfig = "O"

if initConfig == "F": # Fully Extendedからスタートする場合
    plot_lim = 0.6*N
else: #　Random Coilからスタートする場合
#    plot_lim = 3*np.sqrt(N)
    plot_lim = np.sqrt(10*N)

x_list_steps, y_list_steps = scdm.SAWChainMotion(N, t_max, initConfig)

time_steps = scdm.timeStep(t)

# numpyのバージョンアップにより、""ndarray from ragged nested sequences"の制限が厳しくなり、
# animatplotの途中でエラーが出るようになった。そのための修正が以下の４行
x_list_steps = np.asanyarray(x_list_steps, dtype=object)
y_list_steps = np.asanyarray(y_list_steps, dtype=object)
time_steps = np.asanyarray(time_steps, dtype=object)

# 重心位置
cx_list, cy_list, cx_list_steps, cy_list_steps = scdm.centerOfMass(x_list_steps, y_list_steps, t_max)
cx_list_steps = np.asanyarray(cx_list_steps, dtype=object)
cy_list_steps = np.asanyarray(cy_list_steps, dtype=object)

# 重心移動距離
Dc2_list, Dc2_list_steps = scdm.centerOfMassDist(cx_list, cy_list, t_max)
Dc2_list_steps = np.asanyarray(Dc2_list_steps, dtype=object)
ymax = np.max(Dc2_list)

fig_title1 = "Dynamics of a Single SAW Chain ($N$ = {0})".format(N)
fig_title2 = "$d^{{2}}$ vs $t$"

fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(121, title=fig_title1, xlabel='$X$', ylabel='$Y$',
        xlim=[-plot_lim, plot_lim], ylim=[-plot_lim , plot_lim])        
ax1.grid(axis='both', color="gray", lw=0.5)

singleChainDynamics_c = amp.blocks.Line(cx_list_steps, cy_list_steps, ax=ax1, ls='-', marker="o", markersize=20/plot_lim, color='red')
singleChainDynamics = amp.blocks.Line(x_list_steps, y_list_steps, ax=ax1, ls='-', marker="o", markersize=100/plot_lim, color='blue')

ax2 = fig.add_subplot(122, title=fig_title2, xlabel='$t$', ylabel='$d^{{2}}$',
        xlim=[0, t_max], ylim=[0 , ymax])
ax2.grid(axis='both', color="gray", lw=0.5)

#ax2.plot(t, np.sqrt(N)*np.ones(len(t)), ls='--', color="gray", lw=1)

Dc2Distance = amp.blocks.Scatter(time_steps, Dc2_list_steps, ax=ax2, marker="o", s=30, color='blue')

timeline = amp.Timeline(t, units=' steps', fps=5)

if centerConfig == "O": # 重心描画なし
    anim = amp.Animation([singleChainDynamics, Dc2Distance], timeline)
if centerConfig == "W": # 重心描画あり
    anim = amp.Animation([singleChainDynamics_c, singleChainDynamics, Dc2Distance], timeline)
anim.controls()

if initConfig == "F": # Fully Extendedからスタートする場合
    savefile = "./gif/SingleChain_Dynamics_SAW_N{0}_{1}steps_FE_with_Dc".format(N, t_max)
if initConfig == "R": # Random Coilからスタートする場合
    savefile = "./gif/SingleChain_Dynamics_SAW_N{0}_{1}steps_RC_with_Dc".format(N, t_max)
anim.save_gif(savefile)

plt.show()
plt.close()
