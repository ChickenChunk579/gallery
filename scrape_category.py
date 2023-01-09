import requests
from bs4 import BeautifulSoup
import re
import sys

category = sys.argv[1]

URL = f"https://mylivewallpapers.com/category/{category}"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
pagesToScrape = 3

wallpapers = {}

for i in range(pagesToScrape):
    if i + 1 == 1:
        page = requests.get(URL, headers=headers)
    else:
        page = requests.get(URL + "/page/" + str(i + 1), headers=headers)
    
    soup = BeautifulSoup(page.content, "html.parser")

    posts = soup.find(id="posts")

    for post in posts.find_all("a"):
        if not re.search(r'/page/\d+/$', post['href']):
            id = post['id'].split("-")[1]

            wallpapers[post['href'].split("/")[4]] = [post['href'], post['style'].split("( ")[1].split(" )")[0]]

with open("wallpapers.json", "w") as f:
    f.write(str(wallpapers).replace("'", '"'))