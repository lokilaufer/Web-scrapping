import requests
from bs4 import BeautifulSoup
import json

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
keywords = ['Django', 'Flask']
result = []

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

vacancy_list = soup.find_all('div', class_='vacancy-serp-item')

for vacancy in vacancy_list:
    vacancy_text = vacancy.find('div', class_='g-user-content').get_text()
    if all(keyword.lower() in vacancy_text.lower() for keyword in keywords):
        vacancy_data = {
            'link': vacancy.find('a')['href'],
            'salary': vacancy.find('div', class_='vacancy-serp-item__compensation').get_text(),
            'company': vacancy.find('a', class_='bloko-link_secondary').get_text(),
            'city': vacancy.find('span', class_='vacancy-serp-item__meta-info').get_text()
        }
        result.append(vacancy_data)

with open('vacancies.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
