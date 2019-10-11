
# Carcassonne
A version of the board game Carcassonne with Monte Carlo AIs, including UCT.

## How to play
The [main_functions.py](https://github.com/T3K14/Carcassonne/blob/master/sources/main_functions.py) script contains the two main functions for simulating AI battles and for playing a game against one AI opponent.

**How to make actions:**
- Every Card has four edges, named 0, 1, 2 and 3, where 0 stands for the upper edge, 1 for the right one, etc. In addition every card has four corners, 4, 5, 6 and 7, where 4 stands for the upper left edge, 5 for the upper right edge, etc.

- For every card that is drawn by the human player an information message is printed to the Console that looks like the following example:
	>Die naechste Karte ist [S, O, S, S, G, False]  
	>Sie enthaelt folgende moegliche Meeplepositionen:  
	>Orte:  
	>1 [1]  
	>Strassen:  
	>1 [0]  
	>2 [2]  
	>3 [3]  
	>Wiesen:  
	>1 [4]  
	>2 [5, 6]  
	>3 [7]  
	>Bitte gib deine Aktion an:
	
	The first number in these lines stands for the name of the territories, the second one in the square brackets stands for the list of edges for the Orte (city) and Straßen (street), or the corners for the Wiesen (fields). 
	
 - The human player has to enter the commands via the Python Console. The format for this is:
 x,  y, number of right rotations of the card, type of territory + name of territory

