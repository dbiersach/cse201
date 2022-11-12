# cramers_rule.py

import numpy as np


def main():
    # Declare the 2-dimensional "cofficients" matrix (3 rows x 3 columns)
    coeffs = np.array([[4, 5, -2], [7, -1, 2], [3, 1, 4]])

    # Declare the 1-dimensional "values" vector
    vals = np.array([-14, 42, 28])

    # Calculate determinant of coefficients matrix
    det_coeffs = np.linalg.det(coeffs)

    # Overlay values vector on each column of the coeffs matrix
    # and then calculate the determinant of that "new" matrix
    xa = np.copy(coeffs)
    xa[:, 0] = vals
    det_xa = np.linalg.det(xa)

    ya = np.copy(coeffs)
    ya[:, 1] = vals
    det_ya = np.linalg.det(ya)

    za = np.copy(coeffs)
    za[:, 2] = vals
    det_za = np.linalg.det(za)

    # Use Cramer's rule to solve this system of linear equations
    x = det_xa / det_coeffs
    y = det_ya / det_coeffs
    z = det_za / det_coeffs

    # Display the solutions
    print(f"x = {x}")
    print(f"y = {y}")
    print(f"z = {z}")
    print()

    # Use numpy's linear algebra solver
    sol = np.linalg.solve(coeffs, vals)
    print(f"Numpy Solver: {sol}")


main()
