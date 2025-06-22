import logging
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

class CryptoBacktester:
    def __init__(self, symbol, currency='USD', starting_capital=250.0, limit=2000,
                 cooldown=3, rsi_buy=40, rsi_sell=60, ma_short=10, ma_long=50,
                 sentiment_enabled=False, sentiment_buy_threshold=0.2, sentiment_sell_threshold=-0.2):
        self.symbol = symbol.upper()
        self.currency = currency.upper()
        self.starting_capital = starting_capital
        self.limit = limit

        self.cooldown = cooldown
        self.rsi_buy = rsi_buy
        self.rsi_sell = rsi_sell
        self.ma_short = ma_short
        self.ma_long = ma_long

        self.log_data = []
        self.invested_history = []
        self.capital_history = []

        self.sentiment_enabled = sentiment_enabled
        self.sentiment_buy_threshold = sentiment_buy_threshold
        self.sentiment_sell_threshold = sentiment_sell_threshold

    def get_sentiment(self):
        url = "https://finnhub.io/api/v1/news-sentiment"
        params = {
            "symbol": self.symbol,
            "token": "d16782pr01qvtdbgpbc0d16782pr01qvtdbgpbcg"  # Replace with your real API key
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            score = data.get("sentiment", {}).get("companyNewsScore", 0.5)
            return (score * 2) - 1  # Normalize to [-1, 1]
        except Exception as e:
            print(f"Sentiment API error for {self.symbol}: {e}")
            return 0.0

    def fetch_data(self):
        url = 'https://min-api.cryptocompare.com/data/v2/histoday'
        params = {
            'fsym': self.symbol,
            'tsym': self.currency,
            'limit': self.limit,
            'api_key': '3122b34ac7176b3c5d0018b89ae6bc48a5a9ba33c39ee19907d1928201719cc4'
        }

        response = requests.get(url, params=params)
        json_data = response.json()

        if json_data.get('Response') != 'Success':
            raise RuntimeError(f"Error fetching data: {json_data.get('Message')}")

        df = pd.DataFrame(json_data['Data']['Data'])
        df['date'] = pd.to_datetime(df['time'], unit='s')
        self.data = df[['date', 'close']].rename(columns={'close': 'price'})

        self.raw_start_price = self.data['price'].iloc[0]
        self.raw_end_price = self.data['price'].iloc[-1]

    def compute_indicators(self):
        df = self.data.copy()

        short_col = f'MA{self.ma_short}'
        long_col = f'MA{self.ma_long}'
        df[short_col] = df['price'].rolling(window=self.ma_short).mean()
        df[long_col] = df['price'].rolling(window=self.ma_long).mean()
        df['RSI'] = self.compute_rsi(df['price'])
        df['Upper_Band'], df['Lower_Band'] = self.compute_bollinger_bands(df['price'])
        df['MACD'], df['MACD_Signal'] = self.compute_macd(df['price'])

        self.data = df.dropna().reset_index(drop=True)

    def compute_rsi(self, series, period=14):
        delta = series.diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def compute_bollinger_bands(self, series, window=20):
        mean = series.rolling(window=window).mean()
        std = series.rolling(window=window).std()
        return mean + 2 * std, mean - 2 * std

    def compute_macd(self, series):
        ema12 = series.ewm(span=12, adjust=False).mean()
        ema26 = series.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal

    def analyze_signals(self):
        data = self.data
        signals = []
        cooldown = self.cooldown
        last_action = 'SELL'
        last_trade_index = -cooldown

        ma_short_col = f'MA{self.ma_short}'
        ma_long_col = f'MA{self.ma_long}'

        sentiment_score = self.get_sentiment() if self.sentiment_enabled else 0.0

        for i in range(1, len(data)):
            if i - last_trade_index < cooldown:
                continue

            row = data.iloc[i]
            prev = data.iloc[i - 1]

            price = row['price']
            rsi = row['RSI']
            macd, signal_line = row['MACD'], row['MACD_Signal']
            macd_prev, signal_prev = prev['MACD'], prev['MACD_Signal']

            ma_short = row[ma_short_col]
            ma_long = row[ma_long_col]
            ma_short_prev = prev[ma_short_col]

            upper_band, lower_band = row['Upper_Band'], row['Lower_Band']

            macd_cross_up = macd > signal_line and macd - signal_line < 0.5
            macd_cross_down = macd_prev > signal_prev and macd < signal_line
            price_cross_up = prev['price'] < ma_short_prev and price > ma_short
            price_cross_down = prev['price'] > ma_short_prev and price < ma_short

            uptrend = ma_short > ma_long
            downtrend = ma_short < ma_long
            under_upper_band = price < upper_band * 1.05
            over_lower_band = price > lower_band * 0.95

            buy = macd_cross_up or (price_cross_up and rsi > self.rsi_buy and uptrend and under_upper_band)
            sell = macd_cross_down or (price_cross_down and rsi < self.rsi_sell and downtrend and over_lower_band)

            sentiment_check = (
                (not self.sentiment_enabled) or
                (buy and sentiment_score > self.sentiment_buy_threshold) or
                (sell and sentiment_score < self.sentiment_sell_threshold)
            )

            if buy and last_action == 'SELL' and sentiment_check:
                signals.append({'date': row['date'], 'action': 'BUY', 'price': price})
                last_action = 'BUY'
                last_trade_index = i
            elif sell and last_action == 'BUY' and sentiment_check:
                signals.append({'date': row['date'], 'action': 'SELL', 'price': price})
                last_action = 'SELL'
                last_trade_index = i

        self.signals = signals

    def simulate_trades(self):
        capital = self.starting_capital
        crypto_held = 0.0
        entry_price = 0.0
        holding = False

        signal_map = {s['date']: s for s in self.signals}

        for _, row in self.data.iterrows():
            date = row['date']
            price = row['price']
            action = signal_map.get(date, None)

            if action and action['action'] == 'BUY' and not holding:
                crypto_held = capital / price
                entry_price = price
                capital = 0.0
                self.log_data.append({
                    'timestamp': date, 'action': 'BUY',
                    'crypto_amount': crypto_held, 'price_usd': price,
                    'fiat_spent': crypto_held * price
                })
                holding = True

            elif action and action['action'] == 'SELL' and holding:
                capital = crypto_held * price
                self.log_data.append({
                    'timestamp': date, 'action': 'SELL',
                    'crypto_amount': crypto_held, 'price_usd': price,
                    'fiat_received': capital
                })
                crypto_held = 0.0
                holding = False

            invested = crypto_held * entry_price if holding else 0.0
            total_value = capital + crypto_held * price
            self.invested_history.append(invested)
            self.capital_history.append(total_value)

        log_df = pd.DataFrame(self.log_data)
        log_df.to_csv(f'logs/trading_log_{self.symbol}.csv', index=False)

    def calculate_hodl_profit(self):
        start_price = self.data['price'].iloc[0]
        end_price = self.data['price'].iloc[-1]

        coins_bought = self.starting_capital / start_price
        hodl_final_value = coins_bought * end_price

        hodl_roi = ((hodl_final_value - self.starting_capital) / self.starting_capital) * 100
        return hodl_final_value, hodl_roi

    def run_backtest(self, plot=False):
        os.makedirs('logs', exist_ok=True)
        os.makedirs('plots', exist_ok=True)
        os.makedirs('csv', exist_ok=True)

        self.fetch_data()
        self.compute_indicators()
        self.analyze_signals()
        self.simulate_trades()
        if plot:
            self.plot_results()

        price_df = self.data[['date', 'price']]
        capital_df = pd.DataFrame({'date': self.data['date'], 'capital': self.capital_history})
        invested_df = pd.DataFrame({'date': self.data['date'], 'invested': self.invested_history})

        price_df.to_csv(f'csv/{self.symbol}_price.csv', index=False)
        capital_df.to_csv(f'csv/{self.symbol}_capital.csv', index=False)
        invested_df.to_csv(f'csv/{self.symbol}_invested.csv', index=False)

        final_capital = self.capital_history[-1]
        strategy_roi = ((final_capital - self.starting_capital) / self.starting_capital) * 100
        total_trades = len([log for log in self.log_data if log['action'] == 'SELL'])

        hodl_value, hodl_roi = self.calculate_hodl_profit()
        alpha = strategy_roi - hodl_roi

        buy_sell_pairs = [
            (self.log_data[i], self.log_data[i + 1])
            for i in range(0, len(self.log_data) - 1, 2)
            if self.log_data[i]['action'] == 'BUY' and self.log_data[i + 1]['action'] == 'SELL'
        ]

        profitable_trades = sum(
            1 for buy, sell in buy_sell_pairs
            if float(sell['price_usd']) > float(buy['price_usd'])
        )

        profit_ratio = (profitable_trades / len(buy_sell_pairs)) if buy_sell_pairs else 0.0

        return {
            'symbol': self.symbol,
            'final_capital': final_capital,
            'roi': strategy_roi,
            'hodl_roi': hodl_roi,
            'alpha_vs_hodl': alpha,
            'total_trades': total_trades,
            'profitable_trade_ratio': profit_ratio
        }

    def plot_results(self):
        data = self.data
        fig, ax1 = plt.subplots(figsize=(14, 7), constrained_layout=True)

        # Plot price on left axis
        ax1.plot(data['date'], data['price'], label='Crypto Price', color='blue')
        ax1.set_ylabel(f'Price ({self.symbol})', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Plot capital and HODL value on right axis
        ax2 = ax1.twinx()
        ax2.plot(data['date'], self.capital_history, label='Strategy Capital', color='orange', linestyle='--')

        # Calculate HODL value
        coins_bought = self.starting_capital / data['price'].iloc[0]
        hodl_value = data['price'] * coins_bought
        ax2.plot(data['date'], hodl_value, label='HODL Value', color='purple', linestyle='-.')

        ax2.set_ylabel('Capital / Value (USD)', color='black')
        ax2.tick_params(axis='y', labelcolor='black')

        # Buy/sell signals
        buy_dates = [s['date'] for s in self.signals if s['action'] == 'BUY']
        sell_dates = [s['date'] for s in self.signals if s['action'] == 'SELL']
        buy_prices = data[data['date'].isin(buy_dates)]['price']
        sell_prices = data[data['date'].isin(sell_dates)]['price']

        ax1.scatter(buy_dates, buy_prices, marker='^', color='green', s=100, label='Buy Signal', zorder=5)
        ax1.scatter(sell_dates, sell_prices, marker='v', color='red', s=100, label='Sell Signal', zorder=5)

        # Legend
        legend_elements = [
            Line2D([0], [0], color='blue', label='Price'),
            Line2D([0], [0], color='orange', linestyle='--', label='Strategy Capital'),
            Line2D([0], [0], color='purple', linestyle='-.', label='HODL Value'),
            Line2D([0], [0], marker='^', color='w', label='Buy Signal', markerfacecolor='green', markersize=10),
            Line2D([0], [0], marker='v', color='w', label='Sell Signal', markerfacecolor='red', markersize=10),
        ]
        fig.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5))
        fig.tight_layout(rect=[0, 0, 0.85, 1])
        plt.title(f'{self.symbol} Trading Strategy vs HODL')
        plt.savefig(f'plots/trading_strategy_plot_{self.symbol}.png', bbox_inches='tight')
        plt.close()