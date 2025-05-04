from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# List of credentials for 6 people
users = [
    {"id": "user1@au.edu", "password": "password1"},
    {"id": "user2@au.edu", "password": "password2"},
    {"id": "user3@au.edu", "password": "password3"},
    {"id": "user4@au.edu", "password": "password4"},
    {"id": "user5@au.edu", "password": "password5"},
    {"id": "user6@au.edu", "password": "password6"}
]

# Function to process one user
def process_user(user_id, user_password):
    print(f"Processing user: {user_id}")
    
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    # Add these options to make Chrome faster
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-gpu")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=option)
    
    # Set implicit wait to reduce code verbosity
    driver.implicitly_wait(1)  # Short implicit wait
    
    try:
        driver.get("https://auspark.au.edu/")
        
        # Use explicit waits for critical elements
        login_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/form/div/button'))
        )
        login_button.click()
        
        input_id = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]'))
        )
        input_id.send_keys(user_id + Keys.ENTER)
        
        input_pass = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input'))
        )
        input_pass.send_keys(user_password + Keys.ENTER)
        
        # Handle "No" button with minimal wait
        try:
            no_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input'))
            )
            no_button.click()
        except:
            pass  # Skip silently if no button isn't found
        
        # Try to click planner with optimized approach
        for selector in [
            (By.CSS_SELECTOR, 'a[href="/Planner"]'),
            (By.LINK_TEXT, "Planner"),
            (By.PARTIAL_LINK_TEXT, "Plan")
        ]:
            try:
                planner = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(selector)
                )
                planner.click()
                break  # Exit the loop if successful
            except:
                continue  # Try next selector if this one fails
        
        # Add your planner page actions here
        
        return True
        
    except Exception as e:
        print(f"Error processing user {user_id}: {e}")
        driver.save_screenshot(f"error_{user_id.split('@')[0]}.png")
        return False
    finally:
        driver.quit()  # Close the browser

# Process each user
for user in users:
    success = process_user(user["id"], user["password"])
    print(f"User {user['id']} processed {'successfully' if success else 'with errors'}")

print("All users processed")
