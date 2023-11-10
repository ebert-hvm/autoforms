from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.action_chains import ActionChains
import time
import random

MARK_EMAIL = "/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div[1]/label/div/div[1]/div[2]"

def get_input():
    email = ''
    senha = ''
    prob = []
    cnt = 0
    with open("input.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f.readlines()):
            line = line.strip()
            if i == 0:
                email = line
            elif i==1:
                senha = line
            else:
                val = int(line)
                prob.append(val)
                cnt += val
    if cnt != 100:
        raise ValueError("As probabilidades devem somar 100!")
    return email, senha, prob

def login_webdriver(usernamestr, passwordstr, driver):
    username = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "identifierId")))
    username.send_keys(usernamestr)
    nextButton = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span")
    nextButton.click()
    password = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")))
    password.send_keys(passwordstr)
    time.sleep(0.2)
    signInButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span")))
    signInButton.click()

def click_ball(driver, name_index, field_index, ball_index):
    base_path = '/html/body/div[1]/div[2]/form/div[2]/div/div[2]'
    element_path = f"{base_path}/div[{name_index}]/div/div/div[2]/div/div[1]/div/div[{field_index}]/span/div[{ball_index}]/div"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, element_path))).click()

def main():
    email, senha, prob = get_input()
    while True:
        try:
            driver = webdriver.Firefox()
            driver.maximize_window()
            driver.get("https://docs.google.com/forms/d/e/1FAIpQLSeXvezWsuSI3yACOZh3w02IrdFD7H4NjTb7Er6NlqP6uyxnJQ/viewform")
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div[3]/div[2]/span/span'))).click()
            login_webdriver(email, senha, driver)
        except Exception:
            print(Exception)
            print('tentando dnv em 5s')
            time.sleep(5)
            continue
        else:
            break
    time.sleep(2)
    for i in range(4,67):
        for j in range(2,22,2):
            num = random.choices(range(2, 8), weights=prob)[0]
            click_ball(driver, i, j, num)

if __name__ == "__main__":
    main()