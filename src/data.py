import pandas as pd

offline_data_train = pd.read_csv('../../ccf_data/ccf_offline_stage1_train.csv')
offline_data_positive = offline_data_train[(offline_data_train.Coupon_id != "null") & (offline_data_train.Date != 'null')]
offline_data_test = pd.read_csv('../../ccf_data/ccf_offline_stage1_test.csv')
