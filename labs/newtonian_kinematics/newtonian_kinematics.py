# kinematics_regression.py


import matplotlib.pyplot as plt
import numpy as np

def fit_quadratic(vec_x, vec_y):

    sum_x = sum(vec_x)
    sum_x2 = sum(vec_x**2)
    sum_x3 = sum(vec_x**3)
    sum_x4 = sum(vec_x**4)

    sum_y = sum(vec_y)
    sum_xy = sum(vec_x * vec_y)
    sum_x2y = sum(vec_x**2 * vec_y)

    coeffs = np.array([
        [sum_x4, sum_x3, sum_x2],
        [sum_x3, sum_x2, sum_x],
        [sum_x2, sum_x, len(vec_x)]])

    vals = np.array([sum_x2y, sum_xy, sum_y])

    det_coeffs = np.linalg.det(coeffs)

    mat_a = np.copy(coeffs)
    mat_a[:, 0] = vals
    det_a = np.linalg.det(mat_a)

    mat_b = np.copy(coeffs)
    mat_b[:, 1] = vals
    det_b = np.linalg.det(mat_b)

    mat_c = np.copy(coeffs)
    mat_c[:, 2] = vals
    det_c = np.linalg.det(mat_c)

    a = det_a / det_coeffs
    b = det_b / det_coeffs
    c = det_c / det_coeffs

    return a, b, c


def main():
    plt.figure(__file__)
    ax = plt.axes()

    file_name = "newtonian_kinematics.csv"
    data = np.genfromtxt(file_name, delimiter=",")

    vec_x = data[:, 0]
    vec_y = data[:, 1]

    a, b, c = fit_quadratic(vec_x, vec_y)

    acceleration = a * 2
    initial_velocity = b

    print(f"Constant acceleration = {acceleration:.4f} m/s^2")
    print(f"     Initial velocity = {initial_velocity:.4f} m/s")

    x = np.linspace(np.min(vec_x), np.max(vec_x), 1000)
    ax.plot(x, a * x**2 + b * x + c)

    ax.scatter(vec_x, vec_y, color="red")

    ax.set_title("Newtonian Kinematics")
    ax.set_xlabel("Time (sec)")
    ax.set_ylabel("Distance (m)")
    
    ax.figure.set_size_inches(10, 8)
    plt.savefig("newtonian_kinematics.png", dpi=600)      

    plt.show()


main()
