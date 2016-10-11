# coding: utf-8
import datetime


prefix = "/Users/zhangweimin/Documents/MyDocs/Contest/Ant/ccf_data/"

online_train_file = prefix + "ccf_online_stage1_train.csv"
offline_train_file = prefix + "ccf_offline_stage1_train.csv"
coupon_out_file = prefix + "out_ccf_coupon_feature.csv"

online_type = 20
offline_type = 10
coupon_days_limit = 15
tot_month = 6

null_date = datetime.date(1, 1, 1)
fixed_type = -5