from dht.crawler.base import CrawlerBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TGDDCrawler(CrawlerBase):
    def __init__(self):
        super().__init__("https://www.thegioididong.com/laptop")

        while len(self.driver.find_elements_by_css_selector(".viewmore")) > 0:
            self.driver.find_element_by_css_selector(".viewmore").click()

        self.urls = [u.get_attribute("href") for u in self.driver.find_elements_by_css_selector(".homeproduct  a")]

    def save_review(self):
        for u in self.urls:
            self.driver.get(u)
            try:
                self.driver.find_element_by_css_selector("#boxRatingCmt .rtpLnk").click()
            except Exception as ex:
                print(str(ex))
            else:
                reviews = WebDriverWait(self.driver, 10).until(
                    ec.presence_of_all_elements_located((By.CSS_SELECTOR, ".ratingLst .rc i"))
                )
                for review in reviews:
                    if len(review.text) > 10:
                        print("=== ", review.text)
                        self.save_file(content=review.text)


if __name__ == "__main__":
    TGDDCrawler().execute()
