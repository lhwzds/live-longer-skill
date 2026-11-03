# live-longer-skill

A minimal [Agent Skill](https://agentskills.io) that estimates how many years of life a habit change may add: daily steps, fitness, sleep, fruit and vegetables, nuts and BMI.

- `references/evidence.json`: the data store. For each factor, the all-cause mortality hazard ratios with 95% CIs, the dose-response model, citation, DOI and study design, all checked against the papers.
- `scripts/live_longer.py`: the arithmetic. It reads only `evidence.json`. Python 3 standard library only, no network.
- `tests/`: `python3 -m unittest discover -s tests`.
- `SKILL.md`: what the agent asks, how it runs the script, and the caveats it must state.

Years come from the Gompertz rule: adult mortality roughly doubles every 8 years, so a hazard ratio HR corresponds to roughly `(8 / ln 2) × ln(1/HR) ≈ 11.5 × ln(1/HR)` years.

## Install

```sh
git clone https://github.com/lhwzds/live-longer-skill ~/.claude/skills/live-longer
```

## Run it directly

Each flag is `NOW:TARGET` (`--fitness` is the change in METs):

```sh
python3 scripts/live_longer.py --steps 4000:7000 --nuts 0:28 --fruitveg 200:400 --sleep 6:7
```

```
factor        now  target     HR  years
steps        4000    7000   0.63   +5.3
nuts            0      28   0.78   +2.9
sleep           6       7   0.89   +1.3
fruitveg      200     400   0.90   +1.2

Observational associations, not a promise; the habits overlap, so do not add the years up.
```

The script also prints the source of each factor. The steps figure is probably the most inflated: people who walk little include some who are already ill.

## Sources

| Factor | Source |
| --- | --- |
| Steps | Paluch et al., Lancet Public Health 2022 ([doi](https://doi.org/10.1016/S2468-2667(21)00302-9)) |
| Fitness | Kodama et al., JAMA 2009 ([doi](https://doi.org/10.1001/jama.2009.681)) |
| Fruit and vegetables | Aune et al., Int J Epidemiol 2017 ([doi](https://doi.org/10.1093/ije/dyw319)) |
| Nuts | Aune et al., BMC Medicine 2016 ([doi](https://doi.org/10.1186/s12916-016-0730-3)) |
| BMI | Global BMI Mortality Collaboration, Lancet 2016 ([doi](https://doi.org/10.1016/S0140-6736(16)30175-1)) |
| Sleep | Cappuccio et al., Sleep 2010 ([doi](https://doi.org/10.1093/sleep/33.5.585)) |

## Limits

These are observational associations, so treat the years as rough estimates of direction and size. The habits overlap, so do not add the years up. Values outside a factor's modelled range (for example BMI under 22.5) are rejected. Not medical advice.
