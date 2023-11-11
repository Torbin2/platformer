# platformer game
`a` and `d` to move sideways\
and `space` to switch gravity

# platformer-TASTools

# **Requires pygame version `2.5.2`**

## Current features
- Recording inputs
- Playing inputs
- Frame advance
- ~Frame depart~ (removed by terukaaz because it was broken and savestates also worked)
- ~Savestates (beta, save states with key `w` and load it with key `2`)~ (Currently broken, being fixed)

## Usage
- Change the text inside tasconfig.txt to "read" or "write"
  - If the mode is set to "write", the program tries to write the inputs to the file. After rerunning the program with mode "write" whilst the input file with the same name exists, the program deletes the file and overwrite it.
  - If the mode is set to "read", the program tries to read the inputs from the file. After finishing playing all the inputs, it will crash the game.
- `left` and `right` to advance frame or go back
- `up` to freeze time
