# Draughts

# Rules

## Initial state

* 12 pieces for each player
* Only dark fields are occupied

## Pieces
### Men
* Can jump forward diagonally
* Can jump over hostile pieces and therefore capture it
* Can mulit-jump over successive hostile pieces, the direction can change in one jump
### King
* Is additionally able to jump backwards diagonally
* Can furthermore capture kings
## Win/Loss
* No pieces from one party are left
or
* no allowed moves are left 
#Interfaces
## env.step(actions) returns observation, reward, done, info
* actions: tuple(pieceID, np.array(posx, posy))
* observation: np.array([8, 8, 3])->[posy, posx, type] with type=0:empty / 1: white stone / 2: black / 3: white king / 4: black king
* reward: int
* done: boolean if terminal state is reached
* info: tbd
