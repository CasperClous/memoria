import re
import asyncio
import websockets
import mysql.connector
from mysql.connector import errorcode



def ConectarBaseDeDatos():
    cnx = ""
    curs = ""
    try:
        cnx = mysql.connector.connect(user='pluggin', password='PluginV@lidator2021', host='192.168.100.86',
                                      database='Validator')
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


def get_cantidadBlackList(fromm, curs):
    query = f"SELECT cantidad FROM blacklist WHERE FROMM = \"{fromm}\""
    curs.execute(query)
    cantidad = curs.fetchall()
    if cantidad:
        return int(cantidad)
    else:
        return 0


async def BackEnd(websocket, path):
    separador = " # "
    cnx, curs = ConectarBaseDeDatos()
    score = 0
    primerreceived = await websocket.recv()
    penreceived = await websocket.recv()
    fromm = await websocket.recv()
    msgid = await websocket.recv()
    auth = await websocket.recv()
    fromm = fromm.split("<")
    if len(fromm) > 1:
        fromm = fromm[1].replace(">", "")
    else:
        fromm =fromm[0].replace(">", "")
    msgid = msgid.replace("<", "").replace(">", "")
    query = f"SELECT * FROM Correo WHERE FROMM = \"{fromm}\""
    curs.execute(query)
    res = curs.fetchall()
    cantidad = get_cantidadBlackList(fromm, curs)
    if res and cantidad < 5:
        if primerreceived != penreceived:
            for i,line in enumerate(res[0]):
                if i == 0:
                    msgidsbd = res[0][i].split(separador)
                    for msgidbd in msgidsbd:
                        if re.match(msgidbd, msgid.replace("[","").replace("]","")):
                            score += 1
                            print("PASO MSGID")
                            break
                elif i == 2:
                    primerosBD = res[0][i].split(separador)
                    for primeroBD in primerosBD:
                        if re.findall(primeroBD, primerreceived):
                            print("PASO PRIMERRCV")
                            score += 0.75
                            break
                elif i == 3:
                    pensbd = res[0][i].split(separador)
                    for penbd in pensbd:
                        if re.findall(penbd, penreceived):
                            print("PASO PENRECEV")
                            score += 0.75
                            break
                elif i == 4:
                    utcsbd = res[0][i]
                    if utcsbd:
                        utcsbd = res[0][i].split(separador)
                        for utcbd in utcsbd:
                            pattern = "([\-|\+]\d\d\d\d|(\(\w\w\w\)))"
                            if re.findall(pattern, primerreceived):
                                try:
                                    utcbd = "[" + utcbd + "]"
                                    if re.findall(utcbd, primerreceived):
                                        print("PASO UTC")
                                        score += 1
                                        break
                                except:
                                    utcbd = "(" + utcbd + ")"
                                    if re.findall(utcbd, primerreceived):
                                        score += 1
                                        break
                            else:
                                score += 1
                    else:
                        score += 1
                elif i == 5:
                    authsbd = res[0][i].split(separador)
                    maxi = int(authsbd[0])
                    mini = int(authsbd[1])
                    pattern = "(pass)"
                    a = re.findall(pattern, auth)
                    if int(len(a)) in range(mini, maxi+1):
                        print("PASO AUTH")
                        score += 1.5
        elif primerreceived == penreceived:
            for i,line in enumerate(res[0]):
                if i == 0:
                    msgidsbd = res[0][i].split(separador)
                    for msgidbd in msgidsbd:
                        if re.match(msgidbd, msgid.replace("[","").replace("]","")):
                            print("PASO MSGID")
                            score += 1
                            break
                elif i == 2:
                    primerosBD = res[0][i].split(separador)
                    for primeroBD in primerosBD:
                        if re.findall(primeroBD, primerreceived):
                            print("PASO PRIMERRCV")
                            score += 1.5
                            break
                elif i == 4:
                    utcsbd = res[0][i].split(separador)
                    for utcbd in utcsbd:
                        pattern = "([\-|\+]\d\d\d\d|(\(\w\w\w\)))"
                        if re.findall(pattern, primerreceived):
                            try:
                                utcbd = "[" + utcbd + "]"
                                if re.findall(utcbd, primerreceived):
                                    print("PASO UTC")
                                    score += 1
                                    break
                            except:
                                utcbd = "(" + utcbd + ")"
                                if re.findall(utcbd, primerreceived):
                                    score += 1
                                    break
                        else:
                            score += 1
                elif i == 5:
                    authsbd = res[0][i].split(separador)
                    maxi = int(authsbd[0])
                    mini = int(authsbd[1])
                    pattern = "(pass)"
                    a = re.findall(pattern, auth)
                    if int(len(a)) in range(mini, maxi+1):
                        print("PASO AUTH")
                        score += 1.5
    else:
        if cantidad > 4:
            score = 0
        else:
            score = 6
    await websocket.send(str(score-cantidad))






start_server = websockets.serve(BackEnd, "192.168.100.86", 10000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
