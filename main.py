import os, gc, time
import pandas as pd
import gspread
from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials

fields = ['No', 'Name', 'Address', 'Releasable', 'Released', 'DOP ballance']
data = []

def scraping(no, name, address) :
    service = webdriver.chrome.service.Service(os.path.abspath('chromedriver'))
    service.start()
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome('chromedriver', options = option)
    url = 'https://etherscan.io/address/0x5b13929da9fae9929aba25fc14014305f6e5da89#readContract'
    driver.get(url)
    time.sleep(3)

    try :
        cookieBtn = driver.find_element_by_id("btnCookie")
        cookieBtn.click()
        time.sleep(1)
    except :
        pass

    iframe = driver.find_element_by_id("readcontractiframe")
    driver.switch_to.frame(iframe)

    releasableDiv = driver.find_element_by_css_selector('a[aria-controls="readCollapse7"]')
    releasableDiv.click()
    time.sleep(0.5)

    investorIn = driver.find_element_by_id("input_7_1")
    investorIn.send_keys(address)
    queryBtn = driver.find_element_by_id("btn_7")
    queryBtn.click()
    time.sleep(4)
    try :
        releasableVal = round(int(driver.find_element_by_css_selector("span[id='myanswer_7'] > a").text)/10**18, 4)
    except :
        releasableVal = "0"

    try :
        cookieBtn = driver.find_element_by_id("btnCookie")
        cookieBtn.click()
        time.sleep(1)
    except :
        pass


    releasedDiv = driver.find_element_by_css_selector('a[aria-controls="readCollapse8"]')
    releasedDiv.click()
    time.sleep(0.5)

    investorIn = driver.find_element_by_id("input_8_1")
    investorIn.send_keys(address)
    queryBtn = driver.find_element_by_id("btn_8")
    queryBtn.click()
    time.sleep(3)

    try :
        releasedVal = round(int(driver.find_element_by_css_selector("span[id='myanswer_8'] > a").text)/10**18, 4)
    except :
        releasedVal = "0"
    
    # second part
    url = "https://etherscan.io/address/0x6bb61215298f296c55b19ad842d3df69021da2ef#readContract"
    driver.get(url)
    time.sleep(3)

    try :
        cookieBtn = driver.find_element_by_id("btnCookie")
        cookieBtn.click()
        time.sleep(1)
    except :
        pass

    iframe = driver.find_element_by_id("readcontractiframe")
    driver.switch_to.frame(iframe)

    releasedDiv = driver.find_element_by_css_selector('a[aria-controls="readCollapse4"]')
    releasedDiv.click()
    time.sleep(0.5)

    investorIn = driver.find_element_by_id("input_4_1")
    investorIn.send_keys(address)
    queryBtn = driver.find_element_by_id("btn_4")
    queryBtn.click()
    time.sleep(4)

    try :
        balanceOfVal = round(int(driver.find_element_by_css_selector("span[id='myanswer_4'] > a").text)/10**18, 4)
    except :
        balanceOfVal = "0"
    
    driver.close()

    data.append([no, name, address, releasableVal, releasedVal, balanceOfVal])


def getGSData() :
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    
    # Below google sheet url is test url. So, you have to replace it into your google sheet url
    spreadsheets = client.open_by_url("https://docs.google.com/spreadsheets/d/1Vtj6ErL033b3FqMw9RnF2HAcI8Xyh9SlJRUZYZ9Hz-A/edit#gid=0")
    
    sheet1 = spreadsheets.sheet1

    data = sheet1.get("A1:E339")
    for i in range(1, 339) :
        print(data[i][0] + "   " + data[i][4])
        scraping(i, data[i][0], data[i][4])


def saveDataToCSV() :
    dataTable = pd.DataFrame(data, columns=fields)
    dataTable.to_csv("result.csv", index = False, header=True)

def main() :
    getGSData()
    saveDataToCSV()

if __name__ == '__main__':
    try:
        main()
        gc.collect()

    except Exception as why:
        print(why)
