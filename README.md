# ShooterAI

ShooterAI is a Python project aimed at teaching robots to play a game similar to the showdown mode in Brawl Stars. The goal is to use genetic algorithms to observe different evolutions over generations.

## Game Rules:

It's a 3v3 shooting game lasting for 90 seconds. Players cannot be revived once dead. The game ends when an entire team dies or when time runs out. If neither team wins within the allotted time, it's a draw.

Game statistics are recorded using the `database.py` file, where information such as scores and remaining health points are stored.

## Current Progress:

At the moment, the game version is complete. I've coded the game so that we can easily modify the speed of time passage while keeping the "proportions" of time to shorten long gameplay times. The game isn't visually appealing, but the goal is to have gameplay similar to Brawl Stars.

I've also structured the game so that we can only modify the `ia.py` file if we want to add an AI. I haven't started on the AI yet because it seems quite challenging. Currently, the robot makes decisions randomly. To make decisions, the AI needs to assign values to `direction.x` and `direction.y` and activate the `shoot(x, y)` function with `x` and `y` being the position where the shot should be made. 

I was thinking of simply selecting the top 3 winners and keeping them, while eliminating the other 3.

I've placed important constants in the `config.txt` file. Feel free to modify it; it works without any issues.

Don't hesitate to ask for help if you don't understand certain parts; I'll gladly respond!
