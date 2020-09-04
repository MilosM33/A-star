import random,numpy
import math
import sys
from heap import heap
from datetime import datetime
from PIL import Image
width = 100
height = 100
started = datetime.now()

def get_neighbours(pos,index,collection = set()):
    temp =[]
    w = width*2
    h = height*2
    #up 
    temp.append((pos[0],pos[1]+index))
    #left
    temp.append((pos[0]-index,pos[1]))
    #right
    temp.append((pos[0]+index,pos[1]))
    #down
    temp.append((pos[0],pos[1]-index))
    temp = list(filter(lambda cell: cell[0] >= 0 and cell[1] >= 0 and cell[0] < w and cell[1] < h and cell not in collection,temp))

        
    
    return temp

#init
maze = []
row1 = []
row2 = []
for x in range(0,width):
    row1.append("|")
    row1.append(" ")
    row2.append("+")
    row2.append("-")

row1.append("|")
row2.append("+")
for y in range(0,height):
    maze.append(list(row2))
    maze.append(list(row1))

maze.append(row2)

stack = []
visited = set()
stack.append((1,1))
visited.add((1,1))
maze[1][1] = "#"
count =0
maxCount = width*height*0.1 
while len(stack) > 0:
    current = stack.pop() 
    neigbours = get_neighbours(current,2,visited)
    count+=1
    if count > maxCount:
        count = 0
        print(len(visited)/(width*height))

    if(len(neigbours) > 0):
        stack.append(current)
        chosen = random.choice(neigbours)
        
        x = (chosen[0] - current[0])//2
        y = (chosen[1] - current[1])//2
        #dir
        if x != 0:
            maze[current[0] + x][current[1]] = "#"
        else:
            maze[current[0]][current[1]+y] = "#"

        maze[chosen[0]][chosen[1]] = "#"
        visited.add(chosen)
        stack.append(chosen)



image = []
for y in maze:
    row1 = []
    for x in y:
        if x == '#':
            row1.append((254,254,254))
        else:
            row1.append((0,0,0))
    image.append(row1)

image = numpy.array(image,dtype=numpy.uint8)
numpy.reshape(image,(width*2+1,height*2+1,3))
#finish
image[1,1] = (0,255,0)
image[width*2-1,height*2-1] = (0,255,0)

saved = Image.fromarray(image,"RGB")
saved.save("labyrint.png","PNG")

#g -distance from start to current node
#h - distance from start to end node
#f - sum of g and h
class Node:
    parrent = None
    def __init__(self,pos,walkable):
        self.pos = pos
        self.f = 0
        self.h = 0
        self.g =0
        self.walk = walkable


#A*
nodes = []
for y in range(0,height*2):
    row = []
    for x in range(0,width*2):
        if maze[y][x] =='#':
            node = Node((y,x),True)
            row.append(node)
        else:
            node = Node((y,x),False)
            row.append(node)
    nodes.append(list(row))
nodes = numpy.array(nodes)
def distance(a,b):
    diffX = abs(a.pos[0] - b.pos[0])
    diffY = abs(a.pos[1] - b.pos[1])
    return 14*min(diffX,diffY) + 10* abs(diffX-diffY)

closed = set()
#openlist = set()
found = False
start = nodes[1,1]
end = nodes[width*2-1,height*2-1]
#openlist.add(start)
print("Path finding")
openlist = heap()
openlist.add(start)
while openlist.length() > 0:

    lowestF = float("inf")
    current = openlist.pop()
    closed.add(current)
    print("Current: " , current.pos, " Exit: " ,end.pos)
    if current == end:
        found = True
        print("Found")
        break 
    for neighbor in get_neighbours(current.pos,1):
        node = nodes[neighbor[0],neighbor[1]]
        skip = False
        
        for y in closed:
            if y.pos== node.pos:
                skip = True
                break
        if skip:
            continue
        if node.walk:
            print(current.pos)
            move = current.g + distance(current,node)
            check = openlist.contains(node)
            if move < node.g or not check:
                node.g = move
                node.h = distance(node,end)
                node.parrent = current

                if not check:
                    openlist.add(node)

if found:
    print("backtrack")
    current = end
    while current != start:
        current = current.parrent
        if current:
            image[current.pos[0],current.pos[1]] = (255,0,0)


image[start.pos[0],start.pos[1]] = (0,255,0)
saved = Image.fromarray(image,"RGB")
saved.save("solve.png","PNG")
print("End")
print("Total time: ",datetime.now()-started)
