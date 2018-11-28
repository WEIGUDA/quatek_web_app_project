def convertor1(number1):
    """将 HID 卡号转化为 EDS 系统中使用的8位16进制卡号

    Arguments:
        number1 {str} -- [description]
    """
    try:
        number1 = str(number1)

        # 前三位转化为 16进制
        number1_1 = hex(int(number1[0:3])).replace('0x', '')

        # 后五位转化为 16进制
        number1_2 = hex(int(number1[3:8])).replace('0x', '')

        # 最后转化为 8位 16进制
        number2 = (str(number1_1) + str(number1_2)).upper().rjust(8, '0')
    except:
        return 'cannot convert'
    else:
        return number2
