def getPiece(name):
   if name=="pawn":
      return 0
   elif name=="knight":
      return 1
   elif name=="bishop":
      return 2
   elif name=="rook":
      return 3
   elif name=="queen":
      return 4
   elif name=="king":
      return 5
   else:
      return -1

def getSide(board, position):
   if (board[position]>=10) and (board[position]<=15):
      return 10
   elif (board[position]>=20) and (board[position]<=25):
      return 20
   else:
      return 0

def genBoard():
   r=[0]*64
   White=10
   Black=20
   for i in [White,Black]:
      if i==White:
         factor=+1
         shift=0
      else:
         factor=-1
         shift=63

      r[shift+factor*7] = r[shift+factor*0] = i+getPiece("rook")
      r[shift+factor*6] = r[shift+factor*1] = i+getPiece("knight")
      r[shift+factor*5] = r[shift+factor*2] = i+getPiece("bishop")
      if i==White:
         r[shift+factor*4] = i+getPiece("queen") # queen is on its own color square
         r[shift+factor*3] = i+getPiece("king")
      else:
         r[shift+factor*3] = i+getPiece("queen") # queen is on its own color square
         r[shift+factor*4] = i+getPiece("king")

      for j in range(0,8):
         r[shift+factor*(j+8)] = i+getPiece("pawn")

   return r

def printBoard(board):
   accum="---- BLACK SIDE ----\n"
   max=63
   for j in range(0,8,1):
      for i in range(max-j*8,max-j*8-8,-1):
         accum=accum+'{0: <5}'.format(board[i])
      accum=accum+"\n"
   accum=accum+"---- WHITE SIDE ----"
   return accum

def printProperBoard(board):
   stringRow=""
   print("--- BLACK SIDE ---\n");
   for i in range(7,-1,-1):
      row=board[(i*8):(i*8+8)]
      for item in row:
         if item<10:
            stringRow += " "+str(item)
            stringRow += " "
         else:
            stringRow += str(item)
            stringRow += " "
      print(stringRow)
      stringRow=""
   print("\n")
   print("--- WHITE SIDE ---\n")
   return True

def GetBishopMoves(board, pos):
   enemyinway_upperleft=False
   enemyinway_upperright=False
   enemyinway_lowerleft=False
   enemyinway_lowerright=False
   
   rows_left = pos % 8
   rows_right = 7 - (pos % 8)
   accum=[]
   upper_left = pos
   lower_left = pos
   upper_right = pos
   lower_right = pos

   if getSide(board, pos)==10:
      mySide=10
      enemy=20
   elif getSide(board, pos)==20:
      mySide=20
      enemy=10
   else:
      return []
   
   for i in range(0,rows_left,1):
      if enemyinway_upperleft==False:
         upper_left += 7
         if (IsOnBoard(upper_left)) and (getSide(board, upper_left)!=mySide):
            accum += [upper_left]
            if getSide(board, upper_left)==enemy:
               enemyinway_upperleft=True
         else:
            enemyinway_upperleft=True
      if enemyinway_lowerleft==False:
         lower_left -= 9         
         if (IsOnBoard(lower_left)) and (getSide(board, lower_left)!=mySide):
            accum += [lower_left]
            if getSide(board, lower_left)==enemy:
               enemyinway_lowerleft=True
         else:
            enemyinway_lowerleft=True

   for i in range(0,rows_right,1):
      if enemyinway_upperright==False:
         upper_right += 9
         if (IsOnBoard(upper_right)) and (getSide(board, upper_right)!=mySide):
            accum += [upper_right]
            if getSide(board, upper_right)==enemy:
               enemyinway_upperright=True
         else:
            enemyinway_upperright=True
      if enemyinway_lowerright==False:
         lower_right -= 7         
         if (IsOnBoard(lower_right)) and (getSide(board, lower_right)!=mySide):
            accum += [lower_right]
            if getSide(board, lower_right)==enemy:
               enemyinway_lowerright=True
         else:
            enemyinway_lowerright=True
   return accum

def GetRookMoves(board, pos):
   enemyinway_left=False
   enemyinway_right=False
   enemyinway_down=False
   enemyinway_up=False
   
   rows_left = pos % 8
   rows_right = 7 - (pos % 8)
   rows_down = (pos // 8)
   rows_up = 7 - (pos // 8)
   accum=[]
   left=right=up=down=pos
   if getSide(board, pos)==10:
      mySide=10
      enemy=20
   elif getSide(board, pos)==20:
      mySide=20
      enemy=10
   else:
      return []
   
   for i in range(0,rows_left,1):
      if enemyinway_left==False:
         left -= 1
         if (IsOnBoard(left)) and (getSide(board, left)!=mySide):
            accum += [left]
            if getSide(board, left)==enemy:
               enemyinway_left=True
         else:
            enemyinway_left=True
   for i in range(0,rows_right,1):
      if enemyinway_right==False:
         right += 1
         if (IsOnBoard(right)) and (getSide(board, right)!=mySide):
            accum += [right]
            if getSide(board, right)==enemy:
               enemyinway_right=True
         else:
            enemyinway_right=True
   for i in range(0,rows_down,1):
      if enemyinway_down==False:
         down -= 8
         if (IsOnBoard(down)) and (getSide(board, down)!=mySide):
            accum += [down]
            if getSide(board, down)==enemy:
               enemyinway_down=True
         else:
            enemyinway_down=True
   for i in range(0,rows_up,1):
      if enemyinway_up==False:
         up += 8
         if (IsOnBoard(up)) and (getSide(board, up)!=mySide):
            accum += [up]
            if getSide(board, up)==enemy:
               enemyinway_up=True
         else:
            enemyinway_up=True

   return accum

def GetQueenMoves(board, pos):
   return GetRookMoves(board, pos) + GetBishopMoves(board, pos)

def GetPawnMoves(board, pos):
   accum=[]
   rows_left = pos % 8
   rows_right = 7 - (pos % 8)
   if getSide(board, pos)==10:
      mySide=10
      enemy=20
   elif getSide(board, pos)==20:
      mySide=20
      enemy=10
   else:
      return []
   if mySide==10:
      up=pos
      kill_upleft=pos
      kill_upright=pos
      up += 8
      if (IsOnBoard(up)) and (getSide(board, up)!=mySide) and (getSide(board, up)!=enemy):
         accum += [up]
      kill_upleft += 7
      if (IsOnBoard(kill_upleft)) and (getSide(board, kill_upleft)==enemy) and (rows_left>=1):
         accum += [kill_upleft]
      kill_upright += 9
      if (IsOnBoard(kill_upright)) and (getSide(board, kill_upright)==enemy) and (rows_right>=1):
         accum += [kill_upright]
         
   elif mySide==20:
      down=pos
      kill_downleft=pos
      kill_downright=pos
      down -= 8
      if (IsOnBoard(down)) and (getSide(board, down)!=mySide) and (getSide(board, down)!=enemy):
         accum += [down]
      kill_downleft -= 9
      if (IsOnBoard(kill_downleft)) and (getSide(board, kill_downleft)==enemy) and (rows_left>=1):
         accum += [kill_downleft]
      kill_downright -= 7
      if (IsOnBoard(kill_downright)) and (getSide(board, kill_downright)==enemy) and (rows_right>=1):
         accum += [kill_downright]
      
   return accum

def GetKnightMoves(board, pos):
   accum=[]
   rows_left = pos % 8
   rows_right = 7 - (pos % 8)
   if getSide(board, pos)==10:
      mySide=10
      enemy=20
   elif getSide(board, pos)==20:
      mySide=20
      enemy=10
   else:
      return []
   possiblePlaces_1=[pos+17, pos-15]
   possiblePlaces_2=[pos+15, pos-17]
   possiblePlaces_3=[pos+6, pos-10]
   possiblePlaces_4=[pos+10, pos-6]
   for location in possiblePlaces_1:
      if (IsOnBoard(location)) and (getSide(board, location)!=mySide) and (rows_right>=1):
         accum += [location]
   for location in possiblePlaces_2:
      if (IsOnBoard(location)) and (getSide(board, location)!=mySide) and (rows_left>=1):
         accum += [location]
   for location in possiblePlaces_3:
      if (IsOnBoard(location)) and (getSide(board, location)!=mySide) and (rows_left>=2):
         accum += [location]
   for location in possiblePlaces_4:
      if (IsOnBoard(location)) and (getSide(board, location)!=mySide) and (rows_right>=2):
         accum += [location]
   return accum

def GetKingMoves(board, pos):
   accum=[]
   rows_left = pos % 8
   rows_right = 7 - (pos % 8)
   if getSide(board, pos)==10:
      mySide=10
      enemy=20
   elif getSide(board, pos)==20:
      mySide=20
      enemy=10
   else:
      return []
   
   up=pos
   kill_upleft=pos
   kill_upright=pos
   up += 8
   if (IsOnBoard(up)) and (getSide(board, up)!=mySide):
      accum += [up]
   kill_upleft += 7
   if (IsOnBoard(kill_upleft)) and (getSide(board, kill_upleft)!=mySide) and (rows_left>=1):
      accum += [kill_upleft]
   kill_upright += 9
   if (IsOnBoard(kill_upright)) and (getSide(board, kill_upright)!=mySide) and (rows_right>=1):
      accum += [kill_upright]
         
   down=pos
   kill_downleft=pos
   kill_downright=pos
   down -= 8
   if (IsOnBoard(down)) and (getSide(board, down)!=mySide):
      accum += [down]
   kill_downleft -= 9
   if (IsOnBoard(kill_downleft)) and (getSide(board, kill_downleft)!=mySide) and (rows_left>=1):
      accum += [kill_downleft]
   kill_downright -= 7
   if (IsOnBoard(kill_downright)) and (getSide(board, kill_downright)!=mySide) and (rows_right>=1):
      accum += [kill_downright]

   right=pos
   left=pos
   right += 1
   left -=1
   if (IsOnBoard(right)) and (getSide(board, right)!=mySide) and (rows_right>=1):
      accum += [right]
   if (IsOnBoard(left)) and (getSide(board, left)!=mySide) and (rows_left>=1):
      accum += [left]
   return accum

def IsOnBoard(pos):
   if (pos >= 0) and (pos <= 63):
      return True
   else:
      return False

def GetPlayerPositions(board,player):
   positions=[]
   if (player!=10) and (player!=20):
      return []
   elif player==10:
      for i in range(0,64,1):
         if(board[i]>=10) and (board[i]<=15):
            positions+=[i]
   else:
      for i in range(0,64,1):
         if(board[i]>=20) and (board[i]<=25):
            positions+=[i]
   return positions

def GetPieceLegalMoves_original(board, pos):
   if board[pos]==10 or board[pos]==20:
      return GetPawnMoves(board, pos)
   elif board[pos]==11 or board[pos]==21:
      return GetKnightMoves(board, pos)
   elif board[pos]==12 or board[pos]==22:
      return GetBishopMoves(board, pos)
   elif board[pos]==13 or board[pos]==23:
      return GetRookMoves(board, pos)
   elif board[pos]==14 or board[pos]==24:
      return GetQueenMoves(board, pos)
   elif board[pos]==15 or board[pos]==25:
      return GetKingMoves(board, pos)
   else:
      return []

def GetPieceLegalMoves(board, pos):
   if getSide(board, pos)==10:
      mySide=10
      myKing=15
   elif getSide(board, pos)==20:
      mySide=20
      myKing=25
   enemyKillerLocation = IsPositionUnderThreat(board, findKing(board, mySide))[1]
   if IsPositionUnderThreat(board, findKing(board, mySide))[0]==True:
      if board[pos]==myKing:
         for move in GetKingMoves(board, pos):
            if move == enemyKillerLocation:
               return [move]
         return GetKingMoves(board, pos)
      else:
         for move in GetPieceLegalMoves_original(board, pos):
            if move == enemyKillerLocation:
               return [move]
         return []
   else:
      return GetPieceLegalMoves_original(board, pos)

def IsPositionUnderThreat(board, position):
   if getSide(board, position)==10:
      mySide=10
      enemy=20
   elif getSide(board, position)==20:
      mySide=20
      enemy=10
   else:
      print("Wrong input for player")
      return False
   enemyCurrentPositions=GetPlayerPositions(board, enemy)
   for enemyPos in enemyCurrentPositions:
      for location in GetPieceLegalMoves_original(board, enemyPos):
         if location==position:
            return [True, enemyPos]
   return [False, None] 

def isWhite(board, pos):
   if IsOnBoard(pos) and getSide(board, pos)==10:
      return True
   else:
      return False
   
def isBlack(board, pos):
   if IsOnBoard(pos) and getSide(board, pos)==20:
      return True
   else:
      return False

def isLegalMove(board, currentPlace, goingTo):
   possibleMoves=GetPieceLegalMoves(board, currentPlace)
   for place in possibleMoves:
      if goingTo==place:
         return True
   return False

def findKing(board, player):
   if player==10:
      king=15
   else:
      king=25
      
   for i in range(0,64,1):
      if board[i]==king:
         return i

def switchMoveToKing(board, player):
   kingPos=findKing(board, player)
   if IsPositionUnderThreat(board, kingPos, player)==True:
      return True 
   else:
      return False

   
def testBoard():
   board=genBoard()
   print("\n")
   print("raw board is: (index=0 ... index=63):")
   print(board)
   print("Actual board: \n")
   print(printBoard(board))
   print("\n")
   print(" Note 1: lower right hand square is WHITE")
   print(" Note 2: two upper rows are for BLACK PIECES")
   print(" Note 3: two lower rows are for WHITE PIECES")
   print("White Positions")
   print(GetPlayerPositions(board,10))
   print("Black Positions")
   print(GetPlayerPositions(board,20))










