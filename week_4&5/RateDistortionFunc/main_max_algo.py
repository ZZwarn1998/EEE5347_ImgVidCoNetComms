import copy
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate


def centroidCondition(t, hx):
    f1 = lambda x: x * (1 / (10 * np.sqrt(2 * np.pi)) * np.exp(-((x - 0)**2) / (2 * (10**2))))
    f2 = lambda x: 1 / (10 * np.sqrt(2 * np.pi)) * np.exp(-((x - 0)**2) / (2 * (10**2)))

    for i in range(0, len(hx)):
        hx[i] = integrate.quad(f1, t[i], t[i+1])[0] / integrate.quad(f2, t[i], t[i+1])[0]
    return hx


def nearestNeighborhood(t, hx):
    for i in range(1, len(t)-1):
        t[i] = (hx[i-1] + hx[i]) / 2
    return t


def averageQuantizationDistortion(t, hx, M):
    f3 = lambda x, hatx:  ((x - hatx) ** 2) * (1 / (10 * np.sqrt(2 * np.pi)) * np.exp(-((x - 0)**2) / (2 * (10**2))))
    d = 0
    for i in range(M):
        hxi = hx[i]
        d += (integrate.quad(f3, t[i], t[i+1], args=(hxi,))[0])
    return d


def calEntropy(t):
    f2 = lambda x: 1 / (10 * np.sqrt(2 * np.pi)) * np.exp(-((x - 0) ** 2) / (2 * (10 ** 2)))
    E = 0
    for i in range(len(t)-1):
        p = integrate.quad(f2, t[i], t[i+1])[0]
        E += (- p * math.log2(p))
    return E


def scalarQuantizer(M, epsilon):
    t = [-np.inf]
    t.extend(sorted(random.sample(range(-100, 100), M - 1)))
    t.append(np.inf)

    d_k = 0
    d_kminus1 = math.inf

    hx = [0 for i in range(M)]

    while(True):
        hx = centroidCondition(t, hx)
        t = nearestNeighborhood(t, hx)
        d_k = averageQuantizationDistortion(t, hx, M)

        if (d_kminus1 - d_k) / d_k < epsilon:
            break
        else:
            d_kminus1 = d_k

    DM = d_k
    RM = calEntropy(t)

    return DM, RM, hx, t


if __name__ == '__main__':
    dml = []
    rml = []
    epsilon = 0.0001
    for M in range(1, 101):
        DM, RM, hx, t = scalarQuantizer(M, epsilon)
        print("-"*100)
        print("M:", M, "DM:", DM, "RM:", RM)
        print("t:", t)
        print("hat_x:", hx)
        dml.append(DM)
        rml.append(RM)

    thy_rd_func = lambda d: - 1 / 2 * np.log2(d / 100)
    thry_rml = [thy_rd_func(d) for d in range(101)]

    plt.figure(1)
    plt.title("the curve of Rate-Distortion")
    plt.xlabel("D")
    plt.ylabel("R(D)")
    plt.legend()
    plt.grid()

    zipdr = zip(dml,rml)
    sorted_zipdr = sorted(zipdr, key = lambda x:(x[0],x[1]))
    dml, rml = zip(* sorted_zipdr)

    plt.plot(dml, rml, marker='o',color='blue', label = "real")
    plt.plot(range(101), thry_rml,  color='red', label = "theoretical")
    plt.legend()
    plt.show()

