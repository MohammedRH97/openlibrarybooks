import unittest
import requests

class BookInformationTest(unittest.TestCase):

    def create_response(self):
        """
        Helper method to create API response.
        """
        response = requests.get('https://openlibrary.org/isbn/9780140328721.json')
        return response


    def test_response_status_code(self):
        """
        Response returns 200 status code upon success.
        """
        response = self.create_response()      
        self.assertEqual(response.status_code, 200)


    def test_response_data(self):
        """
        Testing relevant data obtained from response API with the example ISBN13: 9780140328721.
        """
        response = self.create_response()
        data = response.json()
        for items in data:
                isbn13 = data['isbn_13'][0]
                title = data['title']
                publishers = data['publishers'][0]
                publication_date = data['publish_date']
                unique_id = data['key']
        
        self.assertEqual(isbn13, '9780140328721')
        self.assertEqual(title, 'Fantastic Mr. Fox')
        self.assertEqual(publishers, 'Puffin')
        self.assertEqual(publication_date, 'October 1, 1988')
        self.assertEqual(unique_id, '/books/OL7353617M')    



if __name__ == '__main__':
    unittest.main()