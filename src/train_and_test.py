# -*- coding: utf-8 -*-
import sample
import raw_feature
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from common import *
from sklearn.ensemble import GradientBoostingClassifier
from src.utils.change_to_xgboost_data import *
from src.utils.file_io import *
from tsrc.data import *
from src.utils.ccf_log import *
import time
import xgboost as xgb



samples = sample.get_raw_train_sample()
train_samples = [i for i in samples if  i.get(DATE_RECEIVED) < '20160601']
test_samples = [i for i in samples if i.get(DATE_RECEIVED) >= '20160601']
# test_samples = []
# test_samples_positive = []
# test_samples_negative = []
# for i in samples:
#     if i.get(DATE_RECEIVED)>='20160601' and i.get(LABEL)==0:
#         test_samples_negative.append(i)
#     if i.get(DATE_RECEIVED) >= '20160601' and i.get(LABEL) == 1:
#         test_samples_positive.append(i)
# length = len(test_samples_positive)
# test_samples = test_samples_positive + test_samples_negative[0:length/10]
X1,Y1 = raw_feature.getSampleFeature(train_samples)
X2,Y2 = raw_feature.getSampleFeature(test_samples)

def test_rf():
    rf = RandomForestClassifier(n_estimators=100)
    rf = rf.fit(X1,Y1)
    pre = rf.predict_proba(X2)
    pre = [i[1] for i in pre]
    auc(Y2,pre)
    # fpr, tpr, thresholds = metrics.roc_curve(Y2, pre, pos_label=1)
    # print metrics.auc(fpr, tpr)
    # for i in range(10000):
    #     print (Y2[i],pre[i]),(Y2[-i],pre[-i])


def test_lr():
    lr = LogisticRegression(C=1000.0, penalty='l1')
    lr = lr.fit(X1,Y1)
    pre = lr.predict_proba(X2)
    pre = [i[1] for i in pre]
    fpr, tpr, thresholds = metrics.roc_curve(Y2, pre, pos_label=1)
    print metrics.auc(fpr, tpr)


def test_xgboost():
    log_info("test_xgboost, X1:" + str(len(X1)) + " Y1:" + str(len(Y1)) + " X2:" + str(len(X2)) )

    data1 = change_to_xgb_feature(X1, Y1, 1, False)
    csv_write_file(xgb_train_file, data1)
    data2 = change_to_xgb_feature(X2, [], 1, False)
    csv_write_file(xgb_test_file, data2)

    cnt = 0
    cnt_2 = 0
    for i in range(0, len(Y1)):
        if int( Y1[i] ) == 1:
            cnt += 1
        if i >= len(data2) : continue
        if int(data2[i][0]) == 1:
            cnt_2 += 1
    log_info("xgboost init data end, train rows:" + str(len(data1)) + " col:" + str(len(data1[0])) + " " + str(data1[0]) )
    log_info("train: pos:" + str(cnt) + " neg:" + str(len(Y1) - cnt))
    log_info("test pos:" + str(cnt_2) + " neg:" + str(len(Y2) - cnt_2) + " line:" + str(data2[0]))


    eta = 0.1

    max_depth = 6

    subsample = 0.8

    colsample_bytree = 0.8

    start_time = time.time()

    print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'.format(eta, max_depth, subsample, colsample_bytree))

    params = {

        "objective": "binary:logistic",

        "booster" : "gbtree",

        "eval_metric": "auc",

        "eta": eta,

        "max_depth": 6,

        "subsample": subsample,

        "colsample_bytree": colsample_bytree,

        "silent": 1,

        "seed": 0,
    }
    num_boost_round = 260
#    early_stopping_rounds = 20
#    test_size = 0.1

    log_info("xgboost read data ")

    dtrain = xgb.DMatrix(xgb_train_file)
    dtest = xgb.DMatrix(xgb_test_file)
    watchlist = [(dtest,'eval'), (dtrain,'train')]
    num_round = 3000

    log_info("xgboost start train ")
    bst = xgb.train(params, dtrain, num_round, watchlist)

    log_info("xgboost predict ")
    ypred1 = bst.predict(dtest, ntree_limit=1)
    # by default, we predict using all the trees
    ypred2 = bst.predict(dtest)
    auc(Y2, ypred1)
    auc(Y2, ypred2)

def test_gbdt():
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05,max_depth = 6, random_state = 0).fit(X1, Y1)
    pre = clf.predict_proba(X2)
    pre = [i[1] for i in pre]
    auc(Y2, pre)


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



if __name__ == "__main__":

    #test_rf()
    test_xgboost()
    test_gbdt()