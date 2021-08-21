from typing import List, Sized
import numpy as np
import itertools
from numpy.lib import tracemalloc_domain

# gotta make is valid into a different file
def is_valid_nonogram(cords:List[List[List[int]]]) -> bool:
    """Checks if a list of cordinations describe a real nonogram
    parameters
    -----------
    :cords: list of cordinationsf
    """
    size = (len(cords[0]), len(cords[1]))
    for x in cords[0]: #duplicated code must create a function
        if(len(x) > 1 and sum(x) == len(cords[1])):
            print("you cant split a full row")
            return False
        if(len(x) == 0):
            print("empty cords must contain 0")
            return False
        if(sum(x) > size[1]):
            print("sum of some cord is larger then capacity")
            return False
    for y in cords[1]:
        if(len(y) > 1 and sum(y) == len(cords[0])):
            print("you cant split a full row")
            return False
        if(len(y) == 0):
            print("empty cords must contain 0")
            return False
        if(sum(y) > size[0]):
            print("sum of some cord is larger then capacity")
            return False
    return True

def cord_depicts_arr(arr:List[int], cords:List[int]) -> bool:
    """returns whether an array depicts a cord 
    ex: [1,0,1,1,0], [1,2] -> True
    parameters
    ------------
    :arr: one dimentional numpy array of ints
    :cords: list of ints
    """
    #runtime must be very low
    cord_counter = np.zeros((len(cords),),dtype = int)
    j = 0
    visited = False
    for i in arr:
        if(i == 1):
            visited = True
            cord_counter[j] += 1
        if(visited and i != 1):
            if(cord_counter[j] != cords[j]):
                return False
            j += 1
            visited = False
    for j in range(cord_counter.size):
        if(cord_counter[j] != cords[j]):
            return False
    return True

def create_nonogram_np(cords:List[List[List[int]]]) -> np.ndarray:
    """creates a boolean matrix from cord dimentions
    parameters
    ------------
    :cords: list of nonogram cordinations 

    :treturn: numpy boolean matrix
    """
    return (np.full((len(cords[1]),len(cords[0])), 0, dtype=int))

def shove_to_arr(arr:List[int], cord:int) -> np.ndarray:
    """function gets a number and shoves it after a sequance of ones in arr
    ex -> 2, [1, 0, 0, 0, 0] -> [1, 0, 1, 1, 0]
    parameters
    ------------
    :arr: one dimentional numpy array of ints
    :cord: int, describes number of ones to shove to arr
    """
    i = arr.size - 1
    while(arr[i] == 0 and i != 0):
        i -= 1
    if(i != 0 or (arr[0] == 1 and i == 0)):
        i += 2
    boundary = arr.size - i
    if(boundary < cord):
        raise IndexError

    for _ in range(cord):
        arr[i] = 1
        i += 1
    return arr

def remove_from_arr(arr:List[int], cord:int) -> np.ndarray:
    """function returns an array after removing cord's number of ones from every block in array
    ex: [1,1,1,1,0,1,1,1], 2 -> [0,0,1,1,0,0,0,1]
    parameters
    ------------
    :arr: one dimentional numpy array of ints
    :cord: int, describes number of ones to remove from- arr
    """
    i = 0
    while(i < arr.size):
        if(arr[i] == 1):
            count = 0
            while(count != cord and arr[i] == 1 and i < arr.size):
                arr[i] = 0
                count += 1
                i += 1
            while(i < arr.size and arr[i] == 1):
                i += 1
        i += 1

def nonogram_logics(mat:List[List[int]], cords:List[List[List[int]]]) -> np.ndarray:
    """solves the nonogram via normal logistics (human capable)
    parameters
    ------------
    :mat: numpy boolean matrix
    :cords: list of nonogram cordinations

    :treturn: numpy boolean matrix
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
    for y in range(len(cords[0])):
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

    #finalize
    # cords that describe a solved row, should be filled with -1
    # ex: [1,1] [1,0,0,1] -> [1,-1,-1,1]
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

def is_solved(mat, cords) -> bool:
    for x in range(len(cords[0])):
        if(not cord_depicts_arr(mat[:,x], cords[0][x])):
            return False
    for y in range(len(cords[1])):
        if(not cord_depicts_arr(mat[y,:], cords[1][y])):
            return False
    return True

def generate_nonogram_solution(mat, cords):
    filled_sum = sum(cords[0])
    for x in mat:
        pass

def main():
    cords = [[[1],[1,2],[1]] , [[1],[1,1],[1],[1]]]
    mat = np.array([[0,1,0],[1,0,1],[0,1,0],[0,1,0]], dtype=int)
    #cords = [[[10], [1], [7], [1,7], [1,1], [1,1], [1,1,2], [1,2], [1,1], [1,1]],[[7,2], [1,1], [1,8], [1,3], [1,2], [1,2,2], [1,2,2], [1,1],[1,1],[1]]]
    
    empty_mat = create_nonogram_np(cords)
    print(is_valid_nonogram(cords))
    nonogram_logics(empty_mat,cords)
    print(empty_mat)
    print(is_solved(empty_mat, cords))
    
if __name__ == "__main__":
    main()