import numpy as np


def calc_matrix(data):
    priority_map = {item: index for index, group in enumerate(data)
                    for item in (group if isinstance(group, list) else [group])}

    size = len(priority_map)
    return [[1 if priority_map[col] >= priority_map[row] else 0
             for col in range(1, size + 1)] for row in range(1, size + 1)]


def calc_uhon(X, Y):
    X, Y = np.array(X), np.array(Y)
    print(np.logical_or(X * Y, X.T * Y.T))


data1 = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
data2 = [[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]

def main (data1, data2):
    matrix1 = calc_matrix(data1)
    matrix2 = calc_matrix(data2)

    calc_uhon(matrix1, matrix2)
main(data1,data2)