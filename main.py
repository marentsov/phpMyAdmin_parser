import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USERNAME = "test"
PASSWORD = "JHFBdsyf2eg8*"
BASE_URL = "http://185.244.219.162/phpmyadmin"
LOGIN_URL = f"{BASE_URL}/index.php"
TABLE_URL = f"{BASE_URL}/index.php?route=/sql&db=testDB&table=users&pos=0"


def extract_token(html):
    """Извлечение CSRF-токена из HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    token_input = soup.find('input', {'name': 'token'})
    if token_input:
        return token_input['value']
    raise ValueError("Токен не найден")


def login(session, token):
    """Вход в phpMyAdmin."""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "pma_username": USERNAME,
        "pma_password": PASSWORD,
        "server": 1,
        "target": "index.php",
        "lang": "ru",
        "token": token
    }
    response = session.post(LOGIN_URL, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception("Вход не удался")


def get_table_data(session, token):
    """Получение данных таблицы users."""
    url = f"{TABLE_URL}&token={token}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": LOGIN_URL
    }
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Не удалось загрузить страницу с таблицей")
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'table_results'})
    if not table:
        raise Exception("Таблица не найдена")

    rows = table.find_all("tr")[1:]
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            id_value = cols[-2].get_text(strip=True)
            name_value = cols[-1].get_text(strip=True)
            data.append([id_value, name_value])

    return data


def main():
    session = requests.Session()
    response = session.get(LOGIN_URL)
    if response.status_code != 200:
        logger.error("Страница входа недоступна")
        return
    token = extract_token(response.text)

    try:
        login(session, token)
    except Exception as e:
        logger.error(f"Ошибка входа: {e}")
        return

    try:
        data = get_table_data(session, token)
        if data:
            print("\nДанные таблицы users:")
            print("--------------------------------")
            print(f"{'ID':<10} {'Имя':<20}")
            print("--------------------------------")
            for row in data:
                print(f"{row[0]:<10} {row[1]:<20}")
    except Exception as e:
        logger.error(f"Ошибка получения данных: {e}")


if __name__ == "__main__":
    main()


