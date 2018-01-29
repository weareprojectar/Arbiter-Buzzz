## @Ver     0.8v
## @Author  김세희, 박시형 (Phillip)
## @Date    2017/12/18
## @Details KRX 홈페이지에서 ticker 데이터 스크레이핑

from restapi.models import Ticker
from datetime import datetime
from selenium import webdriver
import pyautogui
import os
from bs4 import BeautifulSoup
import requests
import time


class KRX(object):
    def __init__(self, start_path):
        gecko = start_path + '/geckodriver.exe'
        self.driver = webdriver.Firefox(executable_path=gecko)

    #사이트 접속
    def accessToKRX(self):
        self.driver.get('http://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage')
        time.sleep(4)

    #코스피/코스닥 항목 검색
    def search(self, btn_id):
        btn = self.driver.find_element_by_id(btn_id)
        btn.click()
        self.driver.execute_script('fnSearchWithoutIndex();') #검색 버튼
        time.sleep(3)

    #코스피 엑셀 파일 다운로드
    def downloadKospi(self):
        self.driver.execute_script('fnDownload();')
        time.sleep(4)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(3)

    #코스닥 엑셀 파일 다운로드
    def downloadKosdaq(self):
        self.driver.execute_script('fnDownload();')
        time.sleep(4)
        pyautogui.press('enter')
        time.sleep(4)

    #탭 종료
    def closeKRX(self):
        self.driver.close()


class KosFile():
    def __init__(self, downLoadPath):
        self.downLoadPath = downLoadPath

    #다운로드 폴더로 이동
    def moveToFileDirection(self):
        os.chdir(self.downLoadPath)

    #xls -> txt 변환
    def changeToTxt(self, fileName):
        if (os.path.isfile(fileName) and fileName == "상장법인목록.xls" ):
            os.rename(fileName, 'KOSPI.txt')
        elif (os.path.isfile(fileName) and fileName == "상장법인목록(1).xls"):
            os.rename(fileName, 'KOSDAQ.txt')

    #파일 열기
    def openFile(self, fileName):
        self.kosDoc = open(fileName, "r")
        self.kosSoup = BeautifulSoup(self.kosDoc, "html.parser")

    #파일 지우기
    def deleteFile(self, fileName):
        self.kosDoc.close()
        os.remove(fileName)

    #회사코드 찾기
    def findCompanyCode(self):
        return self.kosSoup.select('td[style*="@"]')

    #회사 정보 가져와서 저장
    def companies(self, date, companyCode, market):
        tickers_list = []
        for i in range(len(companyCode)):
            company = companyCode[i].find_previous_sibling('td').string
            code = companyCode[i].string
            industry = companyCode[i].find_next().string
            #db에 저장
            data = Ticker(code=code, date=date, name=company, market_type=market)
            tickers_list.append(data)
        Ticker.objects.bulk_create(tickers_list)


def main(start_path):

    #오늘의 날짜
    date = datetime.now().strftime('%Y%m%d')

    #코스피, 코스닥 excel 파일 다운로드
    krx = KRX(start_path)
    krx.accessToKRX()
    krx.search('rWertpapier')
    krx.downloadKospi()
    krx.search('rKosdaq')
    krx.downloadKosdaq()
    krx.closeKRX()

    download_dir = os.path.expanduser('~/Downloads') # default download directory for both windows and unix systems

    #객체 생성
    kos = KosFile(download_dir)
    #다운로드 폴더로 이동
    kos.moveToFileDirection()

    #########코스피
    kos.changeToTxt('상장법인목록.xls')
    kos.openFile('KOSPI.txt')

    #종목별 코드 찾기
    kospiCompanyCode = kos.findCompanyCode()

    #코스피 회사명, 회사코드, 종목 저장
    kos.companies(date, kospiCompanyCode, "KP")

    #코스피 파일 지우기
    kos.deleteFile('KOSPI.txt')

    ########코스닥
    kos.changeToTxt('상장법인목록(1).xls')
    kos.openFile('KOSDAQ.txt')

    #종목별 코드 찾기
    kosdaqCompanyCode = kos.findCompanyCode()

    #코스닥 회사명, 회사코드, 종목 저장
    kos.companies(date, kosdaqCompanyCode, "KD")

    #코스닥 파일 지우기
    kos.deleteFile('KOSDAQ.txt')

    print('Successfully sent KRX ticker data')

# if __name__=="__main__":
#     main()
