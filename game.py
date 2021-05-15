import curses
import numpy as np
import time
from curses import textpad
from collections import deque
from player import Player


class Game:
    def __init__(self, width=40, height=30, level=1):
        self.stdscr = curses.initscr()

        # compare the current window dimension and the given dimension
        # if the given dimension is greater than the window size
        # use the full window as the game board
        y, x = self.stdscr.getmaxyx()
        if width > x:
            self.width = x - 1
        elif width < 40:
            self.width = 39
        else:
            self.width = width-1

        # one extra line for showing score
        if height > y:
            self.height = y - 2
        elif height < 20:
            self.height = 18
        else:
            self.height = height-2

        # initialize the inner width, inner height and difficult level
        self.innerWidth = self.width-1
        self.innerHeight = self.height-1
        self.diff_factors = [97, 90, 85]
        self.level = min(len(self.diff_factors), level) - 1
        self.gameover = False
        self.score = 0

        # initialize the board to be empty
        self.board = deque()
        for _ in range(self.innerHeight):
            self.board.append(np.zeros(self.innerWidth, dtype=int))

    # function to run run the game
    def run(self):
        self.main()
        curses.endwin()

    def main(self):
        # curses initialization
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)

        # initialize the rectangle
        textpad.rectangle(self.stdscr, 0, 0, self.height, self.width)

        # create a new player instance for the game
        player = Player(self.innerWidth // 2 + 1, self.innerHeight)
        ticks = 0

        while(not self.gameover):
            # get the user's input
            key = self.stdscr.getch()

            # store the player's previous position for later use
            x = player.getX()
            y = player.getY()

            if key == curses.KEY_RIGHT:
                player.setX(min(x+1, self.innerWidth))
            elif key == curses.KEY_LEFT:
                player.setX(max(1, x-1))

            self.stdscr.addstr(y, x, ' ')

            # generate new obstacles every 10 loops
            if ticks % 10 == 0:
                ticks = 0
                self.updateBoard()
                # update the current score
                self.score += 1
                self.showScore()

            # update the player's position
            self.updatePlayer(player)

            self.stdscr.refresh()
            ticks += 1
            time.sleep(0.02)

        # gameover, show the gameover message
        self.showGameover()

        self.stdscr.nodelay(0)
        key = self.stdscr.getch()

        # only hitting q can exit the program
        while key != ord('q'):
            key = self.stdscr.getch()

    # randomly generate the next round of obstacles
    def generateNext(self):
        diff_factor = self.diff_factors[self.level]
        nextArr = np.random.randint(0, 100, size=self.innerWidth)

        nextArr[nextArr < diff_factor] = 0
        nextArr[nextArr > 0] = 1

        return nextArr

    # update the board to show the next round of obstacles
    def updateBoard(self):
        self.board.appendleft(self.generateNext())

        # remove the obstacles that are out of the screen
        self.board.pop()

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if(self.board[i][j] == 0):
                    self.stdscr.addstr(i+1, j+1, ' ')
                else:
                    self.stdscr.addstr(i+1, j+1, '_')

    # update the player's position on the board
    def updatePlayer(self, player):
        if(self.board[player.getY()-1][player.getX()-1] == 1):
            self.stdscr.addstr(player.getY(), player.getX(), 'x')
            self.gameover = True
        else:
            self.stdscr.addstr(player.getY(), player.getX(), '*')

    # function to show the current score to the user
    def showScore(self):
        score_text = "Score: {}".format(self.score)
        self.stdscr.addstr(self.height + 1, self.width -
                           len(score_text), score_text)

    # function to show game over message to the user
    def showGameover(self):
        gameover_text = "Game Over, press q to exit"
        self.stdscr.addstr(self.height + 1, 1, gameover_text)
