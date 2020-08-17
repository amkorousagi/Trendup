import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm,metrics
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
####################################################################
keyword='남자반바지'
####################################################################

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
    path1 = './k-fold/Training_Fold%d_%s' % (i + 1,keyword)
    path2 = './k-fold/Validation_Fold%d_%s' % (i + 1,keyword)
    c1 = 'Training_Fold%d   = np.array(pd.read_csv(path1, sep=",", header=None))' % (i + 1)
    c2 = 'Validation_Fold%d = np.array(pd.read_csv(path2, sep=",", header=None))' % (i + 1)
    exec(c1)
    exec(c2)

# K-fold 학습/검증 레이블
for i in range(Fold):
    path1 = './k-fold/TrainingFold_Label%d_%s' % (i + 1,keyword)
    path2 = './k-fold/ValidationFold_Label%d_%s' % (i + 1,keyword)
    c1 = 'TrainingFold_Label%d   = np.array(pd.read_csv(path1, sep=",", header=None))' % (i + 1)
    c2 = 'ValidationFold_Label%d = np.array(pd.read_csv(path2, sep=",", header=None))' % (i + 1)
    exec(c1)
    exec(c2)

# 전체 학습용 데이터
path1='./k-fold/Training_All_%s'%(keyword)
path2='./k-fold/Training_All_Label_%s'%(keyword)
Training_All = np.array(pd.read_csv(path1, sep=",", header=None))
Training_All_Label = np.array(pd.read_csv(path2, sep=",", header=None).T.squeeze())

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

KNN_model = KNeighborsClassifier(n_neighbors = 3).fit(Training_All , Training_All_Label)
KNN_predict=KNN_model.predict(date_array)


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
SVM_model.fit(Training_All, Training_All_Label)
SVM_predict=SVM_model.predict(date_array)

sql1="delete from "+keyword+"_MLaccuracy"
query1=str(sql1)
curs.execute(query1)

for i in range(Fold):
    s1 = 'values1=round(knnscore_Fold%d,4)'%(i+1)
    exec(s1)
    s2 = 'values2=round(svmscore_Fold%d,4)' % (i + 1)
    exec(s2)
    values1=values1*100
    values1=str(values1)
    values2 = values2 * 100
    values2 = str(values2)
    values=(values1,values2)
    values=(values1,values2)
    sql1 = "insert into "+keyword+"_MLaccuracy (KNN,SVM) values(%s,%s)"
    query1 = str(sql1)
    curs.execute(query1,values)

for i in range(156):
    value1=(str(KNN_predict[i]),str(SVM_predict[i]))
    sql1 = "insert into " + keyword + "_MLpredict (KNN,SVM) values(%s,%s)"
    query1 = str(sql1)
    curs.execute(query1, value1)

value2=keyword
sql2="insert into MLpredict_list (word) values (%s)"
curs.execute(sql2,value2)

conn.commit()
conn.close()
