import unittest

from src.cjlutils import SoundUtil, FileUtil
from src.cjlutils.SoundUtil import SolmizationEnum, PitchEnum


class CreateWaveTestCase(unittest.TestCase):
    def test_the_second_walt(self):
        sample_rate = 44100
        g1 = SoundUtil.get_frequency_by_clef(SoundUtil.ClefTypeEnum.TREBLE, 1,
                                             SoundUtil.get_average_12_order(SoundUtil.SolmizationEnum.SOL))
        be = SoundUtil.get_frequency_by_clef(SoundUtil.ClefTypeEnum.TREBLE, 1,
                                             SoundUtil.get_average_12_order(SoundUtil.SolmizationEnum.MI, -1))
        d = SoundUtil.get_frequency_by_clef(SoundUtil.ClefTypeEnum.TREBLE, 1,
                                            SoundUtil.get_average_12_order(SoundUtil.SolmizationEnum.RE))
        c = SoundUtil.get_frequency_by_clef(SoundUtil.ClefTypeEnum.TREBLE, 1,
                                            SoundUtil.get_average_12_order(SoundUtil.SolmizationEnum.DO))

        speed = 174
        arr = list(SoundUtil.create_wave(g1, 3 * 60 / speed, sample_rate=sample_rate))
        arr += list(SoundUtil.create_wave(be, 2 * 60 / speed, sample_rate=sample_rate))
        arr += list(SoundUtil.create_wave(d, 1 * 60 / speed, sample_rate=sample_rate))
        arr += list(SoundUtil.create_wave(c, 3 * 60 / speed, sample_rate=sample_rate))
        FileUtil.create_audio_file(arr, './audio/sound.wav', sample_rate=sample_rate)
        print('done')


class SolmizationEnumTestCase(unittest.TestCase):
    def test_get_by_str_match(self):
        self.assertEqual(SolmizationEnum.DO, SolmizationEnum.get_by_str('Do'))
        self.assertEqual(SolmizationEnum.RE, SolmizationEnum.get_by_str('Re'))
        self.assertEqual(SolmizationEnum.MI, SolmizationEnum.get_by_str('Mi'))
        self.assertEqual(SolmizationEnum.FA, SolmizationEnum.get_by_str('Fa'))
        self.assertEqual(SolmizationEnum.SOL, SolmizationEnum.get_by_str('Sol'))
        self.assertEqual(SolmizationEnum.LA, SolmizationEnum.get_by_str('La'))
        self.assertEqual(SolmizationEnum.TI, SolmizationEnum.get_by_str('Ti'))

    def test_get_by_str_small_case(self):
        self.assertEqual(SolmizationEnum.DO, SolmizationEnum.get_by_str('do'))
        self.assertEqual(SolmizationEnum.RE, SolmizationEnum.get_by_str('re'))
        self.assertEqual(SolmizationEnum.MI, SolmizationEnum.get_by_str('mi'))
        self.assertEqual(SolmizationEnum.FA, SolmizationEnum.get_by_str('fa'))
        self.assertEqual(SolmizationEnum.SOL, SolmizationEnum.get_by_str('sol'))
        self.assertEqual(SolmizationEnum.LA, SolmizationEnum.get_by_str('la'))
        self.assertEqual(SolmizationEnum.TI, SolmizationEnum.get_by_str('ti'))

    def test_get_by_str_large_case(self):
        self.assertEqual(SolmizationEnum.DO, SolmizationEnum.get_by_str('DO'))
        self.assertEqual(SolmizationEnum.RE, SolmizationEnum.get_by_str('RE'))
        self.assertEqual(SolmizationEnum.MI, SolmizationEnum.get_by_str('MI'))
        self.assertEqual(SolmizationEnum.FA, SolmizationEnum.get_by_str('FA'))
        self.assertEqual(SolmizationEnum.SOL, SolmizationEnum.get_by_str('SOL'))
        self.assertEqual(SolmizationEnum.LA, SolmizationEnum.get_by_str('LA'))
        self.assertEqual(SolmizationEnum.TI, SolmizationEnum.get_by_str('TI'))

    def test_get_by_str_special_case(self):
        self.assertEqual(SolmizationEnum.DO, SolmizationEnum.get_by_str('dO'))
        self.assertEqual(SolmizationEnum.RE, SolmizationEnum.get_by_str('rE'))
        self.assertEqual(SolmizationEnum.MI, SolmizationEnum.get_by_str('mI'))
        self.assertEqual(SolmizationEnum.FA, SolmizationEnum.get_by_str('fA'))
        self.assertEqual(SolmizationEnum.SOL, SolmizationEnum.get_by_str('soL'))
        self.assertEqual(SolmizationEnum.SOL, SolmizationEnum.get_by_str('SoL'))
        self.assertEqual(SolmizationEnum.SOL, SolmizationEnum.get_by_str('sOL'))
        self.assertEqual(SolmizationEnum.LA, SolmizationEnum.get_by_str('lA'))
        self.assertEqual(SolmizationEnum.TI, SolmizationEnum.get_by_str('tI'))


class PitchEnumTestCase(unittest.TestCase):
    def test_get_by_str_match(self):
        self.assertEqual(PitchEnum.C, PitchEnum.get_by_str('C'))
        self.assertEqual(PitchEnum.D, PitchEnum.get_by_str('D'))
        self.assertEqual(PitchEnum.E, PitchEnum.get_by_str('E'))
        self.assertEqual(PitchEnum.F, PitchEnum.get_by_str('F'))
        self.assertEqual(PitchEnum.G, PitchEnum.get_by_str('G'))
        self.assertEqual(PitchEnum.A, PitchEnum.get_by_str('A'))
        self.assertEqual(PitchEnum.B, PitchEnum.get_by_str('B'))

    def test_get_by_str_small_case(self):
        self.assertEqual(PitchEnum.C, PitchEnum.get_by_str('c'))
        self.assertEqual(PitchEnum.D, PitchEnum.get_by_str('d'))
        self.assertEqual(PitchEnum.E, PitchEnum.get_by_str('e'))
        self.assertEqual(PitchEnum.F, PitchEnum.get_by_str('f'))
        self.assertEqual(PitchEnum.G, PitchEnum.get_by_str('g'))
        self.assertEqual(PitchEnum.A, PitchEnum.get_by_str('a'))
        self.assertEqual(PitchEnum.B, PitchEnum.get_by_str('b'))


if __name__ == '__main__':
    unittest.main()
