from tkinter import *
import random
from itertools import count
import numpy as np
import matplotlib.pyplot as plt
from pylab import axis, sqrt
from numpy import random

n = 100000 # n powtorzen petli :)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
p = random.rand(n, 3)

idx = np.where(sqrt(p[:, 0] ** 2 + p[:, 1] ** 2 + p[:, 2]) < 1)[0]

idx2 = np.where(sqrt(p[:, 0] ** 2 + p[:, 1] ** 2 + p[:, 2]) >= 1)[0]

ax.set_title('Losowe Punkty')
ax.scatter(xs=p[idx, 0], ys=p[idx, 1], zs=p[idx, 2], c='b')

ax.scatter(xs=p[idx2, 0], ys=p[idx2, 1], zs=p[idx2, 2], c='r', marker='x')



plt.show()