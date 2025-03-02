import unittest
import json
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fin_insight

class TestFinInsight(unittest.TestCase):
    def test_get_stock_data(self):
        """Test stock data retrieval for a valid ticker"""
        stock_data = fin_insight.get_stock_data('AAPL')
        self.assertIsNotNone(stock_data)
        self.assertIn('latest_price', stock_data)
        self.assertIn('financial_highlights', stock_data)

    def test_get_stock_data_invalid_ticker(self):
        """Test stock data retrieval for an invalid ticker"""
        stock_data = fin_insight.get_stock_data('INVALID')
        self.assertIsNone(stock_data)

    def test_main_function(self):
        """Test the main function with a valid ticker"""
        result = fin_insight.main('MSFT')
        result_json = json.loads(result)
        
        self.assertIn('ticker', result_json)
        self.assertIn('latest_price', result_json)
        self.assertIn('sentiment_summary', result_json)
        self.assertIn('financialHighlights', result_json)
        self.assertIn('rating', result_json)

    def test_create_json_response(self):
        """Test JSON response creation"""
        financial_highlights = {
            'revenue_growth': 0.1,
            'earnings_growth': 0.15,
            'forward_pe': 22.5,
            'debt_to_equity': 1.2
        }
        response = fin_insight.create_json_response(
            'GOOGL', 
            1500.50, 
            'Positive sentiment', 
            financial_highlights, 
            'Buy'
        )
        
        response_json = json.loads(response)
        self.assertEqual(response_json['ticker'], 'GOOGL')
        self.assertEqual(response_json['rating'], 'Buy')

if __name__ == '__main__':
    unittest.main()
