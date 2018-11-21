from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
driver = webdriver.Chrome("C:/Users/yalog/PycharmProjects/selenium/chromedriver.exe")
time.sleep(2)

_start_date = "2018-12-10"
_finish_date = "2018-12-15"
start_date_element = None
finish_date_element = None
driver.get("https://www.booking.com")
search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "ss")))
search_input.clear()

calendar = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[1]/div[2]/div/div/div/div/button')
calendar.click()
time.sleep(2)
all_dates = driver.find_elements_by_class_name("bui-calendar__date")
for date in all_dates:
    attr = date.get_attribute("data-date")
    if attr == _start_date:
        start_date_element = date
        continue
    if attr == _finish_date:
        finish_date_element = date
time.sleep(1)
#submit = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[4]/div[2]/button')
submit = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[4]/div[2]/button')
button_w = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div[2]/a')
button_w.click()
time.sleep(1)
search_input.send_keys("Милан")
calendar.click()
time.sleep(1)
ActionChains(driver).click(start_date_element).click(finish_date_element).perform()
time.sleep(1)
submit.click()

summa_list = 0
list_price = []
new_list = []
average = 0
summa = 0
n = 0
for n in range(20):
    time.sleep(5)
    price = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'availprice'))) # ждем загрузки соед. страницы
    for name in price:
        list_price.append(name.find_element_by_tag_name('b').text)
    button45 = driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/div[1]/ul/li[3]')
    button45.click()
    time.sleep(5)
for price in list_price:
    price = price.replace(" ", "")
    new_list.append(int(price.replace("руб.", "")))
for average in new_list:
    summa_list += average
    summa += 1
print(round((summa_list/summa), 2))