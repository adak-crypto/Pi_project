import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

import time

VARIABLE_2D = 2
VARIABLE_3D = 3


def pi(number_of_points, points_inside, points_vector_bool, number_of_loop):

    points_inside_matrix = np.ones(number_of_points) * points_inside
    pi_results = np.zeros(number_of_points)

    for i in range(number_of_points):
        points_inside_matrix[i] += np.sum(points_vector_bool[:i + 1])

        if dimension_variable.get() == VARIABLE_2D:
            pi_results[i] = points_inside_matrix[i] / (i + number_of_loop + 1) * 4

        else:
            pi_results[i] = points_inside_matrix[i] / (i + number_of_loop + 1) * 6

    points_inside = points_inside_matrix[number_of_points - 1]

    return pi_results, points_inside


def chart():

    break_time = 0.0001

    pi_results = np.zeros(number_of_points_variable.get())
    points_inside = 0

    fig = plt.figure()

    if dimension_variable.get() == VARIABLE_2D:
        ax1 = fig.add_subplot(221)
        ax1.add_artist(plt.Circle((0, 0), 1, color='m', fill=False))
        ax1.set(xlim=(-0.01, 1.01), ylim=(-0.01, 1.01))
        ax1.set_aspect('equal')
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")

    if dimension_variable.get() == VARIABLE_3D:
        ax1 = fig.add_subplot(221, projection='3d')

    ax1.set_title('Losowe Punkty')

    ax2 = fig.add_subplot(222)
    ax2.set_title('Liczba Pi')
    ax2.set_ylabel('Liczba Pi')
    ax2.set_xlabel('Liczba punktów')

    ax3 = fig.add_subplot(223)
    ax3.set_title('Histogram')

    if starting_points_variable.get() > 0:

        points = np.random.rand(starting_points_variable.get(), dimension_variable.get())
        points_vector_bool = np.sqrt(np.sum(points ** 2, axis=1)) < 1

        # points_inside_matrix = np.zeros(starting_points_variable.get())

        temporary_pi_results, points_inside = pi(starting_points_variable.get(), points_inside, points_vector_bool, 0)
        pi_results[:starting_points_variable.get()] = temporary_pi_results

        # for i in range(starting_points_variable.get()):
        #     points_inside_matrix[i] = np.sum(points_vector_bool[:i+1])
        #
        #     if dimension_variable.get() == VARIABLE_2D:
        #         pi_results[i] = points_inside_matrix[i] / (i + 1) * 4
        #
        #     else:
        #         pi_results[i] = points_inside_matrix[i] / (i + 1) * 6
        #
        # points_inside = points_inside_matrix[starting_points_variable.get() - 1]

        if dimension_variable.get() == VARIABLE_2D:
            ax1.scatter(points[points_vector_bool, 0], points[points_vector_bool, 1], c='b')  # inside
            ax1.scatter(points[points_vector_bool == False, 0], points[points_vector_bool == False, 1], c='r',
                        marker='x')

        else:
            ax1.scatter(points[points_vector_bool, 0], points[points_vector_bool, 1], points[points_vector_bool, 2],
                        c='b')  # inside
            ax1.scatter(points[points_vector_bool == False, 0], points[points_vector_bool == False, 1],
                        points[points_vector_bool == False, 2], c='r', marker='x')

        plt.pause(break_time)

        ax2.scatter(np.arange(starting_points_variable.get()), pi_results[:starting_points_variable.get()], c='g', marker='x')
        ax2.scatter(np.arange(starting_points_variable.get()), [np.pi] * starting_points_variable.get(),
                    c='r', marker=0)
        plt.pause(break_time)

        ax3.hist(pi_results, 20, color='b')
        plt.pause(break_time)

    for i in range(starting_points_variable.get(), number_of_points_variable.get(), step_points_variable.get()):
        points = np.random.rand(step_points_variable.get(), dimension_variable.get())
        points_vector_bool = np.sqrt(np.sum(points ** 2, axis=1)) < 1

        # points_inside_matrix = np.ones(step_points_variable.get()) * points_inside
        # # print("points_inside_matrix początkowe", points_inside_matrix)
        # #pi = np.zeros(step_points_variable.get())
        #
        # for j in range(step_points_variable.get()):
        #
        #     if i + j >= number_of_points_variable.get():
        #         break
        #     points_inside_matrix[j] += np.sum(points_vector_bool[:j + 1])
        #     # print("np.sum(points_vector_bool[:j + 1]) ", np.sum(points_vector_bool[:j + 1]))
        #     # print("points_inside_matrix ", points_inside_matrix[j])
        #
        #     if dimension_variable.get() == VARIABLE_2D:
        #         pi_results[i+j] = points_inside_matrix[j] / (i + j + 1) * 4
        #
        #     else:
        #         pi_results[i+j] = points_inside_matrix[j] / (i + j + 1) * 6
        #
        # points_inside = points_inside_matrix[step_points_variable.get() - 1]



        temporary_pi_results, points_inside = pi(step_points_variable.get(), points_inside, points_vector_bool, i)
        pi_results[i:i+step_points_variable.get()] = temporary_pi_results

        print("points_inside ", points_inside)

        if dimension_variable.get() == VARIABLE_2D:
            ax1.scatter(points[points_vector_bool, 0], points[points_vector_bool, 1], c='b')  # inside
            ax1.scatter(points[points_vector_bool == False, 0], points[points_vector_bool == False, 1], c='r',
                        marker='x')

        else:
            ax1.scatter(points[points_vector_bool, 0], points[points_vector_bool, 1], points[points_vector_bool, 2],
                        c='b')  # inside
            ax1.scatter(points[points_vector_bool == False, 0], points[points_vector_bool == False, 1],
                        points[points_vector_bool == False, 2], c='r', marker='x')

        plt.pause(break_time)

        # print("t shape ", np.arange(i, i + step_points_variable.get()))
        # print("pi shape ", pi_results[i:i + step_points_variable.get()])

        ax2.scatter(np.arange(i, i + step_points_variable.get()), pi_results[i:i + step_points_variable.get()], c='g',
                    marker='x')
        ax2.scatter(np.arange(i, i + step_points_variable.get()), [np.pi] * step_points_variable.get(), c='r', marker=0)
        plt.pause(break_time)

        n, bins, _ = ax3.hist(pi_results[:i + step_points_variable.get()], bins=[0,1,2,3,4,5,6,7,8], color='b', stacked=True)

        # print("n ", n)
        # print("bins ", bins)
        plt.pause(break_time)
    plt.show()


def entry_field(variable, text, row, label_column):

    label = tk.Label(window, text=text)
    label.grid(row=row, column=label_column, padx=10, pady=10, ipady=10)
    variable_str = tk.Entry(window, textvariable=variable)
    variable_str.grid(row=row, column=label_column+1, padx=10, pady=10, ipady=10)


window = tk.Tk()
window.geometry("600x200")
window.title("Monte Carlo - Wyznaczanie liczby Pi")

dimension_variable = tk.IntVar()
radio_button_2_d = tk.Radiobutton(window, text="Wykres 2D", variable=dimension_variable, value=VARIABLE_2D)
radio_button_2_d.grid(row=0, column=0, padx=10, pady=10, ipady=10)

radio_button_3_d = tk.Radiobutton(window, text="Wykres 3D", variable=dimension_variable, value=VARIABLE_3D)
radio_button_3_d.grid(row=1, column=0, padx=10, pady=10, ipady=10)

number_of_points_variable = tk.IntVar()
entry_field(number_of_points_variable, "Podaj liczbę punktów", 0, 1)

start_button = tk.Button(window, text="Start", command=lambda: chart())
start_button.grid(row=0, column=3, padx=10, pady=10, ipady=10)

starting_points_variable = tk.IntVar()
entry_field(starting_points_variable, "Podaj początkową liczbę punktów", 1, 1)


step_points_variable = tk.IntVar()
step_points_variable.set(1)
entry_field(step_points_variable, "Podaj krok", 2, 1)


window.mainloop()
