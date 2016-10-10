# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker HDfull.tv para PalcoTV
# Fecha de creación (30/07/2016)
# Autor By Aquilesserr
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)

import urlparse,urllib2,urllib,re
import os, sys

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import requests

import traceback
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

web = "http://hdfull.tv"
referer = "http://hdfull.tv/"
fanart = 'https://www.cubbyusercontent.com/pl/hdfull_fanart.png/_3f045d37290740d084bb24b233cc04de'
thumbnail = 'https://www.cubbyusercontent.com/pl/hdfull_logo.png/_9e1e67a167034c32badf466dd2ab1d91'

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.2]"

def hdfull_linker0(params):
    plugintools.log("[%s %s] Linker HDfull.tv %s" % (addonName, addonVersion, repr(params)))

    page_url = params.get("page")
    plugintools.log("URL= "+page_url)

    if 'pelicula' in page_url:
        params['url']=page_url
        hd_peli_linker(params)
    if 'serie' in page_url:
        params['url']=page_url
        hd_serietemp_linker(params)

# Peliculas -------------------------->>

def hd_peli_linker(params):
    plugintools.log("[%s %s] Linker HDfull.tv %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker HDfull"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    url = params.get("url")
    r = requests.get(url)
    data = r.content

    fondo = plugintools.find_single_match(data,'<div style="background-image:url\(([^)]+)\)').strip()
    if "walter.trakt.us" in fondo: fondo = fanart 
    logo = plugintools.find_single_match(data,'<img itemprop="image" src="([^"]+)"')
    if logo =="": logo = thumbnail  
    title = plugintools.find_single_match(data,'<div id="summary-title" itemprop="name">([^<]+)</div>').upper()
    punt_imdb = plugintools.find_single_match(data,'<meta itemprop="ratingValue" content="([^"]+)"')
    if punt_imdb =="": punt_imdb = 'N/D'
    year = plugintools.find_single_match(data,'<p><span>A&ntilde;o: </span>\s+<a href="http://hdfull.tv/buscar/year/(.*?)">')
    if year =="": year = 'N/D'
    direct = plugintools.find_single_match(data,'<span>Director:</span>.*?<span itemprop="name">([^<]+)</span></a>')
    if direct =="": direct = 'N/D'
    id_imdb = plugintools.find_single_match(data,'<a href="http://www.imdb.com/title/(.*?)"')

    durac = imdb_time(id_imdb)
    genr = imdb_genr(id_imdb)

    sinopsis = plugintools.find_single_match(data,'itemprop="description">(.*?)<br />').strip().replace('\n','')

    datamovie = {
    'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt_imdb)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]+datamovie["sinopsis"]
    
    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  

    bloq_film = plugintools.find_single_match(data,'<div class="row-pages-wrapper">(.*?)<div id="link_list"')
    film =plugintools.find_multiple_matches(bloq_film,'<div class="embed-selector"(.*?)<div class="embed-movie">')
    for item in film:
        lang = plugintools.find_single_match(item,'Idioma:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","").replace('&ntilde;','ñ')
        lang = lang.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
        lang = lang.replace('Audio','').replace('Español','Esp').replace('Latino','Lat').replace('Subtítulo','Sub -').replace('Original','V.O')

        serverfull = plugintools.find_single_match(item,'class="provider" style="background-image: url\(.*?\)">([^<]+)</b>')
        quality = plugintools.find_single_match(item,'Calidad:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","")
        #id_vid = plugintools.find_single_match(item,'onclick="reportMovie\((.*?)\)')
        url_vid = plugintools.find_single_match(item,'<a href="javascript.*?<a href="([^"]+)"')
        #server = video_analyzer(serverfull)
        titlefull = sc+serverfull.title()+ec+" "+sc2+" ["+lang.strip()+"] "+ec2+" "+sc+"Video: "+ec+sc5+quality+ec5
        plugintools.addPeli(action="getlink_hdfull_linker",url=url_vid,title=titlefull,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
    
# Series ----------------------------->>

def hd_serietemp_linker(params):
    plugintools.log("[%s %s] Linker HDfull.tv %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker HDfull"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    url = params.get("url")
    r = requests.get(url)
    data = r.content
    
    fondo = plugintools.find_single_match(data,'<div style="background-image:url\(([^)]+)\)').strip()
    if "walter.trakt.us" in fondo: fondo = fanart  
    logo = plugintools.find_single_match(data,'<div class="show-poster">\s+<img src="([^"]+)"')
    if logo =="": logo = thumbnail  
    title = plugintools.find_single_match(data,'<div id="summary-title" itemprop="name">([^<]+)</div>').upper()
    punt_imdb = plugintools.find_single_match(data,'<meta itemprop="ratingValue" content="([^"]+)"')
    if punt_imdb =="": punt_imdb = 'N/D'
    year = plugintools.find_single_match(data,'<p><span>A&ntilde;o: </span>\s+<a href="http://hdfull.tv/buscar/year/(.*?)">')
    if year =="": year = 'N/D'
    n_temp = plugintools.find_multiple_matches(data,"<li><a href='.*?'>(.*?)</a>");n_temp = n_temp[-1]
    if n_temp =="": direct = 'N/D'
    id_imdb = plugintools.find_single_match(data,'<a href="http://www.imdb.com/title/(.*?)"')
    estado = plugintools.find_single_match(data,'<p><span>Estado: </span>.*?>(.*?)</a>')
    durac = imdb_time(id_imdb)
    genr = imdb_genr(id_imdb)
    sinopsis = plugintools.find_single_match(data,'itemprop="description">(.*?)<br />').strip().replace('\n','')

    datamovie = {
    'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(n_temp)+', '+ec,
    'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt_imdb)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["season"]+datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]+datamovie["sinopsis"]
    
    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5+sc2+"  ("+estado+")"+ec2,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  

    patron_temp = 'itemprop="season"(.*?)</div>'
    item_temp = re.compile(patron_temp,re.DOTALL).findall(data)
    for temp in item_temp:
        url = plugintools.find_single_match(temp,"<a href='([^']+)'")
        img = plugintools.find_single_match(temp,'src="([^"]+)"')
        if img =="": img = logo
        name_temp = plugintools.find_single_match(temp,'itemprop="name">([^<]+)<')
        plugintools.add_item(action="hd_epis_linker",url=url,title=sc2+name_temp+' >>'+ec2,info_labels=datamovie,thumbnail=img,fanart=fondo,folder=True,isPlayable=False)
        
def hd_epis_linker(params):
    plugintools.log("[%s %s] Linker HDfull.tv %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker HDfull"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url")
    fondo =params.get("fanart")
    logo =params.get("thumbnail")
    name_temp = params.get('title').replace('>>','')
    r = requests.get(url)
    data = r.content
    plugintools.addPeli(action="",url="",title=sc2+"-- "+name_temp+" --"+ec2,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)

    post = 'action=season&start=0&limit=0'
    show = plugintools.find_single_match(data,"var sid = '([^']+)")
    season = plugintools.find_single_match(data,"var ssid = '([^']+)")
    params_post = post+'&show='+show+'&season='+season
    url_js = 'http://hdfull.tv/a/episodes'
  
    body,response_headers = plugintools.read_body_and_headers(url_js,post=params_post)
    data_js = json.loads(body)
    try:
        i = 0
        epis = data_js[i]
        for epis in data_js:
            #epis = js[i]
            num_temp = epis['season'].encode('utf8');num_epis = epis['episode'].encode('utf8')
            #img = 'http://hdfull.tv/tthumb/220x124/'+epis['thumbnail']
            id_epis = epis['id']
            title = epis['title']['es'].encode('utf8')
            if title =="":
                title = epis['title']['en'].encode('utf8')
            url = params.get("url")+'/episodio-'+num_epis
            titlefull = str(sc+num_temp+'x'+num_epis+' -- '+title+ec)#+' '+sc2+lang+ec2)
            plugintools.add_item(action="hd_serieserver_linker",url=url,title=titlefull,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
            epis = int(i)+1
    except:
        plugintools.addPeli(action="",url="",title=sc4+'No existen capitulos'+ec4,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)

def hd_serieserver_linker(params):
    plugintools.log("[%s %s] Linker HDfull.tv %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker HDfull"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    url = params.get("url")
    fondo =params.get("fanart")
    logo =params.get("thumbnail")
    r = requests.get(url)
    data = r.content

    punt_imdb = plugintools.find_single_match(data,'<meta itemprop="ratingValue" content="([^"]+)"')
    if punt_imdb =="": punt_imdb = 'N/D'
    year = plugintools.find_single_match(data,'<p><span>A&ntilde;o: </span>\s+<a href="http://hdfull.tv/buscar/year/(.*?)">')
    if year =="": year = 'N/D'
    id_imdb = plugintools.find_single_match(data,'<a href="http://www.imdb.com/title/(.*?)"')
    durac = imdb_time(id_imdb)
    genr = imdb_genr(id_imdb)
    bloq_film = plugintools.find_single_match(data,'<div class="row-pages-wrapper">(.*?)<div id="link_list"')
    film =plugintools.find_multiple_matches(bloq_film,'<div class="embed-selector"(.*?)<div class="embed-movie">')
    for item in film:
        lang = plugintools.find_single_match(item,'Idioma:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","").replace('&ntilde;','ñ')
        lang = lang.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
        lang = lang.replace('Audio','').replace('Español','Esp').replace('Latino','Lat').replace('Subtítulo','Sub -').replace('Original','V.O')
        '''
        serverfull = plugintools.find_single_match(item,'class="provider" style="background-image: url\(.*?\)">([^<]+)</b>')
        quality = plugintools.find_single_match(item,'Calidad:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","")
        id_vid = plugintools.find_single_match(item,'onclick="reportMovie\((.*?)\)')
        url_redir = plugintools.find_single_match(item,'<a href="javascript.*?<a href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = sc+server.title()+ec+" "+sc2+" ["+lang.strip()+"] "+ec2+" "+sc+"Video: "+ec+sc5+quality+ec5
        plugintools.addPeli(action=server,url=url_redir,title=titlefull,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        '''
        serverfull = plugintools.find_single_match(item,'class="provider" style="background-image: url\(.*?\)">([^<]+)</b>')
        quality = plugintools.find_single_match(item,'Calidad:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","")
        #id_vid = plugintools.find_single_match(item,'onclick="reportMovie\((.*?)\)')
        url_vid = plugintools.find_single_match(item,'<a href="javascript.*?<a href="([^"]+)"')
        #server = video_analyzer(serverfull)
        titlefull = sc+serverfull.title()+ec+" "+sc2+" ["+lang.strip()+"] "+ec2+" "+sc+"Video: "+ec+sc5+quality+ec5
        plugintools.addPeli(action="getlink_hdfull_linker",url=url_vid,title=titlefull,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)

def getlink_hdfull_linker(params):
    plugintools.log('[%s %s] Linker HDfull %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {"Host":"hdfull.tv","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0","Referer":"http://hdfull.tv/"}
    r=requests.get(url)
    data = r.content
    url_final = plugintools.find_single_match(data, '<a class="btn btn-large btn-info" href="(.*?)"')
    
    if url_final.find("allmyvideos") >= 0: params["url"]=url_final; allmyvideos(params)
    elif url_final.find("vidspot") >= 0: params["url"]=url_final; vidspot(params)
    elif url_final.find("played.to") >= 0: params["url"]=url_final; playedto(params)
    elif url_final.find("streamin.to") >= 0: params["url"]=url_final; streaminto(params)
    elif url_final.find("streamcloud") >= 0: params["url"]=url_final; streamcloud(params)
    elif url_final.find("nowvideo.sx") >= 0: params["url"]=url_final; nowvideo(params)
    elif url_final.find("veehd") >= 0: params["url"]=url_final; veehd(params)
    elif url_final.find("vk") >= 0: params["url"]=url_final; vk(params)
    elif url_final.find("lidplay") >= 0: params["url"]=url_final; vk(params)
    elif url_final.find("tumi.tv") >= 0: params["url"]=url_final; tumi(params)
    elif url_final.find("novamov") >= 0: params["url"]=url_final; novamov(params)
    elif url_final.find("moevideos") >= 0: params["url"]=url_final; moevideos(params)
    elif url_final.find("gamovideo") >= 0: params["url"]=url_final; gamovideo(params)
    elif url_final.find("movshare") >= 0: params["url"]=url_final; movshare(params)
    elif url_final.find("powvideo") >= 0: params["url"]=url_final; powvideo(params)
    elif url_final.find("mail.ru") >= 0: params["url"]=url_final; mailru(params)
    elif url_final.find("mediafire") >= 0: params["url"]=url_final; mediafire(params)
    elif url_final.find("netu") >= 0: params["url"]=url_final; netu(params)
    elif url_final.find("waaw") >= 0: params["url"]=url_final; waaw(params)
    elif url_final.find("movreel") >= 0: params["url"]=url_final; movreel(params)
    elif url_final.find("videobam") >= 0: params["url"]=url_final; videobam(params)    
    elif url_final.find("vimeo/videos") >= 0: params["url"]=url_final; vimeo(params)
    elif url_final.find("vimeo/channels") >= 0: params["url"]=url_final; vimeo_pl(params)
    elif url_final.find("veetle") >= 0: params["url"]=url_final; veetle(params)
    elif url_final.find("videoweed") >= 0: params["url"]=url_final; videoweed(params)
    elif url_final.find("streamable") >= 0: params["url"]=url_final; streamable(params)
    elif url_final.find("rocvideo") >= 0: params["url"]=url_final; rocvideo(params)
    elif url_final.find("realvid") >= 0: params["url"]=url_final; realvid(params)
    elif url_final.find("videomega") >= 0: params["url"]=url_final; videomega(params)
    elif url_final.find("video.tt") >= 0: params["url"]=url_final; videott(params)
    elif url_final.find("flashx") >= 0: params["url"]=url_final; flashx(params)
    elif url_final.find("openload") >= 0: params["url"]=url_final; openload(params)
    elif url_final.find("turbovideos") >= 0: params["url"]=url_final; turbovideos(params)
    elif url_final.find("ok.ru") >= 0: params["url"]=url_final; okru(params)
    elif url_final.find("vidto.me") >= 0: params["url"]=url_final; vidtome(params)
    elif url_final.find("playwire") >= 0: params["url"]=url_final; playwire(params)
    elif url_final.find("copiapop") >= 0: params["url"]=url_final; copiapop(params)
    elif url_final.find("vimple.ru") >= 0: params["url"]=url_final; vimple(params)
    elif url_final.find("vidgg") >= 0: params["url"]=url_final; vidggto(params)
    elif url_final.find("uptostream.com") >= 0: params["url"]=url_final; uptostream(params)
    elif url_final.find("youwatch") >= 0: params["url"]=url_final; youwatch(params)
    elif url_final.find("idowatch") >= 0: params["url"]=url_final; idowatch(params)
    elif url_final.find("cloudtime") >= 0: params["url"]=url_final; cloudtime(params)
    elif url_final.find("allvid") >= 0: params["url"]=url_final; allvid(params)
    elif url_final.find("vodlocker") >= 0: params["url"]=url_final; vodlocker(params)
    elif url_final.find("vidzi.tv") >= 0: params["url"]=url_final; vidzitv(params)
    elif url_final.find("streame.net") >= 0: params["url"]=url_final; streamenet(params)
    elif url_final.find("myvideoz") >= 0: params["url"]=url_final; myvideoz(params)
    elif url_final.find("streamplay") >= 0: params["url"]=url_final; streamplay(params)
    elif url_final.find("watchonline") >= 0: params["url"]=url_final; watchonline(params)
    elif url_final.find("rutube") >= 0: params["url"]=url_final; rutube(params)
    elif url_final.find("dailymotion") >= 0: params["url"]=url_final; dailymotion(params)
    elif url_final.find("auroravid") >= 0: params["url"]=url_final; auroravid(params)
    elif url_final.find("wholecloud") >= 0: params["url"]=url_final; wholecloud(params)
    elif url_final.find("bitvid") >= 0: params["url"]=url_final; bitvid(params)
    elif url_final.find("spruto") >= 0: params["url"]=url_final; spruto(params)
    elif url_final.find("stormo") >= 0: params["url"]=url_final; stormo(params)
    elif url_final.find("myvi.ru") >= 0: params["url"]=url_final; myviru(params)
    elif url_final.find("youtube.com") >= 0: params["url"]=url_final; youtube(params)
    elif url_final.find("filmon.com") >= 0: params["url"]=url_final; filmon(params)
    elif url_final.find("thevideo.me") >= 0: params["url"]=url_final; thevideome(params)
    elif url_final.find("videowood.tv") >= 0: params["url"]=url_final; videowood(params)
    elif url_final.find("neodrive.co") >= 0: params["url"]=url_final; neodrive(params)
    elif url_final.find("cloudzilla") >= 0: params["url"]=url_final; cloudzilla(params)
    elif url_final.find("thevideobee.to") >= 0: params["url"]=url_final; thevideobee(params)
    elif url_final.find("fileshow.tv") >= 0: params["url"]=url_final; fileshow(params)
    elif url_final.find("vid.ag") >= 0: params["url"]=url_final; vid(params)
    elif url_final.find("vidxtreme.to") >= 0: params["url"]=url_final; vidxtreme(params)
    elif url_final.find("vidup") >= 0: params["url"]=url_final; vidup(params)
    elif url_final.find("watchvideo") >= 0: params["url"]=url_final; watchvideo(params)
    elif url_final.find("speedvid") >= 0: params["url"]=url_final; speedvid(params)
    elif url_final.find("chefti.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("ajihezo.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("bojem3a.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("vodbeast") >= 0: params["url"]=url_final; vodbeast(params)
    elif url_final.find("nosvideo") >= 0: params["url"]=url_final; nosvideo(params)
    elif url_final.find("noslocker") >= 0: params["url"]=url_final; noslocker(params)
    elif url_final.find("up2stream") >= 0: params["url"]=url_final; up2stream(params)
    elif url_final.find("diskokosmiko") >= 0: params["url"]=url_final; diskokosmiko(params)
    elif url_final.find("smartvid") >= 0: params["url"]=url_final; smartvid(params)
    elif url_final.find("greevid") >= 0: params["url"]=url_final; greevid(params)
    elif url_final.find("letwatch") >= 0: params["url"]=url_final; letwatch(params)
    elif url_final.find("yourupload") >= 0: params["url"]=url_final; yourupload(params)
    elif url_final.find("zalaa") >= 0: params["url"]=url_final; zalaa(params)
    elif url_final.find("uploadc") >= 0: params["url"]=url_final; uploadc(params)
    elif url_final.find("mp4upload") >= 0: params["url"]=url_final; mp4upload(params)
    elif url_final.find("rapidvideo") >= 0: params["url"]=url_final; rapidvideo(params)
    elif url_final.find("yourvideohost") >= 0: params["url"]=url_final; yourvideohost(params)
    elif url_final.find("watchers") >= 0: params["url"]=url_final; watchers(params)
    elif url_final.find("vidtodo") >= 0: params["url"]=url_final; vidtodo(params)
    elif url_final.find("izanagi") >= 0: params["url"]=url_final; izanagi(params)
    elif url_final.find("yotta") >= 0: params["url"]=url_final; yotta(params)
    elif url_final.find("kami") >= 0: params["url"]=url_final; kami(params)
    elif url_final.find("touchfile") >= 0: params["url"]=url_final; touchfile(params)
    elif url_final.find("zstream") >= 0: params["url"]=url_final; zstream(params)
    elif url_final.find("vodlock") >= 0: params["url"]=url_final; vodlock(params)
    elif url_final.find("goodvideohost") >= 0: params["url"]=url_final; goodvideohost(params)
        

################################################### Herramientas #################################################

def imdb_time(id_imdb):
    url = 'http://www.imdb.com/title/'+id_imdb
    r = requests.get(url)
    data = r.content

    es_serie = plugintools.find_single_match(data,'<div class="bp_heading">([^<]+)</div>') #es una serie
    if 'Episode Guide' in es_serie:
        time_h = plugintools.find_single_match(data,'<time itemprop="duration" datetime=".*?">(.*?)</time>').strip().replace("\n","").replace("\t","")
        number_epis = plugintools.find_single_match(data,'<span class="bp_sub_heading">(.*?)</span>').strip().replace("\n","").replace("\t","").replace('episodes','Episodios')
        timefull = time_h+" ("+number_epis+")"
    else:
        time_h = plugintools.find_single_match(data,'<time itemprop="duration" datetime=".*?">(.*?)</time>').strip().replace("\n","").replace("\t","")
        time_m = plugintools.find_single_match(data,'Runtime:</h4>.*?<time itemprop="duration" datetime=".*?">(.*?)</time>').strip().replace("\n","").replace("\t","")
        if time_h =="": time_h = 'N/D'
        if time_m =="": time_m = 'N/D'
        timefull = time_h+" ("+time_m+")"
    return timefull

def imdb_genr(id_imdb):
    url = 'http://www.imdb.com/title/'+id_imdb
    r = requests.get(url)
    data = r.content

    patron = '<span class="itemprop" itemprop="genre">(.*?)</span></a>'
    genr = re.compile(patron,re.DOTALL).findall(data)
    
    if len(genr) ==5: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]+', '+genr[4]
    elif len(genr) ==4: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]
    elif len(genr) ==3: genr = genr[0]+', '+genr[1]+', '+genr[2]
    elif len(genr) ==2: genr = genr[0]+', '+genr[1]
    elif len(genr) ==1: genr = genr[0]
    return genr

######################################### @ By Aquilesserr PalcoTv Team #########################################    