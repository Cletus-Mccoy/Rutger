# Problem
 Download S&P500 data without using an API key and create a graphical presentation in multiple formats.
# Solution
 1. Install yfinance library using 'pip install yfinance'.
2. Download S&P500 data from 2024 using yf.download('^GSPC', start='2024-01-01', end='2024-11-23').
3. Create a graphical presentation in multiple formats using matplotlib.pyplot and save the plots to files.