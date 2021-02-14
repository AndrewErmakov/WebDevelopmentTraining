import requests
from bs4 import BeautifulSoup

ITEMS = 100

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                  'Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


def extract_max_page(url):
    hh_request = requests.get(url, headers=headers)
    pages = []

    hh_soup = BeautifulSoup(hh_request.text, 'html.parser')
    paginator = hh_soup.find_all("span", {'class': 'pager-item-not-in-short-range'})

    for page in paginator:
        pages.append(int(page.find('a').text))

    return pages[-1]


def extract_job(our_vacancy):
    title = our_vacancy.find('a').text
    company = our_vacancy.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text.strip()
    location = our_vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]
    link = our_vacancy.find('a')['href']
    return {'title': title, 'company': company, 'location': location, 'link': link}


def extract_hh_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f'hh: парсинг страницы: {page}')
        html_page_vacancies = requests.get(f'{url}&page={page}', headers=headers)
        soup = BeautifulSoup(html_page_vacancies.text, 'html.parser')
        vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
        for vacancy in vacancies:
            job = extract_job(vacancy)
            jobs.append(job)

    return jobs


def get_jobs(vacancy_title):
    url = f'https://hh.ru/search/vacancy?st=searchVacancy&items_on_page={ITEMS}&text={vacancy_title}'
    max_page = extract_max_page(url)
    return extract_hh_jobs(max_page, url)
