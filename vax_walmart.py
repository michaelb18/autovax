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
args = parser.parse_args()

from ctparse import ctparse
from datetime import datetime
ts = datetime.now()
if(args.login):
    first_name = input('What is your first name: ')
    last_name = input('What is your last name: ')
appt_time = ctparse(input('Enter the time you want the appointment to be made: '), ts=ts)
appt_time = datetime(year = appt_time.resolution.year, month = appt_time.resolution.month, day = appt_time.resolution.day, minute = appt_time.resolution.minute, hour = appt_time.resolution.hour)
while(datetime.now() < appt_time):
    pass
driver = webdriver.Firefox()
driver.get("https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid&r=yes")
if(not args.login):
    try:
        
        #assert "Python" in driver.title
        with open('login.json') as f:
            login = json.load(f)

        elem = driver.find_element_by_name("email")
        elem.clear()
        elem.send_keys(login["email"])

        elem = driver.find_element_by_name("password")
        elem.clear()
        elem.send_keys(login["password"])
        elem.send_keys(Keys.RETURN)
    except:
        with open('login.json') as f:
            login = json.load(f)

        elem = driver.find_element_by_name("email")
        elem.clear()
        elem.send_keys(login["email"])
        elem.send_keys(Keys.RETURN)
        time.sleep(10)

        elem = driver.find_element_by_name("password")
        action = ActionChains(driver)
        action.move_to_element_with_offset(elem, 160, 27)
        action.click()
        action = ActionChains(driver)
        action.send_keys(login["password"])
        action.perform()
        action = ActionChains(driver)
        action.send_keys(Keys.RETURN)
        action.perform()
else:
    from login_maker import gen_acct
    gen_acct(driver, first_name, last_name)
#elem = driver.find_element_by_id("signin-submit-btn")
#elem.click()
ignored_exceptions = (StaleElementReferenceException,)
elem = WebDriverWait(driver, 30, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.CLASS_NAME, "style__pageTitleSection___2eEQw"))
    )
action = ActionChains(driver)
#elem = driver.find_element_by_name("q")
#for i in range(12):
time.sleep(15)
action.move_to_element(elem)
action.click()
action.perform()
action = ActionChains(driver)
action.send_keys(Keys.TAB * 12)
action.send_keys(Keys.RETURN)
action.perform()
elem = WebDriverWait(driver, 30, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.CLASS_NAME, "option-marker"))
    )
action = ActionChains(driver)
#elem = driver.find_element_by_name("q")
#for i in range(12):
time.sleep(.25)
action.move_to_element(elem)
action.click()
action.perform()
#action.send_keys(Keys.TAB * 4)
#action.perform()
action = ActionChains(driver)
action.send_keys(Keys.PAGE_DOWN)
action.perform()
time.sleep(1)

action = ActionChains(driver)
elem = driver.find_element_by_class_name("index__submitBtnSectionCta___3Tu2L")
action.move_to_element_with_offset(elem, 950, 30)
action.click()
action.perform()
action = ActionChains(driver)
"""i = 0
while(True):
    action.send_keys(Keys.TAB)
    action.perform()
    i = i + 1
    print('sent tab'+str(i))"""
time.sleep(.25)
#action.send_keys(Keys.TAB * 13)

"""action.send_keys(Keys.RETURN)
action.perform()"""
action = ActionChains(driver)

time.sleep(.22)
elem = driver.find_element_by_class_name("index__submitBtnSectionCta___3Tu2L")
action.move_to_element_with_offset(elem, 950, 30)
action.click()
action.perform()
action = ActionChains(driver)
time.sleep(5)
elem = driver.find_element_by_class_name("validation-group")
action.move_to_element_with_offset(elem, 0, 0)
action.click()
action.perform()
action = ActionChains(driver)
action.send_keys(Keys.PAGE_DOWN)
action.perform()
time.sleep(1)

action = ActionChains(driver)
elem = driver.find_element_by_class_name("index__submit__btn__section___27owc")
action.move_to_element_with_offset(elem, 950, 20)
action.click()
action.perform()
action = ActionChains(driver)
time.sleep(2)
elem = driver.find_element_by_class_name("index__center-align___28mBP")
action.move_to_element_with_offset(elem, 491, 48)
action.click()
action.perform()
action = ActionChains(driver)
time.sleep(.1)
from selenium.common.exceptions import WebDriverException

if(args.patient_fill):
    with open('patient_info.json') as f:
        info = json.load(f)
    elem = driver.find_element_by_id("patient.bio.dob")
    elem.send_keys(info["dob"])
    gender = info["gender"]

    
    action = ActionChains(driver)
    elem = driver.find_element_by_id("patient-gender-"+gender)
    action.move_to_element_with_offset(elem, 1, 1)
    action.click()
    action.perform()

    select = Select(driver.find_element_by_id("patient.demography.race"))
    select.select_by_visible_text(info["race"])

    select = Select(driver.find_element_by_id("patient.demography.ethnicity"))
    select.select_by_visible_text(info["ethnicity"])
    
    driver.find_element_by_id("patient.address.homeAddress").send_keys(info["homeAddress"])
    driver.find_element_by_id("patient.address.city").send_keys(info["city"])
    Select(driver.find_element_by_id("patient.address.state")).select_by_visible_text(info["state"])
    driver.find_element_by_id("patient.address.zipCode").send_keys(info["zipCode"])
    driver.find_element_by_id("patient.address.phoneNumber").send_keys(info["phone"])

    time.sleep(.25)
    driver.execute_script("window.scrollTo(0, 1000)") 
    time.sleep(.25)
    elem = driver.find_element_by_id("patient-has-primary-physician-"+info["physician"])

    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 1, 1)
    action.click()
    action.perform()
    
    elem = driver.find_element_by_class_name("index__submitBtnSection___3d0g5")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 925, 20)
    action.click()
    action.perform()
    ans = ["allergic", "sick", "health_conditions", "reaction", "seizure", "pregnant", "immunocompromised", "vaccines", "medication", "treatment"]
    cats = ["compounds", "sicknesses", "conditions"]
    cat_idx = 0
    for i in range(10):
        time.sleep(1)
        elem = driver.find_element_by_class_name("style__multiple-buttons___bTlCz")
        action = ActionChains(driver)
        if(info[ans[i]] == "No"):
            action.move_to_element_with_offset(elem, 324, 20)
            action.click()
            action.perform()
        else:
            action.move_to_element_with_offset(elem, 108, 20)
            action.click()
            action.perform()
            action = ActionChains(driver)
            for c in info[cats[cat_idx]]:
                elem = driver.find_element_by_id(c)
                action.move_to_element_with_offset(elem, 5, 5)
                action.click()
                action.perform()
                action = ActionChains(driver)
            elem = driver.find_element_by_class_name("style__single-button___1WLOy")
            action.move_to_element_with_offset(elem, 216, 48)
            action.click()
            action.perform()
            cat_idx = cat_idx + 1
    elem = driver.find_element_by_id("ACCEPT")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 5, 5)
    action.click()
    action.perform()
    elem = driver.find_element_by_class_name("style__consent-action___30fkm")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 190, 100)
    action.click()
    action.perform()

    elem = driver.find_element_by_id("ACCEPT")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 5, 5)
    action.click()
    action.perform()
    elem = driver.find_element_by_class_name("style__consent-action___30fkm")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 190, 100)
    action.click()
    action.perform()

    elem = driver.find_element_by_id("ACCEPT")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 5, 5)
    action.click()
    action.perform()
    elem = driver.find_element_by_class_name("style__consent-action___30fkm")
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 190, 120)
    action.click()
    action.perform()
    if(args.book):
        elem = driver.find_element_by_class_name("index__right-align___31g_-")
        action = ActionChains(driver)
        action.move_to_element_with_offset(elem, 1000, 48)
        action.click()
        action.perform()
else:
    try:
        driver.execute_script("alert('Hey, there, its the guy who made your vaccine appointment. This patient information page is as far as I can take you without comprimising your privacy. It works just like the form you fill out before the doctor sees you, but digital. To fill out the form, click on each box and type in the correct information. After all the information is filled in, click on the blue button that says \"Continue\" at the bottom of the form. Walmart will ask you more questions after this. Answer those, and then acknowledge a couple forms, all the same way as this first page. After you are done, it brings you to a page that lets you book your appointment.');")
    except WebDriverException:
        pass


"""i = 0
while(True):
    action.send_keys(Keys.TAB)
    action.perform()
    i = i + 1
    print('sent tab'+str(i))
    time.sleep(3)
action.send_keys(Keys.TAB * 2)
action.send_keys(Keys.RETURN)"""
action = None
"""
time.sleep(1)
i = 0
while(True):
    action.send_keys(Keys.TAB)
    action.perform()
    i = i + 1
    print('sent tab'+str(i))
    time.sleep(3)
"""
#action = ActionsChains(driver)
#assert "No results found." not in driver.page_source
time.sleep(20000)
driver.close()