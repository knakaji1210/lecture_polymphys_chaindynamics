# Animation of Single Chain Dynamics (2d Square Lattice model)
# Flory-Huggins的に分岐数zに対してz-1で対応するようにすることはできていない
# 重心位置の時間変化（繰り返し平均後）も描画（240121）
# Flory-Huggins的な配置を実現（240124）

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import animatplot as amp
import singleChainDynamicsFunc_FloryHuggins as scd

try:
    N = int(input('Degree of polymerization (default=100): '))
except ValueError:
    N = 100

try:
    t_max = int(input('Number of steps (default=100): '))
except ValueError:
    t_max = 100

try:
    M = int(input('Number of repeat (default=100): '))
except ValueError:
    M = 100

t = np.linspace(0, t_max-1, t_max)

try:
    initConfig = input('Initial Configuration (Fully Extended (F) or Random Coil (R)): ')
    if initConfig == "":
        raise ValueError
except ValueError:
    initConfig = "F"

Dc2_list_repeat = []

for i in range (M):

    x_list_steps = []
    y_list_steps = []

    if initConfig == "F": # Fully Extendedからスタートする場合
        init_coordinate_list = scd.initConfig_FullExted(N)
        x_list, y_list = scd.coordinateList2xyList(init_coordinate_list, N)
        x_list_steps.append(x_list)
        y_list_steps.append(y_list)
        plot_lim = 0.6*N
    else: #　Random Coilからスタートする場合
        init_coordinate_list = scd.initConfig_Random(N)
        x_list, y_list = scd.coordinateList2xyList(init_coordinate_list, N)
        x_list_steps.append(x_list)
        y_list_steps.append(y_list)
        plot_lim = 3*np.sqrt(N)

    for rep in range(t_max-1):
        coordinate_list = scd.terminalSegment(init_coordinate_list, N, 0)
        for i in range(N-1):
            coordinate_list = scd.segmentMotion(coordinate_list, i+1)
            coordinate_list = scd.terminalSegment(init_coordinate_list, N, 1)
        x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
        x_list_steps.append(x_list)
        y_list_steps.append(y_list)

    # 重心位置
    cx_list, cy_list, cx_list_steps, cy_list_steps = scd.centerOfMass(x_list_steps, y_list_steps, t_max)
    cx_list_steps = np.asanyarray(cx_list_steps, dtype=object)
    cy_list_steps = np.asanyarray(cy_list_steps, dtype=object)

    # 重心移動距離
    Dc2_list, Dc2_list_steps = scd.centerOfMassDist(cx_list, cy_list, t_max)
    Dc2_list_steps = np.asanyarray(Dc2_list_steps, dtype=object)
    Dc2_list_repeat.append(Dc2_list)

Dc_mean_list = scd.calcMean(Dc2_list_repeat, t_max, M)

def linearFit(t, diff, b):
    return  2*diff*t+b

param, cov = curve_fit(linearFit, t, Dc_mean_list)
diff = param[0]
sect = param[1]
err_diff = np.sqrt(cov[0][0])
Dc_fit_list = [ linearFit(tim, diff, sect) for tim in t ]

fig_text = "Number of repetition: {}".format(M)
result_text = "$D*100$ = {0:.5f}±{1:.5f}".format(diff*100, err_diff*100)

fig_title = "<$d^{{2}}$> vs $t$ ($N$ = {})".format(N)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, title=fig_title, xlabel='$t$', ylabel='<$d^{{2}}$>',
        xlim=[0, t_max], ylim=[0 , 3*t_max/N])
ax.grid(axis='both', color="gray", lw=0.5)

# Diffusion const
ax.plot(t, Dc_fit_list, lw=2, color='red')
ax.scatter(t, Dc_mean_list, marker="o", s=30, color='blue')


fig.text(0.65, 0.85, fig_text)
fig.text(0.65, 0.80, result_text)

savefile = "./png/SingleChain_Dynamics_FloryHuggins_N{0}_{1}steps_M{2}_Dc".format(N, t_max, M)
fig.savefig(savefile, dpi=300)

plt.show()
plt.close()
