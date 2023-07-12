import requests
from datetime import datetime
from requests import session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import base64
import pytesseract
from PIL import Image 
import time as tt
import keyring

options = Options()
# options.add_argument("--headless")
# options.add_argument("--start-maximized")

driver = webdriver.Chrome(chrome_options=options, executable_path="/Users/jarvis/pymycod/automation/chromedriver")
driver.get("https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp")
wait = WebDriverWait(driver,10)
captchaaa = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/div[4]/div[2]/img')))
tt.sleep(5)
img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
          ele.removeEventListener('load', fn, false);
          var cnv = document.createElement('canvas');
          cnv.width = this.width; cnv.height = this.height;
          cnv.getContext('2d').drawImage(this, 0, 0);
          callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, captchaaa)
with open(r"/Users/jarvis/pymycod/automation/test folder/captcha.jpg", 'wb') as f:
    f.write(base64.b64decode(img_captcha_base64))
    
img = Image.open("/Users/jarvis/pymycod/automation/test folder/captcha.jpg")
gray = img.convert('L')
gray.save('/Users/jarvis/pymycod/automation/test folder/captcha_gray.png')
captcha_solved= pytesseract.image_to_string(gray)
login = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]')))
login.click()
login.send_keys("nn4489")
pass1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passwd"]')))
pass1.click()
pass1.send_keys(keyring.get_password("srmsp","nn4489"))
cap= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ccode"]')))
cap.click()
cap.send_keys(captcha_solved[0:-1])
button1= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/button')))
button1.click()
personal_det= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="listId17"]')))
personal_det.click()
name = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="divMainDetails"]/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/div')))
print(name.text)




