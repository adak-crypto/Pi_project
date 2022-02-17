import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import math

VARIABLE_2D = 2
VARIABLE_3D = 3


def pi(number_of_points, points_inside, loop_point_number):
    """
    Computing the value of pi

    :param number_of_points: number of points from the Monte Carlo simulation for which the pi number is calculated
    :param points_inside: currently known number of points inside the circle
    :param loop_point_number: the current iteration number of the loop
    :return: points - a matrix with drawn coordinates from the Monte Carlo simulation
             points_vector_bool - a matrix with number_of_points dimension with information if drawn points are inside
             (True) or not (False)
             pi_result - a matrix with number_of_points dimension with counted pi value
             points_inside - number of points inside circle
    """
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
    """
    Generating common figure properties

    :return: figure axes and place for text with currently counted pi value
    """
    fig = plt.figure()
    fig.canvas.manager.full_screen_toggle()

    if dimension_variable.get() == VARIABLE_2D:
        ax1 = fig.add_subplot(221)
        ax1.add_artist(plt.Circle((0, 0), 1, color='m', fill=False))
        ax1.set(xlim=(-0.01, 1.01), ylim=(-0.01, 1.01))
        ax1.set_aspect('equal')
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")

    else:
        ax1 = fig.add_subplot(221, projection='3d')
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")

    ax1.set_title('Losowe Punkty')

    ax2 = fig.add_subplot(222)
    ax2.set_title('Liczba Pi')
    ax2.set_ylabel('Liczba Pi')
    ax2.set_xlabel('Liczba punktów')

    if dimension_variable.get() == VARIABLE_2D:
        ax2.set_ylim(-0.5, 7)

    else:
        ax2.set_ylim(-0.5, 9)

    pi_text = ax2.text(0.95, 0.95, 'pi = ', verticalalignment='top', horizontalalignment='right',
                       transform=ax2.transAxes, color='green', fontsize=15)

    ax3 = fig.add_subplot(223)
    ax3.set_title('Histogram')

    return ax1, ax2, ax3, pi_text


def plots(ax1, ax2, ax3, pi_text, number_of_points, random_points, points_vector_bool, pi_results, loop_point_number):
    """
    Generating and refreshing plots

    :param ax1:  points plot axes properties
    :param ax2:  pi value plot axes properties
    :param ax3: histogram axes properties
    :param pi_text: place for currently counted pi value
    :param number_of_points: number of points for which plots will be refreshed
    :param random_points: coordinates of points from the Monte Carlo simulation
    :param points_vector_bool: information if drawn points are inside
             (True) or not (False)
    :param pi_results: all pi results obtained so far
    :param loop_point_number: the current iteration number of the loop
    """

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

    pi_text.set_text('pi = {:.4f}'.format(pi_results[loop_point_number+number_of_points - 1]))
    plt.pause(break_time)

    ax3.hist(pi_results[:loop_point_number + number_of_points], bins=np.arange(0, 8, 0.25), color='b')

    plt.pause(break_time)


def figures():
    """
    Computing pi value and refreshing plots
    """
    no_errors = errors()

    if no_errors:

        number_of_points = int(number_of_points_variable.get())
        starting_points = int(starting_points_variable.get())
        step_points = int(step_points_variable.get())

        pi_results = np.zeros(number_of_points)
        points_inside = 0

        ax1, ax2, ax3, pi_text = initial_axes()

        if starting_points > 0:
            random_points, points_vector_bool, temporary_pi_results, points_inside = pi(starting_points,
                                                                                        points_inside, 0)
            pi_results[:starting_points] = temporary_pi_results

            plots(ax1, ax2, ax3, pi_text, starting_points, random_points, points_vector_bool, pi_results, 0)

        incomplete_loop_points = (number_of_points - starting_points) % step_points
        number_of_complete_loops = (number_of_points - starting_points) // step_points

        if incomplete_loop_points > 0:
            for loop_point_number in range(starting_points, number_of_points - step_points, step_points):
                random_points, points_vector_bool, temporary_pi_results, points_inside = pi(step_points,
                                                                                            points_inside,
                                                                                            loop_point_number)
                pi_results[loop_point_number:loop_point_number + step_points] = temporary_pi_results

                plots(ax1, ax2, ax3, pi_text, step_points, random_points, points_vector_bool, pi_results,
                      loop_point_number)

            random_points, points_vector_bool, temporary_pi_results, points_inside = pi(incomplete_loop_points,
                                                                                        points_inside,
                                                                                        number_of_points -
                                                                                        incomplete_loop_points)
            pi_results[number_of_points - incomplete_loop_points:] = temporary_pi_results

            plots(ax1, ax2, ax3, pi_text, incomplete_loop_points, random_points, points_vector_bool, pi_results,
                  number_of_complete_loops * step_points)

        else:

            for loop_point_number in range(starting_points, number_of_points, step_points):
                random_points, points_vector_bool, temporary_pi_results, points_inside = pi(step_points,
                                                                                            points_inside,
                                                                                            loop_point_number)
                pi_results[loop_point_number:loop_point_number + step_points] = temporary_pi_results

                plots(ax1, ax2, ax3, pi_text, step_points, random_points, points_vector_bool, pi_results,
                      loop_point_number)

        plt.show()


def entry_field(variable, text, row, label_column):
    """
    Generating an entry field

    :param variable: name of the variable to which the data is written
    :param text: text shown near the entry field
    :param row: position of the entry field
    :param label_column: position of the text
    """
    label = tk.Label(window, text=text)
    label.grid(row=row, column=label_column, padx=10, pady=10, ipady=10)
    variable_str = tk.Entry(window, textvariable=variable)
    variable_str.grid(row=row, column=label_column + 1, padx=10, pady=10, ipady=10)


def alert_popup(title, main_message, comments):
    """
    Generating a pop-up window for error messages
    :param title: title of the message
    :param main_message: main message
    :param comments: explain message
    """
    root = tk.Tk()
    root.title(title)
    window_width = 400     # popup window width
    window_height = 200     # popup window height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_center_position = (screen_width - window_width)/2
    y_center_position = (screen_height - window_height)/2
    root.geometry('%dx%d+%d+%d' % (window_width, window_height, x_center_position, y_center_position))
    message = main_message
    message += '\n'
    message += comments
    popup_window = tk.Label(root, text=message, width=120, height=10)
    popup_window.pack()
    button = tk.Button(root, text="OK", command=root.destroy, width=10)
    button.pack()
    tk.mainloop()


def is_int(number):
    """
    Checking if number is int

    :param number: number to check
    :return: bool
    """
    floor_number = math.floor(number)

    if floor_number == number:
        return True
    else:
        return False


def errors():
    """
    Checking if all variables written by user are correctly

    :return: bool
    """
    no_errors = True

    if not (dimension_variable.get() == VARIABLE_2D or dimension_variable.get() == VARIABLE_3D):

        no_errors = False
        alert_popup("Błąd!", "Nie wybrano wymiaru wykresu", "Wybierz jedną z opcji wykresu")

    if not is_int(number_of_points_variable.get()) or number_of_points_variable.get() < 1:
        no_errors = False
        alert_popup("Błąd!", "Podano złą liczbę wszystkich punktów", "Podaj liczbę naturalną dodatnią")

    if not is_int(starting_points_variable.get()) or starting_points_variable.get() > number_of_points_variable.get() \
            or starting_points_variable.get() < 0:
        no_errors = False
        alert_popup("Błąd!", "Podano złą liczbę punktów początkowych", "Podaj liczbę naturalną mniejszą lub równą "
                                                                       "liczbie wszystkich punktów")

    if not is_int(step_points_variable.get()) or step_points_variable.get() < 1:
        no_errors = False
        alert_popup("Błąd!", "Podano złą długość kroku", "Podaj liczbę naturalną dodatnią")

    return no_errors


window = tk.Tk()
window.geometry("600x200")
window.title("Monte Carlo - Wyznaczanie liczby Pi")

dimension_variable = tk.IntVar()
radio_button_2_d = tk.Radiobutton(window, text="Wykres 2D", variable=dimension_variable, value=VARIABLE_2D)
radio_button_2_d.grid(row=0, column=0, padx=10, pady=10, ipady=10)

radio_button_3_d = tk.Radiobutton(window, text="Wykres 3D", variable=dimension_variable, value=VARIABLE_3D)
radio_button_3_d.grid(row=1, column=0, padx=10, pady=10, ipady=10)


number_of_points_variable = tk.DoubleVar()
number_of_points_variable.set(1)
entry_field(number_of_points_variable, "Podaj liczbę wszystkich punktów", 0, 1)

start_button = tk.Button(window, text="Start", command=lambda: figures())
start_button.grid(row=0, column=3, padx=10, pady=10, ipady=10)

starting_points_variable = tk.DoubleVar()
starting_points_variable.set(0)
entry_field(starting_points_variable, "Podaj początkową liczbę punktów", 1, 1)

step_points_variable = tk.DoubleVar()
step_points_variable.set(1)
entry_field(step_points_variable, "Podaj długość kroku", 2, 1)

window.mainloop()
