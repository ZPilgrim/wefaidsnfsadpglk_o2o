# -*- coding: UTF-8 -*-

import time

log_level = 1

def log_info(s):
    print  time.strftime("%H:%M:%S",time.localtime(time.time())) +\
           " [INFO] " + s