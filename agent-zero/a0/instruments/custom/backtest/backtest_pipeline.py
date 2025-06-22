# 🔁 automate_backtest_pipeline.py (consolidated with sentiment-aware trading simulation)
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import optuna
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from crypto_backtester import CryptoBacktester
from textblob import TextBlob
import requests

def optimize_for_symbol(symbol: str, n_trials: int = 30):
    def objective(trial):
        params = {
            'cooldown': trial.suggest_int('cooldown', 1, 5),
            'rsi_buy': trial.suggest_int('rsi_buy', 30, 50),
            'rsi_sell': trial.suggest_int('rsi_sell', 50, 70),
            'ma_short': trial.suggest_int('ma_short', 5, 20),
            'ma_long': trial.suggest_int('ma_long', 30, 100),
        }
        if params['ma_short'] >= params['ma_long']:
            raise optuna.TrialPruned()

        try:
            tester = CryptoBacktester(symbol=symbol, **params)
            result = tester.run_backtest(plot=False)
            result['best_params'] = params

            os.makedirs('optuna_results', exist_ok=True)
            with open(f'optuna_results/{symbol}.json', 'a') as f:
                json.dump(result, f)
                f.write('\n')

            return result['alpha_vs_hodl']
        except Exception as e:
            print(f"[{symbol}] Trial failed: {e}")
            raise optuna.TrialPruned()

    print(f"🚀 Starting optimization for {symbol}")
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    print(f"✅ Done: {symbol} | Best Alpha: {study.best_value:.2f}%")
    return symbol, study.best_value, study.best_params

def run_batch_optimization(symbols, n_trials=30, parallel=True):
    os.makedirs("optuna_results", exist_ok=True)
    if parallel:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(optimize_for_symbol, symbol, n_trials) for symbol in symbols]
            for future in futures:
                try:
                    symbol, best_alpha, best_params = future.result()
                    print(f"\n🏁 {symbol} completed — Alpha: {best_alpha:.2f}% | Params: {best_params}")
                except Exception as e:
                    print(f"\n❌ Error optimizing {symbol}: {e}")
    else:
        for symbol in symbols:
            try:
                symbol, best_alpha, best_params = optimize_for_symbol(symbol, n_trials)
                print(f"\n🏁 {symbol} completed — Alpha: {best_alpha:.2f}% | Params: {best_params}")
            except Exception as e:
                print(f"\n❌ Error optimizing {symbol}: {e}")

def summarize_optuna_results(results_dir='optuna_results'):
    summary = []
    for file in os.listdir(results_dir):
        if not file.endswith('.json'):
            continue
        symbol = file.replace('.json', '')
        file_path = os.path.join(results_dir, file)
        with open(file_path, 'r') as f:
            try:
                results = [json.loads(line.strip()) for line in f if line.strip()]
                if not results:
                    continue
                best = max(results, key=lambda r: r.get('alpha_vs_hodl', -999))
                summary.append({
                    'symbol': symbol,
                    'alpha_vs_hodl': best['alpha_vs_hodl'],
                    'roi': best['roi'],
                    'hodl_roi': best['hodl_roi'],
                    'total_trades': best['total_trades'],
                    'profitable_trade_ratio': best.get('profitable_trade_ratio', 0.0),
                    'best_params': best['best_params'],
                })
            except Exception as e:
                print(f"⚠️ Error processing {file}: {e}")

    summary = sorted(
        summary,
        key=lambda x: (x['alpha_vs_hodl'] * 0.7 + x['profitable_trade_ratio'] * 100 * 0.3),  # example weighting
        reverse=True
    )

    print("\n🏁 Final Optimization Summary:")
    for i, s in enumerate(summary, 1):
        print(
            f"{i}. {s['symbol']} | Alpha: {s['alpha_vs_hodl']:.2f}% | ROI: {s['roi']:.2f}% | HODL: {s['hodl_roi']:.2f}% "
            f"| Trades: {s['total_trades']} | Win Rate: {s['profitable_trade_ratio']:.1%} | Params: {s['best_params']}"
        )
    return summary

def run_backtest_from_best(symbol, result_path='optuna_results'):
    with open(f'{result_path}/{symbol}.json', 'r') as f:
        results = [json.loads(line.strip()) for line in f if line.strip()]
        best = max(results, key=lambda r: r['alpha_vs_hodl'])

    print(f"🏁 Running best backtest for {symbol} | Alpha: {best['alpha_vs_hodl']:.2f}%")
    params = best['best_params']
    tester = CryptoBacktester(symbol=symbol, **params)
    result = tester.run_backtest(plot=True)
    print(f"📊 Win Rate: {result['profitable_trade_ratio']:.1%}")
    tester.plot_results()  # ✅ Only plot here
    return result

def pipeline(symbols, n_trials=30, top_n=3):
    run_batch_optimization(symbols, n_trials=n_trials, parallel=True)
    summary = summarize_optuna_results()
    top_symbols = [entry['symbol'] for entry in summary[:top_n]]
    for symbol in top_symbols:
        run_backtest_from_best(symbol)
    print("\n✅ All steps completed.")

if __name__ == '__main__':
    pipeline(symbols=['ETH', 'BTC', 'ADA', 'XRP', 'LTC'], n_trials=30, top_n=3)
