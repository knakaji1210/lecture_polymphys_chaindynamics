# 一本鎖緩和時間の重合度依存性

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

DP_val = input('Enter DP values separated by comma: ')
RT_val = input('Enter RT values separated by comma: ')
RT_err_val = input('Enter RT err values separated by comma: ')

DP_val = DP_val.split(',')
DP_list = [ float(val) for val in DP_val ]
logDP_list = [ np.log10(DP) for DP in DP_list ]

RT_val = RT_val.split(',')
RT_list = [ float(val) for val in RT_val ]
logRT_list = [ np.log10(RT) for RT in RT_list ]

RT_err_val = RT_err_val.split(',')
RT_err_list = [ float(val) for val in RT_err_val ]
logRT_err_list = [ RT_err/RT for RT_err, RT in zip(RT_err_list, RT_list)]   # 誤差伝播

print(logRT_err_list)

def loglogFit(x, a, b):
    return  a*x + b

param, cov = curve_fit(loglogFit, logDP_list, logRT_list, sigma=logRT_err_list, absolute_sigma=True)
slope = param[0]
err_slope = np.sqrt(cov[0][0])
logRT_fit_list = [ loglogFit(logDP, param[0], param[1]) for logDP in logDP_list ]

resultText = "$τ$  ∝ $N^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(slope, err_slope)

fig = plt.figure(figsize=(8,8))

ax = fig.add_subplot(111, title='Scaling of Relaxation Time, $τ$', 
            xlabel='Log($N$)', ylabel='Log($τ$)')
ax.grid(visible=True, which='major', color='#666666', linestyle='--')

ax.errorbar(logDP_list, logRT_list, yerr = logRT_err_list, capsize=5, fmt='o', markersize=6, ecolor='black', color='r')
# ax.scatter(logDP_list, logRT_list, marker='o', s=50, c='red')
ax.plot(logDP_list, logRT_fit_list,  c='blue')

fig.text(0.65, 0.25, resultText)

savefile = "./png/Scaling_RelaxationTime"
fig.savefig(savefile, dpi=300)

plt.show()
plt.close()