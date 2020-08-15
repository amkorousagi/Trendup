import pandas as pd
import numpy as np
import pymysql.cursors

conn = pymysql.connect(
        host="101.101.217.206",
        port=3306,
        user="trendup",
        passwd="2020",
        database="dbtrendup",
        charset='utf8'
    )
curs=conn.cursor()

####################################
keyword='남자반바지'
###################################

path="./excel files/%s.csv"%(keyword)
raw_data=pd.read_csv(path, encoding='utf-8')
raw_data_array=np.array(raw_data)

for i in raw_data_array:

    values1 = (i[0],i[1])
    sql1 = "insert into " + keyword + "_RawData (date_,N) values(%s,%s)"
    query1 = str(sql1)


    curs.execute(query1, values1)

conn.commit()
conn.close()
