import pytest
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class MainPage:
  def __init__(self, driver: webdriver.Chrome):
    self.driver = driver
    # Определяем директорию загрузки файла
    self.current_directory = Path(__file__).parent.absolute()

  def go_to_download_page(self):
    # Находим "Скачать локальные версии" в подвале сайта
    wait = WebDriverWait(self.driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='sbisru-Footer__link'])[36]"))).click()

  def click_plugin_download_button(self):
    # Нажимаем "Скачать"
    wait = WebDriverWait(self.driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='sbis_ru-DownloadNew-loadLink__link js-link']"))).click()


@pytest.fixture
def driver():
  chrome_options = webdriver.ChromeOptions()
  prefs = {
    "download.default_directory": str(Path(__file__).parent.absolute()),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "safebrowsing.disable_download_protection": True,
  }
  chrome_options.add_experimental_option("prefs", prefs)

  service = Service(executable_path=ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service, options=chrome_options)
  yield driver
  driver.quit()


def test_download_plugin(driver):
  main_page = MainPage(driver)
  driver.get("https://sbis.ru/")
  main_page.go_to_download_page()
  main_page.click_plugin_download_button()
  time.sleep(20)

  # Определяем, что файл был загружен
  downloaded_file = Path(main_page.current_directory, "sbisplugin-setup-web.exe")
  assert downloaded_file.is_file(), "Файл не был загружен"

  # Определяем, что размер файла соответствует указанному
  downloaded_file_size_mb = downloaded_file.stat().st_size / (1024 * 1024)
  expected_file_size_mb = 11.48
  assert round(downloaded_file_size_mb, 2) == expected_file_size_mb, f"Размер файла {downloaded_file_size_mb} МБ не совпадает с ожидаемым размером {expected_file_size_mb} МБ."
