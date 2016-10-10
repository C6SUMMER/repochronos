# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de: TV Sports LivesTream
# Version 0.1 (21.11.2015)
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

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

url = 'http://www.tv-sports-livestream.fr/index.html'
url_ref = 'http://www.tv-sports-livestream.fr/'

def tvsportslive(params):
	plugintools.log("[%s %s] Parser de TV Sports LiveStream... %s " % (addonName, addonVersion, repr(params)))

	thumbnail = 'https://copy.com/2fM1NXOrpJRZlJLO'
	fanart = 'https://copy.com/qLbxeQryHAgaXRxn'
	print "***********************************************************************"
	print "Prueba2"
	print "***********************************************************************"
	
	plugintools.add_item(action="",url="",title="[COLOR blue][B]TV Sports LiveStream[/B][/COLOR][COLOR yellow][I]    **** byDMO ****[/I][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	plugintools.add_item(action="canales_aces",url="",title="[COLOR orange][B]Canales [COLOR blue]Acestream[/B][/COLOR]",thumbnail="https://copy.com/3UwBszjYBSwx3rnQ", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="canales_flash",url="",title="[COLOR orange][B]Canales [COLOR red]Flash[/B][/COLOR]",thumbnail="https://copy.com/ldmHjZR6KH6OfouY", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="canales_eventos",url="",title="[COLOR orange][B]Canales [COLOR blue]MultiEventos[/B][/COLOR]",thumbnail="https://copy.com/43mMgbYLvqJuPm1s", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	plugintools.add_item(action="programacion_diaria",url="",title="[COLOR orange][B]···Programación Diaria···[/B][/COLOR]",thumbnail="https://copy.com/Ti9KI31qfNqGzDOk", fanart=fanart, folder=True, isPlayable=False)


	
	

def canales_aces(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	r = requests.get(url)	
	data = r.content
	
	acota_aces = plugintools.find_single_match(data,'Menu principal:</p>(.*?)<!-- Menu END -->')
	
	cada_canal = plugintools.find_multiple_matches(acota_aces,'<li><a hre(.*?)/a></li>')	
	
	for item in cada_canal:
		url_canal=url_ref+plugintools.find_single_match(item,'f="(.*?)"')
		titulo_canal=plugintools.find_single_match(item,'title="">(.*?)<')
		if len(titulo_canal) == 0:
			titulo_canal=plugintools.find_single_match(item,'title="(.*?)">')
		

		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_canal+'%26referer='+url_ref
		plugintools.add_item(action="runPlugin", title=titulo_canal, url=url_montada, thumbnail=thumbnail , fanart=fanart, folder = False, isPlayable=True)




def canales_flash(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	r = requests.get(url)	
	data = r.content
	
	acota_flash = plugintools.find_single_match(data,'TV Flash</span></p>(.*?)</p></marquee>')
	
	cada_canal = plugintools.find_multiple_matches(acota_flash,'class="ImLink"(.*?)width=')	
	
	for item in cada_canal:
		url_canal=url_ref+plugintools.find_single_match(item,'href="(.*?)"')
		##Como esta sección no tiene Títulos del Canal, lo saco de la propia url quitandole el ".html" y cambiando los guiones por espacios jejeje
		titulo_canal=plugintools.find_single_match(item,'href="(.*?)"').replace(".html", "").replace("_", " ").replace("-", " ")
		logo_canal=url_ref+plugintools.find_single_match(item,'src="(.*?)"')

		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_canal+'%26referer='+url_ref
		plugintools.add_item(action="runPlugin", title=titulo_canal, url=url_montada, thumbnail=logo_canal , fanart=fanart, folder = False, isPlayable=True)

	


def canales_eventos(params):

	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	r = requests.get(url)	
	data = r.content
	
	acota_eventos = plugintools.find_single_match(data,'Multilangue</span></p>(.*?)</span></p>')
	
	cada_canal = plugintools.find_multiple_matches(acota_eventos,'class="ImLink"(.*?)/a>')	
	
	for item in cada_canal:
		url_canal=url_ref+plugintools.find_single_match(item,'href="(.*?)"')
		titulo_canal=plugintools.find_single_match(item,'title=""> (.*?)<').replace("Chaine", "Canal")

		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_canal+'%26referer='+url_ref
		plugintools.add_item(action="runPlugin", title=titulo_canal, url=url_montada, thumbnail=thumbnail , fanart=fanart, folder = False, isPlayable=True)


		
		
		
def programacion_diaria(params):

	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	r = requests.get('http://www.streaming-foot.info/schedule.php')	
	data = r.content
	
	cada_evento = plugintools.find_multiple_matches(data,'<li class="list-group-item"(.*?)</li>')	
	
	fecha_cabecera="01/01/1900"
	for item in cada_evento:
		fecha_ingles=plugintools.find_single_match(item,'<span style="display:none">(.*?) ').strip()
		dia=fecha_ingles.split("-")[2]
		mes=fecha_ingles.split("-")[1]
		anno=fecha_ingles.split("-")[0]
		fecha_esp=dia+'/'+mes+'/'+anno
		if fecha_esp <> fecha_cabecera:
			fecha_cabecera=fecha_esp
			linea="[COLOR orange]             ·····Día "+fecha_esp+"·····[/COLOR]"
			plugintools.add_item(action="",url="",title=linea,thumbnail="https://copy.com/ZeNA62BDIES4C1jW", fanart=fanart, folder=False, isPlayable=False)
		
		hora=plugintools.find_single_match(item,'<span style="">(.*?)</span>')+'h'
		categoria=plugintools.find_single_match(item,'categorie">&nbsp;(.*?)</span>')
		evento=plugintools.find_single_match(item,'name_match">&nbsp;(.*?)</span>')
		canales=plugintools.find_single_match(item,'links">(.*?)</span>')
		
		linea="[COLOR red]"+"("+hora+")-> [COLOR yellow]"+categoria+": "+evento+"  [COLOR red]"+canales.strip()+"[/COLOR]"

		plugintools.add_item(action="",url="",title=linea,thumbnail="https://copy.com/ZeNA62BDIES4C1jW", fanart=fanart, folder=False, isPlayable=False)

		
		
		
