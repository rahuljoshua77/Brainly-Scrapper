from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os,csv
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings, requests
warnings.filterwarnings("ignore", category=DeprecationWarning) 
cwd = os.getcwd()

opts = webdriver.ChromeOptions()
 
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,id;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'session=MTY3MDI2MjM1OXxOd3dBTkVsUVFrWkROVVpLTTAwMFQweFRVbFpMVmxsVFNrTkZXRkpPTXpWUVRrOUtVRWhZUVVWQ00xRTFRVXMzTWsxWE1rRlFXRkU9fPKotQBnbBfh9j-jARnc_axxvmpEabfS6pgBcjoCaEN_; authentication=MTY3MDI2MjM1OXxMbEMxYjNPa2YzX1lRa1JSOWFZNGR3b2htTW1VNWhoakFaOUVycnU0WjdwSDZ2WEF8LgwXDLjoyhzzsUicAykmrHwikBE3TBOUQmedOTk2KM4=',
    'DNT': '1',
    'Origin': 'https://www.klgrth.io',
    'Referer': 'https://www.klgrth.io/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}
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
    if not os.path.exists(f"{cwd}\\jawaban"):
        os.makedirs(f"{cwd}\\jawaban")
    if not os.path.exists(f"{cwd}\\pertanyaan"):
        os.makedirs(f"{cwd}\\pertanyaan")
    if not os.path.exists(f"{cwd}\\gambar"):
        os.makedirs(f"{cwd}\\gambar")
    browser.get(f'https://brainly.co.id/app/ask?entry=hero&q={inputs}')
    for i in range(1,pages+1):
        try:
            get_result = wait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="search-item-facade-wrapper"]/a')))
            urls = [ x.get_attribute('href').split("?referrer")[0].split('brainly.co.id/')[1].split('/')[1] for x in get_result]
            print(f'{date()} Page {i}: Jumlah hasil yang didapat {len(urls)}')
            browser.execute_script('''window.open("","_blank");''')
            browser.switch_to.window(browser.window_handles[1])
            for m,i in enumerate(urls):
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
                                browser.execute_script("arguments[0].scrollIntoView();", ans)
                                collect_answer.append(ans.text)
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
                    
                    with open('success.txt','a',encoding='utf-8') as f:
                            f.write(f'\n==========================\nPERTANYAAN:\n{question}')
                    data = {
                        'lang': 'text',
                        'text': question,
                        'expire': '-1',
                        'password': '',
                        'title': '',
                    }

                    response_question = requests.post('https://www.klgrth.io/paste/new', data=data)
                    code_question = response_question.text.split('<a title="View Raw" href="/paste/')[1].split('/raw')[0]
      
                    with open(f'{cwd}/pertanyaan/{code_question}.txt','a',encoding='utf-8') as f:
                        f.write(f'{question}')
                    string_ans = ""
                    try:
                        for ans_api in collect_answer:
                            string_ans = "Jawaban:\n"+ans_api.replace("Jawaban:","")+"\n"
                    except:
                        string_ans = collect_answer
                        
                    data = {
                        'lang': 'text',
                        'text': string_ans,
                        'expire': '-1',
                        'password': '',
                        'title': '',
                    }

                    response_answer= requests.post('https://www.klgrth.io/paste/new', data=data)
                    code_answer = response_answer.text.split('<a title="View Raw" href="/paste/')[1].split('/raw')[0]
                    
                    with open(f'{cwd}/jawaban/{code_answer}.txt','a',encoding='utf-8') as f:
                        f.write(f'{string_ans}')
                        
                    with open('success.txt','a',encoding='utf-8') as f:
                        f.write(f'\nJAWABAN:\n{string_ans.replace("Jawaban:","")}')
                    for ems in collect_image:
                        with open('success.txt','a',encoding='utf-8') as f:
                            f.write(f'\n==============\nGAMBAR:\n{ems}')
                    
                    string_img = ""
                    try:
                        for img in collect_image:
                            string_img = "\n"+img
                    except:
                        string_img = collect_image
                    
                    data = {
                        'lang': 'text',
                        'text': string_img,
                        'expire': '-1',
                        'password': '',
                        'title': '',
                    }
                    if len(collect_image) > 0:
                        response_img = requests.post('https://www.klgrth.io/paste/new', data=data)
                        code_img = response_img.text.split('<a title="View Raw" href="/paste/')[1].split('/raw')[0]
                        
                        print(code_img)
                        with open(f'{cwd}/gambar/{code_img}.txt','a',encoding='utf-8') as f:
                            f.write(f'{string_img}')
                    if len(collect_image) > 0: 
                        with open('data_txt.txt','a',encoding='utf-8') as f:
                            f.write(f'{code_question}.txt|{code_answer}.txt|{code_img}.txt')
                        with open('data_url.txt','a',encoding='utf-8') as f:
                            f.write(f'https://www.klgrth.io/paste/{code_question}/raw|https://www.klgrth.io/paste/{code_answer}/raw|https://www.klgrth.io/paste/{code_img}/raw')
                    else:
                        with open('data_txt.txt','a',encoding='utf-8') as f:
                            f.write(f'{code_question}.txt|{code_answer}.txt')
                        with open('data_url.txt','a',encoding='utf-8') as f:
                            f.write(f'https://www.klgrth.io/paste/{code_question}/raw|https://www.klgrth.io/paste/{code_answer}/raw')
                    
                           
                    print(f'{date()} {m+1} Question scrapped successfully')
                except Exception as err:
                    print(err)
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
