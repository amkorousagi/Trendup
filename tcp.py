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

YOUTUBE_DATA_PORT = 5002
YOUTUBE_MAP_PORT = 5003

N_SHOPPING_PORT = 5004
C_SHOPPING_PORT = 5005
_11_STREET_PORT = 5006
KEYWORD_RANK_PORT = 5007

ML_MALE_PORT = 5008
ML_FEMALE_PORT = 5009
ML_PREDICT_MALE_PORT = 5010
ML_PREDICT_FEMALE_PORT = 5011


MAX_PORT_NUM = 5011

SOCKET_AMOUNT = 10
sockets = []

FLAG_YOUTUBE_THREAD = False
FLAG_YOUTUBE_DATA = False
FLAG_YOUTUBE_MAP = False

FLAG_WEB_CRAWLING_THREAD = False
FLAG_N_SHOPPING = False
FLAG_C_SHOPPING = False
FLAG_11_STREET = False
FLAG_KEYWORD_RANK = False

FLAG_ML_THREAD = False
FLAG_ML_MALE = False
FLAG_ML_FEMALE = False
FLAG_ML_PREDICT_MALE = False
FLAG_ML_PREDICT_FEMALE = False

STATE = "none"

def youtube_thread():
    global FLAG_YOUTUBE_THREAD
    
    while True:
        while True:
            time.sleep(0.5)
            if FLAG_YOUTUBE_THREAD:
                break

        global FLAG_YOUTUBE_DATA
        FLAG_YOUTUBE_DATA = True

        while True:
            time.sleep(0.5)
            if not (FLAG_YOUTUBE_DATA):
                break
        print("youtube_data is finished")
        global FLAG_YOUTUBE_MAP
        FLAG_YOUTUBE_MAP = True

        while True:
            time.sleep(0.5)
            if not (FLAG_YOUTUBE_MAP):
                break
        print("youtube map is finished")
        FLAG_YOUTUBE_THREAD = False

def youtube_data(staff_socket):
    global FLAG_YOUTUBE_DATA
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
                    print("youtube data success")
                else:
                    print("youtube data" + data.decode())
            else:
                print("youtube data" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("youtube data success")
                else:
                    print("youtube data" + data.decode())
            else:
                print("youtube data" + data.decode())
        else:
            print("wrong state")

        FLAG_YOUTUBE_DATA = False


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
                    print("youtube map success")
                else:
                    print("youtube map" + data.decode())
            else:
                print("youtube map" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("youtube map success")
                else:
                    print("youtube map" + data.decode())
            else:
                print("youtube map" + data.decode())
        else:
            print("wrong state")

        FLAG_YOUTUBE_MAP = False



def n_shopping(staff_socket):
    global FLAG_N_SHOPPING
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_N_SHOPPING:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("n_shopping success")
                else:
                    print("n_shopping" + data.decode())
            else:
                print("n_shopping" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("n_shopping success")
                else:
                    print("n_shopping" + data.decode())
            else:
                print("n_shopping" + data.decode())
        else:
            print("wrong state")

        FLAG_N_SHOPPING = False

def c_shopping(staff_socket):
    global FLAG_C_SHOPPING
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_C_SHOPPING:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("c_shopping success")
                else:
                    print("c_shopping" + data.decode())
            else:
                print("c_shopping" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("c_shopping success")
                else:
                    print("c_shopping" + data.decode())
            else:
                print("c_shopping" + data.decode())
        else:
            print("wrong state")

        FLAG_C_SHOPPING = False


def _11_street(staff_socket):
    global FLAG_11_STREET
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_11_STREET:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("11_street success")
                else:
                    print("11_street" + data.decode())
            else:
                print("11_street" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("11_street success")
                else:
                    print("11_street" + data.decode())
            else:
                print("11_street" + data.decode())
        else:
            print("wrong state")

        FLAG_11_STREET = False


def keyword_rank(staff_socket):
    global FLAG_KEYWORD_RANK
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_KEYWORD_RANK:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("keyword_rank success")
                else:
                    print("keyword_rank" + data.decode())
            else:
                print("keyword_rank" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("keyword_rank success")
                else:
                    print("keyword_rank" + data.decode())
            else:
                print("keyword_rank" + data.decode())
        else:
            print("wrong state")

        FLAG_KEYWORD_RANK = False


def webcrawling_thread():

    global FLAG_WEB_CRAWLING_THREAD


    while True:
        while True:
            time.sleep(0.5)
            if FLAG_WEB_CRAWLING_THREAD:
                break

        global FLAG_N_SHOPPING
        FLAG_N_SHOPPING = True
        global FLAG_C_SHOPPING
        FLAG_C_SHOPPING = True
        global FLAG_11_STREET
        FLAG_11_STREET = True

        while True:
            time.sleep(0.5)
            if not (FLAG_N_SHOPPING or FLAG_C_SHOPPING or FLAG_11_STREET):
                break
        print("webcrawling is finished")
        global FLAG_KEYWORD_RANK
        FLAG_KEYWORD_RANK = True

        while True:
            time.sleep(0.5)
            if not (FLAG_KEYWORD_RANK):
                break
        print("keyword rank is finished")
        FLAG_WEB_CRAWLING_THREAD = False



def ml_male(staff_socket):
    global FLAG_ML_MALE
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_ML_MALE:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("ml_male success")
                else:
                    print("ml_male" + data.decode())
            else:
                print("ml_male" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("ml_male success")
                else:
                    print("ml_male" + data.decode())
            else:
                print("ml_male" + data.decode())
        else:
            print("wrong state")

        FLAG_ML_MALE = False


def ml_female(staff_socket):
    global FLAG_ML_FEMALE
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_ML_FEMALE:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("ml_female success")
                else:
                    print("ml_female" + data.decode())
            else:
                print("ml_female" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("ml_female success")
                else:
                    print("ml_female" + data.decode())
            else:
                print("ml_female" + data.decode())
        else:
            print("wrong state")

        FLAG_ML_FEMALE = False



def ml_predict_male(staff_socket):
    global FLAG_ML_PREDICT_MALE
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_ML_PREDICT_MALE:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("ml_predict_male success")
                else:
                    print("ml_predict_male" + data.decode())
            else:
                print("ml_predict_male" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("ml_predict_male success")
                else:
                    print("ml_predict_male" + data.decode())
            else:
                print("ml_predict_male" + data.decode())
        else:
            print("wrong state")

        FLAG_ML_PREDICT_MALE = False


def ml_predict_female(staff_socket):
    global FLAG_ML_PREDICT_FEMALE
    while True:

        while True:
            time.sleep(0.5)
            if FLAG_ML_PREDICT_FEMALE:
                break
        if STATE == "init":
            staff_socket.send("init".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start init":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("ml_predict_female success")
                else:
                    print("ml_predict_female" + data.decode())
            else:
                print("ml_predict_female" + data.decode())
        elif STATE == "update":
            staff_socket.send("update".encode())
            data = staff_socket.recv(1024)
            if data.decode() == "start update":
                data = staff_socket.recv(1024)
                if data.decode() == "success":
                    print("ml_predict_female success")
                else:
                    print("ml_predict_female" + data.decode())
            else:
                print("ml_predict_female" + data.decode())
        else:
            print("wrong state")

        FLAG_ML_PREDICT_FEMALE = False


def ml_thread():

    global FLAG_ML_THREAD

    while True:
        while True:
            time.sleep(0.5)
            if FLAG_ML_THREAD:
                break


        global FLAG_ML_MALE
        FLAG_ML_MALE = True
        global FLAG_ML_FEMALE
        FLAG_ML_FEMALE = True
        
        while True:
            time.sleep(0.5)
            if not (FLAG_ML_MALE or FLAG_ML_FEMALE):
                break
        print("ml is finished")

        global FLAG_ML_PREDICT_MALE
        FLAG_ML_PREDICT_MALE = True
        global FLAG_ML_PREDICT_FEMALE
        FLAG_ML_PREDICT_FEMALE = True

        while True:
            time.sleep(0.5)
            if not (FLAG_ML_PREDICT_MALE or FLAG_ML_PREDICT_FEMALE):
                break
        print("ml_predict is finished")

        FLAG_ML_THREAD = False




def threaded(staff_socket, address):
    print('Connected by :', address[0], ':', address[1])

    if int(address[1]) == 5002:
        youtube_data(staff_socket)
    elif int(address[1]) == 5003:
        youtube_map(staff_socket)
    elif int(address[1]) == 5004:
        n_shopping(staff_socket)
    elif int(address[1]) == 5005:
        c_shopping(staff_socket)
    elif int(address[1]) == 5006:
        _11_street(staff_socket)
    elif int(address[1]) == 5007:
        keyword_rank(staff_socket)
    elif int(address[1]) == 5008:
        ml_male(staff_socket)
    elif int(address[1]) == 5009:
        ml_female(staff_socket)
    elif int(address[1]) == 5010:
        ml_predict_male(staff_socket)
    elif int(address[1]) == 5011:
        ml_predict_female(staff_socket)


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
    
    start_new_thread(youtube_thread, ())
    start_new_thread(webcrawling_thread, ())
    start_new_thread(ml_thread, ())

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

    global FLAG_YOUTUBE_THREAD
    FLAG_YOUTUBE_THREAD = True
    global FLAG_WEB_CRAWLING_THREAD
    FLAG_WEB_CRAWLING_THREAD = True

    while True:
        time.sleep(0.5)
        if not (FLAG_YOUTUBE_THREAD or FLAG_WEB_CRAWLING_THREAD):
            break
    print("data collecting is finished")
    global FLAG_ML_THREAD
    FLAG_ML_THREAD = True

    while True:
        time.sleep(0.5)
        if not (FLAG_ML_THREAD):
            break
    print("data ml is finished")

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

    global FLAG_YOUTUBE_THREAD
    FLAG_YOUTUBE_THREAD = True
    global FLAG_WEB_CRAWLING_THREAD
    FLAG_WEB_CRAWLING_THREAD = True

    while True:
        time.sleep(0.5)
        if not (FLAG_YOUTUBE_THREAD or FLAG_WEB_CRAWLING_THREAD):
            break
    print("data collecting is finished")
    global FLAG_ML_THREAD
    FLAG_ML_THREAD = True

    while True:
        time.sleep(0.5)
        if not (FLAG_ML_THREAD):
            break
    print("data ml is finished")

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


