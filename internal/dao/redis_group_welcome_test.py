import unittest
from internal.dao.redis_group_welcome import set_greeting_msg, get_greeting


class GPWelcome(unittest.TestCase):
    def test_adding(self):
        set_greeting_msg(514394960, '{"1":"|･ω･｀)","2":"欢迎新朋友~||--来自罗伯特喵喵的自动问候~"}')
        resp = get_greeting(514394960)
        print(resp)
        self.assertEqual(type(resp), dict)  # add assertion here

    def test_nt(self):
        set_greeting_msg(514394960, '{"1":"|･ω･｀)","2":"欢迎新朋友~||--来自罗伯特喵喵的自动问候~"}')
        resp = get_greeting(514394961)
        print(resp)
        self.assertEqual(resp, dict())  # add assertion here

if __name__ == '__main__':
    unittest.main()
