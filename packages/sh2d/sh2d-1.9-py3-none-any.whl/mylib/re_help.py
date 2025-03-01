# -*- coding: UTF-8 -*-

import re
from typing import List, Dict


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
    def ipv4(text: str) -> List[str]:
        """
        从文本中提取 IPv4 地址。
        :param text: 需要提取的文本
        :return: 包含 IPv4 地址的列表
        """
        # IPv4 提取规则
        ipv4_regex = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        return re.findall(ipv4_regex, text)

    @staticmethod
    def ipv6(text: str) -> List[str]:
        """
        从文本中提取 IPv6 地址。
        :param text: 需要提取的文本
        :return: 包含 IPv6 地址的列表
        """
        # IPv6 提取规则
        ipv6_regex = r'\b((?:[0-9a-z]*:{1,4}){1,7}[0-9a-z]{1,4})\b'
        return re.findall(ipv6_regex, text)

    @staticmethod
    def domain(text: str) -> List[str]:
        """
        从文本中提取域名。
        :param text: 需要提取的文本
        :return: 包含域名的列表
        """
        # 域名提取规则
        domain_regex = r'\b((?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})\b'
        return re.findall(domain_regex, text)

    @staticmethod
    def url(text: str) -> List[str]:
        """
        从文本中提取 URL。
        :param text: 需要提取的文本
        :return: 包含 URL 的列表
        """
        #  URL 提取规则
        url_regex = r'https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^\s]*)?'
        return re.findall(url_regex, text)

    @staticmethod
    def icp(text: str) -> List[str]:
        """
        从文本中提取 ICP 备案号。
        :param text: 需要提取的文本
        :return: 包含 ICP 备案号的列表
        """
        #  ICP 提取规则
        icp_regex = r'[\u4e00-\u9fa5]ICP[备证]\d+号(?:-\d+)?'
        return re.findall(icp_regex, text)
    
    @staticmethod
    def all(text: str) -> Dict[str, List[str]]:
        """
        从文本中提取所有信息（IP、IPv4、IPv6、域名、URL、ICP）。
        :param text: 需要提取的文本
        :return: 包含所有提取信息的字典
        """
        return {
            "ip": Extractor.ip(text),
            "ipv4": Extractor.ipv4(text),
            "ipv6": Extractor.ipv6(text),
            "domain": Extractor.domain(text),
            "url": Extractor.url(text),
            "icp": Extractor.icp(text),
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
    def ipv4(address: str) -> bool:
        """
        验证是否是合法的 IPv4 地址。
        :param address: 需要验证的地址字符串
        :return: 如果是合法的 IPv4 地址，返回 True；否则返回 False
        """
        #  IPv4 验证规则
        ipv4_regex = (
            r'^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}'
            r'|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d'
            r'|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        return bool(re.match(ipv4_regex, address))

    @staticmethod
    def ipv6(address: str) -> bool:
        """
        验证是否是合法的 IPv6 地址。
        :param address: 需要验证的地址字符串
        :return: 如果是合法的 IPv6 地址，返回 True；否则返回 False
        """
        #  IPv6 验证规则
        ipv6_regex = (
            r'(^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$)|'
            r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,6}\Z)|'
            r'(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,5}\Z)|'
            r'(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,4}\Z)|'
            r'(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,3}\Z)|'
            r'(\A([0-9a-f]{1,4}:){1,5}(:[0-9a-f]{1,4}){1,2}\Z)|'
            r'(\A([0-9a-f]{1,4}:){1,6}(:[0-9a-f]{1,4}){1,1}\Z)|'
            r'(\A(([0-9a-f]{1,4}:){1,7}|:):\Z)|(\A:(:[0-9a-f]{1,4}){1,7}\Z)|'
            r'(\A((([0-9a-f]{1,4}:){6})(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
            r'(\A(([0-9a-f]{1,4}:){5}[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
            r'(\A([0-9a-f]{1,4}:){5}:[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
            r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
            r'(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,3}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
            r'(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,2}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
            r'(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,1}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
            r'(\A(([0-9a-f]{1,4}:){1,5}|:):(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
            r'(\A:(:[0-9a-f]{1,4}){1,5}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)$')
        return bool(re.match(ipv6_regex, address))

    @staticmethod
    def domain(address: str) -> bool:
        """
        验证是否是合法的域名。
        :param address: 需要验证的地址字符串
        :return: 如果是合法的域名，返回 True；否则返回 False
        """
        # 域名验证规则
        domain_regex = (
            r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
            r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$'
        )
        return bool(re.match(domain_regex, address))


class TextProcessor:
    """
    文本处理类：用于处理文本中的非法字符、HTML 标签等。
    """
    @staticmethod
    def sanitize_filename(text: str, replacement: str = '') -> str:
        """
        替换文件名中的非法字符。
        :param text: 需要处理的文本
        :param replacement: 替换字符，默认为空字符串
        :return: 处理后的文本
        """
        return re.sub(r'[\/\\\:\*\?\"\<\>\|]', replacement, text)
    
    @staticmethod
    def remove_html_tags(text: str, replacement: str = '') -> str:
        """
        移除文本中的 HTML 标签。
        :param text: 需要处理的文本
        :param replacement: 替换字符，默认为空字符串
        :return: 处理后的文本
        """
        return re.sub(r'<[^>]+>', replacement, text)


if __name__ == "__main__":
    # 提取类测试
    text = (
        "My IPs are 192.168.1.1, 256.256.256.256, "
        "2001:0db8:85a3::8a2e:0370:7334, and https://example.com/path 京ICP证030173号"
    )
    print("Extracted IPs:", Extractor.ip(text))  # ['192.168.1.1']
    print("Extracted Domains:", Extractor.domain(text))  # ['example.com']
    # ['https://example.com/path']
    print("Extracted URLs:", Extractor.url(text))
    print("Extracted ICPs:", Extractor.icp(text))  # ['京ICP证030173号']
    print("Extracted All:", Extractor.all(text))  # 
    # 验证类测试
    print("Is IPv4 valid:", Validator.ip("192.168.1.1"))  # True
    print("Is IPv4 valid:", Validator.ip("256.256.256.256"))  # False
    print("Is IPv6 valid:", Validator.ip(
        "2001:0db8:85a3::8a2e:0370:7334"))  # True
    print("Is Domain valid:", Validator.domain("baidu.com"))  # True
    print("Is Domain valid:", Validator.domain("baidu..com"))  # False
    # 测试文本
    filename = "file/name*with?illegal|characters.txt"
    html_text = "<p>This is <b>bold</b> text.</p>"
    # 处理文件名
    sanitized_filename = TextProcessor.sanitize_filename(filename, "_")
    print("Sanitized Filename:", sanitized_filename)  # file_name_with_illegal_characters.txt
    # 移除 HTML 标签
    clean_text = TextProcessor.remove_html_tags(html_text)
    print("Text without HTML Tags:", clean_text)  # This is bold text.