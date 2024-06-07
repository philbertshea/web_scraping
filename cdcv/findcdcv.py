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


def scrape_cdcvouchers(postal, geolocator, start, worksheet, driver):
    website = f"https://www.gowhere.gov.sg/cdcvouchers/?result=addr~{str(postal)}&sort=relevance&status=success"
    driver.get(website)
    worksheet.write(0, 0, "Merchant Address")
    worksheet.write(0, 1, "Merchant Address")
    worksheet.write(0, 2, "Merchant Address")
    worksheet.write(0, 3, "Merchant Name")
    worksheet.write(0, 4, "Merchant Type")
    count = start
    time.sleep(2)
    section = driver.find_element(By.XPATH, "//div[@id='search-results']/div[3]")
    
    driver.execute_script("window.scrollTo(0, 1000000);")
    for row in section.find_elements(By.CSS_SELECTOR, "div[class='sc-dJiZtA gWPuNB']"):
        text = row.text.splitlines()
        if text[1].endswith('away)'):
            address_words = text[1].split(' ')
            last_word = address_words[-2][:address_words[-2].find('(')]
            worksheet.write(count, 3, ' '.join(address_words[:-2]).replace(',', '') + ' ' + last_word)
        else:
            worksheet.write(count, 3, text[1])
        edited_postal = text[2].split(' ')[-1][1:7]
        address = ' '.join(text[2].split(' ')[:-1]).replace(',', '') + ' ' + edited_postal
        print(address)
        worksheet.write(count, 0, address)

        if text[0].startswith("HAWKERS"):
            worksheet.write(count, 4, "CDC Merchant")
        else:
            worksheet.write(count, 4, "Supermarket")
        count = count + 1
    print(f'{count} items found')
    return count

def get_all_cdcv_data():
    workbook = xlsxwriter.Workbook('cdcvdata.xlsx')
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
    scrape_cdcvouchers(506931, prev, worksheet, driver)
    #for postal in postal_codes:
        #prev = scrape_cdcvouchers(postal, prev, worksheet, driver)
    workbook.close()

get_all_cdcv_data()