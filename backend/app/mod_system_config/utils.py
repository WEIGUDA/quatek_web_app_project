def convertor1(number1):
    """将 HID 卡号转化为 EDS 系统中使用的8位16进制卡号
        13149005 --> 131  49005 --> 0083BF6D
        02103646 --> 021  03646 --> 00150E3E
         2103646 -->  21  03646 --> 00150E3E

    Arguments:
        number1 {str} -- 输入的 HID 卡号
    """
    try:
        number1 = str(number1)
        len_number1 = len(number1)

        # 将 number1 分为前半部分, 和后5位部分
        part1 = "{:X}".format(int(number1[0 : len_number1 - 5]))
        part2 = "{:X}".format(int(number1[len_number1 - 5 : len_number1]))

        # 最后 将前半部分补足至4位, 后半部分也补足至4位
        number2 = "{:0>4}{:0>4}".format(part1, part2)

    except:
        return "cannot convert"

    else:
        return number2
