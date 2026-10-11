# Data sources and assumptions

## Telescope-data next milestone

NASA's [TESS data product guide](https://heasarc.gsfc.nasa.gov/docs/tess/data_products.html) describes light curves and archive access. Obtain an appropriate light curve from MAST and document the target ID, sector, product/version, retrieval date, quality filtering, time system, and flux units. No downloader or FITS adapter is implemented in this starter.

Input CSV columns: `time_days,flux`. Times must use one consistent time origin and be finite; flux must be positive and finite. The loader normalizes flux by its median. Do not label relative days as UTC calendar timestamps. Measurement errors and quality flags must be handled before export; the current CSV importer has no columns for them.

For your data: `python run.py --input data/raw/light_curve.csv --source "YOUR_DATASET_URL_OR_ID" --min-period 2 --max-period 5`. The maximum searched period must be no more than half the observed time span. This span check does not guarantee adequate phase coverage. Source reference was checked on 2026-10-10. No third-party dataset is bundled.
