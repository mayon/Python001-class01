from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    browser.get('https://shimo.im/login?from=home')

    browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input').send_keys('13545454545')
    browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input').send_keys('12345678')
    time.sleep(2)
    browser.find_element_by_xpath('//button[contains(@class, "submit")]').click();
    
    cookies = browser.get_cookies()
    print(cookies)
except Exception as e:
    print(e)
finally:
    browser.close()

