from typing import List, Sized
import numpy as np
import itertools
from numpy.lib import tracemalloc_domain
from nonogram_logistics import nonogram_finalize, nonogram_logics
from nonogram_tools import *

error_depot = {
    "CORD_SUM_IS_NOT_SAME" : "cord dimentions need to depict the same amount of nodes",
    "SPLITED_ROW" : "you cant split a full row",
    "MUST_ZERO" : "empty cords must contain 0",
    "NO_SPACE" : "sum of some cord is larger then capacity"
}
def is_valid_nonogram(cords:List[List[List[int]]]) -> str:
    """Checks if a list of cordinations describe a real nonogram
    parameters
    -----------
    :cords: list of cordinations

    :treturn: string,  "" if no errors, otherwise ERROR 
    """
    if(sum([sum(x) for x in cords[1]]) != sum([sum(x) for x in cords[0]])):
        return error_depot["CORD_SUM_IS_NOT_SAME"]
        
    error = check_dimention(cords, 0)
    if (error):
        return error

    error = check_dimention(cords, 0)
    if (error):
        return error

    return ""
def check_dimention(cords:List[List[List[int]]], dim:int) -> str:
    """does simple checks for the sake of not duplicating code in is_valid_nonogram
    """
    if(dim == 1):
        other_dim = 0
    else: 
        other_dim = 1
    shape = (len(cords[0]), len(cords[1]))
    for x in cords[dim]:
        if(len(x) > 1 and sum(x) == len(cords[1])):
            return error_depot["SPLITED_ROW"]         
        if(len(x) == 0):
            return error_depot["MUST_ZERO"]
        if(sum(x) > shape[other_dim]):
            return error_depot["NO_SPACE"]
    return ""

def create_nonogram_np(cords:List[List[List[int]]]) -> np.ndarray:
    """creates a boolean matrix from cord dimentions
    parameters
    ------------
    :cords: list of nonogram cordinations 

    :treturn: numpy boolean matrix
    """
    return (np.full((len(cords[1]),len(cords[0])), 0, dtype=int))

def is_solved(mat:List[List[int]], cords:List[List[List[int]]]) -> bool:
    """returns if the matrix is solved or not depending on the cordination
    ---------------
    :mat: numpy int matrix
    :cords: list of nonogram cordinations

    :treturn: bool
    """
    for x in range(len(cords[0])):
        if(not cord_depicts_arr(mat[:,x], cords[0][x])):
            return False
    for y in range(len(cords[1])):
        if(not cord_depicts_arr(mat[y,:], cords[1][y])):
            return False
    return True
    
def generate_nonogram_solution(mat:List[List[int]], cords:List[List[List[int]]]) -> any:
    """ generate a possibility and checks if it depicts cords, does not return anything
    --------
    :mat: numpy int matrix
    :cords: list of nonogram cordinations
    """
    lst_zeros = array_zeros(mat)
    sum_mat_ones = 0 
    for row in mat:
        for node in row:
            if(node == 1):
                sum_mat_ones += 1 
    needed_ones_sum = sum_cords(cords) - sum_mat_ones
    size = sum_zero(mat)
    for iteration in itertools.product(np.array([1,0], dtype=bool), repeat = size):
        if(sum(iteration) == needed_ones_sum):
            for i in range(size):
                if(iteration[i]):
                    mat[lst_zeros[i][0],lst_zeros[i][1]] = 1
            if(is_solved(mat, cords)):
                nonogram_finalize(mat, cords)
                return
            for node in lst_zeros:
                mat[node] = 0

def main():
    #cords = [[[1],[1,2],[1]] , [[1],[1,1],[1],[1]]]
    cords = [[[10], [1], [7], [1,7], [1,1], [1,1], [1,1,2], [1,2], [1,1], [1,1]],[[7,2], [1,1], [1,8], [1,2], [1,2], [1,2,2], [1,2,2], [1,1],[1,1],[1]]]
    print(is_valid_nonogram(cords))
    empty_mat = create_nonogram_np(cords)
    nonogram_logics(empty_mat, cords)
    generate_nonogram_solution(empty_mat,cords)
    print(empty_mat)
if __name__ == "__main__":
    main()