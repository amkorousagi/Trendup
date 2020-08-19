import pandas as pd
import numpy as np
import pymysql.cursors
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm, metrics


def rms(x):  # RMS 함수 정의
    return np.sqrt(np.mean(x ** 2))


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
curs1 = conn1.cursor()
curs2 = conn2.cursor()

query1 = "select * from keyword_live_male"
curs1.execute(query1)
keyword_female_array1 = curs1.fetchall()

keyword_female1 = []
k=0
for i in keyword_female_array1:
    k = k + 1
    if k ==10:     ##### 상위 10개에 대해서만 특징추출 및 머신러닝
        break
    keyword_female1.append(i[1])

query2 = "select * from MLpredict_list_female"
curs1.execute(query2)
keyword_female_array2 = curs1.fetchall()

keyword_female2 = []
for i in keyword_female_array2:
    keyword_female2.append(i[0])

keyword = []
for i in keyword_female1:
    if i not in keyword_female2:
        keyword.append(i)


### 업데이트된 키워드 rank table에 이전에 머신러닝을 돌리지 않은 
### 키워드가 업데이트 되면 자동 머신러닝

for keyword in keyword:
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

    sql2 = "create table " + keyword + "_DataFeature(max int(200),min int(200),mean int(200),rms int(200),var int(200))"
    query2 = str(sql2)
    curs1.execute(query2)
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
        if i > 80:    ###### 라벨링 조건 - 3주후 키워드 검색수가 80회를 넘는 경우 - 1
            All_Label[(k - 3) % 208] = 1

        k = k + 1


    All_Label[NoOfFold_Data-1] = 1
    All_Label[NoOfFold_Data*2-1] = 1
    All_Label[NoOfFold_Data*3-1] = 1
    All_Label[NoOfFold_Data*4-1] = 1

    All_Label = pd.Series(All_Label)


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
        s1 = 'tempA=Training_Fold%d' % (i + 1)
        exec(s1)
        s2 = 'tempB=Validation_Fold%d' % (i + 1)
        exec(s2)

        sql1 = 'create table Training_Fold%d_%s(n float(10));' % (i + 1, keyword)
        query1 = str(sql1)
        curs2.execute(query1)
        sql2 = 'create table Validation_Fold%d_%s(n float(10));' % (i + 1, keyword)
        query2 = str(sql2)
        curs2.execute(query2)

        for j in tempA:
            sql3 = 'insert into Training_Fold%d_%s (n) values (%s)' % (i + 1, keyword, str(j[0]))
            query3 = str(sql3)
            curs2.execute(query3)

        for j in tempB:
            sql4 = 'insert into Validation_Fold%d_%s (n) values (%s)' % (i + 1, keyword, str(j[0]))
            query4 = str(sql4)
            curs2.execute(query4)

    NoOfData = int(raw_data.shape[0])
    Fold = 4
    NoOfFold_Data = int(NoOfData / Fold)

    ###########  Labeling
    # Validation Data set
    for i in range(Fold):
        temp_label = All_Label.iloc[FoldDataNo * i:FoldDataNo * (i + 1)]
        temp_Label_Final = np.array(temp_label)

        s = 'ValidationFold_Label%d = temp_Label_Final' % (i + 1)
        exec(s)

    # Training Data set
    for i in range(Fold):
        temp_Train_Front = All_Label.iloc[:FoldDataNo * i]
        temp_Train_Back = All_Label.iloc[FoldDataNo * (i + 1):]
        temp_Train_Total = np.concatenate([temp_Train_Front, temp_Train_Back], axis=0)
        temp_Train_Final = np.array(temp_Train_Total)

        s = 'TrainingFold_Label%d = temp_Train_Final' % (i + 1)
        exec(s)


    # for SVM & KNN
    for i in range(Fold):
        s1 = 'tempA=TrainingFold_Label%d' % (i + 1)
        exec(s1)
        s2 = 'tempB=ValidationFold_Label%d' % (i + 1)
        exec(s2)

        sql1 = 'create table TrainingFold_Label%d_%s(n float(10));' % (i + 1, keyword)
        query1 = str(sql1)
        curs2.execute(query1)
        sql2 = 'create table ValidationFold_Label%d_%s(n float(10));' % (i + 1, keyword)
        query2 = str(sql2)
        curs2.execute(query2)

        for j in tempA:
            sql3 = 'insert into TrainingFold_Label%d_%s (n) values (%s)' % (i + 1, keyword, str(j))
            query3 = str(sql3)
            curs2.execute(query3)

        for j in tempB:
            sql4 = 'insert into ValidationFold_Label%d_%s (n) values (%s)' % (i + 1, keyword, str(j))
            query4 = str(sql4)
            curs2.execute(query4)


    temp_Train = np.concatenate((date_array, date_array), axis=0)
    temp_Train_Final = np.concatenate((temp_Train, temp_Train), axis=0)

    Training_All = np.array(temp_Train_Final)
    Training_All_Label1 = np.array(All_Label)
    Training_All_Label = np.array([[0]], dtype=float)
    for i in Training_All_Label1:
        a = np.array([[i]])
        Training_All_Label = np.concatenate((Training_All_Label, a), axis=0)

    Training_All_Label = np.delete(Training_All_Label, 0, 0)


    sql1 = 'create table Training_All_%s(n float(10))' % (keyword)
    query1 = str(sql1)
    curs2.execute(query1)

    sql2 = 'create table Training_All_Label_%s(n float(10))' % (keyword)
    query2 = str(sql2)
    curs2.execute(query2)


    for i in Training_All:
        sql1 = 'insert into Training_All_%s (n) values (%s)' % (keyword, str(i[0]))
        query1 = str(sql1)
        curs2.execute(query1)

    for i in Training_All_Label:
        sql1 = 'insert into Training_All_Label_%s (n) values (%s)' % (keyword, str(i[0]))
        query1 = str(sql1)
        curs2.execute(query1)


    #############################################################################################
    Fold = 4

    date_array = np.array([[0]], dtype=int)
    date_list = np.linspace(0, 365, 156)
    for i in date_list:
        date = round(i)
        date_ = np.array([[date]], dtype=int)
        date_array = np.concatenate((date_array, date_), axis=0)
    date_array = np.delete(date_array, 0, 0)

    # k-fold 학습/검증 데이터
    for i in range(Fold):
        query1 = 'select * from Training_Fold%d_%s' % (i + 1, keyword)
        curs2.execute(query1)
        array1 = curs2.fetchall()
        c1 = 'Training_Fold%d   = np.array(array1)' % (i + 1)
        exec(c1)

        query2 = 'select * from Validation_Fold%d_%s' % (i + 1, keyword)
        curs2.execute(query2)
        array2 = curs2.fetchall()
        c2 = 'Validation_Fold%d = np.array(array2)' % (i + 1)
        exec(c2)

    # K-fold 학습/검증 레이블
    for i in range(Fold):
        query1 = 'select * from TrainingFold_Label%d_%s' % (i + 1, keyword)
        curs2.execute(query1)
        array1 = curs2.fetchall()
        c1 = 'TrainingFold_Label%d   = np.array(array1)' % (i + 1)
        exec(c1)

        query2 = 'select * from ValidationFold_Label%d_%s' % (i + 1, keyword)
        curs2.execute(query2)
        array2 = curs2.fetchall()
        c2 = 'ValidationFold_Label%d = np.array(array2)' % (i + 1)
        exec(c2)


    # 전체 학습용 데이터
    query1 = 'select * from Training_All_%s' % (keyword)
    curs2.execute(query1)
    array1 = curs2.fetchall()
    c1 = 'Training_All = np.array(array1)'
    exec(c1)

    query2 = 'select * from Training_All_Label_%s' % (keyword)
    curs2.execute(query2)
    array2 = curs2.fetchall()
    c2 = 'Training_All_Label = np.array(array2)'
    exec(c2)


    ############   KNN

    for i in range(Fold):
        c1 = 'Training_CurrentFold = Training_Fold%d' % (i + 1)
        exec(c1)
        c2 = 'Validation_CurrentFold = Validation_Fold%d' % (i + 1)
        exec(c2)

        c3 = 'knnModel_CurrentFold = KNeighborsClassifier(n_neighbors = 3).fit(Training_CurrentFold , TrainingFold_Label%d.ravel())' % (
                i + 1)
        exec(c3)
        c4 = 'knnscore_Fold%d = knnModel_CurrentFold.score(Validation_CurrentFold , ValidationFold_Label%d)' % (
            i + 1, i + 1)
        exec(c4)

    KNN_model = KNeighborsClassifier(n_neighbors=3).fit(Training_All, Training_All_Label.ravel())
    KNN_predict = KNN_model.predict(date_array)

    ############   SVM
    for i in range(Fold):
        c1 = 'Training_CurrentFold = Training_Fold%d' % (i + 1)
        exec(c1)
        c2 = 'Validation_CurrentFold = Validation_Fold%d' % (i + 1)
        exec(c2)

        svmModel_CurrentFold = svm.SVC(kernel='rbf')
        c3 = 'svmModel_CurrentFold.fit(Training_CurrentFold , TrainingFold_Label%d.ravel())' % (i + 1)
        exec(c3)
        Predicted = np.array(svmModel_CurrentFold.predict(Validation_CurrentFold))

        c4 = 'svmscore_Fold%d = metrics.accuracy_score(ValidationFold_Label%d , Predicted)' % (i + 1, i + 1)
        exec(c4)

    SVM_model = svm.SVC(kernel='rbf')
    SVM_model.fit(Training_All, Training_All_Label.ravel())
    SVM_predict = SVM_model.predict(date_array)

    #################################################

    sql1 = "create table " + keyword + "_MLaccuracy (KNN float(10),SVM float(10))"
    sql2 = "create table " + keyword + "_MLpredict (KNN float(10),SVM float(10))"
    query1 = str(sql1)
    query2 = str(sql2)
    curs1.execute(query1)
    curs1.execute(query2)

    for i in range(Fold):
        s1 = 'values1=round(knnscore_Fold%d,4)' % (i + 1)
        exec(s1)
        s2 = 'values2=round(svmscore_Fold%d,4)' % (i + 1)
        exec(s2)
        values1 = values1 * 100
        values1 = str(values1)
        values2 = values2 * 100
        values2 = str(values2)
        values = (values1, values2)
        values = (values1, values2)
        sql1 = "insert into " + keyword + "_MLaccuracy (KNN,SVM) values(%s,%s)"
        query1 = str(sql1)
        curs1.execute(query1, values)

    for i in range(156):
        value1 = (str(KNN_predict[i]), str(SVM_predict[i]))
        sql1 = "insert into " + keyword + "_MLpredict (KNN,SVM) values(%s,%s)"
        query1 = str(sql1)
        curs1.execute(query1, value1)

    value2 = keyword
    sql2 = "insert into MLpredict_list_female (word) values (%s)"
    curs1.execute(sql2, value2)

conn1.commit()
conn1.close()
conn2.commit()
conn2.close()
