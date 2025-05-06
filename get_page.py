import requests
import re

url = "https://www.surfline.com/surf-reports-forecasts-cams/algeria/2589581?__cf_chl_rt_tk=PrhUj.o55upwtM2BwiFkmPa3j25pj8bEdZH6SEj7oy8-1746135910-1.0.1.1-j1t5VOaOo5_7DqISubPnadkHghBO6vNfI.lzry4N2v0"

# Extract the first part of the URL path (e.g., "algeria")
match = re.search(r"surf-reports-forecasts-cams/([^/]+)/", url)
if match:
    file_name = match.group(1) + "_page.html"  # Use the first part and append "_page.html"
else:
    file_name = "page.html"  # Fallback file name if the pattern doesn't match

# Fetch the page
response = requests.get(url)

# Save the HTML to the dynamically generated file name
with open(file_name, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"✅ HTML saved to {file_name}")
