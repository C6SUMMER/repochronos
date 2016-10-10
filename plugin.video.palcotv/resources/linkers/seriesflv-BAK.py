# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV Linker de SeriesFLV.com
# Version 0.2 (04.04.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys
import plugintools
import requests
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

from __main__ import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'https://www.cubbyusercontent.com/pl/seriesflv_logo.png/_ee072582352d47b1bae2e37225ce01e7'
fanart = 'https://www.cubbyusercontent.com/pl/seriesflv_fanart.jpg/_8d2814c941a540ed8b77866dc47d2c53'
referer = 'http://www.seriesflv.net/'
web = 'http://www.seriesflv.net/'

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.2]"


def seriesflv_linker0(params):
    plugintools.log('[%s %s] Linker SeriesFlv %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesFlv"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url")
    data,cookie_ses = jump_cloudflare(url)
    #print data
    #print cookie_ses
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Accept-Encoding':'gzip, deflate','Host':'www.seriesflv.net',
    'Referer': url}

    r = requests.get(url,headers=headers)
    
    if 'refresh' in r.headers:
        time.sleep(int(r.headers['refresh'][:1]))
        url = web + r.headers['refresh'][7:]
        print url

    r = requests.get(url,headers=headers)
    data = r.content
    #print data
    '''
    logo = plugintools.find_single_match(data,'<img title=".*?src="([^"]+)"')
    if logo =="": logo = thumbnail  

    title = plugintools.find_single_match(data,'<h1 class="off">([^<]+)</h1>').replace('\\','') 

    votos = plugintools.find_single_match(data,'<span id="reviewCount">(.*?)<')
    if votos =="": votos = 'N/D'

    punt = plugintools.find_single_match(data,'<meta itemprop="ratingValue" content="([^"]+)"')
    if punt =="": punt = 'N/D'

    year = plugintools.find_single_match(data,'<td>Año.*?<td>(.*?)</td>')
    if year =="": year = 'N/D'

    bloq_temp =plugintools.find_single_match(data,'<div class="temporadas m1">(.*?)<div id="lista" class="color1 ma1">')
    n_temp = plugintools.find_multiple_matches(bloq_temp,'<a class="color1 on ma1 font2".*?">Temporada(.*?)<')
    n_temp = n_temp[-1].strip()
    if n_temp =="": n_temp = 'N/D'

    bloq_genr = plugintools.find_single_match(data,'<td>Géneros(.*?)</tr>')
    n_genr = plugintools.find_multiple_matches(bloq_genr,'href=".*?">(.*?)<')
    genr = seriesflv_genr(n_genr)

    bloq_pais = plugintools.find_single_match(data,'<td>País </td>(.*?)/td>')
    pais = plugintools.find_multiple_matches(bloq_pais,'<img src=".*?">(.*?)<')
    try:
        pais = pais[-1].strip()
    except: pais = 'N/D'

    sinopsis = plugintools.find_single_match(data,'<p class="color7">(.*?)</p>').replace('\&quot;','"')
    if sinopsis =="": sinopsis = 'N/D'

    datamovie = {
    'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(n_temp)+', '+ec,
    'votes': sc3+'[B]Votos: [/B]'+ec3+sc+str(votos)+', '+ec,
    'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'country': sc3+'[B]País: [/B]'+ec3+sc+str(pais)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["season"]+datamovie["votes"]+datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["country"]+datamovie["sinopsis"]

    plugintools.add_item(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    patron_temp = '<a class="color1 on ma1 font2"(.*?)/a>'
    item_temp = re.compile(patron_temp,re.DOTALL).findall(data)
    for temp in item_temp:
        url = plugintools.find_single_match(temp,'href="([^"]+)"')
        name_temp = plugintools.find_single_match(temp,'.html">(.*?)<')
        plugintools.addPeli(action="seriesflv_linker_capit",url=url,title=sc2+name_temp+' >>'+ec2,info_labels=datamovie,extra=cookie_ses,thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)
    
def seriesflv_linker_capit(params):
    plugintools.log('[%s %s] Linker SeriesFlv %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesFlv"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    url = params.get("url")
    cookie_ses = params.get("extra") #Pasando el valor de la cookie __cfduid
    
    headers = {"Host":"www.seriesflv.net","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Referer":referer,'__cfduid':cookie_ses}
    r = requests.get(url,headers=headers)
    data = r.content

    bloq_capit = plugintools.find_single_match(data,'<div class="serie-cont left">(.*?)</table>')
    title_temp = plugintools.find_single_match(bloq_capit,'<h1 class="off">(.*?)</h1>').replace('\\','')        
    plugintools.add_item(action="",url="",title=sc2+'[B]'+title_temp+'[/B]'+ec2,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)    
    
    bloq_cover = plugintools.find_single_match(data,'<div class="portada">(.*?)</div>')
    corver = plugintools.find_single_match(bloq_cover,'src="([^"]+)')

    capit= plugintools.find_multiple_matches(bloq_capit,'<td class="sape">(.*?)</tr>')
    for item in capit:
        title_capit = plugintools.find_single_match(item,'class="color4".*?">(.*?)</a>').replace('\\','')
        url_capit = plugintools.find_single_match(item, '<a class="color4" href="([^"]+)"')
        lang = plugintools.find_multiple_matches(item,'http://www.seriesflv.net/images/lang/(.*?).png')
        plugintools.addPeli(action="seriesflv_linker_servers",url=url_capit,title=sc+str(title_capit)+ec,extra=str(cookie_ses)+'|'+str(title_capit),thumbnail=corver,fanart=fanart,folder=True,isPlayable=False)

def seriesflv_linker_servers(params):
    plugintools.log('[%s %s] Linker SeriesFlv %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesFlv"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    url = params.get("url")
    params_web = params.get("extra").split('|') #Pasando titulo del epis y valor de la cookie __cfduid
    cookie_ses =  params_web[0]
    title_capit = params_web[-1]

    headers = {"Host":"www.seriesflv.net","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Referer":referer,'__cfduid':cookie_ses}
    r = requests.get(url,headers=headers)
    data = r.content
    
    bloq_cover = plugintools.find_single_match(data,'<div class="portada">(.*?)</div>')
    corver = plugintools.find_single_match(bloq_cover,'src="([^"]+)')

    bloq_server = plugintools.find_single_match(data,'<div id="enlaces">(.*?)</table>')
    server = plugintools.find_multiple_matches(bloq_server, '<img width="20"(.*?)</tr>')
    
    for item in server:       
        lang = plugintools.find_single_match(item,'src="http://www.seriesflv.net/images/lang/(.*?).png"')
        if lang =='es': lang = sc2+'[I][ESP][/I]'+ec2
        elif lang =='la': lang = sc2+'[I][LAT][/I]'+ec2
        elif lang =='en': lang = sc2+'[I][ENG][/I]'+ec2
        elif lang =='sub': lang= sc2+'[I][SUB][/I]'+ec2 
        else: lang = sc2+'[I][N/D][/I]'+ec2
          
        server_name = plugintools.find_single_match(item,'class="e_server"><img width="16" src="([^"]+)"')
        server_name = server_name.split("domain=")
        server_name = server_name[-1]
        url_redir = plugintools.find_single_match(item,'<td width="84"><a href="([^"]+)"')

        url = getlinkflv(url_redir,cookie_ses)
        server = video_analyzer(server_name)
        titlefull = sc+str(title_capit)+ec+' '+str(lang)+'  '+sc5+'[I]['+str(server)+'][/I]'+ec5
        plugintools.addPeli(action=server,url=url,title=titlefull,extra=cookie_ses,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=True)
    
################################################### Herramientas #################################################

def seriesflv_genr(n_genr):

    if len(n_genr) >=5: n_genr = n_genr[0]+', '+n_genr[1]+', '+n_genr[2]+', '+n_genr[3]+', '+n_genr[4]
    elif len(n_genr) ==4: n_genr = n_genr[0]+', '+n_genr[1]+', '+n_genr[2]+', '+n_genr[3]
    elif len(n_genr) ==3: n_genr = n_genr[0]+', '+n_genr[1]+', '+n_genr[2]
    elif len(n_genr) ==2: n_genr = n_genr[0]+', '+n_genr[1]
    elif len(n_genr) ==1: n_genr = n_genr[0]
    return n_genr   

def jump_cloudflare(url):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Accept-Encoding':'gzip, deflate','Host':'www.seriesflv.net',
    'Referer': url}
    r = requests.get(url,headers=headers)
    if 'refresh' in r.headers:
        time.sleep(int(r.headers['refresh'][:1]))
        url = web + r.headers['refresh'][7:]
    r = requests.get(url,headers=headers)
    data = r.content
    cookie_ses = r.cookies['__cfduid']
    return data,cookie_ses
    
def getlinkflv(url_redir,cookie_ses):

    headers = {"Host":"www.seriesflv.net","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Referer":referer,'__cfduid':cookie_ses}
    r = requests.get(url_redir,headers=headers)
    data = r.content
    url_final = plugintools.find_single_match(data,'<a id="continue" href="([^"]+)"')
    return url_final
    
############################################# By PalcoTv Team ####################################################




