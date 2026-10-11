import argparse
import csv
import html
import json
from pathlib import Path
import random
from src.transits import load_curve,search

ROOT = Path(__file__).resolve().parent


def generate_demo(path):
    rng = random.Random(42)
    with path.open('w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['time_days','flux'])
        for i in range(1000):
            t = i*0.02
            # Inject a 1.5% box dip every 3 days, centered near phase 0.22.
            dip = 0.015 if 0.19 <= (t%3)/3 < 0.25 else 0
            writer.writerow([round(t,4),round(1-dip+rng.gauss(0,0.001),7)])


def main():
    parser = argparse.ArgumentParser(description='Search a light curve for a periodic box-shaped dip.')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--demo',action='store_true')
    mode.add_argument('--input',type=Path)
    parser.add_argument('--source',help='Dataset URL or identifier; required with --input')
    parser.add_argument('--min-period',type=float,default=2)
    parser.add_argument('--max-period',type=float,default=5)
    parser.add_argument('--period-step',type=float,default=0.02)
    args = parser.parse_args()
    if args.input and not args.source:
        parser.error('--input requires --source')
    out = ROOT/'reports'/'generated'
    out.mkdir(parents=True,exist_ok=True)
    path = args.input
    if args.demo:
        path = out/'synthetic_curve.csv'
        generate_demo(path)
    rows = load_curve(path)
    best,grid = search(rows,args.min_period,args.max_period,args.period_step)
    report = {'mode':'synthetic injection demo' if args.demo else 'user-supplied light curve',
              'source':'run.py seed 42' if args.demo else args.source,
              'observations':len(rows),'best_candidate':best,
              'injected_period_days':3 if args.demo else None,
              'injected_depth':0.015 if args.demo else None,
              'period_absolute_error_days':abs(best['period_days']-3) if args.demo and best else None,
              'limitations':'Grid-search score is not statistical significance. Noise can produce a best candidate. No detrending, quality-flag filtering, significance calibration, or planet confirmation is implemented.'}
    (out/'candidate.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    with (out/'period_grid.csv').open('w',newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f,fieldnames=['period_days','sse_improvement'])
        writer.writeheader()
        writer.writerows(grid)
    if best:
        plotted = [(((t-rows[0][0])%best['period_days'])/best['period_days'],f) for t,f in rows]
        xlabel = 'Orbital phase (0 to 1)'
    else:
        span = rows[-1][0]-rows[0][0]
        plotted = [((t-rows[0][0])/span,f) for t,f in rows]
        xlabel = 'Fraction of observed time span'
    low, high = min(f for _,f in rows),max(f for _,f in rows)
    pad = max((high-low)*0.1,0.0001)
    low, high = low-pad, high+pad
    circles = ''.join(f'<circle cx="{60+x*660:.1f}" cy="{270-(f-low)/(high-low)*210:.1f}" r="1.8" fill="#4769a5" opacity="0.6"/>' for x,f in plotted)
    page = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Transit analysis</title>
<style>body{{font:16px system-ui;max-width:1000px;margin:40px auto;padding:0 20px;background:#f4f7fa;color:#183047}}article{{padding:24px;background:white;border-radius:12px;margin:20px 0}}svg{{width:100%;height:auto}}text{{font:12px system-ui}}pre{{white-space:pre-wrap}}</style>
<h1>Exoplanet signal analysis</h1><p><strong>{'SYNTHETIC INJECTION - not telescope data' if args.demo else 'Candidate analysis - not a confirmed planet'}</strong></p>
<article><h2>{'Folded light curve at the best candidate period' if best else 'Light curve: no positive dip candidate'}</h2>
<p>Flux normalized by the median. Plot limits: {low:.5f} to {high:.5f}.</p><svg viewBox="0 0 780 325" role="img" aria-label="Normalized flux plotted against phase or observed time fraction"><line x1="60" y1="270" x2="720" y2="270" stroke="#183047"/>{circles}<text x="60" y="294">0</text><text x="710" y="294">1</text><text x="230" y="316">{xlabel}</text><text x="2" y="60">{high:.4f}</text><text x="2" y="270">{low:.4f}</text></svg></article>
<article><h2>Candidate and limitations</h2><pre>{html.escape(json.dumps(report,indent=2))}</pre></article></html>'''
    (out/'light_curve.html').write_text(page,encoding='utf-8')
    print(json.dumps(report,indent=2))
    print('Open reports/generated/light_curve.html.')


if __name__ == '__main__':
    main()
