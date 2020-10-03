from chessPlayer_gameRules import *
class queue:
   def __init__(self):
      self.store=[]
      self.length=0

   def enqueue(self,value):
      self.store=self.store+[value]
      self.length+=1
      return True

   def dequeue(self):
      if self.length==0:
         return False
      else:
         rVal=self.store[0]
         self.store=self.store[1:len(self.store)]
         self.length-=1
         return rVal 

class tree:
   def __init__(self, board, goFrom, goTo, player):
      self.store=[board,[]]
      self.move=[goFrom, goTo] #this is how it got here, not where it will go next
      self.side = player
      self.parent = None

   def getHeuristicVal(self):
      return getSituationValue(self.getBoard(), self.side)

   def getParent(self):
      return self.parent

   def getMoveFrom(self):
      return self.move[0]

   def getMoveTo(self):
      return self.move[1]

   def addSuccessor(self,subTree):
      subTree.parent = self
      self.store[1]=self.store[1]+[subTree]
      return True

   def getSuccessor(self):
      return self.store[1]

   def getBoard(self):
      return self.store[0]

   def Print_DepthFirst(self):
        self.Print_DepthFirst_helper("   ")
        return True

   def Print_DepthFirst_helper(self,prefix):
        print(prefix+str(self.store[0]))
        for i in self.store[1]:
           i.Print_DepthFirst_helper(prefix+"   ")
        return True

   def Get_LevelOrder(self):
      valList=[]
      tempQueue=queue()
      tempQueue.enqueue(self)
      while len(tempQueue.store)!=0:
         r=tempQueue.dequeue()
         valList+=[r.getBoard()]
         for item in r.getSuccessor():
            tempQueue.enqueue(item)
      return valList
   
   def Get_DepthOrder(self):
      valList=[]
      tempStack=stack()
      tempStack.push(self)
      while len(tempStack.store)!=0:
         r=tempStack.pop()
         valList+=[r.getBoard()]
         for item in r.getSuccessor():
            tempStack.push(item)
      return valList

def createEvalTree(board, player):
   if player==10:
      mySide=10
      enemy=20
   else:
      mySide=20
      enemy=10
   root = tree(board, None, None, mySide)
   fakeBoard = list(board)
   for pos in GetPlayerPositions(fakeBoard, mySide):
      for move in GetPieceLegalMoves(fakeBoard, pos):
         successor = tree(implementMoveReturnFakeBoard(fakeBoard, pos, move), pos, move, mySide)
         root.addSuccessor(successor)
   return root 
 
         
def createEvalTree_ThreeLevels(board, player):
   if player==10:
      mySide=10
      enemy=20
   else:
      mySide=20
      enemy=10
      
   root = tree(board, None, None, mySide)      
   fakeBoard = list(board)
   for playerPosition in GetPlayerPositions(fakeBoard, mySide):      
      for legalMove in GetPieceLegalMoves(fakeBoard, playerPosition):
         root.addSuccessor(tree(implementMoveReturnFakeBoard(fakeBoard, playerPosition, legalMove), playerPosition, legalMove, mySide))
         
   for child_node in root.getSuccessor():
      for pos in GetPlayerPositions(child_node.getBoard(), enemy):
         if len(GetPieceLegalMoves(child_node.getBoard(), pos))!=0:
            firstPos = pos
            firstMove = GetPieceLegalMoves(child_node.getBoard(), pos)[0]
            break
      worst_heuristicVal = getSituationValue(implementMoveReturnFakeBoard(child_node.getBoard(), firstPos, firstMove), mySide) 
      
      for earlierplayerPosition in GetPlayerPositions(child_node.getBoard(), enemy):
         for earlierlegalMove in GetPieceLegalMoves(child_node.getBoard(), earlierplayerPosition):
            if getSituationValue(implementMoveReturnFakeBoard(child_node.getBoard(), earlierplayerPosition, earlierlegalMove), mySide) <= worst_heuristicVal:
               worst_heuristicVal = getSituationValue(implementMoveReturnFakeBoard(child_node.getBoard(), earlierplayerPosition, earlierlegalMove), mySide) 
               child_node.addSuccessor(tree(implementMoveReturnFakeBoard(child_node.getBoard(), earlierplayerPosition, earlierlegalMove), earlierplayerPosition, earlierlegalMove, mySide))

      for deeperChild_node in child_node.getSuccessor():
         for pos in GetPlayerPositions(deeperChild_node.getBoard(), mySide):
            if len(GetPieceLegalMoves(deeperChild_node.getBoard(), pos))!=0:
               firstPos = pos
               firstMove = GetPieceLegalMoves(deeperChild_node.getBoard(), pos)[0]
               break
         best_heuristicVal = getSituationValue(implementMoveReturnFakeBoard(deeperChild_node.getBoard(), firstPos, firstMove), mySide) 
         for playerPosition in GetPlayerPositions(deeperChild_node.getBoard(), mySide):
            for legalMove in GetPieceLegalMoves(deeperChild_node.getBoard(), playerPosition):
               if getSituationValue(implementMoveReturnFakeBoard(deeperChild_node.getBoard(), playerPosition, legalMove), mySide) >= best_heuristicVal:
                  best_heuristicVal = getSituationValue(implementMoveReturnFakeBoard(deeperChild_node.getBoard(), playerPosition, legalMove), mySide)
                  deeperChild_node.addSuccessor(tree(implementMoveReturnFakeBoard(deeperChild_node.getBoard(), playerPosition, legalMove), playerPosition, legalMove, mySide))
   return root            

def implementMoveReturnFakeBoard(board, goFrom, goTo):
   fakeBoard = list(board)
   fakeBoard[goTo] = fakeBoard[goFrom]
   fakeBoard[goFrom] = 0
   return fakeBoard

def evaluateMinMax(node, depth, player, findMax):
   if depth==0:
      return node
   if findMax == True:
      current_rVal = -100000
   elif findMax == False:
      current_rVal = 100000
   current_node = node
   for child_node in node.getSuccessor():
      if findMax == True:
         rNode = evaluateMinMax(child_node, depth-1, player, False)
      elif findMax == False:
         rNode = evaluateMinMax(child_node, depth-1, player, True)
      rValue = rNode.getHeuristicVal()
      if findMax == True:
         if rValue >= current_rVal:
            current_rVal = rValue
            current_node = rNode
      elif findMax == False:
         if rValue <= current_rVal:
            current_rVal = rValue
            current_node = rNode
   return current_node

def getActualNode(node):
   desired_Node = node.getParent().getParent()
   return desired_Node 

def evaluateOneLevel(root):
   firstNode = root.getSuccessor()[0]
   bestVal = firstNode.getHeuristicVal()
   for child in root.getSuccessor():
      if child.getHeuristicVal() >= bestVal:
         bestNode = child
         bestVal = child.getHeuristicVal()
   return bestNode     
  
def getSituationValue(board, player):
   if player==10:
      mySide=10
      enemy=20
   else:
      mySide=20
      enemy=10
   myPiecesLocations = GetPlayerPositions(board, mySide)
   enemyPiecesLocations = GetPlayerPositions(board, enemy)
   sumMyStrength = 0
   sumEnemyStrength = 0
   for position in myPiecesLocations:
      sumMyStrength += getPieceStrength_value(board, position)
      if IsPositionUnderThreat(board, position)[0]==True:
         sumMyStrength -= getPieceStrength_value(board, position)*100
   for position in enemyPiecesLocations:
      sumEnemyStrength += getPieceStrength_value(board, position)
      if IsPositionUnderThreat(board, position)[0]==True:
         sumEnemyStrength -= getPieceStrength_value(board, position)*100
   return (sumMyStrength - sumEnemyStrength)


def getPieceStrength_value(board, pos):
   if board[pos]==10 or board[pos]==20:
      return (1)
   elif board[pos]==11 or board[pos]==21:
      return (3)
   elif board[pos]==12 or board[pos]==22:
      return (3)
   elif board[pos]==13 or board[pos]==23:
      return (5)
   elif board[pos]==14 or board[pos]==24:
      return (9)
   elif board[pos]==15 or board[pos]==25:
      return (90)
   else:
      return 0

def getPieceStrength_Abs(board, pos, player):
   if board[pos]==10 or board[pos]==20:
      return (1 * getPawnWeightedBoard(player)[pos])
   elif board[pos]==11 or board[pos]==21:
      return (3 * getKnightWeightedBoard(player)[pos])
   elif board[pos]==12 or board[pos]==22:
      return (3 * getBishopWeightedBoard(player)[pos])
   elif board[pos]==13 or board[pos]==23:
      return (5 * getRookWeightedBoard(player)[pos])
   elif board[pos]==14 or board[pos]==24:
      return (9 * getQueenWeightedBoard(player)[pos])
   elif board[pos]==15 or board[pos]==25:
      return (90 * getKingWeightedBoard(player)[pos])
   else:
      return 0

def getPawnWeightedBoard(player):
   pawnBoard=[]
   if player==20:
      for i in range(0,8,1):
         pawnBoard+=[0]
      for i in range(0,8,1):
         pawnBoard+=[5]
      pawnBoard+=[1,1,2,3,3,2,1,1]
      pawnBoard+=[0.5,0.5,1,2.5,2.5,1,0.5,0.5]
      pawnBoard+=[0,0,0,2,2,0,0,0]
      pawnBoard+=[0.5,-0.5,-1,0,0,-1,-0.5,0.5]
      pawnBoard+=[0.5,1,1,-2,-2,1,1,0.5]
      for i in range(0,8,1):
         pawnBoard+=[0]
      if len(pawnBoard)==64:
         return pawnBoard
   else:
      for i in range(0,8,1):
         pawnBoard+=[0]
      pawnBoard+=[0.5,1,1,-2,-2,1,1,0.5]
      pawnBoard+=[0.5,-0.5,-1,0,0,-1,-0.5,0.5]
      pawnBoard+=[0,0,0,2,2,0,0,0]
      pawnBoard+=[0.5,0.5,1,2.5,2.5,1,0.5,0.5]
      pawnBoard+=[1,1,2,3,3,2,1,1]
      for i in range(0,8,1):
         pawnBoard+=[5]
      for i in range(0,8,1):
         pawnBoard+=[0]
      if len(pawnBoard)==64:
         return pawnBoard 

def getKingWeightedBoard(player):
   kingBoard=[]
   row=[-3,-4,-4,-5,-5,-4,-4,-3]
   if player==20:
      for i in range(0,4,1):
         kingBoard+=row
      kingBoard+=[-0.2,-0.3,-0.3,-0.4,-0.4,-0.3,-0.3,-0.2]
      kingBoard+=[-0.1,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.1]
      kingBoard+=[0.2,0.2,0,0,0,0,0.2,0.2]
      kingBoard+=[0.2,0.3,0.1,0,0,0.1,0.3,0.2]
      if len(kingBoard)==64:
         return kingBoard
   else:
      kingBoard+=[0.2,0.3,0.1,0,0,0.1,0.3,0.2]
      kingBoard+=[0.2,0.2,0,0,0,0,0.2,0.2]
      kingBoard+=[-0.1,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.1]
      kingBoard+=[-0.2,-0.3,-0.3,-0.4,-0.4,-0.3,-0.3,-0.2]
      for i in range(0,4,1):
         kingBoard+=row      
      if len(kingBoard)==64:
         return kingBoard

def getQueenWeightedBoard(player):
   queenBoard=[]
   if player==20:
      queenBoard+=[-2,-1,-1,-0.5,-0.5,-1,-1,-2]
      queenBoard+=[-1,0,0,0,0,0,0,-1]
      queenBoard+=[-1,0,0.5,0.5,0.5,0.5,0,-1]
      queenBoard+=[-0.5,0,0.5,0.5,0.5,0.5,0,-0.5]
      queenBoard+=[0,0,0.5,0.5,0.5,0.5,0,0]
      queenBoard+=[-1,0.5,0.5,0.5,0.5,0.5,0.5,-1]
      queenBoard+=[-1,0,0,0,0,0.5,0,-1]
      queenBoard+=[-2,-1,-1,-0.5,-0.5,-1,-1,-2]
      if len(queenBoard)==64:
         return queenBoard
   else:
      queenBoard+=[-2,-1,-1,-0.5,-0.5,-1,-1,-2]
      queenBoard+=[-1,0,0,0,0,0.5,0,-1]
      queenBoard+=[-1,0.5,0.5,0.5,0.5,0.5,0.5,-1]
      queenBoard+=[0,0,0.5,0.5,0.5,0.5,0,0]
      queenBoard+=[-0.5,0,0.5,0.5,0.5,0.5,0,-0.5]
      queenBoard+=[-1,0,0.5,0.5,0.5,0.5,0,-1]
      queenBoard+=[-1,0,0,0,0,0,0,-1]
      queenBoard+=[-2,-1,-1,-0.5,-0.5,-1,-1,-2]
      if len(queenBoard)==64:
         return queenBoard

def getRookWeightedBoard(player):
   rookBoard=[]
   row=[-0.5,0,0,0,0,0,0,-0.5]
   if player==20:
      for i in range(0,8,1):
         rookBoard+=[0]
      rookBoard+=[0.5,1,1,1,1,1,1,0.5]
      for i in range(0,5,1):
         rookBoard+=row
      rookBoard+=[0,0,0,0.5,0.5,0,0,0]
      if len(rookBoard)==64:
         return rookBoard
   else:
      rookBoard+=[0,0,0,0.5,0.5,0,0,0]
      for i in range(0,5,1):
         rookBoard+=row
      rookBoard+=[0.5,1,1,1,1,1,1,0.5]
      for i in range(0,8,1):
         rookBoard+=[0]
      if len(rookBoard)==64:
         return rookBoard

def getBishopWeightedBoard(player):
   bishopBoard=[]
   if player==20:
      bishopBoard+=[-2,-1,-1,-1,-1,-1,-1,-2]
      bishopBoard+=[-1,0,0,0,0,0,0,-1]
      bishopBoard+=[-1,0,0.5,1,1,0.5,0,-1]
      bishopBoard+=[-1,0.5,0.5,1,1,0.5,0.5,-1]
      bishopBoard+=[-1,0,1,1,1,1,0,-1]
      bishopBoard+=[-1,1,1,1,1,1,1,-1]
      bishopBoard+=[-1,0.5,0,0,0,0,0.5,-1]
      bishopBoard+=[-2,-1,-1,-1,-1,-1,-1,-2]
      if len(bishopBoard)==64:
         return bishopBoard
   else:
      bishopBoard+=[-2,-1,-1,-1,-1,-1,-1,-2]
      bishopBoard+=[-1,0.5,0,0,0,0,0.5,-1]
      bishopBoard+=[-1,1,1,1,1,1,1,-1]
      bishopBoard+=[-1,0,1,1,1,1,0,-1]
      bishopBoard+=[-1,0.5,0.5,1,1,0.5,0.5,-1]
      bishopBoard+=[-1,0,0.5,1,1,0.5,0,-1]
      bishopBoard+=[-1,0,0,0,0,0,0,-1]
      bishopBoard+=[-2,-1,-1,-1,-1,-1,-1,-2]
      if len(bishopBoard)==64:
         return bishopBoard

def getKnightWeightedBoard(player):
   knightBoard=[]
   if player==20:
      knightBoard+=[-5,-4,-3,-3,-3,-3,-4,-5]
      knightBoard+=[-4,-2,0,0,0,0,-2,-4]
      knightBoard+=[-3,0,1,1.5,1.5,1,0,-3]
      knightBoard+=[-3,0.5,1.5,2,2,1.5,0.5,-3]
      knightBoard+=[-3,0,1.5,2,2,1.5,0,-3]
      knightBoard+=[-3,0.5,1,1.5,1.5,1,0.5,-3]
      knightBoard+=[-4,-2,0,0.5,0.5,0,-2,-4]
      knightBoard+=[-5,-4,-3,-3,-3,-3,-4,-5]
      if len(knightBoard)==64:
         return knightBoard
   else:
      knightBoard+=[-5,-4,-3,-3,-3,-3,-4,-5]
      knightBoard+=[-4,-2,0,0.5,0.5,0,-2,-4]
      knightBoard+=[-3,0.5,1,1.5,1.5,1,0.5,-3]
      knightBoard+=[-3,0,1.5,2,2,1.5,0,-3]
      knightBoard+=[-3,0.5,1.5,2,2,1.5,0.5,-3]
      knightBoard+=[-3,0,1,1.5,1.5,1,0,-3]
      knightBoard+=[-4,-2,0,0,0,0,-2,-4]
      knightBoard+=[-5,-4,-3,-3,-3,-3,-4,-5]
      if len(knightBoard)==64:
         return knightBoard



def testStuff():
   counter_1=0
   counter_2=0
   counter_3=0
   board = genBoard()

   board[16]=10
   board[8]=0

   board[40]=21
   board[57]=0

   board[21]=11
   board[6]=0

   board[45]=20
   board[53]=0

   board[17]=10
   board[9]=0

   board[47]=20
   board[55]=0
   
   root=createEvalTree(board, 10)
   print("----------------AI can make these choices FIRST-------------")
   for node in root.getSuccessor():
      print(node.move)


   print("***************ENEMY can make these choices SECOND************")
   for node in root.getSuccessor():
      counter_1 += 1
      print("After the "+str(counter_1)+"th possible choice by the AI on the first move")
      for deeper_node in node.getSuccessor():
         #print("-------------------------------------------the length is: "+str(len(deeper_node.getSuccessor())))
         print(deeper_node.move)

   print("----------------AI can make these choices THIRD--------------")
   for node in root.getSuccessor():
      counter_3=0
      counter_2 += 1
      print("After the "+str(counter_2)+"th possible choice by the AI on the first move")
      for deeper_node in node.getSuccessor():
         counter_3 += 1
         print("After the "+str(counter_3)+"th possible choice by the ENEMY on the second move")
         for deepest_node in deeper_node.getSuccessor():
            print(deepest_node.move)



            







