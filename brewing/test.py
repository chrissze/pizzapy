from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Set up headless Firefox
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# Navigate to the URL
url = "https://finance.yahoo.com/quote/NVDA/options"
driver.get(url)

# Wait for the page to load (optional)
driver.implicitly_wait(1)

# Get the page source
html = driver.page_source
print(html)

# Close the browser
driver.quit()
