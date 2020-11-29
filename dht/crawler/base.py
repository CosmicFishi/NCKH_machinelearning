from abc import ABC
from dht.helper import Helper
from selenium import webdriver
import uuid


class CrawlerBase(ABC):
    def __init__(self, url, driver_path="/Users/duonghuuthanh/geckodriver"):
        self.driver = webdriver.Firefox(executable_path=driver_path)
        self.driver.get(url)

    def execute(self, ):
        self.save_review()
        self.driver.quit()

    def save_file(self, content, folder="/Users/duonghuuthanh/PycharmProjects/machinelearingapp/dataset/reviews"):
        file_name = str(uuid.uuid4()) + ".txt"
        Helper.write_text_file(path_file_name="%s/%s" % (folder, file_name), content=content)

    def save_review(self):
        raise Exception("Don't support this method.")
