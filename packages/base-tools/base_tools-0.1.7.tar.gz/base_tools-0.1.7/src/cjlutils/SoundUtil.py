import math
from enum import Enum

import numpy as np


# 大小字组
class ClefTypeData:
    def __init__(self, value: int, name: str):
        self.value = value
        self.name = name


class ClefTypeEnum(Enum):
    UNKNOWN = ClefTypeData(0, 'Unknown')
    # 大字组系列
    BASS = ClefTypeData(1, 'Bass')
    # 小字组系列
    TREBLE = ClefTypeData(2, 'Treble')


# 唱名
class SolmizationData:
    def __init__(self, value: int, name: str):
        self.value = value
        self.name = name


class SolmizationEnum(Enum):
    UNKNOWN = SolmizationData(0, 'Unknown')
    DO = SolmizationData(1, 'Do')
    RE = SolmizationData(2, 'Re')
    MI = SolmizationData(3, 'Mi')
    FA = SolmizationData(4, 'Fa')
    SOL = SolmizationData(5, 'Sol')
    LA = SolmizationData(6, 'La')
    TI = SolmizationData(7, 'Ti')

    @staticmethod
    def get_by_str(name: str):
        if name.lower() == SolmizationEnum.DO.value.name.lower():
            return SolmizationEnum.DO
        elif name.lower() == SolmizationEnum.RE.value.name.lower():
            return SolmizationEnum.RE
        elif name.lower() == SolmizationEnum.MI.value.name.lower():
            return SolmizationEnum.MI
        elif name.lower() == SolmizationEnum.FA.value.name.lower():
            return SolmizationEnum.FA
        elif name.lower() == SolmizationEnum.SOL.value.name.lower():
            return SolmizationEnum.SOL
        elif name.lower() == SolmizationEnum.LA.value.name.lower():
            return SolmizationEnum.LA
        elif name.lower() == SolmizationEnum.TI.value.name.lower():
            return SolmizationEnum.TI
        else:
            return SolmizationEnum.UNKNOWN


# 音名
class PitchData:
    def __init__(self, value: int, name: str):
        self.value = value
        self.name = name


class PitchEnum(Enum):
    UNKNOWN = PitchData(0, 'Unknown')
    C = SolmizationData(1, 'C')
    D = SolmizationData(2, 'D')
    E = SolmizationData(3, 'E')
    F = SolmizationData(4, 'F')
    G = SolmizationData(5, 'G')
    A = SolmizationData(6, 'A')
    B = SolmizationData(7, 'B')

    @staticmethod
    def get_by_str(name: str):
        if name.lower() == PitchEnum.C.value.name.lower():
            return PitchEnum.C
        elif name.lower() == PitchEnum.D.value.name.lower():
            return PitchEnum.D
        elif name.lower() == PitchEnum.E.value.name.lower():
            return PitchEnum.E
        elif name.lower() == PitchEnum.F.value.name.lower():
            return PitchEnum.F
        elif name.lower() == PitchEnum.G.value.name.lower():
            return PitchEnum.G
        elif name.lower() == PitchEnum.A.value.name.lower():
            return PitchEnum.A
        elif name.lower() == PitchEnum.B.value.name.lower():
            return PitchEnum.B
        else:
            return PitchEnum.UNKNOWN


def get_average_12_order(solmization: SolmizationEnum | PitchEnum, bias: int = 0) -> int:
    """
    根据唱名获取十二平均律的序号
    :param solmization: 唱名
    :param bias: 偏移。如1：升高半个音；-1：降低半个音。
    :return:
    """
    value = solmization.value.value
    if value == 1:
        base = 1
    elif value == 2:
        base = 3
    elif value == 3:
        base = 5
    elif value == 4:
        base = 6
    elif value == 5:
        base = 8
    elif value == 6:
        base = 10
    elif value == 7:
        base = 12
    else:
        return 0
    return base + bias


def get_frequency_by_clef(clef_type: ClefTypeEnum, clef_order: int, average_12_order: int) -> float:
    """
    获取指定音符的频率

    :param clef_type: 音域类型。即大字组系列和小字组系列
    :param clef_order: 音域类型下的八度区间，小字组和大字组为0，小字一组和大字一组为1，以此类推
    :param average_12_order: 12平均律下的音符，Do为1，Ti为12
    :return:
    """
    if clef_type is None or clef_type == ClefTypeEnum.UNKNOWN or clef_order < 0 or average_12_order > 12 or average_12_order <= 0:
        return 0
    # 标准音：小字一组的A是440Hz（也有435Hz的标准）
    # a = 220：小字组A的频率是小字一组A的一半
    a1 = 440
    log_a1 = math.log2(a1)
    log_c1 = log_a1 - 9 / 12

    log_base_c: float
    if clef_type == ClefTypeEnum.BASS:
        log_C = log_c1 - 2
        log_base_c = log_C - clef_order
    elif clef_type == ClefTypeEnum.TREBLE:
        log_c = log_c1 - 1
        log_base_c = log_c + clef_order
    else:
        return 0
    log_result = log_base_c + (average_12_order - 1) / 12
    return 2 ** log_result


def create_wave(frequency: float, duration: float, sample_rate: float = 44100, amplitude: float = 2 ** 8) -> np.ndarray:
    """
    创建一个指定音高的音频数字信号

    :param frequency: 频率
    :param duration: 时长（秒）
    :param sample_rate: 采样率，每秒采样数量
    :param amplitude: 振幅
    :return: 数字信号
    """
    point_count = int(sample_rate * duration)
    t = np.linspace(0, duration, point_count, False)
    signal = amplitude * np.sin(2 * np.pi * frequency * t)
    return signal

