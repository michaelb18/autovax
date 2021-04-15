
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time
import json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--patient_fill", help="autofill patient info",
                    action="store_true")
parser.add_argument("--book", help="automatically book the appointment without allowing the user to correct the form(risky).",
                    action="store_true")
parser.add_argument("--login", action="store_true")
parser.add_argument("--location", action="store_true")
parser.add_argument("--bday", action="store_true")
args = parser.parse_args()

from ctparse import ctparse
from datetime import datetime
from locator import load_location
from login_maker import gen_acct
ts = datetime.now()
if(args.patient_fill):
    first_name = input('What is your first name: ')
    last_name = input('What is your last name: ')
#bday = ctparse(input('What is your birthday?'), ts=ts, latent_time=False)
bday = None
if(args.bday):
    bday = input('What is your birthday(MMDDYYYY)?')
"""
if hasattr(bday.resolution, 'year'):
    bday = datetime(year = bday.resolution.year, month = bday.resolution.month, day = bday.resolution.day, minute = bday.resolution.minute, hour = bday.resolution.hour)
else:
    bday = input('I didnt understand that date. Can you enter it using MMDDYYYY format?')"""
appt_time = ctparse(input('Enter the time you want the appointment to be made: '), ts=ts)
appt_time = datetime(year = appt_time.resolution.year, month = appt_time.resolution.month, day = appt_time.resolution.day, minute = appt_time.resolution.minute, hour = appt_time.resolution.hour)

while(datetime.now() < appt_time):
    pass

driver = webdriver.Firefox()
driver.get("https://www.nrvroadtowellness.com/get-an-appointment-now")
elem = driver.find_element_by_link_text('Sign up for this clinic.')
elem.click()
time.sleep(1)
action = ActionChains(driver)
action.send_keys(Keys.PAGE_DOWN)
action.perform()
time.sleep(.5)
action = ActionChains(driver)


elem = driver.find_element_by_name('siid')
action.move_to_element_with_offset(elem, 1, 1)
action.click()
action.perform()
time.sleep(1)

action = ActionChains(driver)
elem = driver.find_element_by_id('submitfooter')
action.move_to_element_with_offset(elem, 633, 25)
action.click()
action.perform()
time.sleep(3)
from guerrillamail import GuerrillaMailSession

session = GuerrillaMailSession()
#elem.send_keys(session.get_session_state()['email_address'])
if(args.patient_fill):
    with open('patient_info.json') as f:
        info = json.load(f)
        if(args.location):
            info = load_location(info)
        if(bday is not None):
            if(isinstance(bday, str)):
                info['dob']=bday
            else:
                info['dob']=str(bday.month).zfill(2)+str(bday.day).zfill(2)+str(bday.year).zfill(4)
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ng-binding"))
    )
    elem = driver.find_element_by_xpath("//input[@aria-label='Date of Birth MMDDYYYY']").send_keys(info['dob'])
    driver.find_element_by_id("firstname").send_keys(first_name)
    driver.find_element_by_id("lastname").send_keys(last_name)
    driver.find_element_by_id("email").send_keys(session.get_session_state()['email_address'])
    #Select(driver.find_elements_by_xpath("//*[contains(text(), 'Virginia')]")[0]).select_by_visible_text(info["state"])
    
    elem = driver.find_element_by_id("state_zip")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 200, 18)
    action.click()
    action.perform()
    action = ActionChains(driver)
    action.send_keys(info['zipCode'])
    action.perform()
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 1, 1)
    action.click()
    action.perform()
    action = ActionChains(driver)
    action.send_keys('V'+Keys.RETURN)
    action.click()
    action.perform()
    driver.find_element_by_id("phone_id").send_keys(info['phone']) 
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, -1, -1)
    action.click()
    action.perform()
    action = ActionChains(driver)
    action.send_keys(Keys.PAGE_DOWN)
    action.perform()
    time.sleep(.5)
    elem = driver.find_element_by_id("3127149_id")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 1, 1)
    action.click()
    action.perform()
    action = ActionChains(driver)

    if(info['gender'] == 'male'):
        action.send_keys('M'+Keys.RETURN)
        action.perform()    
    elif(info['gender'] == 'female'):
        action.send_keys('F'+Keys.RETURN)
        action.perform()   
        #Select(driver.find_element_by_id("3127149_id")).select_by_visible_text("F")
    else:
        action.send_keys('O'+Keys.RETURN)
        action.perform()   
        #Select(driver.find_element_by_id("3127149_id")).select_by_visible_text("Others")
    elem = driver.find_element_by_id("3285799_id")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 1, 1)
    action.click()
    action.perform()
    action = ActionChains(driver)
    action.send_keys(info['race']+Keys.RETURN)
    action.perform()
if(args.book):
    elem = driver.find_element_by_link_text('Sign Up Now')
    elem.click()
    #Select(driver.find_element_by_id("3285799_id")).select_by_visible_text(info['race'])
time.sleep(20000)
driver.close()

