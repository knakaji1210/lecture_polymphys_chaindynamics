# Animation of Single Chain Dynamics (2d Square Lattice model)
# Flory-Huggins的に分岐数zに対してz-1で対応するようにすることはできていない
# v3 --- 一部変更（260201）

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
# import animatplot as amp
import singleChainDynamicsFunc_v3 as scd

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

R_list_repeat = []

for i in range (M):

    start_time = time.process_time()

    x_list_steps = []
    y_list_steps = []

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
        plot_lim = 3*np.sqrt(N)

    orderedArray = np.arange(1,N)   # 260214追加

    # ステップごとのセグメントの動作
    for rep in range(t_max-1):
        # まず両末端を動かす
        coordinate_list = scd.terminalSegment(coordinate_list, N, 0)
        coordinate_list = scd.terminalSegment(coordinate_list, N, 1)   # ３行下にあったのをここに移動（両末端を先に変化させる）
        # 次に末端以外のセグメントを動かす
        shuffledArray = np.random.permutation(orderedArray)   # 260214追加
        for j in range(N-1):                                                # i -> j に変更（繰り返しでiを使っていたので）
#            coordinate_list = scd.segmentMotion(coordinate_list, j+1)                   # こちらが元々
            coordinate_list = scd.segmentMotion(coordinate_list, shuffledArray[j])      # 260214変更
        x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
        x_list_steps.append(x_list)
        y_list_steps.append(y_list)

    R_list, R_list_steps = scd.end2endDist(x_list_steps, y_list_steps, N, t_max)
    R_list_repeat.append(R_list)

    end_time = time.process_time()
    elapsed_time = end_time - start_time
    print("Repetition {0}/{1} completed in {2:.2f} seconds.".format(i+1, M, elapsed_time))

R_mean_list = scd.calcMean(R_list_repeat, t_max, M)

def expDecayFit(t, tau, a, b):
    return  a*np.exp(-t/tau)+b

param, cov = curve_fit(expDecayFit, t, R_mean_list)
tau = param[0]
pref = param[1]
equiR = param[2]
err_tau = np.sqrt(cov[0][0])
err_equiR = np.sqrt(cov[2][2])
R_fit_list = [ expDecayFit(tim, tau, pref, equiR) for tim in t ]

fig_text = "Number of repetition: {}".format(M)
result_text1 = "$τ$ = {0:.2f}±{1:.2f}".format(tau, err_tau)
result_text2 = "$R_{{equi}}$ = {0:.2f}±{1:.2f}".format(equiR, err_equiR)

fig_title = "End-to-end Distance, $R$ ($N$ = {})".format(N)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, title=fig_title, xlabel='$t$', ylabel='$R$',
        xlim=[0, t_max], ylim=[0 , 1.2*N])
ax.grid(axis='both', color="gray", lw=0.5)

# R
ax.plot(t, R_fit_list, lw=2, color='red')
ax.scatter(t, R_mean_list, marker="o", s=30, color='blue')


fig.text(0.65, 0.85, fig_text)
fig.text(0.70, 0.55, result_text1)
fig.text(0.70, 0.50, result_text2)

savefile = "./png/SingleChain_Dynamics_N{0}_{1}steps_M{2}_R".format(N, t_max, M)
fig.savefig(savefile, dpi=300)

plt.show()
plt.close()
