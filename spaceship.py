import sys
import getopt
from game import Game

if __name__ == "__main__":
    # read the argument from the command
    opts, args = getopt.getopt(
        sys.argv[1:], '', ['width=', 'height=', 'level='])

    # if there is not enough argument provided, start the game using default value
    if len(opts) != 3:
        b = Game()
    else:
        game_args = [0] * 3
        for opt, arg in opts:
            if opt == '--width':
                game_args[0] = int(arg)
            if opt == '--height':
                game_args[1] = int(arg)
            if opt == 'level':
                game_args[2] = int(arg)
        #run the game with the given width, height and level of difficulty
        b = Game(game_args[0], game_args[1], game_args[2])
    b.run()
