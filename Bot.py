from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import concurrent.futures
import os

# Create a directory for screenshots if it doesn't exist
os.makedirs("screenshots", exist_ok=True)
os.makedirs("screenshots/success", exist_ok=True)
os.makedirs("screenshots/errors", exist_ok=True)

# List of credentials for 6 people
users = [
    {"id": "u6711424@au.edu", "password": ""},
    {"id": "u6710990@au.edu", "password": ""},
    # Add more users here
]

def handle_sweet_alert(driver):
    """Handle SweetAlert popups that might appear on the page"""
    try:
        # Check if a SweetAlert is present (wait up to 3 seconds)
        alert = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "swal-modal"))
        )
        
        # Get the alert text
        alert_text = driver.find_element(By.CLASS_NAME, "swal-text").text
        print(f"SweetAlert detected: {alert_text}")
        
        # Check if it's an error alert
        is_error = len(driver.find_elements(By.CLASS_NAME, "swal-icon--error")) > 0
        
        # Click the appropriate button (usually "OK" or "Confirm")
        buttons = driver.find_elements(By.CLASS_NAME, "swal-button")
        if buttons:
            # Usually the last button is the primary action
            buttons[-1].click()
            print("Alert confirmed")
        
        return True, alert_text, is_error
    except:
        return False, "", False  # No alert found

def navigate_to_planner(driver):
    """Navigate to the Planner page"""
    print("Attempting to navigate to Planner page...")
    
    # Try direct navigation first (fastest method)
    try:
        driver.get("https://auspark.au.edu/Planner")
        print("Direct navigation to Planner page")
        return True
    except:
        print("Direct navigation failed, trying to click links...")
    
    # Try clicking links with shorter timeouts
    for selector in [
        (By.CSS_SELECTOR, 'a[href="/Planner"]'),
        (By.LINK_TEXT, "Planner"),
        (By.PARTIAL_LINK_TEXT, "Plan")
    ]:
        try:
            planner = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(selector)
            )
            planner.click()
            print("Successfully clicked Planner link")
            return True
        except:
            continue  # Try next selector if this one fails
    
    print("Failed to navigate to Planner page")
    return False

def create_new_plan(driver):
    """Create a new plan if none exists"""
    try:
        # Check if "Plan Not Found" message is present
        plan_not_found = driver.find_elements(By.XPATH, "//p[contains(text(), 'Plan Not Found')]")
        
        if plan_not_found:
            print("No plans found, creating a new one...")
            
            # Click the "+" button to create a new plan
            new_plan_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-new-plan"))
            )
            new_plan_button.click()
            print("Clicked new plan button")
            
            # Wait for the new plan page to load
            WebDriverWait(driver, 10).until(
                EC.url_contains("/Planner/NewPlan")
            )
            
            # Take a screenshot of the new plan page
            driver.save_screenshot(f"screenshots/success/new_plan_page.png")
            print("New plan page loaded")
            
            # The system might automatically create a plan with a default name
            # Wait for any redirects or alerts
            time.sleep(2)
            handle_sweet_alert(driver)
            
            return True
        else:
            print("Plans already exist")
            return True
    except Exception as e:
        print(f"Error creating new plan: {e}")
        return False

def wait_for_registration_button(driver):
    """Check if registration button appears and click it if found"""
    try:
        # Look for buttons that might be related to registration
        potential_buttons = [
            (By.XPATH, "//button[contains(text(), 'Register')]"),
            (By.XPATH, "//a[contains(text(), 'Register')]"),
            (By.XPATH, "//button[contains(text(), 'Submit')]"),
            (By.XPATH, "//button[contains(@class, 'btn-primary')]"),
            (By.CSS_SELECTOR, ".box-container_body button"),
            (By.CSS_SELECTOR, "#planSectionContent button")
        ]
        
        for selector in potential_buttons:
            buttons = driver.find_elements(*selector)
            for button in buttons:
                if button.is_displayed() and button.is_enabled():
                    button_text = button.text.strip()
                    print(f"Found potential registration button: '{button_text}'")
                    driver.save_screenshot(f"screenshots/success/found_button_{button_text.replace(' ', '_')}.png")
                    
                    # Highlight the button for screenshot
                    driver.execute_script("arguments[0].style.border='3px solid red'", button)
                    driver.save_screenshot(f"screenshots/success/highlighted_button_{button_text.replace(' ', '_')}.png")
                    driver.execute_script("arguments[0].style.border=''", button)
                    
                    # Don't click yet, just identify
                    return True
        
        print("No registration buttons found yet")
        return False
    except Exception as e:
        print(f"Error checking for registration buttons: {e}")
        return False

def process_user(user):
    user_id = user["id"]
    user_password = user["password"]
    print(f"Processing user: {user_id}")
    
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", False)
    # Add these options to make Chrome faster
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-gpu")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--no-sandbox")
    # Add these options to make page loading faster
    option.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
    option.page_load_strategy = 'eager'  # Don't wait for all resources
    
    # Don't use headless for exploration so we can see the UI
    # option.add_argument("--headless")
    
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
        
        # Take screenshot after successful login
        driver.save_screenshot(f"screenshots/success/login_{user_id.split('@')[0]}.png")
        print(f"Login successful for {user_id} - screenshot saved")
        
        # Handle "No" button with minimal wait
        try:
            no_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input'))
            )
            no_button.click()
        except:
            pass  # Skip silently if no button isn't found
        
        # Navigate to the planner page
        if not navigate_to_planner(driver):
            print(f"Could not navigate to planner page for {user_id}")
            driver.save_screenshot(f"screenshots/errors/navigation_failed_{user_id.split('@')[0]}.png")
            return False
        
        # Take screenshot after successful navigation to planner
        driver.save_screenshot(f"screenshots/success/planner_page_{user_id.split('@')[0]}.png")
        print(f"Navigation to planner successful for {user_id} - screenshot saved")
        
        # Create a new plan if needed
        create_new_plan(driver)
        
        # Check for any SweetAlert popups
        alert_present, alert_text, is_error = handle_sweet_alert(driver)
        if alert_present:
            print(f"Alert handled for {user_id}: {alert_text}")
            if is_error:
                driver.save_screenshot(f"screenshots/errors/alert_error_{user_id.split('@')[0]}.png")
            else:
                driver.save_screenshot(f"screenshots/success/alert_handled_{user_id.split('@')[0]}.png")
        
        # Look for registration buttons
        wait_for_registration_button(driver)
        
        # Take a final screenshot
        driver.save_screenshot(f"screenshots/success/final_state_{user_id.split('@')[0]}.png")
        print(f"Final screenshot taken for {user_id}")
        
        # Wait a bit before closing
        time.sleep(3)
        
        return True
        
    except Exception as e:
        print(f"Error processing user {user_id}: {e}")
        driver.save_screenshot(f"screenshots/errors/error_{user_id.split('@')[0]}.png")
        return False
    finally:
        driver.quit()  # Close the browser

# Main function to run the parallel processing
def main():
    start_time = time.time()
    
    # Process users in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        # Submit all tasks and collect futures
        futures = {executor.submit(process_user, user): user["id"] for user in users}
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(futures):
            user_id = futures[future]
            try:
                success = future.result()
                print(f"User {user_id} processed {'successfully' if success else 'with errors'}")
            except Exception as e:
                print(f"User {user_id} generated an exception: {e}")
    
    end_time = time.time()
    print(f"All users processed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
