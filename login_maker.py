from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from guerrillamail import GuerrillaMailSession
import time
"""session = GuerrillaMailSession()
print(session.get_session_state()['email_address'])
print(session.get_email_list()[0].guid)

first_name = input('What is your first name: ')
print()
last_name = input('What is your last name: ')
print()

driver = webdriver.Firefox()
driver.get("https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid&r=yes")"""

def gen_acct(driver, first_name, last_name):
    session = GuerrillaMailSession()
    try:
        elem = driver.find_element_by_id("password")
        #i = 0
        #while(True):
        #    i = i + 1
        action = ActionChains(driver)
        action.send_keys(Keys.TAB * 7)
        #print(i)
        action.perform()
        action = ActionChains(driver)
        action.send_keys(Keys.RETURN)
        action.perform()
    except:
        elem = driver.find_element_by_id("email")
        action = ActionChains(driver)
        action.send_keys(Keys.TAB * 2)
        action.perform()
        action = ActionChains(driver)
        action.send_keys(Keys.RETURN)
        action.perform()
    elem = driver.find_element_by_id("first-name-su")
    elem.send_keys(first_name)
    elem = driver.find_element_by_id("last-name-su")
    elem.send_keys(last_name)
    elem = driver.find_element_by_id("email-su")
    elem.send_keys(session.get_session_state()['email_address'])
    import string
    password = string.ascii_letters + string.digits + string.punctuation
    elem = driver.find_element_by_id("password-su")
    elem.send_keys(password)
    action = ActionChains(driver)
    action.send_keys(Keys.TAB * 7)
    #print(i)
    action.perform()
    action = ActionChains(driver)
    action.send_keys(Keys.RETURN)
    action.perform()