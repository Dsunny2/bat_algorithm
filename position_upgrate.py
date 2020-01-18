import math
import random
import numpy as np
from numba import jit

# Scramble coordinates
def getnum(v):
    n = len(v)
    index = random.randint(0, n - 1)
    num = v[index]
    v[n-1],v[index]= v[index],v[n-1]
    v.pop()
    return num

def generaterandom(n):
    v = [0] * n
    ran = []
    for i in range(n):
        v[i] = i 
    while len(v) > 0:
        ran.append(getnum(v))
    return ran

def generaterandom_np(n):
    v = [0] * n
    ran = []
    for i in range(n):
        v[i] = i 
    while len(v) > 0:
        ran.append(getnum(v))
    return ran

# bat information
def positionup(city_number,x_best,x,v,f):
    v_diff = []
    for i in range(city_number):
        if x[i] != x_best[i]:##DD
            v_diff.append([x[i],x_best[i]])

    v_all = v + v_diff
    # print(v_all)
    # print("v_all---------")
    l = math.floor(f * city_number) +1
    l = int(l)
    a = len(v_all)  
    b = generaterandom(a)
    v_add = []
    for i in range(l):
        v_add.append(v_all[b[i]])

    # print(v_add)
    # print("v_add---------")
    c = len(v_add)
    index = 0 
    while index < c:
        x[int(v_add[index][0]-1)],x[int(v_add[index][1]-1)] = x[int(v_add[index][1]-1)],x[int(v_add[index][0]-1)]
        index = index + 1

    w = city_number - l
    for i in range(w):
        exchange = [random.randint(1,city_number),random.randint(1,city_number)]
        v_add.append(exchange)
    
    return x,v_add


def positionup_np(city_number,x_best,x,v,f):
    unequal_idx = (x!=x_best)
    v_diff = np.column_stack((x[unequal_idx],x_best[unequal_idx]))
    v_all = np.row_stack((v,v_diff))

    l = int(math.floor(f * city_number) +1)
    a = v_all.shape[0]
    b = np.random.permutation(a) - 1
    v_add = v_all[b[:l],:]

    for i in v_add:
        x[i] = x[i[::-1]]

    w = city_number - l
    exchange = np.random.randint(0,city_number,size = [w,2])
    v_add = np.row_stack((v_add,exchange))
    
    return x,v_add

if __name__ == "__main__":
    x = np.array([1,2,3,4,5,6])
    a = np.array([1,2,3,4,5],dtype = np.uint8)
    b = np.array([2,1,3,4,5],dtype = np.uint8)
    equal_idx = (a != b)
    v_diff = np.column_stack((a[equal_idx],b[equal_idx]))

    print(v_diff)

    for i in v_diff:
        x[i] = x[i[::-1]]
    print(x)