import unittest

from safety import check_plan


class SafetyTests(unittest.TestCase):
    def test_accepts_a_title_check(self):
        steps = [
            {
                "action": "assert_title",
                "by": "text",
                "role": "heading",
                "target": "Example Domain",
                "value": ""
            }
        ]
        check_plan(steps)

    def test_rejects_a_plan_without_verification(self):
        steps = [
            {
                "action": "click",
                "by": "role",
                "role": "button",
                "target": "Learn more",
                "value": ""
            }
        ]
        with self.assertRaises(ValueError):
            check_plan(steps)

    def test_rejects_a_sensitive_navigation_target(self):
        steps = [
            {
                "action": "navigate",
                "by": "text",
                "role": "link",
                "target": "https://example.com/checkout",
                "value": ""
            },
            {
                "action": "assert_title",
                "by": "text",
                "role": "heading",
                "target": "Checkout",
                "value": ""
            }
        ]
        with self.assertRaises(ValueError):
            check_plan(steps)


if __name__ == "__main__":
    unittest.main()
