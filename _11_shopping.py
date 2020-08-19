# -*- coding: utf-8 -*-

import requests
import pymysql.cursors
import tcp

from bs4 import BeautifulSoup

def switch_site(x):
    return {
        0:'1001312',
        1:'1001311'
    }.get(x,-1)

def swithch_gender(x):
    return {
        0:'남성',
        1:'여성'
    }.get(x,-1)

def counter(keyword):
    word_count = {}
    for word in keyword:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

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

def _11_shopping(lst):
    for i in gender:

        url = "http://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain&cornerNo=2&dispCtgrNo="+switch_site(i)

        custom_header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        req = requests.get(url, headers=custom_header)

        html = BeautifulSoup(req.text, "html.parser")

        items = html.select("p")

        allword = []
        keyword = []

        for item in items:
            allword.append(item.text.strip())

        first_one = 0
        for j in range(0, 10):
            allword.remove(allword[first_one])

        split_list = []

        for j in allword:
            r_j = j.replace('[', ' ').replace(']', ' ').replace('/', ' ').replace('(', ' ').replace(')', ' ')
            split_list = r_j.split(" ")
            for k in split_list:
                keyword.append(k)

        keyword = ' '.join(keyword).split()

        word_count = counter(keyword)
        word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

        #keyword 삭제
        banlist = ['남성','남자','여성','여자']

        x=0
        for j in word_count:
            if j[0] in banlist:
                del word_count[x]
                x=x+1
            else:
                x=x+1

        keyword2=[]
        #상위 20개만 추출
        for j in range(0,20):
            keyword2.append(word_count[j])


        k=1
        for j in keyword2:
            gender_=swithch_gender(i)
            values1=(str(k),j[0],str(swithch_gender(i)),str(j[1]))
            query1="insert into _11_shopping (rank,keyword,date_,gender,score) values(%s,%s,cast(now() as char),%s,%s)"

            curs.execute(query1,values1)

            k=k+1
    return 0

staff_socket = tcp.staff_ready(5006)
tcp.staff_update(_11_shopping, [], staff_socket)

conn.commit()
conn.close()
