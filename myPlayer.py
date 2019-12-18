# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

        self._time=0
        self._timelimit=7
        self._tour=0
    
    def getPlayerName(self):
        return "NegaScout Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        self._tour+=1
        move=self.bestMove()
        print(move)
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y)

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")


        
    def getWinner(self):
        if(self._board.is_game_over):
            (nbwhites, nbblacks) = self._board.get_nb_pieces()
            if(nbwhites>nbblacks):
                return self._board._WHITE
            elif(nbwhites<nbblacks):
                return self._board._BLACK

    def heuristiquef(self,color):
        eval=0
        (nbwhites, nbblacks) = self._board.get_nb_pieces()
        total=nbblacks+nbwhites

        #Winning take high priority in endgame
        if(self.getWinner()==self._mycolor and (total)>85):
            return 10000

        #Corners highly valued
        if(self._board._board[0][0]==color or self._board.is_valid_move(color,0,0)):
            eval+=1000
        if(self._board._board[9][9]==color or self._board.is_valid_move(color,9,9)):
            eval+=100
        if(self._board._board[0][9]==color or self._board.is_valid_move(color,0,9)):
            eval+=1000
        if(self._board._board[9][0]==color or self._board.is_valid_move(color,9,0)):
            eval+=1000

        #Giving corners is bad
        '''adversaire=self._board._WHITE

        if(self._mycolor==self._board._WHITE):
            adversaire=self._board._BLACK

        if(self._board._board[0][1]==color and self._board.is_valid_move(adversaire,0,0)):
            eval+=200
        if(self._board._board[1][0]==color and self._board.is_valid_move(adversaire,0,0)):
            eval+=200
        if(self._board._board[1][1]==color and self._board.is_valid_move(adversaire,0,0)):
            eval-=200'''

        if(self._board._board[0][1]==color and self._board._board[0][0]==self._board._EMPTY):
            eval-=500
        if(self._board._board[1][0]==color and self._board._board[0][0]==self._board._EMPTY):
            eval-=500
        if(self._board._board[1][1]==color and self._board._board[0][0]==self._board._EMPTY):
            eval-=500

        if(self._board._board[0][8]==color and self._board._board[0][9]==self._board._EMPTY):
            eval-=500
        if(self._board._board[1][9]==color and self._board._board[0][9]==self._board._EMPTY):
            eval-=500
        if(self._board._board[1][8]==color and self._board._board[0][9]==self._board._EMPTY):
            eval-=500

        if(self._board._board[8][1]==color and self._board._board[9][0]==self._board._EMPTY):
            eval-=500
        if(self._board._board[8][0]==color and self._board._board[9][0]==self._board._EMPTY):
            eval-=500
        if(self._board._board[9][1]==color and self._board._board[9][0]==self._board._EMPTY):
            eval-=500

        if(self._board._board[8][8]==color and self._board._board[9][9]==self._board._EMPTY):
            eval-=500
        if(self._board._board[8][9]==color and self._board._board[9][9]==self._board._EMPTY):
            eval-=500
        if(self._board._board[9][8]==color and self._board._board[9][9]==self._board._EMPTY):
            eval-=500

        #Edges valued
        for i in range(self._board._boardsize):
            if(self._board._board[i][0]==color):
                eval+=20
            if(self._board._board[i][9]==color):
                eval+=20
            if(self._board._board[0][i]==color):
                eval+=20
            if(self._board._board[9][i]==color):
                eval+=20

        #Having more pieces than opponent is values, especially late game
        if(total>78):
            if(self._board._nextPlayer==self._board._BLACK):
                eval+=20*(nbblacks-nbwhites)
            else:
                eval+=20*(nbwhites-nbblacks)

        #Minimize their moves mid to late game
        if(total>47):
            moves=self._board.legal_moves
            if(moves.length==0):
                eval+=200
            elif(moves.length<3):
                eval+=100
            else:
                eval-=moves.length*25

            self._mycolor=color

        #Try to have one piece in each col/row midgame
        '''if(total>31 and total<=78):
            for y in range(self._board.get_board_size()):
                cnt=0
                for x in range(self._board.get_board_size()):
                    if(self._board._board[x][y]==color):
                        cnt+=1
                if(cnt>0):
                    eval+=10

            for x in range(self._board.get_board_size()):
                cnt=0
                for y in range(self._board.get_board_size()):
                    if(self._board._board[x][y]==color):
                        cnt+=1
                if(cnt>0):
                    eval+=10

        #Secured rows are valuable
        for y in range(0,self._board.get_board_size(),9):
            for x in range(self._board.get_board_size()):
                if(self._board._board[0][y]==color):
                    if(self._board._board[x][y]!=color):
                        break
                    eval+=20

            for x in range(self._board.get_board_size()-1,x>=0,-1):
                if(self._board._board[9][y]==color):
                    if(self._board._board[x][y]!=color):
                        break
                    eval+=20

        #Secured cols are valuable
        for x in range(0,self._board.get_board_size(),9):
            for y in range(self._board.get_board_size()):
                if(self._board._board[x][0]==color):
                    if(self._board._board[x][y]!=color):
                        break
                    eval+=20

            for y in range(self._board.get_board_size()-1,y>=0,-1):
                if(self._board._board[9][y]==color):
                    if(self._board._board[x][y]!=color):
                        break
                    eval+=20'''
        
        return eval

        
    def heuristique2(self, player=None):
        adversaire=self._board._WHITE

        if(self._mycolor==self._board._WHITE):
            adversaire=self._board._BLACK

        return self.heuristiquef(self._mycolor)-self.heuristiquef(adversaire)



    def heuristique(self, player=None):
        if player is None:
            player = self._board._nextPlayer

        tot = 0
        for x in range(self._board._boardsize):
            for y in range(self._board._boardsize):
                if(self._board._board[x][y]==self._mycolor):
                    if (x == 0 or x == self._board._boardsize - 1) and (y == 0 or y == self._board._boardsize - 1):
                        tot +=100 # corner
                    elif ((x>1 and x<self._board._boardsize - 2 and (y==0 or y==self._board._boardsize - 1)) or (y>1 and y<self._board._boardsize - 2 and (x==0 or x==self._board._boardsize - 1))):
                        tot +=3
                    elif(x>1 and x<self._board._boardsize - 2 and y>1 and y<self._board._boardsize - 2):
                        tot +=4
                    elif((x>1 and x<self._board._boardsize - 2 and (y==1 or y==self._board._boardsize - 2)) or (y>1 and y<self._board._boardsize - 2) and  (x==1 or x==self._board._boardsize - 2)):
                        tot+=2
                    else:
                        tot += 1

        return tot


        ''' 5133333315
            1122222211
            3244444423
            3244444423
            3244  4423
            3244  4423
            3244444423
            3244444423
            1122222211
            5133333315'''

    def Minimax(self, depth, maximizingPlayer):

        if depth ==0 or not(self._board.at_least_one_legal_move(self._mycolor)):
            return self.heuristique(self._mycolor)

        if maximizingPlayer:
            bestValue = -(float('infinity'))
            for m in self._board.legal_moves():
                if(time.time()-self._time>self._timelimit):
                    break
                self._board.push(m)
                v=self.Minimax(depth-1,False)
                bestValue=max(bestValue,v)
                self._board.pop()
            return bestValue

        else: #minimizingplayer
            bestValue = float('infinity')
            for m in self._board.legal_moves():
                if(time.time()-self._time>self._timelimit):
                    break
                self._board.push(m)
                v=self.Minimax(depth-1,True)
                bestValue=min(bestValue,v)
                self._board.pop()
            return bestValue

    def AlphaBeta(self,depth,alpha,beta,maximizingPlayer):

        if depth ==0 or not(self._board.at_least_one_legal_move(self._mycolor)):
            return self.heuristique(self._mycolor)

        elif not maximizingPlayer:
            v =float('infinity')
            for m in self._board.legal_moves():
                if(time.time()-self._time>self._timelimit):
                    break
                self._board.push(m)
                v= min(v, self.AlphaBeta(depth - 1, alpha, beta, True))
                self._board.pop()
                if alpha>=v:
                    break # alpha cut-off
                beta = min(beta, v)

        else:
            v = -(float('infinity'))
            for m in self._board.legal_moves():
                if(time.time()-self._time>self._timelimit):
                    break
                self._board.push(m)
                v= max(v,self.AlphaBeta(depth - 1, alpha, beta, False))
                self._board.pop()
                if v>=beta:
                    break # beta cut-off
                alpha = max(alpha, v)
        return v

    def NegaMax(self,depth,alpha,beta,player):

        if depth ==0 or not(self._board.at_least_one_legal_move(self._mycolor)):
            return self.heuristique(self._mycolor)

        value=-float('infinity')
        for m in self._board.legal_moves():
            if(time.time()-self._time>self._timelimit):
                    break
            self._board.push(m)
            value=max(value,-self.NegaMax(depth-1,-beta,-alpha, not player))
            self._board.pop()
            alpha=max(alpha,value)
            if alpha>=beta:
                break #cut off
        return value

    def NegaScout(self,depth,alpha,beta,maximizingPlayer):
        if depth ==0 or not(self._board.at_least_one_legal_move(self._mycolor)):
            #return self._board.heuristique(self._mycolor)
            return self.heuristique2(self._mycolor)
        
        cpt=0
        for m in self._board.legal_moves():
            if cpt==0:
                cpt=1
                if(time.time()-self._time>self._timelimit):
                    break
                self._board.push(m)
                score=-self.NegaScout(depth-1,-beta,-alpha,not maximizingPlayer)
                self._board.pop()
            else:
                if(time.time()-self._time>self._timelimit):
                    break
                self._board.push(m) #search with a null window
                score=-self.NegaScout(depth-1,-alpha -1,-alpha,not maximizingPlayer)
                self._board.pop()
                if (alpha < score and score < beta):
                    if(time.time()-self._time>self._timelimit):
                        break
                    self._board.push(m) #if it failed high, do a full research
                    score=-self.NegaScout(depth-1,-beta,-score,not maximizingPlayer)
                    self._board.pop()
            alpĥa=max(alpha,score)
            if alpha >= beta:
                break #beta cut off
        return alpha
        

    def bestMove(self):
        if self._tour<5:
            moves = [m for m in self._board.legal_moves()]
            move = moves[randint(0,len(moves)-1)]
            return move
        
        maxPoints = -(float('infinity'))
        mx = -1; my = -1
        self._time=time.time()
        for i in range(1,97):
            for m in self._board.legal_moves():

                #points = self.AlphaBeta(self._depth,-float('infinity'),float('infinity'), True)
                #points = self.Minimax(depth, True)
                #points=self.NegaMax(self._depth,-float('infinity'),float('infinity'),True)
                points=self.NegaScout(i,-float('infinity'),float('infinity'),True)

                if points >= maxPoints:
                        maxPoints = points
                        mx = m[1]; my = m[2]

                if(time.time()-self._time>self._timelimit):
                    print("Profondeur : ",i)
                    return [self._mycolor, mx, my]
                    
        print("Profondeur : ",i)
        return [self._mycolor, mx, my]
