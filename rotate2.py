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

def rotate_list_right(s_o_list):
    for pos, i in enumerate(s_o_list):
        if i == 3:
            s_o_list[pos] = 0
        else:
            s_o_list[pos] = i + 1
    return s_o_list

def rotateWiesenRight(liste):
    for wiese in liste[:]:
        for pos, i in enumerate(wiese[1]):
            if i == 7:
                wiese[1][pos] = 4
            else:
                wiese[1][pos] += 1
    return liste

if __name__ == "__main__":

    list = [0]
    list2 = list

    rotate_list_right(list)

    print(list, list2)