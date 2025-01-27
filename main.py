import requests
from bs4 import BeautifulSoup

# Define the URL
url = "https://example.com"

# Send an HTTP request
response = requests.get(url)

# Check for successful request
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Find and print all links
    for link in soup.find_all('a'):
        print(link.get('href'))
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
