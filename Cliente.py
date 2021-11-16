import imaplib
import socket
import string


print("Confirmar que tenga habilitado imap \" https://support.google.com/mail/answer/7126229?hl=es#zippy=%2Cstep-check-that-imap-is-turned-on \" ")
print("Confirmar que tenga habilitado el acceso desde aplicaciones no seguras \" https://support.google.com/accounts/answer/6010255?hl=es#zippy=%2Cif-less-secure-app-access-is-on-for-your-account \" ")
print("El correo y la contraseñas no son almacenadas en ningun lado, tanto de manera local como online")
correo = input("Ingresar Correo Electronico: ")
clave = input("Ingresar Contraseña: ")
host = 'imap.gmail.com'
imap = imaplib.IMAP4_SSL(host)
imap.login(correo, clave)
imap.select('Inbox')

ClientSocket = socket.socket()
host = 'validator-tb.ydns.eu'
port = 10001

print('Waiting for connection')
try:
   ClientSocket.connect((host, port))
except socket.error as e:
   print(str(e))

typ, data = imap.search(None, 'ALL')
for num in data[0].split():
    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
    datito = data[0][1].decode()
    datito = datito.translate({ord(c): None for c in string.whitespace})
    datito = datito[12:].rstrip(">").replace("]", "").replace("[", "").replace("\\","")
    MSGID = str(datito)
    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (FROM)])')
    datito = data[0][1].decode()
    datito = datito[6:].replace("\\", "").replace("'", "").replace("]", "").replace("[", "")
    FROMM = str(datito)
    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (Authentication-Results)])')
    datito = data[0][1].decode()
    AUTHRESULT = str(datito)
    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (RECEIVED)])')
    datito = data[0][1].decode()
    datito = datito.split("Received:")
    if len(datito) > 3:
        primerReceived = "Received:" + str(datito[len(datito) - 1])
        penultimoReceived = "Received:" + str(datito[2])
        FROMM = FROMM.replace("\n", "").replace("\r", "").replace("\"", "")
        primerReceived = primerReceived.replace("\n", "").replace("\r", "").replace("\"", "")
        penultimoReceived = penultimoReceived.replace("\n", "").replace("\r", "").replace("\"", "")
        MSGID = MSGID.replace("\n", "").replace("\r", "").replace("\"", "")
        AUTHRESULT = AUTHRESULT.replace("\n", "").replace("\r", "").replace("\"", "")
        mensaje = "1" + " AE " + FROMM + " AE " + primerReceived + " AE " + penultimoReceived + " AE " + MSGID + " AE " + AUTHRESULT
        ClientSocket.send(mensaje.encode())
    elif len(datito) == 3:
        primerReceived = "Reicived" + str(datito[len(datito) - 1])
        FROMM = FROMM.replace("\n", "").replace("\r", "").replace("\"", "")
        primerReceived = primerReceived.replace("\n", "").replace("\r", "").replace("\"", "")
        MSGID = MSGID.replace("\n", "").replace("\r", "").replace("\"", "")
        AUTHRESULT = AUTHRESULT.replace("\n", "").replace("\r", "").replace("\"", "")
        mensaje = "2" + " AE " + FROMM + " AE " + primerReceived + " AE " + MSGID+ " AE " + AUTHRESULT
        ClientSocket.send(mensaje.encode())
ClientSocket.send(b'byebye')
ClientSocket.close()
imap.close()