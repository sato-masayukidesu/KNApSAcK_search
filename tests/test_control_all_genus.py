import unittest
import os
import sys
sys.path.append("../new_version")
from classes2 import control_all_genus
import shutil


class Test_control_all_genus(unittest.TestCase):
    """
    test for control_all_genus
    """

    def test_get_number_of_Cnumber(self):
        """
        test for make_kcfs
        """
        path = "test"
        expected = [('C00002198', 19), ('C00002151', 14), ('C00003672', 11),
                    ('C00002503', 11), ('C00002499', 11)]
        cag = control_all_genus(path)
        Cn_dict = cag.get_number_of_Cnumber()
        for Cn, exnumber in expected:
            actual = Cn_dict[Cn]
            self.assertEqual(actual, exnumber)

    def test_get_split_kcfs(self):
        """
        test for get_split_kcfs
        """
        path = "test"
        expected = 3613
        cag = control_all_genus(path)
        actual = cag.get_split_kcfs()[('RING', 'C-C-C-C-C-C')]
        self.assertEqual(actual, expected)

    def test_get_Cnumber_from_label(self):
        """
        test for get_Cnumber_from_label
        """
        path = "test"
        expected = {'Citrus': ['C00000001', 'C00000003', 'C00000004',
                               'C00000008', 'C00000009', 'C00000017',
                               'C00000019', 'C00000020', 'C00000024',
                               'C00000025', 'C00000029', 'C00000044',
                               'C00000053', 'C00000081', 'C00001388',
                               'C00002074']}
        cag = control_all_genus(path)
        actual = cag.get_Cnumber_from_label('C1y-C6a-O6a')
        self.assertEqual(actual, expected)

    def test_get_specifics(self):
        """
        test for get_specifics
        """
        path = "test"
        expected = [(('TRIPLET', 'C1y-C6a-O6a'), (32, 'Citrus')),
                    (('TRIPLET', 'O-P-O'), (24, 'Citrus')),
                    (('VICINITY', 'C6a(C1y+O6a+O6a)'), (16, 'Citrus')),
                    (('BOND', 'C1y-C6a'), (16, 'Citrus')),
                    (('BOND', 'O-P'), (16, 'Citrus'))]
        cag = control_all_genus(path)
        specific = cag.get_specifics()
        for label, exnumgenus in expected:
            actual = specific[label]
            self.assertEqual(actual, exnumgenus)


if __name__ == "__main__":
    unittest.main()
