# -*- coding: UTF-8 -*-

import re
from typing import List, Dict

# 正则表达式定义
ipv4_regex = r'((?<!\d)(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?!\d))'
ipv4_port_regex = r'((?:(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])(?::(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|[0-9])(?!\d)))'
ipv6_regex = r'((?:(?:(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){6}:[0-9A-Fa-f]{1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?::[0-9A-Fa-f]{1,4}){1,2})|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?::[0-9A-Fa-f]{1,4}){1,6})|(?::(?::[0-9A-Fa-f]{1,4}){1,7})))'
ipv6_port_regex = r'(\[(?:(?:(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){6}:[0-9A-Fa-f]{1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?::[0-9A-Fa-f]{1,4}){1,2})|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?::[0-9A-Fa-f]{1,4}){1,6})|(?::(?::[0-9A-Fa-f]{1,4}){1,7}))\](?::(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|[0-9])(?!\d)))'
domain_regex = r'((?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'
domain_port_regex = r'((?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|[0-9])(?!\d)))'
url_regex = r'(https?://[-\w]+(?:\.[\w-]+)+(?::\d+)?(?:/[^.!,?\"<>\[\]{}\s\x7F-\xFF]*(?:[.!,?]+[^.!,?\"<>\[\]\{\}\s\x7F-\xFF]+)*)?)'
icp_regex = r'([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]ICP[备证]\d+号(?:-\d+)?)'
id_card_regex = r'((?<!\d)[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|10|11|12)(?:0[1-9]|[1-2]\d|30|31)\d{3}[\dXx](?!\dXx))'
bank_card_regex = r'((?<!\d)[1-9]\d{9,29}(?!\d))'
credit_code_regex = r'((?<![0-9A-HJ-NPQRTUWXY])[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}(?![0-9A-HJ-NPQRTUWXY]))'
email_regex = r'((?:(?:[^<>()[\]\\.,;:\s@\"`]+(?:\.[^<>()[\]\\.,;:\s@\"`]+)*)|(?:\".+\"))@(?:(?:\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(?:(?:[a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,})))'

html_tag_regex = r'(<[^>]+>)'
not_filename_regex = r'([\/\\\:\*\?\"\<\>\|])'


class Extractor:
    """
    提取类：用于从文本中提取 IP 地址、域名、URL 等信息。
    """
    @staticmethod
    def ip(text: str) -> List[str]:
        """
        从文本中提取 IP 地址（IPv4 和 IPv6）。
        :param text: 需要提取的文本
        :return: 包含 IP 地址的列表
        """
        return Extractor.ipv4(text) + Extractor.ipv6(text)

    @staticmethod
    def ipv4(text: str, regex: str = ipv4_regex) -> List[str]:
        """
        从文本中提取 IPv4 地址。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含 IPv4 地址的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def ipv4_port(text: str, regex: str = ipv4_port_regex) -> List[str]:
        """
        从文本中提取 IPv4:端口 地址。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含 IPv4:端口  地址的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def ipv6(text: str, regex: str = ipv6_regex) -> List[str]:
        """
        从文本中提取 IPv6 地址。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含 IPv6 地址的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def ipv6_port(text: str, regex: str = ipv6_port_regex) -> List[str]:
        """
        从文本中提取 IPv6:端口 地址。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含 IPv6:端口  地址的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def domain(text: str, regex: str = domain_regex) -> List[str]:
        """
        从文本中提取域名。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含域名的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def domain_port(text: str, regex: str = domain_port_regex) -> List[str]:
        """
        从文本中提取域名:端口。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含域名:端口的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def host_port(text: str) -> List[str]:
        """
        从文本中提取主机:端口。
        :param text: 需要提取的文本
        :return: 包含主机:端口的列表
        """
        return Extractor.ipv4_port(text) + Extractor.ipv6_port(text) + Extractor.domain_port(text)

    @staticmethod
    def url(text: str, regex: str = url_regex) -> List[str]:
        """
        从文本中提取 URL。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含 URL 的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def icp(text: str, regex: str = icp_regex) -> List[str]:
        """
        从文本中提取 ICP 备案号。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含 ICP 备案号的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def id_card(text: str, regex: str = id_card_regex) -> List[str]:
        """
        从文本中提取身份证号码。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含身份证号码的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def bank_card(text: str, regex: str = bank_card_regex) -> List[str]:
        """
        从文本中提取银行卡号。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含银行卡号的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def credit_code(text: str, regex: str = credit_code_regex) -> List[str]:
        """
        从文本中提取统一社会信用代码。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含统一社会信用代码的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def email(text: str, regex: str = email_regex) -> List[str]:
        """
        从文本中提取 邮箱 地址。
        :param text: 需要提取的文本
        :param regex: 正则表达式
        :return: 包含 邮箱 地址的列表
        """
        return re.findall(regex, text)

    @staticmethod
    def all(text: str) -> Dict[str, List[str]]:
        """
        从文本中提取所有信息（IP、IPv4、IPv6、域名、URL、ICP等）。
        :param text: 需要提取的文本
        :return: 包含所有提取信息的字典
        """
        return {
            "ip": Extractor.ip(text),
            "ipv4": Extractor.ipv4(text),
            "ipv6": Extractor.ipv6(text),
            "domain": Extractor.domain(text),
            "ipv4_port": Extractor.ipv4_port(text),
            "ipv6_port": Extractor.ipv6_port(text),
            "domain_port": Extractor.domain_port(text),
            "host_port": Extractor.host_port(text),
            "url": Extractor.url(text),
            "icp": Extractor.icp(text),
            "id_card": Extractor.id_card(text),
            "bank_card": Extractor.bank_card(text),
            "credit_code": Extractor.credit_code(text),
            "email": Extractor.email(text),
        }


class Validator:
    """
    验证类：用于验证 IP 地址、域名等是否合法。
    """
    @staticmethod
    def ip(address: str) -> bool:
        """
        验证 IP 地址是否合法（支持 IPv4 和 IPv6）。
        :param address: 需要验证的 IP 地址
        :return: 如果合法，返回 True；否则返回 False
        """
        return Validator.ipv4(address) or Validator.ipv6(address)

    @staticmethod
    def ipv4(address: str, regex: str = ipv4_regex) -> bool:
        """
        验证是否是合法的 IPv4 地址。
        :param address: 需要验证的地址字符串
        :param regex: 正则表达式
        :return: 如果是合法的 IPv4 地址，返回 True；否则返回 False
        """
        return bool(re.fullmatch(regex, address))

    @staticmethod
    def host_port(address: str) -> bool:
        """
        验证是否是合法的 主机:端口 地址。
        :param address: 需要验证的主机:端口字符串
        :param regex: 正则表达式
        :return: 如果是合法的 主机:端口 地址，返回 True；否则返回 False
        """
        return Validator.ipv4_port(address) or Validator.ipv6_port(address) or Validator.domain_port(address)

    @staticmethod
    def ipv6_port(address: str, regex: str = ipv6_port_regex) -> bool:
        """
        验证是否是合法的 IPv6:端口 地址。
        :param address: 需要验证的IPv6:端口字符串
        :param regex: 正则表达式
        :return: 如果是合法的 IPv6:端口 地址，返回 True；否则返回 False
        """
        return bool(re.fullmatch(regex, address))

    @staticmethod
    def ipv4_port(address: str, regex: str = ipv4_port_regex) -> bool:
        """
        验证是否是合法的 IPv4:端口 地址。
        :param address: 需要验证的IPv4:端口字符串
        :param regex: 正则表达式
        :return: 如果是合法的 IPv4:端口 地址，返回 True；否则返回 False
        """
        return bool(re.fullmatch(regex, address))

    @staticmethod
    def domain_port(address: str, regex: str = domain_port_regex) -> bool:
        """
        验证是否是合法的 域名:端口 地址。
        :param address: 需要验证的域名:端口字符串
        :param regex: 正则表达式
        :return: 如果是合法的 域名:端口 地址，返回 True；否则返回 False
        """
        return bool(re.fullmatch(regex, address))

    @staticmethod
    def ipv6(address: str, regex: str = ipv6_regex) -> bool:
        """
        验证是否是合法的 IPv6 地址。
        :param address: 需要验证的地址字符串
        :param regex: 正则表达式
        :return: 如果是合法的 IPv6 地址，返回 True；否则返回 False
        """
        return bool(re.fullmatch(regex, address))

    @staticmethod
    def domain(address: str, regex: str = domain_regex) -> bool:
        """
        验证是否是合法的域名。
        :param address: 需要验证的地址字符串
        :param regex: 正则表达式
        :return: 如果是合法的域名，返回 True；否则返回 False
        """
        return bool(re.fullmatch(regex, address))

    @staticmethod
    def url(url: str, regex: str = url_regex) -> bool:
        """
        验证 URL 是否合法。
        :param url: 需要验证的 URL
        :param regex: 正则表达式
        :return: 如果合法，返回 True；否则返回 False
        """
        return bool(re.fullmatch(regex, url))

    @staticmethod
    def icp(icp: str, regex: str = icp_regex) -> bool:
        """
        验证 ICP 备案号是否合法。
        :param icp: 需要验证的 ICP 备案号
        :param regex: 正则表达式
        :return: 如果合法，返回 True；否则返回 False
        """
        return bool(re.fullmatch(regex, icp))

    @staticmethod
    def email(email: str, regex: str = email_regex) -> bool:
        """
        验证 邮箱 是否合法。
        :param icp: 需要验证的 邮箱
        :param regex: 正则表达式
        :return: 如果合法，返回 True；否则返回 False
        """
        return bool(re.fullmatch(regex, email))

    @staticmethod
    def id_card(id_card: str, regex: str = id_card_regex) -> bool:
        """
        验证身份证号码是否合法。
        :param id_card: 需要验证的身份证号码
        :param regex: 正则表达式
        :return: 如果合法，返回 True；否则返回 False
        """
        if not re.fullmatch(regex, id_card):
            return False
        # 身份证校验码计算
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        total = sum(int(id_card[i]) * weights[i] for i in range(17))
        return id_card[-1].upper() == check_codes[total % 11]

    @staticmethod
    def bank_card(bank_card: str, regex: str = bank_card_regex) -> bool:
        """
        验证银行卡号是否合法（使用 Luhn 算法）。
        :param bank_card: 需要验证的银行卡号
        :param regex: 正则表达式
        :return: 如果合法，返回 True；否则返回 False
        """
        if not re.fullmatch(regex, bank_card):
            return False
        # Luhn 算法
        total = 0
        for i, char in enumerate(reversed(bank_card)):
            num = int(char)
            if i % 2 == 1:
                num *= 2
                if num > 9:
                    num = num - 9
            total += num
        return total % 10 == 0

    @staticmethod
    def credit_code(credit_code: str, regex: str = credit_code_regex) -> bool:
        """
        验证统一社会信用代码是否合法。
        :param credit_code: 需要验证的统一社会信用代码
        :param regex: 正则表达式
        :return: 如果合法，返回 True；否则返回 False
        """
        if not re.fullmatch(regex, credit_code):
            return False
        # 统一社会信用代码校验码计算
        weights = [1, 3, 9, 27, 19, 26, 16, 17,
                   20, 29, 25, 13, 8, 24, 10, 30, 28]
        chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"
        total = sum(chars.index(credit_code[i])
                    * weights[i] for i in range(17))
        return credit_code[-1] == chars[(31 - total % 31) % 31]

    @staticmethod
    def identify(text: str) -> str:
        """
        遍历所有校验方法，返回匹配的类型标识符。
        :param text: 需要验证的文本
        :return: 匹配的类型标识符（如 "ipv4"），如果未匹配则返回 "unknown"
        """
        if Validator.ipv4(text):
            return "ipv4"
        elif Validator.ipv6(text):
            return "ipv6"
        elif Validator.domain(text):
            return "domain"
        elif Validator.ipv4_port(text):
            return "ipv4_port"
        elif Validator.ipv6_port(text):
            return "ipv6_port"
        elif Validator.domain_port(text):
            return "domain_port"
        elif Validator.url(text):
            return "url"
        elif Validator.icp(text):
            return "icp"
        elif Validator.id_card(text):
            return "id_card"
        elif Validator.bank_card(text):
            return "bank_card"
        elif Validator.credit_code(text):
            return "credit_code"
        elif Validator.email(text):
            return "email"
        else:
            return None


class TextProcessor:
    """
    文本处理类：用于处理文本中的非法字符、HTML 标签等。
    """
    @staticmethod
    def sanitize_filename(text: str, replacement: str = '', regex: str = not_filename_regex) -> str:
        """
        替换文件名中的非法字符。
        :param text: 需要处理的文本
        :param replacement: 替换字符，默认为空字符串
        :param regex: 正则表达式
        :return: 处理后的文本
        """
        return re.sub(regex, replacement, text)

    @staticmethod
    def remove_html_tags(text: str, replacement: str = '', regex: str = html_tag_regex) -> str:
        """
        移除文本中的 HTML 标签。
        :param text: 需要处理的文本
        :param replacement: 替换字符，默认为空字符串
        :param regex: 正则表达式
        :return: 处理后的文本
        """
        return re.sub(regex, replacement, text)


if __name__ == "__main__":
    # 提取类测试
    text = '''
    IPv4 
        192.168.1.2222, 1255.255.255.255  256.100.1.1, 123.456.78.90 192.168.1.1, 256.256.256.256
        192.168.1.1:80 192.168.1.1:65525 192.168.1.1:65537
    IPv6    
        2001:0db8:85a3:0000:0000:8a2e:0370:7334, ::1 2001:db8::85a3::8a2e:370:7334
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",  # 标准格式
        "2001:db8:85a3::8a2e:370:7334",            # 压缩格式
        "::1",                                     # 本地回环地址
        "::",                                      # 无效地址（全省略）
        "2001:db8::1",                             # 压缩格式
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334:extra",  # 无效格式（超出8组）
        "2001:db8::1::",                           # 无效格式（多个双冒号）
        "2001:db8:85a3:0:0:8a2e:370:7334",        # 标准格式（省略前导0）
        "2001:db8:85a3::8a2e:370:7334:1:1",         # 无效格式（超出8组）
        "2001:db8:85a3::8a2e:370:7334",           # 压缩格式
        fe80:0000:0001:0000:0440:44ff:1233:5678
        fe80:0000:0000:0000:0000:0000:0001:0000 —>fe80::0001:0000
        0:0:0:0:0:0:192.168.12.1 或者 ::192.168.12.1
        0:0:0:0:0:FFFF:192.168.12.1 或者 ::FFFF:192.168.12.1
        2001:0db8:85a3::8a2e:0370:7334
        例如: 2031:0000:130f:0000:0000:09c0:876a:130b, [2031:0000:130f:0000:0000:09c0:876a:130b]:8080"
    domain
        www.baidu.com:80 www.baidu.com:65525 www.baidu.com:65537
    url
        https://example.com/path 
        https://weiminfu.github.io:443/QQMusicWebApp/QQMusicWebAppOneIndex.html?name=will&age=24#programmer
        https://192.168.1.1/QQMusicWebApp/QQMusicWebAppOneIndex.html?name=will&age=24#programmer
        https://192.168.1.1:80/
        http://weiminfu.github.io/login
        https://192.168.1.1:80/
        http://username:password@111.86.21.79:9099/test/get
        http://[2001:470:c:1818::2]:80/index.html
    icp 
        京ICP证030173号
    身份证
        是123456789012345678， 
        430124198910058758
    银行卡号
        6228480402564890018，
    统一社会信用代码
        是91350100M000100Y43。"
        91230199126965908A
    邮箱
    常见邮箱格式
        user@example.com
        john.doe@gmail.com
        jane_doe@yahoo.com
        test.user@outlook.com
        support@company.org
        info@domain.net
        admin@server.io
        contact@website.co
        hello.world@mail.com
        user123@testmail.com
        2. 带特殊字符的邮箱
        user+test@example.com
        user.name+alias@domain.com
        user_name@example.com
        user-name@domain.com
        user.name@sub.domain.com
        user.name@sub-domain.com
        user.name@domain.co.uk
        user.name@domain.ac.in
        user.name@domain.edu.au
        user.name@domain.gov.us
        3. 带数字的邮箱
        user123@example.com
        test.user456@domain.com
        user789@mail.com
        user.name2023@domain.com
        user.name.2023@domain.com
        user.name_2023@domain.com
        user.name-2023@domain.com
        user.name+2023@domain.com
        user.name1234@domain.com
        user.name5678@domain.com
        4. 国际化邮箱
        用户@例子.中国 (中文邮箱)
        usuario@ejemplo.es (西班牙语邮箱)
        utilisateur@exemple.fr (法语邮箱)
        benutzer@beispiel.de (德语邮箱)
        ユーザー@例.jp (日语邮箱)
        사용자@예시.kr (韩语邮箱)
        пользователь@пример.рф (俄语邮箱)
        utente@esempio.it (意大利语邮箱)
        gebruiker@voorbeeld.nl (荷兰语邮箱)
        użytkownik@przykład.pl (波兰语邮箱)
        5. 长域名邮箱
        user@sub.domain.example.com
        user@sub.sub.domain.com
        user@long.domain.name.com
        user@sub.domain.co.uk
        user@sub.domain.ac.in
        user@sub.domain.edu.au
        user@sub.domain.gov.us
        user@sub.domain.org.uk
        user@sub.domain.net.au
        user@sub.domain.io

    '''

    print("Extracted All:",)  #
    result = Extractor.all(text)
    for k in result:
        print(f'{k}: {result[k]} , fail: {[i for i in result[k] if not Validator.identify(i)]}')
    # 验证类测试
    test_data = [
        "192.168.1.257", "192.168.1.2",
        "123456789012345678", "1234567890123456789",
        "6228480402564890018", "6228480402564890018x",
        "91350100M000100Y43", "91350100M000100Y43B",
        "京ICP备12345678号", "四ICP备12345678号",
        "https://www.example.com", "htt://www.example.com", "https://example.com/aa?aaa=www",
        "2001:0db8:85a3::8a2e:0370:7334", "2001:0db8:85a3::8a2e::0370:7334", "2001:0db8:85a3::8a2e:0370:7334:1111:1111",
        "[2031:0000:130f:0000:0000:09c0:876a:130b]:8080",
        "192.168.1.1:80",
        "user@sub.domain.io"
    ]
    print('Validator.identify')
    for i in test_data:
        print(f'\t{i} is {Validator.identify(i)}')
    # 文本处理类测试
    filename = "file/name*with?illegal|characters.txt"
    html_text = "<p>This is <b>bold</b> text.</p>"
    # 处理文件名
    sanitized_filename = TextProcessor.sanitize_filename(filename, "_")
    # file_name_with_illegal_characters.txt
    print(f'Sanitized Filename: "{filename}" -> "{sanitized_filename}"')
    # 移除 HTML 标签
    clean_text = TextProcessor.remove_html_tags(html_text)
    # This is bold text.
    print(f'Text without HTML Tags: "{html_text}" -> "{clean_text}"', )
