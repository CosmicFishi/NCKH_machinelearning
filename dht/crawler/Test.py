import unittest
from selenium import webdriver

class GoogleTest(unittest.TestCase):
    def setUp(self):
        print("begin")
        self.driver = webdriver.Firefox(executable_path="/Users/duonghuuthanh/geckodriver")

    def test_title(self):
        print("test1")
        self.driver.get("https://www.google.com.vn/")
        self.assertEqual(self.driver.title, "Google")
        self.assertIsNotNone(self.driver.find_element_by_name("q"))

    def test_title2(self):
        print("test2")

    def tearDown(self):
        print("end")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()