import requests
import pymysql.cursors

from bs4 import BeautifulSoup

def switch_site(x):
    return {
        0:'187069',
        1:'186764'
    }.get(x,-1)

def swithch_gender(x):
    return {
        0:'남성',
        1:'여성'
    }.get(x,-1)

def counter(input_list):
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

def c_shopping():
    for i in gender:

        url ="https://www.coupang.com/np/categories/"+switch_site(i)

        custom_header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        req = requests.get(url, headers=custom_header)

        html = BeautifulSoup(req.text, "html.parser")

        items = html.select("div.name")

        allword = []
        keyword = []

        for item in items:
            allword.append(item.text.strip())

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
        #상위 30개만 추출
        for j in range(0,30):
            keyword2.append(word_count[j])

        k=1
        for j in keyword2:
            gender_=swithch_gender(i)
            values1=(str(k),j[0],str(swithch_gender(i)),str(j[1]))
            query1="insert into c_shopping (rank,keyword,date_,gender,score) values(%s,%s,cast(now() as char),%s,%s)"
            curs.execute(query1,values1)
            k=k+1

conn.commit()
conn.close()
