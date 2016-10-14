# coding: utf-8

import datetime

import pandas as pd

import numpy as np

from sklearn.cross_validation import train_test_split
from src.utils.ccf_log import *


import xgboost as xgb

import random

from operator import itemgetter

import zipfile

from sklearn.metrics import roc_auc_score

import time


prefix = "/Users/zhangweimin/Documents/MyDocs/Contest/Ant/ccf_data/final/"

training_filename = prefix + "coupon_feature5_zwm.csv"

testing_filename = prefix + "coupon_feature_6from5_zwm.csv"

submission_dir = prefix

def load_train():

    print("Loading training data csv: " + training_filename)

    training_data = pd.read_csv(training_filename)

    return training_data

def load_test():

    print("Loading testing data csv: " + testing_filename)

    test = pd.read_csv(testing_filename)


    # TODO

    return test

def create_feature_map(features):

    outfile = open('xgb.fmap', 'w')

    for i, feat in enumerate(features):

        outfile.write('{0}\t{1}\tq\n'.format(i, feat))

    outfile.close()

def get_importance(gbm, features):

    create_feature_map(features)

    importance = gbm.get_fscore(fmap='xgb.fmap')

    importance = sorted(importance.items(), key=itemgetter(1), reverse=True)

    return importance

def print_features_importance(imp):

    for i in range(len(imp)):

        print("# " + str(imp[i][1]))

        print('output.remove(\'' + imp[i][0] + '\')')

def run_XGBoost(train, test, features,target,random_state=0):

    eta = 0.1

    max_depth = 5

    subsample = 0.8

    colsample_bytree = 0.8

    start_time = time.time()

    print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'.format(eta, max_depth, subsample, colsample_bytree))

    params = {

        "objective": "binary:logistic",

        "booster" : "gbtree",

        "eval_metric": "auc",

        "eta": eta,

        "max_depth": max_depth,

        "subsample": subsample,

        "colsample_bytree": colsample_bytree,

        "silent": 1,

        "seed": random_state

    }

    num_boost_round = 260

    early_stopping_rounds = 20

    test_size = 0.1

    X_train, X_valid = train_test_split(train, test_size=test_size, random_state=random_state)

    log_info("xtrain len:" + str(len(X_train)))

    y_train = X_train[target]

    y_valid = X_valid[target]

    #添加缺失数据

    dtrain = xgb.DMatrix(X_train[features],y_train,missing = -9999)

    dvalid = xgb.DMatrix(X_valid[features],y_valid,missing = -9999)

    watchlist = [(dtrain, 'train'), (dvalid, 'eval')]

    gbm = xgb.train(params, dtrain, num_boost_round, evals=watchlist, early_stopping_rounds=early_stopping_rounds, verbose_eval=True)

    print("Validating...")

    check = gbm.predict(xgb.DMatrix(X_valid[features]), ntree_limit=gbm.best_ntree_limit)

    score = roc_auc_score(y_valid.values,check)

    print('Check error value: {:.6f}'.format(score))

    imp = get_importance(gbm, features)

    print('Importance array: ', imp)

    print("Predict test set...")

    test_prediction = gbm.predict(xgb.DMatrix(test[features]), ntree_limit=gbm.best_ntree_limit)

    print('Training time: {} minutes'.format(round((time.time() - start_time)/60, 2)))

    return test_prediction.tolist(), score

def create_submission(score, test, prediction):

    # Make Submission

    now = datetime.datetime.now()

    sub_file = submission_dir + 'submission_' + str(score) + '_' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'

    print('Writing submission: ', sub_file)

    f = open(sub_file, 'w')

    f.write('id,probability\n')

    total = 0

    for id in test['id']:

        str1 = str(id) + ',' + str(prediction[total])

        str1 += '\n'

        total += 1

        f.write(str1)

    f.close()

if __name__ == "__main__":
#    random.seed(3)​
    train = load_train()

    test = load_test()

    features = []
    # TODO!

    #添加特征​

   # features.extend([''])

    print('Length of train: ', len(train))

    print('Length of test: ', len(test))

    print('Features [{}]: {}'.format(len(features), sorted(features)))

    #label是目标字段​

    test_prediction, score = run_XGBoost(train, test, features, 7)

    print('Score = {}'.format(score))

    create_submission(score, test, test_prediction)