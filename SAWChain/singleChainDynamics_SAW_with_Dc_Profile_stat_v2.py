# Animation of Single Chain Dynamics (2d Square Lattice model)
# 重心位置の時間変化（繰り返し平均後）も描画（240121）
# SAW Chainをモデル化（260128作成開始、260201一旦完了）
# v2 Reptation開発時に見つけた諸々を実装
# 末端以外のセグメントを動かす順番をランダムに変更（260208）

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
# import animatplot as amp
import singleChainDynamicsFunc_SAW_v2 as scd

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
        coordinate_list = scd.terminalSegment(coordinate_list, N, 1)
        # 次に末端以外のセグメントを動かす
        shuffledArray = np.random.permutation(orderedArray)   # 260214追加
        for j in range(N-1):                       # i -> j に変更（繰り返しでiを使っていたので）
#            coordinate_list = scd.segmentMotion(coordinate_list, j+1)                   # こちらが元々
            coordinate_list = scd.segmentMotion(coordinate_list, shuffledArray[j])      # 260214変更          
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

    end_time = time.process_time()
    elapsed_time = end_time - start_time
    print("Repetition {0}/{1} completed in {2:.2f} seconds.".format(i+1, M, elapsed_time))

Dc_mean_list = scd.calcMean(Dc2_list_repeat, t_max, M)
ymax = np.max(Dc_mean_list)

def linearFit(t, diff, b):
    return  4*diff*t+b          # 2次元なので<d^2> = 4*D*t

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
        xlim=[0, t_max], ylim=[0 , 1.5*ymax])
ax.grid(axis='both', color="gray", lw=0.5)

# Diffusion const
ax.plot(t, Dc_fit_list, lw=2, color='red')
ax.scatter(t, Dc_mean_list, marker="o", s=30, color='blue')


fig.text(0.65, 0.85, fig_text)
fig.text(0.65, 0.80, result_text)

savefile = "./png/SingleChain_Dynamics_SAW_N{0}_{1}steps_M{2}_Dc".format(N, t_max, M)
fig.savefig(savefile, dpi=300)

plt.show()
plt.close()
