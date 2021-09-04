![banner](https://user-images.githubusercontent.com/71436829/132109244-f473aa7b-1a6a-444d-baef-9d9cc101484c.png)
# Website

[bearwulf.pythonanywhere.com](http://bearwulf.pythonanywhere.com)

## How to use
- Dimention and cordinates should be depicted as ints seperated by kama
.ex: "3,2", "10,10"
- Usually dimentions above 10 will take a long time to load 
-----
## Node modes:
-  1 : True "marked in" node 
- -1 : False, "marked out" node, as in, cannot be marked 1
-  0 : "unmarked" node can be 1 or -1
# Code
`Nonogram_solver/Nonogram_web/nonogram_web/nonogram/ `
<br/>The main process of solving a nonogram is as follows:
- Validate the cordinates
- Create the matrix
- Apply logical functions to mark the nodes 
- use brute force for the remaining unmarked nodes.
