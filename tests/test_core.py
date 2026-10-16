import math
import unittest
from tmga.core import conf_ethical, cbp_triggered, reference_drift_warning

class CoreTests(unittest.TestCase):
    def test_confidence_zero_uncertainty(self):
        self.assertAlmostEqual(conf_ethical([1.0], [1.0], 0.0), 1.0)
    def test_confidence_decay(self):
        self.assertAlmostEqual(conf_ethical([1.0], [1.0], 1.0), math.exp(-1))
    def test_infinite_uncertainty(self):
        self.assertEqual(conf_ethical([1.0], [1.0], math.inf), 0.0)
    def test_invalid_inputs(self):
        for args in [([1.2],[1],0),([1],[1],-1),([1],[1.1],0)]:
            with self.assertRaises(ValueError): conf_ethical(*args)
    def test_warning_not_authorization(self):
        self.assertTrue(reference_drift_warning([.06,.08,.12], .05))
        self.assertEqual(reference_drift_warning([.06,.08,.12], .05),cbp_triggered([.06,.08,.12], .05))
        self.assertFalse(reference_drift_warning([.12,.12,.12], .05))

if __name__ == '__main__': unittest.main()
