
from os import listdir
from os.path import isfile, join
import cv2
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen,Request
import os
import re
import codecs
from urllib.error import HTTPError
from urllib.request import urlretrieve
import sys
import random





class buildDataset():
    def __init__(self, string):
        if random.random() < 0.05:
            print("For more free resources and continued support, Please subscribe SuyashThefreak and spread the word")
        self.query=string

    def buildfromlink(self):
        return None
    def buildfromquery(self,download_path='./',num_requested=None,chromedriver=None):
        searchtext=self.query
        downloadGoogleImages(searchtext,download_path)
    def organisedataset(self):
        return None
    def generatecsv(self):
        return None

def videoToFrames(source,dest):
    video = cv2.VideoCapture(source)
    flag, frame = video.read()
    count = 0
    while flag:
        print(dest+"frame%d.jpg" % count)
        cv2.imwrite(dest+"frame%d.jpg" % count, frame)  # save frame as JPEG file
        flag, frame = video.read()
        print('Read a new frame: ', flag)
        count += 1

def saveVideoFrames(path,destpath):
    if os.path.isdir(path):
        source = [path+'/'+f for f in listdir(path) if isfile(join(path, f)) and os.path.splitext(f)[-1].lower()==".mp4"]
        dest = [ f for f in listdir(path) if
                  isfile(join(path, f)) and os.path.splitext(f)[-1].lower() == ".mp4"]

        if len(source)==0:
            raise("No video file found!")
    elif os.path.isfile(path):
        ext = os.path.splitext(path)[-1].lower()
        if ext == ".mp4":
            source=[path]
        else:
            raise('ValueError: file format incorrect')
    else:
        raise("Error: It is a special file (socket, FIFO, device file)")
    for s,d in zip(source,dest):
        videoToFrames(s, destpath+'/'+d)


def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False

def get_soup(url, header):
    return BeautifulSoup(urlopen(Request(url, headers=header)), 'html.parser')

def downloadGoogleImages(searchterm,path):
  query = searchterm  # you can change the query for the image  here
  image_type = "ActiOn"
  query = query.split()
  query = '+'.join(query)
  url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch&biw=1280&bih=596"
  header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
  soup = get_soup(url, header)
  scripts = soup.findAll('script')
  largest=scripts[0]
  for i in scripts:
    if len(str(i)) > len(str(largest)):
      largest=i
  regex= r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
  matches = re.findall(regex, str(largest))
  startindex=str(largest).index('({')
  endindex=str(largest).index('});')
  string=codecs.decode(str(largest)[startindex+1:endindex+1], 'unicode_escape')
  matches = [ i for i in re.findall(regex, str(string)) if 'https://encrypted' not in i and 'https://' in i]
  count=0
  if not os.path.exists(path+'/'+query.replace(" ",'_')+'/'):
        os.mkdir(path+'/'+query.replace(" ",'_')+'/')
  import socket
  socket.setdefaulttimeout(3)
  for url in matches:
    try:
      if urlopen(url).getcode()==200 and is_url_image(url):
        count+=1
        urlretrieve(url, path+'/'+searchterm.replace(" ",'_')+'/'+str(count)+'.jpg')
        print("fetching image "+str(count)+" from URL: "+url)
      else:
        print("ignoring image from URL: "+url)
    except FileNotFoundError as err:
        print(err)   # something wrong with local path
    except HTTPError as err:
        print(err)  # something wrong with url
    except KeyboardInterrupt:
        print('Interrupt')
        sys.exit(0)
    except:
        print('Unknown error')
    finally:
      pass

