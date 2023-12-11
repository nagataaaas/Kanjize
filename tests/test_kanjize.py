import pytest

from kanjize import (
    number2kanji,
    kanji2number,
    Number,
    KanjizeConfiguration,
    KanjizeZero,
    KanjizeStyle,
)


class TestKanjize:
    """
    test class of kanjize
    """

    def test_kanji2number(self):
        assert 1 == kanji2number("一")
        assert 10 == kanji2number("十")
        assert 11 == kanji2number("十一")
        assert 111 == kanji2number("百十一")
        assert 211 == kanji2number("二百十一")
        assert 121 == kanji2number("百二十一")
        assert 11 == kanji2number("十一")
        assert 111 == kanji2number("百十一")
        assert 211 == kanji2number("二百十一")
        assert 121 == kanji2number("百二十一")
        assert 1_000 == kanji2number("千")
        assert 1_001 == kanji2number("千一")
        assert 2_025 == kanji2number("二千二十五")
        assert 58_076_099 == kanji2number("五千八百七万六千九十九")

        # added 1.0.0
        assert (
                10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000
                == kanji2number("一恒河沙")
        )
        assert (
                9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999
                == kanji2number(
            "九千九百九十九無量大数九千九百九十九不可思議九千九百九十九那由多九千九百九十九阿僧祇九千九百九十九恒河沙九千九百九十九極"
            "九千九百九十九載九千九百九十九正九千九百九十九澗九千九百九十九溝九千九百九十九穣九千九百九十九𥝱九千九百九十九垓"
            "九千九百九十九京九千九百九十九兆九千九百九十九億九千九百九十九万九千九百九十九"
        )
        )

        assert 1 == kanji2number("1")
        assert 10 == kanji2number("10")
        assert 11 == kanji2number("11")
        assert 121 == kanji2number("121")
        assert 1000 == kanji2number("1千")
        assert 1001 == kanji2number("1001")
        assert 2025 == kanji2number("2025")
        assert 5807_6099 == kanji2number("5807万6099")
        assert 223_4235_4256_6000 == kanji2number("223兆4235億4256万6千")
        assert 223_4000_4256_6000 == kanji2number("223兆4千億4256万6千")
        assert 5000_0000_0000_0000_0000 == kanji2number("5千京")
        assert 39_4385_0000_4895_0000 == kanji2number("39京4385兆4895万")

        # added 0.2.1
        assert 1001 == kanji2number("千1")
        assert 2025 == kanji2number("2千2十5")
        assert 400_0000 == kanji2number("4百万")
        assert 5807_6099 == kanji2number("58百7万6千99")
        assert 223_4235_4256_6000 == kanji2number("2百23兆4千2百3十5億4256万6千")
        assert 223_4000_4256_6000 == kanji2number("223兆4千億4256万6千")
        assert 223_4000_4256_6000 == kanji2number("2234千億4256万6千")
        assert 5050_0000_0000_0000_0000 == kanji2number("5千5十京")
        assert 39_4385_0000_4895_0000 == kanji2number("39京4385兆4895万")

        # added 1.0.0
        assert (
                10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000
                == kanji2number("1恒河沙")
        )
        assert (
                999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999_999
                == kanji2number(
            "9999無量大数9999不可思議9999那由多9999阿僧祇"
            "9999恒河沙9999極9999載9999正9999澗9999溝9999穣"
            "9999𥝱9999垓9999京9999兆9999億9999万9999"
        )
        )

        # added 1.1.0
        assert 1_5000_0000 == kanji2number("1.5億")
        assert 25_0320 == kanji2number("250.32千")
        assert 1_5025_0320 == kanji2number("1.5億250.32千")

        # added 1.2.0
        assert -1_5000_0000 == kanji2number("-1.5億")
        assert -25_0320 == kanji2number("-250.32千")
        assert -1_5025_0320 == kanji2number("-1.5億250.32千")

        assert 1234 == kanji2number("一千二百三十四")
        assert 1234 == kanji2number("千二百三十四")

        # added 1.4.0
        assert 0 == kanji2number("零")

        # added 1.5.0
        assert 12345 == kanji2number("12千345")
        with pytest.raises(ValueError):
            kanji2number("1千1000")
        with pytest.raises(ValueError):
            kanji2number("1万10千")
        with pytest.raises(ValueError):
            kanji2number("万1千234")
        with pytest.raises(ValueError):
            kanji2number("1万0万")
        with pytest.raises(ValueError):
            kanji2number("1万.00009億")
        with pytest.raises(ValueError):
            kanji2number("1億-2万")
        with pytest.raises(ValueError):
            kanji2number("1万+2")
        with pytest.raises(ValueError):
            kanji2number("千2e1")
        with pytest.raises(ValueError):
            kanji2number("inf")

        assert 0 == kanji2number("〇")
        assert 404 == kanji2number("四〇四")
        assert 1234 == kanji2number("阡二百三拾四")
        assert 601 == kanji2number("六〇一")
        assert 601 == kanji2number("六零一")

    def test_number2kanji(self):
        assert number2kanji(1) == "一"
        assert number2kanji(10) == "十"
        assert number2kanji(11) == "十一"
        assert number2kanji(111) == "百十一"
        assert number2kanji(211) == "二百十一"
        assert number2kanji(121) == "百二十一"
        assert number2kanji(11) == "十一"
        assert number2kanji(111) == "百十一"
        assert number2kanji(211) == "二百十一"
        assert number2kanji(121) == "百二十一"
        assert number2kanji(1000) == "千"
        assert number2kanji(1001) == "千一"
        assert number2kanji(2025) == "二千二十五"
        assert number2kanji(5807_6099) == "五千八百七万六千九十九"

        # added 1.0.0
        assert (
                number2kanji(
                    1_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000
                )
                == "一恒河沙"
        )
        assert number2kanji(
            9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999
        ) == (
                   "九千九百九十九無量大数九千九百九十九不可思議九千九百九十九那由多九千九百九十九阿僧祇九千九百九十九恒河沙九千九百九十九極"
                   "九千九百九十九載九千九百九十九正九千九百九十九澗九千九百九十九溝九千九百九十九穣九千九百九十九𥝱九千九百九十九垓"
                   "九千九百九十九京九千九百九十九兆九千九百九十九億九千九百九十九万九千九百九十九"
               )

        assert "1" == number2kanji(1, style="mixed")
        assert "10" == number2kanji(10, style="mixed")
        assert "11" == number2kanji(11, style="mixed")
        assert "121" == number2kanji(121, style="mixed")
        assert "1千" == number2kanji(1000, style="mixed")
        assert "1001" == number2kanji(1001, style="mixed")
        assert "2025" == number2kanji(2025, style="mixed")
        assert "5807万6099" == number2kanji(5807_6099, style="mixed")
        assert "223兆4235億4256万6千" == number2kanji(223_4235_4256_6000, style="mixed")
        assert "5千京" == number2kanji(5000_0000_0000_0000_0000, style="mixed")
        assert "5000京" == number2kanji(
            5000_0000_0000_0000_0000, style="mixed", kanji_thousand=False
        )
        assert "39京4385兆4895万" == number2kanji(39_4385_0000_4895_0000, style="mixed")
        assert "223兆4千億4256万6千" == number2kanji(223_4000_4256_6000, style="mixed")
        assert "223兆4000億4256万6000" == number2kanji(
            223_4000_4256_6000, style="mixed", kanji_thousand=False
        )

        # added 1.0.0
        assert "1恒河沙" == number2kanji(
            1_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000,
            style="mixed",
            kanji_thousand=False,
        )
        assert (
                "9999無量大数9999不可思議9999那由多9999阿僧祇9999恒河沙9999極9999載9999正9999澗9999溝9999穣9999𥝱9999垓9999京9999兆9999億9999万9999"
                == number2kanji(
            9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999_9999,
            style="mixed",
        )
        )

        # added 1.2.0
        assert number2kanji(-1_5000_0000, style="mixed") == "-1億5千万"
        assert number2kanji(-25_0320, style="mixed") == "-25万320"
        assert number2kanji(-1_5025_0320, style="mixed") == "-1億5025万320"

        # added 1.4.0
        assert number2kanji(0) == "零"

        # added 1.5.0
        assert "弐佰拾壱" == number2kanji(
            211, config=KanjizeConfiguration(use_daiji=True)
        )
        assert "-1億5025万320" == number2kanji(
            -1_5025_0320, config=KanjizeConfiguration(style=KanjizeStyle.MIXED)
        )
        assert "-1億5千万320" == number2kanji(
            -1_5000_0320,
            config=KanjizeConfiguration(style=KanjizeStyle.MIXED, kanji_thousand=True),
        )
        assert "-1億5阡萬320" == number2kanji(
            -1_5000_0320,
            config=KanjizeConfiguration(
                style=KanjizeStyle.MIXED, use_daiji=True, kanji_thousand=True
            ),
        )
        assert "六〇一" == number2kanji(
            601,
            config=KanjizeConfiguration(style=KanjizeStyle.FLAT, zero=KanjizeZero.SIGN),
        )
        assert "六零一" == number2kanji(
            601,
            config=KanjizeConfiguration(
                style=KanjizeStyle.FLAT, zero=KanjizeZero.KANJI
            ),
        )

    def test_number(self):
        assert 12000 == Number(2_7649_3734) - Number.from_kanji("2億7648万1734")
        assert 12734 == Number(2_7649_3734) - Number.from_kanji("2億7648万1千")
        assert "2億7648万1734" == (Number(2_7649_3734) - Number(1_2000)).to_kanji(
            style="mixed"
        )

        # added 1.4.0
        assert 0 == Number(0) * Number.from_kanji("2億7648万1千")

        with pytest.raises(ZeroDivisionError):
            Number(2) / Number(0)


if __name__ == "__main__":
    pytest.main()
