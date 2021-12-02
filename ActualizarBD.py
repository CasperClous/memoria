import mysql.connector
from mysql.connector import errorcode
from genregex import getRegexId
import re
import string
import itertools
import time


separador = " # "


def ConectarBaseDeDatos():
    cnx = ""
    curs = ""
    try:
        cnx = mysql.connector.connect(user='obtenerRegex', password='Obtener17489563', host='localhost',
                                      database='Validator', auth_plugin='mysql_native_password')
        curs = cnx.cursor()
        print("Conectado a la BD")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            cnx.close()
    return cnx, curs


def InsertBD():
    cnx = ""
    curs =""
    try:
        cnx = mysql.connector.connect(user='addCorreo', password='CorreoV@lidator2021', host='192.168.100.86', database='Validator', auth_plugin='mysql_native_password')
        curs = cnx.cursor()
        print("Conectado a la BD")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            cnx.close()
    return cnx, curs


def getRegexMSGID(regex, valores):
    aux = []
    for line in valores:
        if re.match(regex, line) is not None:
            aux.append(line)
    for ele in aux:
        valores.remove(ele)
    return valores


def MSGID(line):
    valores = []
    regexes = []
    query = f"SELECT MSGID FROM Validator.Coleccion WHERE FROMM = \"{line}\" "
    curs.execute(query)
    resultadosFROMM = curs.fetchall()
    for linea in resultadosFROMM:
        linea = linea[0]
        valores.append(linea.replace("]","").replace("[",""))
    while len(valores) > 0:
        regex = getRegexId(valores)
        valores = getRegexMSGID(regex, valores)
        regexes.append(regex)
    stringa = ""
    for a in list(dict.fromkeys(regexes)):
        stringa += a + separador
    stringa = stringa[:-3]
    return stringa


def getRegexReceived(FROMM, Received):
    global valores
    valores = []
    query = f"SELECT {Received} FROM Validator.Coleccion WHERE FROMM = \"{FROMM}\" "
    curs.execute(query)
    resultados = curs.fetchall()
    auxfrom = []
    auxby = []
    regexes = []
    for line in resultados:
        if line[0] is not None:
            linea = line[0].split(" ")
            for i,ele in enumerate(linea):
                if ele == "from":
                    auxfrom.append(linea[i+1].replace("[","").replace("]",""))
                if ele == "by" and not linea[i+1] == "mx.google.com":
                    auxby.append(linea[i+1].replace("[","").replace("]",""))
    valores = auxfrom
    while len(valores) > 0:
        regex = getRegexId(valores)
        valores = getRegexMSGID(regex, valores)
        regexes.append(regex)
    valores = auxby
    while len(valores) > 0:
        regex = getRegexId(valores)
        valores = getRegexMSGID(regex, valores)
        regexes.append(regex)
    stringa = ""
    for a in list(dict.fromkeys(regexes)):
        stringa += a + separador
    stringab = stringa[:-3]
    regexprimer = stringab
    return regexprimer


def AuthCantidad(FROMM):
    query = f"SELECT AuthenticationResult FROM Validator.Coleccion WHERE FROMM = \"{FROMM}\" "
    curs.execute(query)
    resultados = curs.fetchall()
    max = 0
    min = 100
    for line in resultados:
        pattern = "(pass)"
        a = re.findall(pattern, line[0])
        actual = len(a)
        if actual > max:
            max = actual
        if actual < min:
            min = actual
        if min == " ":
            min = 0
    valor = str(max) + separador + str(min)
    return valor


def get_UTC(FROMM):
    query = f"SELECT PrimerReceived FROM Validator.Coleccion WHERE FROMM = \"{FROMM}\" "
    curs.execute(query)
    resultados = curs.fetchall()
    aux = []
    for line in resultados:
        linea = line[0].split(" ")
        del linea[0]
        maximo = len(linea)
        for i ,ele in enumerate(linea):
            pattern = "[\-|\+]\d\d\d\d"
            if re.fullmatch(pattern, ele):
                if i+1 < maximo:
                    pattern = "(\(\w\w\w\))"
                    if re.match(pattern,linea[i+1]):
                        valor = ele + linea[i+1]
                        aux.append(valor)
                else:
                    aux.append(ele)
    valor = ""
    for ele in list(dict.fromkeys(aux)):
        valor += ele + separador
    valor = valor[:-3]
    return valor


def get_Regexes(FROMM):
    regexMessageID = MSGID(FROMM)
    auth = AuthCantidad(FROMM)
    UTC = get_UTC(FROMM)
    primerR = getRegexReceived(FROMM, "PrimerReceived")
    penUlti = getRegexReceived(FROMM, "PenultimoReceived")
    return regexMessageID, auth, UTC, primerR, penUlti


def obtener_Valores(correos):
    tmsgid = 0
    tprimero = 0
    tpen = 0
    tutc = 0
    tauth = 0
    for i, ele in enumerate(correos[0]):
        if i == 0:
            rgexesMSGID = ele.split(separador)
            qry = f"SELECT MSGID FROM Coleccion WHERE Fromm = \"{line[0]}\""
            CURSSS.execute(qry)
            valoresMSGID = CURSSS.fetchall()
            for elemento in valoresMSGID:
                for regex in rgexesMSGID:
                    if re.match(regex, elemento[0].replace("[","").replace("]","")):
                        tmsgid += 1
                        break
        elif i == 2:
            primero = ele.split(separador)
            qry = f"SELECT PrimerReceived FROM Coleccion WHERE Fromm = \"{line[0]}\""
            CURSSS.execute(qry)
            valoresPrimero = CURSSS.fetchall()
            for elemento in valoresPrimero:
                for regex in primero:
                    if re.findall(regex, elemento[0]):
                        tprimero += 1
                        break
        elif i == 3:
            if ele != "":
                pen = ele.split(separador)
                qry = f"SELECT PenultimoReceived FROM Coleccion WHERE Fromm = \"{line[0]}\""
                CURSSS.execute(qry)
                valoresPrimero = CURSSS.fetchall()
                for elemento in valoresPrimero:
                    if elemento[0] is not None:
                        for regex in pen:
                            if re.findall(regex, elemento[0]):
                                tpen += 1
                                break
                    else:
                        tpen += 1
            else:
                tpen = tprimero
        elif i == 4:
            if ele != "":
                utc = ele.split(separador)
                qry = f"SELECT AuthenticationResult FROM Coleccion WHERE Fromm = \"{line[0]}\""
                CURSSS.execute(qry)
                valoresAUTH = CURSSS.fetchall()
                for elemento in valoresAUTH:
                    pattern = "([\-|\+]\d\d\d\d|(\(\w\w\w\)))"
                    if re.findall(pattern, elemento[0]):
                        for regex in utc:
                            try:
                                regex = "[" + regex + "]"
                                if re.findall(regex, elemento[0]):
                                    tutc += 1
                                    break
                            except:
                                regex = "(" + regex + ")"
                                if re.findall(regex, elemento[0]):
                                    tutc += 1
                                    break
                    else:
                        tutc += 1
            else:
                tutc += tpen
        elif i == 5:
            auth = ele.split(separador)
            qry = f"SELECT AuthenticationResult FROM Coleccion WHERE Fromm = \"{line[0]}\""
            CURSSS.execute(qry)
            valoresAUTH = CURSSS.fetchall()
            for elemento in valoresAUTH:
                maxi = int(auth[0])
                mini = int(auth[1])
                pattern = "(pass)"
                a = re.findall(pattern, elemento[0])
                if int(len(a)) in range(mini, maxi + 1):
                    tauth += 1
    if tmsgid == tprimero == tpen == tutc == tauth:
        print("DELETEADO")
        qquery = f"DELETE FROM Coleccion WHERE Fromm = \"{line[0]}\""
        CURSSS.execute(qquery)
        CNXXX.commit()

    return tmsgid, tprimero, tpen, tutc, tauth


cnx, curs = ConectarBaseDeDatos()
CNXXX, CURSSS = ConectarBaseDeDatos()
query = f"SELECT DISTINCT FROMM FROM Validator.Coleccion WHERE FROMM IN (SELECT DISTINCT FROMM FROM Validator.Coleccion) "
#query = f"SELECT FROMM FROM Validator.Coleccion WHERE FROMM = \"contactos@bancoedwards.cl\""
curs.execute(query)
resultados = curs.fetchall()
CNXX, CURSS = InsertBD()
maxlen = 0
for i, line in enumerate(resultados):
    valores = []
    FROMM = line[0]
    qry = f"SELECT * FROM Validator.Correo WHERE Fromm = \"{FROMM}\""
    CURSSS.execute(qry)
    correos = CURSSS.fetchall()
    print(FROMM)
    if correos:
        tmsgid, tprimero, tpen, tutc, tauth = obtener_Valores(correos)
        if not tmsgid == tprimero == tpen == tutc == tauth:
            maxi = max(tmsgid, tprimero, tpen, tutc, tauth)
            print(maxi)
            print(str(tmsgid) + "       " + str(tprimero) + "       " + str(tpen) + "       " + str(tutc) + "       " + str(tauth))
            print("NO DELETEADO")
            if maxi != tmsgid:
                qry = f"SELECT RegexID FROM Correo WHERE Fromm = \"{FROMM}\""
                curs.execute(qry)
                msgidBD = curs.fetchall()
                msgidBD = msgidBD[0][0].split(separador)
                regexmsgid = MSGID(FROMM).split(separador)
                aux = ""
                for ele in regexmsgid:
                    msgidBD.append(ele)
                for ele in list(dict.fromkeys(msgidBD)):
                    aux += ele + separador
                msgidBD = aux[:-3]
                query = f"UPDATE Correo SET RegexID = \"{msgidBD}\" WHERE FROMM = \"{FROMM}\""
                curs.execute(query)
                cnx.commit()
            if maxi != tprimero:
                qry = f"SELECT Primero FROM Correo WHERE Fromm = \"{FROMM}\""
                curs.execute(qry)
                primerReceivedBD = curs.fetchall()
                primerReceivedBD = primerReceivedBD[0][0].split(separador)
                regexprimer = getRegexReceived(FROMM, "PrimerReceived").split(separador)
                aux = ""
                for ele in regexprimer:
                    primerReceivedBD.append(ele)
                for ele in list(dict.fromkeys(primerReceivedBD)):
                    aux += ele + separador
                primerReceivedBD = aux[:-3]
                query = f"UPDATE Correo SET Primero = \"{primerReceivedBD}\" WHERE FROMM = \"{FROMM}\""
                curs.execute(query)
                cnx.commit()
            if maxi != tpen:
                qry = f"SELECT Penultimo FROM Correo WHERE Fromm = \"{FROMM}\""
                curs.execute(qry)
                penultimoReceivedBD = curs.fetchall()
                if not penultimoReceivedBD[0][0] == "":
                    penultimoReceivedBD = penultimoReceivedBD[0][0].split(separador)
                    regexpen = getRegexReceived(FROMM, "PenultimoReceived").split(separador)
                    aux = ""
                    for ele in regexpen:
                        penultimoReceivedBD.append(ele)
                    for ele in list(dict.fromkeys(penultimoReceivedBD)):
                        aux = ele + separador
                    penultimoReceivedBD = aux[:-3]
                    query = f"UPDATE Correo SET Penultimo = \"{penultimoReceivedBD}\" WHERE FROMM = \"{FROMM}\""
                    curs.execute(query)
                    cnx.commit()
            if maxi != tutc:
                qry = f"SELECT UTC FROM Correo WHERE Fromm = \"{FROMM}\""
                curs.execute(qry)
                utcBD = curs.fetchall()
                if not utcBD[0][0] == "":
                    utcBD = utcBD[0][0].split(separador)
                    regexutcBD =get_UTC(FROMM).split(separador)
                    aux = ""
                    for ele in regexutcBD:
                        utcBD.append(ele)
                    for ele in list(dict.fromkeys(utcBD)):
                        aux = ele + separador
                    utcBD = aux[:-3]
                    query = f"UPDATE Correo SET UTC = \"{utcBD}\" WHERE FROMM = \"{FROMM}\""
                    curs.execute(query)
                    cnx.commit()
            if maxi != tauth:
                qry = f"SELECT AUTH FROM Correo WHERE Fromm = \"{FROMM}\""
                curs.execute(qry)
                authBD = curs.fetchall()
                authBD = authBD[0][0].split(separador)
                auth = AuthCantidad(FROMM)
                auth = auth.split(separador)
                aux = ""
                if int(auth[0]) >= int(authBD[0]):
                    authBD[0] = auth[0]
                if authBD[1] != " ":
                    if int(auth[1]) <= int(authBD[1]):
                        authBD[1]= auth[1]
                else:
                    authBD[1] = str(0)
                for ele in authBD:
                    aux += ele + separador
                authBD = aux[:-3]
                query = f"UPDATE Correo SET AUTH = \"{authBD}\" WHERE FROMM = \"{FROMM}\""
                curs.execute(query)
                cnx.commit()



    else:
        regexMessageID, auth, UTC, primerR, penUlti = get_Regexes(FROMM)
        try:
            query = f"INSERT INTO Validator.Correo (RegexID, Fromm, Primero, Penultimo, UTC, AUTH) VALUES ( %s, %s, %s, %s, %s, %s) "
            values = (regexMessageID,FROMM, primerR, penUlti, UTC, auth)
            CURSS.execute(query, values)
            CNXX.commit()
            print("NUEVA DIRECCION DE CORREO AGREGADA")
        except mysql.connector.Error as error:
            print(error)