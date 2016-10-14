# coding: utf-8
import datetime

tot_month = 7
default_value = -2
global_used_month = [4,5,6]
processed_data_month = [7]

prefix = "/Users/zhangweimin/Documents/MyDocs/Contest/Ant/ccf_data/init_data/"

online_train_file = prefix + "ccf_online_stage1_train.csv"
offline_train_file = prefix + "ccf_offline_stage1_train.csv"
coupon_out_file = prefix + "out_ccf_coupon_feature.csv"
coupon_feature_out_file = prefix  + "out_ccf_coupon_feature" + str(processed_data_month[-1]) + ".csv"
online_and_offline_train_file = prefix + "online_and_offline_train_file.csv"
online_and_offline_test_file = prefix + "online_and_offline_test_file.csv"
test_file = prefix + "ccf_offline_stage1_test_revised.csv"

online_type = 20
offline_type = 10
coupon_days_limit = 15

null_date = datetime.date(1, 1, 1)
fixed_type = -5

