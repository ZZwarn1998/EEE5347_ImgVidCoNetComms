import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def centroidCondition(S, hx, t, M):
    for i in range(0, M):
        if len(S[i]) != 0:
            hx[i] = sum(S[i]) / len(S[i])
        else:
            hx[i] = (t[i] + t[i + 1]) / 2
    return hx


def nearestNeighborhood(t, hx):
    for i in range(1, len(t)-1):
        t[i] = (hx[i-1] + hx[i]) / 2
    return t


def averageQuantizationDistortion(S, hx, M, N):
    d = 0
    for i in range(M):
        hxi = hx[i]
        for sx in S[i]:
            d += ((sx - hxi)**2) / N

    return d


def calEntropy(S, N):
    E = 0
    for i in range(len(S)):
        p = len(S[i]) / N
        if abs(p - 0) < 1e-10:
            E += 0
        else:
            E += (- p * math.log2(p))
    return E


def getNewS(t, x):
    S = [[] for i in range(len(t) - 1)]

    for xi in x:
        left_i = 0
        right_i = len(t) - 1
        mid_i = 0

        while (right_i - left_i > 1 ):
            mid_i = int((right_i + left_i ) / 2)
            if (xi > t[left_i] or abs(xi - t[left_i]) < 1e-10) and xi < t[mid_i]:
                right_i = mid_i
            elif (xi > t[mid_i] or abs(xi - t[mid_i]) < 1e-10) and xi < t[right_i]:
                left_i = mid_i

        S[left_i].append(xi)

    return S


def scalarQuantizer(M, epsilon, x):
    t = [-np.inf]
    t.extend(sorted(random.sample(range(-200, 200), M - 1)))
    t.append(np.inf)

    d_k = 0
    d_kminus1 = math.inf

    hx = [0 for i in range(M)]
    S = getNewS(t, x)

    N = len(x)

    while(True):
        S = getNewS(t, x)
        hx = centroidCondition(S, hx, t, M)
        t = nearestNeighborhood(t, hx)
        d_k = averageQuantizationDistortion(S, hx, M, N)

        if (d_kminus1 - d_k) / d_k < epsilon:
            break
        else:
            d_kminus1 = d_k

    DM = d_k
    RM = calEntropy(S, N)

    return DM, RM, hx, t


if __name__ == '__main__':
    dml = []
    rml = []
    epsilon = 0.0001
    miu = 0
    sigma = 10
    x = list(stats.norm.rvs(miu, sigma, size= 10000))

    for M in range(1, 101):
        DM, RM, hx, t = scalarQuantizer(M, epsilon, x)
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
    sorted_zipdr = sorted(zipdr, key = lambda x:(x[0], x[1]))
    dml, rml = zip(* sorted_zipdr)

    plt.plot(dml, rml, marker='o',color='blue', label = "real")
    plt.plot(range(101), thry_rml,  color='red', label = "theoretical")
    plt.legend()
    plt.show()

