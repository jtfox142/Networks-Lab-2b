from socket import *
import sys # to use system functions
# create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# code for binding and keeping your socket ready to listen
serverPort = 12001
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

while True:
    print("The server is ready to receive")
    
    connectionSocket, addr = serverSocket.accept()
    
    try:
        # receive message request
        message = connectionSocket.recv(1024).decode()
        #Extract the path of the requested object from the message
        #The path is the second part of the HTTP header, identified by [1]
        filename = message.split()[1]
        #The extracted path of the HTTP requests include character ‘\’, so read
        #the path from the second character
        f = open(filename[1:])
        #store the content of the requested file in a temporary buffer
        outputdata = f.read()

        #Send one HTTP header line into socket 
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        #Send the content of the requested file to the client (connection socket)
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            
        connectionSocket.send("\r\n".encode())

        #close the client connection socket
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        #Close client socket
        connectionSocket.close()
    serverSocket.close()
    sys.exit()