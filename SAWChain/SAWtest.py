import matplotlib.pyplot as plt
import animatplot as amp
import singleChainDynamicsFunc_SAW as scd

N = 20

init_coordinate_list = scd.initConfig_Random(N)

print(init_coordinate_list)

plt.figure()
plt.plot([x[0] for x in init_coordinate_list], [x[1] for x in init_coordinate_list], 'o-')

savefile = "./png/SAW.png"
plt.savefig(savefile)

plt.show()