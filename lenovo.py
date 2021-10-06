from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


print("sample test case started")
driver = webdriver.Chrome(r"C:\Users\hites\PycharmProjects\pythonProject\selenium_test\browsers\chromedriver.exe")

#maximize the window size
driver.maximize_window()
#navigate to the url
driver.get("https://www.lenovo.com/us/en/pc/")

# waiting for the pop-up to come so that we can remove it
WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#bx-form-1379920-step-1")))
# closing pop-up
if driver.find_element_by_id("bx-form-1379920-step-1").is_displayed():
    driver.find_element_by_id("bx-close-inside-1379920").click()
# accepting bottom cookies option
if driver.find_element_by_id("evidon_banner_wrap"):
    driver.find_element_by_id("_evidon-accept-button").click()
# closing reward pop up
if driver.find_element_by_class_name("rewards-callout").is_displayed():
    driver.find_element_by_class_name("closebtn").click()

# scroll down
driver.execute_script("window.scrollBy(0,600)", "")

nav_bar = driver.find_element_by_css_selector(".homePage_pc.container .tabs")
nav_bar_list = nav_bar.find_elements_by_tag_name("li")

# Xpath for the tag-button under which the products are located
xpath = ['//*[@id="4dadfb71-db66-4a08-b8e8-86547e3056fe"]/div[2]/ul/li[1]/span', '//*[@id="4dadfb71-db66-4a08-b8e8-86547e3056fe"]/div[2]/ul/li[2]/span', '//*[@id="4dadfb71-db66-4a08-b8e8-86547e3056fe"]/div[2]/ul/li[3]/span', '//*[@id="4dadfb71-db66-4a08-b8e8-86547e3056fe"]/div[2]/ul/li[4]/span', '//*[@id="4dadfb71-db66-4a08-b8e8-86547e3056fe"]/div[2]/ul/li[5]/span']

all_data = {
    'product_link': ['product_link'],
    'product_ID': ['product_ID'],
    'name': ["name"],
    'rating': ["rating"],
    'web_price': ["web_price"],
    'price': ["price"],
    'finance_option': ["finance_option"],
}

for pos, val in enumerate(nav_bar_list):
    nav_bar.find_element_by_xpath(xpath[pos]).click()
    # print(pos, val.text)
    time.sleep(5)
    all_products = driver.find_elements_by_css_selector(".Products > ul > li")
    for inner_pos, inner_val in enumerate(all_products):
        if inner_pos == 4:
            continue
        else:
            try:
                main_element = inner_val.find_element_by_tag_name("a")
                name = main_element.find_element_by_css_selector(".name").text
                product_link = main_element.get_attribute('href')
                product_ID = main_element.get_attribute('productid')
                rating = main_element.find_element_by_css_selector(".rating_list .rating-container")
                rating = rating.get_attribute('data-rating-star')
                web_price = main_element.find_element_by_class_name("webPrice").text
                price = main_element.find_element_by_class_name("price").text
                finance_option = main_element.find_element_by_class_name("finance-option").text
            except NoSuchElementException:
                pass
                # print("not a product in this field")
            all_data['product_link'].append(product_link)
            all_data['product_ID'].append(product_ID)
            all_data['name'].append(name)
            all_data['rating'].append(rating)
            all_data['web_price'].append(web_price)
            all_data['price'].append(price)
            all_data['finance_option'].append(finance_option)
            print(product_link)

# dataframe created
df = pd.DataFrame(all_data)

# printing dataframe into CSV
df.to_csv("PC.csv")

#close the browser
driver.close()
print("lenovo test case successfully completed")