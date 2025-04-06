FRED_SERIES_DETAILS = {
    # GDP Data (Generally Quarterly)
    'GDPC1': {
        'frequency_code': 'q',
        'description': 'Real Gross Domestic Product',
        'url': 'https://fred.stlouisfed.org/series/GDPC1'
    },
    'A191RP1Q027SBEA': {
        'frequency_code': 'q',
        'description': 'Real Gross Domestic Product (Percent Change from Preceding Period, QoQ)',
        'url': 'https://fred.stlouisfed.org/series/A191RP1Q027SBEA'
    },
    'A191RL1Q225SBEA': {
        'frequency_code': 'q',
        'description': 'Real Gross Domestic Product (Percent Change from Year Ago, YoY)',
        'url': 'https://fred.stlouisfed.org/series/A191RL1Q225SBEA'
    },
    'PCECC96': {
        'frequency_code': 'q',
        'description': 'Real Personal Consumption Expenditures',
        'url': 'https://fred.stlouisfed.org/series/PCECC96'
    },
    'GPDIC1': {
        'frequency_code': 'q',
        'description': 'Real Gross Private Domestic Investment',
        'url': 'https://fred.stlouisfed.org/series/GPDIC1'
    },
    'NETEXC': {
        'frequency_code': 'q',
        'description': 'Real Net Exports of Goods and Services',
        'url': 'https://fred.stlouisfed.org/series/NETEXC'
    },
    'GCEC1': {
        'frequency_code': 'q',
        'description': 'Real Government Consumption Expenditures & Gross Investment',
        'url': 'https://fred.stlouisfed.org/series/GCEC1'
    },

    # Employment Index (Monthly)
    'PAYEMS': {
        'frequency_code': 'm',
        'description': 'All Employees, Total Nonfarm (Thousands of Persons)',
        'url': 'https://fred.stlouisfed.org/series/PAYEMS'
    },
    'UNRATE': {
        'frequency_code': 'm',
        'description': 'Unemployment Rate (Percent)',
        'url': 'https://fred.stlouisfed.org/series/UNRATE'
    },

    # Purchasing Power (Monthly)
    'RSAFS': {
        'frequency_code': 'm',
        'description': 'Advance Retail Sales: Retail and Food Services (Millions of Dollars)',
        'url': 'https://fred.stlouisfed.org/series/RSAFS'
    },
    'UMCSENT': {
        'frequency_code': 'm',
        'description': 'University of Michigan: Consumer Sentiment Index',
        'url': 'https://fred.stlouisfed.org/series/UMCSENT'
    },

    # Monetary Policy
    'FEDFUNDS': {
        'frequency_code': 'm',
        'description': 'Effective Federal Funds Rate (Monthly Average, Percent)',
        'url': 'https://fred.stlouisfed.org/series/FEDFUNDS'
    },
    'DFF': {
        'frequency_code': 'd',
        'description': 'Effective Federal Funds Rate (Daily, Percent)',
        'url': 'https://fred.stlouisfed.org/series/DFF'
    },
    'M2SL': {
        'frequency_code': 'm',
        'description': 'M2 Money Stock (Billions of Dollars, Monthly)',
        'url': 'https://fred.stlouisfed.org/series/M2SL'
    },
    'WM2NS': {
        'frequency_code': 'w',
        'description': 'M2 Money Stock (Billions of Dollars, Weekly)',
        'url': 'https://fred.stlouisfed.org/series/WM2NS'
    },

    # Inflation (Monthly)
    'CPIAUCSL': {
        'frequency_code': 'm',
        'description': 'Consumer Price Index for All Urban Consumers: All Items (Index)',
        'url': 'https://fred.stlouisfed.org/series/CPIAUCSL'
    },
    'PCEPI': {
        'frequency_code': 'm',
        'description': 'Personal Consumption Expenditures Price Index (Index)',
        'url': 'https://fred.stlouisfed.org/series/PCEPI'
    },

    # US Bonds (Examples)
    'DGS10': {
        'frequency_code': 'd',
        'description': 'Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity (Percent)',
        'url': 'https://fred.stlouisfed.org/series/DGS10'
    },
    'GS10': {
        'frequency_code': 'm',
        'description': 'Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity (Monthly Average, Percent)',
        'url': 'https://fred.stlouisfed.org/series/GS10'
    }
}

# Example usage:
# print(fred_series_details['PAYEMS']['frequency_code']) # Output: m
# print(fred_series_details['PAYEMS']['url'])          # Output: https://fred.stlouisfed.org/series/PAYEMS
# print(fred_series_details['GDPC1']['frequency_code']) # Output: q
# print(fred_series_details['GDPC1']['url'])          # Output: https://fred.stlouisfed.org/series/GDPC1