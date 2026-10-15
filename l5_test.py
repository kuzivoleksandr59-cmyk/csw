import unittest
from lab5 import validate_brackets, check_brackets


class TestBracketValidator(unittest.TestCase):

    def test_valid_brackets(self):
        self.assertTrue(validate_brackets("()"))
        self.assertTrue(validate_brackets("<div><p>{ test }</p></div>"))
        self.assertTrue(validate_brackets("text without brackets"))

    def test_invalid_brackets_raises_error(self):
        with self.assertRaises(ValueError):
            validate_brackets("<div><p>{ test }}</p</div>")

    def test_invalid_indices(self):
        is_valid, indices = check_brackets("({[}")
        self.assertFalse(is_valid)
        self.assertTrue(len(indices) > 0)


if __name__ == "__main__":
    unittest.main()