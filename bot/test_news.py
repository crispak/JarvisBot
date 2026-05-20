import unittest
import os
from unittest.mock import patch, MagicMock
from news import get_news_response

class TestNews(unittest.TestCase):
    @patch('news.requests.get')
    def test_get_news_success(self, mock_get):
        # Mocking the environment variable
        os.environ['NEWS_API_KEY'] = 'fake_api_key'

        # Mocking the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {'title': 'Article 1', 'url': 'http://url1.com'},
                {'title': 'Article 2', 'url': 'http://url2.com'}
            ]
        }
        mock_get.return_value = mock_response

        message = {'content': '@Jarvis news technology'}
        result = get_news_response(message, None)

        expected_result = "Article 1\nhttp://url1.com\n\nArticle 2\nhttp://url2.com\n\n"
        self.assertEqual(result, expected_result)
        mock_get.assert_called_once_with('https://newsapi.org/v2/everything?q=technology&apiKey=fake_api_key')

    def test_get_news_no_api_key(self):
        # Ensure environment variable is not set
        if 'NEWS_API_KEY' in os.environ:
            del os.environ['NEWS_API_KEY']

        message = {'content': '@Jarvis news technology'}
        result = get_news_response(message, None)

        self.assertEqual(result, "Error: NEWS_API_KEY environment variable is not set.")

    @patch('news.requests.get')
    def test_get_news_api_error(self, mock_get):
        os.environ['NEWS_API_KEY'] = 'fake_api_key'

        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'error', 'message': 'Invalid API key'}
        mock_get.return_value = mock_response

        message = {'content': '@Jarvis news technology'}
        result = get_news_response(message, None)

        self.assertEqual(result, "Error: Could not retrieve articles.")

if __name__ == '__main__':
    unittest.main()
