from chessPlayer_evaluation import *
from chessPlayer_gameRules import *

def chessPlayer(board, player):
   status = True
   if player!=10 and player!=20:
      status = False 
   if len(GetPlayerPositions(board, player))<=0:
      status = False
   rTree = createEvalTree(board, player)
   chosenNode = evaluateOneLevel(rTree)
   moveFrom = chosenNode.getMoveFrom()
   moveTo = chosenNode.getMoveTo()
   move = [moveFrom, moveTo]
   candidateMoves = []
   for pos in GetPlayerPositions(board, player):
      for legalMove in GetPieceLegalMoves(board, pos):
         heuristicVal = getSituationValue(implementMoveReturnFakeBoard(board, pos, legalMove), player)
         individualMove = [[pos, legalMove], heuristicVal]
         candidateMoves += [individualMove]
   evalTree = []
   tempQueue = queue()
   tempQueue.enqueue(rTree)
   while len(tempQueue.store)!=0:
      rVal = tempQueue.dequeue()
      if rVal==False:
         break
      else:
         evalTree = evalTree + [rVal]
         for node in rVal.getSuccessor():
            tempQueue.enqueue(node)
   return [status, move, candidateMoves, evalTree]
   


