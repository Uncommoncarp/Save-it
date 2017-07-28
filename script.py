# A quick script to pull all saved images from a reddit account
from urllib.request import urlopen, Request
from io import BytesIO
import praw
import requests
from PIL import Image
from urllib.parse import urlparse, urlunparse
import requests
import lxml.html
import re
import os

#####################################################################
## ENTER YOUR USERNAME, PASSWORD, CLIENT ID AND CLIENT SECRET HERE ##
#####################################################################
_user = 'YOUR USER NAME'
_pass = 'YOUR PASSWORD'
_client_id = 'YOUR REDDIT CLIENT ID'
_client_secret = 'YOUR REDDIT CLIENT SECRET'

_user_agent_string = ""
_image_formats = ['bmp','dib','eps','ps','gif','im','jpg','jpe','jpeg',
                  'pcd','pcx','png','pbm','pgm','ppm','psd','tif','tiff',
                  'xbm','xpm','rgb','rast','svg']

 
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_image_link(submission):
    if link.subreddit.display_name == 'pics' \
      or 'imgur' in submission.domain.split('.') \
      or submission.url.split('.')[-1] in _image_formats:
        return True
    else:
        return False

def get_album_links(link):
    data = requests.get(link.url).content
    imageLinks = re.findall('<img class=\"post-image-placeholder\" src=\"//i\.imgur\.com\/.*', str(data,'utf-8'))
    imagesLinks = []
    for imageLink in imageLinks:
        imagesLinks.append(re.search('i\.imgur\.com\/.*(jpg|png)', imageLink).group(0))
        
    for image in imagesLinks:
        fname=image.split('/')[-1]
        if "?" in fname:
            fname=fname.split('?')[0]
        f = open("Images/"+fname,'wb')
        data = requests.get("http://"+image).content
        f.write(data)
        f.close()


reddit = praw.Reddit(client_id=_client_id,
             client_secret=_client_secret,
             user_agent='Saved Image Downloader',
             username=_user,
             password=_pass)
reddit.read_only

saved = reddit.redditor('uncommoncarp').saved(limit=None)

ensure_dir("Images/")

for link in saved:
    if not is_image_link(link):
        continue   

    fname=link.url.split('/')[-1]
    if "?" in fname:
        fname=fname.split('?')[0]

    
    if not "." in fname and "/a/" in link.url:
        get_album_links(link)
        print("Album: " + link.url + " done")


    else:
        try:
            data = requests.get(link.url).content
            if "gifv" in fname:
                print(link.url)
                fname = fname.replace("gifv","mp4")
                try:
                    data = requests.get("http://" + re.search('i\.imgur\.com\/.*\.mp4', str(data,'utf-8')).group(0)).content
                except UnicodeDecodeError:
                    print(link.url + " has probably been removed")


            else:
                print(link.url)
                if not "i." in link.url and "imgur" in link.url and not "jpg" in link.url:
                    url = re.search('i\.imgur\.com\/.*\.(jpg|png)', str(data,'utf-8')).group(0)
                    data = requests.get("http://" + url).content
                    fname=url.split('/')[-1]
                    if "?" in fname:
                        fname=fname.split('?')[0]

            f = open("Images/"+fname,'wb')
            f.write(data)
            f.close()
            print("Image: " + link.url + " done")
        except (requests.exceptions.ConnectionError, AttributeError):
            print(link.url + " has probably been removed")

    
