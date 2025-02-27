import os.path
import shutil
import unittest

from src.cjlutils import FileUtil

base_dir = './temp'


class CreateDirTest(unittest.TestCase):
    def test_create_none(self):
        self.assertFalse(FileUtil.create_dir(None))

    def test_create_empty(self):
        self.assertFalse(FileUtil.create_dir(''))

    def test_create_exists(self):
        dir = f'{base_dir}/test'
        self.assertFalse(os.path.exists(dir))
        self.assertTrue(FileUtil.create_dir(dir))
        self.assertTrue(os.path.exists(dir))

        # 目录已经存在，再次创建
        self.assertTrue(FileUtil.create_dir(dir))
        self.assertTrue(os.path.exists(dir))
        shutil.rmtree(dir)
        self.assertFalse(os.path.exists(dir))

    def test_parent_not_exists_and_create(self):
        parent_dir = f'{base_dir}/parent'
        dir = f'{parent_dir}/test'
        self.assertFalse(os.path.exists(parent_dir))
        self.assertFalse(os.path.exists(dir))
        self.assertTrue(FileUtil.create_dir(dir))
        self.assertTrue(os.path.exists(dir))
        shutil.rmtree(parent_dir)
        self.assertFalse(os.path.exists(dir))

    def test_parent_not_exists_and_no_create(self):
        parent_dir = f'{base_dir}/parent'
        dir = f'{parent_dir}/test'
        self.assertFalse(os.path.exists(parent_dir))
        self.assertFalse(os.path.exists(dir))
        self.assertFalse(FileUtil.create_dir(dir, create_parent=False))
        self.assertFalse(os.path.exists(parent_dir))


class CreateFileTest(unittest.TestCase):
    def test_create_none(self):
        self.assertFalse(FileUtil.create_file(None))

    def test_create_empty(self):
        self.assertFalse(FileUtil.create_file(''))
        self.assertFalse(os.path.exists(''))

    def test_file_creation(self):
        file_path = f'{base_dir}/test.txt'
        content = "This is a test content."
        self.assertFalse(os.path.exists(file_path))

        FileUtil.create_file(file_path, content, create_parent=True)
        self.assertTrue(os.path.isfile(file_path))

        shutil.rmtree(base_dir)
        self.assertFalse(os.path.exists(file_path))

    def test_file_content(self):
        file_path = f'{base_dir}/test.txt'
        content = "This is a test content."
        self.assertFalse(os.path.exists(file_path))

        FileUtil.create_file(file_path, content, create_parent=True)
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path, 'r') as file:
            file_content = file.read()
            self.assertEqual(file_content, content)

        shutil.rmtree(base_dir)
        self.assertFalse(os.path.exists(file_path))

    def test_file_content_None(self):
        file_path = f'{base_dir}/test.txt'
        content = None
        self.assertFalse(os.path.exists(file_path))

        FileUtil.create_file(file_path, content, create_parent=True)
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path, 'r') as file:
            file_content = file.read()
            self.assertEqual(file_content, '')

        shutil.rmtree(base_dir)
        self.assertFalse(os.path.exists(file_path))

    def test_no_parent_creation(self):
        dir = f'{base_dir}/test'
        file_path = f'{dir}/test.txt'
        content = "This is a test content."
        FileUtil.create_file(file_path, content, create_parent=False)
        self.assertFalse(os.path.exists(file_path))

    def test_replace(self):
        file_path = f'{base_dir}/test.txt'
        if os.path.exists(file_path):
            os.remove(file_path)
        content = "This is a test content."
        FileUtil.create_file(file_path, content, create_parent=True)
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path, 'r') as file:
            file_content = file.read()
            self.assertEqual(file_content, content)

        new_content = "This is a new content."
        FileUtil.create_file(file_path, new_content, create_parent=True, replace=True)
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path, 'r') as file:
            file_content = file.read()
            self.assertEqual(file_content, new_content)

        shutil.rmtree(base_dir)
        self.assertFalse(os.path.exists(file_path))


# 测试不完整
class CreateRandomFrequencyAudioFileTest(unittest.TestCase):
    def test_regular(self):
        dir = './temp'
        file_path = f'{dir}/audio.wav'
        FileUtil.create_dir(dir)
        self.assertFalse(FileUtil.is_file(file_path))
        self.assertTrue(FileUtil.create_random_audio_file(file_path, 10))
        self.assertTrue(FileUtil.is_file(file_path))
        FileUtil.remove_file(file_path)


# 测试不完整
class CreateRandomImageFileTest(unittest.TestCase):
    def test_regular(self):
        dir = './temp'
        file_path = f'{dir}/image.png'
        FileUtil.create_dir(dir)
        self.assertFalse(FileUtil.is_file(file_path))
        self.assertTrue(FileUtil.create_random_rgb_image_file(file_path, 350, 500))
        self.assertTrue(FileUtil.is_file(file_path))
        FileUtil.remove_file(file_path)


class CreateRandomVideoFileTest(unittest.TestCase):
    def test_regular(self):
        dir = './temp'
        file_path = f'{dir}/video.mp4'
        FileUtil.create_dir(dir)
        FileUtil.create_random_rgb_video_file(file_path, 350, 300, 10, 30)


class GetFileSizeTest(unittest.TestCase):
    def test_file_not_exists(self):
        self.assertEqual(FileUtil.get_file_size(None), -1)
        self.assertEqual(FileUtil.get_file_size(''), -1)
        self.assertEqual(FileUtil.get_file_size('not_exists.txt'), -1)

    def test_file_exists(self):
        file_path = f'{base_dir}/test.txt'
        content = "This is a test content."
        FileUtil.create_file(file_path, content, create_parent=True, replace=True)
        self.assertTrue(os.path.isfile(file_path))
        self.assertEqual(FileUtil.get_file_size(file_path), len(content))
        shutil.rmtree(base_dir)
        self.assertFalse(os.path.exists(file_path))


class GetFileDataTest(unittest.TestCase):
    def test_file_not_exists(self):
        self.assertIsNone(FileUtil.get_file_data(None))
        self.assertIsNone(FileUtil.get_file_data(''))
        self.assertIsNone(FileUtil.get_file_data('not_exists.txt'))

    def test_file_exists(self):
        file_path = f'{base_dir}/test.txt'
        if os.path.exists(file_path):
            os.remove(file_path)
        content = "This is a test content."
        FileUtil.create_file(file_path, content, create_parent=True, replace=True)
        self.assertTrue(os.path.isfile(file_path))
        self.assertEqual(FileUtil.get_file_data(file_path), content.encode())
        shutil.rmtree(base_dir)
        self.assertFalse(os.path.exists(file_path))


class WriteTextTest(unittest.TestCase):
    def test_one_line(self):
        # 前期准备
        dir_path = './temp/WriteTextTest'
        os.makedirs(dir_path, exist_ok=True)
        file_path = f'{dir_path}/test_common.txt'
        self.assertFalse(os.path.exists(file_path))
        file = open(file_path, 'w')
        file.close()

        # 调用API
        content = 'test content'
        self.assertTrue(FileUtil.write_text(file_path, content, True))

        # 结果校验
        file = open(file_path, 'r')
        lines = file.readlines()
        self.assertEqual(1, len(lines), f'expect {content}, but get {lines}')
        self.assertEqual(content, lines[0])
        file.close()

        # 缓存清理
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)


class WriteBinaryTest(unittest.TestCase):
    def test_one_line(self):
        # 前期准备
        dir_path = './temp/WriteBinaryTest'
        os.makedirs(dir_path, exist_ok=True)
        file_path = f'{dir_path}/test_common.txt'
        self.assertFalse(os.path.exists(file_path))
        file = open(file_path, 'w')
        file.close()

        # 调用API
        content = b'test content'
        self.assertTrue(FileUtil.write_binary(file_path, content, True))

        # 结果校验
        file = open(file_path, 'rb')
        lines = file.readlines()
        self.assertEqual(1, len(lines), f'expect {content}, but get {lines}')
        self.assertEqual(content, lines[0])
        file.close()

        # 缓存清理
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)


class ZipFileTest(unittest.TestCase):
    def test_zip_files(self):
        src_dir = './temp/test_zip_file'
        file_names = [
            '/test1.txt',
            '/test2.txt',
            '/test3.txt',
        ]
        file_paths = [f'{src_dir}/{x}' for x in file_names]
        output_path = f'{src_dir}/test.zip'
        for file_path in file_paths:
            FileUtil.create_file(file_path, FileUtil.get_name(file_path), create_parent=True)
        [self.assertTrue(os.path.isfile(path)) for path in file_paths]

        FileUtil.zip_files(file_paths, output_path)
        self.assertTrue(os.path.isfile(output_path))

        [FileUtil.remove_file(path) for path in file_paths]
        FileUtil.remove_file(output_path)


class ZipDocumentTest(unittest.TestCase):
    def test_zip_my_document(self):
        base_dir = '/Users/chenjili/Desktop/长沙银行'
        src_dir = f'{base_dir}/in'
        output_path = f'{base_dir}/out/NIM_iOS_SDK_v7.8.5.zip'
        FileUtil.zip_document(src_dir, output_path)

    def test_zip_document(self):
        base_dir = './temp/test_zip_document'
        src_dir = f'{base_dir}/0'
        file_path = f'{src_dir}/1/2/3/4/test.txt'
        output_path = f'{base_dir}/test.zip'
        FileUtil.create_file(file_path, FileUtil.get_name(file_path), create_parent=True)
        self.assertTrue(os.path.isfile(file_path))
        FileUtil.zip_document(src_dir, output_path)


if __name__ == '__main__':
    unittest.main()
