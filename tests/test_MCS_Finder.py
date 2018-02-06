import unittest
import os
import sys
sys.path.append("../new_version")
from classes2 import MCS_Finder
import shutil


class Test_MCS_Finder(unittest.TestCase):
    """
    test for MCS_Finder
    """

    def test_make_kcfs(self):
        """
        test for make_kcfs
        """
        genus = "Citrus"
        if os.path.exists(genus):
            shutil.rmtree(genus)
        f = MCS_Finder(genus)
        f.make_kcfs2()
        kcfspath = genus + "/kcfs.kcfs"
        kcfscountpath = genus + "/kcfscount.txt"
        splitcountpath = genus + "/splitedcount.txt"
        self.assertTrue(os.path.exists(kcfspath))
        self.assertTrue(os.path.exists(kcfscountpath))
        self.assertTrue(os.path.exists(splitcountpath))
        shutil.rmtree(genus)


if __name__ == "__main__":
    unittest.main()
