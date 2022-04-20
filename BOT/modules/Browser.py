# Load installer class
from . import Installer

try:
    # Import Selenium if installed
    from selenium import webdriver
except ModuleNotFoundError:
    # If not installed, install it
    Installer('selenium', True).install()

try:
    from fake_useragent import UserAgent
except ModuleNotFoundError:
    # If not installed, install it
    Installer('fake_useragent').install()

# Selenium useful modules
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# Fake the User Agent
from fake_useragent import UserAgent

# Simplified class to perform scrapping
class Browser:

    def __init__(self, PATH_TO_DRIVER = ''):
        if not isinstance(PATH_TO_DRIVER, str) or PATH_TO_DRIVER == '':
            print("Path to drive must be a not empty string")
            sys.exit()
        else:
            # Path to the Chrome driver
            self.PATH_TO_DRIVER = PATH_TO_DRIVER

            # Set the options to avoid detection
            self.options = self.set_options()

            # Create the driver instance
            self.driver = webdriver.Chrome(executable_path = PATH_TO_DRIVER, options = self.options)

            # Avoid detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                                                                                    "source":
                                                                                    "const newProto = navigator.__proto__;"
                                                                                    "delete newProto.webdriver;"
                                                                                    "navigator.__proto__ = newProto;"
                                                                                }
                                        )

            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent" : self.user_agent})
        return

    def set_options(self):
        # Set a random user agent in order to avoid captcha
        self.user_agent = UserAgent().random

        # Instantiate a options object of Chrome
        opt = webdriver.ChromeOptions()
        
        # Set some options in order to avoid bot detection
        opt.add_argument('--start-maximized')
        #opt.add_argument('--single-process')
        opt.add_argument('--incognito')
        opt.add_argument('--disable-gpu')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-blink-features')
        opt.add_argument('--disable-blink-features=AutomationControlled') 
        opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument('--disable-impl-side-painting')
        opt.add_argument('--disable-setuid-sandbox')
        opt.add_argument('--disable-seccomp-filter-sandbox')
        opt.add_argument('--disable-breakpad')
        opt.add_argument('--disable-client-side-phishing-detection')
        opt.add_argument('--disable-cast')
        opt.add_argument('--disable-cast-streaming-hw-encoding')
        opt.add_argument('--disable-cloud-import')
        opt.add_argument('--disable-popup-blocking')
        opt.add_argument('--ignore-certificate-errors')
        opt.add_argument('--disable-session-crashed-bubble')
        opt.add_argument('--disable-ipv6')
        opt.add_argument('--allow-http-screen-capture')
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        opt.add_argument('--disable-infobars')
        opt.add_argument('--user-agent={}'.format(self.user_agent))
        
        return opt

    def get_url(self, url = ''):
        self.url = url
        if not isinstance(self.url, str) or self.url == '':
            print("Path to drive must be a not empty string")
            sys.exit()

        self.driver.get(url = self.url)
        return
    
    def find_and_click(self, by = '', value = '', click = False):
        
        if not isinstance(by, str) or by == '':
            print("By must be a not empty string")
            sys.exit()

        if not isinstance(value, str) or value == '':
            print("Value must be a not empty string")
            sys.exit()
        
        if by.lower() == 'id':
            self.driver.find_element(by = By.ID, value = value).click()
        elif by.lower() == 'link_text':
            self.driver.find_element(by = By.LINK_TEXT, value = value).click()
        elif by.lower() == 'xpath':
            self.driver.find_element(by = By.XPATH, value = value).click()
        
        return

    def find_complete_submit(self, by = '', value = '', keys = '', submit = False):
        
        if not isinstance(by, str) or by == '':
            print("By must be a not empty string")
            sys.exit()

        if not isinstance(value, str) or value == '':
            print("Value must be a not empty string")
            sys.exit()

        if not isinstance(keys, (str, list)) or keys == '':
            print("Keys must be a not empty string")
            sys.exit()
        
        if by.lower() == 'id':
            if  isinstance(keys, str):
                element = self.driver.find_element(by = By.ID, value = value).send_keys(keys)
                if submit == True:
                    element.submit()
                    return
                elif submit == False:
                    return
            elif isinstance(keys, list):
                element = self.driver.find_element(by = By.ID, value = value)
                element.send_keys(keys[0])
                if keys[1].lower() == 'return':
                    element.send_keys(Keys.RETURN)

                if submit == True:
                    element.submit()
                    return
                elif submit == False:
                    return
        return