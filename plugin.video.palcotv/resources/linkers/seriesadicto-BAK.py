# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Seriesadicto.com Linker para PalcoTV
# Version 0.2 (11/04/2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

referer = "http://seriesadicto.com/"   
thumbnail = "https://www.cubbyusercontent.com/pl/seriesadicto_logo.png/_551cfa93002e4f19a438b5f841fc109a"
fanart = "https://www.cubbyusercontent.com/pl/Seriesadicto_fanart.jpg/_8b701c2093414398b6d6a11ea6f07aa3"

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.2]"


def seriesadicto_linker0(params):
    plugintools.log('[%s %s] Linker SeriesBlanco %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Seriesadicto"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    url = params.get("url")
    r = requests.get(url)
    data = r.content

    logo = referer + plugintools.find_single_match(data,'<img style="width: 240px; height: 360px;" src="([^"]+)"')
    if logo =="": logo = thumbnail
    title = plugintools.find_single_match(data,'<h1>(.*?)</h1>').strip()
    n_temp = plugintools.find_multiple_matches(data,'<i class="glyphicon"></i(.*?)</tbody>')
    try:
        sinopsis = plugintools.find_single_match(data,'<p>(.*?)</p>').replace('<h3>',sc3+'[B]').replace('</h3>',':[/B]'+ec3)
    except:
        sinopsis = plugintools.find_single_match(data,'<p>(.*?)</p>').replace('<h3>','[B]').replace('</h3>',':[/B]')

    datamovie = {
    'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(len(n_temp))+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["season"]+datamovie["sinopsis"]

    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
    #plugintools.add_item(action="",url="",title=sc5+str(len(n_temp))+" Temporadas disponibles"+ec5,thumbnail=logo,fanart=fanart,folder=False,isPlayable=False)
    for temp in n_temp:
        name_temp = plugintools.find_single_match(temp,'>(.*?)</a>').strip()
        plugintools.add_item(action="",url="",title=sc2+'-- '+name_temp+' --'+ec2,thumbnail=logo,fanart=fanart,folder=False,isPlayable=False)
        capis = plugintools.find_multiple_matches(temp,'<td class="sape">(.*?)</tr>')
        for item in capis:
                
            url_cap = plugintools.find_single_match(item,'<a href="([^"]+)"')
            url_cap = referer+url_cap
                
            title_capi = plugintools.find_single_match(item,'class="color4">(.*?)</a>')
            title_capi = sc+title_capi.strip()+ec
                
            plugintools.add_item(action="seriesadicto_linker_epis",url=url_cap,title=title_capi,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)
    
def seriesadicto_linker_epis(params):
    plugintools.log('[%s %s] Linker SeriesBlanco %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Seriesadicto"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    url = params.get("url")
    r = requests.get(url)
    data = r.content
    
    logo = referer + plugintools.find_single_match(data,'<img style="width: 240px; height: 360px;" src="([^"]+)"')
    if logo =="": logo = thumbnail
    title = plugintools.find_single_match(data,'<h1>(.*?)</h1>').strip()
    num_epis = plugintools.find_single_match(data,'<link rel="canonical" href="http://seriesadicto.com/capitulo/.*?/(.*?)/(.*?)/')
    num_epis = num_epis[0]+'x'+num_epis[1]
    if num_epis =="": num_epis = title
    
    plugintools.addPeli(action="",url="",title=sc2+"[B]"+title+"[/B]"+ec2,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
    
    bloq_link = plugintools.find_single_match(data,'<tbody>(.*?)</table>')
    link = plugintools.find_multiple_matches(bloq_link,'<tr class="(.*?)</tr>')
    for item in link:
        lang = plugintools.find_single_match(item,'<td><img src="([^"]+)"')
        if '1.png' in lang: lang = sc2+'[I][ESP][/I]'+ec2
        if '2.png' in lang: lang = sc2+'[I][LAT][/I]'+ec2
        if '3.png' in lang: lang = sc2+'[I][ENG-SUB][/I]'+ec2
        if '4.png' in lang: lang = sc2+'[I][ENG][/I]'+ec2
        url_server = plugintools.find_single_match(item,'<a href="([^"]+)"')
        server = video_analyzer(url_server)
        titlefull = sc+'Capitulo '+num_epis+ec+" "+sc2+lang+ec2+" "+sc5+'[I]['+server.title()+'][/I]'+ec5
        plugintools.addPeli(action=server,url=url_server,title=titlefull,thumbnail=logo,fanart=fanart,folder=False,isPlayable=True)

############################################# By PalcoTv Team ####################################################