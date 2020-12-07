import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

VARIABLE_2D = 2
VARIABLE_3D = 3


def pi(number_of_points, points_inside, loop_point_number):
    points = np.random.rand(number_of_points, dimension_variable.get())
    points_vector_bool = np.sqrt(np.sum(points ** 2, axis=1)) < 1

    points_inside_matrix = np.ones(number_of_points) * points_inside
    pi_results = np.zeros(number_of_points)

    for point in range(number_of_points):
        points_inside_matrix[point] += np.sum(points_vector_bool[:point + 1])

        if dimension_variable.get() == VARIABLE_2D:
            pi_results[point] = points_inside_matrix[point] / (point + loop_point_number + 1) * 4

        else:
            pi_results[point] = points_inside_matrix[point] / (point + loop_point_number + 1) * 6

    points_inside = points_inside_matrix[number_of_points - 1]

    return points, points_vector_bool, pi_results, points_inside


def initial_axes():
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
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")

    ax1.set_title('Losowe Punkty')

    ax2 = fig.add_subplot(222)
    ax2.set_title('Liczba Pi')
    ax2.set_ylabel('Liczba Pi')
    ax2.set_xlabel('Liczba punktów')

    ax3 = fig.add_subplot(223)
    ax3.set_title('Histogram')

    return ax1, ax2, ax3


def plots(ax1, ax2, ax3, number_of_points, random_points, points_vector_bool, pi_results, loop_point_number):
    break_time = 0.0001

    if dimension_variable.get() == VARIABLE_2D:
        ax1.scatter(random_points[points_vector_bool, 0], random_points[points_vector_bool, 1], c='b')  # inside
        ax1.scatter(random_points[points_vector_bool == False, 0], random_points[points_vector_bool == False, 1], c='r',
                    marker='x')

    else:
        ax1.scatter(random_points[points_vector_bool, 0], random_points[points_vector_bool, 1],
                    random_points[points_vector_bool, 2], c='b')  # inside
        ax1.scatter(random_points[points_vector_bool == False, 0], random_points[points_vector_bool == False, 1],
                    random_points[points_vector_bool == False, 2], c='r', marker='x')

    plt.pause(break_time)

    ax2.scatter(np.arange(loop_point_number, loop_point_number + number_of_points),
                pi_results[loop_point_number:loop_point_number + number_of_points], c='g', marker='x')
    ax2.scatter(np.arange(loop_point_number, loop_point_number + number_of_points), [np.pi] * number_of_points, c='r',
                marker=0)
    plt.pause(break_time)

    ax3.hist(pi_results[:loop_point_number + number_of_points], bins=np.arange(0, 8, 0.25), color='b')

    plt.pause(break_time)


def figures():
    pi_results = np.zeros(number_of_points_variable.get())
    points_inside = 0

    ax1, ax2, ax3 = initial_axes()

    if starting_points_variable.get() > 0:
        random_points, points_vector_bool, temporary_pi_results, points_inside = pi(starting_points_variable.get(),
                                                                                    points_inside, 0)
        pi_results[:starting_points_variable.get()] = temporary_pi_results

        plots(ax1, ax2, ax3, starting_points_variable.get(), random_points, points_vector_bool, pi_results, 0)

    incomplete_loop_points = (number_of_points_variable.get() - starting_points_variable.get()) % \
                              step_points_variable.get()
    number_of_complete_loops = (number_of_points_variable.get() - starting_points_variable.get()) // \
                                step_points_variable.get()

    if incomplete_loop_points > 0:
        for loop_point_number in range(starting_points_variable.get(), number_of_points_variable.get() -
                                 step_points_variable.get(), step_points_variable.get()):
            random_points, points_vector_bool, temporary_pi_results, points_inside = pi(step_points_variable.get(),
                                                                                        points_inside,
                                                                                        loop_point_number)
            pi_results[loop_point_number:loop_point_number + step_points_variable.get()] = temporary_pi_results

            plots(ax1, ax2, ax3, step_points_variable.get(), random_points, points_vector_bool, pi_results,
                  loop_point_number)

        random_points, points_vector_bool, temporary_pi_results, points_inside = pi(incomplete_loop_points,
                                                                                    points_inside,
                                                                                    number_of_points_variable.get() -
                                                                                    incomplete_loop_points)
        pi_results[number_of_points_variable.get() - incomplete_loop_points:] = temporary_pi_results

        plots(ax1, ax2, ax3, incomplete_loop_points, random_points, points_vector_bool, pi_results,
              number_of_complete_loops * step_points_variable.get())

    else:

        for loop_point_number in range(starting_points_variable.get(), number_of_points_variable.get(),
                                 step_points_variable.get()):
            random_points, points_vector_bool, temporary_pi_results, points_inside = pi(step_points_variable.get(),
                                                                                        points_inside,
                                                                                        loop_point_number)
            pi_results[loop_point_number:loop_point_number + step_points_variable.get()] = temporary_pi_results

            plots(ax1, ax2, ax3, step_points_variable.get(), random_points, points_vector_bool, pi_results,
                  loop_point_number)

    plt.show()


def entry_field(variable, text, row, label_column):
    label = tk.Label(window, text=text)
    label.grid(row=row, column=label_column, padx=10, pady=10, ipady=10)
    variable_str = tk.Entry(window, textvariable=variable)
    variable_str.grid(row=row, column=label_column + 1, padx=10, pady=10, ipady=10)


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

start_button = tk.Button(window, text="Start", command=lambda: figures())
start_button.grid(row=0, column=3, padx=10, pady=10, ipady=10)

starting_points_variable = tk.IntVar()
entry_field(starting_points_variable, "Podaj początkową liczbę punktów", 1, 1)

step_points_variable = tk.IntVar()
step_points_variable.set(1)
entry_field(step_points_variable, "Podaj krok", 2, 1)

window.mainloop()
