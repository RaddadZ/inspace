# TODO
#   set bg for all linux distr
#   check if picture of the day is really jpg
#   set timer to change bg every day
#   set prefrences for deleting old bg
#   give notification
#   use git

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
    urlretrieve(sitepath,outpath)
    return filename

def setBG(filename):
    command = "gsettings set org.gnome.desktop.background picture-uri file:///home/ramad/Pictures/Wallpapers/"+filename
    os.system(command)

url = "http://apod.nasa.gov/apod/astropix.html"
soup = bs(urlopen(url))
for link in soup.findAll("a"):
    if link["href"].split(".")[-1] == "jpg":
        filename = downloadJPG()
        setBG(filename)
        break