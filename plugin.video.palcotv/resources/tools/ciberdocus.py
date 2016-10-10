# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de CiberDocumentales.com
# Version 0.1 (23.11.2015)
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

plugintools.setview("tvshows")


url = 'http://www.ciberdocumentales.com/'
url_ref = 'http://www.ciberdocumentales.com/'



def ciberdocus0(params):
	plugintools.log("[%s %s] Parser CiberDocumentales.com... %s " % (addonName, addonVersion, repr(params)))

	thumbnail = 'http://i.imgur.com/XeSIht9.png'
	fanart = 'http://i.imgur.com/rjkRjKQ.png'

	plugintools.add_item(action="",url="",title="[COLOR blue][B]CiberDocumentales.com[/B]   v(0.2)[/COLOR][COLOR yellow][I]    **** byDMO ****[/I][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	plugintools.add_item(action="ciberdocus3",url="",title="[COLOR red][B]····Buscar····[/B][/COLOR]",thumbnail="http://i.imgur.com/2TExUX4.png", extra="1", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Historia[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/2/historia/",thumbnail="http://4.bp.blogspot.com/_oTJ-PjeAJ-g/S7vv4GHqsqI/AAAAAAAAABo/XTIJb0KIpz8/S740/HISTORIA_LOGO.JPG", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Deportes[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/3/deporte/",thumbnail="http://www.incusdrive.com/wp-content/uploads/2015/10/logo-Solo-OKweb.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Misterio[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/1/misterio/",thumbnail="http://www.conspiracionesocultas.es/wp-content/uploads/2014/12/logo-zona-misterios.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Arte y Cine[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/5/arte-y-cine/",thumbnail="http://lamula.pe/media/uploads/2b4501407dd2466ab74dd601303656f9.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Ciencia[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/4/ciencia/",thumbnail="http://intercentres.edu.gva.es/intercentres/46002179/html/Departamentos/FyQ/jupiter_radio/logo_cea6.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Música[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/12/musica/",thumbnail="http://inspirationfeeed.files.wordpress.com/2013/05/music-town1.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Naturaleza[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/6/naturaleza/",thumbnail="http://uniradio.ujaen.es/sites/default/files/logos_programas/RADIO%20NATURALEZA%20VIVA%20logo.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Política[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/9/politica/",thumbnail="http://www.liberalismoespanol.es/wp-content/uploads/2015/02/Captura-de-pantalla-2015-02-06-a-las-00.06.48-874x492.png", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Psicología[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/8/psicologia/",thumbnail="http://static-dms.guiamais.com.br/dms/69/92/48/489269.png", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Religión[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/7/religion/",thumbnail="http://seyma-yenitas.wikispaces.com/file/view/religion-logo2.jpg/279448658/800x600/religion-logo2.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Salud[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/11/salud/",thumbnail="http://www.entreestudiantesupr.org/rcm/files/2015/01/logo_salud_by_luisxolavarria-d6mrwh0-754x583.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Sociedad[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/10/sociedad/",thumbnail="http://latinomics1.files.wordpress.com/2013/07/logo-sociedad.png", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR orange][B]Tecnología[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/13/tecnologia/",thumbnail="http://www.hd-tecnologia.com/imagenes/articulos/2012/02/logo-hd-tecnologia-new.png", fanart=fanart, folder=True, isPlayable=False)

	
	
	
## Cargo las Diferentes Categorías
def ciberdocus1(params):
	plugintools.setview("tvshows")

	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	data = plugintools.read(url)	
	
	group_channel = plugintools.find_single_match(data,'var xajaxRequestUri="(.*?)<div id="paginador">')
	plugintools.log("group_channel= "+group_channel)
	cada_canal = plugintools.find_multiple_matches(group_channel,'<div class="fotonoticia">(.*?)data-layout="standard"')	

	for item in cada_canal:
		plugintools.log("item= "+item)
		
		url_canal=plugintools.find_single_match(item,'" data-href="(.*?)"')
		titulo_canal=plugintools.find_single_match(item,'alt="(.*?)"')
		caratula_canal='http://www.ciberdocumentales.com'+plugintools.find_single_match(item,'src="(.*?)"')

		##Capturo la Sinopsis en un Diccionario para usarla en "plugintools.add_item(" mediante la variable "info_labels"
		sinopsis = plugintools.find_single_match(item,'h3></a><br /><br />(.*?)</div>')
		plugintools.log("Sinopsis= "+sinopsis)
		datamovie = {}
		datamovie["Plot"]=sinopsis
		
		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&item=catcher%3dstreams%26url='+url_canal+'%26referer='+url_ref
		plugintools.add_item(action="runPlugin", title=titulo_canal, url=url_montada, thumbnail=caratula_canal, info_labels=datamovie , fanart=fanart, folder = False, isPlayable=True)

	#Resuelvo la posibilidad de mas de 1 Página en la Categoría

	mas_pag = plugintools.find_single_match(data,'<div class="pagination">(.*?)</div>')

	#En busca meto la url (http://www.ciberdocumentales.com/videos/2/historia/) "menos" la cadena del comienzo (http://www.ciberdocumentales.com/) para obtener esto "videos/2/historia/"
	busca = url.lstrip(url_ref)
	
	lista_paginas = plugintools.find_multiple_matches(mas_pag,busca+'([^/]+)')
	#Con esto te devuelve una lista: ['2' , '3', '4', ... '41', '2']... y como el q me interesa es el penúltimo (41)... lo obtengo así:
	ult_pag = int(lista_paginas[-2])
	
	for num_pag in range(2, ult_pag+1):
		
		url_pag = url+str(num_pag)+'/'  ## Obtengo las páginas así: http://www.ciberdocumentales.com/videos/2/historia/3
		plugintools.add_item(action="ciberdocus2",title="[COLORFFFF0759]Página: " + str(num_pag) + "  >>>[/COLOR]", url=url_pag,thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)


		
def ciberdocus2(params):
	plugintools.setview("tvshows")
	
	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	data = plugintools.read(url)	
		
	group_channel = plugintools.find_single_match(data,'var xajaxRequestUri="(.*?)<div id="paginador">')
	plugintools.log("group_channel= "+group_channel)
	cada_canal = plugintools.find_multiple_matches(group_channel,'<div class="fotonoticia">(.*?)data-layout="standard"')	

	for item in cada_canal:
		plugintools.log("item= "+item)
		
		url_canal=plugintools.find_single_match(item,'" data-href="(.*?)"')
		titulo_canal=plugintools.find_single_match(item,'alt="(.*?)"')
		caratula_canal='http://www.ciberdocumentales.com'+plugintools.find_single_match(item,'src="(.*?)"')

		##Capturo la Sinopsis en un Diccionario para usarla en "plugintools.add_item(" mediante la variable "info_labels"
		sinopsis = plugintools.find_single_match(item,'h3></a><br /><br />(.*?)</div>')
		plugintools.log("Sinopsis= "+sinopsis)
		datamovie = {}
		datamovie["Plot"]=sinopsis

		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&item=catcher%3dstreams%26url='+url_canal+'%26referer='+url_ref
		plugintools.add_item(action="runPlugin", title=titulo_canal, url=url_montada, thumbnail=caratula_canal, info_labels=datamovie , fanart=fanart, folder = False, isPlayable=True)


		
def ciberdocus3(params):
	plugintools.setview("tvshows")

	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	recursividad = params.get("extra")
	page = params.get("page")

	if len(page) <> 0 and recursividad == "vengo de otra busqueda":  # viene busqueda de cine, series y docus
		page = page.replace(" ", "+")
		url_busca="http://www.ciberdocumentales.com/index.php?keysrc="+page+"&categoria=0"
	else:
		if recursividad == "1":
			buscar=""
			buscar = plugintools.keyboard_input().replace(" ", "+")
			url_busca="http://www.ciberdocumentales.com/index.php?keysrc="+buscar+"&categoria=0"

		else:
			url_busca = params.get("url")

	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	data = plugintools.read(url_busca)	
	

	
	group_channel = plugintools.find_single_match(data,'var xajaxRequestUri="(.*?)<div id="paginador">')
	plugintools.log("group_channel= "+group_channel)
	cada_canal = plugintools.find_multiple_matches(group_channel,'<div class="fotonoticia">(.*?)>Ha sido visto')	

	for item in cada_canal:
		plugintools.log("item= "+item)
		
		url_canal=plugintools.find_single_match(item,'<div class="opcionesbot"><a target="_blank" href="(.*?)"')
		titulo_canal=plugintools.find_single_match(item,'alt="(.*?)"')
		caratula_canal='http://www.ciberdocumentales.com'+plugintools.find_single_match(item,'src="(.*?)"')

		##Capturo la Sinopsis en un Diccionario para usarla en "plugintools.add_item(" mediante la variable "info_labels"
		sinopsis = plugintools.find_single_match(item,'h3></a><br /><br />(.*?)</div>')
		plugintools.log("Sinopsis= "+sinopsis)
		datamovie = {}
		datamovie["Plot"]=sinopsis
		
		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&item=catcher%3dstreams%26url='+url_canal+'%26referer='+url_ref
		plugintools.add_item(action="runPlugin", title=titulo_canal, url=url_montada, thumbnail=caratula_canal, info_labels=datamovie , fanart=fanart, folder = False, isPlayable=True)

	
	if recursividad == "1":
		#Resuelvo la posibilidad de mas de 1 Página en la Busqueda
		
		mas_pag = plugintools.find_single_match(data,'<div class="pagination">(.*?)</div>')
		##Si no está vacio... es decir, q hay mas de 1 página
		if len(mas_pag) > 1:
			cadena_busqueda='/index.php?keysrc='+buscar+'&categoria=0&page='
			total_pag=plugintools.find_multiple_matches(mas_pag, 'a href="([^"]+)')
			#Con esto te devuelve una lista: ['/index.php?keysrc=cine&categoria=0&page=2', '/index.php?keysrc=cine&categoria=0&page=3', '/index.php?keysrc=cine&categoria=0&page=2']

			ult_pag=int(total_pag[-2].replace(cadena_busqueda, ""))
			
			for num_pag in range(2, ult_pag+1):
				recursividad="0"
				url_pag=url_ref+'index.php?keysrc='+buscar+'&categoria=0&page='+str(num_pag)  ## Obtengo las páginas así: http://www.ciberdocumentales.com/index.php?keysrc=cine&categoria=0&page=2
				print url_pag
				plugintools.add_item(action="ciberdocus3",title="[COLORFFFF0759]Página: " + str(num_pag) + "  >>>[/COLOR]", url=url_pag, extra=recursividad,  thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

		
	
