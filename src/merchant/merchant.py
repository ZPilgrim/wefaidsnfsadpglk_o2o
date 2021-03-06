# -*- coding: UTF-8 -*-

import numpy

from global_values import distance_level, USER_ID, MERCHANT_ID, COUPON_ID, DISCOUNT_RATE, DISTANCE, DATE_RECEIVED, DATE

from compute_month_sales import *


class Merchant:
    def __init__(self, merchant_id, start_month, end_month, offline_data):
        # 商户特征
        self.merchant_id = merchant_id
        self.dist_user_portion = [0.0] * distance_level  # 距离为i档的用户的个数/该店总的用户的个数
        self.dist_consume_portion = [0.0] * distance_level  # 距离为i档的消费记录的个数/该店总的消费记录的个数
        # 上面两个特征只使用线下数据计算，但未分母去掉距离为null的记录，是否合适？
        self.used_coupon_portion = 0.0  # 使用的优惠券的数量（额度）/所有商店使用的优惠券的数量(额度)
        self.pi_avg = 0.0  # Pi=第I个月消费件数/第I月所有店消费记录个数
        self.pi_var = 0.0
        self.latest_pi = 0.0
        self.gradient_avg = 0.0  # 梯度平均值，即近2个月销售额差值平均值
        self.visit_frequency_without_coupon = 0.0  # 被访问次数/总的记录
        # self.dist_visit_portion = 0.0 #要多个吗？
        # self.coupon_portion = [] #多少个档？
        # 15天内用掉的优惠券数目..

        # 其他所需变量
        self.offline_data = offline_data
        self.start_month = start_month
        self.end_month = end_month
        self.month_sales = [0] * (self.end_month - self.start_month + 1)

    def compute_dist_user_portion(self):
        if len(self.offline_data) == 0:
            self.dist_user_portion = [-1] * distance_level
            return
        sorted(self.offline_data, key=lambda offline_record: offline_record[0])
#        print self.offline_data
        temp_user_id = self.offline_data[0][0]
        user_count = 1
        dist_user_count = [0] * distance_level
        if self.offline_data[0][DISTANCE] != 'null':
            dist_user_count[int(self.offline_data[0][DISTANCE])] += 1
        for r in self.offline_data:
            if temp_user_id != r[0]:
                user_count += 1
                if r[DISTANCE] != 'null':
                    dist_user_count[int(r[DISTANCE])] += 1
        for i in range(distance_level):
            self.dist_user_portion[i] = float(dist_user_count[i]) / float(user_count)
            # print self.dist_user_portion[i]

    def compute_dist_consume_portion(self):
        if len(self.offline_data) == 0:
            self.dist_consume_portion = [-1] * distance_level # 缺失值填负值
            return
        dist_consume_count = [0] * distance_level
        consume_count = 0
        for r in self.offline_data:
            consume_count += 1
            if r[DISTANCE] != 'null':
                dist_consume_count[int(r[DISTANCE])] += 1
        for i in range(distance_level):
            self.dist_consume_portion[i] = float(dist_consume_count[i]) / float(consume_count)
            #            print self.dist_consume_portion[i]

    def compute_used_coupon_portion(self, all_merchants_used_coupons):
        used_coupons = 0
        for r in self.offline_data:
            if r[DATE] != "" and r[COUPON_ID] != "null":
                used_coupons += 1
        if all_merchants_used_coupons != 0:
            self.used_coupon_portion = float(used_coupons) / float(all_merchants_used_coupons)
        # print self.used_coupon_portion

    def compute_month_sales(self):
        self.month_sales = compute_month_sales(self.offline_data, self.start_month, self.end_month)

    def compute_pi(self, all_merchants_month_sales):
        self.compute_month_sales()
        pi = [0.0] * (self.end_month - self.start_month + 1)
        for i in range(len(all_merchants_month_sales)):
            if all_merchants_month_sales[i] != 0:
                pi[i] = float(self.month_sales[i]) / float(all_merchants_month_sales[i])
        self.pi_avg = numpy.mean(pi)
        self.pi_var = numpy.var(pi)
        self.latest_pi = pi[-1]
        # print self.pi_avg, self.pi_var, self.latest_pi

    def compute_gradient_avg(self):
        self.compute_month_sales()
        self.gradient_avg = float(self.month_sales[-1] - self.month_sales[0]) / 2
        # print self.gradient_avg

    def compute_visit_frequency_without_coupon(self):
        visit_times_without_coupon = 0
        for r in self.offline_data:
            if r[COUPON_ID] == "null" and r[DATE] != "":
                visit_times_without_coupon += 1
        self.visit_frequency_without_coupon = float(visit_times_without_coupon) / float(len(self.offline_data))
        # print self.visit_frequency_without_coupon

    def compute_all_features(self, all_merchants_used_coupons, all_merchants_month_sales):
        self.compute_dist_consume_portion()
        self.compute_dist_user_portion()
        self.compute_gradient_avg()
        self.compute_pi(all_merchants_month_sales)
        self.compute_used_coupon_portion(all_merchants_used_coupons)
        self.compute_visit_frequency_without_coupon()

    def to_record(self):
        # [self.merchant_id] +
        return self.dist_user_portion + self.dist_consume_portion + \
               [self.used_coupon_portion, self.pi_avg, self.pi_var, self.latest_pi,
                self.gradient_avg, self.visit_frequency_without_coupon]

