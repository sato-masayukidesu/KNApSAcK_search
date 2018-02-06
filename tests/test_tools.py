import unittest
import time
import sys
sys.path.append("../new_version")
import tools


class Test_tools(unittest.TestCase):
    """
    test for control_all_genus
    """

    def test_search_all_Cnumber_from_label(self):
        """
        test for search_all_Cnumber_from_label
        """
        expected = (['C00001546', 'C00017854', 'C00017855', 'C00027106',
                    'C00036583', 'C00037061', 'C00045424', 'C00045427'], 8)
        label = "N1b-C2c-S2a"
        actual = tools.search_all_Cnumber_from_label(label)
        self.assertEqual(actual, expected)

    def test_get_name(self):
        """
        test for get_name
        """
        expected = "4-Hydroxybenzaldehyde"
        Cnumber = "C00002657"
        actual = tools.get_name(Cnumber)
        time.sleep(2)
        self.assertEqual(actual, expected)

    def test_get_genuses(self):
        """
        test for get_genuses
        """
        expected = ['Brassica campestris', 'Brassica carinata',
                    'Brassica napus', 'Brassica oleracea', 'Brassica rapa',
                    'Brassica sativus']
        actual = tools.get_genuses("C00001546")
        time.sleep(2)
        self.assertEqual(actual, expected)

    def test_make_mol_object(self):
        """
        test for get_specifics
        """
        Cn_list = ['C00001546', 'C00017854', 'C00017855', 'C00027106',
                   'C00036583', 'C00037061', 'C00045424', 'C00045427']
        mol_list = tools.make_mol_object(Cn_list)
        for mol in mol_list:
            self.assertIsNotNone(mol)


if __name__ == "__main__":
    unittest.main()
