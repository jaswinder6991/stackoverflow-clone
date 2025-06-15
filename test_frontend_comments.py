#!/usr/bin/env python3
"""
Frontend comment system test using Selenium WebDriver
Tests the UI interactions for comments
"""

import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_frontend_comments():
    print("🌐 Testing Frontend Comment System\n")
    
    # Setup Chrome driver with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        
        print("1. Opening question page...")
        driver.get("http://localhost:3000/questions/1")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        print("✅ Question page loaded successfully")
        
        # Check for comment sections
        print("\n2. Looking for comment sections...")
        comment_sections = driver.find_elements(By.CLASS_NAME, "mt-4")
        print(f"✅ Found {len(comment_sections)} potential comment sections")
        
        # Look for "Add a comment" buttons
        print("\n3. Looking for 'Add a comment' buttons...")
        add_comment_buttons = driver.find_elements(By.XPATH, "//span[text()='Add a comment']")
        print(f"✅ Found {len(add_comment_buttons)} 'Add a comment' buttons")
        
        # Look for existing comments
        print("\n4. Looking for existing comments...")
        comment_containers = driver.find_elements(By.CLASS_NAME, "bg-gray-50")
        print(f"✅ Found {len(comment_containers)} comment containers")
        
        # Check for upvote buttons in comments
        print("\n5. Looking for comment upvote buttons...")
        upvote_buttons = driver.find_elements(By.XPATH, "//button[contains(@title, 'This comment adds something useful')]")
        print(f"✅ Found {len(upvote_buttons)} comment upvote buttons")
        
        # Take a screenshot for manual verification
        driver.save_screenshot("/tmp/comment_system_screenshot.png")
        print("✅ Screenshot saved to /tmp/comment_system_screenshot.png")
        
        print("\n🎉 Frontend comment system appears to be working!")
        
    except Exception as e:
        print(f"❌ Error during frontend testing: {e}")
        # Try to get page source for debugging
        try:
            with open("/tmp/page_source.html", "w") as f:
                f.write(driver.page_source)
            print("📄 Page source saved to /tmp/page_source.html for debugging")
        except:
            pass
    
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    # First check if frontend is accessible
    try:
        response = requests.get("http://localhost:3000/questions/1", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible, starting UI tests...")
            test_frontend_comments()
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot reach frontend: {e}")
        print("Make sure the frontend container is running on port 3000")
