from selenium import webdriver
from fake_useragent import UserAgent


class ChromeDriverWithOptions(object):

    def __init__(self):
        try:
            self.useragent = UserAgent()
            self.options = webdriver.ChromeOptions()
            # Меняем user-agent
            self.options.add_argument(f"user-agent={self.useragent.chrome}")
            # Убираем WebDriver
            self.options.add_argument("--disable-blink-features=AutomationControlled")
            # Оставляем браузер в фоновом режиме
            self.options.headless = True
            self.driver = webdriver.Chrome(
                executable_path="/Users/nikitaisutov/PycharmProjects/parsers/Scrap_upwork/driver/chromedriver",
                options=self.options)
            self.driver.set_window_size(480, 1080)
        except Exception as ex:
            print(ex)

    def get_from_url(self, url):
        try:
            self.driver.get(url=url)
        except Exception as ex:
            print(ex)

    def close(self):
        self.driver.close()
        self.driver.quit()