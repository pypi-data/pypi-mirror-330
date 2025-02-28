"""Test Address with keyword arguments"""

import unittest
import paf

class TestKwargs(unittest.TestCase):
    """Test Address Keyword Arguments"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address(
            organisation_name="KATH'S CAKES",
            building_name="VICTORIA HOUSE",
            thoroughfare_name="HIGH",
            thoroughfare_descriptor="STREET",
            post_town="PORTSMOUTH",
            postcode="PO1 1AF"
            )

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "KATH'S CAKES",
            "VICTORIA HOUSE",
            "HIGH STREET",
            "PORTSMOUTH",
            "PO1 1AF"
            ]
        self.assertEqual(self.address.as_list(), address, "Incorrect Kwargs list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "KATH'S CAKES, VICTORIA HOUSE, HIGH STREET, PORTSMOUTH. PO1 1AF"
        self.assertEqual(self.address.as_str(), address, "Incorrect Kwargs string format")

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = (
            "KATH'S CAKES",
            "VICTORIA HOUSE",
            "HIGH STREET",
            "PORTSMOUTH",
            "PO1 1AF"
            )
        self.assertEqual(self.address.as_tuple(), address, "Incorrect Kwargs tuple format")

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "KATH'S CAKES",
            'line_2': "VICTORIA HOUSE",
            'line_3': "HIGH STREET",
            'post_town': "PORTSMOUTH",
            'postcode': "PO1 1AF"
            }
        self.assertEqual(self.address.as_dict(), address, "Incorrect Kwargs dict format")

    def test_premises(self):
        """Test premises"""
        premises = {
            'premises_name': 'VICTORIA HOUSE'
            }
        self.assertEqual(self.address.premises(), premises, "Incorrect Kwargs premises")

if __name__ == '__main__':
    unittest.main()
