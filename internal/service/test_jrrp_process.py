import unittest
import internal.service.jrrp as jrrp


class TestJRRP(unittest.TestCase):
    def add_some(self):
        for i in range(10001, 10009):
            res1, res2 = jrrp.jrrp(i)
            print(res1,res2)

    def test_add(self):
        self.add_some()

    def test_cal(self):
        jrrp.jrrp_cal()


if __name__ == '__main__':
    unittest.main()
