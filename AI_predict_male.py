import pymysql.cursors
import time
import tcp

conn = pymysql.connect(
        host="101.101.217.206",
        port=3306,
        user="trendup",
        passwd="2020",
        database="dbtrendup",
        charset='utf8'
    )

curs=conn.cursor()
query5 = "delete from MLpredict_male;"
curs.execute(query5)


def ml_predict_male(lst):
        query1 = "select * from MLpredict_list_male;"
        curs.execute(query1)
        MLpredict_list=curs.fetchall()
        for i in MLpredict_list:
                keyword=i[0]
                sql2 = "select * from "+keyword+"_MLaccuracy"
                query2 = str(sql2)
                curs.execute(query2)
                accuracy=curs.fetchall()

                KNN=0
                SVM=0
                for j in accuracy:
                        KNN=KNN+j[0]
                        SVM=SVM+j[1]
                
                ############### SVM 과 KNN 알고리즘 정확도 비교 및 높은 값 선택
                x=0
                if KNN>SVM:
                        x=0
                if SVM<KNN:
                        x=1

                sql3 = "select * from " + keyword + "_MLpredict"
                query3 = str(sql3)
                curs.execute(query3)
                predict = curs.fetchall()

                month=int(time.strftime('%m', time.localtime(time.time())))
                day=int(time.strftime('%d', time.localtime(time.time())))

                date=month*30+day
                order=round(date/2.34)
                
                ################ database 테이블에 결과 저장
                if predict[order][x]==1:
                        if x==0:
                                value4 = (keyword,KNN/4)
                                query4 = "insert into MLpredict_male (word,accuracy,date_) values (%s,%s,cast(now() as char));"
                                curs.execute(query4, value4)
                        if x==1:
                                value4 = (keyword,SVM/4)
                                query4 = "insert into MLpredict_male (word,accuracy,date_) values (%s,%s,cast(now() as char));"
                                curs.execute(query4,value4)
        return 0

staff_socket = tcp.staff_ready(5010)
tcp.staff_update(ml_predict_male, [], staff_socket)
conn.commit()
conn.close()
