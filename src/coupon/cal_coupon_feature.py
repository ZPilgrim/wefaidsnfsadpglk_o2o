# coding: utf-8

import csv
import copy

from src.coupon.parameters import *
from src.utils.ccf_log import *
from src.coupon.coupon import *
from src.utils.file_io import *

def judge_if_use(c):
    month = -1
    if c.get_date_received() != null_date:
            month = c.get_date_received().month
    #log_special_debug(str(month))
    if month == -1 : return False
    #log_special_debug(str(month in global_used_month))
    return month in global_used_month


def init_offline_coupon(iterms):

   c = Coupon()
   c.set_id(iterms[2])
   c.set_user_id(iterms[0])
   c.set_merchant_id(iterms[1])
   c.set_discount(iterms[3], offline_type)
   c.set_distance(iterms[4])
   c.set_date_received(iterms[5])
   c.set_use_date(iterms[6])

   return c


def init_online_coupon(iterms):

    c = Coupon()
    c.set_id(iterms[3])
    c.set_user_id(iterms[0])
    c.set_merchant_id(iterms[1])
    c.set_action(iterms[2])
    c.set_discount(iterms[4], online_type)
    c.set_date_received(iterms[5])
    c.set_use_date(iterms[6])

    return c

def init_cs(file, type, cs, cs_records, pos):

    log_info("---> init_cs type:" + str(type))
    process_cnt = 0

    reader = csv.reader(file)
    for line in reader:
        iterms = line
        #log_special_debug("line:" + str(iterms))

        id = -1
        if type == offline_type:
            if iterms[2] == "null":
                continue
            c = init_offline_coupon(iterms)
            id = c.get_id()
        else:
            if iterms[3] == "null":
                continue
            c = init_online_coupon(iterms)
            id = c.get_id()
        if id == -1:
            log_special_debug("id == -1" + str(line))
            continue

        if judge_if_use(c) == False:
            continue

        if pos.has_key(id) == False:
            pos[id] = len(cs)
            cs.append(c)

        cs[pos[id]].add_record(c)

        cs_records.append(c)

        process_cnt += 1
        if process_cnt%5000 == 0:
            log_info("process cnt:" + str(process_cnt) )
    log_info("cal_avg_var")
    for c in cs:
        c.cal_avg_var()

    log_info("<--- init_cs type:" + str(type))

    return cs_records, cs, pos

def cal_out_coupon_features(file, data, cs, cs_idx, coupon_idx=2):
    log_info("---> cal_out_coupon_features ")
    process_cnt = 0

    reader = csv.reader(file)
    for line in reader:
        items = line

        if items[coupon_idx] == 'null' or items[5] == 'null' :#or cs_idx.has_key(int(items[coupon_idx])) == False:
            cf = Coupon_feature(0)
            continue
        else:
            if cs_idx.has_key(int(items[coupon_idx])) == False:
                cf = Coupon_feature(0)
            else:
                pos = cs_idx[int(items[coupon_idx])]
                if string_to_date(items[5]).month not in processed_data_month :
                    #log_info("month :" + str(cs[pos].get_date_received().month) )
                    continue
                cf = Coupon_feature(cs[pos])

        data.append(cf.to_tuple())

        process_cnt += 1
        if process_cnt%5000 == 0:
            log_info("cal_out_coupon_features process_cnt:" + str(process_cnt))

    log_info("<--- cal_out_coupon_features ")
    return data


def cal_online_coupon_features(file, data, cs, cs_idx, coupon_idx=3):
    log_info("---> cal_online_coupon_features ")
    process_cnt = 0

    reader = csv.reader(file)
    for line in reader:
        items = line

        if items[coupon_idx] == 'null' or items[5] == 'null' :#or cs_idx.has_key(int(items[coupon_idx])) == False:
            cf = Coupon_feature(0)
            continue
        else:
            if items[coupon_idx] == 'fixed':
                    items[coupon_idx] = str(fixed_type)
            if cs_idx.has_key(int(items[coupon_idx])) == False:
                cf = Coupon_feature(0)
            else:

                pos = cs_idx[int(items[coupon_idx])]
                if string_to_date(items[5]).month not in processed_data_month :
                    #log_info("month :" + str(cs[pos].get_date_received().month) )
                    continue
                cf = Coupon_feature(cs[pos])

        data.append(cf.to_tuple())

        process_cnt += 1
        if process_cnt%5000 == 0:
            log_info("cal_online_coupon_features process_cnt:" + str(process_cnt))

    log_info("<--- cal_online_coupon_features ")
    return data


def cal_out_coupon_features_classifed_by_type(file, cs, data, coupon_idx=3):

    log_info("---> cal_out_coupon_features_classifed_by_type")

    process_cnt = 0

    tcf = []
    tcf_idx = {}
    combine_tcf = []
    combine_tcf_idx = {}

    for c in cs:
        type = c.get_combine_type()
        if tcf_idx.has_key(type) :
            idx = tcf_idx[type]
            tcf[idx].combine_coupon_record(c)
        else:
            tcf_idx[type] = len(tcf)
            tcf.append(c)

        process_cnt += 1
        if process_cnt%5000 == 0:
            log_info("combine cnt:" + str(process_cnt))

    log_info("tcf len:" + str(len(tcf)) + " idx len:" + str(len(tcf_idx)) + " cs len:" + str(len(cs)) )

    process_cnt = 0

    for c in tcf:
        c.cal_avg_var()
        cf = Coupon_feature(c)
        combine_tcf_idx[c.get_combine_type()] = len(combine_tcf)
        combine_tcf.append(cf)

        process_cnt += 1
        if process_cnt%5000 == 0:
            log_info("cal feature cnt:" + str(process_cnt))

    process_cnt = 0
    reader = csv.reader(file)
    for line in reader:
        items = line
        if items[coupon_idx] == 'null' or items[5] == 'null' :#or combine_tcf_idx.has_key(str(items[coupon_idx])) == False:
            cf = Coupon_feature(0)
            continue
        else:
            if combine_tcf_idx.has_key(str(items[coupon_idx])) == False:
                cf = Coupon_feature(0)
            else:
                pos = combine_tcf_idx[str(items[coupon_idx])]

                if string_to_date(items[5]).month not in processed_data_month :
                    log_info("month :" + str(cs[pos].get_date_received().month) )
                    continue

                cf = Coupon_feature(cs[pos])
        data.append(cf.to_tuple())

        process_cnt += 1
        if process_cnt%5000 == 0:
            log_info("cal_out_coupon_features process_cnt:" + str(process_cnt))



    log_info("<--- cal_out_coupon_features_classifed_by_type")


def process_offline_date(offline_train_file, cs, cs_records, pos):

    log_info("process offline file, init cnt:" + str(len(cs)))
    offline_file = file(offline_train_file, 'rb')

    init_cs(offline_file, offline_type, cs, cs_records, pos)

    offline_file.close()

def process_online_data(online_train_file, cs, cs_records, pos):
    log_info("process  online file, init cnt:" + str(len(cs)) )
    online_file = file(online_train_file, 'rb')
    init_cs(online_file, online_type, cs, cs_records, pos )
    online_file.close()


def process_test_data(test_file, cs, feature_data):
    offline_file = file(test_file, 'rb')
    cal_out_coupon_features_classifed_by_type(offline_file, cs, feature_data)
    offline_file.close()

def process_sample_train_data(offline_file, cs, feature_data, pos):
    offline_file = file(offline_file, 'rb')
    cal_out_coupon_features(offline_file, feature_data, cs, pos)
    offline_file.close()

def process_sample_online_data(online_file, cs, feature_data, pos ):
    online = file(online_file, 'rb')
    cal_online_coupon_features(online, feature_data, cs, pos)
    online.close()

if __name__ == "__main__":

    cs_records = []
    cs = []
    pos = {} #key:id value:idx in cs
    cs_offline = []
    feature_data = []

    process_offline_date(offline_train_file, cs, cs_records, pos)
    process_online_data(online_train_file, cs, cs_records, pos)

    #process_sample_train_data(offline_train_file, cs, feature_data, pos)

    process_test_data(test_file, cs, feature_data)

    log_info("dump features to file")
    csv_write_file(coupon_feature_out_file, feature_data)