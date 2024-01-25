# Animation of Single Chain Dynamics (2d Square Lattice model)
# Flory-Huggins的に分岐数zに対してz-1で対応するようにすることはできていない

import numpy as np
import matplotlib.pyplot as plt
import animatplot as amp
import singleChainDynamicsFunc as scd

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

R_list, R_list_steps = scd.end2endDist(x_list_steps, y_list_steps, N, t_max)
time_steps = scd.timeStep(t)

# numpyのバージョンアップにより、""ndarray from ragged nested sequences"の制限が厳しくなり、
# animatplotの途中でエラーが出るようになった。そのための修正が以下の４行
x_list_steps = np.asanyarray(x_list_steps, dtype=object)
y_list_steps = np.asanyarray(y_list_steps, dtype=object)
R_list_steps = np.asanyarray(R_list_steps, dtype=object)
time_steps = np.asanyarray(time_steps, dtype=object)

fig_title1 = "Dynamics of a Single Polymer Chain ($N$ = {0})".format(N)
fig_title2 = "End-to-end Distance, $R$"

fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(121, title=fig_title1, xlabel='$X$', ylabel='$Y$',
        xlim=[-plot_lim, plot_lim], ylim=[-plot_lim , plot_lim])        
ax1.grid(axis='both', color="gray", lw=0.5)

singleChainDynamics = amp.blocks.Line(x_list_steps, y_list_steps, ax=ax1, ls='-', marker="o", markersize=100/plot_lim, color='blue')

ax2 = fig.add_subplot(122, title=fig_title2, xlabel='$t$', ylabel='$R$',
        xlim=[0, t_max], ylim=[0 , 1.2*N])
ax2.grid(axis='both', color="gray", lw=0.5)

#ax2.plot(t, R_list, ls='-', color="gray", lw=3)

end2endDistance = amp.blocks.Scatter(time_steps, R_list_steps, ax=ax2, marker="o", s=30, color='blue')

timeline = amp.Timeline(t, units=' steps', fps=5)

anim = amp.Animation([singleChainDynamics, end2endDistance], timeline)
#anim = amp.Animation([singleChainDynamics], timeline)
anim.controls()

if initConfig == "F": # Fully Extendedからスタートする場合
    savefile = "./gif/SingleChain_Dynamics_N{0}_{1}steps_FE_with_R".format(N, t_max)
if initConfig == "R": # Fully Extendedからスタートする場合
    savefile = "./gif/SingleChain_Dynamics_N{0}_{1}steps_RC_with_R".format(N, t_max)
anim.save_gif(savefile)

plt.show()
plt.close()
