import numpy as np
import pickle
import player_first_threebythree as pl_f
BOARD_SIZE = 9


class State:
    def __init__(self, p1, p2):
        self.board = [
            "-", "-", "-",
            "-", "-", "-",
            "-", "-", "-"
        ]
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        # init p1 plays first
        self.playerSymbol = "X"

    # get unique hash of current board state
    def get_hash(self):
        '''
        Used to create a hash for storing in  a state-value dictionary
        '''
        self.boardHash = str(self.board)
        return self.boardHash

    def winner(self):
        winner = pl_f.check_win(self.board, False)

        if winner == "X":
            self.isEnd = True
            return 1
        if winner == "O":
            self.isEnd = True
            return -1

        # tie
        # no available positions
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # not end
        self.isEnd = False
        return None

    def getHash(self):
        '''
        Used to create a hash for storing in  a state-value dictionary
        '''
        self.boardHash = str(self.board)
        return self.boardHash

    def availablePositions(self):
        positions = []
        for i in range(BOARD_SIZE):
            if self.board[i] == "-":
                positions.append(i)  # need to be tuple | um why?
        return positions

    def updateState(self, position):
        self.board[position] = self.playerSymbol
        # switch to another player
        self.playerSymbol = "O" if self.playerSymbol == "X" else "X"

    # only when game ends
    def giveReward(self):
        result = self.winner()
        # backpropagate reward
        if result == 1:
            self.p1.feedReward(1)
            # self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            # self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            # self.p2.feedReward(0.5)

    # board reset
    def reset(self):
        self.board = [
            "-", "-", "-",
            "-", "-", "-",
            "-", "-", "-"
        ]
        self.boardHash = None
        self.isEnd = False

        self.playerSymbol = "X"

    def train(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(
                    positions, self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                # check board status if it is end

                win = self.winner()
                if win is not None:
                    # self.showBoard()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    # self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2, minimax algorithm
                    positions = self.availablePositions()
                    # p2_action = self.p2.chooseAction(
                    #     positions, self.board, self.playerSymbol)
                    p2_action = self.p2.choose_action(self.board)

                    # action would be a single digit
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    # self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        # self.p2.reset()
                        self.reset()
                        break

    # play with human
    def play2(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(
                positions, self.board, self.playerSymbol)
            # take action and upate board state
            self.updateState(p1_action)
            self.showBoard()
            print()

            # check board status if it is end
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.choose_action(positions)

                self.updateState(p2_action)
                self.showBoard()
                print()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def showBoard(self):
        """
        Displays the board in a 3x3 grid
        """
        print(self.board[0] + " | " + self.board[1] + " | " + self.board[2])
        print(self.board[3] + " | " + self.board[4] + " | " + self.board[5])
        print(self.board[6] + " | " + self.board[7] + " | " + self.board[8])


class AI_minimax:
    def choose_action(self, board):
        return pl_f.find_best_move(board)


class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value

    def getHash(self, board):
        boardHash = str(board)
        return boardHash

    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(
                    next_boardHash) is None else self.states_value.get(next_boardHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action

    # append a hash state
    def addState(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * \
                (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def choose_action(self, positions):
        while True:
            row = int(input("Input a number from 1-9:"))
            action = (row - 1)
            if action in positions:
                return action

    # append a hash state
    def addState(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        pass

    def reset(self):
        pass


def play_game():
    # training
    # p1 = Player("p1")
    # p2 = AI_minimax()

    # st = State(p1, p2)
    # print("training...")
    # st.train(100000)

    # p1.savePolicy()

    # play with human
    p1 = Player("computer", exp_rate=0)
    p1.loadPolicy("policy_p1")

    p2 = HumanPlayer("human")

    st = State(p1, p2)
    st.play2()

play_game()
# WORKS!