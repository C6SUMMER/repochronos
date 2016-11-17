import sys, traceback
###################################################################### DMO ######################################################################
import requests
import xbmcgui
import plugintools  # Gracias PalcoTV y su creador JuarroX, por esta Herramienta

mi_version = ["2016","10","23"]  # OJO!! Cambiar la Version, por supuesto... AQUI Y EN EL FICHERO DE LA NUBE

#r = requests.get("http://pastebin.com/raw/4Frg1rC2")
r = requests.get("http://pastebin.com/raw/2baqp6N8")

data = r.content

fecha = plugintools.find_single_match(data,'sportsdevil>(.*?)<')
version = plugintools.find_single_match(data,'spdVer>(.*?)<')
if len(version) <> 0:
	version = "Ver. "+version
else:
	version ="Ultima Version"
	
ult_version = fecha.split(".")

hay_nueva = False
if mi_version[0] <> ult_version[0]:
	hay_nueva = True
else:
	if mi_version[1] < ult_version[1]:
		hay_nueva = True
	else:
		if mi_version[2] < ult_version[2]:
			hay_nueva = True
			
if hay_nueva == True:
	titu = "ATENCION!!!!"
	lin1 = "         Version [COLOR red]OBSOLETA de SportsDevil[/COLOR] updated by DMO"
	lin2 = " Ya tienes disponible la [COLOR lime]"+version+"[/COLOR] para poder actualizarlo."
	lin3 = "         [COLOR yellow]Descarga:[/COLOR] [COLOR red][B]http://adf.ly/7448402/spdevil-dmo[/COLOR][/B]"
	xbmcgui.Dialog().ok(titu, lin1, lin2, lin3)
###################################################################### DMO ######################################################################














# REMOTE DEBUGGING
REMOTE_DBG = False

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pydevd
        # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True, suspend=False)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)
    except:
        sys.stderr.write('Remote Debugger is not started')




# ACTUAL ADDON
from lib import main

try:
    myAddon = main.Main()
    myAddon.run(sys.argv)
except:
    traceback.print_exc(file = sys.stdout)