import hashlib
import re
from enum import Enum


class StandardEncodings:

    def __init__(self, names: list[str] = None, language_desc_list: list[str] = None):
        self.names = names
        self.language_desc_list = language_desc_list

    @staticmethod
    def new_instance(name: str, alias_list: list[str], language_desc_list: list[str]) -> 'StandardEncodings':
        names = [name]
        names.extend(alias_list)
        return StandardEncodings(names, language_desc_list)

    def get_name(self) -> None | str:
        return self.names[0] if self.names is not None and len(self.names) > 0 else None

    def get_alias_list(self) -> list[str]:
        return self.names[1:] if self.names is not None and len(self.names) > 1 else []

    def __str__(self):
        return f'names: [{", ".join(self.names)}], language_desc_list: [{", ".join(self.language_desc_list)}])'


class StandardEncodingsEnum(Enum):
    EMPTY = StandardEncodings.new_instance('', [], [])
    ASCII = StandardEncodings.new_instance('ascii', ["646", "us-ascii"], ['English'])
    BIG5 = StandardEncodings.new_instance('big5', ["big5-tw", "csbig5"], ['Traditional Chinese'])
    BIG5HKSCS = StandardEncodings.new_instance('big5hkscs', ["big5-hkscs", "hkscs"], ['Traditional Chinese'])
    CP037 = StandardEncodings.new_instance('cp037', ["IBM037", "IBM039"], ['English'])
    CP273 = StandardEncodings.new_instance('cp273', ["273", "IBM273", "csIBM273"], ['German'])
    CP424 = StandardEncodings.new_instance('cp424', ["EBCDIC-CP-HE", "IBM424"], ['Hebrew'])
    CP437 = StandardEncodings.new_instance('cp437', ["437", "IBM437"], ['English'])
    CP500 = StandardEncodings.new_instance('cp500', ["EBCDIC-CP-BE", "EBCDIC-CP-CH", "IBM500"], ['Western Europe'])
    CP720 = StandardEncodings.new_instance('cp720', [], ['Arabic'])
    CP737 = StandardEncodings.new_instance('cp737', [], ['Greek'])
    CP775 = StandardEncodings.new_instance('cp775', ["IBM775"], ['Baltic languages'])
    CP850 = StandardEncodings.new_instance('cp850', ["850", "IBM850"], ['Western Europe'])
    CP852 = StandardEncodings.new_instance('cp852', ["852", "IBM852"], ['Central and Eastern Europe'])
    CP855 = StandardEncodings.new_instance('cp855', ["855", "IBM855"],
                                           ['Bulgarian', 'Byelorussian', 'Macedonian', 'Russian', 'Serbian'])
    CP856 = StandardEncodings.new_instance('cp856', [], ['Hebrew'])
    CP857 = StandardEncodings.new_instance('cp857', ["857", "IBM857"], ['Turkish'])
    CP858 = StandardEncodings.new_instance('cp858', ["858", "IBM858"], ['Western Europe'])
    CP860 = StandardEncodings.new_instance('cp860', ["860", "IBM860"], ['Portuguese'])
    CP861 = StandardEncodings.new_instance('cp861', ["861", "CP-IS", "IBM861"], ['Icelandic'])
    CP862 = StandardEncodings.new_instance('cp862', ["862", "IBM862"], ['Hebrew'])
    CP863 = StandardEncodings.new_instance('cp863', ["863", "IBM863"], ['Canadian'])
    CP864 = StandardEncodings.new_instance('cp864', ["IBM864"], ['Arabic'])
    CP865 = StandardEncodings.new_instance('cp865', ["865", "IBM865"], ['Danish', 'Norwegian'])
    CP866 = StandardEncodings.new_instance('cp866', ["866", "IBM866"], ['Russian'])
    CP869 = StandardEncodings.new_instance('cp869', ["869", "CP-GR", "IBM869"], ['Greek'])
    CP874 = StandardEncodings.new_instance('cp874', [], ['Thai'])
    CP875 = StandardEncodings.new_instance('cp875', [], ['Greek'])
    CP932 = StandardEncodings.new_instance('cp932', ["932", "ms932", "mskanji", "ms-kanji", "windows-31j"],
                                           ['Japanese'])
    CP949 = StandardEncodings.new_instance('cp949', ["949", "ms949", "uhc"], ['Korean'])
    CP950 = StandardEncodings.new_instance('cp950', ["950", "ms950"], ['Traditional Chinese'])
    CP1006 = StandardEncodings.new_instance('cp1006', [], ['Urdu'])
    CP1026 = StandardEncodings.new_instance('cp1026', ["ibm1026"], ['Turkish'])
    CP1125 = StandardEncodings.new_instance('cp1125', ["1125", "ibm1125", "cp866u", "ruscii"], ['Ukrainian'])
    CP1140 = StandardEncodings.new_instance('cp1140', ["ibm1140"], ['Western Europe'])
    CP1250 = StandardEncodings.new_instance('cp1250', ["windows-1250"], ['Central and Eastern Europe'])
    CP1251 = StandardEncodings.new_instance('cp1251', ["windows-1251"],
                                            ['Bulgarian', 'Byelorussian', 'Macedonian', 'Russian', 'Serbian'])
    CP1252 = StandardEncodings.new_instance('cp1252', ["windows-1252"], ['Western Europe'])
    CP1253 = StandardEncodings.new_instance('cp1253', ["windows-1253"], ['Greek'])
    CP1254 = StandardEncodings.new_instance('cp1254', ["windows-1254"], ['Turkish'])
    CP1255 = StandardEncodings.new_instance('cp1255', ["windows-1255"], ['Hebrew'])
    CP1256 = StandardEncodings.new_instance('cp1256', ["windows-1256"], ['Arabic'])
    CP1257 = StandardEncodings.new_instance('cp1257', ["windows-1257"], ['Baltic languages'])
    CP1258 = StandardEncodings.new_instance('cp1258', ["windows-1258"], ['Vietnamese'])
    EUC_JP = StandardEncodings.new_instance('euc_jp', ["eucjp", "ujis", "u-jis"], ['Japanese'])
    EUC_JIS_2004 = StandardEncodings.new_instance('euc_jis_2004', ["jisx0213", "eucjis2004"], ['Japanese'])
    EUC_JISX0213 = StandardEncodings.new_instance('euc_jisx0213', ["eucjisx0213"], ['Japanese'])
    EUC_KR = StandardEncodings.new_instance('euc_kr',
                                            ["euckr", "korean", "ksc5601", "ks_c-5601", "ks_c-5601-1987", "ksx1001",
                                             "ks_x-1001"], ['Korean'])
    GB2312 = StandardEncodings.new_instance('gb2312', ["chinese", "csiso58gb231280", "euc-cn", "euccn", "eucgb2312-cn",
                                                       "gb2312-1980", "gb2312-80", "iso-ir-58"], ['Simplified Chinese'])
    GBK = StandardEncodings.new_instance('gbk', ["936", "cp936", "ms936"], ['Unified Chinese'])
    GB18030 = StandardEncodings.new_instance('gb18030', ["gb18030-2000"], ['Unified Chinese'])
    HZ = StandardEncodings.new_instance('hz', ["hzgb", "hz-gb", "hz-gb-2312"], ['Simplified Chinese'])
    ISO2022_JP = StandardEncodings.new_instance('iso2022_jp', ["csiso2022jp", "iso2022jp", "iso-2022-jp"], ['Japanese'])
    ISO2022_JP_1 = StandardEncodings.new_instance('iso2022_jp_1', ["iso2022jp-1", "iso-2022-jp-1"], ['Japanese'])
    ISO2022_JP_2 = StandardEncodings.new_instance('iso2022_jp_2', ["iso2022jp-2", "iso-2022-jp-2"],
                                                  ['Japanese', 'Korean', 'Simplified Chinese', 'Western Europe',
                                                   'Greek'])
    ISO2022_JP_2004 = StandardEncodings.new_instance('iso2022_jp_2004', ["iso2022jp-2004", "iso-2022-jp-2004"],
                                                     ['Japanese'])
    ISO2022_JP_3 = StandardEncodings.new_instance('iso2022_jp_3', ["iso2022jp-3", "iso-2022-jp-3"], ['Japanese'])
    ISO2022_JP_EXT = StandardEncodings.new_instance('iso2022_jp_ext', ["iso2022jp-ext", "iso-2022-jp-ext"],
                                                    ['Japanese'])
    ISO2022_KR = StandardEncodings.new_instance('iso2022_kr', ["csiso2022kr", "iso2022kr", "iso-2022-kr"], ['Korean'])
    LATIN_1 = StandardEncodings.new_instance('latin_1',
                                             ["iso-8859-1", "iso8859-1", "8859", "cp819", "latin", "latin1", "L1"],
                                             ['Western Europe'])
    ISO8859_2 = StandardEncodings.new_instance('iso8859_2', ["iso-8859-2", "latin2", "L2"],
                                               ['Central and Eastern Europe'])
    ISO8859_3 = StandardEncodings.new_instance('iso8859_3', ["iso-8859-3", "latin3", "L3"], ['Esperanto', 'Maltese'])
    ISO8859_4 = StandardEncodings.new_instance('iso8859_4', ["iso-8859-4", "latin4", "L4"], ['Baltic languages'])
    ISO8859_5 = StandardEncodings.new_instance('iso8859_5', ["iso-8859-5", "cyrillic"],
                                               ['Bulgarian', 'Byelorussian', 'Macedonian', 'Russian', 'Serbian'])
    ISO8859_6 = StandardEncodings.new_instance('iso8859_6', ["iso-8859-6", "arabic"], ['Arabic'])
    ISO8859_7 = StandardEncodings.new_instance('iso8859_7', ["iso-8859-7", "greek", "greek8"], ['Greek'])
    ISO8859_8 = StandardEncodings.new_instance('iso8859_8', ["iso-8859-8", "hebrew"], ['Hebrew'])
    ISO8859_9 = StandardEncodings.new_instance('iso8859_9', ["iso-8859-9", "latin5", "L5"], ['Turkish'])
    ISO8859_10 = StandardEncodings.new_instance('iso8859_10', ["iso-8859-10", "latin6", "L6"], ['Nordic languages'])
    ISO8859_11 = StandardEncodings.new_instance('iso8859_11', ["iso-8859-11", "thai"], ['Thai languages'])
    ISO8859_13 = StandardEncodings.new_instance('iso8859_13', ["iso-8859-13", "latin7", "L7"], ['Baltic languages'])
    ISO8859_14 = StandardEncodings.new_instance('iso8859_14', ["iso-8859-14", "latin8", "L8"], ['Celtic languages'])
    ISO8859_15 = StandardEncodings.new_instance('iso8859_15', ["iso-8859-15", "latin9", "L9"], ['Western Europe'])
    ISO8859_16 = StandardEncodings.new_instance('iso8859_16', ["iso-8859-16", "latin10", "L10"],
                                                ['South-Eastern Europe'])
    JOHAB = StandardEncodings.new_instance('johab', ["cp1361", "ms1361"], ['Korean'])
    KOI8_R = StandardEncodings.new_instance('koi8_r', [], ['Russian'])
    KOI8_T = StandardEncodings.new_instance('koi8_t', [], ['Tajik'])
    KOI8_U = StandardEncodings.new_instance('koi8_u', [], ['Ukrainian'])
    KZ1048 = StandardEncodings.new_instance('kz1048', ["kz_1048", "strk1048_2002", "rk1048"], ['Kazakh'])
    MAC_CYRILLIC = StandardEncodings.new_instance('mac_cyrillic', ["maccyrillic"],
                                                  ['Bulgarian', 'Byelorussian', 'Macedonian', 'Russian', 'Serbian'])
    MAC_GREEK = StandardEncodings.new_instance('mac_greek', ["macgreek"], ['Greek'])
    MAC_ICELAND = StandardEncodings.new_instance('mac_iceland', ["maciceland"], ['Icelandic'])
    MAC_LATIN2 = StandardEncodings.new_instance('mac_latin2', ["maclatin2", "maccentraleurope", "mac_centeuro"],
                                                ['Central and Eastern Europe'])
    MAC_ROMAN = StandardEncodings.new_instance('mac_roman', ["macroman", "macintosh"], ['Western Europe'])
    MAC_TURKISH = StandardEncodings.new_instance('mac_turkish', ["macturkish"], ['Turkish'])
    PTCP154 = StandardEncodings.new_instance('ptcp154', ["csptcp154", "pt154", "cp154", "cyrillic-asian"], ['Kazakh'])
    SHIFT_JIS = StandardEncodings.new_instance('shift_jis', ["csshiftjis", "shiftjis", "sjis", "s_jis"], ['Japanese'])
    SHIFT_JIS_2004 = StandardEncodings.new_instance('shift_jis_2004', ["shiftjis2004", "sjis_2004", "sjis2004"],
                                                    ['Japanese'])
    SHIFT_JISX0213 = StandardEncodings.new_instance('shift_jisx0213', ["shiftjisx0213", "sjisx0213", "s_jisx0213"],
                                                    ['Japanese'])
    UTF_32 = StandardEncodings.new_instance('utf_32', ["U32", "utf32"], ['all languages'])
    UTF_32_BE = StandardEncodings.new_instance('utf_32_be', ["UTF-32BE"], ['all languages'])
    UTF_32_LE = StandardEncodings.new_instance('utf_32_le', ["UTF-32LE"], ['all languages'])
    UTF_16 = StandardEncodings.new_instance('utf_16', ["U16", "utf16"], ['all languages'])
    UTF_16_BE = StandardEncodings.new_instance('utf_16_be', ["UTF-16BE"], ['all languages'])
    UTF_16_LE = StandardEncodings.new_instance('utf_16_le', ["UTF-16LE"], ['all languages'])
    UTF_7 = StandardEncodings.new_instance('utf_7', ["U7", "unicode-1-1-utf-7"], ['all languages'])
    UTF_8 = StandardEncodings.new_instance('utf_8', ["U8", "UTF", "utf8", "cp65001"], ['all languages'])
    UTF_8_SIG = StandardEncodings.new_instance('utf_8_sig', [], ['all languages'])

    def get_with_name(name: str) -> 'StandardEncodingsEnum':
        for encoding in StandardEncodingsEnum:
            if name in encoding.value.names:
                return encoding
        return StandardEncodingsEnum.EMPTY


def contains(string: str, sub: str) -> bool:
    """
    判断字符串是否包含子串
    :param string: 字符串
    :param sub: 子串
    :return: 是否包含
    """
    if string is None or sub is None:
        return False
    return string.find(sub) != -1


def from_bytes(b: bytes, encode: str | StandardEncodingsEnum = StandardEncodingsEnum.UTF_8) -> None | str:
    """
    字节流转字符串
    :param b: 字节流
    :param encode: 编码
    :return:
    """
    if b is None:
        return None
    encode_str = ''
    if isinstance(encode, StandardEncodingsEnum):
        encode_str = encode.value.get_name()
    elif isinstance(encode, str):
        encode_str = encode
    return b.decode(encode_str)


def index_of_first(string: str, substring: str) -> int:
    """
    获取字符串中第一个子串的索引
    :param string: 字符串
    :param substring: 子串
    :return: 第一个子串的索引
    """
    if string is None or substring is None:
        return -1
    return string.find(substring)


def index_of_first_number(string: str) -> int:
    """
    获取字符串中第一个数字的索引
    :param string: 字符串
    :return: 第一个数字的索引
    """
    if string is None:
        return -1
    for i in range(len(string)):
        if string[i].isdigit():
            return i
    return -1


def index_of_first_small_case_alpha(string: str) -> int:
    """
    获取字符串中第一个小写字母的索引
    :param string: 字符串
    :return: 第一个小写字母的索引
    """
    if string is None:
        return -1
    for i in range(len(string)):
        if string[i].islower():
            return i
    return -1


def index_of_first_big_case_alpha(string: str) -> int:
    """
    获取字符串中第一个大写字母的索引
    :param string: 字符串
    :return: 第一个大写字母的索引
    """
    if string is None:
        return -1
    for i in range(len(string)):
        if string[i].isupper():
            return i
    return -1


def index_of_last(string: str, substring: str) -> int:
    """
    获取字符串中最后一个子串的索引
    :param string: 字符串
    :param substring: 子串
    :return: 最后一个子串的索引
    """
    if string is None or substring is None:
        return -1
    return string.rfind(substring)


def index_of_last_number(string: str) -> int:
    """
    获取字符串中最后一个数字的索引
    :param string: 字符串
    :return: 最后一个数字的索引
    """
    if string is None:
        return -1
    for i in range(len(string) - 1, -1, -1):
        if string[i].isdigit():
            return i
    return -1


def index_of_last_small_case_alpha(string: str) -> int:
    """
    获取字符串中最后一个小写字母的索引
    :param string: 字符串
    :return: 最后一个小写字母的索引
    """
    if string is None:
        return -1
    for i in range(len(string) - 1, -1, -1):
        if string[i].islower():
            return i
    return -1


def index_of_last_big_case_alpha(string: str) -> int:
    """
    获取字符串中最后一个大写字母的索引
    :param string: 字符串
    :return: 最后一个大写字母的索引
    """
    if string is None:
        return -1
    for i in range(len(string) - 1, -1, -1):
        if string[i].isupper():
            return i
    return -1


def is_empty(string: None | str) -> bool:
    """
    判断字符串是否为空，None或者长度为0
    :param string: 字符串
    :return: 是否为空
    """
    return string is None or len(string) <= 0


def is_not_empty(string: None | str) -> bool:
    """
    判断字符串是否为空，None或者长度为0
    :param string: 字符串
    :return: 是否为空
    """
    return not is_empty(string)


def md5(string: str) -> str:
    hash_object = hashlib.md5(string.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


def to_bytes(string: None | str, encode: StandardEncodingsEnum | str = StandardEncodingsEnum.UTF_8) -> None | bytes:
    """
    字符串转字节流
    :param string: 字符串
    :param encode: 编码类型， 见https://docs.python.org/3.13/library/codecs.html#standard-encodings
    :return: 字节流
    """
    if string is None:
        return None
    encode_str = ''
    if isinstance(encode, StandardEncodingsEnum):
        encode_str = encode.value.get_name()
    elif isinstance(encode, str):
        encode_str = encode
    return string.encode(encode_str)


def to_camel_case(string: None | str) -> None | str:
    """
    下划线格式转换为驼峰格式
    :param string: 下划线格式字符串
    :return: 驼峰格式字符串
    """
    if string is None:
        return None
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_int(string: None | str) -> None | int:
    """
    字符串转整数
    :param string: 字符串
    :return: 整数
    """
    if string is None:
        return None
    try:
        return int(string)
    except ValueError:
        return None


def to_snake_case(string: None | str) -> None | str:
    """
    驼峰格式转换为下划线格式
    :param string: 驼峰格式字符串
    :return: 下划线格式字符串
    """
    if string is None:
        return None
    # 大写字母前面是大小写字母或者数字时，在大写字母前加上下划线
    s1 = re.sub('([A-Za-z0-9])([A-Z])', r'\1_\2', string)
    # 上面匹配两个字符，导致连续两个大写字母之间可能不会被下划线分割，需要再做一次。
    s1 = re.sub('([A-Za-z0-9])([A-Z])', r'\1_\2', s1)
    return s1.lower()
