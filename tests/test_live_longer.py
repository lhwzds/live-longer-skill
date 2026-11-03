import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "live_longer.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def years(out, factor):
    line = next(l for l in out.splitlines() if l.startswith(factor))
    return float(line.split()[-1])


class LiveLongerTest(unittest.TestCase):
    def test_example(self):
        r = run("--steps", "4000:7000", "--nuts", "0:28", "--fruitveg", "200:400", "--sleep", "6:7")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(years(r.stdout, "nuts"), 2.9)
        self.assertEqual(years(r.stdout, "fruitveg"), 1.2)
        self.assertNotIn("combined", r.stdout)

    def test_same_level_is_zero(self):
        self.assertEqual(years(run("--bmi=27:27").stdout, "bmi"), 0.0)

    def test_negative_fitness_change(self):
        self.assertEqual(years(run("--fitness=-2:0").stdout, "fitness"), 3.2)

    def test_less_sleep_from_normal_is_a_loss(self):
        self.assertEqual(years(run("--sleep=7:5").stdout, "sleep"), -1.3)

    def test_rejected_inputs(self):
        for arg in ("--steps=nan:5000", "--bmi=20:25", "--fitness=0:10000", "--sleep=6:10", "--sleep=9.5:7",
                    "--nuts=10:", "--nuts=10"):
            self.assertNotEqual(run(arg).returncode, 0, arg)


if __name__ == "__main__":
    unittest.main()
