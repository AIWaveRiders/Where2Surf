import requests
from bs4 import BeautifulSoup
import re

url = "https://www.surfline.com/surf-reports-forecasts-cams/algeria/2589581"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    # Match surf spot links
    if re.match(r"^/surf-report/[^/]+/\d+", href):
        full_url = "https://www.surfline.com" + href
        links.append(full_url)

print(f"Found {len(links)} links to surf spots in Algeria.")

# Print or save to a text file
for link in links:
    print(link)

# Optional: save to text
# with open("algeria_links.txt", "w") as f:
#     f.write("\n".join(links))
