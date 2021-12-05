import numpy as np


class Enviroment:
    
    def __init__(self):

        self.Length = 3
        self.board = np.zeros((self.Length,self.Length))
        self.x=-1
        self.o=1
        self.winner=None
        self.ended = False
        self.num_states = 3**(self.Length*self.Length)

    def reward(self,sym):
        if not self.game_over():
            return 0
        
        if self.winner == sym:
            return 1
        else:
            return 0

    def is_empty(self,i,j):
        return self.board[i][j]==0
        

    def fill_board(self):
        self.board=[[1,-1,0],[-1,1,-1],[-1,1,-1]]

    def draw_board(self):

        for i in range(self.Length):
            print("-------------")

            for j in range(self.Length):
                print("|",end='')

                if self.board[i][j]==self.x:
                    print(' X ',end='')

                elif self.board[i][j]==self.o:
                    print(' O ',end='')

                else:
                    print('   ',end='')

            print('|',end='')
            print(' ')

        print("-------------")

    

    def game_over(self,force_recalculate=False):

        if not force_recalculate and self.ended:
          return self.ended

        # return true if someone won false if draw or not ended
        
        # checking along horizontals 
        for i in range(self.Length):
            for player in (self.x,self.o):
                if np.sum(self.board[i])==player*self.Length:
                    self.winner = player
                    self.ended  = True
                    return True
        #checking along verticals
        for player in (self.x,self.o):
            for i in range(self.Length):
                total = self.board[0][i]+self.board[1][i]+self.board[2][i]
                if total == player*self.Length:
                    self.winner = player
                    self.ended  = True
                    return True
        #checking along first diagonal
        for player in (self.x,self.o):
            total = 0        
            for i in range(self.Length):
                total+= self.board[i][i]
            if total == player*self.Length:
                self.winner = player
                self.ended = True
                return True

        #checking along second diagonal
        for player in (self.x,self.o):
            total= self.board[0][2] + self.board[1][1] + self.board[2][0]
            if total == player*self.Length:
                self.winner = player
                self.ended = True
                return True
            
        
        
        # check for draw
        if np.all((self.board == 0) == False):
      # winner stays None
            self.winner = None
            self.ended = True
            return True

    # game is not over
        self.winner = None
        return False

    def is_draw(self):
        return  self.winner and self.ended is None 
    
    def get_state(self):
        h=0
        k=0
        for i in range(self.Length):
            for j in range(self.Length):
                if self.board[i][j] == 0:
                    v = 0
                elif self.board[i][j] == self.x:
                    v = 1
                elif self.board[i][j]==self.o:
                    v = 2
                
                h+= (3**k)*v
                k+=1
        return h
        
if __name__ == '__main__':

    g = Enviroment()
    
    g.draw_board()
    print(g.get_state())