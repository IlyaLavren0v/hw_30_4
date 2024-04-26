import pytest
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Установка неявных ожиданий
    driver.implicitly_wait(5)
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


# Проверка наличия всех питомцев
def test_presence_of_all_pets(driver):
    driver.find_element(By.ID, 'email').send_keys('mi@mi.ru')
    driver.find_element(By.ID, 'pass').send_keys('mi@mi.ru')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    driver.get('http://petfriends.skillfactory.ru/my_pets')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.left')))

    # Ожидание появления информации о количестве питомцев
    pets_count_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.left'))).text
    expected_pets_count = int(re.search(r'Питомцев: (\d+)', pets_count_text).group(1))

    pet_cards = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]//tbody//tr')
    assert len(pet_cards) == expected_pets_count


# Проверка наличия фото у половины питомцев
def test_half_pets_with_photos(driver):
    # Авторизация
    driver.find_element(By.ID, 'email').send_keys('mi@mi.ru')
    driver.find_element(By.ID, 'pass').send_keys('mi@mi.ru')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Переход на страницу с питомцами
    driver.get('http://petfriends.skillfactory.ru/my_pets')

    # Ожидание появления карточек питомцев
    pet_cards = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//table[@class="table table-hover"]//tbody//tr')))

    # Подсчет питомцев с фото
    photos_count = sum(1 for card in pet_cards if card.find_element(By.TAG_NAME, 'img').get_attribute('src'))

    # Проверка, что количество питомцев с фото больше половины общего количества питомцев
    assert photos_count >= len(
        pet_cards) / 2, f"{photos_count} pets have photos, which is less than half of the total {len(pet_cards)} pets"

# Проверка наличия имени, возраста и породы у всех питомцев
def test_info_for_all_pets(driver):
    driver.find_element(By.ID, 'email').send_keys('mi@mi.ru')
    driver.find_element(By.ID, 'pass').send_keys('mi@mi.ru')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    driver.get('http://petfriends.skillfactory.ru/my_pets')

    # Ожидание появления карточек питомцев
    pet_cards = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//table[@class="table table-hover"]//tbody//tr')))

    for card in pet_cards:
        # Ожидание появления имени, возраста и породы у каждого питомца
        name = WebDriverWait(card, 10).until(EC.visibility_of_element_located((By.XPATH, './/td[2]'))).text
        animal_type = WebDriverWait(card, 10).until(EC.visibility_of_element_located((By.XPATH, './/td[3]'))).text
        age = WebDriverWait(card, 10).until(EC.visibility_of_element_located((By.XPATH, './/td[4]'))).text
        assert name and animal_type and age

# Проверка уникальности имен питомцев
def test_unique_names(driver):
    driver.find_element(By.ID, 'email').send_keys('mi@mi.ru')
    driver.find_element(By.ID, 'pass').send_keys('mi@mi.ru')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    driver.get('http://petfriends.skillfactory.ru/my_pets')

    # Ожидание появления карточек питомцев
    pet_cards = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//table[@class="table table-hover"]//tbody//tr')))

    names = []
    for card in pet_cards:
        # Ожидание появления имени каждого питомца
        name = WebDriverWait(card, 10).until(EC.visibility_of_element_located((By.XPATH, './/td[2]'))).text
        names.append(name)

    assert len(names) == len(set(names))
