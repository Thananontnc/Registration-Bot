from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)

Id = "u6711424@au.edu"
Pass = "Plai$1412"

driver.get("https://auspark.au.edu/")
login = driver.find_element(By.XPATH, '/html/body/div/div/div/form/div/button').click()
time.sleep(2)
input_id = driver.find_element(By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]')
input_id.send_keys(Id + Keys.ENTER)
time.sleep(2)
input_pass = driver.find_element(By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input')
input_pass.send_keys(Pass + Keys.ENTER)
no = driver.find_element(By.XPATH, '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input').click()
planner = driver.find_element(By.XPATH, '/html/body/div[2]/nav/ul/li[3]/ul[6]/li[1]/a').click()