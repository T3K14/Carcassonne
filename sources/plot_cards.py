import matplotlib.pyplot as plt
import numpy as np

def display_spielbrett_dict(cards_set):
    bild = plt.figure()
    x_coord_list = []
    y_coord_list = []

    for (a, b) in cards_set:
        x_coord_list.append(a)
        y_coord_list.append(b)

    x_max = max(x_coord_list)
    x_min = min(x_coord_list)

    y_max = max(y_coord_list)
    y_min = min(y_coord_list)

    x_sub = x_max - x_min + 1
    y_sub = y_max - y_min + 1

    from matplotlib.colors import ListedColormap
    custom_cmap = ListedColormap(['green', 'brown', 'white', 'blue', 'k'])

    for nr, info in enumerate(cards_set):
        (x, y) = info
        card = cards_set[info]
        i = (abs(y - y_max)) * x_sub + abs(x - x_min) + 1
        ax = bild.add_subplot(y_sub, x_sub, i)
        ax.title.set_text(str((x,y)))
        ax.matshow(card.matrix, cmap=custom_cmap, vmin=0, vmax=4)

        plt.subplots_adjust(wspace=0, hspace=0)                 # 0, 0
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))
    plt.show()


def draw_card(card):
    from matplotlib.colors import ListedColormap
    custom_cmap = ListedColormap(['green', 'brown', 'white', 'blue', 'k'])
    plt.matshow(card.matrix, 0, cmap=custom_cmap, vmin=0, vmax=4)

    plt.title('Deine Karte')
    plt.xticks(np.array([100]))
    plt.yticks(np.array([100]))
    plt.show()

def display_spielbrett(cards_set):#, choice_list):
    bild = plt.figure()
    x_coord_list = []
    y_coord_list = []
    choice_list = []
    for (a, b), card in cards_set:

        x_coord_list.append(a)
        y_coord_list.append(b)

    x_max = max(x_coord_list)
    x_min = min(x_coord_list)

    y_max = max(y_coord_list)
    y_min = min(y_coord_list)

    x_sub = x_max-x_min+1
    y_sub = y_max-y_min+1

    from matplotlib.colors import ListedColormap
    custom_cmap =  ListedColormap(['green', 'brown', 'white', 'blue', 'k'])

    for nr, info  in enumerate(cards_set):
        (x,y) = info [0]
        card = info[1]
        i = (abs(y-y_max))*x_sub + abs(x-x_min) + 1
        ax = bild.add_subplot(y_sub,x_sub,i)
        ax.title.set_text((x,y))#colormap
        ax.matshow(card.matrix,cmap = custom_cmap, vmin = 0, vmax = 4)
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))

    plt.show()


def display_spielbrett_ohne_text(cards_set):#, choice_list):
    bild = plt.figure()
    x_coord_list = []
    y_coord_list = []
    choice_list = []
    for (a,b), card in cards_set:

        x_coord_list.append(a)
        y_coord_list.append(b)

    x_max = max(x_coord_list)
    x_min = min(x_coord_list)

    y_max = max(y_coord_list)
    y_min = min(y_coord_list)

    x_sub = x_max-x_min+1
    y_sub = y_max-y_min+1

    from matplotlib.colors import ListedColormap
    custom_cmap =  ListedColormap(['green', 'brown', 'white','blue','k'])

    for nr, info  in enumerate(cards_set):
        (x,y) = info [0]
        card = info[1]
        i = (abs(y-y_max))*x_sub + abs(x-x_min) + 1
        ax = bild.add_subplot(y_sub,x_sub,i)
        if (x,y) == (0,0):
            ax.title.set_text((x,y))#colormap
        ax.matshow(card.matrix,cmap = custom_cmap, vmin = 0, vmax = 4)
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))

    plt.show()
