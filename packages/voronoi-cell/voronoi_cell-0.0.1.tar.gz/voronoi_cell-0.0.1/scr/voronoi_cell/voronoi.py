import itertools import product
import numpy as np

def VCell(Q, **rangeorlist):
    if np.linalg.det(np.array(Q)) <=0: 
        raise Exception("your matrix is not positive-definite.")
        return "your matrix is not positive-definite."
    if (np.array(Q).transpose() != np.array(Q)).any():
        raise Exception("your matrix is not symmetric.")
        return "your matrix is not symmetric."
    d = len(Q)
    if "range" in rangeorlist:
        r = rangeorlist["range"]
        if (r <= 0):
            raise Exception("The range must be a positive integer.")
        p = [list(vec) for vec in product(range(-r, r+1), repeat=d)]
        p.remove([0] * d)
    elif "list" in rangeorlist:
        p = rangeorlist["list"]
    else:
        raise Exception("A range or list of potential relevant vectors needs to be given.")
    ineqs = []
    for vert in p:
        #Collect an inequality for each potential relevant vector (not all may be useful)
        #equation is -2 v^T.Q.x + v^T . Q . v >= 0
        b = 0
        for i in range(d):
            for j in range(d):
                b += vert[i]*Q[i][j]*vert[j]
        vec = [-2*sum([vert[i]*Q[i][j] for i in range(d)]) for j in range(d)]
        ineqs += [tuple([b] + vec)]
    VC = Polyhedron(ieqs = ineqs)
    if VC.volume() != 1:
        raise Exception("relevant vector list not complete")
    return VC