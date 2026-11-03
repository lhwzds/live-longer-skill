---
name: live-longer
description: Estimate how many years of life a habit change may add (steps, fitness, sleep, fruit and vegetables, nuts, BMI), using all-cause mortality hazard ratios from large meta-analyses and the Gompertz rule years ≈ 11.5 × ln(1/HR). Use when someone asks how to live longer, which habit matters most for lifespan, or how much a change would extend life.
---

# Live longer

Only factors with a large evidence base and a clear dose-response formula are included. Every hazard ratio below was checked against the paper; do not add factors or numbers from memory.

## Steps

1. Ask only what is missing: smoking (yes/no), steps per day, sleep hours, fruit + vegetables g/day, nuts g/day, BMI (or height and weight), and fitness if known (VO₂max from a watch, or the change in METs; 1 MET = 3.5 ml/kg/min).
   If they smoke, stopping comes first: smoking costs about 10 years (Jha et al., NEJM 2013) and outweighs everything here.
2. Pick realistic targets (e.g. steps toward 8000, nuts 28 g, fruit and vegetables toward 600–800 g, BMI under 25, sleep 7–8 h).
3. Run `python3 scripts/live_longer.py --steps 4000:7000 --nuts 0:28 --fruitveg 200:400 --bmi 28:25 --sleep 6:7` (each flag is `NOW:TARGET`; `--fitness 0:1` means +1 MET). Values outside a factor's modelled range (e.g. BMI under 22.5) are rejected: say that factor cannot be estimated.
4. Answer: a table of factor, now → target, HR, years; the top 3 changes ranked by years with one concrete way to do each; then the caveats below in one or two lines.

## Formula

`years gained ≈ (8 / ln 2) × ln(HR_now / HR_target) ≈ 11.5 × ln(1/HR)`

Adult all-cause mortality roughly doubles every 8 years (Gompertz law), so multiplying the death rate by HR at every age shifts the survival curve by about `−ln(HR) / (ln 2 / 8)` years. This is a rough life-expectancy difference that assumes the association is causal and holds at every age. Quick table: HR 0.95 → 0.6 y, 0.90 → 1.2 y, 0.80 → 2.6 y, 0.70 → 4.1 y, 0.50 → 8 y. Most accurate from about age 30.

## Factors

The data store is `references/evidence.json`: per factor the model, hazard ratios with 95% CIs, the citation, DOI, study design and the verification date. The script reads only that file. To add or update a factor, check the number in the paper itself, add the entry with its CI and DOI, and update this summary table.

| Factor | Hazard ratio model (all-cause mortality) | Source |
| --- | --- | --- |
| Steps | Quartile medians 3553 / 5801 / 7842 / 10901 steps/day → HR 1 / 0.60 / 0.55 / 0.47; log-interpolated, flat outside | Paluch et al., Lancet Public Health 2022, 15 cohorts ([10.1016/S2468-2667(21)00302-9](https://doi.org/10.1016/S2468-2667(21)00302-9)) |
| Fitness | HR 0.87 per +1 MET of maximal aerobic capacity | Kodama et al., JAMA 2009, 33 studies ([10.1001/jama.2009.681](https://doi.org/10.1001/jama.2009.681)) |
| Fruit + vegetables | HR 0.90 per 200 g/day, up to 800 g/day (most of the benefit by ~400 g) | Aune et al., Int J Epidemiol 2017, 95 studies ([10.1093/ije/dyw319](https://doi.org/10.1093/ije/dyw319)) |
| Nuts | HR 0.78 per 28 g/day, not extrapolated beyond 28 g | Aune et al., BMC Medicine 2016 ([10.1186/s12916-016-0730-3](https://doi.org/10.1186/s12916-016-0730-3)) |
| BMI | HR 1.31 per 5 kg/m² above 25 (reference 22.5–25; below 22.5 not modelled) | Global BMI Mortality Collaboration, Lancet 2016, 239 cohorts, 10.6M people ([10.1016/S0140-6736(16)30175-1](https://doi.org/10.1016/S0140-6736(16)30175-1)) |
| Sleep | ≤ 6 h: HR 1.12 (approximate cut-off), otherwise 1; long sleep (≥ 9 h, HR 1.30) is recorded but not scored, inputs above 8.5 h are rejected | Cappuccio et al., Sleep 2010, 1.38M people ([10.1093/sleep/33.5.585](https://doi.org/10.1093/sleep/33.5.585)) |

## Caveats to state

- These are observational associations; people who move little include some who are already ill, which inflates the step effect. Treat years as rough estimates of direction and size.
- Do not add up factors: the habits overlap, so the script gives no combined figure. For scale, all five low-risk habits together (including not smoking) were associated with about 12–14 more years at age 50 (Li et al., Circulation 2018).
- Long sleep is mostly a marker of ill health, so sleeping less is never scored as a gain; do not advise it.
- Not medical advice; for disease, pregnancy or medication questions refer to a clinician.
