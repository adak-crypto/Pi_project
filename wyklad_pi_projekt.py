#!/usr/bin/env python3
from tkinter import *
import random
from itertools import count
import numpy as np
import matplotlib.pyplot as plt
from pylab import axis, sqrt
from numpy import random

import time

window = Tk()
window.geometry("600x200")
window.title("Monte Carlo - wyznaczanie liczby Pi")

n2dVar = StringVar()
n2dInput = Entry(window, textvariable=n2dVar)
n2dInput.grid(row=0, column=2, padx=10, pady=10, ipady=10)

n3dVar = StringVar()
n3dInput = Entry(window, textvariable=n3dVar)
n3dInput.grid(row=1, column=2, padx=10, pady=10, ipady=10)

nnButton = Button(window, text="Dodaj n dla 2d = ", command=lambda: wykres_2d())
nnButton.grid(row=0, column=0, padx=10, pady=10, ipady=10)
diButton = Button(window, text="Dodaj n dla 3d = ", command=lambda: wykres_3d())
diButton.grid(row=1, column=0, padx=10, pady=10, ipady=10)

# start/stop:
startButton = Button(window, text="start", command=lambda: wykres_2d())
startButton.grid(row=0, column=5, padx=10, pady=10, ipady=10)
stopButton = Button(window, text="stop", command=lambda: wykres_2d())
stopButton.grid(row=0, column=6, padx=10, pady=10, ipady=10)

startButton = Button(window, text="start", command=lambda: wykres_3d())
startButton.grid(row=1, column=5, padx=10, pady=10, ipady=10)
stopButton = Button(window, text="stop", command=lambda: wykres_3d())
stopButton.grid(row=1, column=6, padx=10, pady=10, ipady=10)


def wykres_2d():
    czas = 0.0001
    #global n2dVar
    n = int(n2dVar.get())

    lista_pi_result = np.zeros(n)
    ilosc_inside = 0
    ilosc_outside = 0
    czy_rysowac_dalej = True

    fig = plt.figure()

    for i in range(1, n + 1):
        p = random.rand(1, 2)
        idx = sqrt(p[:, 0] ** 2 + p[:, 1] ** 2) < 1
        ax = fig.add_subplot(221)
        ax.set_title('Losowe Punkty')
        ax.set_aspect('equal')
        ax.add_artist(plt.Circle((0, 0), 1, color='m', fill=False))
        ax.scatter(p[idx, 0], p[idx, 1], c='b')  # inside
        if p[idx, 0] > 0:
            ilosc_inside += 1
        plt.pause(czas)
        ax.scatter(p[idx == False, 0], p[idx == False, 1], c='r', marker='x')
        if p[idx == False, 0] > 0:
            ilosc_outside += 1
        plt.pause(czas)
        axis([-0.01, 1.01, -0.01, 1.01])

        ax = fig.add_subplot(222)
        ax.set_title('Liczba Pi')
        ax.set_ylabel('Liczba Pi')
        ax.set_xlabel('n')
        pi = ilosc_inside / i * 4
        lista_pi_result[i-1] = pi
        ax.scatter(i, pi, c='g', marker='x')
        ax.scatter(i, np.pi, c='r', marker=0)
        plt.pause(czas)

        ax = fig.add_subplot(223)
        ax.set_title('Histogram')
        ax.hist(lista_pi_result[:i], 20, color='b')
        plt.pause(czas)
    plt.show()


def wykres_3d():

    time0 = time.time()
    czas = 0.00001
    #global n3dVar
    n = int(n3dVar.get())  # n powtorzen petli :)

    step = 10

    lista_pi_result = np.zeros(n)
    ilosc_inside = 0
    # ilosc_outside = 0vbgggggggggggh
    # czy_rysowac_dalej = True
    fig = plt.figure()
    ax = fig.add_subplot(221, projection='3d')
    for i in range(1, n + 1):
        p = random.rand(1, 3)
        idx = sqrt(p[:, 0] ** 2 + p[:, 1] ** 2 + p[:, 2]) < 1
        ax.set_title('Losowe Punkty')
        ax.scatter(xs=p[idx, 0], ys=p[idx, 1], zs=p[idx, 2], c='b')
        if p[idx, 0] > 0:
            ilosc_inside += 1
        plt.pause(czas)
        ax.scatter(xs=p[idx == False, 0], ys=p[idx == False, 1], zs=p[idx == False, 2], c='r', marker='x')
        # if p[idx == False, 0] > 0:
        #     ilosc_outside += 1
        plt.pause(czas)

        pi = float(ilosc_inside) / float(i) * 6
        lista_pi_result[i-1] = pi
        print("ilość inside = ", ilosc_inside)
        print("pi = ", pi)

        if i % step == 0:
            ax2 = fig.add_subplot(222)
            ax2.set_title('Liczba Pi')
            ax2.set_ylabel('Liczba Pi')
            ax2.set_xlabel('n')

            ax2.scatter(np.arange(i+1-step, i+1), lista_pi_result[i-step:i], c='g', marker='x')
            ax2.scatter(np.arange(i+1-step, i+1), [np.pi]*step, c='r', marker=0)
            plt.pause(czas)

            ax3 = fig.add_subplot(223)
            ax3.set_title('Histogram')
            ax3.hist(lista_pi_result[i-step:i], color='b', bins=[0, 1, 2, 3, 4])
            plt.pause(czas)
    print("czas = ", time.time() - time0)

    plt.show()


window.mainloop()
