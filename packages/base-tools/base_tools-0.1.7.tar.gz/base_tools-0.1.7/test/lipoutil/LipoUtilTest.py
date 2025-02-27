import os
import unittest

from src.cjlutils import LipoUtil

lib_fat = './libs/libgtest_main.a'
lib_arm64 = './libs/libgtest_main_arm64.a'

ERROR_DESC_NO_INPUT_FILES_SPECIFIED = 'no input files specified'
ERROR_DESC_NO_SUCH_FILE_OR_DIRECTORY = 'No such file or directory'
ERROR_DESC_ARCHITECTURES_IN_THE_FAT_FILE = 'Architectures in the fat file'
ERROR_DESC_NON_FAT_FILE = 'Non-fat file'
ERROR_DESC_CANT_OPEN_INPUT_FILE = 'can\'t open input file'
ERROR_DESC_DOES_NOT_CONTAIN_THE_SPECIFIED_ARCHITECTURE = 'does not contain the specified architecture'


class CreateTest(unittest.TestCase):

    def test_none_none(self):
        result = LipoUtil.create(None, None)
        self.assertTrue(result.stderr.find(ERROR_DESC_NO_INPUT_FILES_SPECIFIED) >= 0)

    def test_empty_empty(self):
        result = LipoUtil.create([], '')
        self.assertTrue(result.stderr.find(ERROR_DESC_NO_INPUT_FILES_SPECIFIED) >= 0)

    def test_empty_none(self):
        result = LipoUtil.create([], None)
        self.assertTrue(result.stderr.find(ERROR_DESC_NO_INPUT_FILES_SPECIFIED) >= 0)

    def test_none_empty(self):
        result = LipoUtil.create(None, '')
        self.assertTrue(result.stderr.find(ERROR_DESC_NO_INPUT_FILES_SPECIFIED) >= 0)

    def test_has_none(self):
        output_path = './out.a'
        result = LipoUtil.create([None], output_path)
        self.assertTrue(result.stderr.find(ERROR_DESC_NO_INPUT_FILES_SPECIFIED) >= 0)

    def test_has_empty(self):
        output_path = './out.a'
        result = LipoUtil.create([''], output_path)
        self.assertTrue(result.stderr.find(ERROR_DESC_NO_INPUT_FILES_SPECIFIED) >= 0)

    def test_has_libgtest_main(self):
        output_path = './out.a'
        result = LipoUtil.create([lib_fat], output_path)
        self.assertEqual('', result.stderr)
        self.assertTrue(os.path.isfile(output_path))
        os.remove(output_path)
        self.assertFalse(os.path.exists(output_path))


class InfoTest(unittest.TestCase):

    def test_none(self):
        result = LipoUtil.info(None)
        self.assertTrue(result.stderr.find(ERROR_DESC_NO_SUCH_FILE_OR_DIRECTORY) >= 0)

    def test_empty(self):
        result = LipoUtil.info('')
        self.assertTrue(result.stderr.find(ERROR_DESC_NO_SUCH_FILE_OR_DIRECTORY) >= 0)

    def test_fat_file(self):
        result = LipoUtil.info(lib_fat)
        self.assertEqual('', result.stderr)
        self.assertTrue(result.stdout.find(ERROR_DESC_ARCHITECTURES_IN_THE_FAT_FILE) >= 0)

    def test_thin_file(self):
        result = LipoUtil.info(lib_arm64)
        self.assertEqual('', result.stderr)
        self.assertTrue(result.stdout.find(ERROR_DESC_NON_FAT_FILE) >= 0)


class ThinTest(unittest.TestCase):
    def test_none_none_none(self):
        result = LipoUtil.thin(None, None, None)
        self.assertTrue(result.stderr.find(ERROR_DESC_CANT_OPEN_INPUT_FILE) >= 0)
        self.assertTrue(len(result.stderr) > 0)

    def test_empty_empty_empty(self):
        result = LipoUtil.thin('', None, '')
        self.assertTrue(result.stderr.find(ERROR_DESC_CANT_OPEN_INPUT_FILE) >= 0)

    def test_none_any_none(self):
        result = LipoUtil.thin(None, LipoUtil.Architecture.ANY, None)
        self.assertTrue(result.stderr.find(ERROR_DESC_CANT_OPEN_INPUT_FILE) >= 0)

    def test_empty_any_empty(self):
        result = LipoUtil.thin('', LipoUtil.Architecture.ANY, '')
        self.assertTrue(result.stderr.find(ERROR_DESC_CANT_OPEN_INPUT_FILE) >= 0)

    def test_other_architecture(self):
        out_path = './temp/out.a'
        self.assertFalse(os.path.exists(out_path))
        result = LipoUtil.thin(lib_fat, LipoUtil.Architecture.I386, out_path)
        self.assertTrue(result.stderr.find(ERROR_DESC_DOES_NOT_CONTAIN_THE_SPECIFIED_ARCHITECTURE) >= 0)
        self.assertFalse(os.path.exists(out_path))

    def test_arm64_architecture(self):
        out_path = './temp/out_arm64.a'
        self.assertFalse(os.path.exists(out_path))
        result = LipoUtil.thin(lib_fat, LipoUtil.Architecture.ARM64, out_path)
        self.assertTrue(result.stderr == '')
        self.assertTrue(os.path.exists(out_path))
        os.remove(out_path)
        self.assertFalse(os.path.exists(out_path))


class GetArchitecturesTest(unittest.TestCase):
    def test_none(self):
        result = LipoUtil.get_architectures(None)
        self.assertIsNotNone(result)
        self.assertEqual(0, len(result))

    def test_empty(self):
        result = LipoUtil.get_architectures('')
        self.assertIsNotNone(result)
        self.assertEqual(0, len(result))

    def test_fat_file(self):
        result = LipoUtil.get_architectures(lib_fat)
        self.assertIsNotNone(result)
        self.assertEqual({LipoUtil.Architecture.ARM64, LipoUtil.Architecture.X86_64, LipoUtil.Architecture.ARM64.ARMV7},
                         result)

    def test_thin_file(self):
        result = LipoUtil.get_architectures(lib_arm64)
        self.assertIsNotNone(result)
        self.assertEqual({LipoUtil.Architecture.ARM64}, result)


if __name__ == '__main__':
    unittest.main()
