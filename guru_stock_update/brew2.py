r"""

    
"""

# STANDARD LIBRARIES

from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
from io import StringIO
from os.path import basename
from os import environ
from pathlib import Path
from re import search, sub
from subprocess import run
from sys import argv, platform
from typing import List, Optional
from urllib.parse import urlparse


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup, ResultSet

from pandas import DataFrame, ExcelWriter, isna, read_html

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tenacity import retry, RetryError, stop_after_attempt
from webdriver_manager.chrome import ChromeDriverManager






# Function to get the final redirected URL
def get_redirect_url_html(url, get_source=False) -> tuple[str, str]:
    """

    """
    print('    .')

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--enable-javascript")
    options.add_argument("--headless=new")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Recommended for running as root
    options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues
    options.add_argument("--incognito")  # Start in incognito mode to disable cache

    service=Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(
        options=options, 
        service=service
    )

    html_text = ""
    browser.get(url)

    if get_source:
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        
        # html_text should be placed before redirect_url to load the whole page
        html_text: str = browser.page_source
        
    redirect_url: str = browser.current_url

    browser.quit()
    return redirect_url, html_text



        
    

def main():
    url = 'https://macrotrends.net/stocks/charts/NVDA/nvidia/shares-outstanding'
    u2, src = get_redirect_url_html(url, get_source=True)
    print(u2)
    print(src)






if __name__ == '__main__':
    main()