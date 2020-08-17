import pandas as pd
import numpy as np
import pymysql.cursors
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm,metrics

def rms(x): # RMS 함수 정의
    return np.sqrt(np.mean(x**2))

conn1 = pymysql.connect(
        host="101.101.217.206",
        port=3306,
        user="trendup",
        passwd="2020",
        database="dbtrendup",
        charset='utf8'
    )

conn2 = pymysql.connect(
        host="101.101.217.206",
        port=3306,
        user="trendup",
        passwd="2020",
        database="dbML",
        charset='utf8'
    )
curs1=conn1.cursor()
curs2=conn2.cursor()

query1="select * from keyword_live_male"
curs1.execute(query1)
keyword_male_array1=curs1.fetchall()

keyword_male1=[]
for i in keyword_male_array1:
    keyword_male1.append(i[1])

query2="select * from MLpredict_list_male"
curs1.execute(query2)
keyword_male_array2=curs1.fetchall()

keyword_male2=[]
for i in keyword_male_array2:
    keyword_male2.append(i[0])

keyword=[]
for i in keyword_male1:
    if i not in keyword_male2:
        keyword.append(i)

for word in keyword:
    sql1 = "select * from " + keyword + "_RawData;"
    query1 = str(sql1)
    curs1.execute(query1)
    raw_data = curs1.fetchall()

    NoOfSensor = 1
    NoOfFeature = 5

    raw_data = np.array(raw_data)
    NoOfData = int(raw_data.shape[0])
    Fold = 4
    NoOfFold_Data = int(NoOfData / Fold)

    N_Feature = np.zeros((Fold, NoOfSensor * NoOfFeature))
    raw_data = pd.DataFrame(raw_data)
    for i in range(Fold):
        temp_raw_data = raw_data.iloc[NoOfFold_Data * i: NoOfFold_Data * (i + 1), 1]
        temp_raw_data = np.array(temp_raw_data, dtype=np.float)
        N_Feature[i, 0] = np.max(temp_raw_data)
        N_Feature[i, 1] = np.min(temp_raw_data)
        N_Feature[i, 2] = np.mean(temp_raw_data)
        N_Feature[i, 3] = rms(temp_raw_data)
        N_Feature[i, 4] = np.var(temp_raw_data)

    N_Feature = np.array(N_Feature, dtype=object)
    N_Feature_Data = pd.DataFrame(N_Feature)

    #### 특징 저장
    data_feature_array = np.array(N_Feature_Data)
    for i in data_feature_array:
        values1 = (i[0], i[1], i[2], i[3], i[4])
        sql1 = "insert into " + keyword + "_DataFeature (max,min,mean,rms,var) values(%s,%s,%s,%s,%s)"
        query1 = str(sql1)

        curs1.execute(query1, values1)

    All_Label = np.zeros(NoOfData)
    N_array = np.array(raw_data.iloc[:, 1], dtype=float)

    #### Labeling
    k = 208
    for i in N_array:
        if i > 80:
            All_Label[(k - 3) % 208] = 1

        k = k + 1

    All_Label = pd.Series(All_Label)

    All_Label_forANN = np.zeros((NoOfData, 2))


    k = 0
    for i in N_array:
        if i > 80:
            All_Label_forANN[k, 1] = 1
        else:
            All_Label_forANN[k, 0] = 1

        k = k + 1

    All_Label_forANN = pd.DataFrame(All_Label_forANN)

    NoOfData = int(raw_data.shape[0])
    Fold = 4

    FeatNo = int(raw_data.shape[1] - 1)  # 데이터 특징 수 (=데이터 차원)
    FoldDataNo = int(NoOfData / Fold)  # 1개 Fold 당 (검증)데이터 개수

    date_array = np.zeros((FoldDataNo, 1))

    start_date = 3
    for i in range(FoldDataNo):
        date_array[i] = start_date
        start_date = start_date + 7

    date_array = np.array(date_array)

    ############### sensor data
    # Validation Data set
    for i in range(Fold):
        temp_raw_data = date_array

        s = 'Validation_Fold%d = np.array(temp_raw_data)' % (i + 1)
        exec(s)

    # Training Data set
    for i in range(Fold):
        temp_Train = np.concatenate((date_array, date_array), axis=0)
        temp_Train_Final = np.concatenate((temp_Train, date_array), axis=0)

        s = 'Training_Fold%d  = np.array(temp_Train_Final)' % (i + 1)
        exec(s)

    for i in range(Fold):
        s1 = 'tempA=Training_Fold%d_%s'% (i + 1, keyword)
        exec (s1)
        s2 = 'tempB=Validation_Fold%d_%s' % (i + 1, keyword)
        exec (s2)

        sql1 = 'create table Training_Fold%d_%s(n float(10));' % (i + 1, keyword)
        query1=str(sql1)
        curs2.execute(query1)
        sql2 = 'create table Validation_Fold%d_%s(n float(10));' % (i + 1, keyword)
        query2 = str(sql2)
        curs2.execute(query2)

        for i in tempA:
            sql3 = 'insert into Training_Fold%d_%s (n) values (%s)'% (i + 1, keyword)
            values3 = i[0]
            curs2.execute(sql3,values3)

        for i in tempB:
            sql4 = 'insert into Validation_Fold%d_%s (n) values (%s)' % (i + 1, keyword)
            values4 = i[0]
            curs2.execute(sql4, values4)


    NoOfData = int(raw_data.shape[0])
    Fold = 4
    NoOfFold_Data = int(NoOfData / Fold)

    ###########  Labeling
    # Validation Data set
    for i in range(Fold):
        temp_label = All_Label.iloc[FoldDataNo * i:FoldDataNo * (i + 1)]
        temp_Label_Final = pd.DataFrame(temp_label)

        s = 'ValidationFold_Label%d = temp_Label_Final' % (i + 1)
        exec(s)

    # Training Data set
    for i in range(Fold):
        temp_Train_Front = All_Label.iloc[:FoldDataNo * i]
        temp_Train_Back = All_Label.iloc[FoldDataNo * (i + 1):]
        temp_Train_Total = np.concatenate([temp_Train_Front, temp_Train_Back], axis=0)
        temp_Train_Final = pd.DataFrame(temp_Train_Total)

        s = 'TrainingFold_Label%d = temp_Train_Final' % (i + 1)
        exec(s)

    # Validation Data set
    for i in range(Fold):
        temp_label_forANN = All_Label_forANN.iloc[FoldDataNo * i:FoldDataNo * (i + 1), :]
        temp_Label_Final_forANN = pd.DataFrame(temp_label_forANN)

        s = 'ValidationFold_Label%d_forANN = temp_Label_Final_forANN' % (i + 1)
        exec(s)

    # Training Data set
    for i in range(Fold):
        temp_Train_Front_forANN = All_Label_forANN.iloc[:FoldDataNo * i, :]
        temp_Train_Back_forANN = All_Label_forANN.iloc[FoldDataNo * (i + 1):, :]
        temp_Train_Total_forANN = np.concatenate([temp_Train_Front_forANN, temp_Train_Back_forANN], axis=0)
        temp_Train_Final_forANN = pd.DataFrame(temp_Train_Total_forANN)

        s = 'TrainingFold_Label%d_forANN = temp_Train_Final_forANN' % (i + 1)
        exec(s)

    # for SVM & KNN
    for i in range(Fold):
        path1 = './k-fold/TrainingFold_Label%d_%s' % (i + 1, keyword)
        path2 = './k-fold/ValidationFold_Label%d_%s' % (i + 1, keyword)

        c1 = 'TrainingFold_Label%d.to_csv(path1, header = None, index = None)' % (i + 1)
        c2 = 'ValidationFold_Label%d.to_csv(path2, header = None, index = None)' % (i + 1)
        exec(c1)
        exec(c2)

    # for ANN
    for i in range(Fold):
        path1 = './k-fold/TrainingFold_Label%d_forANN_%s' % (i + 1, keyword)
        path2 = './k-fold/ValidationFold_Label%d_forANN_%s' % (i + 1, keyword)

        c1 = 'TrainingFold_Label%d_forANN.to_csv(  path1, header = None, index = None)' % (i + 1)
        c2 = 'ValidationFold_Label%d.to_csv(path2, header = None, index = None)' % (i + 1)
        exec(c1)
        exec(c2)

conn1.commit()
conn1.close()
conn2.commit()
conn2.close()
