import random
import copy

def play_random(Kartenliste):
    """zieht zufällig karten und setzt diese random""" #mit präferenz auf positionen, die von 3 oder 4 karten umgeben sind """

    Kartenliste_in = copy.deepcopy(Kartenliste)

    c_s_in = copy.deepcopy(cards_set)
    p_c_in = list(possible_coordinates)
    u_c_in = list(unavailable_coordinates)

    random.shuffle(Kartenliste_in)
    running = True

    while running:
        if len(Kartenliste_in) < 1:  # 59
            break
        card = Kartenliste_in[0]

        moegliche_anlegestellen = check_card_to_possible_coordinates(card, p_c_in, c_s_in)

        try:
            choice = random.choice(moegliche_anlegestellen)

            c_s_in, p_c_in, u_c_in = set_card(choice, card, p_c_in, u_c_in, c_s_in)
            del Kartenliste_in[0]
        except IndexError:
            print(card.matrix)
            del Kartenliste_in[0]
            #random.shuffle(Kartenliste_in)
            continue
    # global zahl
    # print("neu",zahl)
    # zahl += 1
    #display_spielbrett(c_s_in)
