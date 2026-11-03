#!/usr/bin/env python3
"""Years of life a habit change may add, from published all-cause mortality hazard ratios.

  years ~= (8 / ln 2) * ln(HR_now / HR_target)
Adult all-cause mortality roughly doubles every 8 years (Gompertz), so lowering the death rate
to HR times its level at every age shifts the survival curve by about -ln(HR) / (ln 2 / 8) years,
a rough life-expectancy difference that assumes the association is causal.

All paper data lives in ../references/evidence.json; this file holds no numbers from papers.
Usage: live_longer.py --steps 4000:8000 --nuts 0:28 --fruitveg 200:400 --bmi 28:25 \
                      --sleep 6:7 --fitness 0:1
Each flag is NOW:TARGET (for fitness, the change in METs: 0:1 = +1 MET; 1 MET = 3.5 ml/kg/min VO2max).
"""
import argparse
import json
import math
from pathlib import Path

EVIDENCE = json.loads((Path(__file__).resolve().parent.parent / "references" / "evidence.json").read_text())
YEARS_PER_LN_HR = 8 / math.log(2)  # ~11.5


def hazard(f, x):
    """HR at level x relative to the factor's reference, by the model stored in evidence.json."""
    model = f["model"]
    if model == "points":
        pts = f["points"]
        if x <= pts[0][0]:
            return pts[0][1]
        for (x0, h0), (x1, h1) in zip(pts, pts[1:]):
            if x <= x1:
                t = (x - x0) / (x1 - x0)
                return math.exp(math.log(h0) + t * (math.log(h1) - math.log(h0)))
        return pts[-1][1]
    if model == "per_unit_change":  # x is a signed change, e.g. -1 MET
        return f["hr_per_unit"] ** (x / f["per"])
    if model == "per_unit":
        x = min(x, f.get("max", x))
        x = max(x - f.get("min", 0), 0)
        return f["hr_per_unit"] ** (x / f["per"])
    if model == "bands":
        for lo, hi, hr in f["bands"]:
            if (lo is None or x >= lo) and (hi is None or x <= hi):
                return hr
        return 1.0
    raise ValueError(f"unknown model {model}")


def years(hr_ratio):
    return YEARS_PER_LN_HR * math.log(1 / hr_ratio)


def pair(text):
    now, sep, target = text.partition(":")
    if not sep or not target:
        raise argparse.ArgumentTypeError("use NOW:TARGET, e.g. 4000:7000")
    return float(now), float(target)


def check(ap, name, f, value):
    lo, hi = f["range"]
    if not all(math.isfinite(v) and lo <= v <= hi for v in value):
        ap.error(f"--{name} values must be between {lo:g} and {hi:g} {f['unit']} (the range the model covers)")


def main():
    factors = EVIDENCE["factors"]
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for name, f in factors.items():
        ap.add_argument(f"--{name}", type=pair, metavar="NOW:TARGET", help=f["unit"])
    args = ap.parse_args()

    rows = []
    for name, f in factors.items():
        value = getattr(args, name)
        if value is not None:
            check(ap, name, f, value)
            now, target = value
            rows.append((name, now, target, hazard(f, target) / hazard(f, now)))
    if not rows:
        ap.error("give at least one factor")

    print(f"{'factor':<9}{'now':>8}{'target':>8}{'HR':>7}{'years':>7}")
    for name, now, target, ratio in sorted(rows, key=lambda r: r[3]):
        print(f"{name:<9}{now:>8g}{target:>8g}{ratio:>7.2f}{years(ratio):>+7.1f}")
    print("\nObservational associations, not a promise; the habits overlap, so do not add the years up.")
    print("\nSources:")
    for name, *_ in rows:
        src = factors[name]["source"]
        print(f"  {name}: {src['cite']}. doi:{src['doi']}")


if __name__ == "__main__":
    main()
