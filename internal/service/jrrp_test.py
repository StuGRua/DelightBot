import copy
import datetime
from unittest import TestCase
from internal.service.jrrp import get_exp_time_4am

class TestTime4AM(TestCase):
    def test_add(self):
        ss = get_exp_time_4am()
        print(ss)

    def test_sim(self):
        ex = datetime.datetime.now().timetuple()
        ex_org = datetime.datetime(ex.tm_year, ex.tm_mon, ex.tm_mday, 2)
        ex = ex_org.timetuple()
        if ex.tm_hour < 4:
            ex_time = datetime.datetime(ex.tm_year, ex.tm_mon, ex.tm_mday) + datetime.timedelta(hours=4)
            print("0-4")
        else:
            ex_time = datetime.datetime(ex.tm_year, ex.tm_mon, ex.tm_mday) + datetime.timedelta(days=1, hours=4)
        exp_range_time = int(ex_time.timestamp() - ex_org.timestamp())
        print(ex_org)
        print(ex_time)
        print(exp_range_time/3600)