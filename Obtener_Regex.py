import mysql.connector
from mysql.connector import errorcode
from genregex import getRegexId
import re
import string
import itertools
import time


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
    for a in regexes:
        stringa += a + ";"
    stringa = stringa[:-1]
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
    stringa = ""
    for a in regexes:
        stringa += a + ";"
    stringaa = stringa[:-1]
    valores = auxby
    while len(valores) > 0:
        regex = getRegexId(valores)
        valores = getRegexMSGID(regex, valores)
        regexes.append(regex)
    stringa = ""
    for a in regexes:
        stringa += a + ";"
    stringab = stringa[:-1]
    regexprimer = stringaa + ";" + stringab
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
    valor = str(max) + ";" + str(min)
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
        valor += ele + ";"
    valor = valor[:-1]
    return valor


cnx, curs = ConectarBaseDeDatos()
query = f"SELECT DISTINCT FROMM FROM Validator.Coleccion WHERE FROMM IN (SELECT DISTINCT FROMM FROM Validator.Coleccion) "
#query = f"SELECT FROMM FROM Validator.Coleccion WHERE FROMM = \"contactos@bancoedwards.cl\""
curs.execute(query)
resultados = curs.fetchall()
CNXX, CURSS = InsertBD()
maxlen = 0
for i, line in enumerate(resultados):
    valores = []
    FROMM = line[0]
    regexMessageID = MSGID(FROMM)
    auth = AuthCantidad(FROMM)
    UTC = get_UTC(FROMM)
    primerR = getRegexReceived(FROMM, "PrimerReceived")
    penUlti = getRegexReceived(FROMM, "PenultimoReceived")
    msgid = len(regexMessageID)
    try:
        query = f"INSERT INTO Validator.Correo (RegexID, Fromm, Primero, Penultimo, UTC, AUTH) VALUES ( %s, %s, %s, %s, %s, %s) "
        values = (regexMessageID,FROMM, primerR, penUlti, UTC, auth)
        CURSS.execute(query, values)
        CNXX.commit()
    except mysql.connector.Error as error:
        print(error)

    perc = i / len(resultados)
    print(perc)
