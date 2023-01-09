import os, sys

if sys.argv[1] == "help":
    print("Usage:")
    print("python main.py [category] [name] [resolution (4k / 1080p)] [output]")
else:
    os.system(f"python ./scrape_category.py {sys.argv[1]} | python ./download_wallpaper.py {sys.argv[2]} {sys.argv[3]} {sys.argv[4]}")