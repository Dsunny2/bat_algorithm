import numpy as np
import math

def logistic_proj(z,mu = 4):
    '''
    Logistic map，equation（4）
    '''
    # if k == 0:  
    return mu*z*(1 - z)
    # return math.cos(k*math.cosh(z))

def V_C(V):
    '''
    change a pointer V to a path C
    '''
    C = np.zeros(V.shape[0] + 1,dtype = int)
    elements = list(range(1,V.shape[0] + 2))
    # print(V)
    for i in range(V.shape[0]):
        element = elements[int(V[i] - 1)]
        elements.remove(elements[int(V[i] - 1)])
        C[i] = element
    C[-1] = elements[0]
    return C

def D_V(order = 3,d = 4):
    '''
    given n and D_0，change D to V
    '''
    V = np.zeros(order-1,dtype = int)
    D = np.zeros(order,dtype = int)
    print(d)
    D[0] = d
    for i in range(1,order):
        V[i - 1] = np.ceil(D[i-1]/math.factorial(order - i))
        D[i] = D[i - 1] - (V[i - 1] - 1)*math.factorial(order - i)
    return V

def V_D(V,order):
    D = 1
    for i in range(1,order):
        D += math.factorial(order - i) * (V[i - 1] - 1)
    return D

def C_V(C,order):
    # print("C",C)
    # print(C)
    C = np.array(C,dtype = np.uint64)
    # print(C)
    zero_map = np.zeros(order)
    V = []
    # print(C[int(order - 1)] - 1)
    zero_map[int(C[int(order - 1)] - 1)] = 1
    for i in range(order - 2,-1,-1):
        zero_map[int(C[i] - 1)] = 1
        V.append(int(np.sum(zero_map[:int(C[i])])))
    return np.array(V[::-1],dtype = np.uint64)

def C_D(C,order):
    return V_D(C_V(C,order),order)


def chaotic_V(zi,order = 3):
    '''
    map a chaos z_i to a sequence C，equation（6）
    '''
    V = np.zeros(order - 1,dtype = int)
    d = np.zeros(order - 1)
    d[0] = order * zi
    V[0] = np.ceil(d[0])
    for i in range(2,order):
        d[i - 1] = (order - i + 1)*(d[i - 1]-V[i - 1] + 1)
        V[i - 1] = np.ceil(d[i - 1])
    return V_C(V)-1

if __name__ == "__main__":
    z0 = 0.3
    # for i in range(100):
    #     print('Chaotic value z[{}] = {}'.format(i,z0))
    print(chaotic_V(z0,10))
    z0 = logistic_proj(z0)
    V_D(chaotic_V(z0,10),10)

    for i in range(1,7):
        V = D_V(3,i)
        C = V_C(V)
        print(C_D(C,3))
