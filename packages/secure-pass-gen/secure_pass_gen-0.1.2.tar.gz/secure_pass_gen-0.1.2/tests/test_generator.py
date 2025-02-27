import unittest
from password_generator.generator import generate_password


class TestPasswordGenerator(unittest.TestCase):

    def test_password_length(self):
        password = generate_password(14)
        self.assertEqual(len(password), 14)

    def test_password_not_empty(self):
        password = generate_password()
        self.assertTrue(bool(password))

    def test_password_contains_all_characters(self):
        password = generate_password(20)
        self.assertTrue(any(c.isupper() for c in password))  # Uppercase check
        self.assertTrue(any(c.islower() for c in password))  # Lowercase check
        self.assertTrue(any(c.isdigit() for c in password))  # Digit check
        self.assertTrue(
            any(c in "!@#$%^&*()_+" for c in password)
        )  # Special char check

    def test_password_min_length(self):
        with self.assertRaises(ValueError):
            generate_password(6)  # Should raise an error


if __name__ == "__main__":
    unittest.main()
