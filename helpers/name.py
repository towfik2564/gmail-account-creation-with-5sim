import requests
from bs4 import BeautifulSoup
import random

class ArabicName:
    def __init__(self):
        self.url = 'https://www.almrsal.com/post/1107699'
        print(f'[arabic name] fetching data from: {self.url}')

    def generate_a_name(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        name_tags = soup.select('ul li span:not([class])')
        sentences = [nt.get_text() for nt in name_tags]
        print(f'[arabic name] total {len(sentences)} names found')
        print(f'[arabic name] selecting a random combination')
        names = []
        for sentence in sentences:
            name =  sentence.split(':')[0]
            names.append(name)
        random_numbers = [random.randint(0, len(names)) for _ in range(2)]
        first_name = names[random_numbers[0]]
        last_name = names[random_numbers[1]]
        user = {
            'first_name': first_name,
            'last_name': last_name,
        }
        print(f'[arabic name] selected name: {first_name} {last_name}')
        return user
            
            