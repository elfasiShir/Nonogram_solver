from typing import List, Sized
import numpy as np
from .nonogram_tools import *

def nonogram_logics(mat:List[List[int]], cords:List[List[List[int]]]) -> np.ndarray:
    """solves the nonogram via normal logistics (human capable)
    ------------
    :mat: numpy int matrix
    :cords: list of nonogram cordinations

    :treturn: numpy int matrix
    """
    #logical 1:
    #cord equal to grid size
    for x in range(len(cords[0])):
        if(cords[0][x][0] == mat[:,x].size): 
            mat[:,x] = 1
        
    for y in range(len(cords[1])):
        if(cords[1][y][0] == mat[y,:].size):
            mat[y,:] = 1
    
    #cord depicts a full row with breaks (ex: "1,1" depicts a full row: "true false true")
    for x in range(len(cords[0])):
        if((sum(cords[0][x]) + (len(cords[0][x]) - 1) ) == mat[:,x].size):
            mat[:,x] = 1           
            for i in range(len(cords[0][x]) - 1 ):
                mat[cords[0][x][i],x] = -1

    for y in range(len(cords[1])):
        if((sum(cords[1][y]) + (len(cords[1][y]) - 1) ) == mat[y,:].size):
            mat[y,:] = 1
            for i in range(len(cords[1][y]) - 1 ):
                mat[y,cords[1][y][i]] = -1
    
    #cord dipicts sequance that can fill more then half row
    #!in this instance there is danger of changing exsiting filled node!
    for x in range(len(cords[0])):
        depicted_cord_sum = (sum(cords[0][x]) + (len(cords[0][x]) - 1))
        if((depicted_cord_sum > mat[:,x].size/2) and (depicted_cord_sum != mat[:,x].size)):
            temp_array = np.zeros(mat[:,x].shape,dtype=int)
            residual =  mat[:,x].size - depicted_cord_sum
            for cord in cords[0][x]:
                shove_to_arr(temp_array, cord)
            remove_from_arr(temp_array, residual)
            for i in range(mat[:,x].size):
                if(mat[:,x][i] == 0):
                    #we can change 1 > 1 and 0 > 1 but we cant change -1 > 1
                    mat[:,x][i] = temp_array[i]
    for y in range(len(cords[1])):
        depicted_cord_sum =(sum(cords[1][y]) + (len(cords[1][y]) - 1))
        if((depicted_cord_sum > mat[y,:].size/2) and (depicted_cord_sum != mat[y,:].size)):
            temp_array = np.zeros(mat[y,:].shape,dtype=int)
            residual =  mat[y,:].size - depicted_cord_sum
            for cord in cords[1][y]:
                shove_to_arr(temp_array, cord)
            remove_from_arr(temp_array, residual)
            for i in range(mat[y,:].size):
                if(mat[y,:][i] == 0):
                    #we can change 1 > 1 and 0 > 1 but we cant change -1 > 1
                    mat[y,:][i] = temp_array[i]
    #all that left is to finalize
    nonogram_finalize(mat, cords)

def nonogram_finalize(mat, cords):
    """finalizes the nonogram
    cords that describe a solved row, should be filled with -1
    ex: [1,1] [1,0,0,1] -> [1,-1,-1,1]
    """
    for x in range(len(cords[0])):
        if(cord_depicts_arr(mat[:,x],cords[0][x])):
            for i in range(mat[:,x].size):
                if(mat[:,x][i] == 0):
                    mat[:,x][i] = -1
    for y in range(len(cords[1])):
        if(cord_depicts_arr(mat[y,:],cords[1][y])):
            for i in range(mat[y,:].size):
                if(mat[y,:][i] == 0):
                    mat[y,:][i] = -1