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

###########################################  Chrome Options  #################################################################################
options = Options()
# options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")


###########################################  Setting of webdriver  #################################################################################
driver = webdriver.Chrome(chrome_options=options, executable_path="/Users/jarvis/pymycod/automation/chromedriver")
driver.get("https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp")
wait = WebDriverWait(driver,10)


###########################################  Setting logger  #################################################################################
logging.basicConfig(filename="/Users/jarvis/pymycod/automation/test folder/logs.log",format="%(message)s, %(asctime)s  ", filemode="a",datefmt="%d/%m/%Y %I:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.ERROR)



###########################################  Functions  #################################################################################
def convert(captcha_loc):
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
          """, captcha_loc)
  with open(r"/Users/jarvis/pymycod/automation/test folder/captcha.jpg", 'wb') as f:
      f.write(base64.b64decode(img_captcha_base64))
      
  img = Image.open("/Users/jarvis/pymycod/automation/test folder/captcha.jpg")
  gray = img.convert('L')
  gray.save('/Users/jarvis/pymycod/automation/test folder/captcha_gray.png')
  captcha_solved= pytesseract.image_to_string(gray)
  tt(1)
  return captcha_solved[0:-1]
  
def login(captcha_loc):
  login = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login"]')))
  login.click()
  login.send_keys("nn4489")
  pass1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passwd"]')))
  pass1.click()
  pass1.send_keys(keyring.get_password("srmsp","nn4489"))
  cap= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ccode"]')))
  cap.click()
  cap.send_keys(convert(captcha_loc))
  button1= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/button')))
  button1.click()
  
def err(reason,num):
  place = {0:"captcha can't be located",1:"pytesseract gave error",2:"work being handled"}
  print(f"error encountered- {num}")
  message = f'''following block is the possible reason for the raised exception {num},
  reason - {place[num]}, 
  exception raised - {reason}'''
  inter_msg = message.split(",")
  final_message = f'''{inter_msg[0]},
  {inter_msg[1]},
  {inter_msg[2].split("Stacktrace:")[0]}'''
  logger.error(final_message)
  


###########################################  Start of code  #################################################################################
try: 
  captchaaa = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/div[4]/div[2]/img')))
except Exception as error0:
  err(error0,0)

flag = False
while flag==False:
  try:
    login(captchaaa)
    try:
      grades= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="listId24"]')))
      flag=True
    except:
      flag=False
  except Exception as error1:
    err(error1,1)
  
if flag==True:
  try:
    grades= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="listId24"]')))
    print(grades)
    # grades.click()
    # # while: 
    # name = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="divMainDetails"]/div/div/div/div/div[2]/div[2]/table')))
    # name = driver.find_elements((By.XPATH,'//*[@id="divMainDetails"]/div/div/div/div/div[2]/div[2]/table'))
    # # print(name)
  except Exception as error2:
    err(error2,2)

  










