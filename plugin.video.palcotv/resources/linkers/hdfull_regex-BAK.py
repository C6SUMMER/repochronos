# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de HDfull.tv para PalcoTV
# Fecha de creación (13/03/2016)
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
version = " [0.1]"

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
    #plugintools.add_item(action="",url="",title=sc+"Género: "+ec+sc3+str(genr)+ec3+sc+"  imdb: "+ec+sc3+punt_imdb+ec3,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    #plugintools.add_item(action="",url="",title=sc+"Año: "+ec+sc3+year+ec3+"  "+sc+"Duracion: "+ec+sc3+durac+ec3,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    #plugintools.add_item(action="",url="",title=sc5+"Enlaces disponibles"+ec5,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)

    bloq_film = plugintools.find_single_match(data,'<div class="row-pages-wrapper">(.*?)<div id="link_list"')
    film =plugintools.find_multiple_matches(bloq_film,'<div class="embed-selector"(.*?)<div class="embed-movie">')
    for item in film:
        lang = plugintools.find_single_match(item,'Idioma:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","").replace('&ntilde;','ñ')
        lang = lang.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
        lang = lang.replace('Audio','').replace('Español','Esp').replace('Latino','Lat').replace('Subtítulo','Sub -').replace('Original','V.O')

        serverfull = plugintools.find_single_match(item,'class="provider" style="background-image: url\(.*?\)">([^<]+)</b>')
        quality = plugintools.find_single_match(item,'Calidad:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","")
        id_vid = plugintools.find_single_match(item,'onclick="reportMovie\((.*?)\)')
        url_vid = plugintools.find_single_match(item,'<a href="javascript.*?<a href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = sc+server.title()+ec+" "+sc2+" ["+lang.strip()+"] "+ec2+" "+sc+"Video: "+ec+sc5+quality+ec5
        plugintools.addPeli(action=server,url=url_vid,title=titlefull,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
    
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
    #plugintools.add_item(action="",url="",title=sc+"Género: "+ec+sc3+str(genr)+ec3+sc+"  imdb: "+ec+sc3+punt_imdb+ec3,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    #plugintools.add_item(action="",url="",title=sc+"Año: "+ec+sc3+year+ec3+"  "+sc+"Duracion: "+ec+sc3+durac+ec3,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    #plugintools.add_item(action="",url="",title=sc+"Director: "+ec+sc3+direct+ec3,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
    #plugintools.add_item(action="",url="",title=sc5+n_temp+" Temporadas disponibles"+ec5,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)

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

        serverfull = plugintools.find_single_match(item,'class="provider" style="background-image: url\(.*?\)">([^<]+)</b>')
        quality = plugintools.find_single_match(item,'Calidad:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","")
        id_vid = plugintools.find_single_match(item,'onclick="reportMovie\((.*?)\)')
        url_vid = plugintools.find_single_match(item,'<a href="javascript.*?<a href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = sc+server.title()+ec+" "+sc2+" ["+lang.strip()+"] "+ec2+" "+sc+"Video: "+ec+sc5+quality+ec5
        plugintools.addPeli(action=server,url=url_vid,title=titlefull,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        

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