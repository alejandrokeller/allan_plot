# Allan Deviation Calculator

This Python script calculates the Allan deviation for one or more time series stored in CSV files. It supports both normal and overlapping Allan deviation, generates plots, and optionally includes uncertainty estimates and sample counts in the output.

## Features

- Calculates **normal** or **overlapping** Allan deviation
- Accepts **single** CSV input or **batch processing** of a folder
- Supports custom CSV **delimiter**
- Outputs CSV file with:
  - Allan deviation (`col`)
  - Error (`col_err`)
  - Sample count (`col_n`)
- Produces a log-log **plot** with shaded error bands
- Customizable averaging time mode: `all`, `octave`, or `decade`

## Requirements

- Python 3.x
- `pandas`
- `numpy`
- `matplotlib`
- `allantools`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Single file

```bash
python allan_deviation_calculator.py \
    --input_csv data.csv \
    -r 1 \
    -t overlapping \
    -c freq1 freq2 \
    --taus octave \
    --delimiter ";" \
    --output_dir results
```

### Batch mode

```bash
python allan_deviation_calculator.py \
    --batch_folder ./data \
    -r 1 \
    -t normal \
    -c signal1 signal2 \
    --taus decade \
    --delimiter ";" \
    --output_dir output
```

## Output

For each input CSV:
- `*_adev.csv`: CSV file with tau, Allan deviation, error, and sample count
- `*_plot.png`: Log-log plot with error bands

## Author

alejandro.keller@fhnw.ch
