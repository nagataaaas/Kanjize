from warnings import warn


def int2kanji(number, error="raise"):
    """
    :param number - int: Integer to convert into Kanji
    :param error - str: How to handle Error. "raise": raise error. "ignore": ignore error , "warn": warn but don't raise
    :return: str
    """
    if error not in ("raise", "warn", "ignore"):
        raise ValueError("unexpected value {} for argument error".format(error))

    kanji = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    digits = ("", "万", "億", "兆", "京", "垓", "𥝱")

    if number >= 10 ** 28:
        if error == "raise":
            raise ValueError("{} ( >= 10 ** 28) is too big to this function".format(number))
        elif error == "warn":
            warn("{} ( >= 10 ** 28) is too big to this function\npart that is too big will be ignored".format(number))

    res = ""

    for i in range(6, -1, -1):
        add_dig = False
        c_num = str((number % (10 ** ((i + 1) * 4))) // (10 ** (i * 4))).zfill(4)
        c_str = ""
        if c_num[0] > "0":
            add_dig = True
            if c_num[0] != "1":
                c_str += kanji[int(c_num[0])]
            c_str += "千"
        if c_num[1] > "0":
            add_dig = True
            if c_num[1] != "1":
                c_str += kanji[int(c_num[1])]
            c_str += "百"
        if c_num[2] > "0":
            add_dig = True
            if c_num[2] != "1":
                c_str += kanji[int(c_num[2])]
            c_str += "十"
        if c_num[3] > "0":
            add_dig = True
            c_str += kanji[int(c_num[3])]
        if add_dig:
            c_str += digits[i]
        res += c_str
    return res


def kanji2int(kanjis, error="raise"):
    """
    :param kanjis - str: Kanji str to convert into Integer
    :param error - str: How to handle Error. "raise": raise error. "ignore": ignore error , "warn": warn but don't raise
    :return: int
    """
    if error not in ("raise", "warn", "ignore"):
        raise ValueError("unexpected value {} for argument error".format(error))
    kanji = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10, "百": 100, "千": 1000,
             "万": 10 ** 4, "億": 10 ** 8, "兆": 10 ** 12, "京": 10 ** 16, "垓": 10 ** 20, "𥝱": 10 ** 24}
    digits = ("十", "百", "千", "万", "億", "兆", "京", "垓", "𥝱")

    num = 0
    c_num = 0
    c_digit = 0
    dig = "𥝱"
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
