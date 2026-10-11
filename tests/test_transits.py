import tempfile
from pathlib import Path
import unittest
from src.transits import load_curve, search
from run import generate_demo


class TransitTests(unittest.TestCase):
    def test_injected_period_is_recovered_on_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'curve.csv'
            generate_demo(path)
            best,_ = search(load_curve(path))
        self.assertLessEqual(abs(best['period_days']-3),0.04)
        self.assertGreater(best['relative_depth'],0.01)

    def test_constant_curve_has_no_dip(self):
        rows = [(i*0.05,1.0) for i in range(400)]
        best,_ = search(rows)
        self.assertIsNone(best)

    def test_period_longer_than_half_baseline_rejected(self):
        with self.assertRaisesRegex(ValueError,'two cycles'):
            search([(i*0.05,1.0) for i in range(100)])

    def test_duplicate_or_nonfinite_curve_rejected(self):
        for invalid in ['0,1\n0,1\n','0,nan\n1,1\n']:
            with tempfile.TemporaryDirectory() as d:
                path = Path(d)/'curve.csv'
                path.write_text('time_days,flux\n'+invalid,encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_curve(path)
