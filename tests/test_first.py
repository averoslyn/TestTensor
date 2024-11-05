import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MainPage:
  def __init__(self, driver):
    self.driver = driver
    self.wait = WebDriverWait(self.driver, 10)

  def open_contacts_page(self):
    # Клик по кнопке "Контакты"
    contacts_button = ("xpath", "//div[@class='sbisru-Header-ContactsMenu js-ContactsMenu']")
    self.wait.until(EC.element_to_be_clickable(contacts_button)).click()
    self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".sbisru-Header-ContactsMenu__items.sbisru-Header-ContactsMenu__items-visible")))

  def click_first_link(self):
    # Переход во вкладку "Контакты"
    self.driver.find_elements(By.CLASS_NAME, "sbisru-link")[0].click()

class TensorPage:
  def __init__(self, driver):
    self.driver = driver
    self.wait = WebDriverWait(self.driver, 10)

  def click_tensor_banner(self):
    # Поиск баннера Тензор и клик по нему
    logo_tensor = ("xpath", "//a[@class='sbisru-Contacts__logo-tensor mb-12']")
    self.wait.until(EC.element_to_be_clickable(logo_tensor)).click()

  def check_tensor_url(self):
    # Проверка url сайта
    self.wait.until(EC.number_of_windows_to_be(2))
    self.driver.switch_to.window(self.driver.window_handles[-1])
    assert self.driver.current_url == "https://tensor.ru/", "Ошибка в URL, открыта не та страница"

  def check_sila_v_lyudyah_block(self):
    # Проверка, что есть блок "Сила в людях"
    sila_v_lyudyah_block = (By.XPATH, "//div[@class='tensor_ru-Index__block4-content tensor_ru-Index__card']")
    self.wait.until(EC.visibility_of_element_located(sila_v_lyudyah_block))
    assert sila_v_lyudyah_block, 'Блок "Сила в людях" отсутствует'

  def open_about_page(self):
    # В блоке "Сила в людях" перейти на вкладку "Подробнее"
    more_about = (By.XPATH, "(//a[@class='tensor_ru-link tensor_ru-Index__link'])[2]")
    self.wait.until(EC.element_to_be_clickable(more_about)).click()

  def check_rabotaem_block(self):
    # Находим раздел "Работаем"
    rabotaem_block = (By.XPATH, "//div[@class='tensor_ru-container tensor_ru-section tensor_ru-About__block3']")
    self.wait.until(EC.visibility_of_element_located(rabotaem_block))
    assert rabotaem_block, 'Блок "Работаем" отсутствует'

  def check_photo_sizes(self):
    # Проверяем размер фото в разделе "Работаем"
    photos = self.driver.find_elements(By.XPATH, "//img[@class='tensor_ru-About__block3-image new_lazy loaded']")
    for photo in photos:
      assert photo.size["height"] == 192 and photo.size["width"] == 270, "Фотографии разных размеров"

@pytest.fixture
def driver():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--window-size=1920, 1080")
  service = Service(executable_path=ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service, options=chrome_options)
  driver.implicitly_wait(10)
  yield driver
  driver.quit()

def test_tensor_page(driver):
  main_page = MainPage(driver)
  driver.get("https://sbis.ru/")
  main_page.open_contacts_page()
  main_page.click_first_link()

  tensor_page = TensorPage(driver)
  tensor_page.click_tensor_banner()
  tensor_page.check_tensor_url()
  tensor_page.check_sila_v_lyudyah_block()
  tensor_page.open_about_page()
  tensor_page.check_rabotaem_block()
  tensor_page.check_photo_sizes()