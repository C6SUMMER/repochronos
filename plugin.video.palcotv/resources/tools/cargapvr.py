# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de Cargar el TV-PVR
# Version 0.1 (29.05.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
import xbmc,plugintools,json
def cargapvr0(params):
 for i in json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid": "alltv"},"id": 1}'))['result']['channels']:
  #print str(i['channelid']),i['label'].encode('utf-8','ignore'),'_'*35
  plugintools.add_item(title=i['label'].encode('utf-8','ignore'),action='cargapvr1',url=params['url'],page=str(i['channelid']),thumbnail=params['thumbnail'],fanart=params['fanart'],isPlayable=True,folder=False);

def cargapvr1(params):
 play_id=params['page'];query='{"jsonrpc": "2.0","id": 1,"method": "Player.Open","params": {"item": {"channelid": '+play_id+'}}}'
 xbmc.executeJSONRPC(query)
 
def carga_pvr_grupos0(params):
 for i in json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannelGroups", "params": {"channeltype":"tv"},"id": 1}'))['result']['channelgroups']:
  plugintools.add_item(title=i['label'].encode('utf-8','ignore'),action='carga_pvr_grupos160',url=params['url'],page=str(i['channelgroupid']),thumbnail=params['thumbnail'],fanart=params['fanart'],isPlayable=False,folder=True);
def carga_pvr_grupos160(params):
 for i in json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid": '+params['page']+'},"id": 1}'))['result']['channels']:
  tit=i['label'].split(']')[1];tit=tit.encode('utf-8','ignore')
  plugintools.add_item(title=tit,action='carga_pvr_grupos161',url=params['url'],page=str(i['channelid']),thumbnail=params['thumbnail'],fanart=params['fanart'],isPlayable=True,folder=False);
def carga_pvr_grupos161(params):
 play_id=params['page'];query='{"jsonrpc": "2.0","id": 1,"method": "Player.Open","params": {"item": {"channelid": '+play_id+'}}}';xbmc.executeJSONRPC(query)