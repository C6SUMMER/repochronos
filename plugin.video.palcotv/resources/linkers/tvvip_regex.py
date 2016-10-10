# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de TV-vip para PalcoTV
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

web = "http://tv-vip.com/"
referer = "http://tv-vip.com/"
fanart = 'https://www.cubbyusercontent.com/pl/Tvvip_fanart.jpg/_a0c1e65637344710bba76739e644ce88'
thumbnail = 'https://www.cubbyusercontent.com/pl/tvvip_logo.png/_c6c69ac499f94a4fafa38cce8878c6be' 

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.1]"

def tvvip_linker0(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    page_url = params.get("page")
    page_url = page_url.replace('%C3%A1','á').replace('%C3%A9','é').replace('%C3%AD','í').replace('%C3%B1','ñ')
  
    if 'film' in page_url:
        params['url']=page_url
        tvvip_peli(params)
    if 'section' in page_url:
        params['url']=page_url
        tvvip_serie_temp(params)
    
# Peliculas -------------------------->>

def tvvip_peli(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker TV-vip"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    url = params.get("url")
    url = url.replace('film','json/repo')+'index.json'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
    
    r = requests.get(url,headers=headers)
    print r.headers
    if 'refresh' in r.headers:
        time.sleep(int(r.headers['refresh'][:1]))
        url = web + '/' + r.headers['refresh'][7:]
    r = requests.get(url,headers=headers)
    data = r.text.encode('utf8')
    
    data_js = r.text.encode('utf8')
    js = json.loads(data_js)

    logo = params.get("url").replace('film','json/repo')+'poster.jpg'
    fondo = params.get("url").replace('film','json/repo')+'thumbnail.jpg'
    
    title = js['name'].encode('utf8').strip().replace("\n","").replace("\t","")
    title = title.replace('Ã¡','á').replace('Ã©','é').replace('Ã­','í').replace('Ã³','ó').replace('Âº','ú').replace('Ã±','ñ') 

    genr = tvvip_genr(url)
    if genr =="": genr = 'N/D'
    year = js['year'].encode('utf8').strip().replace("\n","").replace("\t","")
    if year =="": year = 'N/D'
    durac = js['durationHuman'].encode('utf8').strip().replace("\n","").replace("\t","")
    if durac =="": durac = 'N/D'
    punt = js['rate'].encode('utf8').strip().replace("\n","").replace("\t","")
    if punt =="": punt = 'N/D'
    sinopsis = js['description'].encode('utf8').strip().replace("\n","").replace("\t","")
    if sinopsis =="": sinopsis = 'N/D'

    lang = tvvip_lang(url)
    subtitle = tvvip_lang_sub(url)

    datamovie = {
    'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+', '+ec,
    'audiochannels': sc3+'[B]Audio: [/B]'+ec3+sc+str(lang)+', '+ec,
    'subtitleslanguage': sc3+'[B]Subtitulos: [/B]'+ec3+sc+str(subtitle)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]+datamovie["audiochannels"]+datamovie["subtitleslanguage"]+datamovie["sinopsis"]
    
    plugintools.add_item(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
    quality_grup = js['profiles']
    for quality in quality_grup.keys():
        quality_max = js['profiles'][quality]['videoResolution'].encode('utf8')
        peso = js['profiles'][quality]['sizeHuman'].encode('utf8')
        #http://hcb.tv-vip.com/transcoder/Dumbo.mp4/240-mp4/Dumbo.mp4.mp4
        try: 
            server1 = js['profiles'][quality]['servers'][0]['url'].encode('utf8')
            if not 's/transcoder' in server1:
                server1 = server1.replace('transcoder','s/transcoder')
            url = server1+js['profiles'][quality]['videoUri'].encode('utf8')
            plugintools.addPeli(action="play",url=url,title=sc+title+' (Serv.1)'+ec+sc2+"  ["+str(quality_max)+"]"+ec2+sc5+" ["+peso+"]"+ec5,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True) 
        except: pass
        
        try:
            server2 = js['profiles'][quality]['servers'][1]['url'].encode('utf8')
            if not 's/transcoder' in server2:
                server2 = server2.replace('transcoder','s/transcoder')  
            url = server2+js['profiles'][quality]['videoUri'].encode('utf8')
            plugintools.addPeli(action="play",url=url,title=sc+title+' (Serv.2)'+ec+sc2+"  ["+str(quality_max)+"]"+ec2+sc5+" ["+peso+"]"+ec5,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)   
        except: pass
        
# Series ----------------------------->>

def tvvip_serie_temp(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker TV-vip"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    url = params.get("url")
    url = url.replace('section','json/playlist')+'/index.json'
    headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
    
    r = requests.get(url,headers=headers)
    
    if 'refresh' in r.headers:
        time.sleep(int(r.headers['refresh'][:1]))
        url = web + '/' + r.headers['refresh'][7:]

    r = requests.get(url,headers=headers)
    data = r.text.encode('utf8')

    data_js = r.text
    js = json.loads(data_js)
    
    logo = params.get("url").replace('section','json/playlist')+'/thumbnail_300x300.jpg'
    fondo = params.get("url").replace('section','json/playlist')+'/background.jpg'

    title = js['name'].encode('utf8').strip().replace("\n","").replace("\t","")
    title = title.replace('Ã¡','á').replace('Ã©','é').replace('Ã­','í').replace('Ã³','ó').replace('Âº','ú').replace('Ã±','ñ') 
    genr = tvvip_genr(url)
    if genr =="": genr = 'N/D'
    year = js['year'].encode('utf8').strip().replace("\n","").replace("\t","")
    if year =="": year = 'N/D'
    durac = js['runtime'].encode('utf8').strip().replace("\n","").replace("\t","")
    if durac =="": durac = 'N/D'
    punt = js['rate'].encode('utf8').strip().replace("\n","").replace("\t","")
    if punt =="": punt = 'N/D'

    lang = tvvip_lang(url)

    n_epis = js['number']
    n_temp = js['numberOfSeasons']

    datamovie = {
    'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(n_temp)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+ec}
    
    datamovie["plot"]=datamovie["season"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]

    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
    try:
        plugintools.add_item(action="",url="",title=sc2+"Extras"+ec2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
        extras = js['sortedRepoChilds']
        i = 0
        epis = js['sortedRepoChilds'][i]
        for epis in extras:
            title = epis['name'].encode('utf8').replace('Ã¡','á').replace('Ã©','é').replace('Ã­','í').replace('Ã³','ó').replace('Âº','ú').replace('Ã±','ñ') 
            durac = epis['runtime']#.encode('utf8')
            if durac =="":
                durac = "N/D"
            url = 'http://tv-vip.com/film/'+epis['id']+'/' # / necesaria para enviar a tvvip_peli
            plugintools.add_item(action="tvvip_peli",url=url,title=sc+title+ec+sc3+" ["+durac+"]"+ec3,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
            epis = int(i)+1
    except: pass
    try:
        tempfull = js['playListChilds']
        i = 0
        temp = js['playListChilds'][i]
        for temp in tempfull:
            logo = 'http://tv-vip.com/json/playlist/'+temp+'/thumbnail_300x300.jpg'
            title_temp = temp.replace('-',' ').title()
            url = 'http://tv-vip.com/section/'+temp+'/'
            plugintools.add_item(action="tvvip_serie_epis",url=url,title=sc2+title_temp+" >>"+ec2,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
    except: pass

def tvvip_serie_epis(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker TV-vip"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    title_temp = '[B]'+params.get("title").replace('>>','')+'[/B]'
    logo = params.get('thumbnail')
    fondo = params.get("url").replace('section','json/playlist')+'/background.jpg' 
    plugintools.add_item(action="",url="",title=sc2+title_temp+ec2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)

    url = params.get("url")
    headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
    url = url.replace('section','json/playlist')+'index.json'
    
    r = requests.get(url,headers=headers)
    data = r.text.encode('utf8')
    js = json.loads(data)
    try:
        episfull = js['sortedRepoChilds']
        i = 0
        epis = js['sortedRepoChilds'][i]
        for epis in episfull:
            title_epis = epis['name'].encode('utf8').strip().replace("\n","").replace("\t","")
            titlefull = sc+title_epis+ec
            url = 'http://tv-vip.com/film/'+epis['id'].encode('utf8')+'/' # / necesaria para enviar a tvvip_serie_resolvers
        
            plugintools.addPeli(action="tvvip_serie_resolvers",url=url,title=titlefull,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
            epis = int(i)+1
    except: pass

def tvvip_serie_resolvers(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker TV-vip"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    url = params.get("url")
    
    headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
    url = url.replace('film','json/repo')+'index.json'
   
    r = requests.get(url,headers=headers)
    data = r.text.encode('utf8')
    
    data_js = r.text
    js = json.loads(data_js)
    
    logo = params.get("thumbnail")
    fondo = params.get("url").replace('film','json/repo')+'thumbnail.jpg'
    
    title = js['name'].encode('utf8').strip().replace("\n","").replace("\t","")
    title = title.replace('Ã¡','á').replace('Ã©','é').replace('Ã­','í').replace('Ã³','ó').replace('Âº','ú').replace('Ã±','ñ') 

    genr = tvvip_genr(url)
    if genr =="": genr = 'N/D'

    year = js['year'].encode('utf8').strip().replace("\n","").replace("\t","")
    if year =="": year = 'N/D'
    durac = js['durationHuman'].encode('utf8').strip().replace("\n","").replace("\t","")
    if durac =="": durac = 'N/D'
    punt = js['rate'].encode('utf8').strip().replace("\n","").replace("\t","")
    if punt =="": punt = 'N/D'

    lang = tvvip_lang(url)
    subtitle = tvvip_lang_sub(url)

    datamovie = {
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+', '+ec,
    'audiochannels': sc3+'[B]Audio: [/B]'+ec3+sc+str(lang)+', '+ec,
    'subtitleslanguage': sc3+'[B]Subtitulos: [/B]'+ec3+sc+str(subtitle)+ec}
    
    datamovie["plot"]=datamovie["duration"]+datamovie["audiochannels"]+datamovie["subtitleslanguage"]
    
    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
    quality_grup = js['profiles']
    
    for quality in quality_grup:
        quality_max = js['profiles'][quality]['videoResolution'].encode('utf8')
        peso = js['profiles'][quality]['sizeHuman'].encode('utf8')
        try:
            server1 = js['profiles'][quality]['servers'][0]['url'].encode('utf8')
            #http://hs.tv-vip.com/s/transcoder/Anatomía_de_Grey_12x01.mp4/240-mp4/Anatomía_de_Grey_12x01.mp4.mp4
            if not 's/transcoder' in server1:
                server1 = server1.replace('transcoder','s/transcoder')
            url = server1+js['profiles'][quality]['videoUri'].encode('utf8')
            print url
            plugintools.add_item(action="play",url=url,title=sc+title+' (Serv.1)'+ec+sc2+"  ["+str(quality_max)+"]"+ec2+sc5+" ["+peso+"]"+ec5,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        except: pass
        try:
            server2 = js['profiles'][quality]['servers'][1]['url'].encode('utf8')
            if not 's/transcoder' in server2:
                server2 = server2.replace('transcoder','s/transcoder')
            url = server2+js['profiles'][quality]['videoUri'].encode('utf8')
            print url
            plugintools.addPeli(action="play",url=url,title=sc+title+' (Serv.2)'+ec+sc2+"  ["+str(quality_max)+"]"+ec2+sc5+" ["+peso+"]"+ec5,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        except: pass

################################################### Herramientas #################################################

def tvvip_genr(url):
    
    try:
        headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
        r = requests.get(url,headers=headers)
        data_js = r.text.encode('utf8')
        js = json.loads(data_js)
    
        genr = js['tags']
        if len(genr) ==5: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]+', '+genr[4]
        elif len(genr) ==4: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]
        elif len(genr) ==3: genr = genr[0]+', '+genr[1]+', '+genr[2]
        elif len(genr) ==2: genr = genr[0]+', '+genr[1]
        elif len(genr) ==1: genr = genr[0]
        elif len(genr) >5: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]+', '+genr[4]
        return genr.encode('utf8')
    except: return 'N/D'
    
def tvvip_lang(url):
    
    try:
        headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
        r = requests.get(url,headers=headers)
        data_js = r.text.encode('utf8')
        js = json.loads(data_js)
    
        lang = js['languages']
        if len(lang) ==5: lang = lang[0]+', '+lang[1]+', '+lang[2]+', '+lang[3]+', '+lang[4]
        elif len(lang) ==4: lang = lang[0]+', '+lang[1]+', '+lang[2]+', '+lang[3]
        elif len(lang) ==3: lang = lang[0]+', '+lang[1]+', '+lang[2]
        elif len(lang) ==2: lang = lang[0]+', '+lang[1]
        elif len(lang) ==1: lang = lang[0]
        elif len(genr) >5: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]+', '+genr[4]
        lang = lang.replace('1','').replace('2','').replace('3','').replace('4','').replace('5','')
        lang = lang.replace('6','').replace('7','').replace('8','').replace('9','').replace('0','')
        lang = lang.replace('spa','[ESP]').replace('eng','[ENG]').replace('-','').replace('und','N/D')
        return lang.encode('utf8')    
    except: return 'N/D'
    
def tvvip_lang_sub(url):
    
    try:
        headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
        r = requests.get(url,headers=headers)
        data_js = r.text.encode('utf8')
        js = json.loads(data_js)
    
        lang_sub = js['subtitles']
        if len(lang_sub) ==5: lang_sub = lang_sub[0]+', '+lang_sub[1]+', '+lang_sub[2]+', '+lang_sub[3]+', '+lang_sub[4]
        elif len(lang_sub) ==4: lang_sub = lang_sub[0]+', '+lang_sub[1]+', '+lang_sub[2]+', '+lang_sub[3]
        elif len(lang_sub) ==3: lang_sub = lang_sub[0]+', '+lang_sub[1]+', '+lang_sub[2]
        elif len(lang_sub) ==2: lang_sub = lang_sub[0]+', '+lang_sub[1]
        elif len(lang_sub) ==1: lang_sub = lang_sub[0]
        elif len(genr) >5: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]+', '+genr[4]
        lang_sub = lang_sub.replace('1','').replace('2','').replace('3','').replace('4','').replace('5','')
        lang_sub = lang_sub.replace('6','').replace('7','').replace('8','').replace('9','').replace('0','')
        lang_sub = lang_sub.replace('spa','[ESP]').replace('eng','[ENG]').replace('-','')
        return lang_sub.encode('utf8')    
    except: return 'N/D'
    
######################################### @ By Aquilesserr PalcoTv Team ######################################### 

    
