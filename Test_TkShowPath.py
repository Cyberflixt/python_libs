
import tkinter as tk
import libs.pathfinding as pathfinding
from libs.vectors import *







### TK


#wsx = vecSize.x*cellSize + cellSpace*(vecSize.x-1)
#wsy = vecSize.y*cellSize + cellSpace*(vecSize.y-1)

fen = tk.Tk() # cration de l'objet "fenêtre"
fen_longeur = fen.winfo_screenwidth()
fen_hauteur = fen.winfo_screenheight()
fen.geometry(f'{1500}x{900}') # fenetre de la taille de l'écran
fen.title('Pathfinding')

can = tk.Canvas(fen, bg = 'white') # création d'une zone de dessin
can.pack(fill = tk.BOTH, expand = True)

def displayPathfind(vecA,vecB, obstacles=[]):
    path = pathfinding.pathfindingAStar(vecA,vecB, obstacles)
    if not path:
        raise Exception('Could not pathfind')
    
    minVec, maxVec = Vector.bounds(path)
    
    cellSize = 20
    cellSpace = 2
    cellExtra = 2
    vecSize = maxVec-minVec+1 + cellExtra*2

    anchor = Vector(minVec)*(cellSize+cellSpace)
    
    can.delete('all')

    for y in range(vecSize.y):
        for x in range(vecSize.x):
            vec = minVec+[x,y]-cellExtra
            i = 0
            if vec in obstacles: i = 1
            if vec==vecA or vec==vecB: i = 5
            if vec in path:
                i = 2
                if vec==vecA: i = 3
                if vec==vecB: i = 4
            
            colors = ['white', 'red','#00A0FF','#0030FF','#00FFFF','#FF00FF']
            
            pos = Vector(x,y)
            rectPos = pos*(cellSize+cellSpace)+anchor
            
            rect = can.create_rectangle(
                *rectPos,
                *(rectPos+cellSize),
                
                fill = colors[i],
                outline = 'grey',
            )
    
    def canvasClicked(e):
        mp = Vector(e.x,e.y)-anchor
        cellAnchor = mp//(cellSize+cellSpace)
        vec = cellAnchor + minVec - cellExtra
        
        if vec in obstacles:
            obstacles.remove(vec)
        else:
            obstacles.append(vec)
        displayPathfind(vecStart,vecEnd, obstacles)
            
    can.bind('<Button-1>', canvasClicked)

walls = [Vector(3,0),Vector(3,1),Vector(3,2),Vector(3,3),
         Vector(3,4),Vector(3,5),Vector(3,6),Vector(3,7),
         Vector(3,8),Vector(3,9),Vector(3,10),Vector(3,11)]

vecStart = Vector(1,4)
vecEnd = Vector(6,8)
displayPathfind(vecStart,vecEnd, walls)

fen.mainloop()



