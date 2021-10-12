#!/usr/bin/env python

import feedparser
import json
import re
import os
import glob
import urllib.request
import random
import string
from resizeimage import resizeimage

from resizeimage.imageexceptions import ImageSizeError

from PIL import Image, ImageDraw, ImageFont

feedUrl = "https://www.reddit.com/r/EarthPorn.rss"

sizeRegex = re.compile(r'\[\d+x\d+\]')
imageRegex = re.compile(r'<a href="(\S*)">\[link\]</a>')

min_x = 1920
min_y = 1080

images_folder = "/home/bmateu/.local/share/spotlight-from-reddit/"

raw_folder = '/raw/'
wallpaper_folder = '/wallpaper/'
lockscreen_folder = '/lock/'

"""
Check if size of image is big enough for screen

Returns: True if size is acceptable
"""
def size_match(entry):
    match = sizeRegex.findall(entry.title)
    if not match: return False
    size_x, size_y = match[0][1:-1].split('x')

    return int(size_x) >= min_x and int(size_y) >= min_y

"""
Returns url of given image
"""
def get_url(entry):
    match = imageRegex.findall(entry.content[0].value)
    return match[0]

def fetch_image(url):
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    urllib.request.urlretrieve(url, images_folder + raw_folder + name + '.jpg') 
    return True


def resize_images():
    _, _, filenames = next(os.walk(images_folder + '/raw/'))
    for filename in filenames:
        with open(images_folder + raw_folder + filename, 'rb') as f:
            with Image.open(f) as image:
                try:
                    formatted_image = resizeimage.resize_cover(image, [min_x, min_y]).convert('RGBA')
                    txt = Image.new('RGBA', formatted_image.size, (255,255,255,0))
                    draw = ImageDraw.Draw(txt)
                    fnt = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans.ttf', 15)
                    text = "helloWorld"
                    draw.text((txt.size[0]-7, txt.size[1]-4), text, anchor="rb", font=fnt, fill="#808080F0")
                    combined = Image.alpha_composite(formatted_image, txt)
                    combined.convert('RGB').save(images_folder + wallpaper_folder + filename, quality=100, subsampling=0)
                except ImageSizeError as e:
                    print(e.message)

def generate_lockscreen_images():
    _, _, filenames = next(os.walk(images_folder + wallpaper_folder))
    for filename in filenames:
        with open(images_folder + wallpaper_folder + filename, 'rb') as f:
            with Image.open(f) as image:
                draw = ImageDraw.Draw(image, 'RGBA')
                draw.rectangle([(60, image.size[1] - 40), (560, image.size[1] - 170)], fill="#00000090")
                image.convert('RGB').save(images_folder + lockscreen_folder + filename, quality=100, subsampling=0)

def clean_raw_images():
    files = glob.glob(images_folder + raw_folder + "/*")
    for f in files:
        os.remove(f)

def clean_processed_images():
    files = glob.glob(images_folder + wallpaper_folder + "/*")
    for f in files:
        os.remove(f)
    files = glob.glob(images_folder + lockscreen_folder + "/*")
    for f in files:
        os.remove(f)

if __name__ == "__main__":

    if not os.path.exists(images_folder):
        os.mkdir(images_folder)
    if not os.path.exists(images_folder + raw_folder):
        os.mkdir(images_folder + raw_folder)
    if not os.path.exists(images_folder + wallpaper_folder):
        os.mkdir(images_folder + wallpaper_folder)
    if not os.path.exists(images_folder + lockscreen_folder):
        os.mkdir(images_folder + lockscreen_folder)

    print("Gatherihg RSS feed...", flush=True, end='')

    feed = feedparser.parse(feedUrl)
    entry = feed.entries[2]

    print(" done !")
    clean_raw_images()
    print("Raw images removed !")
    print("Downloading images ", flush=True, end='')

    for entry in feed.entries:
        if not size_match(entry): continue

        url = get_url(entry)
        fetch_image(url)
        print('.', end='', flush=True)

    print(" done !")
    clean_processed_images()
    print("Resizing images...", flush=True, end='')
    resize_images()
    print(" done")
    print("Generating lockscreens...", flush=True, end='')
    generate_lockscreen_images()
    print(" done")

    clean_raw_images()
    print("Raw images removed !")
