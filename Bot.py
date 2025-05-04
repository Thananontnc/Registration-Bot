from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)

Id = "YOUR_EMAIL"
Pass = "$YOUR_PASSWORD"

driver.get("https://auspark.au.edu/")
login = driver.find_element(By.XPATH, '/html/body/div/div/div/form/div/button').click()
time.sleep(2)
input_id = driver.find_element(By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]')
input_id.send_keys(Id + Keys.ENTER)
time.sleep(2)
input_pass = driver.find_element(By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input')
input_pass.send_keys(Pass + Keys.ENTER)

# Add explicit wait for the "No" button
try:
    # Wait up to 10 seconds for the element to be present
    no_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input'))
    )
    no_button.click()
except:
    # If the button doesn't appear, just continue
    print("No button not found or not needed, continuing...")

# Wait for the page to fully load after login
print("Waiting for page to load...")
time.sleep(5)

# Try multiple approaches to find and click the planner button
try:
    # First try using a more reliable CSS selector based on the HTML you provided
    print("Trying to find planner link...")
    planner = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/Planner"]'))
    )
    print("Found planner link, clicking...")
    planner.click()
    print("Clicked planner link successfully")
except Exception as e:
    print(f"First attempt failed: {e}")
    try:
        # Try by link text
        planner = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Planner"))
        )
        planner.click()
        print("Clicked planner using link text")
    except Exception as e:
        print(f"Second attempt failed: {e}")
        try:
            # Try by partial link text
            planner = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Plan"))
            )
            planner.click()
            print("Clicked planner using partial link text")
        except Exception as e:
            print(f"All attempts to click planner failed: {e}")
            # Take a screenshot to help debug
            driver.save_screenshot("error_screenshot.png")
            print("Screenshot saved as error_screenshot.png")
