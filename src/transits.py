"""Educational box-shaped periodic-dip search, not a discovery pipeline."""
import csv
import math
from pathlib import Path
import statistics


def load_curve(path):
    rows, seen = [], set()
    with Path(path).open(newline='',encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not {'time_days','flux'}.issubset(reader.fieldnames or []):
            raise ValueError('CSV requires time_days and flux columns.')
        for line,row in enumerate(reader,2):
            try:
                time, flux = float(row['time_days']),float(row['flux'])
                if not math.isfinite(time) or not math.isfinite(flux) or flux <= 0:
                    raise ValueError('time must be finite and flux positive and finite')
                if time in seen:
                    raise ValueError('duplicate time')
                seen.add(time)
                rows.append((time,flux))
            except (ValueError,TypeError) as e:
                raise ValueError(f'Line {line}: {e}') from e
    if len(rows) < 30:
        raise ValueError('Need at least 30 observations.')
    rows.sort()
    med = statistics.median(f for _,f in rows)
    return [(t,f/med) for t,f in rows]


def search(rows, minimum=2, maximum=5, step=0.02, bins=50, width=3):
    """Compare two-level dip fits to a constant mean using SSE improvement.

    Fixed fractional duration = width/bins. Score is not a significance level.
    Phase bins speed up the grid search, at the cost of boundary precision.
    """
    if not rows or minimum <= 0 or maximum < minimum or step <= 0:
        raise ValueError('Require positive periods/step and max >= min.')
    if bins < 4 or not 1 <= width < bins//2:
        raise ValueError('Invalid phase bin or duration settings.')
    if maximum > (rows[-1][0]-rows[0][0])/2:
        raise ValueError('Maximum period must allow at least two cycles in the observed time span.')
    count = int((maximum-minimum)/step + 1e-9)+1
    if count > 5000:
        raise ValueError('Grid too large; increase period step.')
    total = sum(f for _,f in rows)
    n = len(rows)
    best, grid = None, []
    for index in range(count):
        period = minimum + index*step
        sums, counts = [0.0]*bins,[0]*bins
        for t,f in rows:
            b = int(((t-rows[0][0])%period)/period*bins)%bins
            sums[b] += f
            counts[b] += 1
        period_best = None
        for start in range(bins):
            indices = [(start+j)%bins for j in range(width)]
            nin = sum(counts[b] for b in indices)
            nout = n-nin
            if nin < 5 or nout < 5:
                continue
            inside = sum(sums[b] for b in indices)
            in_mean, out_mean = inside/nin, (total-inside)/nout
            depth = out_mean-in_mean
            if depth <= 1e-10:
                continue
            improvement = depth*depth*nin*nout/n
            candidate = {'period_days':round(period,6), 'phase_start':start/bins,
                         'duration_fraction':width/bins, 'relative_depth':depth/out_mean,
                         'in_transit_points':nin,'out_of_transit_points':nout,
                         'sse_improvement':improvement, 'reference_time_days':rows[0][0]}
            if period_best is None or improvement > period_best['sse_improvement']:
                period_best = candidate
        grid.append({'period_days':round(period,6),'sse_improvement':period_best['sse_improvement'] if period_best else 0})
        if period_best and (best is None or period_best['sse_improvement'] > best['sse_improvement']):
            best = period_best
    return best,grid
