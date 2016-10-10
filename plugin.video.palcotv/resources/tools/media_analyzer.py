# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Analizador de medios de PalcoTV
# Version 0.1 (11/12/2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a Juarrox
#------------------------------------------------------------

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import plugintools
import urllib2
import HTMLParser
import urllib,urlparse

from BeautifulSoup import BeautifulSoup as bs
from resources.tools.resolvers import *
import json

from __main__ import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

def plugin_analyzer(data, title, plot, datamovie, thumbnail, fanart):
    plugintools.log("[%s %s] Analizando plugin... %s " % (addonName, addonVersion, fanart))
    
    if data.startswith("plugin://plugin.video.SportsDevil/") == True:
        url = data.strip()
        plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [SportsDevil][/I][/COLOR]', url = url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif data.startswith("plugin://plugin.video.f4mTester") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [F4M][/I][/COLOR]', plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                    
    elif data.startswith("plugin://plugin.video.youtube") == True:
        if data.startswith("plugin://plugin.video.youtube/channel/") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] Channel][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )            
        elif data.startswith("plugin://plugin.video.youtube/user/") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] User][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        elif data.startswith("plugin://plugin.video.youtube/playlist/") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] Playlist][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )            
        elif data.startswith("plugin://plugin.video.youtube/play/?playlist_id") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] Playlist][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )            
        else:
            plugintools.runAddon( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] Video][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
       
    elif data.find("plugin.video.p2p-streams") == True:                        
        if data.find("mode=1") >= 0 :  # Acestream
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Acestream][/I][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        
        elif data.find("mode=2") >= 0 :  # Sopcast
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Sopcast][/I][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

        elif data.find("mode=401") >= 0 :  # P2P-Streams Parser
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [p2p-streams][/I][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )            

    elif data.startswith("plugin://plugin.video.p2psport") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [P2P Sport][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif data.startswith("plugin://plugin.video.live.streamspro") == True:
        if data.strip().find("mode=1&name=") >=0 or data.strip().find("makelist") >=0 :  # Parcheado por DMO: Soporte de pseudo parsers de LSP y listas  (DMO)
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [LiveStreams][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        else:
            plugintools.runAddon( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [LiveStreams][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            
    elif data.startswith("plugin://plugin.video.stalker") == True:
        mac=plugintools.read('https://copy.com/HuEtREKgnvlc9XrS');  # Mac Arena+
        data=data.replace("MAC_STALKER", mac).strip()
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Stalker][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )

    elif data.startswith("plugin://plugin.video.dailymotion_com") == True:  # Dailymotion (2.1.5)
        if data.find("mode=showPlaylist") >= 0:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Dailymotion Playlist][/I][/COLOR]', url = data , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        else:
            plugintools.runAddon( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Dailymotion Video][/I][/COLOR]', url = data , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )

    elif data.startswith("plugin://plugin.video.ArenaDevil") == True:  # ArenaDevil modules
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [ArenaDevil][/I][/COLOR]', url = data , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif data.startswith("plugin://plugin.video.videodevil") == True:  # VideoDevil modules
        plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [VideoDevil][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )          
		
    elif data.startswith("plugin://plugin.video.pelisalacarta") == True:  # Pelisalacarta
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Pelisalacarta][/I][/COLOR]' , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif data.startswith("plugin://script.extendedinfo") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [ExtendedInfo][/I][/COLOR]' , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif data.startswith("plugin://plugin.video.pulsar/movie/") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Pulsar][/I][/COLOR]' , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )        

    else:        
        plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Addon][/I][/COLOR]' , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
      

def p2p_builder_url(url, title_fixed, p2p):

    if p2p == "ace":
        p2p_launcher = plugintools.get_setting("p2p_launcher")
        plugintools.log("p2p_launcher= "+p2p_launcher)        
        if p2p_launcher == "0":
            url = 'plugin://program.plexus/?url='+url+'&mode=1&name='+title_fixed
        else:
            url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed

    elif p2p == "sop":
        p2p_launcher = plugintools.get_setting("p2p_launcher")
        plugintools.log("p2p_launcher= "+p2p_launcher)
        if p2p_launcher == "0":
            url = 'plugin://program.plexus/?url='+url+'&mode=2&name='+title_fixed
        else:
            url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=2&name='+title_fixed

    elif p2p == "torrent":
        url = urllib.quote_plus(url)
        addon_torrent = plugintools.get_setting("addon_torrent")
        if addon_torrent == "Stream":  # Stream (por defecto)
            url = 'plugin://plugin.video.stream/play/'+url
        elif addon_torrent == "Pulsar":  # Pulsar
            url = 'plugin://plugin.video.pulsar/play?uri=' + url     
        elif addon_torrent == "XBMCtorrent":  # XBMCtorrent
            url = 'plugin://plugin.video.quasar/play?uri=' + url
        elif addon_torrent == "Plexus":  # Plexus
            url = 'plugin://program.plexus/?url=' + url
        elif addon_torrent == "Quasar":  # Quasar
            url = 'plugin://plugin.video.quasar/play?uri=' + url
        elif addon_torrent == "YATP":  # YATP
            url = 'plugin://plugin.video.yatp/play?uri=' + url              

    elif p2p == "magnet":
        addon_magnet = plugintools.get_setting("addon_magnet")
        if addon_magnet == "0":  # Stream (por defecto)
            url = 'plugin://plugin.video.stream/play/'+url
        elif addon_magnet == "1":  # Pulsar
            url = 'plugin://plugin.video.pulsar/play?uri=' + url
        elif addon_magnet == "2":  # Kmediatorrent
            url = 'plugin://plugin.video.kmediatorrent/play/'+url
        elif addon_magnet == "3":  # XBMCtorrent
            url = 'plugin://plugin.video.xbmctorrent/play?uri=' + url             
        elif addon_magnet == "4":  # Quasar
            url = 'plugin://plugin.video.quasar/play?uri=' + url
        elif addon_magnet == "5":  # YATP
            url = 'plugin://plugin.video.yatp/play?uri=' + url               

    plugintools.log("[%s %s] Creando llamada para URL P2P... %s " % (addonName, addonVersion, url))
    return url

def video_analyzer(url):
    plugintools.log("[%s %s] Análisis de URL de vídeo... " % (addonName, addonVersion))
    
    if url.find("allmyvideos") >=0: server = "allmyvideos"
    elif url.find("vidspot") >= 0: server = "vidspot"
    elif url.find("played") >= 0: server = "playedto"
    elif url.find("streamin.to") >= 0: server = "streaminto"
    elif url.find("streamcloud") >= 0: server = "streamcloud"
    elif url.find("nowvideo") >= 0: server = "nowvideo"
    elif url.find("veehd") >= 0: server = "veehd"
    elif url.find("vk") >= 0: server = "vk"
    elif url.find("lidplay") >= 0: server = "vk"   
    elif url.find("tumi") >= 0: server = "tumi"
    elif url.find("novamov") >= 0: server = "novamov"
    elif url.find("moevideos") >= 0: server = "moevideos"
    elif url.find("gamovideo") >= 0: server = "gamovideo"
    elif url.find("movshare") >= 0: server = "movshare"
    elif url.find("powvideo") >= 0: server = "powvideo"
    elif url.find("mail.ru") >= 0: server = "mailru"
    elif url.find("mediafire") >= 0: server = "mediafire"
    elif url.find("netu") >= 0: server = "netu"
    elif url.find("waaw") >= 0: server = "waaw"
    elif url.find("movreel") >= 0: server = "movreel"
    elif url.find("videobam") >= 0: server = "videobam"
    elif url.find("vimeo/videos") >= 0: server = "vimeo"
    elif url.find("vimeo/channels") >= 0: server = "vimeo_pl"        
    elif url.find("veetle") >= 0: server = "veetle"
    elif url.find("videoweed") >= 0: server = "videoweed"
    elif url.find("streamable") >= 0: server = "streamable"
    elif url.find("rocvideo") >= 0: server = "rocvideo"
    elif url.find("realvid") >= 0: server = "realvid"
    elif url.find("videomega") >= 0: server = "videomega"
    elif url.find("video.tt") >= 0: server = "videott"
    elif url.find("flashx") >= 0: server = "flashx"
    elif url.find("openload") >= 0: server = "openload"
    elif url.find("turbovideos") >= 0: server = "turbovideos"
    elif url.find("ok.ru") >= 0: server = "okru"
    elif url.find("vidto") >= 0: server = "vidtome"
    elif url.find("playwire") >= 0: server = "playwire" 
    elif url.find("copiapop") >= 0: server = "copiapop"   
    elif url.find("vimple") >= 0: server = "vimple"
    elif url.find("vidgg") >= 0: server = "vidggto"
    elif url.find("uptostream") >= 0: server = "uptostream"
    elif url.find("youwatch") >= 0: server = "youwatch"
    elif url.find("idowatch") >= 0: server = "idowatch"
    elif url.find("cloudtime") >= 0: server = "cloudtime"
    elif url.find("allvid") >= 0: server = "allvid"
    elif url.find("vodlocker") >= 0: server = "vodlocker"
    elif url.find("vidzi") >= 0: server = "vidzitv"
    elif url.find("streame") >= 0: server = "streamenet"
    elif url.find("myvideoz") >= 0: server = "myvideoz"
    elif url.find("streamplay") >= 0: server = "streamplay"
    elif url.find("watchonline") >= 0: server = "watchonline"
    elif url.find("rutube") >= 0: server = "rutube"
    elif url.find("dailymotion") >= 0: server = "dailymotion"
    elif url.find("auroravid") >= 0: server = "auroravid"
    elif url.find("wholecloud") >= 0: server = "wholecloud"
    elif url.find("bitvid") >= 0: server = "bitvid"
    elif url.find("spruto") >= 0: server = "spruto"
    elif url.find("stormo") >= 0: server = "stormo"
    elif url.find("myvi.ru") >= 0: server = "myviru"
    elif url.find("youtube") >= 0: server = "youtube"
    elif url.find("filmon") >= 0: server = "filmon"
    elif url.find("thevideo.me") >= 0: server = "thevideome"
    elif url.find("videowood") >= 0: server = "videowood"
    elif url.find("neodrive") >= 0: server = "neodrive"
    elif url.find("cloudzilla") >= 0: server = "cloudzilla"
    elif url.find("thevideobee") >= 0: server = "thevideobee"
    elif url.find("fileshow") >= 0: server = "fileshow"
    elif url.find("vid.ag") >= 0: server = "vid"
    elif url.find("vidxtreme") >= 0: server = "vidxtreme"
    elif url.find("vidup") >= 0: server = "vidup"
    elif url.find("watchvideo") >= 0: server = "watchvideo"
    elif url.find("speedvid") >= 0: server = "speedvid"
    elif url.find("chefti.info") >= 0: server = "exashare"
    elif url.find("ajihezo.info") >= 0: server = "exashare"
    elif url.find("erd9x4.info") >= 0: server = "exashare"
    elif url.find("bojem3a.info") >= 0: server = "exashare"
    elif url.find("vodbeast") >= 0: server = "vodbeast"
    elif url.find("nosvideo") >= 0: server = "nosvideo"
    elif url.find("noslocker") >= 0: server = "noslocker"
    elif url.find("up2stream") >= 0: server = "up2stream"
    elif url.find("diskokosmiko") >= 0: server = "diskokosmiko"
    elif url.find("smartvid") >= 0: server = "smartvid"
    elif url.find("greevid") >= 0: server = "greevid"
    elif url.find("letwatch") >= 0: server = "letwatch"
    elif url.find("yourupload") >= 0: server = "yourupload"
    elif url.find("zalaa") >= 0: server = "zalaa" 
    elif url.find("uploadc") >= 0: server = "uploadc" 
    elif url.find("mp4upload") >= 0: server = "mp4upload"
    elif url.find("rapidvideo") >= 0: server = "rapidvideo"
    elif url.find("yourvideohost") >= 0: server = "yourvideohost"
    elif url.find("watchers") >= 0: server = "watchers"
    elif url.find("vidtodo") >= 0: server = "vidtodo"
    elif url.find("izanagi") >= 0: server = "izanagi"
    elif url.find("yotta") >= 0: server = "yotta"
    elif url.find("kami") >= 0: server = "kami"
    elif url.find("touchfile") >= 0: server = "touchfile"
    elif url.find("zstream") >= 0: server = "zstream"
    elif url.find("vodlock") >= 0: server = "vodlock"
    elif url.find("goodvideohost") >= 0: server = "goodvideohost"
    elif url.find("happystreams") >= 0: server = "happystreams"     
    else: server = 'unknown'
    return server
    '''
    print url;print playable
    
    if url.find("streamcloud") >=0: 
        if playable == True: streamcloud(url)
        else: server = "streamcloud";return server
    else: return 'unknown'
    '''
def server_analyzer(params):
    plugintools.log("[%s %s] Análisis de Servidores de vídeo... " % (addonName, addonVersion))

    url_final = params.get("url")
    plugintools.log(">>>>> Analizando Servidor Para la Url= "+ url_final)
    
    if url_final.find("allmyvideos") >= 0: params["url"]=url_final; allmyvideos(params)
    elif url_final.find("vidspot") >= 0: params["url"]=url_final; vidspot(params)
    elif url_final.find("played.to") >= 0: params["url"]=url_final; playedto(params)
    elif url_final.find("streamin.to") >= 0: params["url"]=url_final; streaminto(params)
    elif url_final.find("streamcloud") >= 0: params["url"]=url_final; streamcloud(params)
    elif url_final.find("nowvideo.sx") >= 0: params["url"]=url_final; nowvideo(params)
    elif url_final.find("veehd") >= 0: params["url"]=url_final; veehd(params)
    elif url_final.find("vk") >= 0: params["url"]=url_final; vk(params)
    elif url_final.find("lidplay") >= 0: params["url"]=url_final; vk(params)
    elif url_final.find("tumi.tv") >= 0: params["url"]=url_final; tumi(params)
    elif url_final.find("novamov") >= 0: params["url"]=url_final; novamov(params)
    elif url_final.find("moevideos") >= 0: params["url"]=url_final; moevideos(params)
    elif url_final.find("gamovideo") >= 0: params["url"]=url_final; gamovideo(params)
    elif url_final.find("movshare") >= 0: params["url"]=url_final; movshare(params)
    elif url_final.find("powvideo") >= 0: params["url"]=url_final; powvideo(params)
    elif url_final.find("mail.ru") >= 0: params["url"]=url_final; mailru(params)
    elif url_final.find("mediafire") >= 0: params["url"]=url_final; mediafire(params)
    elif url_final.find("netu") >= 0: params["url"]=url_final; netu(params)
    elif url_final.find("waaw") >= 0: params["url"]=url_final; waaw(params)
    elif url_final.find("movreel") >= 0: params["url"]=url_final; movreel(params)
    elif url_final.find("videobam") >= 0: params["url"]=url_final; videobam(params)    
    elif url_final.find("vimeo/videos") >= 0: params["url"]=url_final; vimeo(params)
    elif url_final.find("vimeo/channels") >= 0: params["url"]=url_final; vimeo_pl(params)
    elif url_final.find("veetle") >= 0: params["url"]=url_final; veetle(params)
    elif url_final.find("videoweed") >= 0: params["url"]=url_final; videoweed(params)
    elif url_final.find("streamable") >= 0: params["url"]=url_final; streamable(params)
    elif url_final.find("rocvideo") >= 0: params["url"]=url_final; rocvideo(params)
    elif url_final.find("realvid") >= 0: params["url"]=url_final; realvid(params)
    elif url_final.find("videomega") >= 0: params["url"]=url_final; videomega(params)
    elif url_final.find("video.tt") >= 0: params["url"]=url_final; videott(params)
    elif url_final.find("flashx") >= 0: params["url"]=url_final; flashx(params)
    elif url_final.find("openload") >= 0: params["url"]=url_final; openload(params)
    elif url_final.find("turbovideos") >= 0: params["url"]=url_final; turbovideos(params)
    elif url_final.find("ok.ru") >= 0: params["url"]=url_final; okru(params)
    elif url_final.find("vidto.me") >= 0: params["url"]=url_final; vidtome(params)
    elif url_final.find("playwire") >= 0: params["url"]=url_final; playwire(params)
    elif url_final.find("copiapop") >= 0: params["url"]=url_final; copiapop(params)
    elif url_final.find("vimple.ru") >= 0: params["url"]=url_final; vimple(params)
    elif url_final.find("vidgg") >= 0: params["url"]=url_final; vidggto(params)
    elif url_final.find("uptostream.com") >= 0: params["url"]=url_final; uptostream(params)
    elif url_final.find("youwatch") >= 0: params["url"]=url_final; youwatch(params)
    elif url_final.find("smed79") >= 0: params["url"]=url_final; youwatch(params)
    elif url_final.find("idowatch") >= 0: params["url"]=url_final; idowatch(params)
    elif url_final.find("cloudtime") >= 0: params["url"]=url_final; cloudtime(params)
    elif url_final.find("allvid") >= 0: params["url"]=url_final; allvid(params)
    elif url_final.find("vodlocker") >= 0: params["url"]=url_final; vodlocker(params)
    elif url_final.find("vidzi.tv") >= 0: params["url"]=url_final; vidzitv(params)
    elif url_final.find("streame.net") >= 0: params["url"]=url_final; streamenet(params)
    elif url_final.find("myvideoz") >= 0: params["url"]=url_final; myvideoz(params)
    elif url_final.find("streamplay") >= 0: params["url"]=url_final; streamplay(params)
    elif url_final.find("watchonline") >= 0: params["url"]=url_final; watchonline(params)
    elif url_final.find("rutube") >= 0: params["url"]=url_final; rutube(params)
    elif url_final.find("dailymotion") >= 0: params["url"]=url_final; dailymotion(params)
    elif url_final.find("auroravid") >= 0: params["url"]=url_final; auroravid(params)
    elif url_final.find("wholecloud") >= 0: params["url"]=url_final; wholecloud(params)
    elif url_final.find("bitvid") >= 0: params["url"]=url_final; bitvid(params)
    elif url_final.find("spruto") >= 0: params["url"]=url_final; spruto(params)
    elif url_final.find("stormo") >= 0: params["url"]=url_final; stormo(params)
    elif url_final.find("myvi.ru") >= 0: params["url"]=url_final; myviru(params)
    elif url_final.find("youtube.com") >= 0: params["url"]=url_final; youtube(params)
    elif url_final.find("filmon.com") >= 0: params["url"]=url_final; filmon(params)
    elif url_final.find("thevideo.me") >= 0: params["url"]=url_final; thevideome(params)
    elif url_final.find("videowood.tv") >= 0: params["url"]=url_final; videowood(params)
    elif url_final.find("neodrive.co") >= 0: params["url"]=url_final; neodrive(params)
    elif url_final.find("cloudzilla") >= 0: params["url"]=url_final; cloudzilla(params)
    elif url_final.find("thevideobee.to") >= 0: params["url"]=url_final; thevideobee(params)
    elif url_final.find("fileshow.tv") >= 0: params["url"]=url_final; fileshow(params)
    elif url_final.find("vid.ag") >= 0: params["url"]=url_final; vid(params)
    elif url_final.find("vidxtreme.to") >= 0: params["url"]=url_final; vidxtreme(params)
    elif url_final.find("vidup") >= 0: params["url"]=url_final; vidup(params)
    elif url_final.find("watchvideo") >= 0: params["url"]=url_final; watchvideo(params)
    elif url_final.find("speedvid") >= 0: params["url"]=url_final; speedvid(params)
    elif url_final.find("chefti.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("ajihezo.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("bojem3a.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("erd9x4.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("vodbeast") >= 0: params["url"]=url_final; vodbeast(params)
    elif url_final.find("nosvideo") >= 0: params["url"]=url_final; nosvideo(params)
    elif url_final.find("noslocker") >= 0: params["url"]=url_final; noslocker(params)
    elif url_final.find("up2stream") >= 0: params["url"]=url_final; up2stream(params)
    elif url_final.find("diskokosmiko") >= 0: params["url"]=url_final; diskokosmiko(params)
    elif url_final.find("smartvid") >= 0: params["url"]=url_final; smartvid(params)
    elif url_final.find("greevid") >= 0: params["url"]=url_final; greevid(params)
    elif url_final.find("letwatch") >= 0: params["url"]=url_final; letwatch(params)
    elif url_final.find("yourupload") >= 0: params["url"]=url_final; yourupload(params)
    elif url_final.find("zalaa") >= 0: params["url"]=url_final; zalaa(params)
    elif url_final.find("uploadc") >= 0: params["url"]=url_final; uploadc(params)
    elif url_final.find("mp4upload") >= 0: params["url"]=url_final; mp4upload(params)
    elif url_final.find("rapidvideo") >= 0: params["url"]=url_final; rapidvideo(params)
    elif url_final.find("yourvideohost") >= 0: params["url"]=url_final; yourvideohost(params)
    elif url_final.find("watchers") >= 0: params["url"]=url_final; watchers(params)
    elif url_final.find("vidtodo") >= 0: params["url"]=url_final; vidtodo(params)
    elif url_final.find("izanagi") >= 0: params["url"]=url_final; izanagi(params)
    elif url_final.find("yotta") >= 0: params["url"]=url_final; yotta(params)
    elif url_final.find("kami") >= 0: params["url"]=url_final; kami(params)
    elif url_final.find("touchfile") >= 0: params["url"]=url_final; touchfile(params)
    elif url_final.find("zstream") >= 0: params["url"]=url_final; zstream(params)
    elif url_final.find("vodlock") >= 0: params["url"]=url_final; vodlock(params)
    elif url_final.find("goodvideohost") >= 0: params["url"]=url_final; goodvideohost(params)
    elif url_final.find("happystreams") >= 0: params["url"]=url_final; happystreams(params)
    
def parser_title(title):
    #plugintools.log('[%s %s].parserr_title %s' % (addonName, addonVersion, title))

    cyd=title;patcolor=plugintools.find_multiple_matches(cyd, '\[([^\]]+)')
    for entry in patcolor:
        entry='['+entry+']'
        cyd=cyd.replace(entry, "")

    cyd=cyd.replace("/", "").replace("[", "").replace("]", "").replace("&quot;", '"')
    cyd=cyd.replace("[/COLOR]", "").replace("[B]", "").replace("[/B]", "").replace("[I]", "").replace("[/I]", "")
    cyd=cyd.replace("[Auto]", "").replace("[Parser]", "").replace("[TinyURL]", "").replace("[Auto]", "").replace("[Filtros]", "").replace("[Filtro]", "")    
    cyd = cyd.replace("[", "").replace("]", "").replace("[B]", "").replace("[I]", "").replace("[/B]", "").replace("[/I]", "")  # Control para evitar errores al crear archivos

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")
    cyd = cyd.replace(" [Multilink]", "")
    cyd = cyd.replace(" [Multi]", "").replace("[Multi]", "")
    cyd = cyd.replace(" [Multiparser]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]PLX[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]M3U[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]", "")
    cyd = cyd.replace(' [COLOR gold][CBZ][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][CBR][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][Mediafire][/COLOR]', "")
    cyd = cyd.replace(' [CBZ]', "")
    cyd = cyd.replace(' [CBR]', "")
    cyd = cyd.replace(' [Mediafire]', "")
    cyd = cyd.replace(' [EPG-TXT]', "")    

    title=cyd
    if title.endswith(" .plx") == True:
        title = title.replace(" .plx", ".plx")

    return cyd

def launch_magnet(params):
    plugintools.log('[%s %s] launch_magnet... %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    addon_magnet = plugintools.get_setting("addon_magnet")
    plugintools.log("Addon para ejecutar archivo Magnet: "+addon_magnet)
    #url = urllib.quote_plus(url)
    if addon_magnet == "0":  # Stream (por defecto)
        url = 'plugin://plugin.video.stream/play/'+url
        plugintools.log("Iniciando Stream... "+url)
    elif addon_magnet == "1":  # Pulsar
        url = 'plugin://plugin.video.pulsar/play?uri=' + url
        plugintools.log("Iniciando Pulsar... "+url)
    elif addon_magnet == "2":  # KMediaTorrent
        url = 'plugin://plugin.video.kmediatorrent/play/'+url
        plugintools.log("Iniciando KMediaTorrent... "+url)
    elif addon_magnet == "3":  # XBMCtorrent
        url = 'plugin://plugin.video.xbmctorrent/play/'+url
        plugintools.log("Iniciando XBMCtorrent... "+url)
    elif addon_magnet == "4":  # Quasar
        url = 'plugin://plugin.video.quasar/play?uri=' + url
        plugintools.log("Iniciando Quasar... "+url)      
        
    plugintools.log("Magnet URL= "+url)
    plugintools.play_resolved_url(url)

def launch_torrent(params):
    plugintools.log('[%s %s] launch_torrent... %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")

    addon_torrent = plugintools.get_setting("addon_torrent")
    #url = urllib.quote_plus(url)
    if addon_torrent == "0":  # Stream (por defecto)
        url = 'plugin://plugin.video.stream/play/'+url
        plugintools.log("Iniciando Stream... "+url)
    elif addon_torrent == "1":  # Pulsar
        url = 'plugin://plugin.video.pulsar/play?uri=' + url
        plugintools.log("Iniciando Pulsar... "+url)
    elif addon_torrent == "2":  # XBMCtorrent
        url = 'plugin://plugin.video.xbmctorrent/play/' + url
        plugintools.log("Iniciando XBMCtorrent... "+url)
    elif addon_torrent == "3":  # Plexus
        plugintools.log("Iniciando Plexus... "+url)
        url = 'plugin://plugin.program.plexus/?url=http://'+url+'&mode=1&name='
    elif addon_torrent == "4":  # Quasar
        url = 'plugin://plugin.video.quasar/play?uri=' + url
        plugintools.log("Iniciando Quasar... "+url)   

    plugintools.log("Torrent File= "+url)
    plugintools.play_resolved_url(url)
    
def devil_analyzer(url,ref):
    url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url+'%26referer='+referer
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')
