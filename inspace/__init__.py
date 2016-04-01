# TODO
#   set bg for all linux distr - noew is for gnome
#   check if picture of the day is really jpg - done
#   set timer to change bg every day - cron job / cronTab 2.0
#   set prefrences for deleting old bg
#   give notification
#   use git - done
#   set random wallpaper form archive by option
#   show proccess while slow downloading
#   add more resources: telegraph, national geo, theguardian

from BeautifulSoup import BeautifulSoup as bs
from urllib2 import urlopen
from urllib import urlretrieve
import os
import subprocess


def downloadJPG():
    # to check the pictures dir for diffrent linux dist and diffrent languages
    pathtoPic = subprocess.check_output(['xdg-user-dir', 'PICTURES'])[:-1]
    out_folder=pathtoPic+"/Wallpapers"
    sitepath = "http://apod.nasa.gov/apod/" + link["href"]
    filename = sitepath.split("/")[-1]
    outpath = os.path.join(out_folder,filename)
    print "downloading"
    urlretrieve(sitepath,outpath)
    return outpath

def setBG(src):
    command = "gsettings set org.gnome.desktop.background picture-uri file://" + src
    os.system(command)
    print "Enjoy ur new bg"

url = "http://apod.nasa.gov/apod/astropix.html"
soup = bs(urlopen(url))
for link in soup.findAll("a"):
    if link["href"].split(".")[-1] == "jpg":
        src = downloadJPG()
        setBG(src)
        break
    else:
        print "no image for today :/"