import unittest
from src.core.pii_detection import detect_emails  # Adjust import based on your project structure

class TestPIIDetection(unittest.TestCase):
    def test_detect_emails(self):
        # Test cases
        test_cases = [
            ("My email is john.doe@example.com", ["john.doe@example.com"]),
            ("Contact me at jane_doe123@mail.org", ["jane_doe123@mail.org"]),
            ("Send it to admin+support@company.co.uk", ["admin+support@company.co.uk"]),
            ("No emails here!", []),  # No email in text
            ("Invalid email like john.doe@.com", []),  # Invalid email format
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(detect_emails(input_text), expected)

if __name__ == "__main__":
    unittest.main()