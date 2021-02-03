import sqlite3
import selenium
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from security import Security

conn = sqlite3.connect("assets.db")
conn.row_factory = sqlite3.Row

c = conn.cursor()

driver = webdriver.Chrome('C:/Users/maxim/Sync/Projects/asset_manager/chromedriver')


def insert_asset(asset):
    with conn:
        c.execute("INSERT INTO assets VALUES (:asset_ID, :bdate, :num)",
                {'asset_ID': asset.ISIN, 'bdate': asset.bdate, 'num': asset.num,})

def delete_asset(asset):
    with conn:
        c.execute("DELETE from assets WHERE asset_ID = :asset_ID",
        {'asset_ID': asset.ISIN})

def update_asset(asset):
    with conn:
        c.execute("""UPDATE assets SET bdate = :bdate, num = :num
                    WHERE asset_ID = :asset_ID""",
                  {'asset_ID': asset.ISIN, 'bdate': asset.bdate, 'num': asset.num})

def update_DB(tempAssetList):                #update DB
    for asset in tempAssetList:
        with conn:
            c.execute("""UPDATE assets SET curPrice = :curPrice, name = :name
                        WHERE asset_ID = :asset_ID""",
                    {'asset_ID': asset.ISIN, 'curPrice': asset.curPrice, 'name': asset.name})



driver.get("https://www.justetf.com/de/")
try:
    closeButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
    )
    closeButton.click()
except:
    print("Kein cookiepopup gefunden")
    driver.quit()


tempAssetList = []                          #temporary list of all assets in DB
c.execute('SELECT * FROM assets') 
for asset in c:
    tempAsset = Security(asset[0], asset[1], asset[2], asset[3], asset[4])
    
    isin = asset[0]
        
    if asset[3] == 1:
        driver.get("https://www.justetf.com/de/etf-profile.html?groupField=index&from=search&isin="+ isin)

        e_head = driver.find_element_by_class_name("e_head")
        assetName = e_head.find_element_by_class_name("h1").text
        infobox = driver.find_element_by_class_name("infobox")
        price = infobox.find_element_by_class_name("val").text[4:]
        price = price.replace(",", ".")
        
        print(assetName + "    " + price + " EUR")
   
    elif asset[3] == 2:

        driver.get("https://www.boersennews.de/markt/aktien/detail/"+ isin)

        exKurs = driver.find_element_by_id("exKurs")
        price = exKurs.text[:-4]
        price = price.replace(",", ".")
        assetName = driver.find_element_by_xpath("/html/body/div[3]/div[5]/div[5]/div[1]/div/h1/span[1]").text
                             
        print(assetName + "     " + price + " EUR")

    tempAsset.curPrice = price
    tempAsset.name  = assetName
    tempAssetList.append(tempAsset)             #append asset to list





driver.quit()                           #close browser window
conn.close()                            #close connection to DB

#security1 = Security('US1912161007', '17.04.2020', 5)

#insert_asset(security1)
#delete_asset(security1)
#update_asset(security1)

#ISIN muss in Datenbank einzigartig sein!!!