# -*- coding: utf-8 -*-
import sample
import raw_feature
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from common import *
from sklearn.ensemble import GradientBoostingClassifier
from data import _5_data,_4_data,_3_data,_2_data,_1_data

#构造样本，2月的数据用1月的特征，3月的数据用2月的特征，以此类推
samples = sample.get_raw_train_sample()
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160601' and i.get(DATE_RECEIVED) >= '20160501']
X1,Y1 = raw_feature.getSampleFeature(train_samples,_4_data)
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160501' and i.get(DATE_RECEIVED) >= '20160401']
temp_X1,temp_Y1 = raw_feature.getSampleFeature(train_samples,_3_data)
X1 += temp_X1
Y1 += temp_Y1
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160401' and i.get(DATE_RECEIVED) >= '20160301']
temp_X1,temp_Y1 = raw_feature.getSampleFeature(train_samples,_2_data)
X1 += temp_X1
Y1 += temp_Y1
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160301' and i.get(DATE_RECEIVED) >= '20160201']
temp_X1,temp_Y1 = raw_feature.getSampleFeature(train_samples,_1_data)
X1 += temp_X1
Y1 += temp_Y1


test_samples = [i for i in samples if i.get(DATE_RECEIVED)>= '20160601']
X2,Y2 = raw_feature.getSampleFeature(test_samples,_5_data)

def test_rf():
    rf = RandomForestClassifier(n_estimators=10)
    rf = rf.fit(X1,Y1)
    pre = rf.predict_proba(X2)
    pre = [i[1] for i in pre]
    auc(Y2,pre)


def test_gbdt():
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05,max_depth = 6, random_state = 0).fit(X1, Y1)
    pre = clf.predict_proba(X2)
    pre = [i[1] for i in pre]
    auc(Y2, pre)

def test_lr():
    lr = LogisticRegression(C=1000.0, penalty='l1')
    lr = lr.fit(X1,Y1)
    pre = lr.predict_proba(X2)
    pre = [i[1] for i in pre]
    fpr, tpr, thresholds = metrics.roc_curve(Y2, pre, pos_label=1)
    print metrics.auc(fpr, tpr)

def auc(Y,pre):
    dict = {}
    auc_sum = 0.0
    count = 0
    fpr, tpr, thresholds = metrics.roc_curve(Y2, pre, pos_label=1)
    print '总体auc'
    print metrics.auc(fpr, tpr)
    for i in range(len(test_samples)):
        coupon_id = test_samples[i].get(COUPON_ID)
        if coupon_id not in dict:
            dict[coupon_id]=[[],[]]
        dict[coupon_id][0].append(Y[i])
        dict[coupon_id][1].append(pre[i])

    for coupon in dict:
        flag1 = 0
        flag2 = 0
        for i in dict[coupon][0]:
            if i==0:
                flag1 = 1
            else:
                flag2 = 1
        if(flag1==1 and flag2==1):
            #两类样本都存在
            count += 1
            auc_sum += metrics.roc_auc_score(dict[coupon][0], dict[coupon][1])
    print "平均auc"
    print auc_sum/float(count)



# test_rf()
test_gbdt()