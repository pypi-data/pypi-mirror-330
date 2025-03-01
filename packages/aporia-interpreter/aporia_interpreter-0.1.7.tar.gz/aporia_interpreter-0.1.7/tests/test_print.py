import unittest
from tests.util import interpret

class TestPrint(unittest.TestCase):
    def test_one_exp_arg(self):
        source = """
        true: print(2)
        """
        self.assertEqual('2', interpret(source))

    def test_str_with_exp(self):
        source = """
        true: print("this is a nine: ", 9)
        """
        self.assertEqual("this is a nine: 9", interpret(source))

    def test_one_str(self):
        source = """
        true: print("hello world")
        """
        self.assertEqual("hello world", interpret(source))


if __name__ == '__main__':
    unittest.main()
