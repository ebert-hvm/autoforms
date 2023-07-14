from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.action_chains import ActionChains
import time
import random


def rand_ans(prob):
    ans = 3
    r = 100*random.random()
    if r < prob[0]:
        ans *= 0
    elif r < prob[0]+prob[1]:
        ans *= 1
    elif r < prob[0]+prob[1]+prob[2]:
        ans *= 2
    elif r < prob[0]+prob[1]+prob[2]+prob[3]:
        ans *= 3
    else:
        ans *= 4
    return ans

def get_credentials():
    global avaliador
    with open("credentials.txt", "r") as f:
        lines = f.readlines()
        avaliador = lines[2]
        return lines[0], lines[1]

def get_names(avaliador, ignored):
    names = {}
    with open("names.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            num, name, classroom = line.strip().split(",")
            names[name] = [num, classroom]
    if avaliador in names.keys():
        del names[avaliador]
    
    for name in ignored:
        if name in names.keys():
            del names[name]
    print(names)
    return names

def get_input():
    avaliador = ''
    email = ''
    senha = ''
    prob = []
    ignored = []
    with open("input.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f.readlines()):
            line = line.strip()
            if i == 0:
                avaliador = line
            elif i==1:
                email = line
            elif i==2:
                senha = line
            elif i<8:
                prob.append(int(line))
            else:
                ignored.append(line)
    return avaliador, email, senha, prob, ignored

def login_webdriver(usernamestr, passwordstr, driver):
    username = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "identifierId")))
    username.send_keys(usernamestr)
    
    nextButton = driver.find_element(By.ID, "identifierNext")
    nextButton.click()
    password = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME, "password")))
    password.send_keys(passwordstr)
    time.sleep(0.5)
    signInButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "passwordNext")))
    signInButton.click()

def fill(driver, avalstr, namestr, numstr, classroomstr, prob):
    # preenchendo avaliador
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div"))).click()
    time.sleep(0.5)
    elements = driver.find_elements(By.XPATH, f'//div[@class="MocG8c HZ3kWc mhLiyf OIC90c LMgvRb"]')
    for el in elements:
        if el.text == avalstr:
            print(el.text)
            #ActionChains(driver).move_to_element(el).click(el).perform()
            el.click()
            #time.sleep(1)
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdg1k2PXu6Pr7bikcAmp_7fkaDVHqykNhWBaMJsgEg_-D8BdA/viewform")
    
    # preenchendo avaliado
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div"))).click()
    time.sleep(0.5)
    elements = driver.find_elements(By.XPATH, f'//div[@class="MocG8c HZ3kWc mhLiyf OIC90c LMgvRb"]')
    
    for el in elements:
        if el.text == namestr:
            print(el.text)
            el.click()
            #time.sleep(1)
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdg1k2PXu6Pr7bikcAmp_7fkaDVHqykNhWBaMJsgEg_-D8BdA/viewform")
    
    # preenchendo turma
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div"))).click()
    time.sleep(0.5)
    elements = driver.find_elements(By.XPATH, f'//div[@class="MocG8c HZ3kWc mhLiyf OIC90c LMgvRb"]')
    for el in elements:
        if el.text == f'1º Ano - {classroomstr}':
            print(el.text)
            el.click()
            #time.sleep(1)
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdg1k2PXu6Pr7bikcAmp_7fkaDVHqykNhWBaMJsgEg_-D8BdA/viewform")
    #driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdg1k2PXu6Pr7bikcAmp_7fkaDVHqykNhWBaMJsgEg_-D8BdA/viewform")
    
    # preenchendo numero
    num = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")))
    time.sleep(0.5)
    num.send_keys(numstr)

    # preenchendo bolinhas
    for cnt in range(21,591,19):
        id_num = cnt+rand_ans(prob)
        print(id_num)
        button = driver.find_element(By.ID, f"i{id_num}")
        button.click()
    time.sleep(0.5)

def clear(driver):
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/form/div[2]/div/div[3]/div[2]/div[3]/div"))).click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[3]/div[2]"))).click()

def send_email(driver):
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i587"]'))).click()

def submit(driver):
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div[2]/div[1]/div"))).click()
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdg1k2PXu6Pr7bikcAmp_7fkaDVHqykNhWBaMJsgEg_-D8BdA/viewform")
    
avaliador, email, senha, prob, ignored = get_input()
names = get_names(avaliador, ignored)


#clear(driver)

while True:
    try:
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdg1k2PXu6Pr7bikcAmp_7fkaDVHqykNhWBaMJsgEg_-D8BdA/viewform")

        login_webdriver(email, senha, driver)
    except Exception:
        print(Exception)
        print('tentando dnv em 5s')
        time.sleep(5)
        continue
    else:
        break

for name in names:
    while True:
        try:
            fill(driver, avaliador, name, names[name][0], names[name][1], prob)
            send_email(driver)
            submit(driver)
        except Exception:
            print(Exception)
            print(name)
            print('tentando dnv em 5s')
            time.sleep(5)
            continue
        else:
            print(name)
            break