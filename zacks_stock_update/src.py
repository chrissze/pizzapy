# STANDARD LIBRARIES
import time
import random
import re
import subprocess
import logging
from datetime import datetime
from os.path import basename, exists
from os import environ, remove
from pathlib import Path
from sys import argv, platform
from typing import List, Optional
from urllib.parse import urlparse

# THIRD PARTY LIBRARIES
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import get_browser_version_from_os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_chrome_version():
    """Get the correct Chrome version with multiple fallback methods"""
    try:
        # Method 1: Use webdriver_manager's detection
        version = get_browser_version_from_os("google-chrome")
        if version:
            return version.split('.')[0]  # Return major version
        
        # Method 2: Check registry on Windows
        if platform == "win32":
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon") as key:
                version = winreg.QueryValueEx(key, "version")[0]
                return version.split('.')[0]
        
        # Method 3: Execute chrome --version
        try:
            result = subprocess.check_output(["google-chrome", "--version"])
            version = re.search(r'\d+', result.decode().split()[2])[0]
            return version
        except:
            # Method 4: Try alternative command
            result = subprocess.check_output(["chrome", "--version"])
            version = re.search(r'\d+', result.decode().split()[2])[0]
            return version
            
    except Exception as e:
        logger.error(f"Error detecting Chrome version: {str(e)}")
        return "136"  # Fallback to your current version

def human_like_interaction(driver):
    """Simulate human-like interactions"""
    try:
        # Random mouse movements
        action = webdriver.ActionChains(driver)
        for _ in range(random.randint(2, 5)):
            x_offset = random.randint(-50, 50)
            y_offset = random.randint(-50, 50)
            action.move_by_offset(x_offset, y_offset).pause(random.uniform(0.1, 0.3)).perform()
        
        # Human-like scrolling
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_pos = 0
        while scroll_pos < scroll_height:
            scroll_pos += random.randint(200, 500)
            driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
            time.sleep(random.uniform(0.2, 0.7))
            
            # Random scroll back sometimes
            if random.random() > 0.8:
                driver.execute_script(f"window.scrollTo(0, {scroll_pos - random.randint(50, 150)});")
                time.sleep(random.uniform(0.3, 0.6))
                
        # Scroll to top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.5, 1.2))
    except Exception:
        pass

def solve_incapsula(driver):
    """Solve Incapsula protection challenges"""
    try:
        # Check if challenge page is displayed
        if "Incapsula" in driver.title or "DDoS protection" in driver.page_source:
            logger.info("Solving Incapsula challenge...")
            
            # Solution 1: Click verify button if exists
            try:
                verify_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Verify')] | //button[contains(., 'Verify')]"))
                )
                verify_button.click()
                logger.info("Clicked verify button")
                time.sleep(3)
            except:
                pass
            
            # Solution 2: Execute JavaScript challenge solver
            driver.execute_script("""
                if (typeof _cf_chl_opt === 'object') {
                    _cf_chl_opt.cUPMDTk = new Date().getTime();
                    _cf_chl_opt.cRay = Math.random().toString(36).substring(2, 15);
                }
                if (typeof solveChallenge === 'function') solveChallenge();
                if (typeof _cf_chl_enter === 'function') _cf_chl_enter();
            """)
            time.sleep(5)
            
            # Solution 3: Refresh if still blocked
            if "Incapsula" in driver.title:
                logger.info("Refreshing after challenge solve attempt")
                driver.refresh()
                time.sleep(5)
                
        return "Incapsula" not in driver.title
    except Exception as e:
        logger.error(f"Error solving Incapsula: {str(e)}")
        return False

def create_driver():
    """Create properly configured Chrome driver with version matching"""
    # Get correct Chrome major version
    chrome_major_version = get_chrome_version()
    logger.info(f"Using Chrome major version: {chrome_major_version}")
    
    # Configure Chrome options
    options = uc.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Set user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.0.0 Safari/537.36".format(chrome_major_version),
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={user_agent}")
    
    # Create undetected Chrome driver with version matching
    driver = uc.Chrome(
        options=options,
        version_main=int(chrome_major_version),
        headless=False,  # Crucial for bypassing
        use_subprocess=True,
    )
    
    # Set window size
    driver.set_window_size(1280 + random.randint(-100, 100), 1024 + random.randint(-50, 50))
    
    # Apply stealth settings
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = {runtime: {}, app: {isInstalled: false}};
        """
    })
    
    return driver

def get_html(url, get_source=False) -> tuple[str, str]:
    logger.info("Initializing browser to bypass Incapsula...")
    
    driver = None
    try:
        # Create driver with automatic version matching
        driver = create_driver()
        logger.info(f"Accessing: {url}")
        
        # First visit to prime cookies
        driver.get("https://www.zacks.com/")
        time.sleep(random.uniform(2.5, 4.5))
        human_like_interaction(driver)
        
        # Navigate to target URL
        driver.get(url)
        time.sleep(random.uniform(3.0, 5.0))
        
        # Solve protection challenges
        if not solve_incapsula(driver):
            logger.warning("Could not bypass protection on first attempt. Retrying...")
            driver.get(url)
            time.sleep(random.uniform(4.0, 6.0))
            solve_incapsula(driver)
        
        # Simulate human interaction
        human_like_interaction(driver)
        
        # Wait for page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//body"))
        )
        
        # Final interaction
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight/2);")
        time.sleep(1.2)
        
        # Get results
        html_text = driver.page_source if get_source else ""
        redirect_url = driver.current_url
        
        # Save debug info
        driver.save_screenshot('debug_screenshot.png')
        if get_source:
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(html_text)
            logger.info("Saved debug files: debug_screenshot.png, debug_page.html")
        
        return redirect_url, html_text
        
    except Exception as e:
        logger.error(f"Navigation error: {str(e)}")
        html_text = driver.page_source if driver and get_source else ""
        redirect_url = driver.current_url if driver else url
        return redirect_url, html_text
        
    finally:
        if driver:
            driver.quit()

def test1():
    url = 'https://www.zacks.com/stock/research/NVDA/stock-style-scores'
    logger.info("Starting test...")
    x, y = get_html(url, get_source=True)
    logger.info(f"Final URL: {x}")
    logger.info(f"Page source length: {len(y) if y else 0} characters")

if __name__ == "__main__":
    test1()