import requests
import json
import csv
import os.path

# Main API url
base_url = 'https://openlibrary.org'

# Dictionary in which response data will be added and then used to generate a CSV file.
data_dict = {}

class bookInformation:
    """
    Taking user input for a valid ISBN13 identifier and then calling the public API
    to get relevant book data (ISBN13, Title, Publisher, Publication Date, Author and a unique identifier).
    """
    def get_identifier(self):
        """
        Check whether the user input is a digit.
        """
        while True:
            self.identifier = input('Enter the ISBN13 identifier: ')
            if self.identifier.isdigit():
                return self.identifier
            else:
                print('Input is not numeric... Try Again!')
                continue


    def get_book(self):
        """
        First, calls main API response using identifier provided by user.
        If identifier is not valid, repeat.
        If identifier is valid, get relevant book data as well as an author_key
        which will allow me to call another API to get author's 'name'.
        Once successful, data is added to data_dict and used to generate book_data.csv file.
        """
        response = requests.get(base_url + '/isbn/' + str(self.identifier) + '.json')

        # Upon successful API request.
        if response.status_code == 200:
            data = response.json() # JSON formatted data.
            for items in data:
                isbn13 = data['isbn_13'][0] # '0' to get the first element instead of a list.
                title = data['title']
                publishers = data['publishers'][0] # '0' to get the first element instead of a list.
                publication_date = data['publish_date']
                unique_id = data['key']
                
                for a in data['authors']:
                    author_key = a['key']

            # Call another API using author_key to get author's name.
            author_response = requests.get(base_url + str(unique_id) + str(author_key) + '.json')

            if author_response.status_code == 200:
                author_data = author_response.json()
                for items in author_data:
                    author = author_data['name']

                # Adding all data to data_dict.
                data_dict['ISBN13'] = isbn13
                data_dict['Title'] = title
                data_dict['Publishers'] = publishers
                data_dict['Publication Date'] = publication_date
                data_dict['Author'] = author
                data_dict['Unique ID'] = unique_id

                # if book_data.csv exists, then data from data_dict will just be appended to file,
                # otherwise new file with headers will be created.
                if os.path.exists('book_data.csv'):
                    with open('book_data.csv', 'a', newline='') as f:
                        w = csv.DictWriter(f, data_dict.keys())
                        w.writerow(data_dict)
                        print('Data has been added to existing book_data.csv file.')
                else:
                    with open('book_data.csv', 'w', newline='') as f:
                        w = csv.DictWriter(f, data_dict.keys())
                        w.writeheader()
                        w.writerow(data_dict)
                        print('Data has been added to a new book_data.csv file.')
            
            else:
                print('Could not connect to author_response API, please ensure you have entered a valid ISBN13 identifier')
                self.get_identifier()
                self.get_book()

        else:
            print('Could not connect to response API, please ensure you have entered a valid ISBN13 identifier.')
            self.get_identifier()
            self.get_book()

b = bookInformation()
b.get_identifier()
b.get_book()