# Animation of Single Chain Dynamics (2d Square Lattice model)
# 重心位置の時間変化（繰り返し平均後）も描画（240121）
# v3 --- 一部変更（260201）
# Reptation開発時に見つけた諸々を実装
# FuncMを利用する形に変更
# フィッティングの繰り返しに加え、それをさらに繰り返して標準偏差を正しく算出できるようにした
# ただし、描画はそのうちの一つ（最後のもの）を表記するようにした

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
import singleChainDynamicsFuncM_v1 as scdm

try:
    N = int(input('Degree of polymerization (default=100): '))
except ValueError:
    N = 100

try:
    t_max = int(input('Number of steps (default=100): '))
except ValueError:
    t_max = 100

try:
    M = int(input('Number of repeat for curve fitting (default=100): '))
except ValueError:
    M = 100

try:
    repeat = int(input('Number of repeat for statistical analysis (default=50): '))
except ValueError:
    repeat = 50

t = np.linspace(0, t_max-1, t_max)

try:
    initConfig = input('Initial Configuration (Fully Extended (F) or Random Coil (R)): ')
    if initConfig == "":
        raise ValueError
except ValueError:
    initConfig = "F"

if initConfig == "F": # Fully Extendedからスタートする場合
    plot_lim = 0.6*N
else: #　Random Coilからスタートする場合
#    plot_lim = 3*np.sqrt(N)
    plot_lim = np.sqrt(10*N)

def linearFit(t, diff, b):
    return  4*diff*t+b          # 2次元なので<d^2> = 4*D*t

Dc_list = []

for j in range (repeat):

    start_time_rep = time.process_time()

    Dc2_list_repeat = []

    for i in range (M):

        start_time = time.process_time()

        x_list_steps, y_list_steps = scdm.idealChainMotion(N, t_max, initConfig)

        # 重心位置
        cx_list, cy_list, cx_list_steps, cy_list_steps = scdm.centerOfMass(x_list_steps, y_list_steps, t_max)
        cx_list_steps = np.asanyarray(cx_list_steps, dtype=object)
        cy_list_steps = np.asanyarray(cy_list_steps, dtype=object)

        # 重心移動距離
        Dc2_list, Dc2_list_steps = scdm.centerOfMassDist(cx_list, cy_list, t_max)
        Dc2_list_steps = np.asanyarray(Dc2_list_steps, dtype=object)
        Dc2_list_repeat.append(Dc2_list)

        end_time = time.process_time()
        elapsed_time = end_time - start_time
#        print("Repetition {0}/{1} completed in {2:.2f} seconds.".format(i+1, M, elapsed_time))

    Dc_mean_list = scdm.calcMean(Dc2_list_repeat, t_max, M)
    ymax = np.max(Dc_mean_list)

    param, cov = curve_fit(linearFit, t, Dc_mean_list)
    diff = param[0]
    sect = param[1]
    err_diff = np.sqrt(cov[0][0])
    Dc_fit_list = [ linearFit(tim, diff, sect) for tim in t ]
    Dc_list.append(diff)

    end_time_rep = time.process_time()
    elapsed_time_rep = end_time_rep - start_time_rep
    print("Repetition {0}/{1} completed in {2:.2f} seconds.".format(j+1, repeat, elapsed_time_rep))

# 以下はlog(Dc)をエラー付きで記録するため
logDc_list = [ np.log10(Dc) for Dc in Dc_list ]
mean_logDc = np.mean(logDc_list)
std_logDc = np.std(logDc_list)

print("N = {0}, Max Steps = {1}".format(N, t_max))
print("Rep (fitting) = {0}, Rep (statistics) = {1}".format(M, repeat))
print("Mean of relaxation time log(τ): {0:.6f}".format(mean_logDc))
print("STD of log(τ): {0:.6f}".format(std_logDc))

fig_text = "Number of repetition: {}".format(M)
result_text = "$D*100$ = {0:.5f}±{1:.5f}".format(diff*100, err_diff*100)

fig_title = "<$d^{{2}}$> vs $t$ of Single Ideal Chains ($N$ = {})".format(N)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, title=fig_title, xlabel='$t$', ylabel='<$d^{{2}}$>',
        xlim=[0, t_max], ylim=[0 , 1.5*ymax])
ax.grid(axis='both', color="gray", lw=0.5)

# Diffusion const
ax.plot(t, Dc_fit_list, lw=2, color='red')
ax.scatter(t, Dc_mean_list, marker="o", s=30, color='blue')


fig.text(0.65, 0.85, fig_text)
fig.text(0.65, 0.80, result_text)

savefile = "./png/SingleChain_Dynamics_ideal_N{0}_{1}steps_M{2}_Dc".format(N, t_max, M)
fig.savefig(savefile, dpi=300)

plt.show()
plt.close()
