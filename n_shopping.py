# -*- coding: utf-8 -*-
import tcp
import requests
import pymysql.cursors

from bs4 import BeautifulSoup

def switch_site(x):
    return {
        0:'50000169',
        1:'50000167'
    }.get(x,-1)

def swithch_gender(x):
    return {
        0:'남성',
        1:'여성'
    }.get(x,-1)
gender={0,1}

conn = pymysql.connect(
        host="101.101.217.206",
        port=3306,
        user="trendup",
        passwd="2020",
        database="dbtrendup",
        charset='utf8'
    )
curs=conn.cursor()

def n_shopping(lst):
    for i in gender:

        url = "https://search.shopping.naver.com/best100v2/detail/kwd.nhn?catId=" + switch_site(i) + "&kwdType=KWD"

        custom_header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        req = requests.get(url, headers=custom_header)

        html = BeautifulSoup(req.text, "html.parser")

        items = html.select("span.txt")

        keyword = []
        for item in items:
            keyword.append(item.text.strip())

        k = 1

        for j in keyword:
            gender_ = swithch_gender(i)
            values1 = (str(k), j, str(swithch_gender(i)))
            query1 = "insert into n_shopping (rank,keyword,date_,gender) values(%s,%s,cast(now() as char),%s)"

            curs.execute(query1, values1)

            k = k + 1
    return 0
            
staff_socket = tcp.staff_ready(5004)
tcp.staff_update(n_shopping, [], staff_socket)
            
conn.commit()
conn.close()

