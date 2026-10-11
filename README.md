# Exoplanet Transit Signal Analysis

**Status: runnable starter. Real-data portfolio results are still to be built.**

Investigate whether a simple periodic-dip search can recover known or injected signals. The first version provides a synthetic light curve, a transparent search, and a folded plot.

## Run it in five minutes

Requires Python 3.11 or newer. This starter uses only Python's standard library: no dependency installation, API key, or paid service is needed.

1. Click **Code > Download ZIP** on GitHub and extract it.
2. Open the extracted folder containing `run.py`.
3. Click the Windows File Explorer address bar, type `powershell`, and press Enter.
4. Check Python: `python --version`. If Windows does not find it, try `py --version` and substitute `py` in the commands below. If neither works, install Python from [python.org](https://www.python.org/downloads/) and enable the installer option to add Python to PATH.
5. Run:

```powershell
python run.py --demo
```

Then open `reports/generated/light_curve.html`. Generated files are local outputs and are ignored by Git. The starter's sample results demonstrate the workflow, not research or business findings.

## What works now

- Generates 1,000 synthetic observations with a 3-day period, 1.5% injected depth, and seeded Gaussian noise.
- Validates finite positive flux and unique times, sorts the curve, and normalizes by median flux.
- Searches periods from 2 to 5 days in 0.02-day steps, using 50 phase bins and a fixed 6% transit duration.
- Ranks positive dip fits by improvement in squared error relative to a constant model.
- Exports the best candidate, period grid, injection error, and a folded HTML plot.

## First task for you

In `run.py`, change the injected dip depth from `0.015` to `0.008` and change the matching injected-depth metadata from `0.015` to `0.008`. Run the demo again. Compare the recovered depth and period. Then restore the values before running the supplied fixture tests, which expect the original injection.

See [START_HERE.md](START_HERE.md) for a guided session and [ROADMAP.md](ROADMAP.md) for the project milestones.

## Validation

```powershell
python -m unittest discover -s tests -v
```

GitHub Actions runs the same tests and demo on Python 3.11. Tests cover selected failure cases and starter behavior; they do not validate scientific conclusions or portfolio readiness.

## Limitations

No telescope observations are included. The model has a fixed fractional duration, assumes a flat baseline, ignores measurement uncertainties, and does not detrend or apply quality flags. Grid scanning can select dips from noise and aliases. The score is not a calibrated significance statistic. A best candidate is not evidence of a confirmed planet. The single injection demo does not estimate recovery rate or false-positive rate.

## Sources and method

See [data sources](docs/DATA_SOURCES.md). Keep a development log of decisions and evidence in [docs/LEARNING_LOG.md](docs/LEARNING_LOG.md). No performance or impact claim should be added to a resume until it is supported by work you can reproduce and explain.
