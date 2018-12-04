def convertor1(number1):
    """将 HID 卡号转化为 EDS 系统中使用的8位16进制卡号
    卡号现有机制是8位数，结果是前三位转换+后五位转换，结果少于8位的补0到8位。 卡号转换出错，问
    题出在后五位，有的后五位转换下来只有三位，应当补0成为4位，再和前面的放在一起。 考虑到前三位
    也有可能存在这个问题，那就应该是前三位转换，结果不足两位的话补0到两位，后五位转换，结果不足
    4位的话补0到四位，结果前面再加两个00 以及如果方便的话，加一个检测到输入数据只有7个数的情
    况，前面补0成为8位数再进行前三位和后五位转换加00，因为excel有的格式不会显示数据前面的0

    Arguments:
        number1 {str} -- [description]
    """
    try:
        number1 = str(number1)
        len_number1 = len(number1)

        # 将 number1 分为前半部分, 和后5位部分
        part1 = "{:X}".format(int(number1[0:len_number1-5]))
        part2 = "{:X}".format(int(number1[len_number1-5:len_number1]))

        # 最后 将前半部分补足至4位, 后半部分也补足至4位
        number2 = "{:0>4}{:0>4}".format(part1, part2)

    except:
        return 'cannot convert'
    else:
        return number2
