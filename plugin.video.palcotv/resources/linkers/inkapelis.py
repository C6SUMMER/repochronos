# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de Inkapelis.com para PalcoTV
# Version 0.1 (07/05/2016)
# Autor By Aquilesserr
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)
#------------------------------------------------------------

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
import requests
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = "https://www.cubbyusercontent.com/pl/Inkapelis-logo.png/_b77459d1fdd74672b78eab8e04077230"
fanart = "https://www.cubbyusercontent.com/pl/Inkapelis_fanart.jpg/_ca5dfbfc2ee742079f1e48103fb75e9d"
sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.1]"

web = "http://www.inkapelis.com/"
referer = "http://www.inkapelis.com/"

def inkapelis_linker0(params):
    plugintools.log("[%s %s] Linker Inkapelis %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Inkapelis"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url")
    r = requests.get(url)
    data = r.content
    
    fondo = plugintools.find_single_match(data,'style="background-image: url\(([^)]+)\)').strip()
    if fondo =="": fondo = fanart 
    logo = plugintools.find_single_match(data,'<div class="col-xs-2 poster"> <img src="([^"]+)"')
    if logo =="": logo = thumbnail 
    
    bloq_info = plugintools.find_single_match(data,'<h2>Sinopsis</h2>(.*?)<span class="aa">Reparto</span>') 

    title = plugintools.find_single_match(bloq_info,'<span class="aa">Título</span> <span class="ab">([^<]+)</span>').upper().strip()
    votos = plugintools.find_single_match(bloq_info,'<span class="aa">Calificación</span> <span class="ab">([^<]+)</span>').strip()
    if votos =="": punt_imdb = 'N/D'
    year = plugintools.find_single_match(bloq_info,'<span class="aa">Año de lanzamiento</span> <span class="ab">([^<]+)</span>').strip()
    if year =="": year = 'N/D'

    durac = plugintools.find_single_match(bloq_info,'<span class="aa">Duración</span> <span class="ab">([^<]+)</span>').strip()
    if durac =="": durac = 'N/D'

    genrfull = plugintools.find_multiple_matches(bloq_info,'rel="category tag">([^<]+)</a>')
    genr = inkapelis_genr(genrfull)

    sinopsis = plugintools.find_single_match(bloq_info,'<p class="trasnparente">(.*?)</p>').strip().replace('<a href=','').replace('</strong>','').replace('<strong>','')

    datamovie = {
    'rating': sc3+'[B]Votos: [/B]'+ec3+sc+str(votos)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]+datamovie["sinopsis"]
    
    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    lang_embed1 = plugintools.find_single_match(data,'<a href="#embed1" data-toggle="tab">(.*?)</a>')
    if lang_embed1 !="":
    	quality_embed1 = plugintools.find_single_match(data,'id="embed1"><div class="calishow">(.*?)</div>')
    	url_embed1 = plugintools.find_single_match(data,'id="embed1">.*?src="([^"]+)"')
    	server1 = video_analyzer(url_embed1)
    	titlefull1 = sc+server1.title()+ec+" "+sc2+' [I]['+lang_embed1+'][/I]'+ec2+" "+sc+" Video: "+ec+sc5+quality_embed1+ec5
    	plugintools.addPeli(action=server1,url=url_embed1,title=titlefull1,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
    else: pass
   
    lang_embed2 = plugintools.find_single_match(data,'<a href="#embed2" data-toggle="tab">(.*?)</a>')
    if lang_embed2 !="":
    	quality_embed2 = plugintools.find_single_match(data,'id="embed2"><div class="calishow">(.*?)</div>')
    	url_embed2 = plugintools.find_single_match(data,'id="embed2">.*?src="([^"]+)"')
    	server2 = video_analyzer(url_embed2)
    	titlefull2 = sc+server2.title()+ec+" "+sc2+' [I]['+lang_embed2+'][/I]'+ec2+" "+sc+" Video: "+ec+sc5+quality_embed2+ec5
    	plugintools.addPeli(action=server2,url=url_embed2,title=titlefull2,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
    else: pass
    
    lang_embed3 = plugintools.find_single_match(data,'<a href="#embed3" data-toggle="tab">(.*?)</a>')
    if lang_embed3 !="":
        quality_embed3 = plugintools.find_single_match(data,'id="embed3"><div class="calishow">(.*?)</div>')
        url_embed3 = plugintools.find_single_match(data,'id="embed3">.*?src="([^"]+)"')
        server3 = video_analyzer(url_embed3)
        titlefull3 = sc+server3.title()+ec+" "+sc2+' [I]['+lang_embed3+'][/I]'+ec2+" "+sc+" Video: "+ec+sc5+quality_embed3+ec5
        plugintools.addPeli(action=server3,url=url_embed3,title=titlefull3,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
    else: pass
    
    lang_embed4 = plugintools.find_single_match(data,'<a href="#embed4" data-toggle="tab">(.*?)</a>')
    if lang_embed4 !="":
        quality_embed4 = plugintools.find_single_match(data,'id="embed4"><div class="calishow">(.*?)</div>')
        url_embed4 = plugintools.find_single_match(data,'id="embed4">.*?src="([^"]+)"')
        server4 = video_analyzer(url_embed4)
        titlefull4 = sc+server4.title()+ec+" "+sc2+' [I]['+lang_embed4+'][/I]'+ec2+" "+sc+" Video: "+ec+sc5+quality_embed4+ec5
        plugintools.addPeli(action=server4,url=url_embed4,title=titlefull4,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
    else: pass

    bloq_server = plugintools.find_single_match(data,'class="dlmt">Opciones Para Ver Online</h2>(.*?)class="dlmt">Opciones Para Descargar</h2>')
    serverfull = plugintools.find_multiple_matches(bloq_server,'<tr><td>(.*?)</tr>')
    for item in serverfull:
    	lang = plugintools.find_single_match(item,'</span></td><td>([^<]+)</td><td>').strip()
        lang = '['+lang+']'
    	quality = plugintools.find_single_match(item,'</span></td><td>.*?</td><td>([^<]+)</td>').strip()
        url_vid = plugintools.find_single_match(item,'<a href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = sc+server.title()+ec+" "+sc2+" [I]"+lang+"[/I] "+ec2+" "+sc+"Video: "+ec+sc5+quality+ec5
        plugintools.addPeli(action=server,url=url_vid,title=titlefull,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)


################################################### Herramientas #################################################

def inkapelis_genr(genrfull):
    
    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    elif len(genrfull) >5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    else: genrfull = 'N/D' 
    return genrfull

######################################### @ By Aquilesserr PalcoTv Team #########################################  
    