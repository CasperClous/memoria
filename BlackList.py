import re
import asyncio
import websockets
import mysql.connector
from mysql.connector import errorcode


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
    fromm = await websocket.recv()
    fromm = fromm.split("<")
    if len(fromm) > 1:
            fromm = fromm[1].replace(">", "")
    else:
            fromm = fromm[0].replace(">", "")
    query = f"SELECT cantidad FROM blacklist WHERE FROMM = \"{fromm}\""
    curs.execute(query)
    cantidad = curs.fetchall()
    if cantidad:
        cantidad = int(cantidad[0][0]) + 1
        cantidad = str(cantidad)
        query = f"UPDATE Validator.blacklist SET cantidad = {cantidad} WHERE FROMM = \"{fromm}\""
        curs.execute(query)
        cnx.commit()
    else:
        query = f"INSERT INTO Validator.blacklist (FROMM, cantidad) VALUES ( %s, %s) "
        values = (fromm, "1")
        curs.execute(query, values)
        cnx.commit()



start_server = websockets.serve(BackEnd, "", 10002)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
