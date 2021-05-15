# Spaceship Dodge Game
A terminal base spaceship dodge game

## How to play
### Install dependence
make sure you install these two package: `numpy` and `curses`, you can install them by doing:
```
pip install numpy
pip install windows-curses
```
note: you might not need to install `curses` if you are on a Linux systems

### Run the game
Then in the root director of this project run:
```
python spaceship.py
```
This will start the game with the default dimension and level of difficulity(default is level 1), you can also provide dimension and difficulity(1-3) by running:
```
python spaceship.py --width=50 --height=50 --level=3
```

### Control
Use left and right arrows to control the spaceship to avoid the coming obstacles. 