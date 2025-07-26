def reverse_list(l: list):
    """
    Reverse a list without using any built-in function.
    The function should return a reversed list.
    Input l is a list that may contain any type of data.
    """
    reversed_list = []
    for item in l:
        reversed_list = [item] + reversed_list
    return reversed_list


def solve_sudoku(matrix):
    """
    Write a program to solve a 9*9 Sudoku board.
    The board must be completed so that every row, column and 3*3 exction
    contains all digits from 1 to 9.
    Input: a 9*9 matrix representing the board
    """

    def is_valid(row, col, num):
        if num in matrix[row] or num in [matrix[i][col] for i in range(9)]:
            return False
        if num in [
            matrix[r][c]
            for r in range(row // 3 * 3, row // 3 * 3 + 3)
            for c in range(col // 3 * 3, col // 3 * 3 + 3)
        ]:
            return False
        return True

    def backtrack():
        for row in range(9):
            for col in range(9):
                if matrix[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(row, col, num):
                            matrix[row][col] = num
                            if backtrack():
                                return True
                            else:
                                matrix[row][col] = 0
                    return False
        return True

    return backtrack()


if __name__ == "__main__":
    print(reverse_list(["s", 1, None, [1, 23, 8]]))
    matrix = [
        [5, 0, 4, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    solve_sudoku(matrix)
    print(matrix)
