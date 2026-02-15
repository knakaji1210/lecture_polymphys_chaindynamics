# Animation of Single Chain Dynamics (2d Square Lattice model)
# Flory-Huggins的に分岐数zに対してz-1で対応するようにすることはできていない
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

def expDecayFit(t, tau, a, b):
    return  a*np.exp(-t/tau)+b

tau_list = []

for j in range (repeat):

    start_time_rep = time.process_time()

    R_list_repeat = []

    for i in range (M):

        start_time = time.process_time()

        x_list_steps, y_list_steps = scdm.idealChainMotion(N, t_max, initConfig)

        R_list, R_list_steps = scdm.end2endDist(x_list_steps, y_list_steps, N, t_max)
        R_list_repeat.append(R_list)

        end_time = time.process_time()
        elapsed_time = end_time - start_time
#        print("Repetition {0}/{1} completed in {2:.2f} seconds.".format(i+1, M, elapsed_time))

    R_mean_list = scdm.calcMean(R_list_repeat, t_max, M)

    param, cov = curve_fit(expDecayFit, t, R_mean_list)
    tau = param[0]
    pref = param[1]
    equiR = param[2]
    err_tau = np.sqrt(cov[0][0])
    err_equiR = np.sqrt(cov[2][2])
    R_fit_list = [ expDecayFit(tim, tau, pref, equiR) for tim in t ]
    tau_list.append(tau)

    end_time_rep = time.process_time()
    elapsed_time_rep = end_time_rep - start_time_rep
    print("Repetition {0}/{1} completed in {2:.2f} seconds.".format(j+1, repeat, elapsed_time_rep))

# 以下はlog(tau)をエラー付きで記録するため
logtau_list = [ np.log10(tau) for tau in tau_list ]
mean_logtau = np.mean(logtau_list)
std_logtau = np.std(logtau_list)

print("N = {0}, Max Steps = {1}".format(N, t_max))
print("Rep (fitting) = {0}, Rep (statistics) = {1}".format(M, repeat))
print("Mean of relaxation time log(τ): {0:.2f}".format(mean_logtau))
print("STD of log(τ): {0:.2f}".format(std_logtau))

fig_text = "Number of repetition: {}".format(M)
result_text1 = "$τ$ = {0:.2f}±{1:.2f}".format(tau, err_tau)
result_text2 = "$R_{{equi}}$ = {0:.2f}±{1:.2f}".format(equiR, err_equiR)

fig_title = "End-to-end Distance of Single Ideal Chains, $R$ ($N$ = {})".format(N)

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

savefile = "./png/SingleChain_Dynamics_ideal_N{0}_{1}steps_M{2}_R".format(N, t_max, M)
fig.savefig(savefile, dpi=300)

plt.show()
plt.close()
