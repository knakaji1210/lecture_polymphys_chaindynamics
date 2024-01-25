# Functions of Single Chain Dynamics (2d Square Lattice model)

import random as rd
import numpy as np
from math import *

def initConfig_FullExted(N):
    x, y = -N/2, 0
    init_coordinate_list = [[x,y]]
    for i in range(N):
        x = x + 1
#        y = y + 1
        coordinate = [x, y]
        init_coordinate_list.append(coordinate)
    return init_coordinate_list

def initConfig_Random(N):
    x, y = 0, 0
    init_coordinate_list = [[x,y]]
    angle_list = (0, 90, 180, 270)
    for i in range(N):
        angle = rd.choice(angle_list)
        x = x + int(np.cos(np.radians(angle)))
        y = y + int(np.sin(np.radians(angle)))
        coordinate = [x, y]
        init_coordinate_list.append(coordinate)
    return init_coordinate_list

# initConfig_Randomに置き換え
def initConfig_Random_old(N):
    x, y = 0, 0
    init_coordinate_list = [[x,y]]
    direction_list = ([1,0],[-1,0],[0,1],[0,-1])
    for i in range(N):
        step = rd.choice(direction_list)
        x = x + step[0]
        y = y + step[1]
        coordinate = [x, y]
        init_coordinate_list.append(coordinate)
    return init_coordinate_list

# 末端の動き・・・隣を中心に回転できることをプログラム
def terminalSegment(coordinate_list, N, p):
    angle_list = (0, 90, 180, 270)
    angle = rd.choice(angle_list)
    if p == 0:
        x1 = coordinate_list[1][0]
        y1 = coordinate_list[1][1]
        x0 = x1 + int(np.cos(np.radians(angle)))
        y0 = y1 + int(np.sin(np.radians(angle)))
        updated_coordinate = [x0, y0]
        coordinate_list[0] = updated_coordinate
    if p == 1:
        xp = coordinate_list[N-1][0]
        yp = coordinate_list[N-1][1]
        xe = xp + int(np.cos(np.radians(angle)))
        ye = yp + int(np.sin(np.radians(angle)))
        updated_coordinate = [xe, ye]
        coordinate_list[N] = updated_coordinate
    return coordinate_list

def segmentMotion(coordinate_list, i):
    angle_list = (0, 90, 180, 270)
    onoff_list = ("on", "off")
    xp = coordinate_list[i-1][0] # p = previous
    yp = coordinate_list[i-1][1]
    xi = coordinate_list[i][0]
    yi = coordinate_list[i][1]
    xn = coordinate_list[i+1][0] # n = next
    yn = coordinate_list[i+1][1]
    # o---o---oの形になっているときは何も動けない
    if (yp == yn and int(np.abs(xn - xp)) == 2) or (xp == xn and int(np.abs(yn - yp)) == 2):
#        print("a")
        xi = xi
        yi = yi
        updated_coordinate = [xi, yi]
        coordinate_list[i] = updated_coordinate
    else:
        # oo===oの形になっているときは[xp, yp]を中心に回転できる
        if xp == xn and yp == yn:
#            print("b")
            angle = rd.choice(angle_list)
#            print("angle = {}".format(angle))
            xi = xp + int(np.cos(np.radians(angle)))
            yi = yn + int(np.sin(np.radians(angle)))
            updated_coordinate = [xi, yi]
            coordinate_list[i] = updated_coordinate
        else:
            if (xp == xi) and ((xn == xp + 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp + 1)):
#                print("c")
                onoff = rd.choice(onoff_list)
#                print(onoff)
                if onoff == "on":
                    xi = xn
                    yi = yp
                if onoff == "off":
                    xi = xi
                    yi = yi               
                updated_coordinate = [xi, yi]
                coordinate_list[i] = updated_coordinate
            else:
                if (xn == xi) and ((xn == xp - 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp - 1)):
#                    print("d")
                    onoff = rd.choice(onoff_list)
#                    print(onoff)
                    if onoff == "on":
                        xi = xp
                        yi = yn
                    if onoff == "off":
                        xi = xi
                        yi = yi   
                    updated_coordinate = [xi, yi]
                    coordinate_list[i] = updated_coordinate
                else:
                    print("e")
    return coordinate_list

def coordinateList2xyList(coordinate_list, N):
    x_list = [ coordinate_list[i][0] for i in range(N+1) ]
    y_list = [ coordinate_list[i][1] for i in range(N+1) ]
    return x_list, y_list

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

def timeStep(t):
    time_steps = [ t[:i].tolist() for i in range(len(t)+1) ]
    time_steps = time_steps[1:]
    return time_steps

def calcMeanR(R_list_repeat, t_max, M):
    R_mean_list = []
    for i in range(t_max):
        R_rep_list = [ R_list_repeat[j][i] for j in range(M) ]
        R_mean = np.mean(R_rep_list)
        R_mean_list.append(R_mean)
    return R_mean_list