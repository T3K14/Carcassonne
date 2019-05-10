Kartenliste = []


import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Karte():
    """erstellt zu jeder eingabe von Infoliste passende Matrix der Karte"""
    def __init__(self,a,b,c,d,m=None,Schild=False):
        self.mitte = m
        self.info = [a,b,c,d,m]
        self.info_alt = [a,b,c,d,m]
        self.matrix = np.array([[0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0]])
        self.info_schild = [a,b,c,d,m,Schild]
        #liste = []
        self.strassen = []
        self.orte = []
        x = True
        while x:
            s = True
            while s:
                #infoliste = self.info
                #print(infoliste)
                for position, status in enumerate(self.info[:-1]):
                    #print(self.info)
                    if status == "S":
                        self.strassen.append((position))
                #print(self.strassen)
                if len(self.strassen) == 2:
                    if self.strassen[0] == 0:
                            if self.strassen[1] == 1:
                                self.matrix[:,3][0:3], self.matrix[3][3:] = 2,2
                            if self.strassen[1] == 2:
                                self.matrix[:,3] = 2
                            if self.strassen[1] == 3:
                                self.matrix[:,3][0:3],self.matrix[3][0:4] = 2,2

                    else:
                        self.info = self.rotate_card_right()
                        #self.matrix = self.rotate_matrix_right()
                        self.strassen=[]
                        continue
                if len(self.strassen) == 3:
                    if self.strassen[0] == 0:
                        if self.strassen[1] == 1:
                            if self.strassen[2] ==2:
                                self.matrix[:,3],self.matrix[3][3:] = 2,2
                            else:
                                self.matrix[:,3][0:3],self.matrix[3] = 2,2
                        if self.strassen[1] == 2:
                            self.matrix[:,3],self.matrix[3][0:3] = 2,2

                    else:
                        self.info= self.rotate_card_right()
                        #self.matrix = self.rotate_matrix_right()
                        self.strassen = []
                        continue
                if len(self.strassen) == 4:
                    self.matrix[:,3],self.matrix[3] = 2,2
                #self.strassen=[]
                s=False

            #liste und matrix auf anfang zurückdrehen? ne, da self.info gedreht wurde, stimmen die ortsplätze
            #noch in bezug auf die strassenplätze

            while True:

                if self.info == self.info_alt:
                    break
                else:
                    self.info = self.rotate_card_right()
                    self.matrix = self.rotate_matrix_right()

            o = True
            while o:

                for position, status in enumerate(self.info[:-1]):
                    if status == "O":
                        self.orte.append((position))
                if len(self.orte) == 1:
                    if self.orte[0] == 0:
                        self.matrix[0] = 1
                    else:
                        self.info = self.rotate_card_right()
                        self.matrix = self.rotate_matrix_right()
                        self.orte = []
                        continue

                if len(self.orte) == 2:
                    #print(self.orte)
                    if self.mitte == "O":
                        if abs(self.orte[0]-self.orte[1]) == 2:         #O,W,O,W,O
                            if self.orte[0] == 0:
                                self.matrix = np.ones(self.matrix.shape)
                                self.matrix[:,0][1:-1], self.matrix[:,6][1:-1] = 0,0
                            else:
                                self.info = self.rotate_card_right()
                                self.matrix = self.rotate_matrix_right()
                                self.orte = []
                                continue
                        elif self.orte[0] == 0:                       #O,O,W,W,O
                            if self.orte[1] == 1:
                                self.matrix[0],self.matrix[:,6],self.matrix[1][1:], self.matrix[:,5][:-1] = 1,1,1,1
                            else:
                                self.info = self.rotate_card_left()
                                self.matrix = self.rotate_matrix_left()
                                self.orte = []
                                continue
                        else:
                            self.info = self.rotate_card_left()
                            self.matrix = self.rotate_matrix_left()
                            self.orte = []
                            continue
                    else:
                        if abs(self.orte[0]-self.orte[1]) == 2:         #O,W,O,W,!=O
                            if self.orte[0] == 0:
                                self.matrix[0], self.matrix[6] = 1,1
                            else:
                                self.info = self.rotate_card_left()
                                self.matrix = self.rotate_matrix_left()
                                self.orte = []
                                continue
                        elif self.orte[0] == 0:
                            if self.orte[1] == 1:
                                self.matrix[0], self.matrix[:,6] = 1, 1
                            else:
                                self.info = self.rotate_card_left()
                                self.matrix = self.rotate_matrix_left()
                                self.orte = []
                                continue
                        else:
                            self.info = self.rotate_card_left()
                            self.matrix = self.rotate_matrix_left()
                            self.orte = []
                            continue
                if len(self.orte) == 3:
                    #if "S" not in self.info[:-1]:
                        for i in [0,1,2,3]:
                            if self.info[0] == "O":
                                self.info = self.rotate_card_right()
                                self.matrix = self.rotate_matrix_right()
                                self.orte = []
                                continue
                            elif self.info[0] != "O":
                                self.matrix = np.ones((7,7))
                                self.matrix[1][2:-2], self.matrix[0][1:-1] = 0,0
                                if "S" in self.info:
                                    self.matrix[:,3][:2] = 2
                                break

                if len(self.orte) == 4:
                    self.matrix = np.ones((7,7))

                #self.orte = []
                o = False
            if self.mitte == "K":
                self.matrix[3][3] = 3
                if "S" in self.info:
                    self.matrix[:,3][4:] = 2
            if self.mitte == "G":
                self.matrix[3][3] = 4

            x=False


        #dient dazu nach erstellen der karte, info und matrix auf ausgangsposition zu drehen
        while True:
                if self.info == self.info_alt:
                    break
                else:
                    self.info = self.rotate_card_right()
                    self.matrix = self.rotate_matrix_right()




    def rotate_card_left(self):
        info = []
        for i, seite in enumerate(self.info):
            info.append(self.info[i])
        for i, seite in enumerate(info[:-1]):
            if i == 3:
                info[i] = self.info[0]
            else:
                info[i] = info[i+1]
        return(info)

    def rotate_card_right(self):
        info = []
        for i, seite in enumerate(self.info):
            info.append(self.info[i])
        for i, seite in enumerate(info[:-1]):
            if i == 0:
                info[0] = self.info[-2]
            else:
                info[i] = self.info[i-1]
        return(info)

    def rotate_matrix_right(self):
        m_neu = self.matrix.transpose()
        for zeile in range(7):
            row = m_neu[zeile]
            for i in range(3):
                row[i], row[-(i+1)] = row[-(i+1)], row[i]
        return (m_neu)

    def rotate_matrix_left(self):
        m_neu = self.matrix.transpose()
        for spalte in range(7):
            column = m_neu[:,spalte]
            for i in range(3):
                column[i], column[-(i+1)] = column[-(i+1)], column[i]
        return (m_neu)





Karteninfos = ["4WWWWK","8WWSWK","OOOOOT","3SOSW","5OWWW","2WOWOOT","OWOWO","3WOWO","2WOOW","3OSSW","3SOWS",
               "3SOSSG","2OWWOOT","3OWWOO","2OSSOOT","3OSSOO","OOWOOT","3OOWOO","2OOSOOT","OOSOO","8SWSW",
               "9WWSS","4WSSSG","SSSSG"]
Karteninfos_neu = []

for pos,card in enumerate(Karteninfos):
    i = list(card)

    try :
        if int(i[0]) in range(10):

            for z in range(int(i[0])):
                Karteninfos_neu.append(card[1:])

    except ValueError:
        nr = 0
        Karteninfos_neu.append(card)

#print(Karteninfos_neu)

for card in Karteninfos_neu:
    i = list(card)

    try :
        nr = int(i[0])
        del i[0]
    except ValueError:
        nr = 1

    if len(i) == 4:
        a,b,c,d,m,schild = i[0],i[1],i[2],i[3],None,False
    elif len(i) == 5:
        a,b,c,d,m,schild = i[0],i[1],i[2],i[3],i[4],False
    else:
        a,b,c,d,m,schild = i[0],i[1],i[2],i[3],i[4],True

    card_to_add = Karte(a,b,c,d,m,schild)
    for i in range(nr):
        Kartenliste.append(card_to_add)

unavailable_coordinates = [(0,0)]


def rotate_card_left(infoliste):
    info = []
    for i, seite in enumerate(infoliste):
        info.append(infoliste[i])
    for i, seite in enumerate(info[:-1]):
        if i == 3:
            info[i] = infoliste[0]
        else:
            info[i] = info[i+1]
    return(info)

def rotate_card_right(infoliste):
    info = []
    for i, seite in enumerate(infoliste):
        info.append(infoliste[i])
    for i, seite in enumerate(info[:-1]):
        if i == 0:
            info[0] = infoliste[-2]
        else:
            info[i] = infoliste[i-1]
    return(info)

def rotate_matrix_right(matrix):
    m_neu = matrix.transpose()
    for zeile in range(7):
        row = m_neu[zeile]
        for i in range(3):
            row[i], row[-(i+1)] = row[-(i+1)], row[i]
    return (m_neu)

def rotate_matrix_left(matrix):
    m_neu = matrix.transpose()
    for spalte in range(7):
        column = m_neu[:,spalte]
        for i in range(3):
            column[i], column[-(i+1)] = column[-(i+1)], column[i]
    return (m_neu)




#k = Karte("S","O","S","W")
#l = Karte("O","O","O","O")
#m = Karte("S","S","O","W")
#n = Karte("W","W","S","S")
#o = Karte("W","S","S","W")
#p = Karte("S","W","S","W")
#q = Karte("S","W","W","S")

#cards_set =[((0,0),k),((1,0),l),((1,1),m),((1,2),n),((0,2),o),((-1,1),p),((-1,0),q)]
#possible_coordinates=[(0,1),(-1,2),(0,3),(1,3),(2,2),(3,1),(2,0),(1,-1),(0,-1),(-1,0)]



def check_card_to_possible_coordinates(Karte,possible_coordinates,cards_set):
    """checkt, ob und wie karte an jede freie stelle gelegt werden kann,
        returned liste mit tupel bestehend aus möglicher anlegestelle und anzahl von rotationen die dafür nötig sind """

    possible_anlegemöglichkeiten = []
    possible_anlegemöglichkeiten_3 = []
    possible_anlegemöglichkeiten_4 = []

    card = Karte


    ij = [(0,2),(1,3),(2,0),(3,1)]
    for x,y in possible_coordinates:
        nkoos = [(x,y+1),(x+1,y),(x,y-1),(x-1,y)]
        nks = []

        for relative_pos, nkoo in enumerate(nkoos):
            for gelegte_karte in cards_set:
                if gelegte_karte[0] ==nkoo:
                    nks.append((gelegte_karte,relative_pos))

        if len(nks) == 1:
            i,j = ij[nks[0][1]]
            for z in range(4):
                if card.info[i] == nks[0][0][1].info[j]:
                    possible_anlegemöglichkeiten.append(((x,y),z))
                card.info = rotate_card_right(card.info)

        if len(nks) == 2:
            ij_neu = [ij[nks[länge][1]] for länge in range(len(nks))]
            for z in range(4):

                i,j = ij_neu[0]
                if card.info[i] == nks[0][0][1].info[j]:
                    i,j = ij_neu[1]
                    if card.info[i] == nks[1][0][1].info[j]:
                        possible_anlegemöglichkeiten.append(((x,y),z))
                card.info = rotate_card_right(card.info)

        if len(nks) == 3:
            ij_neu = [ij[nks[länge][1]] for länge in range(len(nks))]
            for z in range(4):

                i,j = ij_neu[0]
                if card.info[i] == nks[0][0][1].info[j]:
                    i,j = ij_neu[1]
                    if card.info[i] == nks[1][0][1].info[j]:
                        i,j = ij_neu[2]
                        if card.info[i] == nks[2][0][1].info[j]:
                            possible_anlegemöglichkeiten.append(((x,y),z))
                            possible_anlegemöglichkeiten_3.append(((x,y),z))

                card.info = rotate_card_right(card.info)

        if len(nks) == 4:
            ij_neu = [ij[nks[länge][1]] for länge in range(len(nks))]
            for z in range(4):

                i,j = ij_neu[0]
                if card.info[i] == nks[0][0][1].info[j]:
                    i,j = ij_neu[1]
                    if card.info[i] == nks[1][0][1].info[j]:
                        i,j = ij_neu[2]
                        if card.info[i] == nks[2][0][1].info[j]:
                            i,j = ij_neu[3]
                            if card.info[i] == nks[3][0][1].info[j]:
                                possible_anlegemöglichkeiten.append(((x,y),z))
                                possible_anlegemöglichkeiten_4.append(((x,y),z))
                                #print(card.matrix)

                card.info = rotate_card_right(card.info)
    #if len(possible_anlegemöglichkeiten) == 0:
    return(possible_anlegemöglichkeiten,possible_anlegemöglichkeiten_3,possible_anlegemöglichkeiten_4)

def set_card(tuple,Karte,possible_coordinates,unavailable_coordinates,cards_set):                   #parameter karte einfügen
    """setzt karte an koordinaten (x,y) und updated cards_set und possible_coordiantes"""
    (x,y) = tuple[0]
    z = tuple[1]
    #Karte = Kartenliste[0]
    for i in range(z):
        Karte.info = rotate_card_right(Karte.info)
        Karte.matrix = rotate_matrix_right(Karte.matrix)

    cards_set.append(((x,y),Karte))

    for i,(v,w) in enumerate(possible_coordinates):
        if (x,y) == (v,w):
            unavailable_coordinates.append((v,w))
            del possible_coordinates[i]
            for (a,b) in [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]:
                if (a,b) not in possible_coordinates and (a,b) not in unavailable_coordinates:
                    possible_coordinates.append((a,b))


    return cards_set,possible_coordinates,unavailable_coordinates


cards_set = [((0,0),Karte("S","O","S","W"))]
possible_coordinates=[(0,1),(1,0),(0,-1),(-1,0)]

def display_spielbrett(cards_set):#, choice_list):
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
import copy

def play_random(Kartenliste):
    """zieht zufällig karten und setzt diese mit präferenz auf positionen, die von 3 oder 4karten umgeben sind """
    choice_list = []
    Kartenliste_in = copy.deepcopy(Kartenliste)

    c_s_in = copy.deepcopy(cards_set)
    p_c_in = list(possible_coordinates)
    u_c_in = list(unavailable_coordinates)


    #print (Kartenliste_in[0], Kartenliste[0])
    random.shuffle(Kartenliste_in)
    nulf = 1
    running = True
    while running:

        #print(len(Kartenliste_in))
        if len(Kartenliste_in) == 0:             #59
            break

        card = Kartenliste_in[0]
        #print (nulf,":",card.info)
        #print(card.matrix)
        mögliche_anlegestellen,mögliche_anlegestellen_3,mögliche_anlegestellen_4 = check_card_to_possible_coordinates(card,p_c_in,c_s_in)
        #print(mögliche_anlegestellen)
        try:
            choice_4 = random.choice(mögliche_anlegestellen_4)
            choice_list.append(choice_4[0])
            c_s_in,p_c_in,u_c_in = set_card(choice_4,card,p_c_in,u_c_in,c_s_in)
            #print("CHOICE_4:",choice_4)
            del Kartenliste_in[0]
            nulf += 1
            #display_spielbrett_ohne_text(c_s_in)

            continue


        except IndexError:
            try:
                choice_3 = random.choice(mögliche_anlegestellen_3)
                choice_list.append(choice_3[0])
                c_s_in,p_c_in,u_c_in = set_card(choice_3,card,p_c_in,u_c_in,c_s_in)
                #print("CHOICE_3:",choice_3)
                del Kartenliste_in[0]
                nulf += 1
                #display_spielbrett_ohne_text(c_s_in)

                continue


            except IndexError:
                try:
                    choice = random.choice(mögliche_anlegestellen)
                    choice_list.append(choice[0])
                    c_s_in,p_c_in,u_c_in = set_card(choice,card,p_c_in,u_c_in,c_s_in)
                    #print(choice)
                    del Kartenliste_in[0]
                    nulf += 1
                    #display_spielbrett_ohne_text(c_s_in)


                except IndexError:
                    print(card.matrix)
                    random.shuffle(Kartenliste_in)
                    continue

        #choice_list.append(choice[0])


        #c_s_in,p_c_in,u_c_in = set_card(choice,card,p_c_in,u_c_in,c_s_in)


        #print(choice)#,card.matrix)


        #del Kartenliste_in[0]
        #nulf += 1

    display_spielbrett_ohne_text(c_s_in)
        #print("\n")
    #display_spielbrett(c_s_in)
    print("neu\n\n")


while True:
    play_random(Kartenliste)
    #display_spielbrett_ohne_text()
