import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def initialize_browser():
    """Инициализирует браузер с драйвером Chrome."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Уберите комментарий для отладки
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    return browser

def fetch_html_via_browser(url):
    """Загружает HTML с помощью браузера."""
    browser = initialize_browser()
    try:
        logging.info(f"Открываем URL: {url}")
        browser.get(url)

        # Ждём появления <body> в течение 20 секунд
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logging.info("Страница успешно загружена.")
        return browser.page_source  # Получаем HTML-код страницы
    except Exception as e:
        logging.error(f"Ошибка при загрузке страницы: {e}")
        return None
    finally:
        browser.quit()
        logging.info("Браузер закрыт.")

def extract_and_save_text(html):
    """Извлекает текст из <p data-testid='drop-cap-letter'> и сохраняет в файл."""
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем все теги <p> с атрибутом data-testid="drop-cap-letter"
    elements = soup.find_all('p', {'data-testid': 'drop-cap-letter'})

    if elements:
        # Собираем все тексты в одну строку
        full_text = "\n".join([element.get_text(strip=True) for element in elements])

        # Сохраняем текст в файл article.txt
        with open("article.txt", "w", encoding="utf-8") as f:
            f.write(full_text)

        logging.info("Текст успешно сохранён в файл article.txt.")
    else:
        logging.warning("Не удалось найти элементы <p data-testid='drop-cap-letter'>.")

def main():
    url = input("Введите URL для анализа: ").strip()
    logging.info(f"Получен URL от пользователя: {url}")

    html = fetch_html_via_browser(url)
    if html:
        logging.info("HTML успешно загружен.")
        extract_and_save_text(html)
    else:
        logging.warning("Не удалось загрузить HTML.")

if __name__ == "__main__":
    logging.info("Запуск программы.")
    main()
    logging.info("Программа завершена.")
