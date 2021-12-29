import re
import asyncio
import websockets
import mysql.connector
from mysql.connector import errorcode

def insert1(FROM, primerReceived, penultimoReceived, MSGID, AUTHRESULT, cnx, curs):
    try:
        add_Correo = "INSERT INTO Coleccion (FROMM, PrimerReceived, PenultimoReceived, MSGID, AuthenticationResult) VALUES (%s,%s,%s,%s,%s)"
        val = (FROM, primerReceived, penultimoReceived, MSGID, AUTHRESULT)
        curs.execute(add_Correo, val)
        cnx.commit()
    except mysql.connector.Error as error:
        print(error)


def insert2(FROM, primerReceived, MSGID, AUTHRESULT, cnx, curs):
    try:
        add_Correo = "INSERT INTO Coleccion (FROMM, PrimerReceived, MSGID, AuthenticationResult) VALUES (%s,%s,%s,%s)"
        val = (FROM, primerReceived, MSGID, AUTHRESULT)
        curs.execute(add_Correo, val)
        cnx.commit()
    except mysql.connector.Error as error:
        print(error)

def ConectarBaseDeDatos():
    cnx = ""
    curs = ""
    try:
        cnx = mysql.connector.connect(user='pluggin', password='', host='',
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


async def BackEnd(websocket, path):
    cnx, curs = ConectarBaseDeDatos()
    primerreceived = await websocket.recv()
    penreceived = await websocket.recv()
    fromm = await websocket.recv()
    msgid = await websocket.recv()
    auth = await websocket.recv()
    fromm = fromm.split("<")
    if len(fromm) > 1:
        fromm = fromm[1].replace(">", "")
    else:
        fromm = fromm[0].replace(">", "")
    msgid = msgid.replace("<","").replace(">","")
    if primerreceived == penreceived:
        insert2(fromm, primerreceived, msgid, auth, cnx, curs)
    else:
        insert1(fromm, primerreceived, penreceived, msgid, auth, cnx, curs)


start_server = websockets.serve(BackEnd, "", 10003)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
