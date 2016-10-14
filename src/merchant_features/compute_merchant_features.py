# -*- coding: UTF-8 -*-

import pandas
from default_values import *
from logs import *
from merchant import *
from compute_month_sales import *


def grouped_and_compute_features(offline_data_arg, online_data_arg, total_months):
    data = pandas.DataFrame(pandas.concat([offline_data_arg, online_data_arg]))
    all_merchants_used_coupons = len(data[(data.Coupon_id != 'null') & (data.Date != 'null')].index)
    # print all_merchants_used_coupons
    all_merchant_month_sales = compute_month_sales(offline_data_arg.values, online_data_arg.values, total_months)
    merchant_list = {}
    process_cnt = 0
    for merchant_id, group in data.groupby('Merchant_id'):
        offline_data = offline_data_arg[offline_data_arg.Merchant_id == merchant_id].values
        online_data = online_data_arg[online_data_arg.Merchant_id == merchant_id].values
        mer = merchant(merchant_id, total_months, offline_data, online_data)
        mer.compute_all_features(all_merchants_used_coupons, all_merchant_month_sales)
        merchant_list[merchant_id] = mer.to_record()
        process_cnt += 1
        if process_cnt >= 200 and process_cnt % 200 == 0:
            log_info("已处理" + str(process_cnt) + "组数据")
        # print mer.to_record()
    return merchant_list

if __name__ == "__main__":

    # 读取文件
    log_info("读取文件")
    offline_data_train = pandas.read_csv('..\..\data/ccf_offline_stage1_train.csv')
    online_data_train = pandas.read_csv('..\..\data/ccf_online_stage1_train.csv')
    # 插入使线上线下相同便于操作，值无所谓
    offline_data_train.insert(2, 'Action', online_data_train['Action'])
    online_data_train.insert(5, 'Distance', offline_data_train['Distance'])
    # 1.用1-6月数据得到7月特征
    log_info("用1-6月数据得到7月特征")
    # 数据按merchant_id分组,并计算特征
    log_info("处理中")
    merchant_list_1_6 = grouped_and_compute_features(offline_data_train, online_data_train, 6)
    # print merchant_list_1_6
    # 写入文件
    log_info("写入文件")
    # 先取得测试数据顺序
    offline_data_test = pandas.read_csv('..\..\data/ccf_offline_stage1_test_revised.csv')
    test_data_merchant_ids = offline_data_test['Merchant_id'].values
    # 生成要写入列表
    merchant_features_7 = []
    for i in test_data_merchant_ids:
        if i in merchant_list_1_6:  # 是否有不在的？不在的要给个平均值之类的吗？按相似度预测？
            merchant_features_7.append(merchant_list_1_6[i])
        else:
            merchant_features_7.append(default_values)
    # 写入
    merchant_features_7_df = pandas.DataFrame(merchant_features_7)
    merchant_features_7_df.to_csv("..\..\data\offline_test_merchant-features_month7.csv", index=False)
    del merchant_list_1_6
    del offline_data_test
    del test_data_merchant_ids
    del merchant_features_7
    del merchant_features_7_df

    # 2.用1-5月数据得到1-6月特征
    log_info("用1-5月数据得到1-6月特征")
    # 由读入数据拆分处出1-5月数据
    offline_data_1_5 = offline_data_train[((offline_data_train.Date_received != 'null') &
                                           (offline_data_train.Date_received < '20160601'))
                                          |((offline_data_train.Date_received == 'null') &
                                            (offline_data_train.Date < '20160601'))]
    online_data_1_5 = online_data_train[((online_data_train.Date_received != "null") &
                                           (online_data_train.Date_received < '20160601'))
                                          |((online_data_train.Date_received == 'null') &
                                            (online_data_train.Date < '20160601'))]
    del online_data_train
    # print offline_data_1_5
    # 数据按merchant_id分组计算特征
    log_info("处理中")
    merchant_list_1_5 = grouped_and_compute_features(offline_data_1_5, online_data_1_5, 5)
    # 写入文件
    log_info("写入文件")
    # 1-5月
    merchant_features_1_5 = []
    for m in offline_data_1_5[offline_data_1_5.Coupon_id != 'null'].values:
        merchant_id = m[1]
        merchant_features_1_5.append(merchant_list_1_5[merchant_id])
    merchant_features_1_5_df = pandas.DataFrame(merchant_features_1_5)
    merchant_features_1_5_df.to_csv("..\..\data\offline_train_merchant-features_month1-5.csv", index=False)
    del merchant_features_1_5
    del merchant_features_1_5_df
    # 6月
    merchant_features_6 = []
    offline_data_6_coupon = offline_data_train[(((offline_data_train.Date_received != 'null') &
                                                 (offline_data_train.Date_received >= '20160601'))
                                                | ((offline_data_train.Date_received == 'null') &
                                                   (offline_data_train.Date >= '20160601')))
                                               & (offline_data_train.Coupon_id != 'null')]
    del offline_data_train
    for m in offline_data_6_coupon.values:
        merchant_id = m[1]
        if merchant_id in merchant_list_1_5:
            merchant_features_6.append(merchant_list_1_5[merchant_id])
        else:
            merchant_features_6.append(default_values)
    merchant_features_6_df = pandas.DataFrame(merchant_features_6)
    merchant_features_6_df.to_csv("..\..\data\offline_train_merchant-features_month6.csv", index=False)
    log_info("运行完毕")

    # log_info("写入文件")
    # test_data_merchant_ids = []
    # csv_file = file('..\data\ccf_offline_stage1_test_revised.csv', 'rb')
    # reader = csv.reader(csv_file)
    # for line in reader:
    #     test_data_merchant_ids.append(int(line[1])) # pandas读入后为整型，这里要相应转换
    # csv_file.close()
    # csv_file = file("..\data\offline_test_merchant-features_month7.csv", 'wb')
    # writer = csv.writer(csv_file, dialect='excel')
    # count = 0
    # for i in test_data_merchant_ids:
    #     if i in merchant_list_1_6: # 是否有不在的？不在的要给个平均值之类的吗？按相似度预测？
    #         writer.writerow(merchant_list_1_6[i])
    #     else:
    #         writer.writerow(default_values)
    #     count += 1
    #     if count >= 5000 and count % 5000 == 0:
    #         log_info("已写入" + str(count) + "条数据")
    # csv_file.close()


    # log_info("写入文件")
    # csv_file1 = file("..\data\offline_train_merchant-features_month1-5.csv", 'wb')
    # csv_file2 = file("..\data\offline_train_merchant-features_month6.csv", 'wb')
    # writer1 = csv.writer(csv_file1, dialect='excel')
    # writer2 = csv.writer(csv_file2, dialect='excel')
    # count = 0
    # for i in range(len(offline_data_train.index)):
    #     r = offline_data_train.values[i]
    #     if r[3] == "null": # 普通样本不作为训练数据
    #         continue
    #     if r[1] in merchant_list_1_5:
    #         m = merchant_list_1_5[r[1]] # 似乎有不在的
    #     else:
    #         writer.writerow(default_values)
    #     if r[6] != 'null':
    #         if '20160101' <= r[6] < '20160601':
    #             writer1.writerow(m)
    #         elif '20160601' <= r[6] < '20160701':
    #             writer2.writerow(m)
    #     else:
    #         if '20160101' <= r[7] < '20160601':
    #             writer1.writerow(m)
    #         elif '20160601' <= r[7] < '20160701':
    #             writer2.writerow(m)
    #     count += 1
    #     if count >= 500 and count % 500 == 0:
    #         log_info("已写入" + str(count) + "条数据")
    # csv_file1.close()
    # csv_file2.close()
    # log_info("运行完毕")

# 下一步：
# 15天之内，datetime；另两个特征
# 4,5,6拆开。。
# 线上线下数据距离等
# 商户与优惠券关联等
# 商户相似度，未出现过的商户特征的求法

#文件写回；类，列表等

    # offline_data_1_5 = [record for record in offline_data_train.values
    #     if record[6] < '20160601' or (record[6] == 'null' and record[5] < '20160601')]
    # offline_data_6 = [record for record in offline_data_train.values
    #     if record[6] >= '20160601' or (record[6] == 'null' and record[5] >= '20160601')]
    # online_data_1_5 = [record for record in online_data_train.values
    #     if record[6] < '20160601' or (record[6] == 'null' and record[5] < '20160601')]
    # online_data_6 = [record for record in online_data_train.values
    #     if record[6] >= '20160601' or (record[6] == 'null' and record[5] >= '20160601')]
#    print online_data_6
    # all_merchants_used_coupons = len(offline_data_1_5[offline_data_1_5.Coupon_id != 'null' &
    #                                                   offline_data_1_5.Date != 'null']) + \
    #                              len(online_data_1_5[online_data_1_5.Coupon_id != 'null' &
    #                                                   online_data_1_5.Date != 'null'])
