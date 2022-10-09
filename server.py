import threading
import socket

# IF Simple HTTP/1.0 Server
HTTP1 = True

# IF HTTP 1.1
HTTP1_1 = False  # Set to true to check HTTP 1.1 and set HTTP1 to False at that time above
set_connection_time = 0.5  # set http 1.1 connection time if you select above value to true, current set to 5 second

import sys
import datetime

# Arguments of path and port
n = len(sys.argv)
patht = 0
portt = 0
for i in range(0, n):
    if patht == 1:
        path = sys.argv[i]
        if path[-1] != "/":
            path = path + "/"

        patht = 0
    if portt == 1:
        port = int(sys.argv[i])

        portt = 0
    if (sys.argv[i]) == "-document_root":
        patht = 1
    if (sys.argv[i]) == "-port":
        portt = 1



# Define socket port and host
SERVERHOST = 'localhost'
SERVERPORT = port
# Create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((SERVERHOST, SERVERPORT))
serversocket.listen(5)
print('Listening port on %s ...' % SERVERPORT)


def responder(clientconnection, clientaddress):
    import time
    timeout = time.time() + 1
    while time.time() < timeout:
        try:
            request = clientconnection.recv(1024).decode()  # request received from client end

            headers = request.split('\n')
            
            if 'GET' not in headers[0]:
              
                if HTTP1 == True:
                   
                    response = 'HTTP 1.0 400 Bad Request\n\n400 Error caused by an invalid request'   
                    print("HTTP 1.0 400 Bad Request")
                    clientconnection.sendall(response.encode())
                    clientconnection.close()
                    break
                if HTTP1_1 == True:
                    response = 'HTTP 1.1 400 Bad Request\n\n400 Error caused by an invalid request'
                    print("HTTP 1.1 400 Bad Request")
                    clientconnection.sendall(response.encode())
                    clientconnection.close()
                    break

            filename = headers[0].split()[1]  # filename asked for
            if filename.split("/")[-1] == '/' or filename.split("/")[-1] == "" or filename.split("/")[
                -1] == "index.html":
                filename = "/index.html"
            elif filename.split("/")[-1] == "about":
                filename = "/About SJSU _ About.html"
            elif filename.split("/")[-1] == "visit":
                filename = "/Visit.html"
            elif filename.split("/")[-1] == "family-programs":
                filename = "/Parent and Family Programs.html"
            elif filename.split("/")[-1] == "admission":
                filename = "/Admissions.html"
            else:
                pass

            try:
                if filename.split("/")[-1][-4:-1] == ".jp":

                    img = open(path + filename.split("/")[-1], 'rb')  # opening image files # path is root directory
                    content = img.read()  # read file
                    img.close()

                    clientconnection.sendall(content)
                else:
                    fil = open(path + filename.split("/")[-1])  # open regular file
                    content = fil.read()  # read file
                    fil.close()

                    if HTTP1_1 == True:
                        response = 'HTTP/1.1 200 OK ~ ' "Content-Type: text/http ~ " + 'Content-length: ' + str(
                            sys.getsizeof(content)) + '~ ' + 'Date: ' + str(datetime.datetime.now()) + '~\n\n' + content
                    # response has header plus content read from root directory

                    if HTTP1 == True:
                        response = 'HTTP/1.0 200 OK ~ ' "Content-Type: text/http ~ " + 'Content-length: ' + str(
                            sys.getsizeof(content)) + '~ ' + 'Date: ' + str(datetime.datetime.now()) + '~\n\n' + content

                    if HTTP1 == True:
                        print("HTTP 1.0 200" + " " + filename.split("/")[-1])

                    if HTTP1_1 == True:
                        print("HTTP 1.1 200" + " " + filename.split("/")[-1])

                    
                    clientconnection.sendall(response.encode())

            except Exception as e:

                if "Permission" in str(e):
                    if HTTP1_1 == True:
                        response = 'HTTP 1.1 403 File Forbidden\n\n403 Forbidden you do not have permission to access this file'
                    print("HTTP 1.1 403 Forbidden you do not have permission to access this resource" + " " +
                          filename.split("/")[-1])
                    if HTTP1 == True:
                        response = 'HTTP 1.0 403 File Forbidden\n\n403 Forbidden you do not have permission to access this file'
                    print("HTTP 1.0 403 Forbidden you do not have permission to access this resource" + " " +
                          filename.split("/")[-1])

                else:
                    if HTTP1_1 == True:
                        response = 'HTTP 1.1 404 FILE NOT FOUND\n\n404 File Not Found'

                    print("HTTP 1.1 404 File NOT FOUND" + " " + filename.split("/")[-1])
                    if HTTP1 == True:
                        response = 'HTTP 1.0 404 FILE NOT FOUND\n\n404 File Not Found'

                    print("HTTP 1.0 404 File NOT FOUND" + " " + filename.split("/")[-1])
               
                clientconnection.sendall(response.encode())

            if HTTP1 == True:
                clientconnection.close()
                break
            elif HTTP1_1 == True:
                pass
            else:
                clientconnection.close()
                break
        except Exception as e:

            pass


def connection_killer(clientconnection, set_connection_time):
    import time
    time.sleep(set_connection_time)
    clientconnection.close()  # close http 1.1 connection


while True:
    clientconnection, clientaddress = serversocket.accept()  # accepting connection
    threading.Thread(target=responder, args=(clientconnection,
                                             clientaddress,)).start()  # multithreading # responder is the main process to recieve and send requests response common for both http 1 and http 1.1
    if HTTP1_1 == True:
        threading.Thread(target=connection_killer, args=(
        clientconnection, set_connection_time,)).start()  # closing http 1.1 connections after specified time

serversocket.close()
