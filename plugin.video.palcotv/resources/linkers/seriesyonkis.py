# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de SeriesYonkis para PalcoTV
# Version 0.2 (01.04.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de pelisalacarta de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys

import plugintools
from resources.tools.resolvers import *
from resources.tools.bers_sy import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'https://www.cubbyusercontent.com/pl/seriesyonkis_logo.png/_1490091a06d847b4b5fae1c8d3d990e1'
fanart = 'https://www.cubbyusercontent.com/pl/seriesyonkis_fondo1.jpg/_28de253510514830a245d8fef18ddff8'
referer = 'http://www.seriesyonkis.sx/'

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.2]"


def serieyonkis_linker0(params):
    plugintools.log('[%s %s] Linker SeriesYonkis %s' % (addonName, addonVersion, repr(params)))
    
    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesYonkis"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    bers_sy_on = plugintools.get_setting("bers_sy_on")
    bers_sy_level = plugintools.get_setting("bers_sy_level")
    plugintools.log("bers_sy_on= "+bers_sy_on)
    plugintools.log("bers_sy_level= "+bers_sy_level)
	
    if bers_sy_on == "true" and bers_sy_level == "1":  # Control para ejecutar el BERS para toda la serie
        bers_sy0(params)
    else:    
        datamovie={}
        if params.get("plot") != "":
                datamovie["Plot"]=params.get("plot")  # Cargamos sinopsis de la serie... (si existe)
        else:
                datamovie["Plot"]="."
       
        url = params.get("url")
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        request_headers.append(["Referer", referer])
        data,response_headers = plugintools.read_body_and_headers(url,headers=request_headers)

        title = plugintools.find_single_match(data,'<h1 class="underline" title="(.*?)\(').strip()
        year = plugintools.find_single_match(data,'<h1 class="underline" title=".*?\((.*?)\)').strip()
        if year =="": year = 'N/D'
        punt = plugintools.find_single_match(data,'<div class="rating">\s+<p>(.*?)</p>').strip().replace('\n','').replace('\t','')
        if punt =="": punt = 'N/D'
        n_temp = plugintools.find_single_match(data,'id="votes">\s+<p>\s+([0-9]+).*?<span id="votes_value">').strip().replace('\n','').replace('\t','').replace('|','')
        if n_temp =="": n_temp = 'N/D'
        sinopsis = plugintools.find_single_match(data,'<p style=";">(.*?)</p>').strip()
        if sinopsis =="": sinopsis = 'N/D'

        logo = plugintools.find_single_match(data, '<img src="([^"]+)"')
        print logo

        datamovie = {
        'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(n_temp)+', '+ec,
        'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt)+', '+ec,
        'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+'[CR]'+ec,
        'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
        datamovie["plot"]=datamovie["season"]+datamovie["rating"]+datamovie["year"]+datamovie["sinopsis"]

        plugintools.add_item(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
        #plugintools.add_item(action="",url="",title=sc+"Año: "+ec+sc3+year+ec3+"  "+sc+"  Puntuación SeriesYonkis: "+ec+sc3+punt+ec3,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        #plugintools.add_item(action="",url="",title=sc5+n_temp+" Temporadas disponibles"+ec5,thumbnail=logo,fanart=fanart,folder=False,isPlayable=False)
        
        bloq_temp = plugintools.find_single_match(data,'<div id="section-content">(.*?)</ul>')
        temps = plugintools.find_multiple_matches(bloq_temp,'<h3 class="season"(.*?)</li>')
        for item in temps:
            name_temp = plugintools.find_single_match(item,'<strong class="season_title">(.*?)</strong>').strip()
            plugintools.addPeli(action="",url="",title=sc2+'-- '+name_temp+' --'+ec2,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=False,isPlayable=False)
            capis = plugintools.find_multiple_matches(item,'<td class="episode-title">(.*?)</td>')
            for entri in capis:
                
                url_cap = plugintools.find_single_match(entri,'href="([^"]+)')
                url_cap = 'http://www.seriesyonkis.sx'+url_cap
                
                num_cap = plugintools.find_single_match(entri,'<strong>(.*?)</strong>')
                num_cap = num_cap.strip()
                
                title_cap = plugintools.find_single_match(entri,'</strong>(.*?)</a>')
                title_cap = title_cap.strip()
                
                title_capi = sc+num_cap+title_cap+ec.strip()
                title_fixed = num_cap + title_cap
                title_fixed = title_fixed.strip()
                plugintools.addPeli(action="enlaces_capi_linker",title=title_capi,url=url_cap,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=True,extra=title_fixed,isPlayable=False)
        
def enlaces_capi_linker(params):
    plugintools.log('[%s %s] Linker SeriesYonkis %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesYonkis"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    datamovie = {}
    datamovie["Plot"] = params.get("plot")

    url = params.get("url")
    title_fixed = params.get("extra")
    referer = 'http://www.seriesyonkis.sx/'
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer]) 

    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)   
    
    matches = plugintools.find_single_match(data,'<h2 class="header-subtitle veronline">(.*?)</table>')
    match_veronline = plugintools.find_single_match(matches, '<tbody>(.*?)</tbody>')
    match_links = plugintools.find_multiple_matches(match_veronline, '<tr>(.*?)</tr>')
    for entry in match_links:
        title_url = plugintools.find_single_match(entry,'title="([^"]+)')
        page_url = plugintools.find_single_match(entry,'<a href="([^"]+)')
        name_server = plugintools.find_single_match(entry,'watch via([^"]+)')
        idioma_capi = plugintools.find_single_match(entry,'<span class="flags(.*?)</span></td>')
        idioma_capi_fixed = idioma_capi.split(">")

        if len(idioma_capi_fixed) >= 2: idioma_capi = idioma_capi_fixed[1]
        if idioma_capi == "English": idioma_capi = ' [ENG]'
        elif idioma_capi == "english": idioma_capi = ' [ENG]'            
        elif idioma_capi == "Español": idioma_capi = ' [ESP]'
        elif idioma_capi == "Latino": idioma_capi = ' [LAT]'
        elif idioma_capi.find("English-Spanish SUBS") >= 0: idioma_capi = ' [VOSE]'
        elif idioma_capi.find("Japanese-Spanish SUBS") >= 0: idioma_capi = ' [VOSE]'
        else: idioma_capi = " [N/D]"
                     
        plot = datamovie["Plot"]
        source_web="seriesyonkis"
        bers_sy_on = plugintools.get_setting("bers_sy_on")  # Control para activar BERS para el capítulo

        page_url = 'http://www.seriesyonkis.sx'+page_url
        server = video_analyzer(name_server)
        img_server = plugintools.find_single_match(entry,'<img height="35" src="([^"]+)"')
        if img_server =="":
            img_server = thumbnail
        title = sc+title_fixed+ec+sc2+' [I]'+idioma_capi+ec2+sc5+'[/I]  [I]['+server+'][/I]'+ec5

        plugintools.add_item(action="getlink_linker",title=title,url=page_url,thumbnail=img_server,info_labels=datamovie,fanart=fanart,folder=False,isPlayable=True)
        if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)

        
def getlink_linker(params):
    plugintools.log('[%s %s] Linker SeriesYonkis %s' % (addonName, addonVersion, repr(params)))  

    page_url = params.get("url")

    referer = 'http://www.seriesyonkis.sx/'
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    data,response_headers = plugintools.read_body_and_headers(page_url, headers=request_headers)   
    match = plugintools.find_single_match(data,'<table class="episodes full-width">(.*?)</table>')
    url_final = plugintools.find_single_match(match,'<a class="link p2" href="([^"]+)')
    print url_final
    
    if url_final.find("allmyvideos") >= 0: params["url"]=url_final; allmyvideos(params)
    elif url_final.find("streamcloud") >= 0: params["url"]=url_final; streamcloud(params)
    elif url_final.find("played.to") >= 0: params["url"]=url_final; playedto(params)
    elif url_final.find("vidspot") >= 0: params["url"]=url_final; vidspot(params)
    elif url_final.find("vk") >= 0: params["url"]=url_final; vk(params)
    elif url_final.find("nowvideo.sx") >= 0: params["url"]=url_final; nowvideo(params)
    elif url_final.find("tumi.tv") >= 0: params["url"]=url_final; tumi(params)
    elif url_final.find("veehd") >= 0: params["url"]=url_final; veehd(params)
    elif url_final.find("turbovideos.net") >= 0: params["url"]=url_final; turbovideos(params)       
    elif url_final.find("streamin.to") >= 0: params["url"]=url_final; streaminto(params)
    elif url_final.find("powvideo") >= 0: params["url"]=url_final; powvideo(params)
    elif url_final.find("mail.ru") >= 0: params["url"]=url_final; mailru(params)
    elif url_final.find("mediafire") >= 0: params["url"]=url_final; mediafire(params)
    elif url_final.find("novamov") >= 0: params["url"]=url_final; novamov(params)
    elif url_final.find("gamovideo") >= 0: params["url"]=url_final; gamovideo(params)
    elif url_final.find("moevideos") >= 0: params["url"]=url_final; moevideos(params)
    elif url_final.find("movshare") >= 0: params["url"]=url_final; movshare(params)
    elif url_final.find("movreel") >= 0: params["url"]=url_final; movreel(params)
    elif url_final.find("videobam") >= 0: params["url"]=url_final; videobam(params)    
    elif url_final.find("vimeo") >= 0: params["url"]=url_final; vimeo(params)
    elif url_final.find("veetle") >= 0: params["url"]=url_final; veetle(params)
    elif url_final.find("videoweed") >= 0: params["url"]=url_final; videoweed(params)
    elif url_final.find("streamable") >= 0: params["url"]=url_final; streamable(params)
    elif url_final.find("rocvideo") >= 0: params["url"]=url_final; rocvideo(params)
    elif url_final.find("realvid") >= 0: params["url"]=url_final; realvid(params)
    elif url_final.find("netu") >= 0: params["url"]=url_final; netu(params)
    elif url_final.find("waaw") >= 0: params["url"]=url_final; waaw(params)
    elif url_final.find("videomega") >= 0: params["url"]=url_final; videomega(params)
    elif url_final.find("video.tt") >= 0: params["url"]=url_final; videott(params)
    elif url_final.find("flashx.tv") >= 0: params["url"]=url_final; flashx(params)
    elif url_final.find("ok.ru") >= 0: params["url"]=url_final; okru(params)
    elif url_final.find("vidto.me") >= 0: params["url"]=url_final; vidtome(params)
    elif url_final.find("playwire") >= 0: params["url"]=url_final; playwire(params)
    elif url_final.find("uptostream.com") >= 0: params["url"]=url_final; uptostream(params)
    elif url_final.find("youwatch") >= 0: params["url"]=url_final; youwatch(params)
    elif url_final.find("vidgg.to") >= 0: params["url"]=url_final; vidggto(params)
    elif url_final.find("vimple.ru") >= 0: params["url"]=url_final; vimple(params)
    elif url_final.find("idowatch.net") >= 0: params["url"]=url_final; idowatch(params)
    elif url_final.find("cloudtime.to") >= 0: params["url"]=url_final; cloudtime(params)
    elif url_final.find("vidzi.tv") >= 0: params["url"]=url_final; vidzitv(params)
    elif url_final.find("vodlocker") >= 0: params["url"]=url_final; vodlocker(params)
    elif url_final.find("streame.net") >= 0: params["url"]=url_final; streamenet(params)
    elif url_final.find("watchonline") >= 0: params["url"]=url_final; watchonline(params)
    elif url_final.find("allvid") >= 0: params["url"]=url_final; allvid(params)
    elif url_final.find("streamplay") >= 0: params["url"]=url_final; streamplay(params)
    elif url_final.find("myvideoz") >= 0: params["url"]=url_final; myvideoz(params)
    elif url_final.find("streamplay.to") >= 0: params["url"]=url_final; streamplay(params)
    elif url_final.find("watchonline") >= 0: params["url"]=url_final; watchonline(params)
    elif url_final.find("rutube.ru") >= 0: params["url"]=url_final; rutube(params)
    elif url_final.find("dailymotion") >= 0: params["url"]=url_final; dailymotion(params)
    elif url_final.find("auroravid") >= 0: params["url"]=url_final; auroravid(params)
    elif url_final.find("wholecloud.net") >= 0: params["url"]=url_final; wholecloud(params)
    elif url_final.find("bitvid.sx") >= 0: params["url"]=url_final; bitvid(params)
    elif url_final.find("spruto.tv") >= 0: params["url"]=url_final; spruto(params)
    elif url_final.find("stormo.tv") >= 0: params["url"]=url_final; stormo(params)
    elif url_final.find("myvi.ru") >= 0: params["url"]=url_final; myviru(params)
    elif url_final.find("youtube.com") >= 0: params["url"]=url_final; youtube(params)
    elif url_final.find("filmon.com") >= 0: params["url"]=url_final; filmon(params)
    elif url_final.find("thevideo.me") >= 0: params["url"]=url_final; thevideome(params)
    elif url_final.find("videowood.tv") >= 0: params["url"]=url_final; videowood(params)
    elif url_final.find("neodrive.co") >= 0: params["url"]=url_final; neodrive(params)
    elif url_final.find("thevideobee.to") >= 0: params["url"]=url_final; thevideobee(params)
    elif url_final.find("fileshow.tv") >= 0: params["url"]=url_final; fileshow(params)
    elif url_final.find("vid.ag") >= 0: params["url"]=url_final; vid(params)
    elif url_final.find("vidxtreme.to") >= 0: params["url"]=url_final; vidxtreme(params)
    elif url_final.find("vidup") >= 0: params["url"]=url_final; vidup(params)
    elif url_final.find("watchvideo") >= 0: params["url"]=url_final; watchvideo(params)
    elif url_final.find("speedvid") >= 0: params["url"]=url_final; speedvid(params)
    elif url_final.find("chefti.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("vodbeast") >= 0: params["url"]=url_final; vodbeast(params)
    elif url_final.find("nosvideo") >= 0: params["url"]=url_final; nosvideo(params)
    elif url_final.find("noslocker") >= 0: params["url"]=url_final; noslocker(params)
    elif url_final.find("up2stream") >= 0: params["url"]=url_final; up2stream(params)

    
############################################# By PalcoTv Team ####################################################