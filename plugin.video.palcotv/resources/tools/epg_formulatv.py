# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV EPG FórmulaTV.com
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#------------------------------------------------------------

import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import requests
import time
from datetime import datetime

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

tmp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
FANART = "fanart"
OTHER = "other"
MUSIC = "music"


def epg_ftv(title):
    plugintools.log('[%s %s].epg_ftv %s' % (addonName, addonVersion, title))
    channel = title.lower()
    channel = channel.replace("Opción 1", "").replace("HD", "").replace("720p", "").replace("1080p", "").replace("SD", "").replace("HQ", "").replace("LQ", "").strip()
    channel = channel.replace("Opción 2", "")
    channel = channel.replace("Opción 3", "")
    channel = channel.replace("Op. 1", "")
    channel = channel.replace("Op. 2", "")
    channel = channel.replace("Op. 3", "")
    plugintools.log("Canal a identificar: "+channel)
    params = plugintools.get_params()

    #tvdic = { "la 1": "la 1", "la 1 hd": "la 1", "la 2": "la 2", "antena 3": "antena 3 televisión", "antena 3 hd", "antena 3 televisión", "cuatro": "cuatro", "cuatro hd": "cuatro", "telecinco": "telecinco", "telecinco hd": "telecinco", "la sexta": "lasexta", "la sexta hd": "lasexta" }
              
    
    if channel == "la 1" or channel == "la 1 hd":
        channel = "la 1"
    elif channel == "la 2":
        channel = "la 2"
    elif channel == "antena 3" or channel == "antena 3 hd":
        channel = "antena 3 televisión"
    elif channel == "cuatro" or channel == "cuatro hd":
        channel = "cuatro"
    elif channel == "telecinco hd" or channel == "telecinco":
        channel == "telecinco"
    elif channel == "la sexta" or channel == "la sexta hd":
        channel = "lasexta"
    elif channel == "atreseries" or channel == "a3s" or channel == "a3series":
        channel = "atreseries"
    elif channel == "canal+1" or channel == "canal+ 1" or channel == "canal plus" or channel == "canal+ hd":
        channel = "canal+"
    elif channel == "canal+2" or channel == "canal+ 2" or channel == "canal plus 2" or channel == "canal+ 2 hd":
        channel = "canal+ 2"
    elif channel == "c+ acción" or channel == "canal+ acción":
        channel = "canal+ acción"
    elif channel == "canal+ estrenos" or channel == "c+ estrenos":
        channel = "canal+ estrenos"
    elif channel == "canal+ series":
        channel = "canal+ series"
    elif channel == "goltv" or channel == "golt":
        channel = "gol televisión"
    elif channel == "40 tv":
        channel = "40 tv"
    elif channel == "canal sur" or channel == "andalucia tv":
        channel = "canal sur"
    elif channel == "aragón tv" or channel == "aragon tv":
        channel = "aragon-television"
    elif channel == "axn" or channel == "axn hd":
        channel = "axn"
    elif channel == "axn white" or channel == "axn white hd":
        channel = "axn white"
    elif channel == "xtrm":
        channel = "xtrm"
    elif channel == "bio":
        channel = "bio"
    elif channel == "calle 13" or channel == "calle 13 hd":
        channel = "calle 13"
    elif channel == "amc" or channel == "amc españa" or channel == "amc hd":
        channel = "amc (españa)"
    elif channel == "canal barça" or channel == "canal barca":
        channel = "barça tv"
    elif channel == "andalucía tv" or channel == "andalucia tv":
        channel = "andalucia-tv"
    elif channel == "aragón tv" or channel == "aragon tv":
        channel = "aragon-television"
    elif channel == "axn" or channel == "axn hd":
        channel = "axn"
    elif channel == "bio":
        channel = "bio"
    elif channel == "canal barça" or channel == "canal barca":
        channel = "canal barca"
    elif channel == "canal+ 30" or channel == "canal+ ...30" or channel == "canal plus 30":
        channel = "canal+ 1... 30"
    elif channel == "canal+ accion" or channel == "canal+ acción" or channel=="canal plus accion" or channel == "c+ acción":
        channel = "canal+ acción"
    elif channel == "canal+ comedia" or channel == "canal plus comedia" or channel == "c+ comedia":
        channel = "canal+ comedia"
    elif channel == "canal+ decine" or channel == "canal plus decine":
        channel = "dcine español"
    elif channel == "canal+ deporte" or channel == "canal plus deporte":
        channel = "canal+ deporte"
    elif channel == "canal+ futbol" or channel == "canal+ fútbol" or channel == "canal plus fútbol" or channel == "canal plus futbol":
        channel = "canal+ fútbol"
    elif channel == "canal+ liga":
        channel = "canal+ liga"
    elif channel == "canal+ golf" or channel == "canal plus golf":
        channel = "golf+"
    elif channel == "canal+ toros" or channel == "canal plus toros":
        channel = "canal+ toros"
    elif channel == "canal+ extra" or channel=="canal+ xtra":
        channel = "canal+ xtra"
    elif channel == "canal 33" or channel == "canal33":
        channel = "canal33"
    elif channel == "canal cocina":
        channel = "canal cocina"
    elif channel == "cartoon network" or channel == "cartoon network hd":
        channel = "cartoon network"
    elif channel == "castilla-la mancha televisión" or channel == "castilla-la mancha tv":
        channel = "castilla-la-mancha"
    elif channel == "caza y pesca":
        channel = "caza-y-pesca"
    elif channel == "clan" or channel == "clan tve 50" or channel == "clan tve":
        channel = "clan tve"
    elif channel == "nickelodeon" or channel == "nickelodeon españa":
        channel = "nickelodeon (españa)"
    elif channel == "boing":
        channel = "boing"
    elif channel == "somos":
        channel = "somos"        
    elif channel == "cnbc":
        channel = "cnbc"
    elif channel == "cnn-international" or channel == "cnn int":
        channel = "cnn international"
    elif channel == "cosmopolitan" or channel == "cosmopolitan tv" or channel == "cosmopolitan hd" or channel == "cosmo" or channel == "cosmo hd":
        channel = "cosmopolitan"
    elif channel == "a&e" or channel == "a&e españa":
        channel = "a&e españa"
    elif channel == "canal+ dcine" or channel == "canal plus dcine" or channel == "dcine español":
        channel = "canal+ dcine"
    elif channel == "decasa":
        channel = "decasa"
    elif channel == "discovery channel" or channel=="discovery channel hd":
        channel = "discovery channel"
    elif channel == "national geographic" or channel == "national geographic hd":
        channel = "national geographic"
    elif channel == "discovery max":
        channel = "discovery max"
    elif channel == "disney channel" or channel == "disney channel hd":
        channel = "disney channel"
    elif channel == "disney cinemagic" or channel == "disney cinemagic hd":
        channel = "disney cinemagic"
    elif channel == "disney xd":
        channel = "disney xd"
    elif channel == "disney junior" or channel == "disney jr":
        channel = "disney junior"
    elif channel == "divinity":
        channel = "divinity"
    elif channel == "mega":
        channel = "mega"
    elif channel == "energy":
        channel = "energy"
    elif channel == "etb1" or channel == "etb 1":
        channel = "euskal telebista 1"
    elif channel == "etb 2" or channel == "etb2":
        channel = "euskal telebista 1"
    elif channel == "factoría de ficción" or channel == "factoria de ficcion" or channel == "fdf":
        channel = "fdf"
    elif channel == "buzz":
        channel = "buzz"
    elif channel == "fox life" or channel == "fox life hd":
        channel = "fox life"
    elif channel == "fox" or channel == "fox hd":
        channel = "fox-espana"        
    elif channel == "fox news":
        channel = "fox news"
    elif channel == "historia" or channel == "historia hd":
        channel = "canal de historia"
    elif channel == "natura" or channel == "canal natura":
        channel = "canal natura"
    elif channel == "cosmopolitan" or channel == "cosmopolitan tv":
        channel = "cosmopolitan"
    elif channel == "hollywood" or channel == "hollywood channel" or channel == "hollywood hd":
        channel = "canal hollywood"
    elif channel == "ib3 televisio" or channel == "ib3 televisió":
        channel = "ib3 televisio"
    elif channel == "intereconomia" or channel == "intereconomía" or channel == "intereconomía tv":
        channel = "intereconomia"
    elif channel == "mtv" or channel == "mtv españa" or channel == "mtv espana":
        channel = "mtv"
    elif channel == "sol música" or channel == "sol musica":
        channel = "sol música"
    elif channel == "nat geo wild" or channel == "nat geo wild hd":
        channel = "nat geo wild"
    elif channel == "neox":
        channel = "neox"
    elif channel == "nick jr." or channel == "nick jr":
        channel = "nick jr."
    elif channel == "odisea" or channel == "odisea hd":
        channel = "odisea"
    elif channel == "nova":
        channel = "nova"
    elif channel == "panda":
        channel = "panda"
    elif channel == "paramount channel":
        channel = "paramount channel"
    elif channel == "playboy tv":
        channel = "playboy tv"
    elif channel == "playhouse disney":
        channel = "playhouse disney"
    elif channel == "rtv murcia 7" or channel == "radiotelevisión de murcia" or channel == "rtv murcia":
        channel = "7 región de murcia"
    elif channel == "real madrid tv":
        channel = "real madrid tv"
    elif channel == "syfy" or channel== "syfy españa" or channel == "syfy hd":
        channel = "syfy españa"
    elif channel == "sony entertainment":
        channel = "sony entertainment"
    elif channel == "sportmania" or channel == "sportmania hd":
        channel = "sportmania"
    elif channel == "tcm" or channel == "tcm hd":
        channel = "tcm"
    elif channel == "comedy central" or channel == "comedy central hd":
        channel = "comedy central"
    elif channel == "teledeporte" or channel == "teledeporte hd":
        channel = "teledeporte"
    elif channel == "telemadrid" or channel == "telemadrid hd":
        channel = "telemadrid"
    elif channel == "televisión canaria" or channel == "televisión canaria":
        channel = "television canaria"
    elif channel == "televisión de galicia" or channel == "television de galicia" or channel == "tvg":
        channel = "tvg"
    elif channel == "tnt" or channel == "tnt hd":
        channel = "tnt españa"
    elif channel == "tv3" or channel == "tv3 hd":
        channel = "tv3"
    elif channel == "vh1":
        channel = "vh1"
    elif channel == "viajar":
        channel = "canal viajar"
    elif channel == "baby tv":
        channel = "baby tv"
    elif channel == "canal panda":
        channel = "canal panda"
    elif channel == "arenasports 1":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-1')
    elif channel == "arenasports 2":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-2')
    elif channel == "arenasports 3":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-3')
    elif channel == "arenasports 4":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-4')
    elif channel == "arenasports 5":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-5')
    elif channel == "sportklub 1" or channel == "sport klub 1":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-sport-klub-1')
    elif channel == "sportklub 2" or channel == "sport klub 2":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-sport-klub-2')
    
    params["url"]='http://www.formulatv.com/programacion/movistarplus/'
    plugintools.log("Canal: "+channel)
    if channel != "":
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    else: channel = channel
    
    


def epg_formulatv(params, channel):
    plugintools.log('[%s %s] Cargando EPG del canal %s de la web de FórmulaTV... %s' % (addonName, addonVersion, channel, repr(params)))
    thumbnail = params.get("thumbnail");url=params.get("url");fanart = params.get("extra")
    plugintools.log("Solicitamos EPG de: "+url)
    canal_buscado = channel.lower()
    canal_buscado= canal_buscado.replace(" hd", "")
    epg_channel = []
    params["plot"]=""

    backup_ftv = tmp + 'backup_ftv.txt' 
    if os.path.exists(backup_ftv):
        pass
    else:
        backup_epg = open(backup_ftv, "a")
        r=requests.get(url);backup_epg.write(r.content);backup_epg.close()

    # Abrimos backup
    backup_epg = open(backup_ftv, "r")
    data = backup_epg.read()
    
    # Calculando hora actual
    ahora = datetime.now()
    minutejo = str(ahora.minute)
    
    if ahora.minute < 10:  # Añadimos un cero delante del minuto actual por si es inferior a la decena
        minuto_ahora = '0'+str(ahora.minute)
    else:
        minuto_ahora = str(ahora.minute)
       
    hora_ahora = str(ahora.hour)+":"+minuto_ahora
    epg_channel.append(hora_ahora)   # index 0              
            
    # Vamos a leer la fuente de datos
    body = plugintools.find_multiple_matches(data, '<td class="prga-d">(.*?)</tr>')    
    for entry in body:
        plugintools.log("entry= "+entry)
        channel = plugintools.find_single_match(entry, 'title=\"([^"]+)')
        if channel == "": channel = plugintools.find_single_match(entry, 'alt=\"([^"]+)')
        channel = channel.lower()
        plugintools.log("Buscando canal: "+canal_buscado)
        plugintools.log("Channel: "+channel)
        if channel == canal_buscado:
            print 'channel',channel
            evento_ahora = plugintools.find_single_match(entry, '<p>(.*?)</p>')
            epg_channel.append(evento_ahora)   # index 1            
            hora_luego = plugintools.find_single_match(entry, 'class="fec1">(.*)</span>')
            hora_luego = hora_luego.split("</span>")
            hora_luego = hora_luego[0]
            print 'hora_luego',hora_luego
            epg_channel.append(hora_luego)   # index 2
            diff_luego = plugintools.find_single_match(entry, 'class="fdiff">([^<]+)').strip()
            print 'diff_luego',diff_luego
            epg_channel.append(diff_luego)   # index 3 
            evento_luego = plugintools.find_single_match(entry, '<span class="tprg1">(.*?)</span>')
            print 'evento_luego',evento_luego
            epg_channel.append(evento_luego)   # index 4 
            hora_mastarde = plugintools.find_single_match(entry, 'class="fec2">(.*)</span>')
            hora_mastarde = hora_mastarde.split("</span>")
            hora_mastarde = hora_mastarde[0]
            print 'hora_mastarde',hora_mastarde
            epg_channel.append(hora_mastarde)   # index 5 
            evento_mastarde = plugintools.find_single_match(entry, '<span class="tprg2">(.*?)</span>')
            print 'evento_mastarde',evento_mastarde
            epg_channel.append(evento_mastarde)    # index 6            
            sinopsis = '[COLOR lightgreen][I]('+str(diff_luego)+') [/I][/COLOR][COLOR white][B]'+str(hora_luego)+' [/COLOR][/B]'+str(evento_luego)+'[CR][COLOR white][B][CR]'+str(hora_mastarde)+' [/COLOR][/B] '+str(evento_mastarde)
            print sinopsis
            plugintools.log("Sinopsis: "+sinopsis)
            datamovie = {}
            datamovie["Plot"]=sinopsis
            #plugintools.add_item(action="", title= '[COLOR orange][B]'+channel+' [/B][COLOR lightyellow]'+str(ahora)+'[/COLOR] [COLOR lightgreen][I]('+str(diff_luego)+') [/I][/COLOR][COLOR white][B]'+str(hora_luego)+' [/COLOR][/B] '+str(evento_luego), info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
            #plugintools.log("entry= "+entry)
            return epg_channel            
        



# Petición de la URL
def gethttp_headers(params):
    plugintools.log('[%s %s].gethttp_headers %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",'http://www.digitele.com/pluginfiles/canales/'])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    return body                    

    
        
        
    
    
