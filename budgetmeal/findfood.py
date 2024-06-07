import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import xlsxwriter
import time

def scroll(driver):
    # Scroll to bottom
    prev_height = -1
    max_scrolls = 100
    scroll_count = 0

    while scroll_count < max_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # give some time for new results to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height
            scroll_count += 1
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")

def scrape_budgetmeal(postal, start, worksheet, driver):
    ROOT = "https://www.gowhere.gov.sg/budgetmeal/search?result=addr~"
    website = ROOT + str(postal) + '&sort=relevance'
    driver.get(website)
    worksheet.write(0, 0, "Eatery Name")
    worksheet.write(0, 1, "Eatery Address")
    worksheet.write(0, 2, "Item")
    worksheet.write(0, 3, "Price")
    worksheet.write(0, 4, "Halal?")
    count = start
    time.sleep(5)
    section = driver.find_element(By.CSS_SELECTOR, "div[class='w-full max-w-[1020px] m-auto mb-5 p-[16px] rounded-xl']")

    for a in range(2):
        for row in section.find_elements(By.XPATH, ".//div[@role = 'row']"):
            text = row.text.splitlines()
            for i in range(len(text) - 3):
                if text[3].startswith('1.'):
                    j = 1
                else:
                    j = 0
                worksheet.write(count, 0, ' '.join(text[0+j].split(' ')[:-2]))
                edited_postal = text[1+j].split(' ')[-1][1:]
                num_of_words = len(text[1+j].split(' '))
                worksheet.write(count, 1, ' '.join(text[1+j].split(' ')[1:num_of_words - 1]) + " " + edited_postal)
                item = text[2 + j + i].strip()
                if item.endswith("Halal"):
                    worksheet.write(count, 4, "Yes")
                    item = ' '.join(item.split(' ')[:-2])
                worksheet.write(count, 2, item[3:len(item)-8])
                worksheet.write(count, 3, item[len(item)-5:len(item)-1])
                count = count + 1
        print(count)
        driver.execute_script("window.scrollTo(0, 4500);")
    print(f'{count} number of budget foods found')
    return count

def get_all_food_data():
    workbook = xlsxwriter.Workbook('fooddata.xlsx')
    worksheet = workbook.add_worksheet()
    driver = webdriver.Chrome()
    postal_codes = [506931,
    486030,
    519528,
    460021,
    523890,
    540299,
    539517,
    400327,
    449875,
    797563,
    808724,
    550242,
    380016,
    437437,
    229900,
    310075,
    560302,
    768893,
    757443,
    730816,
    729569,
    668387,
    659547,
    128381,
    277855,
    119081,
    109684,
    259772,
    100108,
    619160,
    648195,
    629649,
    638778,
    637566,
    628283,
    627724]
    prev = 1
    for postal in postal_codes:
        prev = scrape_budgetmeal(postal, prev, worksheet, driver)
    workbook.close()

get_all_food_data()