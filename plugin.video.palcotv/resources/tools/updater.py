# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
# PalcoTV Updater v0.2 (21.10.2014)
# Version 0.3.0 (18.10.2014)
#---------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de Jesús (www.mimediacenter.info)
#---------------------------------------------------------------------


import os, sys, urllib, urllib2, re, shutil, zipfile
import xbmc, xbmcgui, xbmcaddon, xbmcplugin, time
import plugintools
from dateutil.parser import parse

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


home = xbmcaddon.Addon().getAddonInfo('path')+'/'
playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
art = xbmc.translatePath(os.path.join(addonPath,'art/'))


# Comprobamos qué versión es la más reciente
def check_update(params):
    plugintools.log("[%s %s] Checking updates... %s" % (addonName, addonVersion, repr(params)))    

    data = plugintools.read( params.get("url") )
    plotter="";datamovie = {}
    #plugintools.log("data= "+data)
    title = params.get("title")
    name_channel = parser_title(title);print name_channel
    # name_channel = parser_title(name_channel)
    data_update = plugintools.find_single_match(data, '<name>'+name_channel+'(.*?)</channel>');print data_update
    subchannel = plugintools.find_multiple_matches(data_update, '<subchannel>(.*?)</subchannel>')
    #datamovie["Plot"]='Módulo de actualizaciones para [B]Arena+[/B]'
    #plugintools.add_item(action = "", title = '[COLOR gold]Updater Arena+[/COLOR]', url = "" , info_labels=datamovie, thumbnail = params.get("thumbnail") , fanart = params.get("fanart") , folder = False , isPlayable = False)    
    i = 0
    for entry in subchannel:
        try:
            #plugintools.log("entry= "+entry)
            title = plugintools.find_single_match(entry, '<name>(.*?)</name>')
            url = plugintools.find_single_match(entry, '<url>([^<]+)</url>')
            thumbnail = plugintools.find_single_match(entry, '<thumbnail>([^<]+)</thumbnail>')
            version = plugintools.find_single_match(entry, '<version>([^<]+)</version>')
            author = plugintools.find_single_match(entry, '<author>([^<]+)</author>')
            size_remote = plugintools.find_single_match(entry, '<filesize>([^<]+)</filesize>')
            ts_remote = plugintools.find_single_match(entry, '<update>([^<]+)</update>')
            path = plugintools.find_single_match(entry, '<path>([^<]+)</path>')
            fanart = plugintools.find_single_match(entry, '<fanart>([^<]+)')
            datamovie["Plot"] = '[COLOR white]'+plugintools.find_single_match(entry, '<changelog>(.*?)</changelog>')+'[/COLOR]'
            f = open(home+path, 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            last_modified = time.ctime(os.path.getmtime(home+path))  # Última modificación del archivo
            dt = parse(last_modified)
            ts_local = time.mktime(dt.timetuple())
            ts = parse(ts_remote)
            ts_remote = time.mktime(ts.timetuple())
            print 'ts_local',ts_local  # Última modificación del archivo local
            print 'ts_remote',ts_remote  # Última modificación del archivo remoto
            if int(ts_remote) <= int(ts_local) :
                plugintools.log("[%s %s] No es necesario actualizar el módulo= %s " % (addonName, addonVersion, path))
            else:
                # Hay que actualizar, así que mostramos la entrada
                #plugintools.addShow(action = "update_file", title = '[COLOR white]'+title+'[/COLOR][COLOR lightblue][I] [' + author + '][/I][/COLOR][COLOR lightgreen][I] [' + version + '][/I][/COLOR]', url = url , info_labels=datamovie, thumbnail = thumbnail , extra = home+path , fanart = fanart , folder = False , isPlayable = False)
                plugintools.log("[%s %s] Nueva actualización: %s " % (addonName, addonVersion, path))
                i = i + 1
                # Guardamos sinopsis de actualizaciones
                if plotter == "": plotter = '[COLOR white]'+title+'[/COLOR][COLOR lightblue][I] [' + author + '][/I][/COLOR][COLOR lightgreen][I] [' + version + '][/I][/COLOR]'
                else: plotter = plotter+'[CR]'+'[COLOR white]'+title+'[/COLOR][COLOR lightblue][I] [' + author + '][/I][/COLOR][COLOR lightgreen][I] [' + version + '][/I][/COLOR]'              

        except: plugintools.log("Error en lectura de entrada: "+title)
        pass        
                    
    if i != 0:
        datamovie["Plot"]=plotter
        plugintools.addDir(action = "updater_menu", title = '[COLOR lightblue]Actualizaciones [COLOR lightyellow][B][I]('+str(i)+')[/COLOR][/I][/B][/COLOR]', url = params.get("url"), plot=params.get("plot"), info_labels=datamovie, thumbnail = params.get("thumbnail") , fanart = params.get("fanart") , folder = True, isPlayable = False)
    else:
        pass
        #plugintools.addShow(action = "", title = '[COLOR white]No hay actualizaciones pendientes[/COLOR]', url = "" , info_labels=datamovie, thumbnail = 'http://www.clker.com/cliparts/U/b/3/E/T/z/ok-icon-hi.png' , fanart = params.get("fanart") , folder = False , isPlayable = False)
        #plugintools.addShow(action = "", title = '[COLOR lightblue]Actualizaciones [/COLOR][COLOR lightyellow][B][I](0)[/I][/B][/COLOR]', url = "" , info_labels=datamovie, thumbnail = 'http://www.clker.com/cliparts/U/b/3/E/T/z/ok-icon-hi.png' , fanart = params.get("fanart") , folder = False , isPlayable = False)
        


# Comprobamos qué versión es la más reciente
def updater_menu(params):
    plugintools.log("[%s %s] Opening Updater menu... %s" % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )
    datamovie = {}
    #plugintools.log("data= "+data)
    title = params.get("title")
    name_channel = parser_title(title);name_channel=name_channel.split("(")[0].strip()
    # name_channel = parser_title(name_channel)
    data_update = plugintools.find_single_match(data, '<name>'+name_channel+'(.*?)</channel>');print data_update
    subchannel = plugintools.find_multiple_matches(data_update, '<subchannel>(.*?)</subchannel>')
    
    i = 0
    try:
        for entry in subchannel:
            title = plugintools.find_single_match(entry, '<name>(.*?)</name>')
            url = plugintools.find_single_match(entry, '<url>([^<]+)</url>')
            thumbnail = plugintools.find_single_match(entry, '<thumbnail>([^<]+)</thumbnail>')
            version = plugintools.find_single_match(entry, '<version>([^<]+)</version>')
            author = plugintools.find_single_match(entry, '<author>([^<]+)</author>')
            size_remote = plugintools.find_single_match(entry, '<filesize>([^<]+)</filesize>')
            ts_remote = plugintools.find_single_match(entry, '<update>([^<]+)</update>')
            path = plugintools.find_single_match(entry, '<path>([^<]+)</path>')
            fanart = plugintools.find_single_match(entry, '<fanart>([^<]+)')
            datamovie["Plot"] = '[COLOR white]'+plugintools.find_single_match(entry, '<changelog>(.*?)</changelog>')+'[/COLOR]'
            f = open(home+path, 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            last_modified = time.ctime(os.path.getmtime(home+path))  # Última modificación del archivo
            dt = parse(last_modified)
            ts_local = time.mktime(dt.timetuple())
            ts = parse(ts_remote)
            ts_remote = time.mktime(ts.timetuple())
            print 'ts_local',ts_local  # Última modificación del archivo local
            print 'ts_remote',ts_remote  # Última modificación del archivo remoto
            if int(ts_remote) <= int(ts_local) :
                plugintools.log("[%s %s] No es necesario actualizar el módulo: %s " % (addonName, addonVersion, path))
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.log("[%s %s] Actualización disponible: %s " % (addonName, addonVersion, path))
                if path == "version.dat":
                    plugintools.addShow(action = "update_palco", title = '[COLOR gold][B]'+title+'[/B][/COLOR][COLOR lightblue][I] [' + author + '][/I][/COLOR]', url = url , info_labels=datamovie, thumbnail = thumbnail , extra = size_remote , fanart = fanart , folder = False , isPlayable = False)
                    i = i + 1                
                elif path == "spdevil.dat":
                    plugintools.addShow(action = "update_addon", title = '[COLOR gold][B]'+title+'[/B][/COLOR][COLOR lightblue][I] [' + author + '][/I][/COLOR]', url = url , info_labels=datamovie, thumbnail = thumbnail , extra = size_remote , fanart = fanart , folder = False , isPlayable = False)
                    i = i + 1                
                else:
                    plugintools.addShow(action = "update_file", title = '[COLOR white]'+title+'[/COLOR][COLOR lightblue][I] [' + author + '][/I][/COLOR][COLOR lightgreen][I] [' + version + '][/I][/COLOR]', url = url , info_labels=datamovie, thumbnail = thumbnail , extra = home+path , fanart = fanart , folder = False , isPlayable = False)
                    i = i + 1
    except: pass                    
                    
    if i == 0:
        datamovie["Plot"]='¡Felicidades! Tu copia de [B]Arena+[/B] tiene todos los módulos actualizados ;)[CR][CR][COLOR red]NOTA:[/COLOR] Bugs o sugerencias a [B]juarrox@gmail.com[/B]'
        plugintools.addShow(action = "", title = '[COLOR white]No hay actualizaciones pendientes[/COLOR]', url = "" , info_labels=datamovie, thumbnail = 'http://www.clker.com/cliparts/U/b/3/E/T/z/ok-icon-hi.png' , fanart = params.get("fanart") , folder = False , isPlayable = False)
        



def update_file(params):
    plugintools.log("[PalcoTV-0.3.0].Update_now "+repr(params))

    nobackup = 0
    title = params.get("title").replace("[COLOR white]", "").split("[")[0]
    runUpdate = xbmcgui.Dialog().yesno(addonName, '¿Desea actualizar el módulo [B]'+title+'[/B]?')
    
    if(runUpdate):
        local_file = params.get("extra")
        local_filename = local_file.split("/")[-1]
        remote_file = params.get("url")
        runBackup = xbmcgui.Dialog().yesno(addonName, '¿Desea crear una copia de seguridad de [B]'+title+'[/B]?')
        if(runBackup):
            plugintools.log("Iniciando backup del módulo local...") 
            backup = local_filename.split(".py")[0];backup=backup+'-BAK.py'
            local_filebak = local_file.replace(local_filename, backup)
            try:
                shutil.copyfile(local_file, local_filebak)
            except:
                nobackup = -1
                pass
                    
    if(runUpdate):
        if nobackup == -1:
            runUpdateWithBackup = xbmcgui.Dialog().yesno(addonName, 'Error al crear [B]'+backup+'[/B]', '¿Desea continuar con la actualización?')
        if nobackup != -1 or runUpdateWithBackup:            
            progreso = xbmcgui.DialogProgressBG()
            progreso.create("Iniciando actualización... " , local_filename )
            yesno = 0
            plugintools.log("remote= "+remote_file)        
            r = urllib2.urlopen(remote_file)
            f = open(temp + local_filename, "wb")
            f.write(r.read())
            f.close()
            
            try:
                progreso.update(50, "Copiando archivo... " , local_filename)
                shutil.copyfile(temp + local_filename, local_file)        
                progreso.update(100, "Actualización completada! " , local_filename)
                progreso.close()
            except:
                progreso.update(0, "Error al sobreescribir! " , local_filename)
                pass       
                
            try:
                os.remove(temp + local_filename)
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (addonName, "Actualización completada!", 3 , art+'icon.png'))
                plugintools.log("Completada la actualización de "+fname)
            except:
                pass
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (addonName, "Actualización cancelada!", 3 , art+'icon.png'))
            plugintools.log("Error en la actualización de "+fname)

    xbmc.executebuiltin("Container.Refresh")


def update_palco(params):
    plugintools.log("[PalcoTV-0.3.0].update_palco "+repr(params))
    #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Espere...", 3 , art+'icon.png'))
    fname=addonId + "-"+parser_title(params.get("title")).replace("Arena+ ", "").split("[")[0].strip()+".zip"
    local_path = addons + fname
    remote_file = params.get("url")
    plugintools.log("local_path= "+local_path)
    plugintools.log("remote_file= "+remote_file)
    plugintools.log("fname= "+fname)
    #first_run(upgrade=True)
    
    runUpdate = xbmcgui.Dialog().yesno(addonName, '¿Desea actualizar el addon [B]'+fname+'[/B]?')
    
    if(runUpdate):
        runBackup = xbmcgui.Dialog().yesno(addonName, '¿Desea crear una copia de seguridad de [B]'+addonName+'[/B]?')
        if(runBackup):
            version_ts = time.ctime(os.path.getmtime(addonPath+'/version.dat'))  # Última modificación del archivo
            dt = parse(version_ts);ts_local = time.mktime(dt.timetuple())
            addonbak = addons + addonId+'-BAK-'+str(ts_local).split(".")[0]
            if os.path.exists(addonbak) is False:
                shutil.copytree(addons+addonId, addonbak)

            if os.path.exists(addonbak):  # Iniciamos actualización
                #try:
                dp = xbmcgui.DialogProgress()
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
                print 'archivo descargado'
                #except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (addonName, "Error en la descarga!", 3 , art+'icon.png')); return False;return False
                
                if os.path.isfile(local_path) is True:
                    size_remote = params.get("extra")
                    f = open(local_path, 'r')
                    f.seek(0,2)
                    dl_size = f.tell()
                    dl_size = str(dl_size)
                    #print 'dl_size',dl_size
                    #print 'size_remote',size_remote
                    if str(dl_size) == str(size_remote):
                        unzipper = ziptools()
                        unzipper.extract(local_path, addons, params)
                        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (addonName, "Actualización completada!", 3 , art+'icon.png'))
                else:            
                    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (addonName, "Error! No se encuentra archivo descargado", 3 , art+'icon.png'))
                    return False

                # Anotamos número de versión en archivo de control 'version.dat'
                vdat=addonPath+'/version.dat';print vdat
                try: f = open(vdat, "wb");version = fname.split("-")[1].replace(".zip", "").strip();vdat.write(version);f.close();plugintools.log("Versión: "+version)
                except: pass

                # Eliminamos archivo de descarga (debería ser opcional)
                try: os.remove(local_path)
                except: pass

    xbmc.executebuiltin("Container.Refresh")
            

def update_addon(params):
    plugintools.log("[PalcoTV-0.3.0].update_addon "+repr(params))
    #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Espere...", 3 , art+'icon.png'))
    fname='plugin.video.'+parser_title(params.get("title")).split("[")[0].strip()
    local_path = addons + fname+".zip"
    remote_file = params.get("url")
    plugintools.log("local_path= "+local_path)
    plugintools.log("remote_file= "+remote_file)
    plugintools.log("fname= "+fname)
    
    runUpdate = xbmcgui.Dialog().yesno(addonName, '¿Desea actualizar el addon [B]'+fname+'[/B]?')
    
    if(runUpdate):
        runBackup = xbmcgui.Dialog().yesno(addonName, '¿Desea crear una copia de seguridad de [B]'+fname+'[/B]?')
        if(runBackup):
            version_ts = time.ctime(os.path.getmtime(addonPath+'/spdevil.dat'))  # Última modificación del archivo
            dt = parse(version_ts);ts_local = time.mktime(dt.timetuple())
            addonbak = addons + fname+'-BAK-'+str(ts_local).split(".")[0]
            if os.path.exists(addonbak) is False:
                shutil.copytree(addons+fname, addonbak)

            if os.path.exists(addonbak):  # Iniciamos actualización
                try:
                    dp = xbmcgui.DialogProgress()
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
                    print 'archivo descargado'
                except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (addonName, "Error en la descarga!", 3 , art+'icon.png')); return False;return False
                
                if os.path.isfile(local_path) is True:
                    size_remote = params.get("extra")
                    f = open(local_path, 'r')
                    f.seek(0,2)
                    dl_size = f.tell()
                    dl_size = str(dl_size)
                    #print 'dl_size',dl_size
                    #print 'size_remote',size_remote
                    if str(dl_size) == str(size_remote):
                        unzipper = ziptools()
                        unzipper.extract(local_path, addons, params)
                        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (fname, "Actualización completada!", 3 , art+'icon.png'))
                else:            
                    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (fname, "Error! No se encuentra archivo descargado", 3 , art+'icon.png'))
                    return False

                # Anotamos número de versión en archivo de control 'version.dat'
                vdat=addonPath+'/spdevil.dat';plugintools.log("vdat= "+vdat)
                try: f = open(vdat, "wb");version = fname.split("-")[1].replace(".zip", "").strip();f.write(version);f.close();plugintools.log("Versión: "+version)
                except: pass

                # Eliminamos archivo de descarga (debería ser opcional)
                try: os.remove(local_path)
                except: pass

    xbmc.executebuiltin("Container.Refresh")
            



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

        dir = addons        
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
            curdir = os.path.join(addons, dir)
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
    
 

      
def parser_title(title):
    plugintools.log("[PalcoTV-0.3.0].parser_title " + title)

    cyd = title

    cyd = cyd.replace("[COLOR lightyellow]", "")
    cyd = cyd.replace("[COLOR green]", "")
    cyd = cyd.replace("[COLOR red]", "")
    cyd = cyd.replace("[COLOR blue]", "")    
    cyd = cyd.replace("[COLOR royalblue]", "")
    cyd = cyd.replace("[COLOR white]", "")
    cyd = cyd.replace("[COLOR pink]", "")
    cyd = cyd.replace("[COLOR cyan]", "")
    cyd = cyd.replace("[COLOR steelblue]", "")
    cyd = cyd.replace("[COLOR forestgreen]", "")
    cyd = cyd.replace("[COLOR olive]", "")
    cyd = cyd.replace("[COLOR khaki]", "")
    cyd = cyd.replace("[COLOR lightsalmon]", "")
    cyd = cyd.replace("[COLOR orange]", "")
    cyd = cyd.replace("[COLOR lightgreen]", "")
    cyd = cyd.replace("[COLOR lightblue]", "")
    cyd = cyd.replace("[COLOR lightpink]", "")
    cyd = cyd.replace("[COLOR skyblue]", "")
    cyd = cyd.replace("[COLOR darkorange]", "")    
    cyd = cyd.replace("[COLOR greenyellow]", "")
    cyd = cyd.replace("[COLOR yellow]", "")
    cyd = cyd.replace("[COLOR yellowgreen]", "")
    cyd = cyd.replace("[COLOR orangered]", "")
    cyd = cyd.replace("[COLOR grey]", "")
    cyd = cyd.replace("[COLOR gold]", "")
    cyd = cyd.replace("[COLOR=FF00FF00]", "")  
                
    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[Multi]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")

    title = cyd
    title = title.strip()
    plugintools.log("title_parsed= "+title)
    return title


class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)
