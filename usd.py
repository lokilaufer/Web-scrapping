import requests
from bs4 import BeautifulSoup
import json

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

jobs = []

for vacancy in soup.find_all('div', class_='vacancy-serp-item'):
    title = vacancy.find('a', class_='bloko-link').text.strip()
    link = vacancy.find('a', class_='bloko-link')['href']
    salary = vacancy.find('span', class_='bloko-header-section').text.strip()

    if 'USD' not in salary:
        continue

    company = vacancy.find('a', class_='bloko-link bloko-link_secondary').text.strip()
    city = vacancy.find('span', class_='vacancy-serp-item__meta-info').text.strip()

    if 'Django' in title or 'Flask' in title:
        job = {
            'title': title,
            'link': link,
            'salary': salary,
            'company': company,
            'city': city
        }
        jobs.append(job)

with open('jobs.json', 'w') as f:
    json.dump(jobs, f, ensure_ascii=False, indent=4)
