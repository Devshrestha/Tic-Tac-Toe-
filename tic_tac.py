import numpy as np
from ENV import Enviroment
Length = 3
class Agent:

    def __init__(self,eps=0.1,alpha=0.3):
        self.eps = eps
        self.alpha= alpha
        self.verbose =False
        self.state_history=[]

    def set_V(self,V):
        self.V=V

    def set_symbol(self,sym):
        self.sym =sym

    def set_verbose(self,v):
        self.verbose=v

    def reset_history(self):
        self.state_history=[]

    def take_action(self,env):
        if self.verbose:
            r = 1
        else:
            r = np.random.rand()
        best_state =None

        if r < self.eps:
            # explore
            if self.verbose:
                print("Taking random action:")
            
            possible_moves = []

            for i in range(Length):
                for j in range(Length):
                    if env.is_empty(i,j):
                        possible_moves.append((i,j))
            idx = np.random.choice(len(possible_moves))
            next_move = possible_moves[idx]
        else:
            # exploit
            pos2value = {}
            next_move =None 
            best_value = -1
            for i in range(Length):
                for j in range(Length):
                    if env.is_empty(i,j):
                        env.board[i][j] = self.sym
                        state = env.get_state()
                        env.board[i][j]=0
                        pos2value[(i,j)]=self.V[state]
                        if self.V[state] > best_value:
                            next_move=(i,j)
                            best_value=self.V[state]
                            best_state = state
        
            if self.verbose:
                print("Taking a greedy action")
                for i in range(Length):
                    print("------------------")
                    for j in range(Length):
                        if env.is_empty(i,j):
                            # print the value
                            print(" %.2f|" % pos2value[(i,j)], end="")
                        else:
                            print("  ", end="")
                            if env.board[i,j] == env.x:
                                print("x  |", end="")
                            elif env.board[i,j] == env.o:
                                print("o  |", end="")
                            else:
                                print("   |", end="")
                    print("")
                print("------------------")

        # make the move
        env.board[next_move[0], next_move[1]] = self.sym

                        
    def update_state_history(self,s):            
        self.state_history.append(s)


    def update(self,env):
        reward = env.reward(self.sym)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha*(target-self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()


class Human:

    def __init__(self):
        pass

    def set_symbol(self,sym):
        self.sym = sym

    def take_action(self,env):
        while True:
            enter = input("Enter a location i,j")
            i,j = enter.split(',')
            i =int(i)
            j = int(j)
            if env.is_empty(i,j):
                env.board[i][j] = self.sym
                break

    def update_state_history(self,env):
        pass

    def update(self,env):
        pass

def get_state_hash_and_winner(env,i=0,j=0):
    result = []
    for v in [0,env.x,env.o]:
        env.board[i][j]=v
        if j ==2:
            if i ==2:
                state = env.get_state()
                ended = env.game_over(force_recalculate=True)
                winner = env.winner
                result.append((state,winner,ended))
            else:
                result+=get_state_hash_and_winner(env,i+1,0)
        else:
            result+=get_state_hash_and_winner(env,i,j+1)
    return result

def initialV_o(env,state_winner_triple):
    V = np.zeros(env.num_states)
    for state,winner,ended in state_winner_triple:
        if ended:
            if winner == env.o:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state]=v
    return V

def initialV_x(env,state_winner_triple):
    V = np.zeros(env.num_states)
    for state,winner,ended in state_winner_triple:
        if ended:
            if winner == env.x:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state]=v
    return V

def play_game(p1,p2,env,draw=False):
    
    current_player = None

    while not env.game_over():
        
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1
        
        if draw:
            if draw == 1 and current_player == p1:
                
                print(env.is_draw())
            if draw == 2 and current_player == p2:
                env.draw_board()
                

        current_player.take_action(env)
        
        state = env.get_state()
        p1.update_state_history(state)
        p2.update_state_history(state)
    
    if draw:
        env.draw_board()
    
    p1.update(env)
    p2.update(env)


if __name__ == '__main__':

    p1 = Agent()
    p2 = Agent()

    env = Enviroment()
    state_winner_triple=get_state_hash_and_winner(env)

    Vx  = initialV_x(env,state_winner_triple)
    p1.set_V(Vx)

    Vo = initialV_o(env,state_winner_triple)
    p2.set_V(Vo)

    p1.set_symbol(env.x)
    p2.set_symbol(env.o)

    for t in range(10000):
        if t%500 == 0:
            print(t)
        play_game(p1,p2,Enviroment())

    human = Human()
    human.set_symbol(env.o)
    while True:
        p1.set_verbose(True)
        play_game(p1, human, Enviroment(), draw=2)
        answer = input("Play again? [Y/n]: ")
        if answer and answer.lower()[0] == 'n':
            break

