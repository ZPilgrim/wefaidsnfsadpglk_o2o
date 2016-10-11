# coding: utf-8

import csv

from src.coupon.parameters import *
from src.utils.ccf_log import *
from src.coupon.coupon import *
from src.utils.file_io import *

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
            if iterms[2] == "null":continue
            c = init_offline_coupon(iterms)
            id = c.get_id()
        else:
            if iterms[3] == "null":continue
            c = init_online_coupon(iterms)
            id = c.get_id()
        if id == -1:
            log_special_debug("id == -1" + str(line))
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

    return cs_records, cs

if __name__ == "__main__":

    cs_records = []
    cs = []
    pos = {} #key:id value:idx in cs

    log_info("process offline file")
    offline_file = file(offline_train_file, 'rb')

    init_cs(offline_file, offline_type, cs, cs_records, pos)

    offline_file.close()

    log_info("process  online file")
    online_file = file(online_train_file, 'rb')
    init_cs(online_file, online_type, cs, cs_records, pos )
    online_file.close()

    log_info("dump cs_data to file")
    cs_data = []
    for c in cs:
        cs_data.append(c.to_tuple())

    csv_write_file(coupon_out_file, cs_data)

