"""
adding code to print src code below
"""
import requests
from bs4 import BeautifulSoup

url = "https://m.macrotrends.net/stocks/charts/NVDA/nvidia/shares-outstanding"
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    # Fetch webpage
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    # Get HTML content
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract meta description
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        print("\nMeta Description Found:")
        print(meta_description.get('content'))
    else:
        print("\nMeta description not found.")
    
    # Print source code preview
    print("\nSource Code Preview (first 2000 characters):")
    print("-" * 50)
    print(html_content[:2000])
    print("-" * 50)
    print(f"... [truncated] Total length: {len(html_content)} characters")
    
    # Save full source to file
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("\nFull source code saved to 'page_source.html'")

except requests.exceptions.RequestException as e:
    print(f"\nRequest failed: {e}")
except Exception as e:
    print(f"\nError occurred: {e}")