# 重心の拡散係数の重合度依存性
# v2 エラーバーを考慮し、重み付きでフィッティングできるように変更

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

DP_val = input('Enter DP values separated by comma: ')
logDC_val = input('Enter logDC values separated by comma: ')
logDC_std_val = input('Enter logDC STD values separated by comma: ')

DP_val = DP_val.split(',')
DP_list = [ float(val) for val in DP_val ]
logDP_list = [ np.log10(DP) for DP in DP_list ]

logDC_val = logDC_val.split(',')
logDC_list = [ float(val) for val in logDC_val ]

logDC_std_val = logDC_std_val.split(',')
logDC_std_list = [ float(val) for val in logDC_std_val ]

def loglogFit(x, a, b):
    return  a*x + b

param, cov = curve_fit(loglogFit, logDP_list, logDC_list, sigma=logDC_std_list, absolute_sigma=True)
slope = param[0]
err_slope = np.sqrt(cov[0][0])
logDC_fit_list = [ loglogFit(logDP, param[0], param[1]) for logDP in logDP_list ]

resultText = "$D$  ∝ $N^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(slope, err_slope)

fig = plt.figure(figsize=(8,8))

ax = fig.add_subplot(111, title='Scaling of Diffusion Const, $D$', 
            xlabel='Log($N$)', ylabel='Log($D$)')
ax.grid(visible=True, which='major', color ='#666666', linestyle='--')

ax.errorbar(logDP_list, logDC_list, yerr = logDC_std_list, capsize=5, fmt='o', markersize=6, ecolor='black', color='r')
# ax.scatter(logDP_list, logDC_list, marker='o', s=50, c='red')
ax.plot(logDP_list, logDC_fit_list,  c='blue')

fig.text(0.65, 0.70, resultText)

savefile = "./png/Scaling_DiffusionConst"
fig.savefig(savefile, dpi=300)

plt.show()
plt.close()