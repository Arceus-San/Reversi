# -*- coding: utf-8 -*-

import time
import ReversiModif
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = ReversiModif.Board(10)
        self._mycolor = None
        self._depth = 4

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
                        tot += 4 # corner
                    elif (x == 0 or x == self._board._boardsize - 1) or (y == 0 or y == self._board._boardsize - 1):
                        tot += 2 # side
                    else:
                        tot += 1
        
        
        return tot
    
    def Minimax(self, depth, maximizingPlayer):
        
        if depth ==0 or not(self._board.at_least_one_legal_move(self._mycolor)):  
            #return self._board.heuristique(self._mycolor)
            return self.heuristique(self._mycolor)

        if maximizingPlayer:
            bestValue = self._board._minEvalBoard
            for m in self._board.legal_moves():
                self._board.push(m)
                v=self.Minimax(depth-1,False)
                self._board.pop()
                bestValue=max(bestValue,v)
                
        else: #minimizingplayer
            bestValue = self._board._maxEvalBoard
            for m in self._board.legal_moves():
                self._board.push(m)
                v=self.Minimax(depth-1,True)

                self._board.pop()
                bestValue=min(bestValue,v)
                
        return bestValue
    
    def AlphaBeta(self,depth,alpha,beta,maximizingPlayer):
        
        if depth ==0 or not(self._board.at_least_one_legal_move(self._mycolor)):  
            #return self._board.heuristique(self._mycolor)
            return self.heuristique(self._mycolor)
        
        if maximizingPlayer:
            v = self._board._minEvalBoard
            for m in self._board.legal_moves():
                self._board.push(m)
                v= max(v,self.AlphaBeta(depth - 1, alpha, beta, False))
                self._board.pop()
                alpha = max(alpha, v)
                if beta <= alpha:
                    break # beta cut-off
            return v
        
        else:
            v =self._board._maxEvalBoard
            for m in self._board.legal_moves():
                self._board.push(m)
                v=v = min(v, self.AlphaBeta(depth - 1, alpha, beta, True))
                self._board.pop()
                beta = min(beta, v)
                if beta <= alpha:
                    break # alpha cut-off
                    
            return v

    def bestMove(self, depth):
        maxPoints = 0
        mx = -1; my = -1
        for m in self._board.legal_moves():
            print(m)
            
            points = self.AlphaBeta(depth,self._board._minEvalBoard,self._board._maxEvalBoard, True)
            #points = self.Minimax(depth, True)
            
            if points > maxPoints:
                    maxPoints = points
                    mx = m[1]; my = m[2]
        print("player=",self._mycolor," mx=",mx," my=",my)
        return [self._mycolor, mx, my]
