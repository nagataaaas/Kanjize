import re
import itertools
from warnings import warn


def int2kanji(number, error="raise", style="all", kanji_thousand=True):
    """
    :param number - int: Integer to convert into Kanji
    :param error - str: How to handle Error. "raise": raise error. "ignore": ignore error , "warn": warn but don't raise
    :param style - str: Which style of format will be used. "mixed": Arabic and Kanji Mixed like "4億5230万3千", "all": All letter will be Kanji.
    :param kanji_thousand - bool: Whether make thousand to kanji. this will be used if style="mixed"
    :return: str
    """
    if error not in ("raise", "warn", "ignore"):
        raise ValueError("unexpected value {} for argument error".format(error))
    if style not in ("all", "mixed"):
        raise ValueError("unexpected value {} for argument style".format(style))  # check arguments

    kanji = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    digits = ("", "万", "億", "兆", "京", "垓", "𥝱")

    if number >= 10 ** 28:  # check number limit
        if error == "raise":
            raise ValueError("{} ( >= 10 ** 28) is too big to this function".format(number))
        elif error == "warn":
            warn("{} ( >= 10 ** 28) is too big to this function\npart that is too big will be ignored".format(number))

    if style == "all":
        res = ""  # all letters will be added to this

        for i in range(6, -1, -1):
            c_num = str((number % (10 ** ((i + 1) * 4))) // (10 ** (i * 4))).zfill(4)  # reminder
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
                res += c_str + digits[i]
        return res

    elif style == "mixed":
        res = ""  # all letters will be added to this

        for i in range(6, -1, -1):
            c_num = (number % (10 ** ((i + 1) * 4))) // (10 ** (i * 4))  # reminder
            c_str = ""
            if kanji_thousand and c_num // 1000 == c_num / 1000 and c_num // 1000:  # If number is n * thousand
                c_str += str(c_num).zfill(4)[-4] + "千"
            elif c_num:
                c_str = str(c_num)
            if c_str:
                res += c_str + digits[i]
        return res


def kanji2int(kanjis, error="raise", style="auto"):
    """
    :param kanjis - str: Kanji str to convert into Integer
    :param error - str: How to handle Error. "raise": raise error. "ignore": ignore error , "warn": warn but don't raise
    :param style - str: Which style of format will be used. "mixed": Arabic and Kanji Mixed like "4億5230万3千", "all": All letter will be Kanji, "auto": detect automatically by checking any arabic character is in kanjis.
    :return: int
    """
    if error not in ("raise", "warn", "ignore"):
        raise ValueError("unexpected value {} for argument error".format(error))
    kanji = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10, "百": 100, "千": 1000,
             "万": 10 ** 4, "億": 10 ** 8, "兆": 10 ** 12, "京": 10 ** 16, "垓": 10 ** 20, "𥝱": 10 ** 24}
    digits = ("十", "百", "千", "万", "億", "兆", "京", "垓", "𥝱")
    if style not in ("all", "mixed", "auto"):
        raise ValueError("unexpected value {} for argument style".format(style))  # check arguments

    num = 0
    c_num = 0
    c_digit = 0
    dig = "𥝱"
    if style == "mixed" or (style == "auto" and any(str(num) in kanjis for num in range(10))):
        for spl in re.compile("[0-9]+千?[万億兆京垓]?").findall(kanjis):
            c_num = int("".join(filter(str.isdecimal, spl)))
            c_digit = 1
            for dig in itertools.filterfalse(str.isdecimal, spl):
                c_digit *= kanji[dig]
            num += c_num * c_digit
        return num
    else:
        for word in kanjis:
            try:
                if word in digits:
                    if kanji[word] >= kanji[dig]:
                        num += (c_num + c_digit) * kanji[word]
                        c_num, c_digit = 0, 0
                    elif c_digit:
                        c_num += c_digit * kanji[word]
                        c_digit = 0
                    else:
                        c_num += kanji[word]
                    dig = word
                else:
                    c_digit += kanji[word]
            except KeyError:
                if error == "raise":
                    raise ValueError("unexpected letter")
                elif error == "warn":
                    warn("unexpected letter")
        return num + c_num + c_digit


class Number(int):
    @classmethod
    def from_kanji(cls, kanjis, error="raise", style="auto"):
        return cls(kanji2int(kanjis=kanjis, error=error, style=style))

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
