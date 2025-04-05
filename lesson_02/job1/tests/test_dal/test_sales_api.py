"""
Tests sales_api.py module.
# TODO: write tests
"""
from unittest import TestCase, mock

# NB: avoid relative imports when you will write your code:
from lesson_02.ht_template.job1.dal.sales_api import get_sales


class GetSalesTestCase(TestCase):
    
    @mock.patch('requests.get')
    def test_get_sales_http_error(self, mock_get):
        # Simulate a 200 response for the first page and a 404 for the second page
        mock_response_1 = mock.Mock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = [{'client': 'Michael Wilkerson',
                                            'purchase_date': '2022-08-09',
                                            'product': 'Vacuum cleaner',
                                            'price': 346}]
        
        mock_response_2 = mock.Mock()
        mock_response_2.status_code = 404  
        mock_get.side_effect = [mock_response_1, mock_response_2]  
        result = get_sales('2022-08-09')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['client'], 'Michael Wilkerson')
        self.assertEqual(result[0]['purchase_date'], '2022-08-09')
        self.assertEqual(result[0]['product'], 'Vacuum cleaner')
        self.assertEqual(result[0]['price'], 346)