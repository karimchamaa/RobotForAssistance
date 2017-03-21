import numpy 
from PIL import Image


def Generate():
    MatrixImage=numpy.asarray(Image.open('Maze.jpg').convert('L'))
    the_map= [[0 for x in range(len(MatrixImage[0]))] for y in range(len(MatrixImage))]
    for i in range(len(MatrixImage)):#Row
        for j in range (len(MatrixImage[0])):# Column
            if MatrixImage[i][j]<125:#Black
                the_map[i][j]=1
            else:
                the_map[i][j]=0
                
    n = len(the_map[0]) 
    m = len(the_map)
    return n,m,the_map

def Print(dx,dy,route,yA,xA,yB,xB,n,m,the_map):
    RowMapped=list()
    ColMapped=list()
    if len(route) > 0:
        x = xA
        y = yA
        ColMapped.append(x)
        RowMapped.append(y)
        the_map[y][x] = 2
        for i in range(len(route)):
            j = int(route[i])
            x += dx[j]
            y += dy[j]
            ColMapped.append(x)
            RowMapped.append(y)
            the_map[y][x] = 3
        the_map[y][x] = 4
    print 'Start: ', yA, xA
    print 'Finish: ', yB, xB
    print 'Map:'
    for y in range(m):
        for x in range(n):
            xy = the_map[y][x]
            if xy == 0:
                print '.', # space
            elif xy == 1:
                print 'O', # obstacle
            elif xy == 2:
                print 'S', # start
            elif xy == 3:
                print 'R', # route
            elif xy == 4:
                print 'F', # finish
        print
    return RowMapped, ColMapped


