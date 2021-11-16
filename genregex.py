import re


def count_up_low_digit(word):
    u = [x for x in word if x.isupper()]
    l = [x for x in word if x.islower()]
    n = [x for x in word if x.isdigit()]
    return len(u), len(l), len(n)


def removeu(word):
    pattern = "[A-Z]"
    word = [re.sub(pattern, '', i) for i in word]
    word = [x for x in word if x]
    return word


def removel(word):
    pattern = "[a-z]"
    word = [re.sub(pattern, '', i) for i in word]
    word = [x for x in word if x]
    return word


def removen(word):
    pattern = "[0-9]"
    word = [re.sub(pattern, '', i) for i in word]
    word = [x for x in word if x]
    return word


def obtenerColumnas(posible):
    pr = []
    final = []
    for string in posible:
        patron = "]]"
        a = re.findall(patron, string)
        if a:
            pip = string.replace("]", "", 1).split("[")
        else:
            pip = string.replace("]", "").split("[")
        dele = "{\d}|{\d\d}|{\d\d\d}"
        del pip[0]
        for ele in pip:
            res = re.sub(dele, "", ele)
            pr.append(res)
        final.append(pr)
        pr = []
    return final


def limpiar(value):
    fila = list(dict.fromkeys(value))
    u, l, n = count_up_low_digit(fila)
    patron1 = "a-z"
    patron2 = "A-Z"
    patron3 = "0-9"
    a = re.findall(patron1, value)
    b = re.findall(patron2, value)
    c = re.findall(patron3, value)
    value = value.replace("\\", "")
    aux = ""
    if a or l > 10:
        aux += "a-z"
        value = removel(value)
    if b or u > 10:
        aux += "A-Z"
        value = removeu(value)
    if c or n > 4:
        aux += "0-9"
        value = removen(value)
    for ele in list(dict.fromkeys(value)):
        if ele in "-_=+":
            aux += "\\" + ele
        else:
            aux += ele
    return aux


def generate_regex(samples):
    maximo = len(max(samples, key=len))
    columna = []
    i = 0
    strg = "["
    aux = ""
    while i < maximo:
        for linea in samples:
            if i < len(linea):
                columna.append(linea[i])
        columna = list(dict.fromkeys(columna))
        for ele in columna:
            aux += ele
        aux = limpiar(aux)
        strg += aux
        strg += "]["
        columna = []
        aux = ""
        i = i + 1
    strg = strg[:-1]
    return strg


def regex(samples):
    fila = []
    posible = []
    i = 0
    while i < len(samples):
        j = 0
        str = ""
        while j < (len(samples[i]) + 2):
            str += "["
            if samples[i][j].isdigit() or samples[i][j].isupper() or samples[i][j].islower() or samples[i][j] in "-_=+":
                while samples[i][j].isdigit() or samples[i][j].isupper() or samples[i][j].islower() or samples[i][
                    j] in "-_=+":
                    fila.append(samples[i][j])
                    j += 1
                    if j > (len(samples[i]) - 1):
                        break
                largototal = len(fila)
                caca = list(dict.fromkeys(fila))
                if len(caca) > 3:
                    u, l, n = count_up_low_digit(fila)
                    if u > 10:
                        str += "A-Z"
                        fila = removeu(fila)
                    if l > 10:
                        str += "a-z"
                        fila = removel(fila)
                    if n > 4:
                        str += "0-9"
                        fila = removen(fila)
                    for ele in fila:
                        if ele in "-_=+":
                            str += "\\" + ele
                        else:
                            str += ele
                    str += "]{%d}" % largototal
                    fila = []
                else:
                    for ele in fila:
                        str += ele
                    str += "]{%d}" % largototal
                    fila = removen(fila)
                    fila = removel(fila)
                    fila = removeu(fila)
            else:
                if j > (len(samples[i]) - 1):
                    break
                if samples[i][j] == "[" or samples[i][j] == "]":
                    str += "\\" + samples[i][j] + "]{1}"
                    j += 1
                else:
                    str += samples[i][j] + "]{1}"
                    j += 1
            if j > (len(samples[i]) - 1):
                break
        posible.append(str)
        i += 1
    return posible


def getRegexId(samples):
    global valor
    posible = regex(samples)
    col = obtenerColumnas(posible)
    strg = generate_regex(col)
    r = []
    po = []
    for a in posible:
        f = a.split("[")
        for l in f:
            j = l.split("{")
            if len(j) > 1:
                r.append(j[1].replace("}", ""))
        po.append(r)
        r = []
    strg = strg.split("[")
    del strg[0]
    maximo = len(strg)
    columna = []
    i = 0
    while i < maximo:
        for linea in po:
            if i < len(linea):
                columna.append(int(linea[i]))
        columna = list(dict.fromkeys(columna))
        if columna:
            maxis = max(columna)
            mini = min(columna)
            if int(mini) > int(maxis):
                valor = "{%s,%s}" % (maxis, mini)
            elif (int(mini) == int(maxis)) and maxis == 1:
                valor = "{%s}" % (maxis)
            else:
                valor = "{%s,%s}" % (mini, maxis)
        strg[i] = strg[i] + valor
        columna = []
        i = i + 1
    result = ""
    for ele in strg:
        result += "[" + ele
    return result
