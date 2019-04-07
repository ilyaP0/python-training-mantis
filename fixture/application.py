from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import Helper_project


class Application:


    def __init__(self, browser, base_Url):
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
        self.base_Url = base_Url

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