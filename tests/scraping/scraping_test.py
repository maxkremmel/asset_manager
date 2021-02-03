import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome('C:/Users/maxim/Sync/Projects/asset_manager/chromedriver')

isin = "IE00BJ0KDQ92"

driver.get("https://www.justetf.com/de/etf-profile.html?groupField=index&from=search&isin="+ isin)

try:
    closeButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
    )
except:
    driver.quit()

closeButton.click()


e_head = driver.find_element_by_class_name("e_head")
assetName = e_head.find_element_by_class_name("h1")

infobox = driver.find_element_by_class_name("infobox")
val = infobox.find_element_by_class_name("val")
price = val.text[4:]

print(assetName.text)
print(price)

driver.quit()


