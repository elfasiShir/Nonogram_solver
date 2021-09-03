from django.shortcuts import render
import numpy as np

from .nonogram.nonogram_main import *
from .nonogram.nonogram_logistics import *
from .nonogram.nonogram_tools import *
ERROR_DEPOT = {
    "NO_KAMA" : "dimentions should be seperated by kama",
    "MAX_DIM" : "there must be maximum two dimentions in a nonogram matrix",
    "TYPE_ER" : "dim should look like: 3,4 1,2 10,10",
    "TOO_BIG" : "nonogram above 10dim will take a long time, and above 15 too long",
    "VALUE_ERROR" : "ValueError: dimention should be an integer",
    "INVALID_DIM" : "minimum dimentions are: 1,1",
}
# Create your views here.
def dim_web(request):
    return render(request, 'dim/dim.html')

def cord_web(request):
    str_dim = request.GET.get("dim", "")
    dim = []
    range_x = []
    range_y = []
    if("," not in str_dim):
        return render(request, 'dim/dim.html', {"error" : ERROR_DEPOT["NO_KAMA"]})
    try:
        dim = str_dim.split(",")
        for i in range(len(dim)):
            dim[i] = int(dim[i])
    except ValueError:
        return render(request, 'dim/dim.html', {"error" : ERROR_DEPOT["VALUE_ERROR"]})
    if(len(dim) != 2 ):
         return render(request, 'dim/dim.html', {"error" : ERROR_DEPOT["MAX_DIM"]})
    if(dim[0] > 15 or dim[1] > 15):
        return render(request, 'dim/dim.html', {"error" : ERROR_DEPOT["TOO_BIG"]})
    if(dim[0] < 1 or dim[1] < 1):
        return render(request, 'dim/dim.html', {"error" : ERROR_DEPOT["INVALID_DIM"]})
    for i in range(dim[1] + 1):
        range_x.append(i)
    for j in range(dim[0] + 1):
        range_y.append(j)
    return render(request, 'cord/cord.html', { "dim": tuple(dim), "range_x": range_x ,"range_y" : range_y})

def generate_web(request):
    """
    #mat = np.array([])
    cords = [[],[]]
    str_dim = request.GET.get("dim", "")
    dim = str_dim.split(",")
    for i in range(len(dim)):
        dim[i] = int(dim[i])
    """
    
    cords = [[],[]]
    i = 1
    j = 0
    while(True):
        try:
            name = "mat_" + str(i) + "_" + str(j)
            str_temp = request.GET.get(name, "")
            cord = str_temp.split(",")
            for c in range(len(cord)):
                cord[c] = int(cord[c])
            cords[1].append(cord)
            i += 1
        except:
            break
    i = 0
    j = 1
    while(True):
        try:
            name = "mat_" + str(i) + "_" + str(j)
            str_temp = request.GET.get(name, "")
            cord = str_temp.split(",")
            for c in range(len(cord)):
                cord[c] = int(cord[c])
            cords[0].append(cord)
            j += 1
        except:
            break    
    if(cords == [[],[]]):
        return render(request, 'cord/cord.html', {"error" : "cord error"})

    error = is_valid_nonogram(cords)
    if(error != ""):
        return render(request, 'cord/cord.html', {"error" : error})
    
    mat = create_nonogram_np(cords)
    nonogram_logics(mat, cords)
    final_msg = generate_nonogram_solution(mat, cords)

    return render(request, 'generate/generate.html', {"mat" : mat, "cords" : cords, "final_msg" : final_msg})

    
    
