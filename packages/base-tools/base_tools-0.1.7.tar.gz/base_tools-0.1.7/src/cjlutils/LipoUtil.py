import subprocess
from enum import Enum
from subprocess import CompletedProcess


class Architecture(Enum):
    UNKNOWN = -1, '',
    ANY = 0, 'any',
    LITTLE = 1, 'little',
    BIG = 2, 'big',
    PPC64 = 3, 'ppc64',
    X86_64 = 4, 'x86_64',
    X86_64H = 5, 'x86_64h',
    ARM64 = 6, 'arm64',
    PPC970_64 = 7, 'ppc970 - 64',
    ARM64_32 = 8, 'arm64_32',
    ARM64E = 9, 'arm64e',
    PPC = 10, 'ppc',
    I386 = 11, 'i386',
    M68K = 12, 'm68k',
    HPPA = 13, 'hppa',
    SPARC = 14, 'sparc',
    M88K = 15, 'm88k',
    I860 = 16, 'i860',
    VEO = 17, 'veo',
    ARM = 18, 'arm',
    PPC601 = 19, 'ppc601',
    PPC603 = 20, 'ppc603',
    PPC603E = 21, 'ppc603e',
    PPC603EV = 22, 'ppc603ev',
    PPC604 = 23, 'ppc604',
    PPC604E = 24, 'ppc604e',
    PPC750 = 25, 'ppc750',
    PPC7400 = 26, 'ppc7400',
    PPC7450 = 27, 'ppc7450',
    PPC970 = 28, 'ppc970',
    I486 = 29, 'i486',
    I486SX = 30, 'i486SX',
    PENTIUM = 31, 'pentium',
    I586 = 32, 'i586',
    PENTPRO = 33, 'pentpro',
    I686 = 34, 'i686',
    PENTIIM3 = 35, 'pentIIm3',
    PENTIIM5 = 36, 'pentIIm5',
    PENTIUM4 = 37, 'pentium4',
    M68030 = 38, 'm68030',
    M68040 = 39, 'm68040',
    HPPA7100LC = 40, 'hppa7100LC',
    VEO1 = 41, 'veo1',
    VEO2 = 42, 'veo2',
    VEO3 = 43, 'veo3',
    VEO4 = 44, 'veo4',
    ARMV4T = 45, 'armv4t',
    ARMV5 = 46, 'armv5',
    XSCALE = 47, 'xscale',
    ARMV6 = 48, 'armv6',
    ARMV6M = 49, 'armv6m',
    ARMV7 = 50, 'armv7',
    ARMV7F = 51, 'armv7f',
    ARMV7S = 52, 'armv7s',
    ARMV7K = 53, 'armv7k',
    ARMV7M = 54, 'armv7m',
    ARMV7EM = 55, 'armv7em',
    ARM64V8 = 56, 'arm64v8',

    @staticmethod
    def get_from_architecture_name(arch_name: str) -> 'Architecture':
        for item in Architecture:
            if item.value[1] == arch_name:
                return item
        return Architecture.UNKNOWN


def create(file_paths: list[str], output_path: str) -> CompletedProcess:
    """
    创建一个合并的文件，如可以将多个有不同架构的.a文件合并为一个有多个架构的.a文件

    :param file_paths: 需要合并的文件路径列表
    :param output_path: 合并后的文件路径
    :return: 执行结果
    """
    if file_paths is None:
        file_paths = list()
    output_path = '' if output_path is None else output_path

    cmd = ['lipo']
    for file_path in file_paths:
        if file_path is None or file_path == '':
            continue
        cmd.append(file_path)

    cmd.extend(['-create', '-output', output_path])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def info(file_path: str) -> None | CompletedProcess:
    """
    获取文件的架构信息

    :param file_path: 文件路径
    :return: 执行结果
    """
    file_path = '' if file_path is None else file_path

    cmd = ['lipo', '-info', file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def thin(file_path: str, architecture: Architecture, output_path) -> None | CompletedProcess:
    """
    提取文件的指定架构，形成新文件

    :param file_path: 被提取文件路径
    :param architecture: 指定架构
    :param output_path: 新文件地址
    :return: 执行结果
    """
    file_path = '' if file_path is None else file_path
    architecture = Architecture.ANY if architecture is None else architecture
    output_path = '' if output_path is None else output_path

    cmd = ['lipo', file_path, '-thin', architecture.value[1], '-output', output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def get_architectures(file_path: str) -> set[Architecture]:
    """
    获取文件的架构列表

    :param file_path: 文件路径
    :return: 架构列表
    """
    result = info(file_path)
    if result is None:
        return set()
    output = result.stdout
    if output is None:
        return set()

    substring_before_muti = 'are: '
    substring_before_single = 'architecture: '
    substring_before: str = ': '
    if output.find(substring_before_muti) >= 0:
        substring_before = substring_before_muti
    elif output.find(substring_before_single) >= 0:
        substring_before = substring_before_single

    start_index = output.rfind(substring_before) + substring_before.__len__()
    arch_names = output.strip()[start_index:].split(' ')
    architectures = set()
    for arch_name in arch_names:
        arch = Architecture.get_from_architecture_name(arch_name)
        if arch is not None and arch != Architecture.UNKNOWN:
            architectures.add(arch)
    return architectures
