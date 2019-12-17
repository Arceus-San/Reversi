# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._depth = 10

        self._minEvalBoard = 0 # min - 1
        self._maxEvalBoard = self._board._boardsize * self._board._boardsize + 4 * self._board._boardsize + 4 + 1 # max + 1

    def getPlayerName(self):
        return "AI Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        move=self.bestMove(self._depth)
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
            #return self._board.heuristique(self._mycolor)
            return self.heuristique(self._mycolor)

        if maximizingPlayer:
            bestValue = -(float('infinity'))
            for m in self._board.legal_moves():
                self._board.push(m)
                v=self.Minimax(depth-1,False)
                bestValue=max(bestValue,v)
                self._board.pop()
            return bestValue

        else: #minimizingplayer
            bestValue = float('infinity')
            for m in self._board.legal_moves():
                self._board.push(m)
                v=self.Minimax(depth-1,True)
                bestValue=min(bestValue,v)
                self._board.pop()
            return bestValue

    def AlphaBeta(self,depth,alpha,beta,maximizingPlayer):

        if depth ==0 or not(self._board.at_least_one_legal_move(self._mycolor)):
            #return self._board.heuristique(self._mycolor)
            return self.heuristique(self._mycolor)

        elif not maximizingPlayer:
            v =float('infinity')
            for m in self._board.legal_moves():
                self._board.push(m)
                #v=v = min(v, self.AlphaBeta(depth - 1, -beta, alpha, True))
                v= min(v, self.AlphaBeta(depth - 1, alpha, beta, True))
                self._board.pop()
                if alpha>=v:
                    break # alpha cut-off
                beta = min(beta, v)

        else:
            v = -(float('infinity'))
            for m in self._board.legal_moves():
                self._board.push(m)
                v= max(v,self.AlphaBeta(depth - 1, alpha, beta, False))
                self._board.pop()
                if v>=beta:
                    break # beta cut-off
                alpha = max(alpha, v)
        return v

    def NegaMax(self,depth,alpha,beta,player):

        if depth ==0 or not(self._board.at_least_one_legal_move(self._mycolor)):
            #return self._board.heuristique(self._mycolor)
            return self.heuristique(self._mycolor)

        value=-float('infinity')
        for m in self._board.legal_moves():
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
            return self.heuristique(self._mycolor)
        
        cpt=0
        for m in self._board.legal_moves():
            if cpt==0:
                cpt=1
                self._board.push(m)
                score=-self.NegaScout(depth-1,-beta,-alpha,not maximizingPlayer)
                self._board.pop()
            else:
                self._board.push(m) #search with a null window
                score=-self.NegaScout(depth-1,-alpha -1,-alpha,not maximizingPlayer)
                self._board.pop()
                if (alpha < score and score < beta):
                    self._board.push(m) #if it failed high, do a full research
                    score=-self.NegaScout(depth-1,-beta,-score,not maximizingPlayer)
                    self._board.pop()
            alpĥa=max(alpha,score)
            if alpha >= beta:
                break #beta cut off
        return alpha
        

    def bestMove(self, depth):
        maxPoints = -(float('infinity'))
        mx = -1; my = -1
        debut=time.time()
        for i in range(1,97):
            for m in self._board.legal_moves():

                #points = self.AlphaBeta(self._depth,-float('infinity'),float('infinity'), True)
                #points = self.Minimax(depth, True)
                #points=self.NegaMax(self._depth,-float('infinity'),float('infinity'),True)
                points=self.NegaScout(i,-float('infinity'),float('infinity'),True)

                if points >= maxPoints:
                        maxPoints = points
                        mx = m[1]; my = m[2]

                if(time.time()-debut>6):
                    return [self._mycolor, mx, my]

        return [self._mycolor, mx, my]
