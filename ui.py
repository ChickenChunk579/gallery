import eel
import json
import os

eel.init('web')

category = "nature"

@eel.expose
def set_category(newCategory):
    global category

    os.system(f"python scrape_category.py {newCategory}")
    category = newCategory

@eel.expose
def get_wallpapers():
    wallpapers = json.load(open("./wallpapers.json", "r"))
    
    for key in wallpapers.keys():
        print(wallpapers[key][0].split("/")[4])
        wallpapers[key].append(wallpapers[key][0].split("/")[4])
    return wallpapers

@eel.expose
def download_wallpaper(name, resolution):
    os.system(f"python main.py {category} {name} {resolution} {name}.zip")
    eel.downloaded()

eel.start('index.html')