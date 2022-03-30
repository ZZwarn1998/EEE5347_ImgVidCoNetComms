

import math
import matplotlib.pyplot as plt
from scipy import integrate

def gaussDistri(mu, sigma, x):
    return 1 /(sigma * math.sqrt(2 * math.pi)) * math.exp(-((x - mu)**2) / (2 * (sigma**2)))

def f2(x):
    return 1 / (10 * math.sqrt(2 * math.pi)) * math.exp(-((x - 0) ** 2) / (2 * (10 ** 2)))

def f1(x):
    return  x * (1 /(10 * math.sqrt(2 * math.pi)) * math.exp(-((x - 0)**2) / (2 * (10**2))))

if __name__ == "__main__":
    mu = 0
    sigma = 10
    st = - 100
    ed = 100
    ntvl = ed - st
    splt = 10000
    x = [st + ntvl / splt * i for i in range(splt)]
    y = [gaussDistri(mu, sigma, i) for i in x]

    plt.figure(1)
    plt.grid()
    plt.fill(x, y)
    plt.xlabel("x")
    plt.ylabel("p(x)")
    plt.title(r'Gaussian Distribution($\mu=0$, $\sigma^{2}=100$)')
    plt.show()