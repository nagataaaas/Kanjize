import enum
import math
import re
import warnings
from decimal import Decimal, DecimalException
from typing import Optional


class KanjizeStyle(enum.Enum):
    ALL = "all"
    MIXED = "mixed"
    FLAT = "flat"


zero_kanji = "零"
zero_sign = "〇"


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
        if self.use_daiji:
            return {
                "壱": 1,
                "弐": 2,
                "参": 3,
                "肆": 4,
                "伍": 5,
                "陸": 6,
                "漆": 7,
                "捌": 8,
                "玖": 9,
            }
        return {
            "一": 1,
            "二": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9,
        }

    @property
    def little_units(self):
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


_default_config = KanjizeConfiguration()


def number2kanji(
    number: int,
    error: Optional[str] = None,
    style: Optional[str] = None,
    kanji_thousand: Optional[bool] = None,
    config: Optional[KanjizeConfiguration] = None,
) -> str:
    """
    :param number: [deprecated] Integer to convert into Kanji.
    :param error: [deprecated] How to handle Error. "raise": raise error. "ignore": ignore error , "warn": warn but don't raise
    :param style: [deprecated] Which style of format will be used. "mixed": Arabic and Kanji Mixed like "4億5230万3千", "all": All letter will be Kanji.
    :param kanji_thousand: [deprecated] Whether you make a thousand to kanji. this will be used if style="mixed"
    :param config: KanjizeConfiguration
    :return: str
    """
    if config is None:
        config = KanjizeConfiguration()

    if (error or style or kanji_thousand) is not None:
        warnings.warn(
            "`error`, `style` and `kanji_thousand` arguments are deprecated. use config instead",
            DeprecationWarning,
        )
    if error is not None:
        if error not in ("raise", "warn", "ignore"):
            raise ValueError(f"unexpected value `{error}` for argument error")
    if style is not None:
        if style not in ("all", "mixed"):
            raise ValueError(f"unexpected value `{style}` for argument style")
        config.style = KanjizeStyle(style)
    if kanji_thousand is not None:
        if not isinstance(kanji_thousand, bool):
            raise ValueError(
                f"unexpected value `{kanji_thousand}` for argument kanji_thousand"
            )
        config.kanji_thousand = kanji_thousand

    if number == 0:
        return config.zero

    digits = {v: k for k, v in config.digits.items()}
    units = ("", *config.unit_dict.keys())

    is_negative = number < 0
    number = abs(number)

    if config.style is KanjizeStyle.ALL:
        result = ""  # all letters will be added to this

        for i in range(math.ceil(math.log(number, 1000)), -1, -1):
            c_num = str((number % (10 ** ((i + 1) * 4))) // (10 ** (i * 4))).zfill(
                4
            )  # remainder
            c_str = ""
            if c_num == "0000":
                continue

            if c_num[0] != "0":  # thousands
                if c_num[0] != "1":
                    c_str += digits[int(c_num[0])]
                c_str += config.little_units[1000]
            if c_num[1] != "0":  # hundreds
                if c_num[1] != "1":
                    c_str += digits[int(c_num[1])]
                c_str += config.little_units[100]
            if c_num[2] != "0":  # tens
                if c_num[2] != "1":
                    c_str += digits[int(c_num[2])]
                c_str += config.little_units[10]
            if c_num[3] != "0":  # ones
                c_str += digits[int(c_num[3])]

            if c_str:
                result += c_str + units[i]

    elif config.style is KanjizeStyle.MIXED:
        result = ""  # all letters will be added to this

        for i in range(math.ceil(math.log(number, 1000)), -1, -1):
            c_num = (number % (10 ** ((i + 1) * 4))) // (10 ** (i * 4))  # reminder
            c_str = ""
            if (
                config.kanji_thousand and c_num >= 1000 and c_num % 1000 == 0
            ):  # If number is n * thousand
                c_str += str(c_num).zfill(4)[-4] + config.little_units[1000]
            elif c_num:
                c_str = str(c_num)
            if c_str:
                result += c_str + units[i]
    elif config.style is KanjizeStyle.FLAT:
        table = str.maketrans(
            {str(v): k for k, v in config.digits.items()} | {str(0): config.zero}
        )
        result = str(number).translate(table)
    if is_negative:
        result = f"-{result}"
    return result


def kanji2number(kanjis: str) -> float:
    """
    :param kanjis: Kanji str to convert into Integer
    :return: float
    """
    if not kanjis:
        raise ValueError("Kanji is empty")

    if kanjis in (zero_sign, zero_kanji):
        return 0

    given = kanjis
    is_negative = kanjis[0] in "-－⁻"
    if kanjis[0] in "-－⁻+＋⁺₊+":
        kanjis = kanjis[1:]
    result = _kanji2number(given, kanjis)[0]
    return result * -1 if is_negative else result


def _kanji2number(given: str, kanjis: str) -> (float, str):
    """Internal function. Converts kanji str without sign to the number.
    This calls itself recursively.

    :param given: Original kanji str to be converted finally
    :param kanjis: Kanji str to be converted
    :return: the value of kanjis and the name of the most significant unit
    :rtype: (float, str)
    :raises ValueError: if the value of kanjis is invalid as number
    """

    match = re.compile(
        r"(?:(.*?)({}))?(.*)".format("|".join(_default_config.unit_dict.keys()))
    ).match(kanjis)
    left_val, left_unit, kanjis = match.groups()

    if left_unit and not left_val:
        raise ValueError(
            f"Kanji `{given}` seems to be invalid. `{left_unit}` needs any leading number."
        )

    base_unit = _default_config.unit_dict[left_unit] if left_unit else 0
    result = parse_short(left_val, base_unit)

    if re.search("|".join(_default_config.unit_dict.keys()), kanjis):
        fraction, unit = _kanji2number(given, kanjis)
        if base_unit <= _default_config.unit_dict[unit]:
            raise ValueError(
                f"Kanji `{given}` seems to be invalid. `{left_unit}` is followed by too large unit `{unit}`."
            )
    else:
        fraction = parse_short(kanjis)

    if base_unit and 10**base_unit <= fraction:
        raise ValueError(
            f"Kanji `{given}` seems to be invalid. `{left_unit}` is followed by too large number `{kanjis}`."
        )

    return result + fraction, left_unit


def parse_short(kanji: Optional[str], base_unit: int = 0) -> float:
    """
    :param kanji: Kanji str to convert into Integer
    :param base_unit: multiply by 10 ** base_unit
    :return: int
    """
    if not kanji:
        return 0
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

    if not re.compile(
        r"[.\d{}{}]+$".format(little_units, "".join(number_dict.keys()))
    ).match(kanji):
        raise ValueError(f"Kanji `{kanji}` seems to be invalid.")
    match = re.compile(r"(?:(.*)[千阡仟])?(?:(.*)[陌佰百])?(?:(.*)[十拾])?(.+)?").match(
        kanji
    )

    thousand, hundred, ten, one = match.groups()
    result = 0
    left_unit = 0
    for v, unit in ([thousand, 1000], [hundred, 100], [ten, 10], [one, 1]):
        if v is None:
            continue
        elif v == "":
            v = Decimal(1)
        else:
            try:
                v = Decimal(v.translate(number_dict_table))
            except DecimalException:
                raise ValueError(f"Kanji `{kanji}` seems to be invalid.")

        if left_unit and left_unit <= v * unit:
            raise ValueError(
                f"Kanji `{kanji}` seems to be invalid. Unit `{left_unit}` is followed by too large number `{v}`."
            )
        left_unit = unit

        result += v * unit
    int_, *float_ = str(result).split(".")
    result *= 10**base_unit

    if float_ and len(float_[0]) > base_unit:
        return float(result)
    return int(result)


class Number(int):
    @classmethod
    def from_kanji(cls, kanjis: str):
        return cls(kanji2number(kanjis=kanjis))

    def to_kanji(
        self,
        error: Optional[str] = None,
        style: Optional[str] = None,
        kanji_thousand: Optional[bool] = None,
        config: Optional[KanjizeConfiguration] = None,
    ):
        return number2kanji(
            number=int(self),
            error=error,
            style=style,
            kanji_thousand=kanji_thousand,
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
