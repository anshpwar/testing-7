import unittest

from lmskit import contract


class ContractTests(unittest.TestCase):
    def test_build_summary(self):
        rec = contract.Record("EN-1", 1250, "open")
        self.assertEqual(
            contract.build_summary(rec),
            {"ref": "EN-1", "amount": 1250, "status": "open", "currency": "USD"},
        )

    def test_describe(self):
        summary = {"ref": "EN-2", "status": "closed", "amount": 99, "currency": "EUR"}
        self.assertEqual(contract.describe(summary), "EN-2 closed 99 EUR")
