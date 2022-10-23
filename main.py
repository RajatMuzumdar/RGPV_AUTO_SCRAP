import pandas as pd
import requests
import time
from enum import Enum, auto
from win32com.client import Dispatch

# from sre_constants import BRANCH
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

import analysis
import config
import input_utils
from captcha_utils import create_dir

class WebpageFields():

    def __init__(self):
        self.navigateRadio = ''
        self.RESULT_URL = ''
        self.PREFIX = ''
        self.SEM = 0
        self.FROM = 0
        self.TO = 0
        self.SHEETNAME = ''
        self.enrList = []
        self.BRANCH = ''


class Status(Enum):
    OK = auto()
    NUM_NOT_FOUND = auto()
    CAPTCHA_ERROR = auto()
    INFO_ERROR = auto()
    UNKNOWN_ERROR = auto()


def init(debug=False, headless=False):

    global driver, debug_setting, DPATH
    debug_setting = debug


    DPATH = create_dir('temp')

    def get_version_via_com(filename):
        parser = Dispatch("Scripting.FileSystemObject")
        try:
            version = parser.GetFileVersion(filename)
        except Exception:
            return None
        return version

    def get_latest_driver_version():
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        curVersion = list(filter(None,
                                 [get_version_via_com(p) for p in paths]))[0]
        versionToFetch = int(curVersion[0:curVersion.find('.')]) - 1
        versionToFetch = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'\
            + str(versionToFetch)
        response = requests.get(versionToFetch)
        return response.text

    from selenium.webdriver import Chrome, ChromeOptions

    opts = ChromeOptions()
    opts.add_argument("--window-size=800,600")
    if headless is True:
        opts.add_argument('--disable-gpu')
        opts.add_argument('--headless')

    # from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    versionNumber = get_latest_driver_version()

    if debug_setting:
        return webdriver.Chrome(config.BROW_DRIVER, options=opts)
    # svc = Service(ChromeDriverManager(version=versionNumber).install())
    # return webdriver.Chrome(service=svc, options=opts)
    return webdriver.Chrome(
        ChromeDriverManager(version=versionNumber).install(), options=opts)
    # return webdriver.Chrome( executable_path=r"C:\Program Files\chromedriver", options=opts )
    # driver = webdriver.Chrome(service=svc, options=opts)


def takeinput():
    
    inputReceived = False
    while (not inputReceived):
        userInput = input_utils.get_input()
        if (not input_utils.validate(userInput)):
            continue
        if (input_utils.confirm(userInput)):
            inputReceived = True

    navigateRadio = {
        'D': '/html/body/form/div[3]/div[2]/div[1]/fieldset/table/tbody/tr/td[13]/input',
        'M': '/html/body/form/div[3]/div[2]/div[1]/fieldset/table/tbody/tr/td[18]/input'
    }
    branchResult = {
        'D': 'http://result.rgpv.ac.in/Result/McaDDrslt.aspx',
        'M': 'http://result.rgpv.ac.in/Result/MCArslt.aspx'
    }

    branch = {'D': 'DDMCA', 'M': 'MCA'}

    page = WebpageFields()

    B = userInput['class'][0].upper()
    page.navigateRadio = navigateRadio[B]
    page.BRANCH = branch[B]
    page.RESULT_URL = branchResult[B]
    page.PREFIX = userInput['prefix']
    page.SEM = int(float(userInput['semester']))
    page.FROM = int(float(userInput['from']))
    page.TO = int(float(userInput['to']))
    # SHEETNAME = MCADD CA19 SEM 6 _unique-id_
    page.SHEETNAME = (f"{userInput['class']} {page.PREFIX[-6:-2]} "
                      f"SEM {page.SEM} uid_{int(time.time())}")
    page.enrList = input_utils.enrgenerator(page.PREFIX, page.FROM, page.TO)
    return page, bool(userInput['hidechrome'])


def automate(pgObj: WebpageFields, i: int) -> Status:

    from captcha_utils import captcha_decode

    global driver, caperror, DPATH, debug_setting

    enrollment = WebDriverWait(driver, 0) \
                .until(EC.element_to_be_clickable(
                        (By.NAME, 'ctl00$ContentPlaceHolder1$txtrollno')))
    year    =   WebDriverWait(driver, 0) \
                .until(EC.element_to_be_clickable(
                        (By.NAME, 'ctl00$ContentPlaceHolder1$drpSemester')))
    capinp  =   WebDriverWait(driver, 0) \
                .until(EC.element_to_be_clickable(
                        (By.NAME, 'ctl00$ContentPlaceHolder1$TextBox1')))
    capinp =    WebDriverWait(driver, 10) \
                .until(EC.element_to_be_clickable(
                        (By.NAME, 'ctl00$ContentPlaceHolder1$TextBox1')))
    enrollment.clear()
    capinp.clear()
    capinp.clear()

    img = driver.find_element(
        by=By.XPATH,
        value=
        '//div[@id="ctl00_ContentPlaceHolder1_pnlCaptcha"]/table/tbody/tr[1]/td/div/img'
    )
    url = img.get_attribute('src')

    enr = pgObj.enrList[i]
    enrollment.send_keys(enr)
    year.send_keys(pgObj.SEM)

    capcode = captcha_decode(url, DPATH)
    if (debug_setting):
        prefix = "DEBUG: "
        print()
        print(prefix, enr)
        print(prefix, f"'{capcode}'")
    capinp.send_keys(capcode)

    time.sleep(2)
    viewr = driver.find_element(
        by=By.NAME, value='ctl00$ContentPlaceHolder1$btnviewresult')
    # time.sleep(2)
    # time.sleep(1)
    viewr.click()
    time.sleep(3)

    stat = Status(Status.OK)
    try:
        WebDriverWait(driver, 0) \
        .until(EC.alert_is_present())

        alert = None
        alert = driver.switch_to.alert

        if (debug_setting):
            print(alert.text)

        if alert.text == 'Result for this Enrollment No. not Found':
            alert.accept()
            reset = driver.find_element(
                By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]')
            reset.click()
            stat = Status.NUM_NOT_FOUND
            # i+=1
            # print(f"Result for {enr} NOT FOUND.")
            # return Status.NUM_NOT_FOUND
        elif alert.text == 'you have entered a wrong text':
            caperror += 1
            alert.accept()
            stat = Status.CAPTCHA_ERROR
            # print('CAPTCHA ERROR')
            # return Status.CAPTCHA_ERROR
        else:
            stat = Status.ERROR_UNKNOWN
    except TimeoutException:
        from selenium.common.exceptions import NoSuchElementException
        try:
            # In case captcha_decode gives an empty string.
            viewr = driver.find_element(
                by=By.NAME, value='ctl00$ContentPlaceHolder1$btnviewresult')
            if (viewr):
                print(viewr)
                raise ValueError
        except ValueError:
            driver.get('%s' % pgObj.RESULT_URL)
            stat = Status.INFO_ERROR
            # print('INFO MISSING')
        except NoSuchElementException:
            # print("NO ALERT...")
            stat = Status.OK
            # return Status.OK
    finally:
        print()
        if (debug_setting):
            if stat == Status.INFO_ERROR:
                print(prefix, "INFO ERROR")
            elif stat == Status.CAPTCHA_ERROR:
                print(prefix, "CAPTCHA ERROR")
            elif stat == Status.UNKNOWN_ERROR:
                print(prefix, "UNKNOWN ERROR")
        prefix = "STATUS:"
        if (stat == Status.NUM_NOT_FOUND):
            print(prefix, f"Result for {enr} NOT FOUND.")
        elif (stat == Status.OK):
            print(prefix, f"{enr} details fetched.")
        # print()
        return stat


def scrape(pgObj: WebpageFields, studentsList: list):

    global driver, records

    gradesList = []
    idList_StuInfo = [
        "ctl00_ContentPlaceHolder1_lblNameGrading",
        "ctl00_ContentPlaceHolder1_lblRollNoGrading",
        "ctl00_ContentPlaceHolder1_lblResultNewGrading",
        "ctl00_ContentPlaceHolder1_lblSGPA",
        "ctl00_ContentPlaceHolder1_lblcgpa"
    ]
    idList_DdmcaGrade = [
        '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[2]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[3]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[4]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[5]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[6]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[7]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlshowRslt"]/table/tbody/tr[3]/td/table[8]/tbody/tr/td[4]'
    ]
    idList_McaGrade = [
        '//*[@id="ctl00_ContentPlaceHolder1_pnlGrading"]/table/tbody/tr[3]/td/table[2]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlGrading"]/table/tbody/tr[3]/td/table[3]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlGrading"]/table/tbody/tr[3]/td/table[4]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlGrading"]/table/tbody/tr[3]/td/table[5]/tbody/tr/td[4]',
        '//*[@id="ctl00_ContentPlaceHolder1_pnlGrading"]/table/tbody/tr[3]/td/table[6]/tbody/tr/td[4]'
    ]

    soup = BeautifulSoup(driver.page_source, 'lxml')
    documentObjectModel = etree.HTML(str(soup))
    for id in idList_StuInfo:
        studentsList.append((soup.find('span', id=id)).string)

    if pgObj.BRANCH == 'MCA':
        for id in idList_McaGrade:
            gradesList.append(documentObjectModel.xpath(id)[0].text)
    elif pgObj.BRANCH == 'DDMCA':
        for id in idList_DdmcaGrade:
            gradesList.append(documentObjectModel.xpath(id)[0].text)

    gradesList = list(map(str.strip, gradesList))
    studentsList.extend(gradesList)

    reset = driver.find_element(
        By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]')
    reset.click()
    records += 1


def extract(pgObj: WebpageFields, students: list):

    global caperror, records

    if debug_setting:
        print(students)
        print()
        print(f'Captcha recognition failed {caperror} times!')
    EXCELFILE = pgObj.SHEETNAME + '.xlsx'
    print(students)
    df = pd.DataFrame()
    if pgObj.BRANCH == 'DDMCA':
        df['Name'] = students[0::12]
        df['Enrollment'] = students[1::12]
        df['Result'] = students[2::12]
        df['SGPC'] = students[3::12]
        df['CGPA'] = students[4::12]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '01'] = students[5::12]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '02'] = students[6::12]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '03'] = students[7::12]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '04'] = students[8::12]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '05'] = students[9::12]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '06'] = students[10::12]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '07'] = students[11::12]

    elif pgObj.BRANCH == 'MCA':
        df['Name'] = students[0::10]
        df['Enrollment'] = students[1::10]
        df['Result'] = students[2::10]
        df['SGPC'] = students[3::10]
        df['CGPA'] = students[4::10]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '01'] = students[5::10]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '02'] = students[6::10]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '03'] = students[7::10]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '04'] = students[8::10]
        df[pgObj.BRANCH + ' ' + str(pgObj.SEM) + '05'] = students[9::10]

    with pd.ExcelWriter(EXCELFILE, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=pgObj.PREFIX, index=True)
    print('Data extraction done.')
    print(f'{records} records extracted to \'{pgObj.SHEETNAME}.xlsx\'.')
    print()
    
    analysis.getData(EXCELFILE,pgObj.BRANCH)
    print("Press Ctrl+c to exit.")


def main():

    global driver, records, caperror, DPATH

    pageData: WebpageFields
    pageData, _headless = takeinput()
    driver = init(headless=_headless)

    students = list()
    records = caperror = 0
    i = 0
    # i = pageData.FROM

    driver.get("http://result.rgpv.ac.in/Result/ProgramSelect.aspx")
    Radio = driver.find_element(by=By.XPATH,
                                value='%s' % pageData.navigateRadio)
    Radio.click()

    # while(i in range(pageData.FROM, pageData.TO + 1)):
    while i < len(pageData.enrList):
        # pageStatus = automate(driver, pageData, i)
        pageStatus = automate(pageData, i)
        if (pageStatus == Status.OK):
            scrape(pageData, students)
        if (pageStatus in (Status.NUM_NOT_FOUND, Status.OK)):
            i += 1
            time.sleep(3)
        # elif (pageStatus == Status.INFO_ERROR):
        # else:
        #     continue
    driver.close()
    extract(pageData, students)
    # cleanup(driver)


if __name__ == '__main__':
    main()
