# -*- coding: utf-8 -*-
import sample
import raw_feature
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from common import *
from data import coupon_feature_5,coupon_feature_6form5,merchant_feature_5,merchant_feature_6from5


samples = sample.get_raw_train_sample()
train_samples = [i for i in samples if i.get(DATE_RECEIVED) < '20160601']
test_samples = [i for i in samples if i.get(DATE_RECEIVED) >= '20160601']
X1,Y1 = raw_feature.getSampleFeature(train_samples)
X2,Y2 = raw_feature.getSampleFeature(test_samples)
# print test_samples,X2

def data_merge():
    count = 0
    while count < len(X1):
        for i in coupon_feature_5.values[count]:
            X1[count].append(i)
        for i in merchant_feature_5.values[count]:
            X1[count].append(i)
        count += 1

    count = 0
    while count < len(X2):
        for i in coupon_feature_6form5.values[count]:
            X2[count].append(i)
        for i in merchant_feature_6from5.values[count]:
            X2[count].append(i)
        count += 1


def test_rf():
    rf = RandomForestClassifier(n_estimators=100)
    rf = rf.fit(X1, Y1)
    pre = rf.predict_proba(X2)
    pre = [i[1] for i in pre]
    auc(Y2,pre)

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
        count += 1
        fpr, tpr, thresholds = metrics.roc_curve(dict[coupon_id][0],dict[coupon_id][1], pos_label=1)
        auc_sum += metrics.auc(fpr, tpr)
    print "平均auc"
    print auc_sum/float(count)


data_merge()
test_rf()