import time

import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def find_price(city_name, _start_date, _finish_date):
    driver.delete_all_cookies()
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
    submit = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[4]/div[2]/button')
    button_w = driver.find_element_by_xpath('//*[@id="cookie_warning"]/div[2]/a')
    if button_w is not None:
        button_w.click()
    time.sleep(1)
    search_input.send_keys(city_name)
    calendar.click()
    time.sleep(1)

    ActionChains(driver).click(start_date_element).click(finish_date_element).perform()
    time.sleep(1)
    submit.click()
    summat_list = 0
    list_price = []
    new_list = []
    summat = 0
    for n in range(1):
        time.sleep(5)
        prices = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'availprice')))  # ждем загрузки соед. страницы
        for name in prices:
            list_price.append(name.find_element_by_tag_name('b').text)
        button_cash = driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/div[1]/ul/li[3]')
        button_cash.click()
        time.sleep(5)
    for prices in list_price:
        prices = prices.replace(" ", "")
        new_list.append(int(prices.replace("руб.", "")))
    for average in new_list:
        summat_list += average
        summat += 1
    return int(summat_list / summat)


def flights(city_name):
    driver.delete_all_cookies()
    driver.get("https://www.google.com/flights")
    button_search = driver.find_element_by_xpath('//*[@id="flt-app"]/div[2]/main[1]/div[4]/div[1]/div[2]/div[2]/div[3]/div[3]')
    button_search.click()
    time.sleep(2)
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="sb_ifc50"]/input')))
    search_input.send_keys(city_name)
    time.sleep(2)
    search_input.send_keys(u'\ue007')
    time.sleep(2)
    but_search = driver.find_element_by_xpath('//*[@id="flt-app"]/div[2]/main[1]/div[4]/div[1]/div[2]/div[4]/floating-action-button')
    but_search.click()

    time.sleep(2)
    price_all = driver.find_element_by_xpath('//*[@id="flt-app"]/div[2]/main[2]/div[9]/div[1]/div[3]/div[5]/div[3]/ol/li[1]/div/div[1]/div[2]/div[1]/div[1]/div[6]/div[1]/jsl[1]/jsl')
    price = price_all.text
    price = price.replace("₽", "")
    price = price.replace(" ", "")
    return(int(price))


if __name__ == "__main__":
    # input("введите дату заселения, например(2018-12-31): ")
    S = "2018-12-20"
    # input("введите дату выселения, например(2018-12-31): ")
    F = "2018-12-25"
    driver = webdriver.Chrome("C:/Users/yalog/PycharmProjects/selenium/chromedriver.exe")
    time.sleep(2)
    List_city_price = []
    price = []
    List_city = ['Heidelberg', 'Paris']
    for C in List_city:
        price1 = find_price(C, S, F)
        price2 = flights(C)
        all_price = price1 + (price2 * 2)
        price.append(all_price)
    plt.bar(List_city, price)
    plt.show()
