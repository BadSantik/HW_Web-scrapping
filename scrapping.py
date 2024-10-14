import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
print(f"Нужно найти слова {KEYWORDS} на портале ХАБРА:")
print()

BASE_URL = 'https://habr.com/ru/articles/page'

total_articles = 0
total_keyword_counts = defaultdict(int)


def process_page(page_number):
    global total_articles

    url = f'{BASE_URL}{page_number}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article')
    total_articles += len(articles)

    keyword_counts = defaultdict(int)

    for article in articles:
        preview_element = article.find('div', class_='article-formatted-body')
        preview = preview_element.text.lower() if preview_element else ''

        for keyword in KEYWORDS:
            count = preview.count(keyword)
            keyword_counts[keyword] += count
            total_keyword_counts[keyword] += count

    date_element = soup.find('time')
    date = date_element['datetime'] if date_element else 'Дата не найдена'
    formatted_date = datetime.fromisoformat(date).strftime(
        '%d.%m.%Y (время: %H:%M:%S)') if date != 'Дата не найдена' else date

    print(f"Страница №{page_number}")
    print(f"Адрес страницы: {url}")
    print(f"Дата создания: {formatted_date}")
    print("Слова (константы):")
    for keyword in KEYWORDS:
        print(f"'{keyword}' – {keyword_counts[keyword]} раз")
    print("======================\n")


for page in range(1, 51):
    process_page(page)

print("Итого:")
print(f"Всего статей: {total_articles} шт.")
print("Обнаружено слов (констант):")
for keyword in KEYWORDS:
    print(f"'{keyword}' – {total_keyword_counts[keyword]} раз")
