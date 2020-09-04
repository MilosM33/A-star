import math
class heap():
    def __init__(self):
        self.array = []
        self.current = 0
    
    def swap(self,a,b):
        arr = self.array
        arr[a.index] = b
        arr[b.index] = a
        temp = a.index
        a.index = b.index
        b.index = temp

    def up(self):
        index = len(self.array)-1
        
        parrent = (index-1)/2
        arr = self.array

        while index >=0 and arr[int(parrent)].f > arr[int(index)].f:
            self.swap(arr[int(parrent)],arr[int(index)])
            index = (index-1)/2
            parrent = (index-1)/2

    def down(self):
        index = 0
        left = int(index*2+1)
        arr = self.array
        length = len(arr)
        while left < length:
            small = left
            right = int(index*2+2)
            if right < length and arr[left].f > arr[right].f:
                small = right
            
            if arr[index].f < arr[small].f:
                break
            else:
                self.swap(arr[index],arr[small])
                index = small
                left = int(index*2+1)

    def pop(self):
        item = self.array[0]
        self.current -=1
        self.array[0] = self.array[self.length()-1]
        self.array[0].index = 0
        self.array.pop(self.length()-1)
        self.down()
        return item

    def add(self,item):
        item.index = self.current
        self.array.append(item)
        self.current +=1
        self.up()
    
    def length(self):
        return len(self.array)
    
    def contains(self,item):
        if item in self.array:
            return True
