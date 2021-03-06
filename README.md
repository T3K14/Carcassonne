
# Carcassonne
A version of the board game Carcassonne with Monte Carlo AIs, including UCT. This Code is part of my [bachelor thesis](https://github.com/T3K14/Carcassonne/blob/master/Bachelorarbeit.pdf) (written in german).

## How to play
The code is written in Python 3.7 and requires the modules numpy and matplotlib.

The [main_functions.py](https://github.com/T3K14/Carcassonne/blob/master/sources/main_functions.py) script contains the two main functions for simulating AI battles and for playing a game against one AI opponent.

There are four AI-Players implemented. The **random_play** function is making moves at random. The **mc** function implements the simple Monte Carlo approach, the **flat_ucb** function implements a modifed MC-player that simulates games according to the UCB selection policy and the **uct** function that implements a standard UCB-player with modificated simulataion evalutaion. The functions are explained in the thesis and in the doc-strings of the functions in the [main_functions.py](https://github.com/T3K14/Carcassonne/blob/master/sources/main_functions.py) script.

**How to make actions:**
- Every Card has four edges, named 0, 1, 2 and 3, where 0 stands for the upper edge, 1 for the right one, etc. In addition every card has four corners, 4, 5, 6 and 7, where 4 stands for the upper left edge, 5 for the upper right edge, etc.

- For every card that is drawn by the human player, a simplified image of the card is drawn to the screen and an information message is printed to the console that looks like the following example:
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
	
	The first line shows the information about the drawn card. The first four letters, here **S, O, S, S** stand for the territory types of the four edges of the card (**S** for streets, **O** for cities and **W** for fields). The fifth letter shows what is in the middle of the card (**G** for a crossing, **K** for a cloister, **O** for a bigger city and **None** for everything else). The boolean at the end of the list is True, if the city of the card owns a shield.
	
	The first number in the number-lines stands for the name of the territories, the second one in the square brackets stands for the list of edges for the Orte (city) and Straßen (street), or the corners for the Wiesen (fields). 
	
 - The human player has to enter the commands via the Python Console. The format for this is:
 x,  y, number of right rotations of the card, type of territory + name of territory

	The territory names are the lowercase letters **o** for cities, **s** for streets, **k** for cloister and **w** for fields and **n** if one doesn't wan't to place a meeple.
	When not placing a meeple, or placing a meeple on a cloister one dosn't have to enter a name of a territory.
	An example for the example might be:
	>Bitte gib deine Aktion ein:-3 2 2 s2
	
	This example stands for the following action:
	- place a **meeple on the street with number 2** (the one that ends on the lower edge of the card) 
	- rotate the card **two times** to the right
	- place the card on the field with the coordinates **(-3, 2)**

	Another example is:
	>Bitte gib deine Aktion ein:0 4 0 n
	
	This example stands for the following action:
		
	- place **no meeple**
	- **don't rotate** the card
	- place the card on the filed with the coordinates **(0, 4)**
		
