#!/bin/bash

# ==================================================
# Script: run_backtest_pipeline.sh
# Purpose: Guide and run the crypto backtest pipeline
# ==================================================

# Optional: Create a virtual environment (recommended)
# python3 -m venv venv
# source venv/bin/activate

# Install required Python packages
pip install optuna pandas matplotlib textblob requests

# Ensure local modules (like crypto_backtester) are accessible
# Example: export PYTHONPATH="$PYTHONPATH:/path/to/your/modules"

# --------------------------------------------------
# Run the pipeline
# --------------------------------------------------

# Define symbols and parameters
SYMBOLS=("ETH" "BTC" "ADA" "XRP" "LTC")
N_TRIALS=30
TOP_N=3

# Construct comma-separated symbol list for script input
SYMBOL_LIST=$(IFS=, ; echo "${SYMBOLS[*]}")

echo "🚀 Starting backtest pipeline for: $SYMBOL_LIST"
python3 /a0/instruments/custom/backtest/backtest_pipeline.py

# If you want to customize symbols or trials:
# python3 /a0/instruments/custom/backtest/backtest_pipeline.py --symbols "DOGE,SOL,AVAX" --n_trials 50 --top_n 2

echo "✅ Backtest pipeline completed."
