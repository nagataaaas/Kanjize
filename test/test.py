import unittest
import sys

from datetime import date, datetime

sys.path.append('../japanera')

from kanjize import kanji2int, int2kanji


class TestKanjize(unittest.TestCase):
    """
    test class of kanjize
    """

    def testkanji2int(self):
        self.assertEqual(1, kanji2int("一"))
        self.assertEqual(10, kanji2int("十"))
        self.assertEqual(11, kanji2int("十一"))
        self.assertEqual(111, kanji2int("百十一"))
        self.assertEqual(211, kanji2int("二百十一"))
        self.assertEqual(121, kanji2int("百二十一"))
        self.assertEqual(11, kanji2int("十一"))
        self.assertEqual(111, kanji2int("百十一"))
        self.assertEqual(211, kanji2int("二百十一"))
        self.assertEqual(121, kanji2int("百二十一"))
        self.assertEqual(1000, kanji2int("千"))
        self.assertEqual(1001, kanji2int("千一"))
        self.assertEqual(2025, kanji2int("二千二十五"))
        self.assertEqual(58076099, kanji2int("五千八百七万六千九十九"))

    def testint2kanji(self):
        self.assertEqual(int2kanji(1), "一")
        self.assertEqual(int2kanji(10), "十")
        self.assertEqual(int2kanji(11), "十一")
        self.assertEqual(int2kanji(111), "百十一")
        self.assertEqual(int2kanji(211), "二百十一")
        self.assertEqual(int2kanji(121), "百二十一")
        self.assertEqual(int2kanji(11), "十一")
        self.assertEqual(int2kanji(111), "百十一")
        self.assertEqual(int2kanji(211), "二百十一")
        self.assertEqual(int2kanji(121), "百二十一")
        self.assertEqual(int2kanji(1000), "千")
        self.assertEqual(int2kanji(1001), "千一")
        self.assertEqual(int2kanji(2025), "二千二十五")
        self.assertEqual(int2kanji(58076099), "五千八百七万六千九十九")


if __name__ == "__main__":
    unittest.main()
