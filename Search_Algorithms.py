class Node:
  def __init__(self,state,pathCost,parent,height):
    self.state = state
    self.pathCost = pathCost
    self.parent = parent
    self.height = height

class mission:

  def __init__(self, algo,rows,cols,landingSite,Z,N,targets,matrix):
    self.algo = algo
    self.rows = rows
    self.cols = cols
    self.landingSite = landingSite
    self.Z = Z
    self.N = N
    self.targets = targets
    self.matrix = matrix
    self.visited =[[0] * self.cols for _ in range(self.rows)]

  def reset(self):
    self.visited = [[0] * self.cols for _ in range(self.rows)]

  def route(self,final,i):
    f = open("output.txt","a")
    if final:
      self.route(final.parent,i)
      f.write(str(final.state[1]))
      f.write(",")
      f.write(str(final.state[0]))
      if(final.state[0]==self.targets[i][0] and final.state[1]==self.targets[i][1] and i!=(len(self.targets)-1)):
        f.write("\n")
      elif(final.state[0]==self.targets[i][0] and final.state[1]==self.targets[i][1]) and i==(len(self.targets)-1):
        f.write("")
      else:
        f.write(" ")
    elif final == () and i==-2:
      f.write("FAIL")
    elif final == ():
      f.write("FAIL")
      if i!=(len(self.targets)-1):
        f.write("\n")
    return 

  def compute(self):
    if (self.landingSite[0]>(self.rows-1)) or (self.landingSite[1]>(self.cols-1)) or (self.landingSite[0]<0) or (self.landingSite[1]<0):
      final= ()
      self.route(final,-2)
      return "FAIL"
    i=0
    while(i<len(self.targets)):
      """if self.algo == "A*":
        final = self.Astar(self.targets[i]) """
      if self.algo == "BFS":
        final = self.BFS(self.targets[i])
      elif self.algo == "UCS":
        final = self.UCS(self.targets[i])
      elif self.algo == "A*":
        final = self.UCS(self.targets[i])
      else:
        final = ()
        self.route(final,i)
        return "FAIL"
      if final:
        self.route(final,i)
      else:
        final=()
        self.route(final,i)
      self.reset()
      i=i+1

  def heuristic(self,parent,me,myAlt):
    #return(abs(matrix[self.landingSite[0]][self.landingSite[1]]-myAlt))
    return(abs(self.landingSite[0]-me[0])+abs(self.landingSite[1]-me[1]))   
  
  def cost(self,parent,current,value):
    if self.algo == "BFS":
      return parent.pathCost + 1
    elif self.algo == "UCS":
      if parent.state[0] == current[0] or parent.state[1] == current[1]:
        return parent.pathCost + 10
      else:
        return parent.pathCost + 14
    elif self.algo == "A*":
      t = parent.pathCost + abs(parent.height-value)
      t = t + self.heuristic(parent,current,value)
      if parent.state[0] == current[0] or parent.state[1] == current[1]:
        return t + 10
      else:
        return t + 14

  def getValidNeighbors(self,parent):
    neighbors = []
    x = int(parent.state[0])
    y = int(parent.state[1])
    for i in range(x-1,x+2):
      for j in range(y-1,y+2):
        try:
          if (i!=x or y!= j) and (i>=0 and j>=0) and (i < self.rows and j < self.cols):
            if abs(self.matrix[i][j] - parent.height)<= self.Z:
              if self.visited[i][j]==0:
                pathCost = self.cost(parent,[i,j],self.matrix[i][j])
                tempnode = Node([i,j],pathCost,parent,self.matrix[i][j])
                neighbors.append(tempnode)
        except:
          pass
    return neighbors

  def BFS(self,target):
    queue = []
    pathCost = int(0)
    parent = None
    aNode = Node(self.landingSite,pathCost,parent,self.matrix[self.landingSite[0]][self.landingSite[1]])
    self.visited[self.landingSite[0]][self.landingSite[1]] = 1
    queue.append(aNode)
    while queue:
      popped = queue.pop(0)
      if popped.state[0] == target[0] and popped.state[1] == target[1]:
        return popped
      else:
        neighbors = self.getValidNeighbors(popped)
        for i in neighbors:
          self.visited[i.state[0]][i.state[1]] = int(1)
          queue.append(i)
    return None

  def UCS(self,target):
    queue = []
    pathCost = int(0)
    parent = None
    aNode = Node(self.landingSite,pathCost,parent,self.matrix[self.landingSite[0]][self.landingSite[1]])
    queue.append(aNode)
    while True:
      if not queue:
        break
      popped = queue.pop(0)
      if popped.state[0] == target[0] and popped.state[1] == target[1]:
        return popped
      if self.visited[popped.state[0]][popped.state[1]] == 1:
        continue
      self.visited[popped.state[0]][popped.state[1]] = 1
      neighbors = self.getValidNeighbors(popped)
      for i in neighbors:
        if not queue:
          queue.append(i)
        else:
          lenOfPathQueue = len(queue)
          iterator = int(0)
          while iterator < lenOfPathQueue:
            if i.pathCost < queue[iterator].pathCost:
              queue.insert(iterator,i)
              break
            iterator += 1
          if iterator == lenOfPathQueue:
            queue.append(i)

with open('input.txt') as inputFile:
  targets = []
  matrix = []
  lines = inputFile.readlines()  
  algo = lines[0][0:-1]    
  cols, rows = map(int,lines[1][0:-1].split(" "))
  Y, X = map(int,lines[2][0:-1].split(" "))
  landingSite = [X,Y]
  Z = lines[3][0:-1]
  Z = int(Z)
  N = lines[4][0:-1]
  N = int(N)
  for i in range(0,N):
    q,p = map(int,lines[i+5][0:-1].split(" "))
    targets.append([p,q])
  for i in range(0,rows):
    slope = lines[i + 5 + N].split(" ")
    value = []
    for j in slope:
        try:
            e=int(j)
        except:
            pass
        value.append(e)
    matrix.append(value)
landing = mission(algo,rows,cols,landingSite,Z,N,targets,matrix)
temp = open("output.txt","w")
temp.close()
landing.compute()