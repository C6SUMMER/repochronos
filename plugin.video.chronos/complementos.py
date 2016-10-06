# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import cookielib,base64
import zipfile

def ExtractAll(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
        return False

    return True


def SportsDevil():
    print "SportsDevil"
    url = "http://proyectoluzdigital.info/download/plugin.video.SportsDevil12-04-16.zip"
    addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
    packageFile = os.path.join(addonsDir, 'packages', 'pld.zip')
    
    urllib.urlretrieve(url, packageFile)
    ExtractAll(packageFile, addonsDir)
        
    try:
        os.remove(packageFile)
    except:
        pass
            
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")
	
def F4mProxy():
    print "F4mProxy"
    url = "http://proyectoluzdigital.info/download/script.video.F4mProxy-2.4.5.zip"
    addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
    packageFile = os.path.join(addonsDir, 'packages', 'pld1.zip')
    
    urllib.urlretrieve(url, packageFile)
    ExtractAll(packageFile, addonsDir)
        
    try:
        os.remove(packageFile)
    except:
        pass
            
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")
	
def F4mTester():
    print "F4mTester"
    url = "http://proyectoluzdigital.info/download/plugin.video.f4mTester-2.2.4.zip"
    addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
    packageFile = os.path.join(addonsDir, 'packages', 'pld2.zip')
    
    urllib.urlretrieve(url, packageFile)
    ExtractAll(packageFile, addonsDir)
        
    try:
        os.remove(packageFile)
    except:
        pass
            
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")  
		
	
	
	
def Vettle():
    print "Vettle"
    url = "http://proyectoluzdigital.info/download/plugin.video.veetle-0.3.3.zip"
    addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
    packageFile = os.path.join(addonsDir, 'packages', 'pld3.zip')
    
    urllib.urlretrieve(url, packageFile)
    ExtractAll(packageFile, addonsDir)
        
    try:
        os.remove(packageFile)
    except:
        pass
            
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("UpdateAddonRepos")	
	
	
elif mode==10:
    SportsDevil()
    F4mProxy()
    F4mTester()
    Vettle()	