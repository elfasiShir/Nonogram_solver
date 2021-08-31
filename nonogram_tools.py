from typing import List, Sized
import numpy as np

def cord_depicts_arr(arr:List[int], cords:List[int]) -> bool:
    """returns whether an array depicts a cord 
    ex: [1,0,1,1,0], f-> True
    parameters
    ------------
    :arr: one dimentional numpy array of ints
    :cords: list of ints
    """
    #runtime must be very low
    cord_counter = np.zeros((len(cords),),dtype = int)
    cord_counter_size = cord_counter.size
    j = 0
    visited = False
    for i in arr:
        if(j == cord_counter_size):
            break
        if(i == 1):
            visited = True
            cord_counter[j] += 1
        if(visited and i != 1):
            if(cord_counter[j] != cords[j]):
                return False
            j += 1
            visited = False
    for j in range(cord_counter_size):
        if(cord_counter[j] != cords[j]):
            return False
    return True

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


def sum_zero(mat:List[List[int]]) -> int:
    """returns the number of zeros left in a nonogram matrix
    -------------
    :mat: nonogram numpy matrix

    :treturn: int
    """
    sum = 0
    for row in mat:
        for node in row: 
            if(node == 0):
                sum += 1
    return sum

def array_zeros(mat:List[List[int]]) -> List[tuple[int]]:
    """makes an array that describes the location of every zero in the nonogram
    ---------
    :mat: numpy matrix  
    """
    arr = []
    shape = mat.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if(mat[i][j] == 0):
                arr.append((i,j))
    return arr

def sum_cords(cords:List[List[List[int]]]) -> int:
    """ sum one dimention of cords
    ex: [[[1],[1,2],[1]] , [[1],[1,1],[1],[1]]] -> 5
    -------
    :cords: list of nonogram cordinations
    """
    sum = 0
    for cord in cords[0]:
        for i in cord:
            sum += i
    return sum
