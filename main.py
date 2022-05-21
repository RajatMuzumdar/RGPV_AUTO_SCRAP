#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from datetime import datetime
# from xlwt import Workbook
import os, glob
import openpyxl
import csv 
from openpyxl import load_workbook
import time
from bs4 import BeautifulSoup
import pytesseract
# import xlsxwriter
import requests
from lxml import etree
import pandas as pd
from PIL import Image
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert

from selenium.webdriver.chrome.service import Service
from captcha_utils import captcha_decode
import config

# In[ ]:
from win32com.client import Dispatch

def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version

paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
curVersion = list(filter(
    None, [get_version_via_com(p) for p in paths])
    )[0]
versionToFetch = int(curVersion[0:curVersion.find('.')]) - 1
versionToFetch = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'\
    + str(versionToFetch)
response = requests.get(versionToFetch)
versionNumber = response.text


# In[ ]:

# driver = webdriver.Chrome(config.BROW_DRIVER)

from selenium.webdriver import Chrome, ChromeOptions
opts = ChromeOptions()
opts.add_argument("--window-size=800,600")
# service = Service(executable_path=config.BROW_DRIVER)
# driver = webdriver.Chrome(service=service, options=opts)
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="100.0.4896.20").install()), options=opts)
svc = Service(ChromeDriverManager(version=versionNumber).install())

# In[ ]:
import input
inputReceived = False
while(not inputReceived):
    userInput = input.get_input()
    if(not input.validate(userInput)):
        continue
    if(input.confirm(userInput)): 
        inputReceived = True


branchResult = {
    'D': 'http://result.rgpv.ac.in/Result/McaDDrslt.aspx',
    'M': 'http://result.rgpv.ac.in/Result/MCArslt.aspx'
}

RESULT_URL  = branchResult[ userInput['class'].upper()[0] ]
PREFIX      = userInput['prefix']
SEM         = int(float(userInput['semester']))
FROM        = int(float(userInput['from']))
TO          = int(float(userInput['to']))

from captcha_utils import create_dir
DPATH = create_dir('temp')
SHEETNAME = f"{PREFIX}XX"

driver = webdriver.Chrome(service=svc, options=opts)

# RESULT_URL = "http://result.rgpv.ac.in/Result/McaDDrslt.aspx"
# prefix='0827ca21dd'
# SEM = '01'

enrList = input.enrgenerator(PREFIX, FROM, TO)

grade = student = []
i = records = caperror = 0

driver.get('%s' % RESULT_URL)

print(os.getcwd())

while True and i<len(enrList):
    enr = enrList[i]

    #driver.maximize_window()
    enrollment = WebDriverWait(driver, 0) \
                .until(EC.element_to_be_clickable(
                        (By.NAME, 'ctl00$ContentPlaceHolder1$txtrollno')))
    year    =   WebDriverWait(driver, 0) \
                .until(EC.element_to_be_clickable(
                        (By.NAME, 'ctl00$ContentPlaceHolder1$drpSemester')))
    capinp  =   WebDriverWait(driver, 0) \
                .until(EC.element_to_be_clickable(
                        (By.NAME, 'ctl00$ContentPlaceHolder1$TextBox1')))

    
    enrollment.clear()
    capinp.clear()
    enrollment.send_keys(enr)
    print()
    print(enr)
    year.send_keys(SEM)

    # img = driver.find_element(by=By.XPATH, 
    #   value='//div[@id="ctl00_ContentPlaceHolder1_pnlCaptcha"]/table/tbody/tr[1]/td/div/img')
    # src = img.get_attribute('src')


    # if __name__ == '__main__':
    img = driver.find_element(by=By.XPATH,
      value='//div[@id="ctl00_ContentPlaceHolder1_pnlCaptcha"]/table/tbody/tr[1]/td/div/img')
    url = img.get_attribute('src')
    
    
    capcode = ""
    # while (not capcode):
    # try:
    capcode = captcha_decode(url, DPATH)
    # except AttributeError:
    #     continue
    print("'" + capcode + "'")
    capinp = WebDriverWait(driver, 10) \
            .until(EC.element_to_be_clickable(
                    (By.NAME, 'ctl00$ContentPlaceHolder1$TextBox1')))
    capinp.clear()
    capinp.send_keys(capcode)
    time.sleep(1)
    viewr = driver.find_element(by=By.NAME, 
      value='ctl00$ContentPlaceHolder1$btnviewresult')
    # time.sleep(2)
    # time.sleep(1)
    viewr.click()
    time.sleep(2)


    try:
        WebDriverWait(driver, 0) \
        .until(EC.alert_is_present())
        
        alert = None
        alert = driver.switch_to.alert

        print(alert.text)
        if alert.text == 'Result for this Enrollment No. not Found':
            print("enrollment error for enr no." ,enr)
            alert.accept()
            i+=1
            reset = driver.find_element(By.XPATH,
              '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]')
            reset.click()
            continue
        elif alert.text == 'you have entered a wrong text':
            print('CAPTCHA ERROR')
            caperror+=1
            alert.accept()
    except TimeoutException:
        from selenium.common.exceptions import NoSuchElementException
        try:
            # In case captcha_decode gives an empty string.
            viewr = driver.find_element(by=By.NAME,
                    value='ctl00$ContentPlaceHolder1$btnviewresult')
            if(viewr):
                print(viewr)
                raise ValueError
        except ValueError:
            driver.get('%s' % RESULT_URL)
            print('INFO MISSING')
            continue
        except NoSuchElementException:
            pass
        print("NO ALERT...")
        # time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml') 
        documentObjectModel = etree.HTML(str(soup)) 
        student.append((soup.find('span',
            id="ctl00_ContentPlaceHolder1_lblNameGrading")).string)
        student.append((soup.find('span',
            id="ctl00_ContentPlaceHolder1_lblRollNoGrading")).string)
        student.append((soup.find('span',
            id="ctl00_ContentPlaceHolder1_lblResultNewGrading")).string)
        student.append((soup.find('span',
            id="ctl00_ContentPlaceHolder1_lblSGPA")).string)
        student.append((soup.find('span',
            id="ctl00_ContentPlaceHolder1_lblcgpa")).string)
        grade.append(documentObjectModel.xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[2]/tbody/tr/td[4]'
            )[0].text)
        grade.append(documentObjectModel.xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[3]/tbody/tr/td[4]'
            )[0].text)
        grade.append(documentObjectModel.xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[4]/tbody/tr/td[4]'
            )[0].text)
        grade.append(documentObjectModel.xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[5]/tbody/tr/td[4]'
            )[0].text)
        grade.append(documentObjectModel.xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[6]/tbody/tr/td[4]'
            )[0].text)
        grade.append(documentObjectModel.xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[7]/tbody/tr/td[4]'
            )[0].text)
        grade.append(documentObjectModel.xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[8]/tbody/tr/td[4]'
            )[0].text)
        grade = list(map(str.strip,grade))
        student.extend(grade)
        reset = driver.find_element(By.XPATH,
          '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]')
        reset.click()
        grade=[]    
        i+=1
        records += 1
    # except AttributeError:
    #     print("ERRRRR")
    #     continue
    time.sleep(2)
driver.close()
print()
print(student)
print()
print('Captcha recognition failed ', caperror, ' times!')
excelfile = SHEETNAME + '.xlsx'
df = pd.DataFrame()
df['Name'] = student[0::12]
df['Enrollment'] = student[1::12]
df['Result'] = student[2::12]
df['SGPC'] = student[3::12]
df['CGPA'] = student[4::12]
df['Sub1'] = student[5::12]
df['Sub2'] = student[6::12]
df['Sub3'] = student[7::12]
df['Sub4'] = student[8::12]
df['Sub5'] = student[9::12]
df['Sub6'] = student[10::12]
df['Sub7'] = student[11::12]
with pd.ExcelWriter(excelfile, engine='openpyxl') as writer:  
    df.to_excel(writer, 
                sheet_name=SHEETNAME + '-' + str(int(time.time())), 
                index = True)
print(f'Data extraction done. {records} records extracted to Excel.\n')
print("Press Ctrl+c to exit.")
# import sys
# sys.stdin.read(1)
# sys.exit()

# for filename in glob.glob("C:/Users/Nice/captchaImage*"):
#     os.remove(filename) 
#     print(filename," removed")


# %%
