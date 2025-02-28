"""Test Address Rule X formatting"""

import unittest
import paf

class TestRuleXWithSubBuildingName(unittest.TestCase):
    """Test Address Rule X with Sub-Building Name Exception"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'sub_building_name': "30C",
            'dependent_thoroughfare_name': "JENNENS",
            'dependent_thoroughfare_descriptor': "COURT",
            'thoroughfare_name': "JENNENS",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "BIRMINGHAM",
            'postcode': "B5 5JR"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["30C JENNENS COURT", "JENNENS ROAD", "BIRMINGHAM", "B5 5JR"]
        self.assertEqual(
            self.address.as_list(), address, "Incorrect Rule X w/ sub-building list format"
            )

    def test_string(self):
        """Test conversion to a string"""
        address = "30C JENNENS COURT, JENNENS ROAD, BIRMINGHAM. B5 5JR"
        self.assertEqual(
            self.address.as_str(), address, "Incorrect Rule X w/ sub-building string format"
            )

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("30C JENNENS COURT", "JENNENS ROAD", "BIRMINGHAM", "B5 5JR")
        self.assertEqual(
            self.address.as_tuple(), address, "Incorrect Rule X w/ sub-building tuple format"
            )

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "30C JENNENS COURT",
            'line_2': "JENNENS ROAD",
            'post_town': "BIRMINGHAM",
            'postcode': "B5 5JR"
            }
        self.assertEqual(
            self.address.as_dict(), address, "Incorrect Rule X w/ sub-building dict format"
            )

    def test_premises(self):
        """Test premises"""
        premises = {
            'premises_name': 'JENNENS COURT',
            'sub_premises_number': 30,
            'sub_premises_suffix': 'C'
            }
        self.assertEqual(
            self.address.premises(), premises, "Incorrect Rule X w/ sub-building premises"
            )

class TestRuleXWithoutSubBuildingName(unittest.TestCase):
    """Test Address Rule X without Sub-Building Name Exception"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'sub_building_name': "THE ANNEX",
            'thoroughfare_name': "ST MARYS",
            'thoroughfare_descriptor': "ROAD",
            'dependent_locality': "BIRNAM",
            'post_town': "DUNKELD",
            'postcode': "PH8 0BJ"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["THE ANNEX", "ST MARYS ROAD", "BIRNAM", "DUNKELD", "PH8 0BJ"]
        self.assertEqual(
            self.address.as_list(), address, "Incorrect Rule X w/o sub-building list format"
            )

    def test_string(self):
        """Test conversion to a string"""
        address = "THE ANNEX, ST MARYS ROAD, BIRNAM, DUNKELD. PH8 0BJ"
        self.assertEqual(
            self.address.as_str(), address, "Incorrect Rule X w/o sub-building string format"
            )

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("THE ANNEX", "ST MARYS ROAD", "BIRNAM", "DUNKELD", "PH8 0BJ")
        self.assertEqual(
            self.address.as_tuple(), address, "Incorrect Rule X w/o sub-building tuple format"
            )

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "THE ANNEX",
            'line_2': "ST MARYS ROAD",
            'line_3': "BIRNAM",
            'post_town': "DUNKELD",
            'postcode': "PH8 0BJ"
            }
        self.assertEqual(
            self.address.as_dict(), address, "Incorrect Rule X w/o sub-building tuple format"
            )

    def test_premises(self):
        """Test premises"""
        premises = {'premises_name': 'THE ANNEX'}
        self.assertEqual(
            self.address.premises(), premises, "Incorrect Rule X w/o sub-building premises"
            )

if __name__ == '__main__':
    unittest.main()
