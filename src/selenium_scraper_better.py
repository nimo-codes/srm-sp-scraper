from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import base64
import pytesseract
from PIL import Image 
from time import sleep as tt
import keyring
import logging 

options = Options()
options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(chrome_options=options, executable_path="/Users/jarvis/pymycod/automation/chromedriver")
driver.get("https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp")
wait = WebDriverWait(driver,10)

logging.basicConfig(filename="/Users/jarvis/pymycod/automation/test folder/logs.log",format="%(message)s, %(asctime)s  ", filemode="a",datefmt="%d/%m/%Y %I:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def err(reason,num):
  place = {0:"captcha can't be located",1:"pytesseract gave error",2:"login and password can't be located or have some issues in clicking or sending credentials",
           3:"invalid captcha:- prolly due to pressing submit before filling",4:"can't get personal details"}
  print(f"error encountered- {num}")
  message = f'''following block is the possible reason for the raised exception {num},
  reason - {place[num]}, 
  exception raised - {reason}'''
  inter_msg = message.split(",")
  final_message = f'''{inter_msg[0]},
  {inter_msg[1]},
  {inter_msg[2].split("Stacktrace:")[0]}'''
  logger.error(final_message)
  


try: 
  captchaaa = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/div[4]/div[2]/img')))
except Exception as error0:
  err(error0,0)

captcha_solved = 0
try:
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
  tt(1)
except Exception as error1:
  err(error1,1)
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
  tt(2)
  
try: 
  login = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]')))
  login.click()
  login.send_keys("nn4489")
  pass1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passwd"]')))
  pass1.click()
  pass1.send_keys(keyring.get_password("srmsp","nn4489"))
except Exception as error2:
  err(error2,2)

try:
  cap= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ccode"]')))
  cap.click()
  cap.send_keys(captcha_solved[0:-1])
  button1= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/button')))
  button1.click()
except Exception as error3:
  err(error3,3)

try:
  personal_det= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="listId17"]')))
  personal_det.click()
  name = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="divMainDetails"]/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/div')))
  print(name.text)
except Exception as error4:
  err(error4,4)










