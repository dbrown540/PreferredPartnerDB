import selenium
from selenium import webdriver

print("Selenium Version: ", selenium.__version__)
version = webdriver.ChromeVersion().version

print(version)