import math
import re
import warnings
from decimal import Decimal, DecimalException
from typing import Optional


def int2kanji(number: int, error="raise", style="all", kanji_thousand=True) -> str:
    """
    :param number: Integer to convert into Kanji
    :param error: How to handle Error. "raise": raise error. "ignore": ignore error , "warn": warn but don't raise
    :param style: Which style of format will be used. "mixed": Arabic and Kanji Mixed like "4億5230万3千", "all": All letter will be Kanji.
    :param kanji_thousand: Whether you make a thousand to kanji. this will be used if style="mixed"
    :return: str
    """
    if error not in ("raise", "warn", "ignore"):
        raise ValueError("unexpected value {} for argument error".format(error))
    if style not in ("all", "mixed"):
        raise ValueError("unexpected value {} for argument style".format(style))  # check arguments

    kanji = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    digits = (
        '', '万', '億', '兆', '京', '垓', '𥝱', '穣', '溝', '澗', '正', '載', '極', '恒河沙', '阿僧祇', '那由多',
        '不可思議',
        '無量大数')

    negative = number < 0
    number = abs(number)

    if style == "all":
        result = ""  # all letters will be added to this

        for i in range(math.ceil(math.log(number, 1000)), -1, -1):
            c_num = str((number % (10 ** ((i + 1) * 4))) // (10 ** (i * 4))).zfill(4)  # remainder
            c_str = ""
            if c_num == "0000":
                continue
            if c_num[0] > "0":  # 1st digit
                if c_num[0] != "1":
                    c_str += kanji[int(c_num[0])]
                c_str += "千"
            if c_num[1] > "0":  # 2nd digit
                if c_num[1] != "1":
                    c_str += kanji[int(c_num[1])]
                c_str += "百"
            if c_num[2] > "0":  # 3rd digit
                if c_num[2] != "1":
                    c_str += kanji[int(c_num[2])]
                c_str += "十"
            if c_num[3] > "0":  # 4th digit
                c_str += kanji[int(c_num[3])]
            if c_str:
                result += c_str + digits[i]

    elif style == "mixed":
        result = ""  # all letters will be added to this

        for i in range(math.ceil(math.log(number, 1000)), -1, -1):
            c_num = (number % (10 ** ((i + 1) * 4))) // (10 ** (i * 4))  # reminder
            c_str = ""
            if kanji_thousand and c_num // 1000 == c_num / 1000 and c_num // 1000:  # If number is n * thousand
                c_str += str(c_num).zfill(4)[-4] + "千"
            elif c_num:
                c_str = str(c_num)
            if c_str:
                result += c_str + digits[i]
    if negative:
        result = f'-{result}'
    return result


def kanji2int(kanjis: str, error="raise", style="auto") -> int:
    """
    :param kanjis: Kanji str to convert into Integer
    :param error: How to handle Error. "raise": raise error. "ignore": ignore error , "warn": warn but don't raise
    :param style: Which style of format will be used. "mixed": Arabic and Kanji Mixed like "4億5230万3千", "all": All letter must be Kanji, "auto": detect automatically by checking any arabic character is in kanjis.
    :return: int
    """
    warnings.warn("`kanji2int` is deprecated. consider using `kanji2number` instead", DeprecationWarning)
    given = kanjis
    if error not in ("raise", "warn", "ignore"):
        raise ValueError("unexpected value {} for argument error".format(error))
    number_dict = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    little_digit_dict = {"十": 1, "百": 2, "千": 3}
    digit_dict = {"万": 4, "億": 8, "兆": 12, "京": 16, "垓": 20, "𥝱": 24, "穣": 28, "溝": 32, "澗": 36, "正": 40,
                  "載": 44, "極": 48, "恒河沙": 52, "阿僧祇": 56, "那由多": 60, "不可思議": 64, "無量大数": 68}

    if style not in ("all", "mixed", "auto"):
        raise ValueError("unexpected value {} for argument style".format(style))  # check arguments

    negative = False
    if kanjis[0] in '-－⁻':
        negative = True
        kanjis = kanjis[1:]
    elif kanjis[0] in '+＋⁺₊+':
        kanjis = kanjis[1:]

    result = 0
    if style == "mixed" or (style == "auto" and any(str(num) in kanjis for num in range(10))):
        while kanjis:
            value = 0
            while kanjis:
                left_value = re.compile(rf'(^\d*)(\.\d+)?([千百十]?)(.*)').search(kanjis)

                current, float_number, little_digit, kanjis = left_value.groups()
                head = re.match(r'{}'.format('|'.join(digit_dict.keys())), kanjis)

                if kanjis and not any([current, float_number, little_digit, head]):
                    if error == "raise":
                        raise ValueError(f"Kanji `{given}` seems not to be a valid kanji number.")
                    elif error == "warn":
                        warnings.warn(f"Kanji `{given}` seems not to be a valid kanji number.")
                    return result

                current = int(current or 1)
                if float_number:
                    current += float(float_number)
                if little_digit:
                    current *= 10 ** little_digit_dict[little_digit]
                value += current

                if not kanjis or head:
                    digit = head.group(0) if kanjis else ''
                    result += value * 10 ** digit_dict.get(digit, 0)
                    value = 0
                    kanjis = kanjis[len(digit):]
    else:
        current_mini_num = 0
        current_num = 0
        for word in re.compile(
                '|'.join(list(number_dict.keys()) + list(little_digit_dict.keys()) + list(digit_dict.keys()))) \
                .findall(kanjis):
            if word in number_dict:
                current_mini_num = number_dict[word]
            elif word in little_digit_dict:
                current_num += (current_mini_num if current_mini_num else 1) * 10 ** little_digit_dict[word]
                current_mini_num = 0
            elif word in digit_dict:
                result += (current_num + current_mini_num) * 10 ** digit_dict[word]
                current_num = current_mini_num = 0
            else:
                if error == "raise":
                    raise ValueError("unexpected letter: {}".format(word))
                elif error == "warn":
                    warnings.warn("unexpected letter: {}".format(word))
                return result
        result += current_num + current_mini_num

    return -result if negative else result


def kanji2number(kanjis: str) -> float:
    """
    :param kanjis: Kanji str to convert into Integer
    :return: float
    """
    given = kanjis
    digit_dict = {"万": 4, "億": 8, "兆": 12, "京": 16, "垓": 20, "𥝱": 24, "穣": 28, "溝": 32, "澗": 36, "正": 40,
                  "載": 44, "極": 48, "恒河沙": 52, "阿僧祇": 56, "那由多": 60, "不可思議": 64, "無量大数": 68}

    negative = False
    if kanjis[0] in '-－⁻':
        negative = True
        kanjis = kanjis[1:]
    elif kanjis[0] in '+＋⁺₊+':
        kanjis = kanjis[1:]

    match = re.compile(r'(?:(.+?)({}))?(.*)'.format('|'.join(digit_dict.keys()))).match(kanjis)
    left_val, left_digit, kanjis = match.groups()

    if left_digit and not left_val:
        raise ValueError(f"Kanji `{given}` seems to be invalid. `{left_digit}` is not followed by any number.")

    base_digit = digit_dict[left_digit] if left_digit else 0
    result = parse_short(left_val, base_digit)

    if re.search('|'.join(digit_dict.keys()), kanjis):
        result += kanji2number(kanjis)
    else:
        result += parse_short(kanjis)

    return result * -1 if negative else result


def parse_short(kanji: Optional[str], base_digit: int = 0) -> float:
    """
    :param kanji: Kanji str to convert into Integer
    :param base_digit: multiply by 10 ** base_digit
    :return: int
    """
    if not kanji:
        return 0
    number_dict = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    little_digit_dict = {"十": 1, "百": 2, "千": 3}
    if not re.compile(r'[.\d{}{}]'.format(''.join(little_digit_dict.keys()),
                                          ''.join(number_dict.keys()))).match(kanji):
        raise ValueError(f"Kanji `{kanji}` seems to be invalid.")
    match = re.compile(r'(?:(.*)(?:千))?(?:(.*)(?:百))?(?:(.*)(?:十))?(.+)?').match(kanji)

    thousand, hundred, ten, one = match.groups()
    result = 0
    for v, digit in ([thousand, 1000], [hundred, 100], [ten, 10], [one, 1]):
        if v is None:
            continue
        if v == '':
            v = 1
        try:
            v = Decimal(v)
        except DecimalException:
            v = number_dict.get(v, None)
            if v is None:
                raise ValueError(f"Kanji `{kanji}` seems to be invalid.")
            v = Decimal(v)
        result += v * digit
    int_, *float_ = str(result).split('.')
    result *= 10 ** base_digit

    if float_ and len(float_[0]) > base_digit:
        return float(result)
    return int(result)


class Number(int):
    @classmethod
    def from_kanji(cls, kanjis: str):
        return cls(kanji2number(kanjis=kanjis))

    def to_kanji(self, error="raise", style="all", kanji_thousand=True):
        return int2kanji(number=int(self), error=error, style=style, kanji_thousand=kanji_thousand)

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
        return "Number<{}>".format(int(self))
