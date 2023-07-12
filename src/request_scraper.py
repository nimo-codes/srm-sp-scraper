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
import keyring
options = Options()
# options.add_argument("--headless")
# options.add_argument("--start-maximized")

driver = webdriver.Chrome(chrome_options=options, executable_path="/Users/jarvis/pymycod/automation/chromedriver")

driver.get("https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp")
wait = WebDriverWait(driver,10)
element1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/div[4]/div[2]/img')))
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
        """, element1)
with open(r"/Users/jarvis/pymycod/automation/test folder/captcha.jpg", 'wb') as f:
    f.write(base64.b64decode(img_captcha_base64))
    
img = Image.open("/Users/jarvis/pymycod/automation/test folder/captcha.jpg")
gray = img.convert('L')
gray.save('/Users/jarvis/pymycod/automation/test folder/captcha_gray.png')
captcha_solved= pytesseract.image_to_string(gray)



URL = "https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp"
payload = {
    "login":"",
"passwd": "", 
"ccode" :"", 
"txtPageAction": 1,
"txtSK": "nn4489",
"txtAN": f"{keyring.get_password('srmsp','nn4489')}",
"hdnCaptcha": f"{captcha_solved[0:-1]}",
"_tries": 1,
"_md5": ""
}
with session() as c:
    r = c.get(URL)
    changing_date= r.headers["Date"]
    changing_cookies = r.headers["Set-Cookie"]
    def_headers = {'Date': f'{changing_date}', 'Server': 'Apache/2.4.41 (Ubuntu)', 'Set-Cookie': f'{changing_cookies}; Path=/srmiststudentportal; HttpOnly', 'Vary': 'Accept-Encoding', 'Content-Encoding': 'gzip', 'Content-Length': '2915', 'Keep-Alive': 'timeout=5, max=100', 'Connection': 'Keep-Alive', 'Content-Type': 'text/html;charset=UTF-8'}
    resp = c.post(URL,data=payload,headers=def_headers)
    print(resp.text)
    
    # resp = c.get("https://sp.srmist.edu.in/srmiststudentportal/students/template/HRDSystem.jsp#!")
    # r2 =c.post("https://sp.srmist.edu.in/srmiststudentportal/students/report/studentPersonalDetails.jsp",headers=def_headers,data={"iden":17,"filter": ""})   
    # print(r2.text)
    




# # time_stamp = datetime.now()
# # # time_stamp.day
# # week_day_dict = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}
# # print(week_day_dict[time_stamp.weekday()])
# # date_format
