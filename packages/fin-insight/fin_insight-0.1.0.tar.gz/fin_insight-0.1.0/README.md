# Financial Insight Stock Analysis Tool

## Overview
Financial Insight is a Python-based stock analysis tool that provides comprehensive insights into stock performance by combining financial data, news sentiment, and intelligent rating generation.

## Features
- Fetch real-time stock data using Yahoo Finance
- Retrieve latest financial news articles
- Perform sentiment analysis on news articles
- Generate stock ratings (Buy/Sell/Hold)
- Detailed financial highlights
- JSON output for easy integration

## Prerequisites
- Python 3.8+
- NewsAPI API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fin_insight.git
cd fin_insight
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up NewsAPI Key:
```bash
export NEWS_API_KEY='your_newsapi_key_here'  # On Windows use `set NEWS_API_KEY=your_key`
```

## Usage
```bash
python fin_insight.py AAPL  # Replace AAPL with desired stock ticker
```

## Example Output
```json
{
    "ticker": "AAPL",
    "latest_price": 175.23,
    "sentiment_summary": "Positive sentiment in news articles",
    "financialHighlights": {
        "revenueGrowthPercentage": "12.50%",
        "earningsGrowthPercentage": "15.75%",
        "forwardPERatio": "22.30",
        "debtToEquityRatio": "1.10"
    },
    "rating": "Buy"
}
```

## Components
- `get_stock_data()`: Retrieves stock financial data
- `get_financial_news()`: Fetches recent news articles
- `analyze_sentiment()`: Performs sentiment analysis
- `generate_rating()`: Calculates stock recommendation

## Configuration
Adjust rating thresholds and weights in `generate_rating()` function for custom analysis.

## Error Handling
- Validates ticker symbols
- Checks for missing API keys
- Provides detailed error messages

## Dependencies
- yfinance: Stock data retrieval
- requests: News article fetching
- vaderSentiment: Sentiment analysis
- pandas: Data manipulation

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License

## Disclaimer
This tool provides financial insights for informational purposes only. Always conduct your own research and consult financial advisors before making investment decisions.
