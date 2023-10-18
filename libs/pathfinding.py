
from libs.vectors import *

def pathfindingReconstruct(parents, v):
    res = [v]
    while (v in parents):
        v = parents[v]
        res = [v]+res
    return res

def pathfindingAStar(a,b, blocked=[], maxIteration=999):
    vstart = Vector(a)
    vend = Vector(b)
    
    dim = len(vstart)
    offsets = []
    for i in range(dim):
        for v in [-1,1]:
            vec = [0 for _ in range(dim)]
            vec[i] = v
            offsets.append(Vector(vec))

    fCost = {vstart: 0}
    gCost = {vstart: 0}
    cellsParent = {}
    cellsOpen = [vstart]
    
    it = 0
    while len(cellsOpen)>0 and it<maxIteration:
        it+=1
        
        current = None
        for vec in cellsOpen:
            if current==None or fCost[vec]<fCost[current]:
                current = vec

        if current==vend:
            return pathfindingReconstruct(cellsParent, vend)
        cellsOpen.remove(current)

        # calculate neighboors
        for offset in offsets:
            neigh = current + offset
            if not(neigh in blocked):
                newGCost = gCost[current] + 1 # 1 is always the distance
                if not(neigh in gCost) or newGCost < gCost[neigh]:
                    cellsParent[neigh] = current
                    
                    gCost[neigh] = newGCost
                    fCost[neigh] = newGCost + vend.mag(neigh)
                    if not(neigh in cellsOpen):
                        cellsOpen.append(neigh)
