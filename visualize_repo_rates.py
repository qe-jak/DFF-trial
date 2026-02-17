"""
Repo Market Rates Visualization in Fee Space (Spread over DFF)

Reads Cantor_BNP_Repo_Market_Data_with_DFF.csv and plots time series of
each rate minus the Daily Fed Funds (DFF) rate.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), "Cantor_BNP_Repo_Market_Data_with_DFF.csv")

# ── Column groupings ────────────────────────────────────────────────
BASE_COLS = ["GC", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
O_COLS    = ["O2Y", "O3Y", "O5Y", "O7Y", "O10Y", "O20Y", "O30Y"]
OO_COLS   = ["OO2Y", "OO3Y", "OO5Y", "OO7Y", "OO10Y", "OO20Y", "OO30Y"]
OOO_COLS  = ["OOO2Y", "OOO3Y", "OOO5Y", "OOO7Y", "OOO10Y", "OOO20Y", "OOO30Y"]

SERIES_GROUPS = {
    "Base Repo Rates": BASE_COLS,
    "O‑Series Repo Rates": O_COLS,
    "OO‑Series Repo Rates": OO_COLS,
    "OOO‑Series Repo Rates": OOO_COLS,
}


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["time"])
    df = df.set_index("time").sort_index()

    # Coerce everything to numeric; '#DIV/0!' and blanks become NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def compute_spreads(df: pd.DataFrame) -> pd.DataFrame:
    """Subtract DFF from every other column to get fee-space spreads."""
    spread = df.drop(columns=["DFF"]).subtract(df["DFF"], axis=0)
    # Convert from percentage points to basis points
    spread = spread * 100
    return spread


def plot_group(ax, spread: pd.DataFrame, cols: list[str], title: str):
    for col in cols:
        if col in spread.columns:
            ax.plot(spread.index, spread[col], label=col, linewidth=1.2)

    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_ylabel("Spread over DFF (bps)")
    ax.set_xlabel("Date")
    ax.axhline(0, color="black", linewidth=0.6, linestyle="--", alpha=0.5)
    ax.legend(loc="best", fontsize=8, ncol=2)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)


def main():
    df = load_data(CSV_FILE)
    spread = compute_spreads(df)

    fig, axes = plt.subplots(2, 2, figsize=(18, 12), constrained_layout=True)
    fig.suptitle(
        "Repo Market Rates – Fee Space (Spread over Daily Fed Funds Rate)",
        fontsize=16,
        fontweight="bold",
    )

    for ax, (title, cols) in zip(axes.flat, SERIES_GROUPS.items()):
        plot_group(ax, spread, cols, title)

    output_path = os.path.join(os.path.dirname(__file__), "repo_rates_fee_space.png")
    fig.savefig(output_path, dpi=150)
    print(f"Saved figure to {output_path}")
    plt.show()


if __name__ == "__main__":
    main()
