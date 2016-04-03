# TODO
#   set bg for all linux distr - now is for gnome supported linux
#   check if picture of the day is really jpg - done im getting the img tag only
#   set timer to change bg every day - cron job / cronTab 2.0
#   set prefrences for deleting old bg
#   give notification
#   use git - done
#   set random wallpaper from archive by option - done
#   show file details and progress while slow downloading
#   add more resources: telegraph, national geo, theguardian
#   check if the photo already exists, if so just set it as bg don't download
#   change bg aligment optional
#   handle errors
#   paackage it !

from BeautifulSoup import BeautifulSoup as bs
from urllib2 import urlopen
from urllib import urlretrieve
import os
import subprocess
import random
import time
import argparse


VERSION = 0.1

def downloadJPG(link):
    # to check the pictures dir for diffrent linux dist and diffrent languages
    pathtoPic = subprocess.check_output(['xdg-user-dir', 'PICTURES'])[:-1]
    out_folder=pathtoPic+"/Wallpapers"
    sitepath = "http://apod.nasa.gov/apod/" + link
    filename = sitepath.split("/")[-1]
    outpath = os.path.join(out_folder,filename)
    print "downloading"
    urlretrieve(sitepath,outpath)
    return outpath

def setBG(src):
    command = "gsettings set org.gnome.desktop.background picture-uri file://" + src
    os.system(command)
    print "Enjoy ur new bg"

def getrandombeforeyears (years):
    now = time.mktime(time.gmtime())
    # indate = time.mktime(time.strptime('110402', '%y%m%d'))
    before = abs(int(years*365.25*24*60*60))
    first = time.mktime(time.strptime('950616', '%y%m%d'))
    if now - before < first:
        print "wrone date"
        quit()
    randomdate = time.strftime('%y%m%d', time.localtime(now - random.randrange(before)))
    return "http://apod.nasa.gov/apod/ap"+randomdate+".html"

def getimageofdate (date):
    now = time.mktime(time.gmtime())
    given = time.mktime(time.strptime(date, '%y%m%d'))
    first = time.mktime(time.strptime('950616', '%y%m%d'))
    if given > now or given < first:
        print "wrone date"
        quit()
    return "http://apod.nasa.gov/apod/ap"+date+".html"


def run(url="http://apod.nasa.gov/apod/astropix.html"):
    print ("Nasa page:\t%s" % url)
    soup = bs(urlopen(url))
    print ("Image title:\t%s" % soup.findAll("center")[1].b.string[1:])
    # print soup.find_all(string="falcon")
    img = soup.img
    if img != None:
        src = downloadJPG(img.parent["href"])
        setBG(src)
    else:
        print "no image found"


parser = argparse.ArgumentParser(prog='inspace',description='Jump into space with Nasa\'s images')
parser.add_argument('-v',action='version',version='%(prog)s '+str(VERSION))
parser.add_argument('-r',metavar='years',type=float, help='set number of past years to get a random date from')
parser.add_argument('-d',metavar='YYMMDD', help='get the image of the given date')
args = parser.parse_args()

if args.r != None:
    run(getrandombeforeyears(args.r))
elif args.d != None:
    run(getimageofdate(args.d))
else:
    run()