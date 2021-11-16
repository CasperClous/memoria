from _thread import *
import mysql.connector
from mysql.connector import errorcode
import socket
global cnx
global curs


def insert1(FROM, primerReceived, penultimoReceived, MSGID, AUTHRESULT):
    ConectarBaseDeDatos()
    try:
        print("Insert1")
        add_Correo = "INSERT INTO Coleccion (FROMM, PrimerReceived, PenultimoReceived, MSGID, AuthenticationResult) VALUES (%s,%s,%s,%s,%s)"
        val = (FROM, primerReceived, penultimoReceived, MSGID, AUTHRESULT)
        curs.execute(add_Correo, val)
        cnx.commit()
        cnx.close()
    except mysql.connector.Error as error:
        print(error)
        cnx.close()


def insert2(FROM, primerReceived, MSGID, AUTHRESULT):
    ConectarBaseDeDatos()
    try:
        print("Insert2")
        add_Correo = "INSERT INTO Coleccion (FROMM, PrimerReceived, MSGID, AuthenticationResult) VALUES (%s,%s,%s,%s)"
        val = (FROM, primerReceived, MSGID, AUTHRESULT)
        curs.execute(add_Correo, val)
        cnx.commit()
        cnx.close()
    except mysql.connector.Error as error:
        print(error)
        cnx.close()


def ConectarBaseDeDatos():
    global cnx
    global curs
    try:
        cnx = mysql.connector.connect(user='addCorreo', password='CorreoV@lidator2021', host='192.168.100.86',
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


def Servidor():
    ServerSideSocket = socket.socket()
    host = '192.168.100.86'
    port = 10001
    ThreadCount = 0
    try:
        ServerSideSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Socket is listening..')
    ServerSideSocket.listen(5)
    while True:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSideSocket.close()


def multi_threaded_client(connection):
    while True:
        datos = connection.recv(2048).decode()
        datos = datos.split(" AE ")
        print(datos)
        if datos[0].strip(" AE ") == "byebye":
            break
        if int(datos[0].strip(" AE ")) == 1:
            FROMM = datos[1].strip(" AE ")
            print(FROMM)
            primerReceived = datos[2].strip(" AE ")
            print(primerReceived)
            penultimoReceived = datos[3].strip(" AE ")
            print(penultimoReceived)
            MSGID = datos[4].strip(" AE ")
            print(MSGID)
            AUTHRESULT = datos[5].strip(" AE ")
            print(AUTHRESULT)
            insert1(FROMM, primerReceived, penultimoReceived, MSGID, AUTHRESULT)
        elif int(datos[0].strip(" AE ")) == 2:
            print(datos)
            FROMM = datos[1].strip(" AE ")
            print(FROMM)
            primerReceived = datos[2].strip(" AE ")
            print(primerReceived)
            MSGID = datos[3].strip(" AE ")
            print(MSGID)
            AUTHRESULT = datos[4].strip(" AE ")
            print(AUTHRESULT)
            insert2(FROMM, primerReceived, MSGID, AUTHRESULT)
        else:
            connection.close()


Servidor()
