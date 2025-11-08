# classification_stats.py
# Utilities to summarize classification labels from your classified Excel.

import os
import pandas as pd
from typing import Tuple

def _ensure_cols(df: pd.DataFrame) -> pd.DataFrame:
    if "Classification" not in df.columns:
        raise ValueError("Input file must contain a 'Classification' column.")
    # Optional columns in many of your files:
    for c in ("Year", "Title", "Abstract", "Related"):
        if c not in df.columns:
            df[c] = None
    return df

def _normalize_label(x) -> str:
    if pd.isna(x):
        return "Unclassified"
    # single-label pipeline should give one label, but be defensive:
    first = str(x).split(",")[0].strip()
    return first if first else "Unclassified"

def summarize_overall(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a dataframe: Label | Count | Percent
    """
    df = _ensure_cols(df.copy())
    df["Label"] = df["Classification"].apply(_normalize_label)
    counts = df["Label"].value_counts(dropna=False).rename_axis("Label").reset_index(name="Count")
    total = counts["Count"].sum()
    counts["Percent"] = (counts["Count"] / total * 100).round(2)
    return counts.sort_values(["Count", "Label"], ascending=[False, True]).reset_index(drop=True)

def summarize_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a long table: Year | Label | Count
    If Year missing, adds Year=None and still returns counts.
    """
    df = _ensure_cols(df.copy())
    df["Label"] = df["Classification"].apply(_normalize_label)
    # Coerce Year to numeric where possible
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    by_year = (
        df.groupby(["Year", "Label"], dropna=False)
          .size()
          .reset_index(name="Count")
          .sort_values(["Year", "Count"], ascending=[True, False])
    )
    return by_year

def write_classification_summaries(input_xlsx: str, output_dir: str) -> Tuple[str, str]:
    """
    Reads `input_xlsx`, writes two summary files into `output_dir`:
      - classification_summary_overall.xlsx
      - classification_summary_by_year.xlsx
    Returns (overall_path, by_year_path)
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_excel(input_xlsx)

    overall = summarize_overall(df)
    by_year = summarize_by_year(df)

    overall_path = os.path.join(output_dir, "classification_summary_overall.xlsx")
    by_year_path = os.path.join(output_dir, "classification_summary_by_year.xlsx")

    overall.to_excel(overall_path, index=False)
    by_year.to_excel(by_year_path, index=False)

    return overall_path, by_year_path


# Optional CLI for ad-hoc runs:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Summarize classification labels.")
    parser.add_argument("--input", required=True, help="Path to the classified Excel file.")
    parser.add_argument("--outdir", required=False, default="results", help="Output directory.")
    args = parser.parse_args()

    overall_path, by_year_path = write_classification_summaries(args.input, args.outdir)
    print("Wrote:\n ", overall_path, "\n ", by_year_path)
