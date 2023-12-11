import unittest

from kanjize import *


class TestKanjize(unittest.TestCase):
    """
    test class of kanjize
    """

    def test_kanji2number(self):
        self.assertEqual(1, kanji2number("一"))
        self.assertEqual(10, kanji2number("十"))
        self.assertEqual(11, kanji2number("十一"))
        self.assertEqual(111, kanji2number("百十一"))
        self.assertEqual(211, kanji2number("二百十一"))
        self.assertEqual(121, kanji2number("百二十一"))
        self.assertEqual(11, kanji2number("十一"))
        self.assertEqual(111, kanji2number("百十一"))
        self.assertEqual(211, kanji2number("二百十一"))
        self.assertEqual(121, kanji2number("百二十一"))
        self.assertEqual(1_000, kanji2number("千"))
        self.assertEqual(1_001, kanji2number("千一"))
        self.assertEqual(2_025, kanji2number("二千二十五"))
        self.assertEqual(58_076_099, kanji2number("五千八百七万六千九十九"))

        # added 1.0.0
        self.assertEqual(10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,
                         kanji2number("一恒河沙"))
        self.assertEqual(
            9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999,
            kanji2number("九千九百九十九無量大数九千九百九十九不可思議九千九百九十九那由多九千九百九十九阿僧祇九千九百九十九恒河沙九千九百九十九極"
                         "九千九百九十九載九千九百九十九正九千九百九十九澗九千九百九十九溝九千九百九十九穣九千九百九十九𥝱九千九百九十九垓"
                         "九千九百九十九京九千九百九十九兆九千九百九十九億九千九百九十九万九千九百九十九")
        )

        self.assertEqual(1, kanji2number("1"))
        self.assertEqual(10, kanji2number("10"))
        self.assertEqual(11, kanji2number("11"))
        self.assertEqual(121, kanji2number("121"))
        self.assertEqual(1000, kanji2number("1千"))
        self.assertEqual(1001, kanji2number("1001"))
        self.assertEqual(2025, kanji2number("2025"))
        self.assertEqual(5807_6099, kanji2number("5807万6099"))
        self.assertEqual(223_4235_4256_6000, kanji2number("223兆4235億4256万6千"))
        self.assertEqual(223_4000_4256_6000, kanji2number("223兆4千億4256万6千"))
        self.assertEqual(5000_0000_0000_0000_0000, kanji2number("5千京"))
        self.assertEqual(39_4385_0000_4895_0000, kanji2number("39京4385兆4895万"))

        # added 0.2.1
        self.assertEqual(1001, kanji2number("千1"))
        self.assertEqual(2025, kanji2number("2千2十5"))
        self.assertEqual(400_0000, kanji2number("4百万"))
        self.assertEqual(5807_6099, kanji2number("58百7万6千99"))
        self.assertEqual(223_4235_4256_6000, kanji2number("2百23兆4千2百3十5億4256万6千"))
        self.assertEqual(223_4000_4256_6000, kanji2number("223兆4千億4256万6千"))
        self.assertEqual(223_4000_4256_6000, kanji2number("2234千億4256万6千"))
        self.assertEqual(5050_0000_0000_0000_0000, kanji2number("5千5十京"))
        self.assertEqual(39_4385_0000_4895_0000, kanji2number("39京4385兆4895万"))

        # added 1.0.0
        self.assertEqual(10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,
                         kanji2number("1恒河沙"))
        self.assertEqual(
            999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999,
            kanji2number("9999無量大数9999不可思議9999那由多9999阿僧祇"
                         "9999恒河沙9999極9999載9999正9999澗9999溝9999穣"
                         "9999𥝱9999垓9999京9999兆9999億9999万9999")
        )

        # added 1.1.0
        self.assertEqual(1_5000_0000, kanji2number("1.5億"))
        self.assertEqual(25_0320, kanji2number("250.32千"))
        self.assertEqual(1_5025_0320, kanji2number("1.5億250.32千"))

        # added 1.2.0
        self.assertEqual(-1_5000_0000, kanji2number("-1.5億"))
        self.assertEqual(-25_0320, kanji2number("-250.32千"))
        self.assertEqual(-1_5025_0320, kanji2number("-1.5億250.32千"))

        self.assertEqual(1234, kanji2number("一千二百三十四"))
        self.assertEqual(1234, kanji2number("千二百三十四"))

        # added 1.4.0
        self.assertEqual(0, kanji2number("零"))

        # added 1.5.0
        self.assertEqual(12345, kanji2number("12千345"))
        with self.assertRaises(ValueError):
            kanji2number("1千1000")
        with self.assertRaises(ValueError):
            kanji2number("1万10千")
        with self.assertRaises(ValueError):
            kanji2number("万1千234")
        with self.assertRaises(ValueError):
            kanji2number("1万0万")
        with self.assertRaises(ValueError):
            kanji2number("1万.00009億")
        with self.assertRaises(ValueError):
            kanji2number("1億-2万")
        with self.assertRaises(ValueError):
            kanji2number("1万+2")
        with self.assertRaises(ValueError):
            kanji2number("千2e1")
        with self.assertRaises(ValueError):
            kanji2number("inf")

        self.assertEqual(0, kanji2number("〇"))
        self.assertEqual(404, kanji2number("四〇四"))
        self.assertEqual(1234, kanji2number("阡二百三拾四"))

    def test_number2kanji(self):
        self.assertEqual(number2kanji(1), "一", "all")
        self.assertEqual(number2kanji(10), "十", "all")
        self.assertEqual(number2kanji(11), "十一", "all")
        self.assertEqual(number2kanji(111), "百十一", "all")
        self.assertEqual(number2kanji(211), "二百十一", "all")
        self.assertEqual(number2kanji(121), "百二十一", "all")
        self.assertEqual(number2kanji(11), "十一", "all")
        self.assertEqual(number2kanji(111), "百十一", "all")
        self.assertEqual(number2kanji(211), "二百十一")
        self.assertEqual(number2kanji(121), "百二十一")
        self.assertEqual(number2kanji(1000), "千")
        self.assertEqual(number2kanji(1001), "千一")
        self.assertEqual(number2kanji(2025), "二千二十五")
        self.assertEqual(number2kanji(5807_6099), "五千八百七万六千九十九")

        # added 1.0.0
        self.assertEqual(number2kanji(1_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000), "一恒河沙")
        self.assertEqual(
            number2kanji(9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999),
            ("九千九百九十九無量大数九千九百九十九不可思議九千九百九十九那由多九千九百九十九阿僧祇九千九百九十九恒河沙九千九百九十九極"
             "九千九百九十九載九千九百九十九正九千九百九十九澗九千九百九十九溝九千九百九十九穣九千九百九十九𥝱九千九百九十九垓"
             "九千九百九十九京九千九百九十九兆九千九百九十九億九千九百九十九万九千九百九十九")
        )

        self.assertEqual("1", number2kanji(1, style="mixed"))
        self.assertEqual("10", number2kanji(10, style="mixed"))
        self.assertEqual("11", number2kanji(11, style="mixed"))
        self.assertEqual("121", number2kanji(121, style="mixed"))
        self.assertEqual("1千", number2kanji(1000, style="mixed"))
        self.assertEqual("1001", number2kanji(1001, style="mixed"))
        self.assertEqual("2025", number2kanji(2025, style="mixed"))
        self.assertEqual("5807万6099", number2kanji(5807_6099, style="mixed"))
        self.assertEqual("223兆4235億4256万6千", number2kanji(223_4235_4256_6000, style="mixed"))
        self.assertEqual("5千京", number2kanji(5000_0000_0000_0000_0000, style="mixed"))
        self.assertEqual("5000京", number2kanji(5000_0000_0000_0000_0000, style="mixed", kanji_thousand=False))
        self.assertEqual("39京4385兆4895万", number2kanji(39_4385_0000_4895_0000, style="mixed"))
        self.assertEqual("223兆4千億4256万6千", number2kanji(223_4000_4256_6000, style="mixed"))
        self.assertEqual("223兆4000億4256万6000", number2kanji(223_4000_4256_6000, style="mixed", kanji_thousand=False))

        # added 1.0.0
        self.assertEqual("1恒河沙", number2kanji(1_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000,
                                                 style="mixed", kanji_thousand=False))
        self.assertEqual(
            "9999無量大数9999不可思議9999那由多9999阿僧祇9999恒河沙9999極9999載9999正9999澗9999溝9999穣9999𥝱9999垓9999京9999兆9999億9999万9999",
            number2kanji(9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999,
                         style='mixed')
        )

        # added 1.2.0
        self.assertEqual(number2kanji(-1_5000_0000, style="mixed"), "-1億5千万")
        self.assertEqual(number2kanji(-25_0320, style="mixed"), "-25万320")
        self.assertEqual(number2kanji(-1_5025_0320, style="mixed"), "-1億5025万320")

        # added 1.4.0
        self.assertEqual(number2kanji(0), "零")

        # added 1.5.0
        self.assertEqual("弐佰拾壱",
                         number2kanji(211, config=KanjizeConfiguration(use_daiji=True)))
        self.assertEqual("-1億5025万320",
                         number2kanji(-1_5025_0320, config=KanjizeConfiguration(style=KanjizeStyle.MIXED)))
        self.assertEqual("-1億5千万320",
                         number2kanji(-1_5000_0320,
                                      config=KanjizeConfiguration(style=KanjizeStyle.MIXED, kanji_thousand=True)))
        self.assertEqual("-1億5阡萬320",
                         number2kanji(-1_5000_0320,
                                      config=KanjizeConfiguration(style=KanjizeStyle.MIXED, use_daiji=True,
                                                                  kanji_thousand=True)))
        self.assertEqual("六〇一",
                         number2kanji(601, config=KanjizeConfiguration(style=KanjizeStyle.FLAT,
                                                                       zero=KanjizeZero.SIGN)))
        self.assertEqual("六零一",
                         number2kanji(601, config=KanjizeConfiguration(style=KanjizeStyle.FLAT,
                                                                       zero=KanjizeZero.KANJI)))

    def test_number(self):
        self.assertEqual(12000, Number(2_7649_3734) - Number.from_kanji("2億7648万1734"))
        self.assertEqual(12734, Number(2_7649_3734) - Number.from_kanji("2億7648万1千"))
        self.assertEqual("2億7648万1734", (Number(2_7649_3734) - Number(1_2000)).to_kanji(style="mixed"))

        # added 1.4.0
        self.assertEqual(0, Number(0) * Number.from_kanji("2億7648万1千"))

        with self.assertRaises(ZeroDivisionError):
            Number(2) / Number(0)


if __name__ == "__main__":
    unittest.main()
