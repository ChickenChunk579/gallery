import sys
import json
import requests
import os
from bs4 import BeautifulSoup
from PIL import Image

wallpaperName = sys.argv[1]

wallpapersScraped = json.load(open("wallpapers.json", "r"))

wallpaper = wallpapersScraped[wallpaperName][0]

URL = wallpaper
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

downloadLink = ""

if sys.argv[2] == "4k":
    for link in soup.find_all("a"):
        try:
            #print(link['href'])
            if link['data-downloadurl'].startswith("https://mylivewallpapers.com/download/") and not link['data-downloadurl'].startswith("https://mylivewallpapers.com/download/mobile-"):
                downloadLink = link['data-downloadurl']
        except:
            pass
if sys.argv[2] == "1080p":
    for link in soup.find_all("a"):
        try:
            #print(link['href'])
            if link['data-downloadurl'].startswith("https://mylivewallpapers.com/download/") and not link['data-downloadurl'].startswith("https://mylivewallpapers.com/download/mobile-") and not link['data-downloadurl'].startswith("https://mylivewallpapers.com/download/4k-"):
                downloadLink = link['data-downloadurl']
        except:
            pass

thumbnailLink = wallpapersScraped[wallpaperName][1]

print("Found download link: " + downloadLink)

r = requests.get(downloadLink, allow_redirects=True, headers=headers)
open("wallpaper.mp4", 'wb').write(r.content)

print("Downloaded!")
print("Downloading thumbnail...")

r = requests.get(thumbnailLink, allow_redirects=True, headers=headers)
open("thumbnail.jpg", 'wb').write(r.content)


print("Creating package...")

import shutil
shutil.copytree("./packageTemplate", "./working")

shutil.move("./wallpaper.mp4", "./working/wallpaper.mp4")
shutil.move("./thumbnail.jpg", "./working/thumbnail.jpg")

Image.open("./working/thumbnail.jpg").save("./working/preview.gif")

def process_name(name):
    final = ""
    for word in name.split("-"):
        index = name.split("-").index(word)
        if index == len(name.split("-")) - 1:
            final += word.capitalize()
        else:
            final += word.capitalize() + " "

    return final.replace(" Live Wallpaper", "")

manifest = ""

with open("./working/LivelyInfo.json", "r") as f:
    manifest = f.read().replace("name", process_name(sys.argv[1]))

with open("./working/LivelyInfo.json", "w") as f:
    f.write(manifest)

shutil.move("./working", os.environ.get("AppData") + f"\\..\\Local\\Packages\\12030rocksdanister.LivelyWallpaper_97hta09mmv6hy\\LocalCache\\Local\\Lively Wallpaper\\Library\\wallpapers\\{sys.argv[1]}")

print("Done!")