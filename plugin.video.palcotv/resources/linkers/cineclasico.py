# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de Descargacineclasico.net para PalcoTV
# Version 0.1 (02/05/2016)
# Autor By Aquilesserr
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
import requests, base64
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = "https://www.cubbyusercontent.com/pl/Cineclasico_logo.png/_e6b9332a9a65417ba1d10ba4743eb5f0"
fanart = "https://www.cubbyusercontent.com/pl/Cineclasico_Fanart.jpg/_260f35172d844f78a7d222067c3d0c26"
sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.1]"

web = "http://www.descargacineclasico.net/"
referer = "http://www.descargacineclasico.net/"

def cineclasico_linker0(params):
    plugintools.log("[%s %s] Linker Descarga Cine Clasico %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker CineClasico"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url")
    r = requests.get(url)
    data = r.content
    
    fondo = plugintools.find_single_match(data,'<meta property="og:image" content="([^"]+)"')
    if fondo =="": fondo = fanart 
    logo = plugintools.find_single_match(data,'<img width="145" height="245" src="([^"]+)"')
    if logo =="": logo = thumbnail

    title = plugintools.find_single_match(data,'<h1 class="page-title">([^\()]+)\(').upper()

    pais = plugintools.find_single_match(data,'<strong>País:</strong></td>.*?rel="tag">(.*?)</a></td>')
    if pais =="": pais = 'N/D'

    year = plugintools.find_single_match(data,'<strong>Año:</strong></td>.*?rel="tag">(.*?)</a></td>')
    if year =="": year = 'N/D'

    bloq_genr = plugintools.find_single_match(data,'<strong>Género:</strong></td>(.*?)</td>')
    genrfull = plugintools.find_multiple_matches(bloq_genr,'rel="category tag">([^<]+)<')
    genr = imdb_genr(genrfull)

    sinopsis = plugintools.find_single_match(data,'<div style="margin-top:-10px;"><p><strong>(.*?)<h3>')
    sinopsis = sinopsis.replace('&#8216;','').replace('&#8220;','').replace('&#8221;','').replace('&#8230;','')
    sinopsis = sinopsis.replace('<strong>','').replace('</strong>','').replace('<br/>','').replace('<em>','').replace('</em>','')
    sinopsis = sinopsis.replace('<p>','').replace('</p>','').replace('&amp;','')
    if sinopsis =="": sinopsis = 'N/D'

    datamovie = {
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["genre"]+datamovie["year"]+datamovie["sinopsis"]

    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    bloq_film = plugintools.find_single_match(data,'<h3>Ver Online(.*?)</center>')
    film =plugintools.find_multiple_matches(bloq_film,'class="MO">(.*?)rel="/nofollow"')
    
    for item in film:
        lang = plugintools.find_single_match(item,'src="http://www.descargacineclasico.net/wp-content/themes/TvClasico/imgdes/(.*?).png').strip()
        if 'esp' in lang:
        	lang = lang.replace('esp','[I][ESP][/I]')
        elif 'dual-sub' in lang:
        	lang = lang.replace('dual-sub','[I][ESP-SUB][/I]')
        elif 'esp-lat-mex' in lang:
        	lang = lang.replace('esp-lat-mex','[I][LAT][/I]')
        elif 'vo' in lang:
        	lang = lang.replace('vo','[I][VO][/I]')
        else: lang = 'N/D'

        quality = plugintools.find_single_match(item,'<span>Opci&oacute;n.*?</span>\s+<span>([^<]+)</span>').strip().replace("\n","").replace("\t","")
        url_vid = plugintools.find_single_match(item,'<a href=(.*?)target="').strip()
        url = cineclasico_adfly(url_vid)
        server = video_analyzer(url)
        titlefull = sc+server.title()+ec+" "+sc2+lang+ec2+" "+sc+" Video: "+ec+sc5+quality+ec5
        plugintools.addPeli(action=server,url=url,title=titlefull,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)

################################################### Herramientas #################################################

def cineclasico_adfly(url):

	r=requests.get(url,timeout=10)
	data = r.text
	ysmm = re.findall(r"var ysmm =.*\;?", data)
	if len(ysmm) > 0:
		ysmm = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])
		left = ''
		right = ''
		for c in [ysmm[i:i+2] for i in range(0, len(ysmm), 2)]:
			left += c[0]
			right = c[1] + right
		decoded_url = base64.b64decode(left.encode() + right.encode())[2:].decode()
		return decoded_url

def imdb_genr(genrfull):
    
    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    elif len(genrfull) >5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    else: genrfull = 'N/D' 
    return genrfull

######################################### @ By Aquilesserr PalcoTv Team ######################################### 