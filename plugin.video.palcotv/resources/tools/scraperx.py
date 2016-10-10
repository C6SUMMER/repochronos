# -*- coding: utf-8 -*-
#------------------------------------------------------------
# ScraperX para PalcoTV
# Version 0.5 (29.06.2016)
# Creado por Juarrox & Aquilesserr
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import urlparse,urllib2,urllib,re,shutil
import os, sys

import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import plugintools, requests, json, time, zipfile, shutil

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

art = addonPath + "/art/"
playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

thumbnail = 'https://www.cubbyusercontent.com/pl/ScraperX_Logo.png/_1a56f5b06ec84d009cbc4003b4bb5c57'
thumbnail_nofound = 'https://www.cubbyusercontent.com/pl/PosterNoDispScraperLogo.png/_90a8df5244e149939c6f6aa8a9b1a4f0'
fanart = 'https://www.cubbyusercontent.com/pl/scraperx.png/_565e39ceea7844cca9a0853f099857b3'

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR lightgreen]";ec5 = "[/COLOR]"
version = " 0.5"

API_KEY_PEL = plugintools.get_setting("tmdb_key")  # TMDB.org API Key (solicitar al usuario en config)
API_KEY_SER = plugintools.get_setting("tvdb_apikey")  # TheTVDB.org API Key (solicitar al usuario en config)

def scraperx0(params):
    plugintools.log("[%s %s]Scraper PalcoTV %s " % (addonName, addonVersion, repr(params)))
    
    name = 'Scraseries'
    update = '29/06/2016 11:00'
    Autor = 'Juarrox'
    filename = 'MIS_SERIES.m3u'

    if plugintools.get_setting("tmdb_key") == "":
        plugintools.add_item(action="", title=sc4+"[B]Introduce tu API_KEY themoviedb.org en la configuración.[/B]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    if plugintools.get_setting("tvdb_apikey") == "":
        plugintools.add_item(action="", title=sc4+"[B]Introduce tu API_KEY thetvdb.com en la configuración.[/B]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    datamovie={}
    datamovie['Plot']='[COLOR lightyellow][Juarrox&Aquilesserr / PalcoTV Team][/COLOR][CR][CR]Este scraper creado por Aquilesserr y Juarrox para PalcoTV permite realizar búsquedas de pelis y series en TMDB/TVDB y guarda los metadatos seleccionados por el usuario en la ruta [COLOR lightyellow][I]kodi / userdata / tmp / [/I][/COLOR] como enlaces #multi.'

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]ScraperX [/B][/COLOR][COLOR lightyellow][I]("+version+")[/I][/COLOR]",info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    plugintools.add_item(action="scraperx_bus",url="",title="[COLOR lightgreen]Buscar película...[/COLOR]",thumbnail=thumbnail,fanart=fanart,page="peli",folder=True,isPlayable=False)
    plugintools.add_item(action="scraperx_bus",url="",title="[COLOR lightgreen]Buscar serie...[/COLOR]",thumbnail=thumbnail,fanart=fanart,page="serie",folder=True,isPlayable=False)
    plugintools.addScraper1(action="",url="",title="",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    # Abrir archivos M3U con pelis y series escrapeadas con m3u_reader
    datamovie={};datamovie["plot"]='Lista de películas scrapeadas se aloja en la carpeta [COLOR lightblue][B][I]KODI[/B][/COLOR]/userdata/temp/[COLOR lightyellow][B]MIS_PELIS.m3u[/B][/COLOR][/I]. Si pulsas con el botón derecho sobre cada película puedes [B]recargar, exportar y eliminar entradas[/B].'
    plugintools.add_item(action="scraperx_m3u",url="",title="[COLOR gold][I]MIS_PELIS.m3u[/I][/COLOR]",info_labels=datamovie,page="peli",thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
    datamovie={};datamovie["plot"]='Lista de películas scrapeadas se aloja en la carpeta [COLOR lightblue][B][I]KODI[/B][/COLOR]/userdata/temp/[COLOR lightyellow][B]MIS_SERIES.m3u[/B][/COLOR][/I]. Si pulsas con el botón derecho sobre cada serie puedes [B]recargar, exportar y eliminar entradas[/B].'
    plugintools.add_item(action="scraperx_m3u",url="",title="[COLOR gold][I]MIS_SERIES.m3u[/I][/COLOR]",info_labels=datamovie,page="serie",thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)

def scraperx_m3u(params):   
    tipo=params.get("page")
    plugintools.log("tipo= "+tipo)
    if tipo == "peli":
        try:
            plugintools.log("Leyendo MIS_PELIS.m3u... ")
            list_file = open(temp + 'MIS_PELIS.m3u', "r")
            #list_file.seek(0)
            archivo = list_file.read()  # Leyendo el archivo m3u
            bloq_full = plugintools.find_multiple_matches(archivo,'#EXTINF:-1,(.*?)#multi')
            if bloq_full !="":
                for title in bloq_full:
                    titlefilm = plugintools.find_single_match(title,'(.*?),')
                    logo = plugintools.find_single_match(title,'tvg-logo="([^"]+)"')
                    fondo = plugintools.find_single_match(title,'tvg-wall="([^"]+)"')
                    rating = plugintools.find_single_match(title,'imdb="([^"]+)"')
                    year = plugintools.find_single_match(title,'year="([^"]+)"')
                    plot = plugintools.find_single_match(title,'sinopsis="([^"]+)"')
                    votes = plugintools.find_single_match(title,'votes="([^"]+)"')
                    duration = plugintools.find_single_match(title,'duration="([^"]+)"')
                    genre = plugintools.find_single_match(title,'genre="([^"]+)"')
                    director = plugintools.find_single_match(title,'director="([^"]+)"')
                    guion = plugintools.find_single_match(title,'guion="([^"]+)"');plugintools.log("guion= "+guion)
                    reparto = plugintools.find_single_match(title,'reparto="([^"]+)"');plugintools.log("reparto= "+reparto)
                    titlefull = sc+titlefilm+' ('+year+')'+ec
                    datamovie={};datamovie['year']=year;datamovie['rating']=rating;datamovie['plot']=plot;datamovie["duration"]=duration;datamovie["votes"]=votes;datamovie['genre']=genre;datamovie['director']=director;datamovie['cast']=reparto.split(", ");datamovie['writer']=guion
                    datamovie["plot"]='[B]'+datamovie["year"]+'[/B][COLOR lightgreen][I] '+str(int(datamovie["duration"])/60)+' min  [/I][/COLOR][COLOR white][B]IMDB: [COLOR lightblue]'+datamovie["rating"]+'[/B][/COLOR][B][COLOR white] Dir:[/B][/COLOR] '+datamovie["director"]+'[CR]'+datamovie["plot"]
                    plugintools.addScraper1(action="",url="",title='  '+titlefull,page="peli",thumbnail=logo,fanart=fondo,info_labels=datamovie,folder=False,isPlayable=False)
                    list_file.close()
            else: plugintools.addScraper1(action="",url="",title='Lista vacía',page="peli",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        except: plugintools.addScraper1(action="",url="",title='Lista vacía',page="peli",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

        xbmcplugin.setContent( int(sys.argv[1]) ,"movies" )
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
    elif tipo == "serie":
        try:
            plugintools.log("Leyendo MIS_SERIES.m3u... ")
            list_file = open(temp + 'MIS_SERIES.m3u', "r")
            archivo = list_file.read()  # Leyendo el archivo m3u
            bloq_full = plugintools.find_multiple_matches(archivo,'#EXTINF:-1,(.*?)#multi')
            if bloq_full !="":
                for title in bloq_full:
                    titleshow = plugintools.find_single_match(title,'(.*?),')
                    logo = plugintools.find_single_match(title,'tvg-logo="([^"]+)"')
                    banner = plugintools.find_single_match(title,'banner="([^"]+)"')
                    fondo = plugintools.find_single_match(title,'tvg-wall="([^"]+)"')
                    rating = plugintools.find_single_match(title,'tvdb_id="([^"]+)"')
                    votes = plugintools.find_single_match(title,'votes="([^"]+)"')
                    imdb = plugintools.find_single_match(title,'imdb_id="([^"]+)"')
                    tvdb = plugintools.find_single_match(title,'tvdb_id="([^"]+)"')
                    plot = plugintools.find_single_match(title,'sinopsis="([^"]+)"')
                    duration = plugintools.find_single_match(title,'duration="([^"]+)"')
                    network = plugintools.find_single_match(title,'network="([^"]+)"')
                    premiere = plugintools.find_single_match(title,'premiere="([^"]+)"')
                    genre = plugintools.find_single_match(title,'genre="([^"]+)"')
                    episodes = plugintools.find_single_match(title,'episodes="([^"]+)"')
                    titlefull = sc+titleshow+' [COLOR lightgreen][I]['+network+'][/I]'+ec+ec
                    datamovie={};datamovie["TVShowTitle"]=titleshow;datamovie['rating']=rating;datamovie['plot']=plot;datamovie["duration"]=duration;datamovie["premiered"]=premiere;datamovie["totalseasons"]="15x12";datamovie["votes"]=votes;datamovie['genre']=genre
                    seasons=episodes.split("x")[1];episodes=episodes.split("x")[0];totalepis=int(episodes)*int(seasons);vistos="33";datamovie['episode']=totalepis;datamovie['WatchedEpisodes']="33";novistos=int(totalepis)-int(vistos);datamovie['WatchedEpisodes']=33;datamovie["plot"]=plot
                    plugintools.log("episodes= "+episodes)
                    #'[B]'+datamovie["year"]+'[/B][COLOR lightgreen][I] '+str(int(datamovie["duration"])/60)+' min  [/I][/COLOR][COLOR white][B]IMDB: [COLOR lightblue]'+datamovie["rating"]+'[/B][/COLOR][B][COLOR white] Dir:[/B][/COLOR] '+datamovie["director"]+'[CR]'+datamovie["plot"]
                    plugintools.addScraper1(action="",url="",title='  '+titlefull,page="serie",thumbnail=banner,fanart=fondo,info_labels=datamovie,vistos="33",novistos=str(novistos),folder=False,isPlayable=False)
                    list_file.close()
            else: plugintools.addScraper1(action="",url="",title='Lista vacía',page="serie",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        except: plugintools.addScraper1(action="",url="",title='Lista vacía',page="serie",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

        xbmcplugin.setContent( int(sys.argv[1]) ,"tvshows" )
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
 
def scraperx_bus(params):
    plugintools.log('ScraperX: Búsqueda de títulos...')

    page = params.get("page")
    if page == "serie":
        ##### Control de la API_KEY ####
        if API_KEY_SER == "":
            errormsg = plugintools.message("PalcoTV Buscar Serie...","Es necesario una API_KEY de www.thetvdb.com para realizar busquedas[CR]Consulta en http://arena.pe.hu/forums/index.php")
            scraperx0(params)
        else:
            xbmcplugin.setContent( int(sys.argv[1]) ,"tvshows" )
            texto="";texto = plugintools.keyboard_input(texto)
            texto = texto.lower()  # Pasamos el texto a minúsculas para evitar problemas en la busqueda
            texto = texto.replace(',','').replace(':','').replace('/','').replace('.','').replace('-','').replace('_','').replace(';','')
            if texto == "": pass
            else:
                texto = texto.lower().strip()
                texto = texto.replace(" ", "+")
                burl = 'https://www.thetvdb.com'
                murl=burl+'/api/'+API_KEY_SER+'/mirrors.xml'
                r=requests.get(murl);data=r.content;
                plugintools.log("murl= "+murl)
                plugintools.log("data= "+data)
                burl=plugintools.find_single_match(data, '<mirrorpath>([^<]+)')#;print 'burl',burl
                url_bus=burl+'/api/GetSeries.php?seriesname='+texto+'&language=es'
                params = plugintools.get_params()
                params["url"] = url_bus;params["page"]="serie"     
                scraperx_result(params)

            xbmcplugin.endOfDirectory(int(sys.argv[1]))

    elif page == "peli":
        ##### Control de la API_KEY ####
        if API_KEY_PEL == "":
            errormsg = plugintools.message("PalcoTV Buscar Película...","Es necesario una API_KEY de www.themoviedb.org para realizar busquedas[CR]Consulta en http://arena.pe.hu/forums/index.php")
            scraperx0(params)
        else:
            xbmcplugin.setContent( int(sys.argv[1]) ,"movies" )
        
            texto="";texto = plugintools.keyboard_input(texto)
            texto = texto.lower()  # Pasamos el texto a minúsculas para evitar problemas en la busqueda
            texto = texto.replace(',','').replace(':','').replace('/','').replace('.','').replace('-','').replace('_','').replace(';','')
            if texto == "": pass
            else:
                texto = texto.lower().strip()
                texto = texto.replace(" ", "+")
                url_bus = 'http://api.themoviedb.org/3/search/movie?api_key='+API_KEY_PEL+'&query='+texto+'&language=es&page=1'    
                params = plugintools.get_params() 
                params["url"] = url_bus;params["page"]="peli"
                scraperx_result(params)

            xbmcplugin.endOfDirectory(int(sys.argv[1]))        
        
def scraperx_result(params):
    url = params.get("url");page=params.get("page")
    r = requests.get(url)
    data = r.content
    
    if page == "serie":    
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]ScraperX PalcoTV"+version+"[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

        plugintools.add_item(action="scraperx_bus",url="",title=sc5+"Buscar serie..."+ec5,page="serie",thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
        result = plugintools.find_multiple_matches(data,'<Series>(.*?)</Series>')
        for item in result:
            tvdb_id=plugintools.find_single_match(item, '<seriesid>([^<]+)')
            title=plugintools.find_single_match(item, '<SeriesName>([^<]+)').replace("amp;", "").strip()
            network=plugintools.find_single_match(item, '<Network>([^<]+)')
            plot=plugintools.find_single_match(item, '<Overview>([^<]+)')
            premiere=plugintools.find_single_match(item, '<FirstAired>([^<]+)')        
            banner='http://thetvdb.com/banners/'+plugintools.find_single_match(item, '<banner>([^<]+)')
            datamovie={};datamovie["plot"]=plot;datamovie["poster"]=banner;datamovie["totalepisodes"]="N/D";datamovie["premiered"]=premiere      
            url = 'http://www.thetvdb.com/api/'+API_KEY_SER+'/series/'+tvdb_id+'/all/es.zip'
            if network == "": network = "N/D"
            titlefull = sc+title+' ('+network+')'+'  '+ec+sc3+'['+tvdb_id+']'+ec3
            plugintools.add_item(action="scraperx_createlist",url=url,title=titlefull,thumbnail=banner,fanart=fanart,info_labels=datamovie,page="serie",extra=tvdb_id, folder=False,isPlayable=False)

    if page == "peli":
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]ScraperX PalcoTV"+version+"[/B][/COLOR]",page="peli",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

        plugintools.add_item(action="scraperx_bus",url="",title=sc5+"Buscar película..."+ec5,page="peli",thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
        try:
            js = json.loads(data)
            results = js['results']
            for item in results:
                id_peli = item['id']

                #'https://api.themoviedb.org/3/movie/'+str(id_peli)+'?api_key='+str(API_KEY_PEL)+'&language=es&append_to_response=images,trailers,external_ids,credits&include_image_language=es,null'
                url = 'https://api.themoviedb.org/3/movie/'+str(id_peli)+'?api_key='+str(API_KEY_PEL)+'&language=es&append_to_response=images,videos,external_ids,credits&include_image_language=es,null'
                title = item['title'].encode('utf-8','ignore')
                title = title.replace('&#x2F;','/').replace('&#x27;',"'").replace('&Amp;','&').replace('&amp;','&')
                date = item['release_date']
                year = date.split('-');year = year[0]
                img = 'https://image.tmdb.org/t/p/w370/'+item['poster_path']
                if img =="": img = thumbnail_nofound
                rating = item['vote_average']
                if not '.' in str(rating): rating = str(rating)+'.0'
                if rating =="": rating = 'N/D'
                titlefull = sc+title+' ('+str(year)+')'+'  '+ec+sc3+'['+str(rating)+']'+ec3
                plugintools.add_item(action="scraperx_createlist",url=url,title=titlefull,thumbnail=img,fanart=fanart,page="peli",folder=False,isPlayable=False)
        except: pass        
               
def scraperx_createlist(params):
    plugintools.log('[%s %s] Creando Lista... %s' % (addonName, addonVersion, repr(params)))

    page=params.get("page")

    if page == "serie": scraper_series(params)
    elif page == "peli": scraper_pelis(params)

def scraper_series(params):
    filename = 'MIS_SERIES.m3u'

    # Comprobamos si no existe el archivo para crearlo
    if not os.path.isfile(temp + filename):
        plugintools.log("PalcoTV Creando Archivo... "+ filename)
        tvdb_file = open(temp + filename, "a")
        tvdb_file.seek(0)
        tvdb_file.write('#EXTM3U,contents:tvshows\n\n')  # Fijando el modo vista 
        tvdb_file.close()
        print "Archivo creado correctamente!"
    else: pass

    # Iniciamos scraper de TheTVDB.org ...
    tvdb_id=params.get("extra")
    remote_file = 'http://www.thetvdb.com/api/'+str(API_KEY_SER)+'/series/'+str(tvdb_id)+'/all/es.zip'
    plugintools.log("remote_file= "+remote_file)
    folder_id = temp + tvdb_id    
    if os.path.exists(folder_id) is False:
        os.mkdir(folder_id)

    if os.path.exists(folder_id):
        fname = 'es.zip';local_path = folder_id+fname
        plugintools.log("Iniciamos descarga de metadatos: "+local_path)
        dp = xbmcgui.DialogProgress();
        msgdp='Espere, por favor...'
        dp.create(fname, msgdp)
        start_time = time.time()
        try: urllib.urlretrieve(remote_file, local_path, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
        except:
            while os.path.exists(local_path):
                try: os.remove(local_path); break
                except: pass
            if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): return False
            else: raise
            return False
        #except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (addonName, "Error en la descarga!", 3 , art+'icon.png')); return False;return False

        if os.path.isfile(local_path) is True:
            unzipper = ziptools()
            unzipper.extract(local_path, folder_id, params)
            #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (addonName, "Info actualizada!", 3 , art+'icon.png'))
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (addonName, "Error! No se encuentra archivo descargado", 3 , art+'icon.png'))

    if os.path.exists(local_path):
        try: os.remove(local_path)
        except: pass            

    # Iniciamos lectura de metadatos ...

    infofile=open(temp+tvdb_id+'/es.xml', "r")
    data = infofile.read()
    #plugintools.log("data= "+data)
    seriebloque=plugintools.find_single_match(data, '<Series>(.*?)</Series>')

    genre=plugintools.find_single_match(seriebloque, '<Genre>\|(.*?)\|</Genre>').replace("|", ", ").strip()
    cast=plugintools.find_single_match(seriebloque, '<Actors>([^<]+)')[1:].replace("|", ", ").strip()
    thumb='http://thetvdb.com/banners/'+plugintools.find_single_match(seriebloque, '<poster>([^<]+)')
    banner='http://thetvdb.com/banners/'+plugintools.find_single_match(seriebloque, '<banner>([^<]+)')
    rating=plugintools.find_single_match(seriebloque, '<Rating>([^<]+)')
    votes=plugintools.find_single_match(seriebloque, '<RatingCount>([^<]+)')
    duration=plugintools.find_single_match(seriebloque, '<Runtime>([^<]+)')
    premiere=plugintools.find_single_match(seriebloque, '<FirstAired>([^<]+)')
    title=plugintools.find_single_match(seriebloque, '<SeriesName>([^<]+)')
    imdb_id=plugintools.find_single_match(seriebloque, '<IMDB_ID>([^<]+)')    
    fanart='http://thetvdb.com/banners/'+plugintools.find_single_match(seriebloque, '<fanart>([^<]+)')
    plot=plugintools.find_single_match(seriebloque, '<Overview>([^<]+)').strip()
    network=plugintools.find_single_match(seriebloque, '<Network>([^<]+)')
    
    plugintools.log("genre= "+genre)
    plugintools.log("cast= "+cast)
    plugintools.log("thumb= "+thumb)
    plugintools.log("fanart= "+fanart)
    plugintools.log("banner= "+banner)
    plugintools.log("title= "+title)
    plugintools.log("imdb_id= "+imdb_id)
    plugintools.log("plot= "+plot)

    # Cálculo de capítulos y temporadas
    episodes = plugintools.find_multiple_matches(data, '<Episode>(.*?)</Episode>')
    tepis_bloque = episodes[-1]
    #plugintools.log("tepis_bloque= "+tepis_bloque)
    tepis= plugintools.find_single_match(tepis_bloque, '<EpisodeNumber>([^<]+)')
    ttemps= plugintools.find_single_match(tepis_bloque, '<SeasonNumber>([^<]+)')
    ttcc=tepis+"x"+ttemps
    plugintools.log("Total: "+ttcc)

    # Comprobamos si no existe el archivo para crearlo
    fm3u='/Series.m3u'
    if not os.path.isfile(temp + fm3u):
        plugintools.log("PalcoTV Creando Archivo... "+ fm3u)
        tvdb_file = open(temp + fm3u, "a")
        tvdb_file.seek(0)
        tvdb_file.write('#EXTM3U,contents:movies\n\n')
        tvdb_file.close()        
    else: tvdb_file = open(temp + fm3u, "a")

    tvdb = {'EXTINF':'#EXTINF:-1,',
    'title':title,
    'tvg_logo': ',tvg-logo="'+str(thumb)+'"',
    'tvg_wall': ',tvg-wall="'+str(fanart)+'"',
    'tvdb': ',tvdb_id="'+str(tvdb_id)+'"',
    'imdb': ',imdb_id="'+str(imdb_id)+'"',
    'rating': ',rating="'+str(rating)+'"',
    'votes': ',votes="'+str(votes)+'"',
    'premiere': ',premiere="'+str(premiere)+'"',            
    'genre': ',genre="'+str(genre)+'"',
    'network': ',network="'+str(network)+'"',                        
    'duration': ',duration="'+str(duration)+'"',
    'sinopsis': ',sinopsis="'+str(plot)+'"',
    'reparto': ',reparto="'+str(cast)+'"',
    'banner': ',banner="'+str(banner)+'"',
    'episodes': ',episodes="'+str(ttcc)+'"'}

    tvdb = tvdb['EXTINF']+tvdb['title']+tvdb['tvg_logo']+tvdb['tvg_wall']+tvdb['banner']+tvdb['tvdb']+tvdb['imdb']+tvdb['rating']+tvdb['votes']+tvdb['duration']+tvdb['premiere']+tvdb['reparto']+tvdb['episodes']+tvdb['genre']+tvdb['network']+tvdb['sinopsis']
   
    # Abrimos archivo para guardar datos de la serie
    try:
        plugintools.log("Abriendo archivo... temp/"+filename)
        tvdb_file = open(temp + filename, "a")
        tvdb_file.write(tvdb+'\n')
        tvdb_file.write('#multi\n'+str(title)+'$serie:\n'+str(title)+'$serie:\n'+str(title)+'$serie:\n'+str(title)+'$serie:\n#multi\n\n')
        tvdb_file.close()
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Serie añadida!", 3 , art+'icon.png'))
    except:
        pass
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Error! Serie no guardada", 3 , art+'icon.png'))

def scraper_pelis(params):
    filename = 'MIS_PELIS.m3u'

    # Comprobamos si no existe el archivo para crearlo
    if not os.path.isfile(temp + filename):
        plugintools.log("PalcoTV Creando Archivo... "+ filename)
        imdb_file = open(temp + filename, "a")
        imdb_file.seek(0)
        imdb_file.write('#EXTM3U,contents:movies\n\n')  # Fijando el modo vista 
        imdb_file.close()
        print "Archivo creado correctamente!"
    else: pass

    url = params.get("url")
    r = requests.get(url)
    data = r.content
    js = json.loads(data)
    
    title = js['title'].encode('utf-8','ignore')
    title = title.replace(',','').replace(':','').replace('&Amp;','&').replace('&amp;','&').replace('&#x2F;','/').replace('&#x27;',"'").replace('"',"'")

    try:
        tvg_logo = 'https://image.tmdb.org/t/p/w370'+js['poster_path']
    except: tvg_logo = thumbnail
    try:
        tvg_fanart = 'https://image.tmdb.org/t/p/original'+js['backdrop_path']
    except: tvg_fanart = fanart

    rating = js['vote_average']
    if not '.' in str(rating): rating = str(rating)+'.0'
    imdb_id = js['imdb_id']
    votes = js['vote_count']
    duration = int(js['runtime'])*60

    date = js['release_date']
    year = date.split('-');year = year[0]
    
    bloq_genre = js['genres']
    bloque = []
    for item in bloq_genre: genr = item['name'].encode('utf-8','ignore');bloque.append(genr)
    genre = imdb_recompile(bloque)
    
    bloq_director = js['credits']['crew']
    bloque = []
    for item in bloq_director:
        if item['job'] == 'Director': director = item['name'].encode('utf-8','ignore');bloque.append(director)
    director = imdb_recompile(bloque)

    bloq_guion = js['credits']['crew']
    bloque = []
    for item in bloq_guion:
        if item['department'] == 'Writing': guion = item['name'].encode('utf-8','ignore');bloque.append(guion)    
    guion = imdb_recompile(bloque)

    sinopsis = js['overview'].encode('utf-8','ignore').replace('"',"'")

    bloq_reparto = js['credits']['cast']
    bloque = []
    for item in bloq_reparto:
        reparto = item['name'].encode('utf-8','ignore');bloque.append(reparto)    
    reparto = imdb_recompile(bloque)

    id_peli = js['id']
    url = 'http://api.themoviedb.org/3/movie/'+str(id_peli)+'/videos?api_key='+str(API_KEY_PEL)+'&language=es&append_to_response=trailers&include_video_language=es'
    trailer_id = imdb_bus_trailer(url) #buscando trailer en ingles si lo hay
    
    imdb = {'EXTINF':'#EXTINF:-1,',
    'title':title,
    'tvg_logo': ',tvg-logo="'+str(tvg_logo)+'"',
    'tvg_wall': ',tvg-wall="'+str(tvg_fanart)+'"',
    'imdb': ',imdb="'+str(rating)+'"',
    'imdb_id': ',imdb_id="'+str(imdb_id)+'"',            
    'votes': ',votes="'+str(votes)+'"',
    'duration': ',duration="'+str(duration)+'"',
    'year': ',year="'+str(year)+'"',
    'genre': ',genre="'+str(genre)+'"',
    'director': ',director="'+str(director)+'"',
    'guion': ',guion="'+str(guion)+'"',
    'sinopsis': ',sinopsis="'+str(sinopsis)+'"',
    'reparto': ',reparto="'+str(reparto)+'"',
    'trailer_id': ',trailer_id="'+str(trailer_id)+'"'}

    imdb = imdb['EXTINF']+imdb['title']+imdb['tvg_logo']+imdb['tvg_wall']+imdb['imdb']+imdb['imdb_id']+imdb['votes']+imdb['duration']+imdb['year']+imdb['genre']+imdb['director']+imdb['guion']+imdb['sinopsis']+imdb['reparto']+imdb['trailer_id']
    
    imdb_multi = {'multi': '#multi\n',
    'title_HDfull' : str(title)+'$peli:\n',
    'title_Oranline' : str(title)+'$peli:\n',
    'title_Pordede' : str(title)+'$peli:\n',
    'title_Pelisadicto' : str(title)+'$peli:\n',
    'title_TVvip' : str(title)+'$peli:\n'}

    imdb_multi = imdb_multi['multi']+imdb_multi['title_TVvip']+imdb_multi['title_HDfull']+imdb_multi['title_Oranline']+imdb_multi['title_Pelisadicto']+imdb_multi['title_Pordede']+imdb_multi['multi']
    
    # Abrimos archivo para guardar datos de la pelicula
    try:
        plugintools.log("Abriendo archivo... temp/"+filename)
        edit_file = open(temp + filename, "a")
        edit_file.write(imdb+'\n')
        edit_file.write(imdb_multi+'\n')
        edit_file.close()
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Película añadida!", 3 , art+'icon.png'))
    except:
        pass
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Error! Película no guardada", 3 , art+'icon.png'))
        
    
################################################### Herramientas ################################################# 

################ Recompila Bloques #######################

def imdb_recompile(bloque):

    # Recompilamos cuatro items
    try:
        if len(bloque) >= 5: bloque = bloque[0]+', '+bloque[1]+', '+bloque[2]+', '+bloque[3]
        elif len(bloque) == 4: bloque = bloque[0]+', '+bloque[1]+', '+bloque[2]+', '+bloque[3]
        elif len(bloque) == 3: bloque = bloque[0]+', '+bloque[1]+', '+bloque[2]
        elif len(bloque) == 2: bloque = bloque[0]+', '+bloque[1]
        elif len(bloque) == 1: bloque = bloque[0]
    except: bloque = ""
    return bloque

################# Busca Trailers ########################

def imdb_bus_trailer(url):

    headers = {'Accept': 'application/json'}
    try:
        #Buscando trailers en Esp.
        r = requests.get(url,headers=headers)
        data = r.text.encode('utf-8','ignore')
        js = json.loads(data)
        trailer_id = js['results'][0]['key']
    except:
        #Buscando trailers en Ing.
        url = url.replace('language=es','language=en')
        r = requests.get(url,headers=headers)
        data = r.text.encode('utf-8','ignore')
        js = json.loads(data)
        trailer_id = js['results'][0]['key']
    return trailer_id
    
############# Elimina Lista Completa ###################

def scraperx_delfile(params):
    plugintools.log("[%s %s] Eliminando lista ... %s " % (addonName, addonVersion, params))    
    
    page = params.get("page")
    if page == "peli":
        runDelete = xbmcgui.Dialog().yesno(addonName, '¿Desea eliminar kodi/userdata/tmp/[B]MIS_PELIS.m3u[/B]?')
        filename = 'MIS_PELIS.m3u'
    elif page == "serie":
        runDelete = xbmcgui.Dialog().yesno(addonName, '¿Desea eliminar kodi/userdata/tmp/[B]MIS_SERIES.m3u[/B]?')
        filename = 'MIS_SERIES.m3u'        

    if(runDelete):
        os.remove(temp+filename)
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Lista eliminada", 3 , art+'icon.png'))
        scraperx_reload(params)

################# Recarga Lista  ######################

def scraperx_reload(params):
    plugintools.log("[%s %s] Recargando... %s " % (addonName, addonVersion, params))

    xbmc.executebuiltin("Container.Refresh")
    page=params.get("page")
    if page == "serie": filename='MIS_SERIES.m3u'
    elif page == "peli": filename='MIS_PELIS.m3u'
    try: ist_file = open(temp + filename, "r");data = list_file.read()
    except: pass

############# Elimina Entrada en Lista  ###############   
    
def scraperx_supr(params):
    page=params.get("page")
    if page == "serie":
        filename='MIS_SERIES.m3u'
        title="#EXTINF:-1,"+params.get("title").replace("[COLOR white]", "").replace("[/COLOR]", "").split("[")[0].strip()
        plugintools.log("Titulo = "+title)
        list_file = open(temp + filename, "r")
        list_file.seek(0)
        lineas = list_file.readlines()
        list_file.close()
        list_file = open(temp + filename, "w")
        for linea in lineas:
            print linea
            if linea.startswith(title+",") == True:
                plugintools.log("Titulo = "+title)
                plugintools.log("Eliminado linea... = "+linea)
            else:
                list_file.write(linea)        
        #except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Error al borrar!", 3 , art+'icon.png'));pass
        scraperx_reload(params)

    if page == "peli":
        filename='MIS_PELIS.m3u'
        title="#EXTINF:-1,"+params.get("title").replace("[COLOR white]", "").replace("[/COLOR]", "").strip()
        title=title.split("(")[0].strip()
        list_file = open(temp + filename, "r")
        list_file.seek(0)
        lineas = list_file.readlines()
        list_file.close()
        list_file = open(temp + filename, "w")
        for linea in lineas:
            print linea
            if linea.startswith(title) == True:
                plugintools.log("Eliminado linea... = "+linea)
            else:
                list_file.write(linea)        
        #except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Error al borrar!", 3 , art+'icon.png'));pass
        scraperx_reload(params)        

################## Exporta Lista  #####################

def scraperx_export(params):  # filename = Archivo origen, fname = Archivo destino/exportado
    page=params.get("page")
    if page == "serie": filename = 'MIS_SERIES.m3u'
    elif page == "peli": filename = 'MIS_PELIS.m3u'

    fname = "";fname = plugintools.keyboard_input(fname)
    if fname == "": errormsg = plugintools.message("PalcoTV","Por favor, introduzca un nombre de archivo válido");return errormsg
    else:
        fname = fname.replace(" ", "_").strip()+".m3u"
        if os.path.exists(playlists+fname) is False:
            fn=open(playlists+fname, "a")
            shutil.copy(temp+filename, playlists+fname)

        if os.path.exists(playlists+fname) is True:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Lista exportada!", 3 , art+'icon.png'))

################# Descarga Serie  ####################

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)    

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total) 
            #e = 'Velocidade: (%.0f Kb/s) ' % kbps_speed
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = 'Tiempo restante' + ': %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
            #if percent=xbmc.executebuiltin("XBMC.Notification(addonName,"+ mbs + e + ",'500000',"+iconpequeno+")")
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Descarga interrumpida')                              

class ziptools:

    def extract(self, file, dir, params):
        plugintools.log("file=%s" % file)

        if not dir.endswith(':') and not os.path.exists(dir):
            os.mkdir(dir)

        zf = zipfile.ZipFile(file)
        self._createstructure(file, dir)
        num_files = len(zf.namelist())

        for name in zf.namelist():
            plugintools.log("name=%s" % name)
            if not name.endswith('/'):
                plugintools.log("no es un directorio")
                plugintools.log("dst_folder= "+dir)                                
                try:
                    (path,file) = os.path.split(os.path.join(dir, name))
                    plugintools.log("path=%s" % path)
                    plugintools.log("name=%s" % name)
                    os.makedirs( path )
                except:
                    pass
                outfilename = os.path.join(dir, name)
                plugintools.log("outfilename=%s" % outfilename)
                try:
                    outfile = open(outfilename, 'wb')
                    outfile.write(zf.read(name))
                except:
                    plugintools.log("Error en fichero "+name)

    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)

    def create_necessary_paths(filename):
        try:
            (path,name) = os.path.split(filename)
            os.makedirs( path)
        except:
            pass
    def _makedirs(self, directories, basedir):
        for dir in directories:
            curdir = os.path.join(temp, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)

    def _listdirs(self, file):
        zf = zipfile.ZipFile(file)
        dirs = []
        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)
        dirs.sort()
        return dirs
############################################# By PalcoTv Team ####################################################
            
