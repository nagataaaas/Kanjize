import enum
import math
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any
from typing import Optional


class KanjizeStyle(enum.Enum):
    ALL = "all"
    MIXED = "mixed"
    FLAT = "flat"


zero_kanji = "零"
zero_sign = "〇"


@dataclass(frozen=True)
class KanjiType:
    daiji: Any
    shoji: Any


DIGITS = KanjiType(
    {
        "壱": 1,
        "弐": 2,
        "参": 3,
        "肆": 4,
        "伍": 5,
        "陸": 6,
        "漆": 7,
        "捌": 8,
        "玖": 9,
    },
    {
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
    },
)
REVERSED_DIGITS = KanjiType(
    {v: k for k, v in DIGITS.daiji.items()},
    {v: k for k, v in DIGITS.shoji.items()},
)


class KanjizeZero(enum.Enum):
    KANJI = zero_kanji
    SIGN = zero_sign


class KanjizeConfiguration:
    def __init__(
            self,
            style: KanjizeStyle = KanjizeStyle.ALL,
            zero: Optional[KanjizeZero] = None,
            kanji_thousand: bool = True,
            use_daiji: bool = False,
    ):
        """

        Args:
            style: Which style of format will be used. `KanjizeStyle.MIXED`: Arabic and Kanji Mixed like "4億5230万3千", `KanjizeStyle.ALL`: All letter will be Kanji. `KanjizeStyle.FLAT`: each digit will be converted into Kanji like "六〇一"
            kanji_thousand: Whether you make a thousand to kanji. this will be used if style=`KanjizeStyle.MIXED`
            use_daiji: Whether you use Daiji (壱, 弐, 参, ..., 阡, 萬) instead of normal Kanji (一, 二, 三, ..., 千, 万)
            zero: Whether you use Kanji (零) or Sign (〇) for zero. this will be used if style=`KanjizeStyle.FLAT` or input is 0
        """
        self.style = style
        self._zero: KanjizeZero = zero or (
            KanjizeZero.SIGN if style is KanjizeStyle.FLAT else KanjizeZero.KANJI
        )
        self.kanji_thousand = kanji_thousand
        self.use_daiji = use_daiji

    @property
    def digits(self):
        return DIGITS.daiji if self.use_daiji else DIGITS.shoji

    @property
    def reversed_digits(self):
        return REVERSED_DIGITS.daiji if self.use_daiji else REVERSED_DIGITS.shoji

    @property
    def little_unit_by_value(self):
        if self.use_daiji:
            return {10: "拾", 100: "佰", 1000: "阡", 10000: "萬"}
        return {10: "十", 100: "百", 1000: "千", 10000: "万"}

    @property
    def unit_dict(self):
        return {
            "萬" if self.use_daiji else "万": 4,
            "億": 8,
            "兆": 12,
            "京": 16,
            "垓": 20,
            "𥝱": 24,
            "穣": 28,
            "溝": 32,
            "澗": 36,
            "正": 40,
            "載": 44,
            "極": 48,
            "恒河沙": 52,
            "阿僧祇": 56,
            "那由多": 60,
            "不可思議": 64,
            "無量大数": 68,
        }

    @property
    def zero(self) -> str:
        return self._zero.value

    @property
    def flat_table(self):
        return self._build_flat_table(self.use_daiji, self.zero)

    @classmethod
    @lru_cache(maxsize=None)
    def _build_flat_table(cls, use_daiji: bool, zero: str):
        return str.maketrans(
            (
                {
                    str(k): v
                    for k, v in (
                    REVERSED_DIGITS.daiji if use_daiji else REVERSED_DIGITS.shoji
                ).items()
                }
            )
            | {"0": zero}
        )


_default_config = KanjizeConfiguration()


def number2kanji(number: int, config: KanjizeConfiguration = _default_config) -> str:
    """
    :param number: [deprecated] Integer to convert into Kanji.
    :param config: KanjizeConfiguration
    :return: str
    """
    if number == 0:
        return config.zero

    units = ("", *config.unit_dict.keys())

    if not isinstance(number, int):
        number = int(number)

    is_negative = number < 0
    number = abs(number)

    result = ""  # all letters will be added to this
    if config.style is KanjizeStyle.ALL:
        digits = config.reversed_digits
        little_unit_by_value = config.little_unit_by_value
        for i in range(math.ceil(len(str(number)) / 4), -1, -1):
            c_num = (number // (10000 ** i)) % 10000
            if not c_num:
                continue

            c_str = ""
            thousands, c_num = divmod(c_num, 1000)
            hundreds, c_num = divmod(c_num, 100)
            tens, ones = divmod(c_num, 10)

            if thousands:
                if thousands > 1:
                    c_str += digits[thousands]
                c_str += little_unit_by_value[1000]
            if hundreds:
                if hundreds > 1:
                    c_str += digits[hundreds]
                c_str += little_unit_by_value[100]
            if tens:
                if tens > 1:
                    c_str += digits[tens]
                c_str += little_unit_by_value[10]
            if ones:
                c_str += digits[ones]

            if c_str:
                result += c_str + units[i]
    elif config.style is KanjizeStyle.MIXED:
        little_unit_by_value = config.little_unit_by_value
        for i in range(math.ceil(len(str(number)) / 4), -1, -1):
            c_num = (number // (10000 ** i)) % 10000
            if (
                    config.kanji_thousand and c_num >= 1000 and c_num % 1000 == 0
            ):  # If number is n * thousand
                result += f"{c_num // 1000}{little_unit_by_value[1000]}{units[i]}"
            elif c_num:
                result += str(c_num) + units[i]
    elif config.style is KanjizeStyle.FLAT:
        result = str(number).translate(config.flat_table)
    if is_negative:
        return f"-{result}"
    return result


def kanji2number(kanjis: str) -> int:
    """
    :param kanjis: Kanji str to convert into Integer
    :return: int
    """
    if not kanjis:
        raise ValueError("Kanji is empty")

    if kanjis in (zero_sign, zero_kanji):
        return 0

    given = kanjis
    is_negative = kanjis[0] in "-－⁻"
    if is_negative or kanjis[0] in "+＋⁺₊+":
        kanjis = kanjis[1:]
    result = _kanji2number(given, kanjis)
    return result * -1 if is_negative else result


short_regex = re.compile(
    r"(?:(.*?)({}))?(.*)".format("|".join(_default_config.unit_dict.keys()))
)
default_unit_dict = _default_config.unit_dict
unit_regex = re.compile("|".join(default_unit_dict.keys()))


def _kanji2number(given: str, kanjis: str) -> int:
    """Internal function. Converts kanji str without sign to the number.
    This calls itself recursively.

    :param given: Original kanji str to be converted finally
    :param kanjis: Kanji str to be converted
    :return: the value of kanjis and the name of the most significant unit
    :rtype: int
    :raises ValueError: if the value of kanjis is invalid as number
    """

    result = 0
    min_unit: int | None = None

    while kanjis:
        left_val, left_unit, kanjis = short_regex.match(kanjis).groups()

        if left_unit and not left_val:
            raise ValueError(
                f"Kanji `{given}` seems to be invalid. `{left_unit}` needs any leading number."
            )

        if (
                min_unit
                and left_unit
                and default_unit_dict[min_unit] <= default_unit_dict[left_unit]
        ):
            raise ValueError(
                f"Kanji `{given}` seems to be invalid. `{min_unit}` is followed by too large unit `{left_unit}`."
            )

        if left_val or left_unit:
            base_unit = default_unit_dict[left_unit] if left_unit else 0
            fragment_value = parse_short(left_val, base_unit)
        elif kanjis:
            fragment_value = parse_short(kanjis)
            kanjis = ""
        else:
            break

        if min_unit and fragment_value >= 10 ** default_unit_dict[min_unit]:
            raise ValueError(
                f"Kanji `{given}` seems to be invalid. `{left_unit}` is followed by too large number `{left_val}`."
            )

        result += fragment_value

        min_unit = left_unit

    return result


number_dict = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "壱": 1,
    "弐": 2,
    "参": 3,
    "肆": 4,
    "伍": 5,
    "陸": 6,
    "漆": 7,
    "捌": 8,
    "玖": 9,
    "零": 0,
    "〇": 0,
}

number_dict_table = str.maketrans({k: str(v) for k, v in number_dict.items()})
little_units = "十百千拾陌佰阡仟萬"
short_validation_regex = re.compile(
    rf"[.\d{little_units}{''.join(number_dict.keys())}]+"
)
short_parser_regex = re.compile(
    r"(?:(.*?)[千阡仟])?(?:(.*?)[陌佰百])?(?:(.*?)[十拾])?(.+)?"
)


def parse_short(kanji: Optional[str], base_unit: int = 0) -> int:
    """
    :param kanji: Kanji str to convert into Integer
    :param base_unit: multiply by 10 ** base_unit
    :return: int
    """
    if not kanji:
        return 0

    if not short_validation_regex.fullmatch(kanji):
        raise ValueError(f"Kanji `{kanji}` seems to be invalid.")

    thousand, hundred, ten, one = short_parser_regex.match(kanji).groups()
    result = 0
    left_unit = 0
    for v, unit in ([thousand, 1000], [hundred, 100], [ten, 10], [one, 1]):
        if v is None:
            continue
        elif v == "":
            v = 1
        else:
            try:
                v = (float if "." in v else int)(v.translate(number_dict_table))
            except ValueError:
                raise ValueError(f"Kanji `{kanji}` seems to be invalid.")

        if left_unit and left_unit <= v * unit:
            raise ValueError(
                f"Kanji `{kanji}` seems to be invalid. Unit `{left_unit}` is followed by too large number `{v}`."
            )
        left_unit = unit

        result += v * unit

    return int(result * 10 ** base_unit)


class Number(int):
    @classmethod
    def from_kanji(cls, kanjis: str):
        return cls(kanji2number(kanjis=kanjis))

    def to_kanji(
            self,
            config: KanjizeConfiguration = _default_config,
    ):
        return number2kanji(
            number=int(self),
            config=config,
        )

    def __add__(self, other):
        return Number(int.__add__(self, other))

    def __sub__(self, other):
        return Number(int.__sub__(self, other))

    def __mul__(self, other):
        return Number(int.__mul__(self, other))

    def __floordiv__(self, other):
        return Number(int.__floordiv__(self, other))

    def __mod__(self, other):
        return Number(int.__mod__(self, other))

    def __pow__(self, power, modulo=None):
        return Number(int.__pow__(self, power, modulo))

    def __and__(self, other):
        return Number(int.__and__(self, other))

    def __or__(self, other):
        return Number(int.__or__(self, other))

    def __xor__(self, other):
        return Number(int.__xor__(self, other))

    def __lshift__(self, other):
        return Number(int.__lshift__(self, other))

    def __rshift__(self, other):
        return Number(int.__rshift__(self, other))

    def __repr__(self):
        return f"Number<{int(self)}>"
