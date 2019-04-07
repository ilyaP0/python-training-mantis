from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import Helper_project
from fixture.james import JamesHelper
from fixture.signup import SignupHelper
from fixture.mail import MailHelper
class Application:


    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.wd.implicitly_wait(5)
        self.wd.maximize_window()
        self.session = SessionHelper(self)
        self.project = Helper_project(self)
        self.james = JamesHelper(self)
        self.mail = MailHelper(self)
        self.signup = SignupHelper(self)
        self.config = config
        self.base_Url = config['web']['baseUrl']

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False



    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_Url)


    def destroy(self):
        self.wd.quit()