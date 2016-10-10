# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker Oranline.com para PalcoTV
# Version 0.4 (30.07.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys,requests
import plugintools
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'https://www.cubbyusercontent.com/pl/oranline_logo1.png/_a3d4af8a72054a33ad96c1f3318ad634'
fanart = 'https://www.cubbyusercontent.com/pl/Oranline_Fondo1.jpg/_fbc8df7ac2934e48a4c66cedda90c0ce'
referer = 'http://www.oranline.com/'

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.5]"

def oranline_linker0(params):
    plugintools.log('[%s %s] Linker Oranline %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    r = requests.get(url, headers=headers)
    data = r.content

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Oranline"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    logo = plugintools.find_single_match(data,'<div class="col-xs-2 poster">.*?<img src="([^"]+)"')
    if logo == "": logo = thumbnail
    info = plugintools.find_single_match(data,'<div id="informacion" class="tab-pane active">(.*?)<div id="produccion" class="tab-pane">')
    fondo = plugintools.find_single_match(info,'<div class="episode-selector-element"><img src="([^"]+)"').replace('w185','original')
    if fondo == "": fondo = fanart
    title = plugintools.find_single_match(info, '<span class="aa">.*?Título.*?</span>.*?<span class="ab">(.*?)</span>').replace('&amp;','').replace('&#8211;','').replace('&#8216;','').replace('&#8217;','')
    if title == "": title = "N/D"
    bloq_genr = plugintools.find_single_match(info,'(<span class="aa">Géneros</span>.*?<span class="ab">.*?</span>)').replace('&amp;','').replace('&#8211;','').replace('&#8216;','').replace('&#8217;','')
    if 'rel="category tag">' in bloq_genr:
        genrfull = plugintools.find_multiple_matches(bloq_genr,'rel="category tag">(.*?)<')
        genr = oranline_genr(genrfull)
    else: genr = "N/D"
    year = plugintools.find_single_match(info,'<span class="aa">Año de lanzamiento</span>.*?<span class="ab">.*?rel="tag">(.*?)<').replace("\t\r\n", "").strip()
    if year =="": year = "N/D"
    durac = plugintools.find_single_match(info,'<span class="aa">Duración</span>.*?<span class="ab">(.*?)</span>').replace('&amp;','').replace('&#8211;','').replace('&#8216;','').replace('&#8217;','')
    if durac == "": durac = "N/D"
    punt = plugintools.find_single_match(info,'<span class="aa">Calificación</span>.*?<span class="ab">(.*?)</span>').replace('&amp;','').replace('&#8211;','').replace('&#8216;','').replace('&#8217;','')
    if punt == "": punt = "N/D"
    
    sinopsis = plugintools.find_single_match(data,'<h2>Sinopsis</h2>.*?<p class="trasnparente">(.*?)</p>').strip()

    datamovie = {
    'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]+datamovie["sinopsis"]

    plugintools.addPeli(action="",title=sc5+"[B]"+title+"[/B]"+ec5,url="",info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    bloque = plugintools.find_single_match(data,'<div id="online">.*?</thead>(.*?)</table>')
    bloque_peli = plugintools.find_multiple_matches(bloque,'<tr>(.*?)</tr>')
    
    i = 1
    for entry in bloque_peli:
        #plugintools.log("entry= "+entry)
        lang_audio = plugintools.find_single_match(entry,'</span></td>\s+<td>([^<]+)</td>').strip()
        if lang_audio =="":
            lang_audio = plugintools.find_single_match(entry,'</span></td><td>([^<]+)</td>').strip()
        formatq = plugintools.find_single_match(entry,'</span></td>\s+<td>[^<]+</td>\s+<td>([^<]+).*?</td>').replace("\t\r\n", "").strip()
        if formatq =="":
            formatq = formatq = plugintools.find_single_match(entry,'</span></td>\<td>[^<]+</td><td>([^<]+).*?</td>')
        server_url = plugintools.find_single_match(entry,'<td><a href="([^"]+)"')
        server = video_analyzer(server_url)
        if server != "":
            titlefull = sc+str(i)+'. '+server.title()+ec+' '+sc2+'[I]['+lang_audio+'][/I]  '+ec2+sc5+'[I]['+formatq+'][/I]'+ec5
            plugintools.addPeli(action=server,url=server_url,title=titlefull,info_labels=datamovie,fanart=fondo,thumbnail=logo,folder=False,isPlayable=True)
        i = i + 1

def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    request_headers.append(["X-Requested-With", "XMLHttpRequest"])
    request_headers.append(["Cookie:","__utma=253162379.286456173.1418323503.1421078750.1422185754.16; __utmz=253162379.1421070671.14.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=http%3A%2F%2Fwww.seriesflv.net%2Fserie%2Fhora-de-aventuras.html; __cfduid=daeed6a2aacaffab2433869fd863162821419890996; __utmb=253162379.4.10.1422185754; __utmc=253162379; __utmt=1"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);print response_headers
    return body

################################################### Herramientas #################################################

def oranline_genr(genrfull):

    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    return genrfull

######################################### @ By Aquilesserr PalcoTv Team ######################################### 


