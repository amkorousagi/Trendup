import pymysql.cursors
import tcp

def swithch_gender(x):
    return {
        0:'남성',
        1:'여성'
    }.get(x,-1)

word_count_male = {}
word_count_female = {}

def counter_male(keyword, number):
    if keyword in word_count_male:
        word_count_male[keyword] += number
    else:
        word_count_male[keyword] = number
    return word_count_male

def counter_female(keyword,number):
    if keyword in word_count_female:
        word_count_female[keyword] += number
    else:
        word_count_female[keyword] = number
    return word_count_female


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

def  keyword_rank(lst):
    query3 = "delete from keyword_live_male;"
    curs.execute(query3)
    query4 = "delete from keyword_live_female;"
    curs.execute(query4)


    query1="SELECT keyword, score FROM n_shopping_live;"
    query2="SELECT keyword, score FROM c_shopping_live;"
    query3="SELECT keyword, score FROM _11_shopping_live;"

    curs.execute(query1)
    n_shopping_list=list(curs.fetchall())

    curs.execute(query2)
    c_shopping_list=list(curs.fetchall())

    curs.execute(query3)
    _11_shopping_list=list(curs.fetchall())

    shopping_list=[n_shopping_list,c_shopping_list, _11_shopping_list]

    for i in shopping_list:

        for j in gender:

            for k in range(20):

                if j==0:
                    word_count_male = counter_male(i[k][0], i[k][1])

                if j==1:
                    k=k+20
                    word_count_female = counter_female(i[k][0], i[k][1])



    word_count_male = sorted(word_count_male.items(), key=lambda x: x[1], reverse=True)

    keyword_male=[]
    #상위 20개만 추출
    for i in range(0,20):
        keyword_male.append(word_count_male[i])

    word_count_female = sorted(word_count_female.items(), key=lambda x: x[1], reverse=True)

    keyword_female=[]
    #상위 20개만 추출
    for i in range(0,20):
        keyword_female.append(word_count_female[i])

    rank=1
    for keyword in keyword_male:
        values1 = (str(rank), keyword[0], '남성', keyword[1])
        query1 = "insert into keyword_live_male (rank,keyword,date_,gender,score) values(%s,%s,cast(now() as char),%s,%s)"
        curs.execute(query1, values1)
        rank=rank+1

    rank=1
    for keyword in keyword_female:
        values1 = (str(rank), keyword[0], '여성', keyword[1])
        query1 = "insert into keyword_live_female (rank,keyword,date_,gender,score) values(%s,%s,cast(now() as char),%s,%s)"
        curs.execute(query1, values1)
        rank = rank + 1



staff_socket = tcp.staff_ready(5007)
tcp.staff_update(keyword_rank, [], staff_socket)


conn.commit()
conn.close()
