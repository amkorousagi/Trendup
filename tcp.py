# -*-coding:utf-8-*-
# Inter-Container-Communication module

# check ACG, ufw, container port forwarding, EXPOSE ...
# we identify container by port number, so must use proper port num
# macro

import socket
import time
from _thread import *

MASTER_PUBLIC_IP = "49.50.164.37"
MASTER_PRIVATE_IP = "10.36.7.36" #this may not work , please find your private ip by "hostname -I" command
STAFF_IP = "0.0.0.0"
MASTER_PORT = 5001
YOUTUBE_DATA_PORT = 5002
WEB_CRAWLING_PORT = 5003
GRAPH_DRAWING_PORT = 5004
MACHINE_LEARNING_PORT = 5005
MAX_PORT_NUM = 5005

SOCKET_AMOUNT = 2
sockets = []
FLAG_YOUTUBE_DATA = False
FLAG_WEB_CRAWLING = False
FLAG_GRAPH_DRAWING = False
FLAG_MACHINE_LEARNING = False
STATE = "none"


def youtube_data(staff_socket):
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_YOUTUBE_DATA:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("youtube success")
                else:
                    print("youtube" + data.decode())
            else:
                print("youtube" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("youtube success")
                else:
                    print("youtube" + data.decode())
            else:
                print("youtube" + data.decode())
        else:
            print("wrong state")
    print()


def web_crawling(staff_socket):
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_WEB_CRAWLING:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("web crawling success")
                else:
                    print("web crawling" + data.decode())
            else:
                print("web crawling" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("web crawling success")
                else:
                    print("web crawling" + data.decode())
            else:
                print("web crawling" + data.decode())
        else:
            print("wrong state")
    print()


def graph_drawing(staff_socket):
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_GRAPH_DRAWING:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("graph drawing success")
                else:
                    print("graph drawing" + data.decode())
            else:
                print("graph drawing" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("graph drawing success")
                else:
                    print("graph drawing" + data.decode())
            else:
                print("graph drawing" + data.decode())
        else:
            print("wrong state")
    print()


def machine_learning(staff_socket):
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_MACHINE_LEARNING:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("machine learning success")
                else:
                    print("machine learning" + data.decode())
            else:
                print("machine learning" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("machine learning success")
                else:
                    print("machine learning" + data.decode())
            else:
                print("machine learning" + data.decode())
        else:
            print("wrong state")
    print()


def threaded(staff_socket, addr):
    print('Connected by :', addr[0], ':', addr[1])

    if int(addr[1]) == 5002:
        youtube_data(staff_socket)
    elif int(addr[1]) == 5003:
        web_crawling(staff_socket)
    elif int(addr[1]) == 5004:
        graph_drawing(staff_socket)
    elif int(addr[1]) == 5005:
        machine_learning(staff_socket)


def master_ready():
    master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    master_socket.bind((MASTER_PRIVATE_IP, MASTER_PORT))
    master_socket.listen()

    while len(sockets) < SOCKET_AMOUNT:
        staff_socket, addr = master_socket.accept()
        sockets.append(staff_socket)
        start_new_thread(threaded, (staff_socket, addr))

    print("all container connected.")


def staff_ready(role_port_num):
    if role_port_num <= 5000 or role_port_num > MAX_PORT_NUM:
        print("wrong port num")
        return

    staff_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    staff_socket.bind((STAFF_IP, role_port_num))
    staff_socket.connect((MASTER_PUBLIC_IP, MASTER_PORT))

    return staff_socket


def master_init():
    global STATE
    STATE = "init"
    global FLAG_YOUTUBE_DATA
    FLAG_YOUTUBE_DATA = True
    global FLAG_WEB_CRAWLING
    FLAG_WEB_CRAWLING = True

    while True:
        time.sleep(0.5)
        if not (FLAG_WEB_CRAWLING or FLAG_YOUTUBE_DATA):
            break

    global FLAG_GRAPH_DRAWING
    global FLAG_MACHINE_LEARNING
    FLAG_GRAPH_DRAWING = True
    FLAG_MACHINE_LEARNING = True

    while True:
        time.sleep(0.5)
        if not (FLAG_GRAPH_DRAWING or FLAG_MACHINE_LEARNING):
            break

    print("initialization is finished")


def staff_init(func, argv_list, staff_socket):
    data = staff_socket.recv(1024)
    if data.decode() == "init":
        staff_socket.send("start init".encode())
        res = func(argv_list)
        if res == 0:
            staff_socket.send("success".encode())
        else:
            staff_socket.send(("fail %d" % res).encode())
    else:
        staff_socket.send("wrong command".encode())
    print()


def master_update():
    global STATE
    STATE = "update"
    global FLAG_YOUTUBE_DATA
    FLAG_YOUTUBE_DATA = True
    global FLAG_WEB_CRAWLING
    FLAG_WEB_CRAWLING = True

    while True:
        time.sleep(0.5)
        if not (FLAG_WEB_CRAWLING or FLAG_YOUTUBE_DATA):
            break

    global FLAG_GRAPH_DRAWING
    global FLAG_MACHINE_LEARNING
    FLAG_GRAPH_DRAWING = True
    FLAG_MACHINE_LEARNING = True

    while True:
        time.sleep(0.5)
        if not (FLAG_GRAPH_DRAWING or FLAG_MACHINE_LEARNING):
            break

    print("update is finished")


def staff_update(func, argv_list, staff_socket):
    data = staff_socket.recv(1024)
    if data.decode() == "update":
        staff_socket.send("start update".encode())
        res = func(argv_list)
        if res == 0:
            staff_socket.send("success".encode())
        else:
            staff_socket.send(("fail %d" % res).encode())
    else:
        staff_socket.send("wrong command".encode())
    print()


