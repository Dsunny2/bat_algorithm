import gzip
import os
import math
import random
import numpy as np
from position_upgrate import positionup,positionup_np
import dvc
import copy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time
import tspparse as tp
from matplotlib.offsetbox import AnchoredText


def experiment(filename,b_size = 1,N = 1,ro = 0.5,ao = 0.5,alpha = 0.9,beta = 0.9,debug = False):
    tsp = tp.read_tsp_file(filename)
    city_number = tsp['DIMENSION']
    tsp_matrix = tsp['DISTANCE_MATRIX']
    vis_coor = tsp['CITIES']
    b_position_initial = np.zeros([b_size,city_number],dtype = int)
    start_whole = time.time()
    for i in range(b_size):
        b_position_initial[i] = np.random.permutation(city_number) - 1

    v_initial = np.random.randint(0,city_number,size = [b_size,city_number,2])
    # print(v_initial)

    # loudness & frequency initialization and update rules
    r = []
    a = []
    r.append(ro)
    a.append(ao)

    # loudness effect
    def update_r(x):
        y = alpha * x
        return y

    # frequency effect
    def update_a(x,t):
        y = ro * (1 - math.exp(-beta * (t)))
        return y


    def wholedistance_np(x):
        x_roll = np.roll(x,1)
        return np.sum(tsp_matrix[x,x_roll])

    fitness_old = np.zeros(b_size)
    best_distance = 10000000
    # local optimal
    for i in range(b_size):
        now_distance = wholedistance_np(b_position_initial[i])
        fitness_old[i] = now_distance
        if now_distance <= best_distance:
            best_distance =  now_distance
            index = i

    best_path = b_position_initial[index].copy()

    # position update
    b_position = copy.deepcopy(b_position_initial)
    v = v_initial

    z0 = 1
    while z0 == 1 or z0 == 0.25 or z0 == 0.75 or z0 == 0.5:
        z0 = random.uniform(0,1)
    print(z0)
    # z0 = 0.23196199337524548
    z_i = 0

    n0 = 0
    x_t = np.zeros(b_size)
    x_r = np.zeros(b_size)
    x_a = np.zeros(b_size)
    f = np.random.uniform(0,1,b_size)##DD
    x_r += ro
    x_a += ao

    end_whole = time.time() - start_whole
    print('initialized complete: {}s'.format(end_whole))

    while n0 < N :
    # every singal bat
        print('Iteration {} starts:'.format(n0+1))
        itertime = time.time()
        for i in range(b_size):
            battime = time.time()
            x_position = b_position[i]
            x_best = best_path.copy()
            batv = v[i]
            f = random.uniform(0,1)
            b_position[i],v[i] = positionup_np(city_number,x_best,x_position,batv,f)

            rand = random.uniform(0,1)

            if rand > x_r[i] :
            # if True:
                print('-----chaotic')
                z0 = dvc.logistic_proj(z0)
                b_position[i] = dvc.chaotic_V(z0,city_number)

            
            b_position_tmp = b_position[i].copy()
            neigh_search_time = time.time()
            if debug:
                print('Bat {} starts local search'.format(i+1))
            start_count = 0
            switch_count = 0
            tmp_best = wholedistance_np(b_position_tmp)
            if debug:
                print('temporarily best: {}'.format(tmp_best))
            while True:
                start_count += 1
                flag2 = 1
                
                for k in range(city_number-3):
                    flag1 = 1
                    for j in range(k+3,city_number):
                        if tsp_matrix[b_position_tmp[k], b_position_tmp[k+1]] + tsp_matrix[b_position_tmp[j-1], b_position_tmp[j]] > tsp_matrix[b_position_tmp[k], b_position_tmp[j-1]] + tsp_matrix[b_position_tmp[k+1], b_position_tmp[j]]:
                            # print("Switching {} and {}".format(k,j)
                            b_position_tmp[k+1:j] = b_position_tmp[j-1:k:-1]
                            tmp_best = wholedistance_np(b_position_tmp)
                            if debug:
                                print('temporarily best: {}'.format(tmp_best))
                            switch_count += 1
                            # print('--------5----------')
                            # print(b_position[i])
                            flag1 = 0
                            break 
                    if flag1 == 0:
                        flag2 = 0
                        break
                if flag2 == 1:
                    break
            if debug:
                print('Local search of Bat {} takes {}s, switch {} times, restart {} times'.format(i+1,time.time()-neigh_search_time,switch_count,start_count))
                
            best_distance_local = wholedistance_np(b_position_tmp)
            # best_path_local = b_position[i].copy()

            # print("local")
            # print(best_distance_local)
            # print("all")
            # print(best_distance)


            rand = random.uniform(0,1)
            if best_distance_local < fitness_old[i] and rand < x_a[i]:
                fitness_old[i] = best_distance_local
                b_position[i] = b_position_tmp.copy()
                x_t[i] += 1
                # x_r = r[t]
                # x_a = a[t]
                x_r[i] = update_r(x_r[i])
                x_a[i] = update_a(ao,x_t[i])
                # r.append(update_r(r[t]))
                # a.append(update_a(ao,t))
                # best_distance = best_distance_local
                # best_path = best_path_local
            if best_distance_local < best_distance:
                print("-----------Better Result!!!----------")
                best_distance = best_distance_local
                best_path = b_position_tmp.copy()
            print('Iteration {}, Bat {}, takes {}s'.format(n0+1,i+1,time.time()-battime))
            # print("all")
            # print(best_distance)
        print("-----------currently best path----------")
        print(best_path)
        print("-----------currently best distance----------")
        print(best_distance)
        print('Iteration {} complete, takes {}s'.format(n0+1,time.time()-itertime))

        n0 += 1


    print("-----------best path----------")
    print(best_path)
    print("-----------best distance----------")
    print(best_distance)

    know1 = tsp['OPT']
    know2 = wholedistance_np(know1)

    print("-----------best path existed----------")
    print(know1)
    print("-----------best path existed----------")
    print(know2)

    fig = plt.figure(figsize = (20,20))
    end_whole = time.time() - start_whole
    print('elapsed time: {0}s'.format(end_whole))

    ax = plt.subplot(111)
    ax.plot(vis_coor[:, 0], vis_coor[:, 1], 'x', color='blue')

    for i in range(city_number):
        ax.text(vis_coor[i, 0], vis_coor[i, 1], str(i))
    n_best_path = [i for i in best_path]
    n_best_path.append(n_best_path[0])
    ax.plot(vis_coor[n_best_path, 0], vis_coor[n_best_path, 1], color='#F08080',alpha = 0.7)

    n_know_path = [i for i in tsp['OPT']]
    n_know_path.append(n_know_path[0])
    ax.plot(vis_coor[n_know_path, 0], vis_coor[n_know_path, 1], color='#4169E1',alpha = 0.4)
    ax.set_title(filename,fontsize = 25)

    at = AnchoredText("File Name:{}\nPopulation:{}\nIteration:{}\nBest Result:{}\nBenchmark:{}\nTime Used:{} s".format(filename,b_size,N,best_distance,know2,np.round(end_whole,4)),
                      loc='upper right', prop=dict(size=8,fontsize = 14), frameon=True,
                      )
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)

    if not os.path.exists('./results'):
        os.makedirs('./results')
    savename = './results/{}_{}_Bats_{}_Iterations.png'.format(filename,b_size,N)
    fig.savefig(savename)
    plt.close(fig)
