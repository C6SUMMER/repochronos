# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de Danko.com para PalcoTV
# Version 0.1 (13/05/2016)
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

thumbnail = "https://www.cubbyusercontent.com/pl/Danko_logo.png/_a2753887a7654c938989f6b89cfa7764"
fanart = "https://www.cubbyusercontent.com/pl/Danko_fondo.jpg/_de99958ad9de4fe98f876afe69839cd0"
sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.1]"

web_pel = "http://pelisdanko.com/"
referer_pel = "http://pelisdanko.com/"
web_ser = "http://seriesdanko.com/"
referer_ser = "http://seriesdanko.com/"

def danko_linker0(params):
    plugintools.log("[%s %s] Linker Series/PelisDanko %s" % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    plugintools.log("URL= "+page_url)

    if 'peli' in page_url:
        params['url']=page_url
        danko_peli_linker(params)
    if 'serie' in page_url:
        params['url']=page_url
        danko_serie_linker(params)

def danko_peli_linker(params):
    plugintools.log("[%s %s] Linker PelisDanko %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker PelisDanko"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url")
    r = requests.get(url)
    data = r.content
    cookie_ses = r.cookies['pelisdanko_session'] #cookie de la sesion
    
    fondo = plugintools.find_single_match(data,'(http://pelisdanko.com/img/movie.backdrops/w396/.*?\.jpg)').strip()
    #if "walter.trakt.us" in fondo: fondo = fanart 
    logo = plugintools.find_single_match(data,'<img class="img-responsive poster" src="([^"]+)"')
    if logo =="": logo = thumbnail 

    title = plugintools.find_single_match(data,'<dt>T&iacute;tulo</dt> <dd>([^<]+)</dd>').upper()
    
    year = plugintools.find_single_match(data,'<dt>Estreno</dt> <dd>([^<]+)</dd>')
    if year =="": year = 'N/D'

    country = plugintools.find_single_match(data,'<span class="label label-success">([^<]+)</span></h4>')
    if country =="": country = 'N/D'

    genrfull = plugintools.find_multiple_matches(data,'<span class="label label-info">([^<]+)</span></h4>')
    genr = danko_genr(genrfull)

    sinopsis = plugintools.find_single_match(data,'<dt>Sinopsis</dt> <dd class="text-justify">(.*?)</dd>').strip()

    datamovie = {
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'country': sc3+'[B]País: [/B]'+ec3+sc+str(country)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["genre"]+datamovie["year"]+datamovie["country"]+datamovie["sinopsis"]
    
    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    bloq_film = plugintools.find_single_match(data,'<h3 class="coolfont">Streaming</h3>(.*?)</tbody>')
    film =plugintools.find_multiple_matches(bloq_film,'<tr class="rip hover"(.*?)</tr>')
    for item in film:
        langfull = plugintools.find_multiple_matches(item,'src="http://pelisdanko.com/img/flags/(.*?).png')
        lang = danko_lang(langfull)
        id_vid = plugintools.find_single_match(item,'data-id="([^"]+)"') #id del video
        slug1 = plugintools.find_single_match(item,'data-slug="([^"]+)"')#slug del video
        
        url_slug1 = params.get("url")+'/'+slug1+'/ss?#ss' #http://pelisdanko.com/peli/deadpool-5233/7V9gGJlcbE1vi7TJ10697/ss?#ss

        #Preparando parametros para danko_slug,cookie, id_video, slug1
        params_danko_slug = cookie_ses+'|'+id_vid+'|'+slug1

        quality = plugintools.find_single_match(item,'quality-.*?">([^<]+)</span>').strip()
        titlefull = sc+"  Audio: "+ec+sc2+lang+ec2+sc+"  Video: "+ec+" "+sc5+'[I]['+quality+'][/I]'+ec5
        plugintools.addPeli(action='danko_slug',url=url_slug1,title=titlefull,info_labels=datamovie,extra=params_danko_slug,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
    	

def danko_slug(params):
    plugintools.log("[%s %s] Linker Danko %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Danko"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    params_danko_slug = params.get("extra").split('|') #separando los parametros
    cookie_ses = params_danko_slug[0];id_vid = params_danko_slug[1];slug1 = params_danko_slug[-1]

    title = params.get("title");logo = params.get("thumbnail");fondo = params.get("fanart")
    
    headers = {'Host': 'pelisdanko.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Referer': params.get("url"),'pelisdanko_session':cookie_ses}
    
    url = params.get("url") #http://pelisdanko.com/peli/deadpool-5233/7V9gGJlcbE1vi7TJ10697/ss?#ss
    r = requests.get(url,headers=headers)
    data = r.content
    
    title_pel = plugintools.find_single_match(data,'<meta itemprop="name" content="([^"]+)').strip()
    plugintools.add_item(action="",url="",title=title,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    streaming = plugintools.find_single_match(data,'<h3 class="coolfont">Streaming</h3>(.*?)</iframe>')
    if streaming !="":
        url_streaming = plugintools.find_single_match(streaming,'src="([^"]+)"')
        server = video_analyzer(streaming)
        titlefull = sc+'1. '+title_pel+ec+sc5+' [I]['+server+'][/I]'+ec5
        plugintools.addPeli(action=server,url=url_streaming,title=titlefull,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
    else: pass
    
    bloq_slug2 = plugintools.find_single_match(data,'class="lnks"><div class="text-center">(.*?)">Mostrar enlaces</span></a>')
    slug2 = plugintools.find_single_match(bloq_slug2,'data-slug="([^"]+)"')
    
    headers = {'Host': 'pelisdanko.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Referer': url,'pelisdanko_session':cookie_ses}
    #http://pelisdanko.com/strms/5233/7V9gGJlcbE1vi7TJ10697/VLr9dzBnPx9A8l8r10697
    
    url = 'http://pelisdanko.com/strms/'+id_vid+'/'+slug1+'/'+slug2
    r = requests.post(url,headers=headers)
    data = r.content

    bloq_server = plugintools.find_multiple_matches(data,'<tr>(.*?)</tr>')
    i=2
    for item in bloq_server:
        url_vid = plugintools.find_single_match(item,'<a href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = sc+str(i)+'. '+title_pel+ec+sc5+' [I]['+server+'][/I]'+ec5 
        plugintools.addPeli(action=server,url=url_vid,title=titlefull,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        i=i+1

def danko_serie_linker(params):
    plugintools.log("[%s %s] Linker Danko %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesDanko"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    url = params.get("url")
    r = requests.get(url)
    data = r.content
    title = plugintools.find_single_match(data,'<meta property="og:title" content="([^"]+)"')
    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    num_temp = plugintools.find_multiple_matches(data,'<div id="T([0-9]*)" style="display:none">')
    bloq_temp = plugintools.find_multiple_matches(data,'<div id="(T[0-9]*)" style="display:none">(.*?)toggle\(\'slow\'\);')
    print bloq_temp
    for item in bloq_temp:
        name_temp = item[0].replace('T','Temporada ')
        img = plugintools.find_single_match(item[1],"<img src='([^']+)'")
        if img =="": img = thumbnail
        plugintools.add_item(action="",url="",title=sc2+'-- '+name_temp+' --'+ec2,thumbnail=img,fanart=fanart,folder=False,isPlayable=False)
        episfull = plugintools.find_multiple_matches(item[1],'<br><br><a(.*?)<img src=')
        for item in episfull:
            url_epis = plugintools.find_single_match(item,"href='([^']+)'")
            url = 'http://seriesdanko.com/'+url_epis
            title_epis = plugintools.find_single_match(item,"href='.*?>(.*?)</a>")
            plugintools.add_item(action="danko_serieserver_linker",url=url,title=sc+str(title_epis)+ec,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)

def danko_serieserver_linker(params):
    plugintools.log("[%s %s] Linker Danko %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesDanko"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    url = params.get("url")
    title_epis = params.get("title")
    logo = params.get("thumbnail")

    plugintools.add_item(action="",url="",title=sc2+'[B]-- '+title_epis.replace(sc,sc2).replace(ec,ec2)+' --[/B]'+ec2,thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)
    r = requests.get(url)
    data = r.content

    bloq_server = plugintools.find_single_match(data,"<td class='tam13'>Comentario</td></tr>(.*?)<b>Opciones de descarga</b>")
    server = plugintools.find_multiple_matches(bloq_server,"<tr><td class='tam12'>(.*?)</td></tr>")
    for item in server:
        lang = plugintools.find_single_match(item,"<img src='/assets/img/banderas/(.*?).png")
        if lang == 'es': lang = lang.replace('es','ESP')
        elif lang == 'la': lang = lang.replace('la','LAT')
        elif lang == 'vos': lang = lang.replace('vos','SUB-ESP')
        elif lang == 'vo': lang = lang.replace('vo','V.O')

        name_server = plugintools.find_single_match(item,"<img src='/assets/img/servidores/(.*?)\.")
        if 'streamin' in name_server: name_server = 'streamin.to'
         
        url = plugintools.find_single_match(item,"href='([^']+)'")
        url_anonim = 'http://seriesdanko.com/'+url
        server = video_analyzer(name_server)
        title_epis = plugintools.find_single_match(title_epis,'.*?([0-9]*X[0-9]*)')
        titlefull = sc+'Capitulo '+title_epis.replace('X','x')+ec+" "+sc2+" [I]["+lang+"][/I] "+ec2+sc5+' [I]['+server.title()+'][/I]'+ec5
        plugintools.addPeli(action="danko_anonim_linker",url=url_anonim,title=titlefull,thumbnail=logo,fanart=fanart,folder=False,isPlayable=True)

def danko_anonim_linker(params):

    url_anonim = params.get("url")
    r = requests.get(url_anonim)
    data = r.content
    print data
    url_final = plugintools.find_single_match(data,'<h1>Esta saliendo de Seriesdanko.com</h1>.*?<a href="([^"]+)"')
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
    
################################################### Herramientas #################################################

def danko_genr(genrfull):
    
    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    elif len(genrfull) >5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    else: genrfull = 'N/D' 
    return genrfull

def danko_lang(langfull):
    
    if len(langfull) ==5: langfull = '['+langfull[0]+'] ['+langfull[1]+'] ['+langfull[2]+'] ['+langfull[3]+'] ['+langfull[4]+']'
    elif len(langfull) ==4: langfull = '['+langfull[0]+'] ['+langfull[1]+'] ['+langfull[2]+'] ['+langfull[3]+']'
    elif len(langfull) ==3: langfull = '['+langfull[0]+'] ['+langfull[1]+'] ['+langfull[2]+']'
    elif len(langfull) ==2: langfull = '['+langfull[0]+'] ['+langfull[1]+']'
    elif len(langfull) ==1: langfull = '['+langfull[0]+']'
    elif len(langfull) >5: langfull = '['+langfull[0]+'] ['+langfull[1]+'] ['+langfull[2]+'] ['+langfull[3]+'] ['+langfull[4]+']'
    langfull = langfull.replace('ES','ESP').replace('ESP_LAT','LAT').replace('GB','ENG') 	    
    return '[I]'+langfull+'[/I]' 
   
######################################### @ By Aquilesserr PalcoTv Team #########################################
    