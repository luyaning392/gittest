import unittest

from detector import detect


class DetectorTests(unittest.TestCase):
    def test_public_security_scam_is_high_risk(self):
        result = detect("我是公安局的，你涉嫌洗钱，请立即将资金转入安全账户配合调查")
        self.assertEqual(result["level"], "high")
        self.assertIn("冒充公检法诈骗", result["scam_types"])

    def test_emergency_relative_request_is_high_risk(self):
        result = detect("妈，我换号了，我出事了，在医院急需打钱")
        self.assertEqual(result["level"], "high")
        self.assertIn("冒充亲友/紧急求助诈骗", result["scam_types"])

    def test_normal_text_is_low_risk(self):
        result = detect("今天天气不错，一起去公园散步吧")
        self.assertEqual(result["level"], "low")
        self.assertEqual(result["hits"], [])

    def test_empty_text_is_low_risk(self):
        result = detect("   ")
        self.assertEqual(result["level"], "low")


if __name__ == "__main__":
    unittest.main()
