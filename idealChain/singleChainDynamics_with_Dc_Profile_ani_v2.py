# Animation of Single Chain Dynamics (2d Square Lattice model)
# 重心を奇跡として描画、重心位置の時間変化も描画（240121）
# v3 --- 一部変更（260201）

import numpy as np
import matplotlib.pyplot as plt
import animatplot as amp
import singleChainDynamicsFunc_v3 as scd

try:
    N = int(input('Degree of polymerization (default=100): '))
except ValueError:
    N = 100

try:
    t_max = int(input('Number of steps (default=100): '))
except ValueError:
    t_max = 100

t = np.linspace(0, t_max-1, t_max)

x_list_steps = []
y_list_steps = []

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
    coordinate_list = scd.initConfig_FullExted(N)
    x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)
    plot_lim = 0.6*N
else: #　Random Coilからスタートする場合
    coordinate_list = scd.initConfig_Random(N)
    x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)
#    plot_lim = 3*np.sqrt(N)
    plot_lim = np.sqrt(10*N)

orderedArray = np.arange(1,N)   # 260214追加

# ステップごとのセグメントの動作
for rep in range(t_max-1):
    # まず両末端を動かす
    coordinate_list = scd.terminalSegment(coordinate_list, N, 0)
    coordinate_list = scd.terminalSegment(coordinate_list, N, 1)
    # 次に末端以外のセグメントを動かす
    shuffledArray = np.random.permutation(orderedArray)   # 260214追加
    for i in range(N-1):
#        coordinate_list = scd.segmentMotion(coordinate_list, i+1)                   # こちらが元々        
        coordinate_list = scd.segmentMotion(coordinate_list, shuffledArray[i])      # 260214変更
    x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)

time_steps = scd.timeStep(t)

# numpyのバージョンアップにより、""ndarray from ragged nested sequences"の制限が厳しくなり、
# animatplotの途中でエラーが出るようになった。そのための修正が以下の４行
x_list_steps = np.asanyarray(x_list_steps, dtype=object)
y_list_steps = np.asanyarray(y_list_steps, dtype=object)
time_steps = np.asanyarray(time_steps, dtype=object)

# 重心位置
cx_list, cy_list, cx_list_steps, cy_list_steps = scd.centerOfMass(x_list_steps, y_list_steps, t_max)
cx_list_steps = np.asanyarray(cx_list_steps, dtype=object)
cy_list_steps = np.asanyarray(cy_list_steps, dtype=object)

# 重心移動距離
Dc2_list, Dc2_list_steps = scd.centerOfMassDist(cx_list, cy_list, t_max)
Dc2_list_steps = np.asanyarray(Dc2_list_steps, dtype=object)
ymax = np.max(Dc2_list)

fig_title1 = "Dynamics of a Single Polymer Chain ($N$ = {0})".format(N)
fig_title2 = "$d^{{2}}$ vs $t$"

fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(121, title=fig_title1, xlabel='$X$', ylabel='$Y$',
        xlim=[-plot_lim, plot_lim], ylim=[-plot_lim , plot_lim])        
ax1.grid(axis='both', color="gray", lw=0.5)

singleChainDynamics_c = amp.blocks.Line(cx_list_steps, cy_list_steps, ax=ax1, ls='-', marker="o", markersize=20/plot_lim, color='red')
singleChainDynamics = amp.blocks.Line(x_list_steps, y_list_steps, ax=ax1, ls='-', marker="o", markersize=100/plot_lim, color='blue')

ax2 = fig.add_subplot(122, title=fig_title2, xlabel='$t$', ylabel='$d^{{2}}$',
        xlim=[0, t_max], ylim=[0 , 1.5*ymax])
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
    savefile = "./gif/SingleChain_Dynamics_N{0}_{1}steps_FE_with_Dc".format(N, t_max)
if initConfig == "R": # Random Coilからスタートする場合
    savefile = "./gif/SingleChain_Dynamics_N{0}_{1}steps_RC_with_Dc".format(N, t_max)
anim.save_gif(savefile)

plt.show()
plt.close()
