from datetime import datetime
import requests
from bs4 import BeautifulSoup

from parser_app.models import Houses


def get_html(URL): # делать запрос по ссылке и возвращать html код этой страницы
    response = requests.get(URL)
    return response.text


def get_posts_links(html):
    links = []
    soup = BeautifulSoup(html, "html.parser")
    table_data = soup.find("div", {"class":"listings-wrapper"})
    data = table_data.find_all("div", {"class":"main-wrapper"})
    for p in data:
        href = p.find('a').get('href')
        full_url = 'https://www.house.kg' + href
        links.append(full_url)
    return links # возвращает ссылки на детальную страницу постов


def get_detail_post(html, post_url):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', {'class':'content-wrapper'})
    detail = content.find('div', {'class':'main-content'})
    title = detail.find('div', {'details-header'}).find('h1').text.strip()
    price_som = detail.find('div', {'prices-block'}).find('div', {'price-som'}).text.strip()
    price_dollar = detail.find('div', {'prices-block'}).find('div', {'price-dollar'}).text.strip()
    phone = detail.find('div', {'phone-fixable-block'}).find('div', {'number'}).text.strip()
    try:
        description = detail.find('div', {'description'}).find('p').text.strip()
    except AttributeError:
        description = 'ОПИСАНИЕ ОТСУТСТВУЕТ'
    price_som = int(price_som.replace("сом", "").strip().replace(" ", ""))
    price_dollar = int(price_dollar.replace("$", "").strip().replace(" ", ""))

    data = {
        'title': title,
        'som':  price_som,
        'dollar': price_dollar,
        'mobile': phone,
        'description': description,
        'link': post_url
    }
    return data


def get_lp_number(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('nav')
    ul = content.find('ul', {'class':'pagination'})
    lp = ul.find_all('a', {'class':'page-link'})[-1]
    n = lp.get('data-page')
    return int(n)


# def write_data(data): # Запись в базу
#     result = manager.insert_house(data)
#     return result


def main():
    start = datetime.now()
    passed_posts = 0
    URL_MAIN = 'https://www.house.kg/'
    filter = 'kupit-kvartiru?region=1&town=2&price_to=1900000&currency=1&sort_by=upped_at+desc'
    # ФИЛЬТР: КУПИТЬ КВАРТИРУ СТОИМОСТЬЮ ДО 1 500 000 СОМОВ
    FULL_URL = URL_MAIN + filter
    last_page = get_lp_number(get_html(FULL_URL))
    for page in range(1, last_page+1):
        print(f'Парсинг страницы: {page}')
        FULL_URL += f'&page={page}'
        html = get_html(FULL_URL)
        post_links = get_posts_links(html)
        for link in post_links:
            post_html = get_html(link)
            post_data = get_detail_post(post_html, post_url=link)

            # Проверяем существование записи с таким link
            if not Houses.objects.filter(link=post_data['link']).exists():
                # Создаем объект Houses и сохраняем его в базе данных
                house = Houses(
                    title=post_data['title'],
                    som=post_data['som'],
                    dollar=post_data['dollar'],
                    mobile=post_data['mobile'],
                    description=post_data['description'],
                    link=post_data['link']
                )
                house.save()  # Сохраняем объект в базе данных

            print(post_data)
            print('сохранено в БД')

    end = datetime.now()
    print('Время выполнения: ', end-start)
    print(f'Количество пропущенных постов: {passed_posts}')


if __name__ == '__main__':
    main()