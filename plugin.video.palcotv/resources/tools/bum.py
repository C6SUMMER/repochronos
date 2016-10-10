# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Buscador Unificado de Magnets para PalcoTV
# Version 0.2 (03.11.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#------------------------------------------------------------
# TODO:
# Añadir pestaña en configuración con nombres de dominio (cambian frecuentemente)
# Recuperar Limetorrents y Monova (Cloudflare)
# Crear opciones de búsqueda individuales
# Acortar extensión de título si excede del ancho de pantalla --> ¡Mostrar info en sinopsis!
# Comprobar que se lista en orden descendente
# Cambiar orden de variables para mejorar aspecto visual (seeds, leechs, size, server)
#------------------------------------------------------------


from __main__ import *

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

import re,urllib,urllib2,sys
import plugintools,requests

from __main__ import *
from resources.tools.media_analyzer import launch_torrent
from resources.tools.media_analyzer import launch_magnet

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))
s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Language':'es-ES,es;q=0.8,ro;q=0.6,en;q=0.4,gl;q=0.2','Accept-Encoding':'gzip, deflate, sdch','Connection':'keep-alive','Upgrade-Insecure-Requests':'1'};

thumbnail = 'http://static.myce.com/images_posts/2011/04/kickasstorrents-logo.jpg'
fanart = 'https://yuq.me/users/19/529/lcqO6hj0XK.png'
show_bum = plugintools.get_setting("bum_id")

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

kurl=plugintools.get_setting("kurl")
bsurl=plugintools.get_setting("bsurl")
tdurl=plugintools.get_setting("tdurl")
lmurl=plugintools.get_setting("lmurl")
ihurl=plugintools.get_setting("ihurl")

def bum_multiparser(params):
    plugintools.log('[%s %s] Iniciando BUM+ ... %s' % (addonName, addonVersion, repr(params)))
    
    # Archivo de control de resultados
    bumfile = temp + 'bum.dat'
    if not os.path.isfile(bumfile):  # Si no existe el archivo de control, se crea y se anotan resultados de la búsqueda
        controlbum = open(bumfile, "wb")
        controlbum.close()    

    texto = parser_title(params.get("title"))
    texto = texto.replace("[Multiparser]", "").replace("[/COLOR]", "").replace("[I]", "").replace("[/I]", "").replace("[COLOR white]", "").replace("[COLOR lightyellow]", "").strip()
    lang = plugintools.get_setting("bum_lang")
    if lang == '0':
        lang = ""            
    elif lang == '1':
        lang = 'spanish'
    elif lang == '2':
        lang = 'english'
    elif lang == '3':
        lang = 'french'
    elif lang == '4':
        lang = 'german'
    elif lang == '5':
        lang = 'latino'

    if lang != "": texto = texto+' ' + lang
    else: texto=texto.strip()
    
    plugintools.set_setting("bum_search",texto)
    params["plot"]=parser_title(texto)
    texto = texto.lower().strip()
    texto = texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
    if texto == "": errormsg = plugintools.message("Arena+","Por favor, introduzca el canal a buscar")
    else:
        url = kurl+'usearch/'+texto+'/'  # Kickass
        params["url"]=url            
        url = params.get("url")
        referer = 'http://www.kat.cr'
        kickass1_bum(params)
        url = bsurl+'search/all/'+texto+'/c/d/1/'  # BitSnoop
        params["url"]=url            
        url = params.get("url")
        referer = 'http://www.bitsnoop.com'
        bitsnoop1_bum(params)
        url = ihurl+'torrents/?ihq='+texto.replace(" ", "+").strip()+'&Torrent_sort=-seeders'  # Isohunt
        params["url"]=url            
        url = params.get("url")
        referer = 'https://isohunt.to'
        isohunt1_bum(params)        
        url = lmurl+'/search/all/'+texto.replace(" ", "-").strip()+'/seeds/1/'
        params["url"]=url
        limetorrents1(params)
        
    controlbum = open(bumfile, "r")
    num_items = len(controlbum.readlines())
    fanart = 'http://images5.fanpop.com/image/photos/29400000/Massive-B-Horror-Collage-Wallpaper-horror-movies-29491579-2560-1600.jpg'

    i = -1
    controlbum.seek(0)
    while i <= num_items:        
        data = controlbum.readline()
        if data.startswith("EOF") == True:
            break
        elif data.startswith("Title") == True:
            title=data.replace("Title: ", "")
            url=controlbum.readline();url=url.replace("URL: ","")
            thumbnail=controlbum.readline();thumbnail=thumbnail.replace("Thumbnail: ", "").strip()
            seeds=controlbum.readline();seeds=seeds.replace("Seeds: ", "").replace(",", "").replace(".", "").strip()
            size=controlbum.readline();size=size.replace("Size: ", "").strip()
            seeds_min=plugintools.get_setting("bum_seeds");seeds_min=int(seeds_min)
            if seeds >= seeds_min:
                if thumbnail == "":
                    thumbnail = art + 'bum.png'                
                if title.find("[Kickass][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="launch_magnet", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[BitSnoop][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="bitsnoop2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[IsoHunt][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="isohunt2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[LimeTorrents][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="limetorrents1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue            
        else:
            i=i+1
            continue

    controlbum.close()
    xbmcplugin.addSortMethod(int(sys.argv[1]), 2)
    plugintools.setview(show_bum)

    # Eliminamos archivo de registro
    try:
        if os.path.exists(bumfile):
            os.remove(bumfile)
    except: pass
    
    xbmc.executebuiltin("Container.SetViewMode(51)")


def bum_linker(params):
    plugintools.log('[%s %s] Iniciando BUM+ ... %s' % (addonName, addonVersion, repr(params)))

    # Archivo de control de resultados
    bumfile = temp + 'bum.dat'
    if not os.path.isfile(bumfile):  # Si no existe el archivo de control, se crea y se anotan resultados de la búsqueda
        controlbum = open(bumfile, "wb")
        controlbum.close()

    texto=params.get("extra").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
    plugintools.set_setting("bum_search",texto)
    params["plot"]=texto
    url = 'https://kat.cr/usearch/'+texto+'/'  # Kickass
    params["url"]=url            
    url = params.get("url")
    referer = 'http://www.kat.cr'
    kickass1_bum(params)
    
    url = bsurl+'search/all/'+texto  # BitSnoop
    params["url"]=url            
    url = params.get("url")
    referer = 'http://www.bitsnoop.com'
    try: bitsnoop1_bum(params)
    except: pass
    
    url = ihurl+'torrents/?ihq='+texto.replace(" ", "+").strip()  # Isohunt
    params["url"]=url            
    #url = params.get("url")
    referer = 'https://isohunt.to'
    try: isohunt1_bum(params)
    except: pass
    
    url = lmurl+'search/all/'+texto.replace(" ", "-").strip()  #Limetorrents
    params["url"]=url
    try: limetorrents1(params)
    except: pass
    
    url = tdurl+'search/?search='+texto.replace(" ", "+").strip()  # Torrent Downloads
    params["url"]=url
    try: tordls0(params)
    except: pass

    url = 'http://torrentz.eu/search?q='+texto.replace(" ", "+").strip()  #Torrentz.eu
    params["url"]=url
    torrentz0(params)
        
    controlbum = open(bumfile, "r")
    num_items = len(controlbum.readlines())
    fanart = 'http://images5.fanpop.com/image/photos/29400000/Massive-B-Horror-Collage-Wallpaper-horror-movies-29491579-2560-1600.jpg'

    i = -1
    controlbum.seek(0)
    while i <= num_items:        
        data = controlbum.readline()
        if data.startswith("EOF") == True:
            break
        elif data.startswith("Title") == True:
            title=data.replace("Title: ", "")
            url=controlbum.readline();url=url.replace("URL: ","")
            thumbnail=controlbum.readline();thumbnail=thumbnail.replace("Thumbnail: ", "").strip()
            seeds=controlbum.readline();seeds=seeds.replace("Seeds: ", "").replace(",", "").replace(".", "").strip()
            size=controlbum.readline();size=size.replace("Size: ", "").strip()
            seeds_min=plugintools.get_setting("bum_seeds");seeds_min=int(seeds_min)
            if seeds >= seeds_min:
                if thumbnail == "":
                    thumbnail = art + 'bum.png'                
                if title.find("[Kickass][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="launch_magnet", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[BitSnoop][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="bitsnoop2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[IsoHunt][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="isohunt2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[LimeTorrents][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="limetorrents1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[Torrent Downloads][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="tordls1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[Torrentz.eu][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="torrentz1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue                 
        else:
            i=i+1
            continue

    controlbum.close()
    xbmcplugin.addSortMethod(int(sys.argv[1]), 2)
    plugintools.setview(show_bum)

    # Eliminamos archivo de registro
    try:
        if os.path.exists(bumfile):
            os.remove(bumfile)
    except: pass
    
    xbmc.executebuiltin("Container.SetViewMode(51)")
    xbmcplugin.addSortMethod(int(sys.argv[1]), 1)



def kickass0_bum(params):
    plugintools.log('[%s %s] [BUM+] Kickass... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)    

    try:
        texto = params.get("plot");texto=parser_title(texto)        
        if texto == "":
            errormsg = plugintools.message("Arena+","Por favor, introduzca el canal a buscar")
        else:           
            texto = texto.lower().strip()
            url = 'https://kat.cr/usearch/'+texto+'/'
            plugintools.log("URL Kickass= "+url)
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.kat.cr/'            
    except:
         pass      

    # Archivo de control de resultados (evita la recarga del cuadro de diálogo de búsqueda tras cierto tiempo)
    bumfile = temp + 'bum.dat'
    if not os.path.isfile(bumfile):  # Si no existe el archivo de control, se crea y se registra la búsqueda
        controlbum = open(bumfile, "a")
        controlbum.close()
        ahora = datetime.now()
        anno_actual = ahora.year
        mes_actual = ahora.month
        hora_actual = ahora.hour
        min_actual = ahora.minute
        seg_actual = ahora.second
        hoy = ahora.day
        # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
        if hoy <= 9:
            hoy = "0" + str(hoy)
        if mes_actual <= 9:
            mes_actual = "0" + str(ahora.month)
        timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
        controlbum = open(temp + 'bum.dat', "a")
        controlbum.seek(0)
        controlbum.write(timestamp+":"+texto)
        controlbum.close()
    else:
        controlbum = open(temp + 'bum.dat', "r")
        controlbum.seek(0)
        data = controlbum.readline()
        controlbum.close()        
        plugintools.log("BUM+= "+data)           
        plugintools.log("Control de BUM+ activado. Analizamos timestamp...")
        data = data.split(":")
        timestamp = data[0]
        term_search = data[1]
        ahora = datetime.now()
        anno_actual = ahora.year
        mes_actual = ahora.month
        hora_actual = ahora.hour
        min_actual = ahora.minute
        seg_actual = ahora.second
        hoy = ahora.day
        # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
        if hoy <= 9:
            hoy = "0" + str(hoy)
        if mes_actual <= 9:
            mes_actual = "0" + str(ahora.month)
        timenow = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
        # Comparamos valores (hora actual y el timestamp del archivo de control)
        if term_search == texto:
            result = int(timenow) - int(timestamp)
            if result > 90:  # Control fijado en 90 segundos; esto significa que una misma búsqueda no podremos realizarla en menos de 90 segundos, y en ese tiempo debe reproducirse el torrent
                # Borramos registro actual y guardamos el nuevo (crear una función que haga esto y no repetir!)
                ahora = datetime.now()
                anno_actual = ahora.year
                mes_actual = ahora.month
                hora_actual = ahora.hour
                min_actual = ahora.minute
                seg_actual = ahora.second
                hoy = ahora.day
                # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
                if hoy <= 9:
                    hoy = "0" + str(hoy)
                if mes_actual <= 9:
                    mes_actual = "0" + str(ahora.month)
                timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
                controlbum = open(temp + 'bum.dat', "a")
                controlbum.seek(0)
                controlbum.write(timestamp+":"+texto)
                controlbum.close()                
                kickass_results(params)
            else:
                kickass_results(params)
        else:
            # Borramos registro actual y guardamos el nuevo (crear una función que haga esto y no repetir!)
            ahora = datetime.now()
            anno_actual = ahora.year
            mes_actual = ahora.month
            hora_actual = ahora.hour
            min_actual = ahora.minute
            seg_actual = ahora.second
            hoy = ahora.day
            # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
            if hoy <= 9:
                hoy = "0" + str(hoy)
            if mes_actual <= 9:
                mes_actual = "0" + str(ahora.month)
            timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
            controlbum = open(temp + 'bum.dat', "a")
            controlbum.seek(0)
            controlbum.write(timestamp+":"+texto)
            controlbum.close()                
            kickass1_bum(params)

    xbmc.executebuiltin("Container.SetViewMode(518)")
                
                
                
def kickass1_bum(params):
    plugintools.log('[%s %s] [BUM+] Kickass results... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)    
    bumfile = temp + 'bum.dat'
    controlbum = open(bumfile, "a")    
    plugintools.setview(show_bum)
    url=params.get("url")
    plugintools.log("KURL= "+url)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", kurl])    
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    thumbnail = plugintools.find_single_match(data, '<img src="([^"]+)')
    thumbnail = 'http:'+thumbnail
    match_num_results = plugintools.find_single_match(data, '<div><h2>(.*?)</a></h2>')
    num_results = plugintools.find_single_match(match_num_results, '<span>(.*?)</span>')
    num_results = num_results.replace("from", "de").replace("results", "Resultados:").strip()
    results = plugintools.find_single_match(data, '<table width="100%" cellspacing="0" cellpadding="0" class="doublecelltable" id="mainSearchTable">(.*?)</table>')
    matches = plugintools.find_multiple_matches(results, '<div class="torrentname">(.*?)<a data-download')
    for entry in matches:
        match_title = plugintools.find_single_match(entry, 'class="cellMainLink">(.*?)</a>')
        match_title = match_title.replace("</strong>", "").replace("<strong>", "").replace('<strong class="red">', "").strip()
        magnet_match = 'magnet:'+plugintools.find_single_match(entry, "magnet:([^']+)").strip()
        plugintools.log("magnet_match= "+magnet_match)
        size = plugintools.find_single_match(entry, 'class=\"nobr center\">(.*?)</td>')
        size = size.replace("<span>","").replace("</span>","").strip()
        seeds = plugintools.find_single_match(entry, '<td class="green center">(.*?)</td>').replace(",", "").replace(".", "")
        leechs = plugintools.find_single_match(entry, '<td class="red lasttd center">(.*?)</td>')
        title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+match_title+' [I]['+size + '] [/COLOR][COLOR orange][Kickass][/I][/COLOR]'
        if seeds > 0:
            controlbum.write('Title: '+title_fixed+'\nURL: '+magnet_match+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeds+'\nSize: '+size+'\n\n')

    controlbum.close()
    xbmc.executebuiltin("Container.SetViewMode(518)")

                            

def bitsnoop0_bum(params):
    plugintools.log('[%s %s] [BUM+] BitSnoop... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)    

    try:
        texto = "";
        texto='riddick'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("Arena+","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # http://bitsnoop.com/search/all/the+strain+spanish/c/d/1/
            url = 'http://bitsnoop.com/search/all/'+texto+'/c/d/1/'
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.bitsnoop.com'
            bitsnoop1_bum(params)
    except:
         pass

    xbmc.executebuiltin("Container.SetViewMode(518)")




def bitsnoop1_bum(params):
    plugintools.log('[%s %s] [BUM+] BitSnoop results... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)
    
    thumbnail = 'http://upload.wikimedia.org/wikipedia/commons/9/97/Bitsnoop.com_logo.png'
    fanart = 'http://wallpoper.com/images/00/41/86/68/piracy_00418668.jpg'

    # Abrimos archivo de registro
    bumfile = temp + 'bum.dat'
    controlbum = open(bumfile, "a")
    plugintools.setview(show_bum)
    url = params.get("url")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", "https://bitsnoop.com/"])    
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    print data
    results = plugintools.find_single_match(data, '<ol id="torrents" start="1">(.*?)</ol>')
    matches = plugintools.find_multiple_matches(results, '<span class="icon cat_(.*?)</div></td>')
    i = 0
    for entry in matches:
        i = i + 1
        page_url = plugintools.find_single_match(entry, 'a href="([^"]+)')
        title_url = plugintools.find_single_match(entry, 'a href="(.*?)</a>')
        title_url = title_url.replace(page_url, "").replace("<span class=srchHL>", "").replace('">', "").replace("<b class=srchHL>", "[COLOR white]").replace("</b>", "[/COLOR]").strip()
        page_url = 'http://bitsnoop.com'+page_url
        seeders = plugintools.find_single_match(entry, 'title="Seeders">(.*?)</span>').replace(",", "").replace(".", "")
        plugintools.log("seeders= "+seeders)
        leechers = plugintools.find_single_match(entry, 'title="Leechers">(.*?)</span>')
        size = plugintools.find_single_match(entry, '<tr><td align="right" valign="middle" nowrap="nowrap">(.*?)<div class="nfiles">')
        if seeders == "":  # Verificamos el caso en que no haya datos de seeders/leechers
            seeders = "0"
        if leechers == "":
            leechers = "0"            
        stats = '[COLOR gold][I]['+seeders+'/'+leechers+'][/I][/COLOR]'
        title_fixed=stats+'  [COLOR white]'+title_url+' [I]['+size+'] [/COLOR][COLOR red][BitSnoop][/I][/COLOR]'
        if seeders > 0: controlbum.write('Title: '+title_fixed+'\nURL: '+page_url+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeders+'\nSize: '+size+'\n\n')

    controlbum.close()
    xbmc.executebuiltin("Container.SetViewMode(518)")



def bitsnoop2_bum(params):
    plugintools.log('[%s %s] [BUM+] BitSnoop getlink... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)
    
    url = params.get("url")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", "https://bitsnoop.com/"])    
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    print data
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match
    plugintools.log("Magnet: "+magnet_match)
    params["url"]=magnet_match
    launch_magnet(params)
    xbmc.executebuiltin("Container.SetViewMode(518)")
    

def isohunt0_bum(params):
    plugintools.log('[%s %s] [BUM+] Isohunt... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)    

    thumbnail = 'http://www.userlogos.org/files/logos/dfordesmond/isohunt%201.png'
    fanart = 'http://2.bp.blogspot.com/_NP40rzexJsc/TMGWrixybJI/AAAAAAAAHCU/ij1--_DQEZo/s1600/Keep_Seeding____by_Carudo.jpg'    
    plugintools.setview(show_bum)
    
    try:
        texto = "";
        texto='riddick'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("Arena+","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://isohunt.to/torrents/?ihq='+texto+'&Torrent_sort=seeders.desc'
            params["url"]=url            
            url = params.get("url")
            referer = 'https://isohunt.to'
            isohunt1_bum(params)
    except:
         pass
    xbmc.executebuiltin("Container.SetViewMode(518)")


def isohunt1_bum(params):
    plugintools.log('[%s %s] [BUM+] Isohunt results... %s' % (addonName, addonVersion, repr(params)))
    plugintools.setview(show_bum)
    thumbnail = 'http://www.userlogos.org/files/logos/dfordesmond/isohunt%201.png'
    fanart = 'http://2.bp.blogspot.com/_NP40rzexJsc/TMGWrixybJI/AAAAAAAAHCU/ij1--_DQEZo/s1600/Keep_Seeding____by_Carudo.jpg' 

    # Abrimos archivo de registro
    bumfile = temp + 'bum.dat'
    controlbum = open(bumfile, "a")    
    url = params.get("url")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", "https://isohunt.to/"])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)  
    matches = plugintools.find_multiple_matches(data, '<tr data-key="(.*?)</td></tr>')    
    for entry in matches:
        page_url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        page_url = 'https://isohunt.to'+page_url
        title_url = plugintools.find_single_match(entry, '<span>(.*?)</span>')
        size = plugintools.find_single_match(entry, '<td class="size-row">(.*?)</td>')
        seeds = plugintools.find_single_match(entry, '<td class="sy">(.*?)</td>').replace(",", "").replace(".", "");leechs = '?'
        category = plugintools.find_single_match(entry, 'title="([^"]+)')
        title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+title_url+' [I]['+size+'] [/COLOR][COLOR lightblue][IsoHunt][/I][/COLOR]'
        if seeds > 0: controlbum.write('Title: '+title_fixed+'\nURL: '+page_url+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeds+'\nSize: '+size+'\n\n')

    controlbum.close()
    xbmc.executebuiltin("Container.SetViewMode(518)")
            
            

def isohunt2_bum(params):
    plugintools.log('[%s %s] [BUM+] Isohunt getlink... %s' % (addonName, addonVersion, repr(params)))    
    plugintools.setview(show_bum)  
    url = params.get("url")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", "https://isohunt.to/"])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match.strip()
    params["url"]=magnet_match
    launch_magnet(params)
    xbmc.executebuiltin("Container.SetViewMode(518)")


def monova0_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova... %s' % (addonName, addonVersion, repr(params)))
    plugintools.setview(show)    
    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    plugintools.setview(show)
    
    try:
        texto = "";
        texto='the strain spanish'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("Arena+","Por favor, introduzca el término a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://www.monova.org/search.php?sort=5&term='+texto+'&verified=1'
            params["url"]=url            
            url = params.get("url")
            referer = 'https://monova.org'
            monova1_bum(params)
    except:
         pass
    xbmc.executebuiltin("Container.SetViewMode(518)")


def monova1_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova results... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)    
    url = params.get("url")
    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", "https://www.monova.org/"])
    print data
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)       
    block_matches = plugintools.find_single_match(data, '<table id="resultsTable"(.*?)<div id="hh"></div>')
    plugintools.log("block_matches= "+block_matches)
    matches = plugintools.find_multiple_matches(block_matches, '<div class="torrentname(.*?)</div></td></tr>')
    for entry in matches:
        plugintools.log("entry= "+entry)
        if entry.find("Direct Download") >= 0:  # Descartamos resultados publicitarios 'Direct Download' que descargan un .exe
            plugintools.log("Direct Download = Yes")
        else:
            plugintools.log("Direct Download = No")
            page_url = plugintools.find_single_match(entry, 'a href="([^"]+)')
            title_url = plugintools.find_single_match(entry, 'title="([^"]+)')
            size_url = plugintools.find_single_match(entry, '<div class="td-div-right pt1">(.*?)</div>')
            seeds = plugintools.find_single_match(entry, '<td class="d">(.*?)<td align="right" id="encoded-').replace(",", "").replace(".", "")
            seeds = seeds.replace("</td>", "")
            seeds = seeds.split('<td class="d">')
            #seeds = seeds.replace('<td align="right" id="encoded-10"', "")
            #seeds = seeds.replace('<td id="encoded-10" align="right"', "")
            try:
                if len(seeds) >= 2:
                    semillas = '[COLOR gold][I]['+seeds[0]+'/'+seeds[1]+'][/I][/COLOR]'
            except:
                pass        

            plugintools.add_item(action="monova2_bum", title = semillas+'  '+title_url+' [COLOR lightgreen][I][ '+size_url+'][/I][/COLOR] ', url = page_url , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = True)

    xbmc.executebuiltin("Container.SetViewMode(518)")
            
            

def monova2_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova getlink... %s' % (addonName, addonVersion, repr(params)))
    plugintools.setview(show_bum) 
    url = params.get("url")    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", "https://www.monova.org/"])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)   
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match
    params["url"]=magnet_match
    launch_magnet(params)
    xbmc.executebuiltin("Container.SetViewMode(518)")
    

def limetorrents0_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova... %s' % (addonName, addonVersion, repr(params)))
    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    
    try:
        texto = "";
        texto='the strain spanish'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("Arena+","Por favor, introduzca el término a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://www.limetorrents.cc/search/all/'+texto.replace(" ", "+").strip()+'/seeds/1/'
            params["url"]=url            
            limetorrents1_bum(params)
    except:
         pass
    xbmc.executebuiltin("Container.SetViewMode(518)")


def limetorrents1(params):
    plugintools.log('[%s %s] [BUM+] LimeTorrents loading... %s' % (addonName, addonVersion, repr(params)))

    burl = 'https://www.limetorrents.cc';url=params.get("url")
    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0','Referer': "https://www.limetorrents.cc",'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language':'es-ES,es;application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;q=0.8,ro;q=0.6,en;q=0.4,gl;q=0.2','Accept':'text/html,','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive','Upgrade-Insecure-Requests':'1','front-end-https':"on"};
    b=s.get(url, headers=s.headers, allow_redirects=False);
    headers=b.headers;cookies=b.cookies;data=b.text;print data
    #cookies: <<class 'requests.cookies.RequestsCookieJar'>[<Cookie __cfduid=d75a112e58a5333964b66daa33ff4332f1461839880 for .limetorrents.cc/>]>  ... no hay requisitos, ok!
    #headers: {'Transfer-Encoding': 'chunked', 'Set-Cookie': '__cfduid=d75a112e58a5333964b66daa33ff4332f1461839880; expires=Fri, 28-Apr-17 10:38:00 GMT; path=/; domain=.limetorrents.cc; HttpOnly', 'Server': 'cloudflare-nginx', 'Connection': 'keep-alive', 'Location': 'https://limetorrents.cc/search/all/juego+de+tronos', 'Date': 'Thu, 28 Apr 2016 10:38:01 GMT', 'CF-RAY': '29a9e1d784d62f3b-MAD', 'Content-Type': 'text/html'}

    #headers=s.headers.update({'Cookie':cookies,'Referer':'https://www.limetorrents.cc/'})
    #https://ajax.cloudflare.com/cdn-cgi/nexp/dok3v=e982913d31
    #cloudf='https://owen.ns.cloudflare.com'+plugintools.find_single_match(data, 'cloudflare:"(.*?)/"');print cloudf
    #b=s.get(cloudf, headers=s.headers, allow_redirects=False);data=b.text;print data,b.cookies
    bumfile = temp + 'bum.dat'
    controlbum = open(bumfile, "a")
    results = plugintools.find_single_match(data, '<h2>Search Results(.*?)Next page')
    matches = plugintools.find_multiple_matches(results, '<div class="tt-name">(.*?)<td class="tdleft">')
    for entry in matches:
        if entry.find("Verified torrent") >= 0:
            page_url = burl + plugintools.find_single_match(entry, '</a><a href="([^"]+)')
            match_title = plugintools.find_single_match(entry, '.html">([^<]+)')
            seeds = plugintools.find_single_match(entry, '<td class="tdseed">(.*?)</td>').replace(",", "").replace(".", "")
            leechs = plugintools.find_single_match(entry, '<td class="tdleech">(.*?)</td>').replace(",", "").replace(".", "")
            size = plugintools.find_single_match(entry, '</a></td><td class="tdnormal">(.*?)B</td>')+'B'
            thumbnail='https://torrentfreak.com/images/limetorrents.jpg'
            plugintools.log("size= "+size)
            title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+match_title+' [I]['+size + '] [/COLOR][COLOR lime][LimeTorrents][/I][/COLOR]'
            if seeds > 0: controlbum.write('Title: '+title_fixed+'\nURL: '+page_url+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeds+'\nSize: '+size+'\n\n')

    #controlbum.write("\n\n\nEOF\n\n")
    controlbum.close()
            


def pbay0(params):
    plugintools.log('[%s %s] [BUM+] Pirate Bay... %s' % (addonName, addonVersion, repr(params)))
    thumbnail=params['thumbnail'];fanart=params.get("fanart");cookie=''
    url='https://thepiratebay.cr/search/Super%20Rugby/0/7/0'
    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': "https://thepiratebay.cr/"}
    b=s.get(url, verify=False)
    resp=b.text;heads=b.headers;cook=b.cookies;print cook
    for cookies in cook:cookie+=cookies.name+'='+cookies.value+'; ';
    s.headers.update({'Cookie':cookie})
    print cookie
    if cookie:
        print resp.encode('utf-8','ignore')



def tordls0(params):
    plugintools.log('[%s %s] [BUM+] Torrent Downloads... %s' % (addonName, addonVersion, repr(params)))
    thumbnail=params['thumbnail'];fanart=params.get("fanart");
    burl='http://www.torrentdownloads.me'
    burl_tordls = params.get("url")
    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': "https://www.torrentdownloads.me/"}
    b=s.get(burl_tordls, allow_redirects=False);cookie=''
    resp=b.text;heads=b.headers;cook=b.cookies;print cook
    for cookies in cook:
        cookie+=cookies.name+'='+cookies.value+'; ';s.headers.update({'Cookie':cookie});print cookie
    if cookie:
        data=resp.encode('utf-8','ignore')
        bumfile = temp + 'bum.dat';controlbum = open(bumfile, "a")  # Abrimos archivo de registro
        items=plugintools.find_multiple_matches(data, '<div class="grey_bar3"><p>(.*?)</span></div>')
        for entry in items:
            page_url = burl + plugintools.find_single_match(entry, 'href="([^"]+)')
            title=plugintools.find_single_match(entry, 'title="View torrent info :(.*?)">')
            thumbnail='http://www.spainjapanyear.com/templates/new/images/logo.png'
            try:
                seeds=plugintools.find_multiple_matches(entry, '<span>(.*?)</span>')[0].replace("&nbsp;", "").strip()
                leechs=plugintools.find_multiple_matches(entry, '<span>(.*?)</span>')[1].replace("&nbsp;", "").strip()
                size=plugintools.find_multiple_matches(entry, '<span>(.*?)</span>')[2].replace("&nbsp;", "").strip()
            except: seeds="?";leechs="?";size="?"
            if title!= "":
                title_fixed=title+" "+seeds+"/"+leechs+" ("+size+")"
                title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+title+' [I]['+size + '] [/COLOR][COLOR lightgreen][Torrent Downloads][/I][/COLOR]'
                #plugintools.add_item(action="tordls1", title=title_fixed, url=page_url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
                if seeds > 0: controlbum.write('Title: '+title_fixed+'\nURL: '+page_url+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeds+'\nSize: '+size+'\n\n')

        controlbum.close()
        xbmc.executebuiltin("Container.SetViewMode(518)")        

                 


def tordls1(params):
    plugintools.log('[%s %s] [BUM+] Torrent Downloads... %s' % (addonName, addonVersion, repr(params)))

    url=params.get("url")
    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': "https://www.torrentdownloads.me/"}
    b=s.get(url, allow_redirects=False);cookie=''
    resp=b.text;heads=b.headers;cook=b.cookies;print cook
    for cookies in cook:
        cookie+=cookies.name+'='+cookies.value+'; ';s.headers.update({'Cookie':cookie});print cookie
    if cookie:
        data=resp.encode('utf-8','ignore');print data
        bloque_url=plugintools.find_single_match(data, '<span>Magnet:(.*?)</a></p></div>');url=plugintools.find_single_match(bloque_url, 'href="([^"]+)').strip()
        plugintools.log("URL Magnet= "+url)
        params["url"]=url
        launch_magnet(params)


def torrentz0(params):
    plugintools.log('[%s %s] [BUM+] Torrentz.eu... %s' % (addonName, addonVersion, repr(params)))
    thumbnail=params['thumbnail'];fanart=params.get("fanart");
    burl='http://www.torrentz.eu'
    url = params.get("url")
    r=requests.get(url);resp=r.text;data=resp.encode('utf-8','ignore')
    
    bumfile = temp + 'bum.dat';controlbum = open(bumfile, "a")  # Abrimos archivo de registro
    items=plugintools.find_multiple_matches(data, '<dl>(.*?)</dl>')
    for entry in items:
        page_url = burl + plugintools.find_single_match(entry, 'href="([^"]+)')
        title=plugintools.find_single_match(entry, '<a href[^>]+>(.*?)</dt>').replace("<b>", "").replace("</b>", "").strip()
        thumbnail='http://images-mediawiki-sites.thefullwiki.org/11/1/5/0/02862953748359480.png'
        try:
            size=plugintools.find_single_match(entry, '<span class="s">(.*?)</span>')
            seeds=plugintools.find_single_match(entry, '<span class="u">(.*?)</span>')
            leechs=plugintools.find_single_match(entry, '<span class="d">(.*?)</span>')
        except: seeds="?";leechs="?";size="?"
        if title!= "":
            title_fixed=title+" "+seeds+"/"+leechs+" ("+size+")"
            title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+title+' [I]['+size + '] [/COLOR][COLOR yellow][Torrentz.eu][/I][/COLOR]'
            #plugintools.add_item(action="tordls1", title=title_fixed, url=page_url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
            if seeds > 0: controlbum.write('Title: '+title_fixed+'\nURL: '+page_url+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeds+'\nSize: '+size+'\n\n')


    controlbum.write("\n\n\nEOF\n\n")
    controlbum.close()
    xbmc.executebuiltin("Container.SetViewMode(518)")        

                 


def torrentz1(params):
    plugintools.log('[%s %s] [BUM+] Torrentz.eu... %s' % (addonName, addonVersion, repr(params)))

    url=params.get("url")
    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': "https://www.torrentdownloads.me/"}
    b=s.get(url, allow_redirects=False);cookie=''
    resp=b.text;heads=b.headers;cook=b.cookies;print cook
    for cookies in cook:
        cookie+=cookies.name+'='+cookies.value+'; ';s.headers.update({'Cookie':cookie});print cookie
    if cookie:
        data=resp.encode('utf-8','ignore');print data
        bloque_url=plugintools.find_single_match(data, '<span>Magnet:(.*?)</a></p></div>');url=plugintools.find_single_match(bloque_url, 'href="([^"]+)').strip()
        plugintools.log("URL Magnet= "+url)
        params["url"]=url
        launch_magnet(params)        

            
        
    

            
            
            



    
