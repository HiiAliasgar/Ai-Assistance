import unittest

from main import calculator, say_hello


class CalculatorTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(calculator.invoke({"expression": "(2 + 3) * 4"}), "The result is 20.")

    def test_division_by_zero_is_reported(self):
        self.assertEqual(calculator.invoke({"expression": "1 / 0"}), "I cannot divide by zero.")

    def test_rejects_code_execution(self):
        result = calculator.invoke({"expression": "__import__('os').system('echo unsafe')"})
        self.assertIn("only evaluate arithmetic", result)

    def test_rejects_boolean_constants(self):
        result = calculator.invoke({"expression": "True + 1"})
        self.assertIn("only evaluate arithmetic", result)

    def test_rejects_unbounded_power(self):
        result = calculator.invoke({"expression": "2 ** 1000000"})
        self.assertIn("only evaluate arithmetic", result)

    def test_rejects_overlong_expression(self):
        result = calculator.invoke({"expression": "1+" * 200 + "1"})
        self.assertIn("only evaluate arithmetic", result)

    def test_greeting_normalizes_whitespace(self):
        self.assertEqual(say_hello.invoke({"name": "  Ada   Lovelace  "}), "Hello Ada Lovelace! I hope you are well today.")


if __name__ == "__main__":
    unittest.main()
