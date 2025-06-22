name: Crypto Backtest Optimization Pipeline
script: backtest_pipeline.py
description: >
  Runs a sentiment-aware, multi-symbol trading strategy backtesting pipeline.
  Uses Optuna for hyperparameter optimization and evaluates performance against HODL.

inputs:
  - name: symbols
    type: list[string]
    description: List of cryptocurrency symbols to run backtests on
    default: ["ETH", "BTC", "ADA", "XRP", "LTC"]
  - name: n_trials
    type: int
    description: Number of Optuna trials per symbol
    default: 30
  - name: top_n
    type: int
    description: Number of top-performing strategies to visualize
    default: 3

outputs:
  - description: JSON logs for each symbol under `optuna_results/`
  - description: Optimization summary printed to console
  - description: Matplotlib plots for top symbols' best-performing backtests

dependencies:
  - Python packages: optuna, pandas, matplotlib, textblob, requests
  - Local module: crypto_backtester (must be available in PYTHONPATH)

execution: |
  python3 backtest_pipeline.py
