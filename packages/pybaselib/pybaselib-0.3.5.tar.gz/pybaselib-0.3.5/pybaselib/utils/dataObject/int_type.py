# -*- coding: utf-8 -*-
# @Author: maoyongfan
# @email: maoyongfan@163.com
# @Date: 2025/2/26 21:19
from pybaselib.utils.net import is_valid_ip
from pybaselib.utils import ParameterError
from functools import reduce

def int_to_hex_string(int_value, length):
    """
    将十进制数转换为指定长度的十六进制字符串
    :param int_value:
    :param length:
    :return:
    """
    return f"{int_value:0{length}X}"


def ip_to_hex_string(ip_value):
    hex_string = ""
    if is_valid_ip:
        for item in ip_value.split("."):
            hex_string += f"{int(item):02X}"
        return hex_string
    else:
        raise ParameterError("无效的IP地址")

def int_to_binary_string(int_value, length):
    """
    将十进制转为指定位数的2进制
    :param int_value:
    :param length:
    :return:
    """
    binary_string = format(int_value, f'0{length}b')
    return reduce(lambda x, y: y + x, binary_string)

if __name__ == '__main__':
    # print(int_to_hex_string(38393,4))
    print(ip_to_hex_string("192.168.1.122"))
