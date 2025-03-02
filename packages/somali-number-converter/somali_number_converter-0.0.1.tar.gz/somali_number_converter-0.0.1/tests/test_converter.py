import unittest
from somali_number_converter import replace_numbers_with_somali

class TestSomaliNumberConverter(unittest.TestCase):
    def test_replace_numbers(self):
        text = "Waxaa haystaa 2 moos iyo 1 shukulaato."
        expected = "Waxaa haystaa laba moos iyo hal shukulaato."
        self.assertEqual(replace_numbers_with_somali(text), expected)

if __name__ == '__main__':
    unittest.main()
