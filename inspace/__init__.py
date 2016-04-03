# TODO
#   change getrandombeforeyears
#   set bg for all linux distr - now is for gnome supported linux
#   check if picture of the day is really jpg - done im getting the img tag only
#   set prefrences for deleting old bg - done
#   use git - done
#   set random wallpaper from archive by option - done
#   show file details and progress while slow downloading - done
#   add more resources: telegraph,  national geo,  theguardian
#   give notification
#   check if the photo already exists,  if so just set it as bg don't download
#   change bg aligment optional
#   handle errors
#   set timer to change bg every day - cron job / cronTab 2.0
#   paackage it !

from BeautifulSoup import BeautifulSoup as bs
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys
import subprocess
import random
import time
import argparse
import glob


VERSION = 0.1
ERROR = {
    'wrongedate': "This date is not valibale",
    'noimg': "Looks like no img in this page"
    }
MSG = {
    'downloading': 'Downloading ...',
    'done': 'Enjoy your new wallpaper.'
    }

DIRPATH = subprocess.check_output(['xdg-user-dir',  'PICTURES'])[:-1] + "/Wallpapers"


def _reporthook(numblocks, blocksize, filesize, url=None):
    # print "reporthook(%s, %s, %s)" % (numblocks, blocksize, filesize)
    # base = os.path.basename(url)
    # XXX Should handle possible filesize=-1.
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
    except:
        percent = 100
    if numblocks != 0:
        sys.stdout.write("\b"*70)
    x = filesize/1024.0
    sys.stdout.write("downloading:\t%.2f %-20s %3d%%" % (x, "kB", percent))


def downloadJPG(link):
    # to check the pictures dir for diffrent linux dist and diffrent languages
    imgpath = "http://apod.nasa.gov/apod/" + link
    filename = "inspace_" + imgpath.split("/")[-1]
    outpath = os.path.join(DIRPATH, filename)
    urlretrieve(imgpath, outpath, lambda nb, bs, fs, url=imgpath: _reporthook(nb, bs, fs, url))
    print
    return outpath


def setBG(src):
    command = "gsettings set org.gnome.desktop.background picture-uri file://" + src
    os.system(command)
    print MSG['done']


def deletePrev(deleteit):
    if deleteit:
        path = os.path.join(DIRPATH, "inspace_*")
        files = glob.glob(path)
        for f in files:
            os.remove(f)


# this code should be modified compined with getimageofdate
def getrandombeforeyears(years):
    now = time.mktime(time.gmtime())
    # indate = time.mktime(time.strptime('110402',  '%y%m%d'))
    before = abs(int(years*365.25*24*60*60))
    first = time.mktime(time.strptime('950616',  '%y%m%d'))
    if now - before < first:
        print ERROR['wrongedate']
        quit()
    randomdate = time.strftime('%y%m%d',  time.localtime(now - random.randrange(before)))
    return "http://apod.nasa.gov/apod/ap"+randomdate+".html"


def getimageofdate(date):
    now = time.mktime(time.gmtime())
    given = time.mktime(time.strptime(date,  '%y%m%d'))
    first = time.mktime(time.strptime('950616',  '%y%m%d'))
    if given > now or given < first:
        print ERROR['wrongedate']
        quit()
    return "http://apod.nasa.gov/apod/ap"+date+".html"


def run(deleteit, url="http://apod.nasa.gov/apod/astropix.html"):
    print ("Nasa page:\t%s" % url)
    soup = bs(urlopen(url))
    print ("Image title:\t%s" % soup.findAll("center")[1].b.string[1:])
    img = soup.img
    if img is not None:
        deletePrev(deleteit)
        src = downloadJPG(img.parent["href"])
        setBG(src)
    else:
        print ERROR['noimg']


parser = argparse.ArgumentParser(prog='inspace', description='Jump into space with Nasa\'s images')
parser.add_argument('-v', action='version', version='%(prog)s '+str(VERSION))
parser.add_argument('-r', metavar='N', type=float, help='set number of past years to get a random date from')
parser.add_argument('-d', metavar='YYMMDD', help='get the image of the given date OVERRIRDS -r')
parser.add_argument('-c', action='store_true', help='clear ALL pervious downloaded images')
args = parser.parse_args()


if args.d is not None:
    run(args.c, getimageofdate(args.d))
elif args.r is not None:
    run(args.c, getrandombeforeyears(args.r))
else:
    run(args.c)
