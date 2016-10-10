# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de PlayLists de Diskokosmiko.mx by DMax
# Version 0.1 (17.07.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
# 

import os
import xbmcplugin
import xbmc, xbmcgui
import urllib

import sys
import urllib
import urllib2
import re

import xbmcaddon

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



buscar=""
#link = "plugin://plugin.video.live.streamspro/?mode=17&regexs=%7bu%27getUrl%27%3a%20%7b%27x-req%27%3a%20u%27XMLHttpRequest%27%2c%20%27cookiejar%27%3a%20%27%27%2c%20%27name%27%3a%20u%27getUrl%27%2c%20%27accept%27%3a%20u%27%2a%2f%2a%27%2c%20%27connection%27%3a%20u%27keep-alive%27%2c%20%27expres%27%3a%20u%27DownloadUrl%22%3a%22(%5b%5e%22%5d%2b)%27%2c%20%27referer%27%3a%20u%27http%3a%2f%2fcopiapop.com%2f%5bmakelist.param1%5d%27%2c%20%27page%27%3a%20u%27http%3a%2f%2fcopiapop.com%2f%5bmakelist.param3%5d%27%2c%20%27rawpost%27%3a%20u%27fileId%3d%5bmakelist.param4%5d%26__RequestVerificationToken%3d%5bmakelist.param5%5d%27%7d%2c%20u%27makelist%27%3a%20%7b%27listrepeat%27%3a%20u%27%5cr%5cn%20%20%20%20%20%20%20%20%3ctitle%3e%5bCOLOR%20yellow%5d%20%5bmakelist.param2%5d%5b%2fCOLOR%5d%3c%2ftitle%3e%5cr%5cn%20%20%20%20%20%20%20%20%3clink%3e%24doregex%5bgetUrl%5d%3c%2flink%3e%5cr%5cn%20%20%20%20%20%20%20%20%3cthumbnail%3eEL_LOGO%3c%2fthumbnail%3e%5cr%%20%20%20%20%20%20%20%20%3cfanart%3eEL_FANART%3c%2ffanart%3e%5cr%5cn%27%2c%20%27expres%27%3a%20u%27class%3d%22name%22.%2ahref%3d%22%5c%5c%2f(%5b%5e%22%5d%2a)%22.%2b%3f%3e(.%2a%3f)%3c%5b%5c%5cw%5c%5cW%5c%5cs%5d%2a%3faction%3d%22%5c%5c%2f(%5b%5e%22%5d%2a)%22.%2b%3fvalue%3d%22(.%2a%3f)%22.%2aToken.%2b%3fvalue%3d%22(.%2a%3f)%22%27%2c%20%27cookiejar%27%3a%20%27%27%2c%20%27name%27%3a%20u%27makelist%27%2c%20%27page%27%3a%20u%27PON EL LINK%27%7d%7d&url=%24doregex%5bmakelist%5d"
link = "plugin://plugin.video.live.streamspro/?mode=17&regexs=%7bu%27getUrl%27%3a%20%7b%27x-req%27%3a%20u%27XMLHttpRequest%27%2c%20%27cookiejar%27%3a%20%27%27%2c%20%27name%27%3a%20u%27getUrl%27%2c%20%27accept%27%3a%20u%27%2a%2f%2a%27%2c%20%27connection%27%3a%20u%27keep-alive%27%2c%20%27expres%27%3a%20u%27DownloadUrl%22%3a%22(%5b%5e%22%5d%2b)%27%2c%20%27referer%27%3a%20u%27http%3a%2f%2fdiskokosmiko.mx%2f%5bmakelist.param2%5d%27%2c%20%27page%27%3a%20u%27http%3a%2f%2fdiskokosmiko.mx%2faction%2fDownloadFile%3flocation%3dfi%26f%3d%5bmakelist.param1%5d%27%2c%20%27rawpost%27%3a%20u%27fileId%3d%5bmakelist.param1%5d%26__RequestVerificationToken%3d%24doregex%5btok%5d%27%7d%2c%20u%27makelist%27%3a%20%7b%27listrepeat%27%3a%20u%27%5cr%5cn%20%20%20%20%20%20%20%20%3ctitle%3e%20%5bmakelist.param3%5d%3c%2ftitle%3e%5cr%5cn%20%20%20%20%20%20%20%20%3clink%3e%24doregex%5bgetUrl%5d%3c%2flink%3e%5cr%5cn%20%20%20%20%20%20%20%20%3cthumbnail%3eEL_LOGO%3c%2fthumbnail%3e%5cr%5cn%5ct%5ct%3cfanart%3eEL_FANART%3c%2ffanart%3e%5cr%5cn%27%2c%20%27expres%27%3a%20u%27href%3d%22%5c%5c%2f.%2a%2c(.%2a%3f)%2clist.%2a%5c%5cn.%2a%5c%5cn.%2a%5c%5cn.%2ahref%3d%22%5c%5c%2f(%5b%5e%22%5d%2a)%22.%2a%3f%3e(.%2a%3f)%3c%27%2c%20%27cookiejar%27%3a%20%27%27%2c%20%27name%27%3a%20u%27makelist%27%2c%20%27page%27%3a%20u%27PON EL LINK%27%7d%2c%20u%27tok%27%3a%20%7b%27cookiejar%27%3a%20%27%27%2c%20%27name%27%3a%20u%27tok%27%2c%20%27connection%27%3a%20u%27keep-alive%27%2c%20%27expres%27%3a%20u%27DownloadFile.%2aRequestVerificationToken.%2a%3fvalue%3d%22(%5b%5e%22%5d%2b)%27%2c%20%27referer%27%3a%20u%27http%3a%2f%2fdiskokosmiko.mx%2fpacharico%2fpeliculas-hd-19324%2flist%2c1%2c1%27%2c%20%27page%27%3a%20u%27http%3a%2f%2fdiskokosmiko.mx%2f%5bmakelist.param2%5d%27%7d%7d&url=%24doregex%5bmakelist%5d"

fanart = 'http://i.imgur.com/ecbbRwO.png'
thumbnail = 'http://i.imgur.com/v1UEycM.png'


def kosmiko_linker(busqueda):
	if busqueda.find("list") < 0:
		if busqueda.find("/gallery,") >= 0:
			busqueda = busqueda.replace("/gallery,", "/list,")
		else:	
			lista = busqueda +"/list,1,1"
	else:
		lista = busqueda
	#Me aseguro empezar x la 1ª
	lista = "http" + plugintools.find_single_match(lista, 'http(.*?)list,') + "list,1,1"

	num_pag = 1

	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": lista}
	r=requests.get(lista, headers=headers)
	data = r.content
	
	logo = thumbnail
	
	
	videos = plugintools.find_multiple_matches(data,'<li data-file-id(.*?)>')
	num_vid1 = len(videos)
	pag_sig = "http://" + plugintools.find_single_match(lista, 'http://(.*?)list,') + "list,1," + str(num_pag+1)

	plugintools.add_item(action="",url="",title="[COLOR yellow][I]              ····[COLOR skyblue]Linker PlayLists de DiskoKosmiko[COLOR yellow]····[COLOR red][B]      (by DMax)[/B][/I][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

	titulo_list = plugintools.find_single_match(data, 'name="keywords" content="(.*?), Descargar').decode('utf-8')
	

	#Dado q aunq pillo la imagen, el formato q tiene no lo soporta, o pongo para todo el logo genérico (no me gusta)...
	#o me la juego con una consulta a imágenes de google por el título y me la "juego" con la 1ª imagen q muestre jejeje.
	'''
	logo0 = plugintools.find_single_match(data, '<div id="CollectionHeader(.*?)cursor: pointer')
	logo = plugintools.find_single_match(logo0, "background-image(.*?);").replace(": url('","").replace("')","")
	'''
	
	consulta = "https://www.google.es/search?newwindow=1&hl=es&site=imghp&tbm=isch&source=hp&biw=1366&bih=643&q="+titulo_list.replace(" ","+")
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": consulta}
	r=requests.get(consulta, headers=headers)
	data2 = r.content
	
	logo = plugintools.find_single_match(data2, '"ou":"(.*?)"')
	if len(logo)== 0:
		logo = thumbnail
	
	nom_canal = plugintools.find_single_match(busqueda, "http://diskokosmiko.mx/(.*?)/")
	canal = "http://diskokosmiko.mx/"+nom_canal
	salir = False
	#Voy a comprobar el nº de pag. q tiene, pues cada 1 tiene mas que la anterior, exepto la q ya "no existe", que tiene el mismo nº q la última
	while salir == False:

		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": pag_sig}
		r=requests.get(pag_sig, headers=headers)
		data = r.content
		
		videos = plugintools.find_multiple_matches(data, '<li data-file-id(.*?)>')
		num_vid2 = len(videos)
		
		if num_vid2 > num_vid1:  #Es una pag. siguiente real
			num_pag = num_pag + 1
			pag_sig = "http://" + plugintools.find_single_match(lista, 'http://(.*?)list,') + "list,1," + str(num_pag+1)
			salir = False
			num_vid1 = num_vid2
		else:
			salir = True

	plugintools.add_item(action="runPlugin",url=link.replace("PON EL LINK",pag_sig).replace("EL_LOGO", logo).replace("EL_FANART", fanart),title="[COLOR white]Ver la Lista: [COLOR red]"+titulo_list+"[/COLOR]",thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)
	plugintools.add_item(action="kosmiko_canal_listas",url=canal,title="[COLOR white]Ver Resto de Listas del Canal: [COLOR red]"+nom_canal+"[/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
		
		
		
		
def kosmiko_canal_listas(params):
	canal = params.get("url")
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": canal}
	r=requests.get(canal, headers=headers)
	data = r.content

	nom_canal = plugintools.find_single_match(canal, "http://diskokosmiko.mx/(.*)")
	plugintools.add_item(action="",url="",title="[COLOR yellow][I]              ····[COLOR skyblue]Todas las Listas del Canal[COLOR red][B]  " + nom_canal + "[COLOR yellow]···· " + "[/B][/I][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

	todas_listas = plugintools.find_single_match(data, '<div class="collections_list responsive_width">(.*?)<div id="recommended_collections" class="recommended_collections" data-ga="collection.otherrecommended">')
	
	lin_cabecera = "¿DESEA BUSCAR UN LOGO PARA CADA LISTA?"
	lin1 = "Las imágenes que emplea la web, no son aceptadas por Kodi. Por lo tanto hay que intentar"
	lin2 = "buscarlas en Google/Images... este proceso [B]RALENTIZA[/B] mucho el proceso."
	busco_imagen = False
	busco_imagen = xbmcgui.Dialog().yesno(lin_cabecera, lin1 , lin2 )

	cada_lista = plugintools.find_multiple_matches(todas_listas, '<a class="name"(.*?)/a>')
	for item in cada_lista:
		url_lista = plugintools.find_single_match(item, 'href="(.*?)"')
		busca = url_lista + '">' + "(.*?)" + "<"

		titulo = plugintools.find_single_match(item, busca).decode('utf-8')

		if busco_imagen == True:
			#Como aquí tampoco son validas las imágenes para Kodi, hago lo mismo, la búsqueda en google
			consulta = "https://www.google.es/search?newwindow=1&hl=es&site=imghp&tbm=isch&source=hp&biw=1366&bih=643&q="+titulo.replace(" ","+")
			headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": consulta}
			r=requests.get(consulta, headers=headers)
			data2 = r.content

			logo = plugintools.find_single_match(data2, '"ou":"(.*?)"')
			if len(logo)== 0:
				logo = thumbnail
		else:
			logo = thumbnail
		
		
		busqueda = "http://diskokosmiko.mx" + url_lista +"/list,1,1"
		plugintools.add_item(action="kosmiko_lanza_lista",url=busqueda,title="[COLOR white]Ver Lista: [COLOR red]"+titulo+"[/COLOR]",thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)
	
	
	
def kosmiko_lanza_lista(params):
	busqueda = params.get("url")
	
	kosmiko_linker(busqueda)

	
	
	
	
	
	
