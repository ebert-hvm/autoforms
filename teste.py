from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from requests_html import HTMLSession

prob = [2,3,10,20,65]

def rand_ans():
    ans = 3
    r = 100*random.random()
    if r < 2:
        ans *= 0
    elif r < 5:
        ans *= 1
    elif r < 15:
        ans *= 2
    elif r < 35:
        ans *= 3
    else:
        ans *= 4
    return ans

def get_credentials():
    with open('credentials.txt', 'r') as f:
        lines = f.readlines()
        return lines[0], lines[1]

#def login(user, password):
    url_login = 'https://docs.google.com/forms/d/e/1FAIpQLSetiktMP6mMr8WzE7gDp6WJ3yv7Lscj_JSdHKLzSY74koucNA/viewform'
    forms = get_all_forms(url_login)
    first_form = forms[0]
    form_details = get_form_details(first_form)
    data_login = {"txtUser": user, "txtSenha" : password}
    res, url = make_request(url_login, form_details, data_login)
    return res.status_code

def login_webdriver(usernamestr, passwordstr, browser):
    time.sleep(2)
    username = browser.find_element(By.ID, 'identifierId')
    username.send_keys(usernamestr)
    nextButton = browser.find_element(By.ID, 'identifierNext')
    nextButton.click()

    time.sleep(2)
    password = browser.find_element(By.NAME, 'password')
    password.send_keys(passwordstr)
    signInButton = browser.find_element(By.ID, 'passwordNext')
    signInButton.click()
    time.sleep(2)

def fill():
    button = browser.find_element(By.ID, 'i14')
    button.click()
    button = browser.find_element(By.ID, 'i27')
    button.click()
    button = browser.find_element(By.XPATH, '/html/body/div/div[3]/form/div[2]/div/div[3]/div/div[1]/div')
    button.click()
    
    

browser = webdriver.Firefox()
browser.get('https://docs.google.com/forms/d/e/1FAIpQLScMxEXb2fmkCNVOD_nx1jP-r2zbed-1YdBNyPgf_UJ8-pqyeQ/viewform')

usr, pswd = get_credentials()
#print('credentials ok')
login_webdriver(usr, pswd, browser)

limpar = browser.find_element(By.XPATH, '/html/body/div/div[3]/form/div[2]/div/div[3]/div/div[2]/div')
limpar.click()
confirmar = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[3]/div[2]')
confirmar.click()
time.sleep(2)

for i in range(65):
    fill()
    browser.get('https://docs.google.com/forms/d/e/1FAIpQLScMxEXb2fmkCNVOD_nx1jP-r2zbed-1YdBNyPgf_UJ8-pqyeQ/viewform')
#for i in range(30):
#    print(rand_ans()/3)

