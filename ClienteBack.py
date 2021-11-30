import mysql.connector
from mysql.connector import errorcode
import socketserver



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
    cnx = ''
    try:
        cnx = mysql.connector.connect(user='addCorreo', password='', host='192.168.100.86', database='Validator')
        curs = cnx.cursor()
        return cnx, curs
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            cnx.close()


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        separador = " ##### "
        cnx, curs = ConectarBaseDeDatos()
        while True:
            datos = self.request.recv(1024).decode()
            datos = datos.split(separador)
            if datos[0].strip(separador) == "byebye":
                break
            if str(datos[0].strip(separador)).isdigit():
                if int(datos[0].strip(separador)) == 1:
                    FROMM = datos[1].strip(separador)
                    primerReceived = datos[2].strip(separador)
                    penultimoReceived = datos[3].strip(separador)
                    MSGID = datos[4].strip(separador)
                    AUTHRESULT = datos[5].strip(separador)
                    insert1(FROMM, primerReceived, penultimoReceived, MSGID, AUTHRESULT, cnx, curs)
                elif int(datos[0].strip(separador)) == 2:
                    FROMM = datos[1].strip(separador)
                    primerReceived = datos[2].strip(separador)
                    MSGID = datos[3].strip(separador)
                    AUTHRESULT = datos[4].strip(separador)
                    insert2(FROMM, primerReceived, MSGID, AUTHRESULT, cnx, curs)
                else:
                    cnx.close()
                    connection.close()

if __name__ == "__main__":
    HOST, PORT = '192.168.100.86', 10001

    # Create the server, binding to localhost on port 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
