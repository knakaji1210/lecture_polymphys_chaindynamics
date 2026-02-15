# Animation of Single Chain Dynamics (2d Square Lattice model)
# FuncM_v1として繰り返しの多い部分をFuncMとして独立させる（260215）

import numpy as np
import singleChainDynamicsFunc_v3 as scd

def idealChainMotion(N, t_max, initConfig):

    x_list_steps = []
    y_list_steps = []

    if initConfig == "F": # Fully Extendedからスタートする場合
        coordinate_list = scd.initConfig_FullExted(N)
        x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
        x_list_steps.append(x_list)
        y_list_steps.append(y_list)
#        plot_lim = 0.6*N
    else: #　Random Coilからスタートする場合
        coordinate_list = scd.initConfig_Random(N)
        x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
        x_list_steps.append(x_list)
        y_list_steps.append(y_list)
#        plot_lim = 3*np.sqrt(N)
#        plot_lim = np.sqrt(10*N)

    orderedArray = np.arange(1,N)   # 260214追加

    # ステップごとのセグメントの動作
    for rep in range(t_max-1):
        # まず両末端を動かす
        coordinate_list = scd.terminalSegment(coordinate_list, N, 0)
        coordinate_list = scd.terminalSegment(coordinate_list, N, 1)   # ３行下にあったのをここに移動（両末端を先に変化させる）
        # 次に末端以外のセグメントを動かす
        shuffledArray = np.random.permutation(orderedArray)   # 260214追加
        for i in range(N-1):
#            coordinate_list = scd.segmentMotion(coordinate_list, i+1)                   # こちらが元々
            coordinate_list = scd.segmentMotion(coordinate_list, shuffledArray[i])      # 260214変更
        x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
        x_list_steps.append(x_list)
        y_list_steps.append(y_list)
    
    return x_list_steps, y_list_steps

# 末端間距離
def end2endDist(x_list_steps, y_list_steps, N, t_max):
    R_list = []
    for i in range(t_max):
        x0 = x_list_steps[i][0]
        y0 = y_list_steps[i][0]
        xe = x_list_steps[i][N]
        ye = y_list_steps[i][N]
        R = np.sqrt((x0 - xe)**2 + (y0 - ye)**2)
        R_list.append(R)
    R_list_steps = [ R_list[:i] for i in range(t_max+1) ]
    R_list_steps = R_list_steps[1:]
    return R_list, R_list_steps

# 重心位置
def centerOfMass(x_list_steps, y_list_steps, t_max):
    cx_list = []
    cy_list = []
    for i in range(t_max):
        xg = np.mean(x_list_steps[i])
        yg = np.mean(y_list_steps[i])
        cx_list.append(xg)
        cy_list.append(yg)
    cx_list_steps = [ cx_list[:i] for i in range(t_max+1) ]
    cy_list_steps = [ cy_list[:i] for i in range(t_max+1) ]
    cx_list_steps = cx_list_steps[1:]
    cy_list_steps = cy_list_steps[1:]
    return cx_list, cy_list, cx_list_steps, cy_list_steps

# 重心移動距離（初期ステップ位置を0に）
def centerOfMassDist(cx_list, cy_list, t_max):
    Dc2_list = []
    for i in range(t_max):
        cx0 = cx_list[0]
        cy0 = cy_list[0]
        cx = cx_list[i]
        cy = cy_list[i]
        Dc2 = (cx0 - cx)**2 + (cy0 - cy)**2
        Dc2_list.append(Dc2)
    Dc2_list_steps = [ Dc2_list[:i] for i in range(t_max+1) ]
    Dc2_list_steps = Dc2_list_steps[1:]
    return Dc2_list, Dc2_list_steps

def timeStep(t):
    time_steps = [ t[:i].tolist() for i in range(len(t)+1) ]
    time_steps = time_steps[1:]
    return time_steps

def calcMean(Data_list_repeat, t_max, M):
    Data_mean_list = []
    for i in range(t_max):
        Data_rep_list = [ Data_list_repeat[j][i] for j in range(M) ]
        Data_mean = np.mean(Data_rep_list)
        Data_mean_list.append(Data_mean)
    return Data_mean_list