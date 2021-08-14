from unittest import TestCase
from internal.service.bili import query_player_status_str


class TestStat(TestCase):
    def test_status(self):
        stat = query_player_status_str(92613)
        print(stat)
