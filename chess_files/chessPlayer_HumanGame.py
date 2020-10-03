from chessPlayer_gameRules import *
from chessPlayer_evaluation import *
from chessPlayer import *

def whiteTurn(board):
   while True:
      print("White piece move from: ")
      whiteFrom=int(input())
      if isWhite(board, whiteFrom)==True:
         break
      else:
         print("Invalid position, choose again")
      
   while True:
      print("White piece move to: ")
      whiteTo=int(input())
      if isLegalMove(board, whiteFrom, whiteTo)==True:
         board[whiteTo]=board[whiteFrom]
         board[whiteFrom]=0
         break
      else:
         print("Invalid position, choose again")         
   return True

def blackTurn(board):
   ##while True:
   #   print("Black piece move from: ")
   #   blackFrom=int(input())
   #   if isBlack(board, blackFrom)==True:
   #      break
   #   else:
   #      print("Invalid position, choose again")
   #   
   #while True:
   #   print("Black piece move to: ")
   #   blackTo=int(input())
   #   if isLegalMove(board, blackFrom, blackTo)==True:
   #      board[blackTo]=board[blackFrom]
   #      board[blackFrom]=0
   #      break
   #   else:
   #      print("Invalid position, choose again")
   #chosenNode = getActualNode(evaluateMinMax(createEvalTree(board, 20), 3, 20, True))     
   #blackMoveFrom = chosenNode.getMoveFrom()
   #blackMoveTo = chosenNode.getMoveTo()
   blackMoveFrom = chessPlayer(board, 20)[1][0]
   blackMoveTo = chessPlayer(board, 20)[1][1]
   print("Black piece move from: "+str(blackMoveFrom))
   print("Black piece move to: "+str(blackMoveTo))
   print(GetPieceLegalMoves(board, blackMoveFrom))
   board[blackMoveTo] = board[blackMoveFrom]
   board[blackMoveFrom] = 0
   return True

def runGame():
   board=genBoard()
   print("-------THE BOARD HAS BEEN INITIALIZED-------\n")
   gameOver=False
   print("Board index")
   print(printBoard(range(0,64,1)))
   print("Actual board")
   print(printBoard(board))
   while gameOver==False:
      whiteTurn(board)
      print("Board index")
      print(printBoard(range(0,64,1)))
      print("Actual board")
      print(printBoard(board))     
      blackTurn(board)
      print("Board index")
      print(printBoard(range(0,64,1)))
      print("Actual board")      
      print(printBoard(board))      

runGame()
   






