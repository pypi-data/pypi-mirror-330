import unittest

from src.cjlutils import BytesUtil


class ToAndFromListMatchTest(unittest.TestCase):
    def test_none(self):
        origin = None
        encoded = BytesUtil.to_list(origin)
        decoded = BytesUtil.from_list(encoded)
        self.assertEqual(origin, decoded)

    def test_empty(self):
        origin = b''
        encoded = BytesUtil.to_list(origin)
        decoded = BytesUtil.from_list(encoded)
        self.assertEqual(origin, decoded)

    def test_single(self):
        origin = b'\x80'
        encoded = BytesUtil.to_list(origin)
        decoded = BytesUtil.from_list(encoded)
        self.assertEqual(origin, decoded)

    def test_multiple(self):
        origin = b''.join([bytes([i]) for i in range(256)])
        encoded = BytesUtil.to_list(origin)
        decoded = BytesUtil.from_list(encoded)
        self.assertEqual(origin, decoded)


class ToListTest(unittest.TestCase):
    def test_none(self):
        origin = None
        encoded = BytesUtil.to_list(origin)
        self.assertEqual(None, encoded)

    def test_empty(self):
        origin = b''
        encoded = BytesUtil.to_list(origin)
        self.assertEqual([], encoded)

    def test_single(self):
        for i in range(256):
            origin = bytes([i])
            encoded = BytesUtil.to_list(origin)
            self.assertEqual([i], encoded)

    def test_multiple(self):
        origin = b''.join([bytes([i]) for i in range(256)])
        encoded = BytesUtil.to_list(origin)
        self.assertEqual(list(range(256)), encoded)


class FromListTest(unittest.TestCase):
    def test_none(self):
        origin = None
        decoded = BytesUtil.from_list(origin)
        self.assertEqual(None, decoded)

    def test_empty(self):
        origin = []
        decoded = BytesUtil.from_list(origin)
        self.assertEqual(b'', decoded)

    def test_single(self):
        for i in range(256):
            origin = [i]
            decoded = BytesUtil.from_list(origin)
            print(decoded)
            self.assertEqual(bytes([i]), decoded)

    def test_single_invalid(self):
        origin = [-1]
        decoded = BytesUtil.from_list(origin)
        self.assertEqual(None, decoded)

        origin = [256]
        decoded = BytesUtil.from_list(origin)
        self.assertEqual(None, decoded)

    def test_multiple(self):
        origin = list(range(256))
        decoded = BytesUtil.from_list(origin)
        self.assertEqual(b''.join([bytes([i]) for i in range(256)]), decoded)

    def test_multiple_invalid(self):
        origin = list(range(256))
        origin[0] = -1
        decoded = BytesUtil.from_list(origin)
        self.assertEqual(None, decoded)

        origin = list(range(256))
        origin[0] = 256
        decoded = BytesUtil.from_list(origin)
        self.assertEqual(None, decoded)


if __name__ == '__main__':
    unittest.main()
