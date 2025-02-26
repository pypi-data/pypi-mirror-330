# 2023/10/16 빌드
# 2023/12/27 셀레니움 세이프브라우징 해제 옵션 추가
# 2024/08/22 Teams 채팅 메시지 함수 추가

from myinfo import *
from colorama import init, Back, Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep
import pytesseract
import shutil
import os
import sys
import pyperclip
import requests
import json

# colorama 초기화
init(autoreset=True)

# 날짜
now = datetime.now()
today = datetime.today().strftime('%Y-%m-%d')
date_mdhm = now.strftime('%m%d%H%M')
temp_folder = 'c:/rpa_temp/'

# temp_folder 초기화
if os.path.isdir(temp_folder) :
    for file in os.listdir(temp_folder):
        try:
            shutil.rmtree(temp_folder)
        except Exception as e:
            pass

if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# 확인 팝업 처리
def handle_alert(driver):
    while True:
        try:
            alert = driver.switch_to.alert
            alert.accept()
            break
        except:
            sleep(1)

# 로딩 처리
def handle_loading(driver):
    while True:
        try:
            # 얼럿이 있는지 먼저 확인
            alert = driver.switch_to.alert
            # 얼럿이 존재할 경우 아무 작업도 하지 않음
            break  # 얼럿이 있어도 계속 대기
        except NoAlertPresentException:
            # 얼럿이 없을 경우 로딩 요소가 더 이상 존재하지 않을 때까지 대기
            try:
                WebDriverWait(driver, 1).until_not(EC.presence_of_element_located((By.ID, 'loading')))
                sleep(1)
                break
            except TimeoutException:
                # 로딩이 계속 진행 중일 경우 계속 대기
                continue

# 로그 타임 처리
def current_time():
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    time_list = time_str.split(" ")
    time_str = "[" +  time_list[0] + " " + time_list[1] + "]"
    return time_str

# 크롬 실행
def create_webbrowser():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-features=InsecureDownloadWarnings")
    # options.add_argument("--headless")
    options.add_experimental_option('detach', True)  # 브라우저 바로 닫힘 방지
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 불필요한 메시지 제거
    options.add_experimental_option('prefs', {'download.default_directory':r'C:\rpa_temp' , 'safebrowsing.enabled': 'False'})
    driver = webdriver.Chrome(options=options)

    return driver

# sdp url 처리
def get_text_after_pattern(pattern):
    patterns = {
        "PRD": "",
        "QA": "qt-",
        "QA2": "qt2-",
    }
    if pattern in patterns:
        return patterns[pattern]
    return None

# SDP 자동 로그인
def sdp_login(target_server):
    server_url = get_text_after_pattern(target_server)
    url = f'http://{server_url}kic.smartdesk.lge.com/admin/main.lge'
    if target_server == 'PRD':
        print(f'[RPA] 운영 서버에 {EPID} 계정으로 로그인 합니다.')
        options = Options()
        options.page_load_strategy = 'none'  # 'none'으로 설정하면 타임아웃 없이 계속 로드됨
        options.add_argument("--start-maximized")
        options.add_argument("--disable-features=InsecureDownloadWarnings")
        options.add_experimental_option('detach', True)  # 브라우저 바로 닫힘 방지
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 불필요한 메시지 제거
        options.add_experimental_option('prefs', {'download.default_directory':r'C:\rpa_temp' , 'safebrowsing.enabled': 'False'})
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        driver.implicitly_wait(2)
        driver.find_element(By.ID,'USER').send_keys(EPID)
        driver.find_element(By.ID,'LDAPPASSWORD').send_keys(EPPW)
        driver.implicitly_wait(2)
        driver.find_element(By.ID,'OTP').click()

        driver.switch_to.window(driver.window_handles[1])

        driver.find_element(By.ID,'pw').send_keys(EPPW)
        driver.find_element(By.ID,'myButton').click()

        sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element(By.XPATH,'//*[@id="TA_01"]/div[4]/div[1]').click()
        driver.switch_to.window(driver.window_handles[2])

        while True:
            try:
                driver.refresh()
                element1 = driver.find_element(By.ID,'photo_imageK')
                element_png = element1.screenshot_as_png 
                with open("otpimg.png", "wb") as file: file.write(element_png)
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
                otpimg = pytesseract.image_to_string(r'otpimg.png')
                driver.find_element(By.ID,'bizidK').send_keys(XID)
                driver.find_element(By.ID,'pcodeK').send_keys(BDAY)
                driver.find_element(By.ID,'answerK').send_keys(otpimg.replace(" ",""))
                driver.find_element(By.XPATH,'//*[@id="form1"]/div[1]/table/tbody/tr[8]/td/input[1]').click() 
                sleep(2) 
                try:
                    sleep(1)
                    result = Alert(driver)
                    print("[RPA] OTP 입력 오류, 재시도 합니다.")
                    result.accept()
                except:
                    print("[RPA] OTP 정상 입력.")
                    break
            except:
                pass

        sleep(1)
        driver.switch_to.window(driver.window_handles[3])
        OTPD = driver.find_element(By.XPATH,'//*[@id="loadingK"]/b').text
        driver.close()
        driver.switch_to.window(driver.window_handles[2])
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element(By.ID,'OTPPASSWORD').send_keys(OTPD)
        driver.find_element(By.ID,'loginSsobtn').click() 
        
        while True:
            try:
                driver.get(url)
                sleep(0.5)
                driver.find_element(By.ID,'USER').send_keys(EPID)
                driver.find_element(By.ID,'LDAPPASSWORD').send_keys(EPPW)
                input(f'{Fore.RED}[ERROR] 로그인 오류, 수동 로그인 후 엔터키 입력..{Style.RESET_ALL}')
                continue
            except:
                break  

        return driver

    elif target_server == 'QA':
        print(f'[RPA] QA 서버에 {QAID} 계정으로 로그인 합니다.')
        server_url = get_text_after_pattern(target_server)
        url = f'http://{server_url}kic.smartdesk.lge.com/admin/main.lge'
        options = Options()
        options.page_load_strategy = 'none'  # 'none'으로 설정하면 타임아웃 없이 계속 로드됨
        options.add_argument("--start-maximized")
        options.add_argument("--disable-features=InsecureDownloadWarnings")
        options.add_experimental_option('detach', True)  # 브라우저 바로 닫힘 방지
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 불필요한 메시지 제거
        options.add_experimental_option('prefs', {'download.default_directory':r'C:\rpa_temp' , 'safebrowsing.enabled': 'False'})
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        handle_alert(driver)
        driver.find_element(By.ID,'USER').send_keys(QAID)
        driver.find_element(By.ID,'LDAPPASSWORD').send_keys(QAPW)
        driver.find_element(By.ID,'loginSsobtn').click() 
        # 비밀번호 변경 메시지 처리
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            pass

        pyperclip.copy(url)
        print('[RPA] QA서버 http 접근을 위해, 브라우저에서 url 을 직접 입력해 주세요 (url 이 복사 되었습니다.)')

        while True :
            if url in driver.current_url:
                break
            else:
                print(f'[RPA] url 입력 까지 대기 합니다.')
                print(f'[RPA] 현제 페이지 : {driver.current_url}')
                sleep(3)
        return driver

    else :
        print(f'[RPA] QA2 서버에 {QAID} 계정으로 로그인 합니다.')
        server_url = get_text_after_pattern(target_server)
        url = f'http://{server_url}kic.smartdesk.lge.com/admin/main.lge'
        options = Options()
        options.page_load_strategy = 'none'  # 'none'으로 설정하면 타임아웃 없이 계속 로드됨
        options.add_argument("--start-maximized")
        options.add_argument("--disable-features=InsecureDownloadWarnings")
        options.add_experimental_option('detach', True)  # 브라우저 바로 닫힘 방지
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 불필요한 메시지 제거
        options.add_experimental_option('prefs', {'download.default_directory':r'C:\rpa_temp' , 'safebrowsing.enabled': 'False'})
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        handle_alert(driver)
        driver.find_element(By.ID,'USER').send_keys(QAID)
        driver.find_element(By.ID,'LDAPPASSWORD').send_keys(QAPW)
        driver.find_element(By.ID,'loginSsobtn').click() 
        # 비밀번호 변경 메시지 처리
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            pass
        driver.get(url)
        return driver

# 화면 보호기 방지
import ctypes
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
SetThreadExecutionState = ctypes.windll.kernel32.SetThreadExecutionState
# 화면 보호기 방지 설정
def prevent_screensaver():
    return SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)
# 화면 보호기 방지 해제 설정
def allow_screensaver():
    return SetThreadExecutionState(ES_CONTINUOUS)

# 오브 젝트 조작
def find_e(driver, locator, action, value=None, index=None, timeout=10, max_tries=3):
    for i in range(max_tries):
        try:
            elements = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(locator))
            if index is not None:
                element = elements[index]
            else:
                element = elements[0]
            if action == 'click':
                element.click()
            elif action == 'send_keys':
                element.send_keys(value)
            elif action == 'clear':
                element.clear()
            else:
                raise ValueError(f"Unsupported action '{action}'")
            break
        except TimeoutException:
            print(current_time(),f"Timeout waiting for element located by {locator}, attempt {i+1} of {max_tries}")
    else:
        print(current_time(),f"Failed to locate element after {max_tries} tries")

def rpa_progress(status):
    # 현재 실행 중인 파이썬 파일명을 얻습니다.
    file_path = sys.argv[0]

    # 파일명만 추출합니다.
    file_name = os.path.basename(file_path)

    # 파일명 + '시작'을 출력합니다.
    print('\n[RPA] ' + current_time() + ' ' + file_name + ' ' +  status)

    return file_name


import ctypes
import os

ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
SetThreadExecutionState = ctypes.windll.kernel32.SetThreadExecutionState

# 화면 보호기 방지 설정
def prevent_screensaver():
    return SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)

# 화면 보호기 방지 해제 설정
def allow_screensaver():
    return SetThreadExecutionState(ES_CONTINUOUS)

# 디스플레이 끄기 및 절전 모드 비활성화
def disable_power_settings():
    os.system("powercfg -change -monitor-timeout-ac 0")
    os.system("powercfg -change -standby-timeout-ac 0")
    os.system("powercfg -change -hibernate-timeout-ac 0")

# 전원 설정 복구
def enable_power_settings(monitor_timeout, standby_timeout, hibernate_timeout):
    os.system(f"powercfg -change -monitor-timeout-ac {monitor_timeout}")
    os.system(f"powercfg -change -standby-timeout-ac {standby_timeout}")
    os.system(f"powercfg -change -hibernate-timeout-ac {hibernate_timeout}")

# HTTP POST 요청을 보내는 함수 정의
def print_webhook(webhook_url, webhook_data, n_print=None):
    # 전송할 데이터 구성
    data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": '🕹 ' + webhook_data,
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }
    
    # HTTP POST 요청 보내기
    response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
    
    # n_print가 없을 때만 print 호출
    if not n_print:
        print(webhook_data)
    
    return response

