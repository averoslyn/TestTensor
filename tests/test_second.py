import pytest
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MainPage:
  def __init__(self, driver):
    self.driver = driver
    self.wait = WebDriverWait(driver, 10)

  def open_contacts_page(self):
    # Клик по кнопке "Контакты"
    contacts_button = ("xpath", "//div[@class='sbisru-Header-ContactsMenu js-ContactsMenu']")
    self.wait.until(EC.element_to_be_clickable(contacts_button)).click()
    self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".sbisru-Header-ContactsMenu__items.sbisru-Header-ContactsMenu__items-visible")))

  def click_first_link(self):
    # Переход во вкладку "Контакты"
    self.driver.find_elements(By.CLASS_NAME, "sbisru-link")[0].click()

  def check_region(self):
    # Проверка, что регион определился
    region = ("xpath", "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    region_element = self.wait.until(EC.visibility_of_element_located(region))
    assert region_element.text, "Регион не определился"

  def check_partners_list(self):
    # Проверка загрузки списка партнеров
    partners_list = self.driver.find_elements("xpath", "//div[@id='contacts_list']")
    assert partners_list, "Список партнеров отсутствует"

  def change_region(self):
    # Изменяем регион на "Камчатский край"
    region = ("xpath", "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    self.wait.until(EC.visibility_of_element_located(region)).click()
    # Ждём видимости панели с выбором региона
    self.wait.until(EC.visibility_of_element_located(("xpath", "//div[@class='sbis_ru-Region-Panel__overlay sbis_ru-Region-Panel--fixed']")))
    # Меняем регион
    time.sleep(2)
    new_region = ("xpath", "//span[@title='Камчатский край']")
    self.wait.until(EC.element_to_be_clickable(new_region)).click()
    # Ждём, пока панель с выбором региона закроется
    self.wait.until(EC.invisibility_of_element_located(("xpath", "//div[@class='sbis_ru-Region-Panel__overlay sbis_ru-Region-Panel--fixed']")))

  def check_region_changed(self):
    # Проверяем, что регион задан верно
    region = ("xpath", "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    region_element = self.wait.until(EC.element_to_be_clickable(region))
    assert "Камчатский край" in region_element.text, "Регион не изменился"

  def check_partners_list_changed(self):
    # Проверяем, что список партнеров изменился
    new_partners = ("xpath", "//div[@title='СБИС - Камчатка']")
    self.wait.until(EC.visibility_of_element_located(new_partners))
    assert new_partners, 'Список партнеров не загрузился'

  def check_url_and_title(self):
    # Проверяем, что URL и заголовок страницы изменились
    assert "kamchatskij-kraj" in self.driver.current_url, "URL не содержит информации о регионе"
    assert "Камчатский край" in self.driver.title, "Заголовок страницы не содержит информации о регионе"

@pytest.fixture
def driver():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--window-size=1920, 1080")
  service = Service(executable_path=ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service, options=chrome_options)
  driver.implicitly_wait(10)
  yield driver
  driver.quit()

def test_sbis_main_page(driver):
  main_page = MainPage(driver)
  driver.get("https://sbis.ru/")
  main_page.open_contacts_page()
  main_page.click_first_link()
  main_page.check_region()
  main_page.check_partners_list()
  main_page.change_region()
  time.sleep(2)
  main_page.check_region_changed()
  main_page.check_partners_list_changed()
  main_page.check_url_and_title()