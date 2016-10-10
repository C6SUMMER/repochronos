# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de VerDirectoTV.net Para Arena+
# Version 0.1 (19.03.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info) y a los tutoriales de Juarrox


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import requests

from resources.tools.resolvers import *
from resources.tools.multilink import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


url = 'http://verdirectotv.net/category/ver-television-de-espana-en-directo-gratis-las-24-horas/'
url_ref = 'http://verdirectotv.net/'

def vercanalestv0(params):
	plugintools.log("[%s %s] Parser www.telefivegb.com... %s " % (addonName, addonVersion, repr(params)))

	thumbnail = 'http://www.vercanalestv.com/imagenes/ver-ahora.gif'
	fanart = 'http://www.statsbay.com/website-screenshot/verdirectotv.net.jpg'

	r = requests.get(url)
	data = r.content

	plugintools.add_item(action="",url="",title="[COLOR blue][B]      VerDirectoTV.net      [I](v0.0.3)[/B][/COLOR][COLOR yellow][I] **** by DarioMO ****[/I][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	grupos = plugintools.find_single_match(data,'>NACIONALES</font>(.*?)</ul>')
	cada_grupo = plugintools.find_multiple_matches(grupos,'<a href=(.*?)/a>')	

	plugintools.add_item(action="vercanalestv_categoria",title="[COLOR orange][B]Todos los Canales Españoles[/B][/COLOR]", url=url,thumbnail="http://www.abc.es/Media/201407/23/bandera-nacional-colon--644x362.jpg", extra="", fanart=fanart, folder=True, isPlayable=False)

	for item in cada_grupo:
		url_grupo = plugintools.find_single_match(item,'"(.*?)"')
		nom_grupo = plugintools.find_single_match(item,'size=4>(.*?)<')
		if nom_grupo.upper() == "DOCUM. ":
			nom_grupo = "DOCUMENTALES"

		if nom_grupo.upper() <> "ADULTOS":
			plugintools.add_item(action="vercanalestv_categoria",title="[COLOR orange][B]"+nom_grupo+"[/B][/COLOR]", url=url_grupo,thumbnail=thumbnail, extra="", fanart=fanart, folder=True, isPlayable=False)

	plugintools.add_item(action="vercanalestv_categoria",title="[COLOR red][B]<<<Solo Adultos>>>[/B][/COLOR]", url="http://verdirectotv.net/category/adultos/",thumbnail="http://www.abc.es/Media/201407/23/bandera-nacional-colon--644x362.jpg", extra="", fanart=fanart, folder=True, isPlayable=False)




## Cargo las Diferentes Categorías
def vercanalestv_categoria(params):
	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	titulo = params.get("extra")
	if len(titulo) <> 0:
		title = titulo
		
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	r=requests.get(url, headers=headers)
	data = r.content

	plugintools.add_item(action="",url="",title="[COLOR lightgreen][B]·····"+title+"·····[/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	cada_canal = plugintools.find_multiple_matches(data,'<div class="latestvideo">(.*?)<div class="latestinfo">')	
	for item in cada_canal:
		url_canal = plugintools.find_single_match(item,'href="(.*?)/"') + "/"
		titulo_canal = plugintools.find_single_match(item,'title="(.*?)"')
		if titulo_canal.upper().find("BEMAD") >=0:  # es de MiTele y no va con SpD
			titulo_canal = "Ver BE-MAD por señal Oficial de MiTele"
		logo_canal = plugintools.find_single_match(item,'img src="(.*?)"')

		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
		r0=requests.get(url_canal, headers=headers)
		data0 = r0.content

		url_valida = plugintools.find_single_match(data0,'0px" allowfullscreen src="(.*?)"')
		if len(url_valida) == 0:
			url_valida = plugintools.find_single_match(data0, '0px" allowfullscreen  src="(.*?)"')
		
		if len(url_valida) == 0:
			url_valida = plugintools.find_single_match(data0,'0px" src="(.*?)"')
		
		nueva_ref =  'http://' + plugintools.find_single_match(url_valida,'http://(.*?)/') + '/'
		if titulo_canal.upper().find("BE-MAD") >=0:  # es de MiTele y no va con SpD
			titulo_canal = "Ver BE-MAD por señal Oficial de MiTele"
			url_montada = "llamada:mitele; NOM_CANAL=bemad"
			params["url"] = url_montada
			params["thumbnail"] = logo_canal
			params["plot"] = []
			params["title"]=titulo_canal
			url_analyzer(params)
		else:	
			url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_valida+'%26referer='+nueva_ref
			plugintools.add_item(action="runPlugin",title=titulo_canal,url=url_montada,thumbnail=logo_canal,fanart=fanart,folder=False,isPlayable=True)



		
		
