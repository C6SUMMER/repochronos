# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV GetPoster (módulo de descarga de posters de películas)
# Version 0.1 (02.11.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)

# TODO:
# Crear botones de paginación y función de lectura de resultados por páginas: getresults(url)
# Mostrar un multilink con las páginas de resultados. El botón tendría de título: "Ir a la página..."
# Buscar alguna forma (si es posible) de mostrar los thumbnails
# Eliminar logs


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
import plugintools
import requests
import ssl

from __main__ import *
from xbmcswift2 import Plugin
from tools2 import *

plugin = Plugin()
storage = Storage(settings.storageName, type="dict")

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

tmdb = 'https://www.themoviedb.org/'
#https://api.themoviedb.org/3/movie/550?api_key=3da95cc4ead9a6608ab55a556072e3bc


temp = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))
tmdb = 'https://www.themoviedb.org/'

def tmdbsearch(title):
    plugintools.log("[%s %s] Searching URL TMDB.org for... %s" % (addonName, addonId, title))

    try:
        title=title.replace(" ", "+")
        tmdb_search = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='+title +'+themoviedb'
        data = gethttp_referer_headers(tmdb_search,referer='')

        # Solicitamos URL de TMDB.org...
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
        url_tmdb = tmdb+plugintools.find_single_match(data, 'https://www.themoviedb.org/([^"]+)')
        return url_tmdb
    except: pass


def scraperfilm(title):
    plugintools.log("[ScraperFilm PalcoTV] "+title)
	
    datamovie = {}
    datamovie = scraper_plugin(title, datamovie)
    print datamovie
    if datamovie["tmdb_id"] == "":
        datamovie = themoviedb(title, datamovie)
    else:
        datamovie = tmdb_fixed(title, datamovie)
        
    print 'datamovie',datamovie
    return datamovie


def scraper_plugin(title, datamovie):

    #Storage information
    url="";stream_info = {}
    information = plugin.get_storage('information')
    information.clear()
    information.sync()
    
    info = UnTaggle(title, url)
    information[title] = info
    datamovie = info.info
    stream_info = info.infoStream
    datamovie["typeVideo"] = info.typeVideo
    if datamovie["typeVideo"] != "MOVIE":
        xbmcplugin.setContent( int(sys.argv[1]) ,"episodes" )
        
    datamovie["VideoResolution"]=stream_info["width"]
    datamovie["VideoAspect"]=stream_info["aspect"]
    information.sync()
    print datamovie

    return datamovie


def save_title(title, datamovie, filename):
    plugintools.log("Arena+ Saving data... "+repr(datamovie))

    # Comprobamos si no existe el archivo para crearlo
    if not os.path.isfile(temp + filename):
        plugintools.log("Creando archivo... temp/"+filename)
        imdb_file = open(temp + filename, "a")
        imdb_file.seek(0)
        imdb_file.write('#EXTM3U,contents:movies\n\n')  # Fijamos modo de vista para la lista de películas
        imdb_file.close()
        print "Archivo creado correctamente!"
    else:
        pass    

    # Abrimos archivo para guardar datos de película
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    title = title.strip()
    if title.find("%nfo=") >= 0:        
        url_nfo = plugintools.find_single_match(title, '%nfo=(.*?)%')
        fixed='%nfo='+url_nfo
        title=title.replace(fixed, "").replace("%", "").strip()

    # Transformamos listas en strings para guardar en M3U
    try:
        cast_final = datamovie["cast"]
        j=len(cast_final)
        i = 0
        total_cast=""
        while i < j:
            if total_cast == "": total_cast=cast_final[i]
            else: total_cast=total_cast+", "+cast_final[i]            
            i = i + 1
    except: cast_final=""
    
    try:
        writers_final = datamovie["writer"]
        j=len(writers_final)
        i = 0
        total_writers=""
        while i < j:
            if total_writers == "": total_writers=writers_final[i]
            else: total_writers = total_writers+', '+writers_final[i]
            i = i + 1
    except: total_writers=""
    
    try:
        genre_final = datamovie["genre"]
        j=len(genre_final)
        i = 0
        total_genre=""
        while i < j:
            if total_genre == "": total_genre=genre_final[i]
            else: total_genre=total_genre+", "+genre_final[i]            
            i = i + 1
    except: total_genre=""        

    plugintools.log("Metadatos a guardar: "+repr(datamovie))
    try:
        imdb_file.write('#EXTINF:-1,'+title+',tvg-logo="'+str(datamovie["cover_url"])+'",tvg-wall="'+str(datamovie["backdrop_url"])+'",imdb="'+str(datamovie["rating"])+'",imdb_id="'+str(datamovie["imdb_id"])+'",genre="'+str(datamovie["genre"])+'",votes="'+str(datamovie["votes"])+'",duration="'+str(datamovie["duration"])+'",year="'+str(datamovie["year"])+'",director="'+str(datamovie["director"])+'",guion="'+str(datamovie["writer"])+'",sinopsis="'+str(datamovie["plot"])+'",reparto="'+total_cast+'",trailer_id="'+str(datamovie["trailer_url"])+'",photoset="'+str(datamovie["photoset"])+'"\n')
    except:
        try:
            director=datamovie["director"].encode('utf8')
            imdb_file.write('#EXTINF:-1,'+title+',tvg-logo="'+str(datamovie["cover_url"])+'",tvg-wall="'+str(datamovie["backdrop_url"])+'",imdb="'+str(datamovie["rating"])+'",imdb_id="'+str(datamovie["imdb_id"])+'",genre="'+str(datamovie["genre"])+'",votes="'+str(datamovie["votes"])+'",duration="'+str(datamovie["duration"])+'",year="'+str(datamovie["year"])+'",director="'+director+'",guion="'+str(datamovie["writer"])+'",sinopsis="'+str(datamovie["plot"])+'",reparto="'+total_cast+'",trailer_id="'+str(datamovie["trailer_url"])+'",photoset="'+str(datamovie["photoset"])+'"\n')
        except:
            try:
                sinopsis=datamovie["plot"].encode('utf8')
                imdb_file.write('#EXTINF:-1,'+title+',tvg-logo="'+str(datamovie["cover_url"])+'",tvg-wall="'+str(datamovie["backdrop_url"])+'",imdb="'+str(datamovie["rating"])+'",imdb_id="'+str(datamovie["imdb_id"])+'",genre="'+str(datamovie["genre"])+'",votes="'+str(datamovie["votes"])+'",duration="'+str(datamovie["duration"])+'",year="'+str(datamovie["year"])+'",director="'+str(datamovie["director"])+'",guion="'+str(datamovie["writer"])+'",sinopsis="'+sinopsis+'",reparto="'+total_cast+'",trailer_id="'+str(datamovie["trailer_url"])+'",photoset="'+str(datamovie["photoset"])+'"\n')
            except:
                plugintools.log("Error al guardar metadatos de "+title)
    imdb_file.close()


def save_url(url, filename):
    plugintools.log("Arena+ Saving URL...")
    
    # Abrimos archivo para guardar datos de película
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    imdb_file.write(url+'\n\n')
    imdb_file.close()


def save_multilink(url, filename):
    plugintools.log("Arena+ Saving URL...")

    # Abrimos archivo para guardar datos de pelicula
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    imdb_file.write(url+'\n')
    imdb_file.close()

def save_multiparser(url, filename):
    plugintools.log("Arena+ Saving URL...")

    # Abrimos archivo para guardar datos de pelÃ­cula
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    imdb_file.write(url+'\n')
    imdb_file.close()


def themoviedb(title, datamovie):
    plugintools.log("The Movie Database: "+title)

    if title.find("%nfo=") >= 0:  # Control para ejecutar lector de NFO files
        plugintools.log("title= "+title)
        url_nfo = plugintools.find_single_match(title, '%nfo=(.*?)%')
        fixed='%nfo='+url_nfo
        title_fixed=title.replace(fixed, "").replace("%", "").strip()
        #plugintools.log("title_fixed= "+title_fixed)
        #plugintools.log("fixed= "+fixed)
        #plugintools.log("url_nfo= "+url_nfo)
        datamovie = nfo_reader(title_fixed, url_nfo)
        return datamovie
        
    else:
        title_fixed=title.replace(" ", "+").strip()
        url = 'https://www.themoviedb.org/search?language=es&charset=utf-8&query='+title_fixed
        plugintools.log("URL búsqueda= "+url)
        referer = 'https://www.themoviedb.org/'
        headers = {"Referer": 'https://www.themoviedb.org/', 'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
        data = gethttp_referer_headers(url,referer)
        url_film = 'https://www.themoviedb.org/movie/'+plugintools.find_single_match(data, '<a id="movie_([^"]+)')+'?language=es';url_film=url_film.strip()
        plugintools.log("URL Film: "+url_film)    
        r=requests.get(url_film, verify=False);body=r.content
        #plugintools.log("body= "+body)
        logo_pattern = plugintools.find_single_match(body, '<img itemprop="image" id="upload_poster"(.*?)>')
        logo = plugintools.find_single_match(logo_pattern, 'src="([^"]+)')
        datamovie["cover_url"] = logo.strip()
        year = plugintools.find_single_match(body, '<h3 id="year">(.*?)</h3>').replace("(", "").replace(")", "").strip()
        #plugintools.log("year= "+year)
        datamovie["year"]=year
        duration_match = plugintools.find_single_match(body, '<p><strong>Runtime:</strong>(.*?)</p>')
        #plugintools.log("duration_match= "+duration_match)
        duration = plugintools.find_single_match(duration_match, '/>(.*?)</span>')        
        #plugintools.log("duration= "+duration)
        datamovie["duration"]=duration
        sinopsis = plugintools.find_single_match(body, 'itemprop="description">(.*?)</p>')
        sinopsis = sinopsis.replace('"', "")
        datamovie["plot"]=sinopsis
        #plugintools.log("sinopsis= "+sinopsis)
        crew_match = plugintools.find_single_match(body, '<h3>Crew</h3>(.*?)</table>')
        match_director = plugintools.find_single_match(crew_match, '<td class="job">Director:</td>(.*?)</td>')
        director = plugintools.find_multiple_matches(match_director, 'itemprop="name">(.*?)</span>')
        directores = ""
        for match in director:
            if directores == "":
                directores = match
            else:
                directores = directores+", "+match
        datamovie["director"] = directores
        #plugintools.log("director(es)= "+directores)
        match_writers = plugintools.find_single_match(crew_match, '<td class="job">Writers:</td>(.*?)</td>')
        writers = plugintools.find_multiple_matches(match_director, 'itemprop="name">(.*?)</span>')
        guionistas = ""
        for entry in writers:
            if guionistas == "":
                guionistas = entry
            else:
                guionistas = guionistas+", "+entry
        datamovie["writer"] = guionistas
        #plugintools.log("guionista(s)= "+guionistas)
        backdrop = plugintools.find_single_match(body, '<meta name="twitter:image" content="([^"]+)')
        datamovie["Fanart"]=backdrop
        #plugintools.log("backdrop= "+backdrop)
        match_genres = plugintools.find_single_match(body, '<span id="genres">(.*?)</ul>')
        genres_match = plugintools.find_multiple_matches(match_genres, '<span itemprop="genre">(.*?)</span>')
        generos = ""
        for genero in genres_match:
            if generos == "":
                generos = genero
            else:
                generos = generos+", "+genero
        datamovie["genre"] = generos
        rating = plugintools.find_single_match(body, '<span itemprop="ratingValue" id="rating_hint">(.*?)</span>')
        datamovie["rating"]=rating
        votes = plugintools.find_single_match(body, '<span itemprop="ratingCount">(.*?)</span>')
        datamovie["votes"]=votes

        try:
            cast_bloque = plugintools.find_single_match(body, '<h3>Cast</h3>(.*?)</table>')
            cast_item = plugintools.find_multiple_matches(cast_bloque, '<div class="castItem">(.*?)</div>')
            cast_final = []
            for item in cast_item:
                cast_item = plugintools.find_single_match(item, 'itemprop="name">([^<]+)</span>')
                if cast_final == "": cast_final=cast_item
                else: cast_final=cast_final.append(cast_item)
                
            datamovie["cast"]=cast_final
            return datamovie

        except: datamovie["cast"]=""


def nfo_reader(title, url):
    data=gethttp_referer_headers(url,referer="")
    datamovie={}
    title=plugintools.find_single_match(data, '<title>([^<]+)')
    datamovie["title"] = title
    imdb_rating=plugintools.find_single_match(data, '<rating>([^<]+)')
    datamovie["rating"] = imdb_rating
    top = plugintools.find_single_match(data, '<top250>([^<]+)')
    datamovie["top250"]=top
    year=plugintools.find_single_match(data, '<year>([^<]+)')
    datamovie["year"] = year
    votes=plugintools.find_single_match(data, '<votes>([^<]+)')
    datamovie["votes"] = votes
    sinopsis=plugintools.find_single_match(data, '<plot>([^<]+)')
    datamovie["plot"] = sinopsis
    tagline=plugintools.find_single_match(data, '<tagline>([^<]+)')
    datamovie["tagline"] = tagline
    duration=plugintools.find_single_match(data, '<runtime>([^<]+)')
    datamovie["duration"] = duration
    fanart_matches=plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')
    fanart=plugintools.find_single_match(fanart_matches, '<thumb[^>]+([^<]+)').replace(">", "").strip()
    datamovie["fanart"] = fanart
    thumbnail=plugintools.find_single_match(data, '<thumb[^>]+([^<]+)').replace(">", "").strip()
    datamovie["poster"] = thumbnail
    genres=plugintools.find_multiple_matches(data, '<genre>([^<]+)')
    genre_final = []
    for genre in genres:
        genre_final.append(genre)
    datamovie["genre"] = genre_final
    director=plugintools.find_single_match(data, '<director>([^<]+)')
    datamovie["director"] = director
    trailer=plugintools.find_single_match(data, '<trailer>([^<]+)')
    datamovie["trailer"] = trailer
    duration=plugintools.find_single_match(data, '<runtime>([^<]+)')
    datamovie["duration"] = duration
    cast_item=plugintools.find_multiple_matches(data, '<actor>(.*?)</actor>')
    cast_final = []
    for item in cast_item:
        #plugintools.log("item= "+item)
        actor=plugintools.find_single_match(item, '<name>(.*?)</name>')
        cast_final.append(actor)
    datamovie["cast"]=cast_final
    studio=plugintools.find_single_match(data, '<studio><thumb preview="([^<]+)')
    datamovie["studio"]=studio
    writers=plugintools.find_multiple_matches(data, '<credits>(.*?)</credits>')
    writers_final=[]
    for item in writers:
        writers_final.append(item)
    datamovie["writer"]=writers_final
    return datamovie


def tmdb_fixed(title, datamovie):   
    headers = {"Referer": 'https://www.themoviedb.org/', 'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    url_film = tmdb+'movie/'+str(datamovie["tmdb_id"])+'?language=es'
    r=requests.get(url_film, verify=False);body=r.content
    plugintools.log("URL Film: "+url_film)

    # Ya guardado: Rating, Year, Duration, Plot (english), VideoAspect, tmdb_id, cover_url (Poster), imdb_id, Director, Género (english), VideoResolution, Overlay
    # Fecha de estreno (premiered), Cast, MPAA, playcount, trailer_url (ID Youtube), trailer (Youtube URL), trailer_url (Youtube)

    datamovie["plot"] = plugintools.find_single_match(body, 'itemprop="description">(.*?)</p>').replace('"', "")
    crew_match = plugintools.find_single_match(body, '<h3>Crew</h3>(.*?)</table>')
    match_writers = plugintools.find_single_match(crew_match, '<td class="job">Writers:</td>(.*?)</td>')
    match_director = plugintools.find_single_match(crew_match, '<td class="job">Director:</td>(.*?)</td>')
    writers = plugintools.find_multiple_matches(match_director, 'itemprop="name">(.*?)</span>')
    guionistas = ""
    for entry in writers:
        if guionistas == "":
            guionistas = entry
        else:
            guionistas = guionistas+", "+entry
    datamovie["writer"] = guionistas
    match_genres = plugintools.find_single_match(body, '<span id="genres">(.*?)</ul>')
    genres_match = plugintools.find_multiple_matches(match_genres, '<span itemprop="genre">(.*?)</span>')
    generos = ""
    for genero in genres_match:
        if generos == "":
            generos = genero
        else:
            generos = generos+", "+genero

    datamovie["genre"] = generos
    cast_bloque = plugintools.find_single_match(body, '<h3>Cast</h3>(.*?)</table>')
    cast_item = plugintools.find_multiple_matches(cast_bloque, '<div class="castItem">(.*?)</div>')
    cast_final = ""
    for item in cast_item:
        cast_item = plugintools.find_single_match(item, 'itemprop="name">([^<]+)</span>')
        if cast_final == "": cast_final=cast_item
        else: cast_final=cast_final+', '+cast_item
        
    datamovie["cast"]=cast_final.split(", ")
    try:
        backdrops=plugintools.find_single_match(body, '<div id="backdrops" class="image_carousel">(.*?)</div>')
        backs=plugintools.find_multiple_matches(backdrops, 'src="([^"]+)')
        if len(backs)>=3:
            datamovie["photoset"]=backs[0]+"$"+backs[1]+"$"+backs[2]+"$"+backs[3]
        elif len(backs)==2:
            datamovie["photoset"]=backs[0]+"$"+backs[1]+"$"+backs[2]
        else:
            datamovie["photoset"]=backs[0]+"$"+backs[1]
    except: pass

    bl_studio=plugintools.find_single_match(body, '<h3>Production Companies</h3>(.*?)</span></a></p>')
    datamovie["studio"]=plugintools.find_single_match(body, 'itemprop="name">([^<]+)')    
    
    return datamovie    

def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    
    return body
