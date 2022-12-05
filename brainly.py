from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
cwd = os.getcwd()

opts = webdriver.ChromeOptions()

opts.headless = True
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--disable-setuid-sandbox')
opts.add_argument('--log-level=3') 
opts.add_argument('--deny-permission-prompts')
opts.add_argument('--disable-infobars')
opts.add_argument('--no-sandbox')
opts.add_argument('--ignore-certifcate-errors')
opts.add_argument('--ignore-certifcate-errors-spki-list')
opts.add_argument("--incognito")
opts.add_argument('--no-first-run')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument("--disable-infobars")
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option("useAutomationExtension", False)
opts.add_experimental_option("excludeSwitches",["enable-automation"])
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
opts.add_argument('--disable-notifications')

def date():
    date = f"[{time.strftime('%d-%m-%y %X')}]"
    return date

def xpath_fast(el):
    element_all = wait(browser,3).until(EC.presence_of_element_located((By.XPATH, el)))
    return browser.execute_script("arguments[0].click();", element_all)

def xpath_type(el,mount):
    return wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)

def xpath_el(el):
    element_all = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el)))
    
    return browser.execute_script("arguments[0].click();", element_all)
        
def open_browser(inputs,pages):
    
    browser.get(f'https://brainly.co.id/app/ask?entry=hero&q={inputs}')
    for i in range(1,pages+1):
        try:
            get_result = wait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="search-item-facade-wrapper"]/a')))
            urls = [ x.get_attribute('href').split("?referrer")[0].split('brainly.co.id/')[1].split('/')[1] for x in get_result]
            print(f'{date()} Page {i}: Jumlah hasil yang didapat {len(urls)}')
            browser.execute_script('''window.open("","_blank");''')
            browser.switch_to.window(browser.window_handles[1])
            for e,i in enumerate(urls):
                try:
                    browser.get(f'https://brainly.co.id/tugas/{i}/?referrer=searchResults')
                    try:
                        question = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="question_box_text"]'))).text.strip()
                        answer = wait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"AnswerBoxLayout-module__content")]')))
                    except:
                        sleep(3)    
                        question = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="question_box_text"]'))).text.strip()
                        answer = wait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"AnswerBoxLayout-module__content")]')))
                    collect_answer = []
                    try:
                        for ans in answer:
                            try:
                                browser.execute_script("arguments[0].scrollIntoView();", i)
                                collect_answer.append(ans.text.strip())
                            except:
                                pass
                    except:
                        if len(collect_answer) == 0:
                            collect_answer == ""
                    collect_image = []
                    try:
                        imgs = wait(browser,1).until(EC.presence_of_all_elements_located((By.XPATH, '//img[@alt="lampiran aktif"]')))
                        for img in imgs:
                            try:
                                collect_image.append(img.get_attribute('src'))
                            except:
                                pass
                    except:
                        collect_image=''
                    with open('success.txt','a') as f:
                        f.write(f'{question}|{" -".join(collect_answer).strip()}|{" -".join(collect_image).strip()}\n')
                    print(f'{date()} {e+1} Question scrapped successfully')
                except Exception as e:
                    pass
            browser.close()
            try:
                browser.switch_to.window(browser.window_handles[0])
            except:
                pass
            xpath_el('(//label[@class="sg-text sg-text--xsmall sg-text--link sg-text--bold sg-text--link-label"])[2]')
        except ConnectionAbortedError or ConnectionError or ConnectionRefusedError or ConnectionResetError:
            print(f'{date()} Connection Error')
            input(f'{date()} Enter to Continue or CTRL + C to Exit')
        except:
            pass
    
if __name__ == '__main__':
    global browser
    global element
    print(f"{date()} Automation Scrape Brainly")
    input_url = input(f"{date()} Input keyword: ")
    pages = int(input(f"{date()} How much pages: "))
    opts.add_argument(f"user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36")
    browser = webdriver.Chrome(ChromeDriverManager().install(),options=opts, desired_capabilities=dc)
    open_browser(input_url,pages)