import unittest
import nzmath.residue as residue

class ResidueTest (unittest.TestCase):
    def testPrimRootDef(self):
        self.assertEqual([2], residue.primRootDef(3))
        self.assertEqual([3,11,12,13,17,21,22,24],residue.primRootDef(31))
        self.assertEqual(\
            [6, 7, 11, 12, 13, 15, 17, 19, 22, 24, 26, 28, 29, 30, 34, 35]\
            , residue.primRootDef(41))
        self.assertEqual(\
            [2, 5, 6, 8, 13, 14, 15, 18, 19, 20, 22, 24, 32, 34, 35, 39, 42\
            , 43, 45, 46, 47, 50, 52, 53, 54, 55, 56, 57, 58, 60, 62, 66, 67\
            , 71, 72, 73, 74, 76, 79, 80]\
            , residue.primRootDef(83))
        self.assertEqual([5, 7, 10, 13, 14, 15, 17, 21, 23, 26, 29, 37,\
            38, 39, 40, 41, 56, 57, 58, 59, 60, 68, 71, 74, 76, 80, 82, 83,\
            84, 87, 90, 92], residue.primRootDef(97))
    def testPrimitive_Root(self):
        self.assertTrue(residue.primitive_root(461) in residue.primRootDef(461))
        self.assertTrue(residue.primitive_root(967) in residue.primRootDef(967))
        self.assertTrue(residue.primitive_root(149) in residue.primRootDef(149))
        self.assertTrue(residue.primitive_root(911) in residue.primRootDef(911))
    def testPrimRootTakagi(self):
        self.assertTrue(residue.primRootTakagi(461) in residue.primRootDef(461))
        self.assertTrue(residue.primRootTakagi(967) in residue.primRootDef(967))
        self.assertTrue(residue.primRootTakagi(149, 147)\
            in residue.primRootDef(149))
        self.assertEqual(2, residue.primRootTakagi(509))

def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
