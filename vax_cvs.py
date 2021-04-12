from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time
import json
def perform_action(action, driver):
    action.perform()
    return ActionChains(driver)
driver = webdriver.Firefox()
driver.get("https://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns")
"""time.sleep(1)
#Click No for testing positive in the last 14 days
elem = driver.find_element_by_id("q7_2")
action = ActionChains(driver)
action.move_to_element_with_offset(elem, 7, 7)
action.click()
action = perform_action(action, driver)

#Click no for having been in close contact inthe last 14 days
elem = driver.find_element_by_id("q8_2")
action.move_to_element_with_offset(elem, 7, 7)
action.click()
action = perform_action(action, driver)

#Click no for are you sick
elem = driver.find_element_by_id("q9_2")
action.move_to_element_with_offset(elem, 7, 7)
action.click()
action = perform_action(action, driver)

#Click continue
elem = driver.find_element_by_class_name("btn-control")
action.move_to_element_with_offset(elem, 10, 10)
action.click()
action = perform_action(action, driver)"""
time.sleep(20000)
driver.close()