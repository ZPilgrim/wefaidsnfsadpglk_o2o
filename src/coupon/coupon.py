# coding: utf-8

import datetime
from src.coupon.parameters import *
from src.utils.ccf_date import *
from src.utils.ccf_log import *


class Coupon:
    def __init__(self):
        self.id = 0
        self.click_cnt = 0
        self.buy_cnt = 0
        self.get_cnt = 0

        self.tot_cnt  = 0
        self.used_cnt_within = 0
        self.used_cnt_out = 0
        self.get_not_used = 0
        # 0 means discount_rate 1 bargin 2 fixed
        # 10 means offline 20 means online
        self.type = 0
        self.discount_rate = 0.0
        self.bargin = [0, 0]
        self.level = -1
        self.used_cnt_within_list = []
        self.used_cnt_out_list = []

        for i in range(0, tot_month):
            self.used_cnt_within_list.append(0)
            self.used_cnt_out_list.append(0)

        self.monthly_used_variance = 0.0
        self.monthly_average_used_within_cnt = 0.0
        self.distance = 0

        self.user_id = 0
        self.merchant_id = 0
        self.action = -1
        self.use_date = null_date
        self.date_received = null_date
        self.combine_type = "null"

    def set_id(self, id):
        #log_debug(str(id))
        if id == 'fixed':
            self.id = fixed_type
            self.combine_type = 'fixed'
            return
        if type(id) == int:
            self.id = id
        else:
            self.id = int(id)

    def get_id(self):
        return self.id

    def set_user_id(self, id):

        if type(id) == int:
            self.user_id = id
        else:
            self.user_id = int(id)

    def set_merchant_id(self, id):

        if type(id) == int:
            self.merchant_id = id
        else:
            self.merchant_id = int(id)

    def set_discount_rate(self, rate):
        self.discount_rate = float(rate)

    def set_action(self, ac):
        self.action = int(ac)

    def set_distance(self, dis):
        if dis == 'null':
            self.distance = -1
        else:
            self.distance = int(dis)

    def set_discount(self, dis, type):
        if dis == "fixed":
            self.type = type + 2
            self.combine_type = dis
            return
        if self.id != fixed_type: self.combine_type = dis
        if dis.find(':') == -1:
            self.type = type + 0
            self.set_discount_rate(dis)
        else:
            pos = dis.find(':')
            self.type = type + 1
            self.bargin = [int(dis[0:pos]), int(dis[pos+1:])]

    def set_date_received(self, time):
        if len(time) >= 8:
            self.date_received = datetime.date(int(time[0:4]), int(time[4:6]), int(time[6:8]))
        else:
            self.date_received = null_date

    def set_use_date(self, time):
        #log_debug("time:" + str(time) + " len:" + str(len(time)))
        if len(time) >= 8:
            self.use_date = datetime.date(int(time[0:4]), int(time[4:6]), int(time[6:8]))
        else:
            self.use_date = null_date

    def get_use_date(self):
        return self.use_date

    def get_combine_type(self):
        return self.combine_type

    def get_date_received(self):
        return self.date_received

    def add_record(self, c):
        if self.id != c.get_id():return

        self.tot_cnt += 1
        if c.get_use_date() == null_date:
            self.get_not_used += 1
        else:

            if date_diff(c.get_use_date(), c.get_date_received()) <= coupon_days_limit:
                self.used_cnt_within += 1
                self.used_cnt_within_list[c.get_use_date().month - 1] += 1
            else:
                self.used_cnt_out += 1
                self.used_cnt_out_list[c.get_use_date().month - 1] += 1

        if c.action == 0: self.click_cnt += 1
        if c.action == 1: self.buy_cnt += 1
        if c.action == 2: self.get_cnt += 1


    def combine_coupon_record(self, c):
        self.tot_cnt += c.tot_cnt
        self.get_not_used += c.get_not_used
        self.used_cnt_within += c.used_cnt_within
        self.used_cnt_out += c.used_cnt_out

        for i in range(0, len( global_used_month )):
            self.used_cnt_within_list[i] += c.used_cnt_within_list[i]
            self.used_cnt_out_list[i] += c.used_cnt_out_list[i]

        self.click_cnt += c.click_cnt
        self.buy_cnt += c.buy_cnt
        self.get_cnt += c.get_cnt


    def cal_avg_var(self):
        tot = 0.0

        for idx in global_used_month:
            tot += self.used_cnt_within_list[idx-1]
        self.monthly_average_used_within_cnt = tot/len(global_used_month)

        for idx in global_used_month:
            self.monthly_used_variance += (self.monthly_average_used_within_cnt - self.used_cnt_within_list[idx-1]) * (self.monthly_average_used_within_cnt - self.used_cnt_within_list[idx-1])

        self.monthly_used_variance /= len(global_used_month)
#       for i in self.used_cnt_within_list:
#            tot += i
#        self.monthly_average_used_within_cnt = tot/len(self.used_cnt_within_list)
#        for i in self.used_cnt_within_list:
#            self.monthly_used_variance += (self.monthly_average_used_within_cnt - i) * (self.monthly_average_used_within_cnt - i)
#
#        self.monthly_used_variance /= len(self.used_cnt_within_list)

    def to_tuple(self):
       return ( str(self.id), str(self.click_cnt), str(self.buy_cnt), str(self.get_cnt), str(self.tot_cnt),
                 str(self.used_cnt_within), str(self.used_cnt_out), str(self.get_not_used), str(self.type), str(self.discount_rate),
                str(self.bargin), str(self.level), str(self.used_cnt_within_list), str(self.used_cnt_out_list), str(self.monthly_used_variance),
                str(self.monthly_average_used_within_cnt), str(self.distance), str(self.user_id), str(self.merchant_id), str(self.action), )



class Coupon_feature:
    def __init__(self, c):

        if type(c) == int:
            self.default_feature()
            return

        self.c = c
        if c.tot_cnt != 0:
           self.used_within_percent = float(c.used_cnt_within)/c.tot_cnt
        else:
            self.used_within_percent = default_value

        if c.tot_cnt != 0:
            self.get_not_used_percent = float(c.get_not_used)/c.tot_cnt
        else:
            self.get_not_used_percent = default_value

        if c.tot_cnt != 0:
            self.used_cnt_out_percent = float(c.used_cnt_out)/c.tot_cnt
        else:
            self.used_cnt_out_percent = default_value

        self.discount_percent = default_value
        if c.type%10 == 0:
            self.discount_percent = c.discount_rate
        if c.type%10 == 1:
            self.discount_percent = float(c.bargin[1])/float(c.bargin[0])

        self.monthly_used_avg_percent = c.monthly_average_used_within_cnt
        self.monthly_used_variance = c.monthly_used_variance
        self.sale_rate = []
        tot_used_within_cnt = 0.0
        for i in c.used_cnt_within_list:
            tot_used_within_cnt += i
        if tot_used_within_cnt == 0:
            for i in range(0, tot_month):
                self.sale_rate.append(0.0)
        else:
            for i in range(0, tot_month):
                self.sale_rate.append(c.used_cnt_within_list[i]/ float(tot_used_within_cnt))

    def default_feature(self):
        self.used_cnt_out_percent = default_value
        self.get_not_used_percent = default_value
        self.used_cnt_out_percent = default_value
        self.discount_percent = default_value
        self.monthly_used_avg_percent = default_value
        self.monthly_used_variance  = default_value
        self.sale_rate = []
        for i in range(0, tot_month):
            self.sale_rate.append(default_value)

    def to_tuple(self):
        ret = []
        ret.append(str(self.used_cnt_out_percent))
        ret.append(str(self.get_not_used_percent))
        ret.append(str(self.used_cnt_out_percent))
        ret.append(str(self.discount_percent))
        ret.append(str(self.monthly_used_avg_percent))
        ret.append(str(self.monthly_used_variance))
        for r in self.sale_rate:
            ret.append(str(r))

        return tuple(ret)

