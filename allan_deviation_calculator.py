import pandas as pd
import numpy as np
import allantools
import argparse
import os
import matplotlib.pyplot as plt

def calculate_adev(data, rate, overlapping=True, taus='octave'):
    if overlapping:
        taus, adevs, errs, ns = allantools.oadev(data, rate=rate, data_type='freq', taus=taus)
    else:
        taus, adevs, errs, ns = allantools.adev(data, rate=rate, data_type='freq', taus=taus)
    return taus, adevs, errs, ns

def plot_adev(results, output_plot):
    plt.figure(figsize=(10, 6))
    for col, (taus, adevs, errs, _) in results.items():
        plt.plot(taus, adevs, label=col)
        plt.fill_between(taus, adevs - errs, adevs + errs, alpha=0.2)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Averaging Time (τ) [s]')
    plt.ylabel('Allan Deviation')
    plt.title('Allan Deviation vs Averaging Time')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_plot)
    plt.close()
    print(f"Plot saved to '{output_plot}'")

def process_file(input_path, args, output_dir):
    df = pd.read_csv(input_path, sep=args.delimiter)
    output_dict = {}
    plot_data = {}

    for col in args.columns:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in {input_path}. Skipping.")
            continue

        series = df[col].dropna().values
        if len(series) < 2:
            print(f"Warning: Not enough data in column '{col}' to calculate Allan deviation. Skipping.")
            continue

        taus, adevs, errs, ns = calculate_adev(series, rate=1.0/args.rate, overlapping=(args.type == "overlapping"), taus=args.taus)
        plot_data[col] = (taus, adevs, errs, ns)

        if "tau" not in output_dict:
            output_dict["tau"] = taus
        output_dict[col] = adevs
        output_dict[f"{col}_err"] = errs
        output_dict[f"{col}_n"] = ns

    if not plot_data:
        print(f"No valid data processed in {input_path}. Skipping.")
        return

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_csv = os.path.join(output_dir, f"{base_name}_adev.csv")
    output_plot = os.path.join(output_dir, f"{base_name}_plot.png")

    result_df = pd.DataFrame(output_dict)
    result_df.to_csv(output_csv, index=False)
    print(f"Saved: {output_csv}")
    plot_adev(plot_data, output_plot)

def main():
    parser = argparse.ArgumentParser(description="Calculate Allan deviation for one or many CSV files.")
    parser.add_argument("--input_csv", help="Path to a single CSV file")
    parser.add_argument("--batch_folder", help="Directory containing multiple CSV files")
    parser.add_argument("-r", "--rate", type=float, default=1.0, help="Sampling interval (seconds)")
    parser.add_argument("-t", "--type", choices=["normal", "overlapping"], default="normal", help="Type of Allan deviation to compute")
    parser.add_argument("-c", "--columns", nargs='+', required=True, help="List of column names for which to calculate Allan deviation")
    parser.add_argument("--taus", choices=["all", "octave", "decade"], default="octave", help="Tau values to use for Allan deviation calculation")
    parser.add_argument("--delimiter", default=";", help="CSV delimiter (default: ';')")
    parser.add_argument("--output_dir", default="output", help="Directory to save output CSVs and plots")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    if args.input_csv:
        process_file(args.input_csv, args, args.output_dir)
    elif args.batch_folder:
        for file in os.listdir(args.batch_folder):
            if file.endswith(".csv"):
                process_file(os.path.join(args.batch_folder, file), args, args.output_dir)
    else:
        print("Error: Please provide either --input_csv or --batch_folder")

if __name__ == "__main__":
    main()
