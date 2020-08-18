# -*-coding:utf-8-*-
# Inter-Container-Communication module

# check ACG, ufw, container port forwarding, EXPOSE ...
# we identify container by port number, so must use proper port num
# macro

import socket
import time
from _thread import *

MASTER_PUBLIC_IP = "49.50.164.37"
MASTER_PRIVATE_IP = "172.17.0.4 " #this may not work , please find your private ip by "hostname -I" command
STAFF_IP = "0.0.0.0"
MASTER_PORT = 5001
YOUTUBE_DATA_PORT1 = 5002
YOUTUBE_DATA_PORT2 = 5003
YOUTUBE_MAP_PORT = 5004
'''
WEB_CRAWLING_PORT = 5003
GRAPH_DRAWING_PORT = 5004
MACHINE_LEARNING_PORT = 5005
'''
MAX_PORT_NUM = 5004

SOCKET_AMOUNT = 3
sockets = []

FLAG_YOUTUBE_DATA1 = False
FLAG_YOUTUBE_DATA2 = False
FLAG_YOUTUBE_MAP = False

'''
FLAG_N_SHOPPING = False
FLAG_G_MARKET = False
FLAG_11_STREET = False
FLAG_KEYWORD_RANK = False
FLAG_MALE_ML = False
FLAG_FEMALE_ML = False
FLAG_MALE_PREDICT = False
FLAG_FEMALE_PREDICT = False
'''
STATE = "none"


def youtube_data1(staff_socket):
    global FLAG_YOUTUBE_DATA1
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_YOUTUBE_DATA1:
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

        FLAG_YOUTUBE_DATA1 = False

def youtube_data2(staff_socket):
    global FLAG_YOUTUBE_DATA2
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_YOUTUBE_DATA2:
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

        FLAG_YOUTUBE_DATA2 = False

def youtube_map(staff_socket):
    global FLAG_YOUTUBE_MAP
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_YOUTUBE_MAP:
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

        FLAG_YOUTUBE_MAP = False


'''
def web_crawling(staff_socket):
    global FLAG_WEB_CRAWLING
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
                    print("1web crawling" + data.decode())
            else:
                print("web crawling" + data.decode())
        else:
            print("wrong state")

        FLAG_WEB_CRAWLING = False


def graph_drawing(staff_socket):
    global FLAG_GRAPH_DRAWING
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

        FLAG_GRAPH_DRAWING = False


def machine_learning(staff_socket):
    global FLAG_MACHINE_LEARNING
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

        FLAG_MACHINE_LEARNING = False

'''
def threaded(staff_socket, address):
    print('Connected by :', address[0], ':', address[1])

    if int(address[1]) == 5002:
        youtube_data1(staff_socket)
    elif int(address[1]) == 5003:
        youtube_data2(staff_socket)
    elif int(address[1]) == 5004:
        youtube_map(staff_socket)
        '''
        web_crawling(staff_socket)
    elif int(address[1]) == 5004:
        graph_drawing(staff_socket)
    elif int(address[1]) == 5005:
        machine_learning(staff_socket)
'''

def master_ready():
    master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    master_socket.bind((MASTER_PRIVATE_IP, MASTER_PORT))
    master_socket.listen()
    i = 0
    while i < SOCKET_AMOUNT:
        staff_socket, address = master_socket.accept()
        i = i + 1
        start_new_thread(threaded, (staff_socket, address))

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
    global FLAG_YOUTUBE_DATA1
    FLAG_YOUTUBE_DATA1 = True
    global FLAG_YOUTUBE_DATA2
    FLAG_YOUTUBE_DATA2 = True

    while True:
        time.sleep(0.5)
        if not (FLAG_YOUTUBE_DATA1 or FLAG_YOUTUBE_DATA2):
            break
    print("both youtube data1 and youtube data2 are finished")
    global FLAG_YOUTUBE_MAP
    FLAG_YOUTUBE_MAP = True

    while True:
        time.sleep(0.5)
        if not (FLAG_YOUTUBE_MAP):
            break
    print("youtube map is finished")

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


def master_update():
    global STATE
    STATE = "update"
    global FLAG_YOUTUBE_DATA1
    FLAG_YOUTUBE_DATA1 = True
    global FLAG_YOUTUBE_DATA2
    FLAG_YOUTUBE_DATA2 = True

    while True:
        time.sleep(0.5)
        if not (FLAG_YOUTUBE_DATA1 or FLAG_YOUTUBE_DATA2):
            break
    print("both youtube data1 and youtube data2 are finished")
    global FLAG_YOUTUBE_MAP
    FLAG_YOUTUBE_MAP = True

    while True:
        time.sleep(0.5)
        if not (FLAG_YOUTUBE_MAP):
            break
    print("youtube map is finished")

    print("update is finished")

def staff_update(func, argv_list, staff_socket):
    data = staff_socket.recv(1024)
    if data.decode() == "update":
        staff_socket.send("start update".encode())
        res = func(argv_list)
        if res == 0:
            staff_socket.send("success".encode())
        else:
            staff_socket.send("fail 0".encode())
    else:
        staff_socket.send("wrong command".encode())


