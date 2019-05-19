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


def rotate_info_right(infoliste):
    """takes eg list ["O", "S", "S", "W"] and swaps elements according to a right rotation of the card"""
    info = [infoliste[-1], 1, 2, 3]
    for i in info[1:]:
        info[i] = infoliste[i-1]
    return info


def rotate_list_right(s_o_list):
    """takes strassen or orts or wiesenkantenlist and changes edges according to a right rotation"""
    for pos, i in enumerate(s_o_list):
        if i == 3:
            s_o_list[pos] = 0
        else:
            s_o_list[pos] = i + 1
    return s_o_list


def rotate_matrix_right(matrix):
    m_neu = matrix.transpose()
    for zeile in range(7):
        row = m_neu[zeile]
        for i in range(3):
            row[i], row[-(i+1)] = row[-(i+1)], row[i]
    return m_neu

def rotate_matrix_left(matrix):
    m_neu = matrix.transpose()
    for spalte in range(7):
        column = m_neu[:,spalte]
        for i in range(3):
            column[i], column[-(i+1)] = column[-(i+1)], column[i]
    return (m_neu)



def rotateWiesenRight(liste):
    for wiese in liste[:]:
        for pos, i in enumerate(wiese[1]):
            if i == 7:
                wiese[1][pos] = 4
            else:
                wiese[1][pos] += 1
    return liste

def rotate_card_right(infoliste):
    """noch fuer rueckwaertskompatibilitaet drin"""
    info = []
    for i, seite in enumerate(infoliste):
        info.append(infoliste[i])
    for i, seite in enumerate(info[:-1]):
        if i == 0:
            info[0] = infoliste[-2]
        else:
            info[i] = infoliste[i-1]
    return(info)


def rotate_kanten_dict_right(dic):
    d = {}
    for i in dic:
        if i == 0:
            d.update({i: dic[3]})
        else:
            d.update({i: dic[i-1]})

    return d

if __name__ == "__main__":

    s = [1, 2]
    inf = ["O", "S", "S", "W"]

    print(rotate_list_right(s))
