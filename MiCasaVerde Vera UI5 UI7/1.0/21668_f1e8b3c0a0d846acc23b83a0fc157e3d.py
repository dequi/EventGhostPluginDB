# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# This plugin is a Telnet server and an HTTP client that sends and receives MiCasaVerde UI5 and UI7 light states.
# This plugin is based on the Vera plugins by Rick Naething
#
# $LastChangedDate: 2015-10-10 20:51:00 -0700 $
# $LastChangedRevision: 9b $
# $LastChangedBy: K $


import eg

eg.RegisterPlugin(
    name = "MiCasaVerde Vera UI5 UI7",
    description = "Control of Dimmers and Switches on the MiCasaVerde Vera UI5 UI7",
    author = "K",
    version = "1.0",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    kind = "other",
    guid = '{321D9F7C-6961-4C62-B6E0-86C950A25279}'
    
)

import sys
import socket
import threading
from copy import deepcopy as dc

DEBUG = False
if DEBUG:
    def log(*args):
        args = list(args)
        for i in range(len(args)):
            if isinstance(args[i], str) or isinstance(args[i], unicode):
                args[i] += ': '
            else:
                args[i] = str(args[i])
        print "MiCasaVerde: "+"".join(args)

else:
    def log(*args): pass

def PE(*args):
    args = list(args)
    for i in range(len(args)):
        if isinstance(args[i], str) or isinstance(args[i], unicode):
            args[i] += ': '
        else:
            args[i] = str(args[i])
    eg.PrintError("MiCasaVerde: "+"".join(args))
    return False

def PN(*args):
    args = list(args)
    for i in range(len(args)):
        if isinstance(args[i], str) or isinstance(args[i], unicode):
            args[i] += ': '
        else:
            args[i] = str(args[i])
    eg.PrintNotice("MiCasaVerde: "+"".join(args))
    return True

class Text:
    PrefixBox = 'Event Prefix Settings'
    Prefix = 'Event Prefix: '
    VeraBox = 'Vera IP and Port Settings'
    VeraIP = 'IP: '
    VeraPort = 'Port: '
    DimmerBox = 'Set the Dim Level of a Dimmable Switch'
    ToggleBox = 'Toggle a Light or Binary Switch to Opposite of Current State'
    SwitchBox = 'Turn a Light or Binary Switch On or Off'
    SceneBox = 'Run A Scene'
    DeviceText = 'Device: '
    SceneText = 'Scene: '
    PercentText = 'Level: '
    StateText = 'ON or OFF: '
    FanModeBox = 'HVAC Fan Mode'
    FanModeText = 'Fan Mode: '
    OppModeBox = 'HVAC Opperating Mode'
    OppModeText = 'Opperating Mode: '
    HSetTempBox = 'HVAC Heat Set Temperature'
    CSetTempBox = 'HVAC Cool Set Temperature'
    TempText = 'Set Teperature: '
    AlarmBox = 'Arm or Disarm Alarm'
    AlarmText = 'Arm or Disarm: '
    class Scene:
        name = 'Run Scene'
        description = 'Runs a Vera Scene'
    class Dimmer:
        name = 'Set Light Level'
        description = 'Set the Dim Level of a Dimmable Switch'
    class Switch:
        name = 'Switch Power'
        description = 'Turn a Light or Binary Switch ON or OFF'
    class Toggle:
        name = 'Toggle Power'
        description = 'Toggle a Light or Binary Switch to Opposite of Current State'
    class FanMode:
        name = 'HVAC Fan Mode'
        description = 'Change the fan Mode on your HVAC Unit'
    class OppMode:
        name = 'HVAC Opperating Mode'
        description = 'Change the Opperating Mode of your HVAC Unit'
    class HSetTemp:
        name = 'HVAC Heat Set Temp'
        description = 'Change the Heat Set Temperature on your HVAC Unit'
    class CSetTemp:
        name = 'HVAC Cool Set Temp'
        description = 'Change the Cool Set Temperature on your HVAC Unit'
    class Alarm:
        name = 'Alarm Control'
        description = 'Arm or Disarm your Security System'

class Scene(eg.ActionBase):

    text = Text

    def __call__(self, scene=0):
        self.plugin.Scene(scene)


    def Configure(self, scene=0):

        text = self.text
        panel = eg.ConfigPanel()
        
        st1 = panel.SpinIntCtrl(scene, max=200)

        box1 = panel.BoxedGroup(
                            text.SceneBox,
                            (text.SceneText, st1)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(st1.GetValue())

class Dimmer(eg.ActionBase):

    text = Text

    def __call__(self, device=0, percent=0):
        self.plugin.Dimmer(device, percent)

    def Configure(self, device=0, percent=0):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.SpinIntCtrl(percent, max=100)
 
        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.DimmerBox,
                            (text.DeviceText, st1),
                            (text.PercentText, st2)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class Switch(eg.ActionBase):

    text = Text
    
    def __call__(self, device=0, state=0):
        self.plugin.Switch(device, state)
        

    def Configure(self, device=0, state=0):

        text = self.text

        panel = eg.ConfigPanel()
        choices = ['OFF', 'ON']

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.Choice(state, choices=choices)

        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.SwitchBox,
                            (text.DeviceText, st1),
                            (text.StateText, st2)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class Toggle(eg.ActionBase):

    text = Text
    
    def __call__(self, device=0):
        self.plugin.Toggle(device)

    def Configure(self, device=0):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.SpinIntCtrl(device, max=200)
        st1.SetStringSelection(device)

        box1 = panel.BoxedGroup(
                            text.ToggleBox,
                            (text.DeviceText, st1)
                            )

        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(st1.GetValue())

class FanMode(eg.ActionBase):

    text = Text

    def __call__(self, device=0, mode=1):
        self.plugin.FanMode(device, mode)

    def Configure(self, device=0, mode=1):

        text = self.text
        panel = eg.ConfigPanel()
        choices = ['ContinuousOn', 'Auto']

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.Choice(mode, choices=choices)


        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.FanModeBox,
                            (text.DeviceText, st1),
                            (text.FanModeText, st2)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class OppMode(eg.ActionBase):

    text = Text

    def __call__(self, device=0, mode=0):
        self.plugin.OppMode(device, mode)

    def Configure(self, device=0, mode=0):

        text = self.text
        panel = eg.ConfigPanel()
        choices = ['OFF', 'CoolOn', 'HeatOn', 'AutoChangeOver']
       
        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.Choice(mode, choices=choices)

        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.OppModeBox,
                            (text.DeviceText, st1),
                            (text.OppModeText, st2)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class HSetTemp(eg.ActionBase):

    text = Text

    def __call__(self, device=0, temp=70):
        self.plugin.HSetTemp(device, temp)

    def Configure(self, device=0, temp=70):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.SpinIntCtrl(temp, min=50, max=90)

        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.HSetTempBox,
                            (text.DeviceText, st1),
                            (text.TempText, st2)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                st1.GetValue(),
                st2.GetValue()
                )

class CSetTemp(eg.ActionBase):

    text = Text

    def __call__(self, device=0, temp=70):
        self.plugin.CSetTemp(device, temp)

    def Configure(self, device=0, temp=70):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.SpinIntCtrl(device, max=200)
        st2 = panel.SpinIntCtrl(temp, min=50, max=90)

        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup(
                            text.CSetTempBox,
                            (text.DeviceText, st1),
                            (text.TempText, st2)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue()
                            )

class Alarm(eg.ActionBase):

    text = Text

    def __call__(self, state=0):
        self.plugin.Alarm(state)

    def Configure(self, state=0):

        text = self.text
        panel = eg.ConfigPanel()
        choices = ['DISARM', 'ARM']

        st1 = panel.Choice(state, choices=choices)
                
        box1 = panel.BoxedGroup(
                            text.AlarmBox,
                            (text.AlarmText, st1)
                            )
       
        panel.sizer.Add(box1, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(st1.GetValue())

class Vera(eg.PluginBase):

    text=Text

    def __init__(self):

        self.AddEvents()
        self.AddAction(Switch)
        self.AddAction(Toggle)
        self.AddAction(Dimmer)
        self.AddAction(Scene)
        self.AddAction(FanMode)
        self.AddAction(OppMode)
        self.AddAction(HSetTemp)
        self.AddAction(CSetTemp)
        self.AddAction(Alarm)

        self.VERA_HTTP_API = VERA_HTTP_API()
        self.Server = Server()
        self.server = False
        self.prefix=None
        self.VDL = {}
        self.ADD = []
        self.ItemLog = []

    def Dimmer(self, device, percent):
        self.VERA_HTTP_API.send(SendType='Dimmer', device=str(device), percent=str(percent))

    def Toggle(self, device):
        self.VERA_HTTP_API.send(SendType='Toggle', device=str(device))

    def Scene(self, scene):
        self.VERA_HTTP_API.send(SendType='Scene', scene=str(scene))

    def Switch(self, device, state):
        self.VERA_HTTP_API.send(SendType='Switch', device=str(device), state=str(state))

    def FanMode(self, device, mode):
        choices = ['ContinuousOn', 'Auto']
        mode = choices[mode]

        self.VERA_HTTP_API.send(SendType='FanMode', device=str(device), mode=str(mode))

    def OppMode(self, device, mode):
        choices = ['OFF', 'CoolOn', 'HeatOn', 'AutoChangeOver']
        mode = choices[mode]

        self.VERA_HTTP_API.send(SendType='OppMode', device=str(device), mode=str(mode))

    def HSetTemp(self, device, temp):
        self.VERA_HTTP_API.send(SendType='HSetTemp', device=str(device), temp=str(temp))

    def CSetTemp(self, device, temp):
        self.VERA_HTTP_API.send(SendType='CSetTemp', device=str(device), temp=str(temp))

    def Alarm(self, state):
        self.VERA_HTTP_API.send(SendType='Alarm', state=str(state))

    def Configure(self, ip="127.0.0.1", port=3480, prefix='MiCasaVerdeVera'):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.TextCtrl(ip)
        st2 = panel.SpinIntCtrl(port, max=65535)
        st3 = panel.TextCtrl(prefix)
 
        eg.EqualizeWidths((st1, st2, st3))
                
        box1 = panel.BoxedGroup(
                            text.VeraBox,
                            (text.VeraIP, st1),
                            (text.VeraPort, st2)
                            )
        box2 = panel.BoxedGroup(
                            text.PrefixBox,
                            (text.Prefix,st3)
                            )

        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND)
            ])

        while panel.Affirmed():
            panel.SetResult(
                        st1.GetValue(),
                        st2.GetValue(),
                        st3.GetValue()
                        )

    def __start__(self, ip="127.0.0.1", port=3480, prefix='MiCasaVerdeVera'):

        self.lock = threading.Lock()
        self.info.eventPrefix = prefix
        self.prefix = prefix
        self.Startup = True
        self.server = self.Server.Start(ip=ip, port=port, plugin=self)
        self.VERA_HTTP_API.connect(ip=ip, port=port)

    def __stop__(self):

        if self.server:
            self.server = self.Server.Close(self.server)

    def SendEvent(self, DevID, EventItems, deviceItems):
        
        Event = self.VDL['Event'][DevID][0][0]
        Category = self.VDL['Event'][DevID][1]
        bPayload = self.VDL['Items'][DevID]

        for Item, Value in EventItems:
            payload = {'key1': self.prefix }
            if bPayload['room'] != '' and bPayload['room'] != None:
                payload['key2'] = bPayload['room']
            if bPayload['name'] != '' and bPayload['name'] != None:
                payload['key3'] = bPayload['name']
            payload['value'] = dc(deviceItems)

            self.TriggerEvent(
                            suffix=str(Event) \
                                    +'.'+str(Category) \
                                    +'.'+str(Item) \
                                    +'.'+str(Value),
                            payload=payload
                            )

    def UpdateDevices(self, vData):

        tmp = vData
        self.CFGDList = {}
        VDL = {'Counters':{}, 'Event':{}, 'NewItems': {}, 'Items': {}}
        if self.Startup: self.VDL = dc(VDL)

        mType =[['devices', 0],['scenes',1],['rooms',2],
                ['categories',3],['sections',4]]

        def BuildEvt(evtData, Type):
            ID = str(evtData['id'])
            midfix = [['room'], ['name'], ['category']]
            for i in range(3):
                S=False
                try: S = evtData[midfix[i][0]]
                except: S = 'None'
                if S == 'None' or None:
                    S = Type if i == 2 else ID if Type == 'device' and i == 1 else None
                midfix[i].append(S)
            return ID, midfix

        def NewItemScan(n, o):
            nItems = dc(n)
            oItems = dc(o)
            mKeys = []
            for nK, nV in nItems.iteritems():
                for oK, oV in oItems.iteritems():
                    if (nK == oK) and (nV == oV):
                        mKeys.append(nK)

            for dK in mKeys:
                del(nItems[dK])

            if nItems == {}: nItems = False
            return dc(nItems), dc(oItems)

        def NewItemsReporting(NI, NC, OI, OC):
            nItems, oItems = NewItemScan(NI, OI)
            nCounters, oCounters = NewItemScan(NC, OC)
            rItem = dc(nItems)
            rCount = NC if nCounters else dc(oCounters)
            noUp = False if nCounters or nItems else True
            
            if nCounters:
                eg.PrintNotice('MicasaVerde: OldCounters: '+str(oCounters))
                eg.PrintNotice('MicasaVerde: NewCounters: '+str(nCounters))

            if nItems:
                self.ItemLog.insert(0, [time.strftime("%c"), nItems])
                eg.PrintNotice('MicasaVerde: NewItems: '+str(nItems))

            return rItem, rCount

        def DeviceMerge(Type):
            typeList = {}
            typeList=dict(mType)
            if Type in typeList:
                Value=tmp[Type]
                for i in range(len(Value)):
                    oldData = dc(Value[i])
           
                    def Merge(Key, dataDict, Key2):
                        typeList={}
                        typeList=dict(mType[:2])
                        if Type in typeList:
                            for i in range(len(dataDict)):
                                mData = dc(dataDict[i])
                                if 'id' in mData:
                                    if mData['id'] == Key:
                                        return dc(mData[Key2])
                    typeList={}
                    typeList=dict(mType[:2])
                    if Type in typeList:
                        if 'room' in oldData:
                            roomName = Merge(oldData['room'], tmp['rooms'],'name')
                            oldData['roomID'] = oldData[str('room')]
                            oldData['room'] = str(roomName)

                    typeList={}
                    typeList=dict(mType[:1])
                    if Type in typeList:
                        if 'category' in oldData:
                            catName = Merge(oldData['category'], tmp['categories'],'name')
                            oldData['catID'] = oldData[str('category')]
                            oldData['category'] = str(catName)

                    typeList = {}
                    typeList=dict(mType)
                    if Type in typeList:
                        if 'id' in oldData:
                            if Type == 'devices' or Type == 'scenes':
                                ID, midfix = BuildEvt(oldData, Type)
                                VDL['Items'][ID] = dict(midfix)

                                for i in range(3): midfix[i] = midfix[i][1]
                                midfix = [['.'.join([midfix[0] ,midfix[1].replace(' Weather','')])] if midfix[0] != None else [midfix[1]], midfix[2]]
                                midfix[0][0] = midfix[0][0].replace(' ', '-').replace(':', '')

                                VDL['Event'][ID] = midfix
                            VDL['Counters'][Type] += 1
                            VDL[Type][str(oldData['id'])]=dc(oldData)

        for Type, idx in mType:
            VDL[Type] ={}
            VDL['Counters'][Type] = 0
            DeviceMerge(Type)
            del(tmp[Type])
            mType[idx][0] = str(idx)

        VDL['system']=dc(tmp)
        tmp = {}

        NI = dc(VDL['Items'])
        NC = dc(VDL['Counters'])
        OI = {}
        OC = {}

        if self.Startup:
            OI = {}
            OC = {}
        else:
            OI = dc(self.VDL['Items'])
            OC = dc(self.VDL['Counters'])
   
        NI, NC  = NewItemsReporting(NI, NC, OI, OC)

        VDL['NewItems'] = NI
        VDL['Counters'] = NC

        if not self.Startup:
            self.EventDetector(
                            dc(VDL['devices']),
                            dc(VDL['scenes']),
                            dc(self.VDL['devices']),
                            dc(self.VDL['scenes'])
                            )
        else: self.Startup = False

        self.VDL = dc(VDL)

    def EventDetector(self, newDevice, newScene, oldDevice, oldScene):

        def IterItem(new, old):
            IDCounter = [0, 0]
            ItemCounter = [0, 0]

            for newID, newItems in new.iteritems():
                IDCounter[0] += 1
                IDMatch = False
                ItemsMatch = False
                for oldID, oldItems in old.iteritems():
                    if newID == oldID:
                        IDCounter[1] += 1
                        if newItems != oldItems:
                            EventItems = []
                            for newItem, newValue in newItems.iteritems():
                                ItemCounter[0] += 1
                                for oldItem, oldValue in oldItems.iteritems():
                                    if newItem == oldItem:
                                        ItemCounter[1] += 1
                                        if newValue != oldValue:
                                            EventItems.append([newItem, newValue])
                            if EventItems != []:
                                self.SendEvent(newID, EventItems, newItems)

        IterItem(newDevice, oldDevice)
        IterItem(newScene, oldScene)

class Server():

    def __init__ (self):

        self.plugin = None
        self.VERA_HTTP_API = VERA_HTTP_API()
        self.DataThreadList = []
        self.ServerThread = None
        self.RunningUpdate=False
        return

    def Start(self, ip, port, plugin):

        self.plugin = plugin
        self.RunningUpdate = self.ConnectHTTPAPI(ip, port)
        if self.RunningUpdate:
           self.ServerThread = self.StartServerThread()
        return self.ServerThread

    def ConnectHTTPAPI(self, ip, port):

        self.VeraPort = port
        self.VeraIP = ip

        return self.VERA_HTTP_API.connect(ip=self.VeraIP, port=self.VeraPort)

    def StartServerThread(self):

        try:
            ServerThread = threading.Thread(name='Vera-Receive', target=self.RequestUpdate)
            ServerThread.start()   
        except:
            ServerThread = False
            PE("Server", "StartServerThread", sys.exc_info())
        finally:
            return ServerThread

    def RequestUpdate(self):
        while self.RunningUpdate:
            try:
                data = self.VERA_HTTP_API.send('ComRoomList')
                log("Server", 'RequestUpdate', repr(data))
                if data:
                    self.EvalData(data)
            except:
                PE("Server", "RequestUpdate", sys.exc_info())
            finally:
                time.sleep(0.1)

    def EvalData(self, data):
        eData = False
        log("Server", 'EvalData', repr(data))

        try:
            eData = dc(json.loads(data))
        except:
            err1=sys.exc_info()
            try:
                eData = eval(data)
            except:
                PE("Server", "EvalData", "Error 1", err1, "Error 2", sys.exc_info())
                eData = False
        finally:
            if eData:
                self.DataReadThread(eData)

    def DataReadThread(self, data):
        try:
            t =  threading.Thread(name='Vera-ProcessData', target=self.plugin.UpdateDevices, args=(data,))
            t.start()
            self.DataThreadList.append(t)
        except:
            PE("Server", "DataReadThread", sys.exc_info())
        return
        
    def Close(self, t):
        for i in range(len(self.DataThreadList)):
            self.DataThreadList.join()
            self.DataThread = False
        t.join()
        self.RunningUpdate = False
        self.ServerThread = False
        self.DataThreadList = []
        PN('Server', 'Server ShutDown')
        return t
 
class VERA_HTTP_API:

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 3480
        self.CONNECTED = False
        self.Startup = True
        return

    def connect(self, ip=None, port=None):
        self.CONNECTED = self.Startup
        self.ip = str(ip) if ip else self.ip
        self.port = port if port else self.port

        self.IPPort = str(self.ip)+":"+str(self.port)
        self.HostData = dc(URLS.DATA['HostData'])
        self.HostData[3][1] = self.IPPort
        self.HostData[3] = "".join(self.HostData[3])

        self.CONNECTED = PN("VERA_HTTP_API", "Connection Successful") if self.send('ComRoomList') \
                            else PE("VERA_HTTP_API", "Connection Failure", "IP", ip, "Port", port)

        return self.CONNECTED
    
    def send(self, SendType, device=False, percent=False, state=False, scene=False, temp=False, mode=False):
        Request=self.Startup
        self.Startup = False

        Request = PE("VERA_HTTP_API", "Connection Failure", "IP", self.ip, "Port", self.port) \
                    if not self.CONNECTED and not self.Startup else ''
        if Request == '':
            SendType = dc(URLS.DATA[SendType])
            for line in SendType:
                Request += line+str(device) if line[-11:] == '&DeviceNum=' \
                        else line

            Request += str(percent) if percent \
                        else str(state) if state \
                        else str(scene) if scene \
                        else str(temp) if temp \
                        else str(mode) if mode \
                        else ''
            Request += " HTTP/1.1"
            Request = [Request, "Host: "+self.IPPort]
            Request.extend(self.HostData)
            Request = "\r\n".join(Request)
            Request = self.SendData(Request)

        return Request

    def SendData(self, url):

        Response = ''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(5.0)
        sock.connect((self.ip, self.port))
        sock.settimeout(5.0)
        sock.sendall(url)
        answer = sock.recv(4096)
        while answer:
            Response += answer
            answer = sock.recv(4096)

        sock.close()

        try:
            if Response[:15] == "HTTP/1.1 200 OK":
                try:
                    Response = Response[39:]
                except:
                    log("VERA_HTTP_API", "SendData 1", sys.exc_info(), Response)
                    Response = False
            else:
                log("VERA_HTTP_API", "SendData 2", Response)
                Response = False
        except:
            log("VERA_HTTP_API", "SendData 3", sys.exc_info(), Response)
            Response = False
        return Response

class URLS:
        DATA = {
        'Dimmer'      : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:Dimming1&action=SetLoadLevelTarget&newLoadlevelTarget=" ],
        'Switch'      : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue="],
        'Toggle'      : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:micasaverde-com:serviceId:HaDevice1&action=ToggleState"],
        'Scene'       : ["GET /data_request?id=lu_action&serviceId=urn:micasaverde-com:","serviceId:HomeAutomationGateway1&action=RunScene&SceneNum="],
        'FanMode'     : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:HVAC_FanOperatingMode1&action=SetMode&NewMode="],                                                                                                                                                         
        'OppMode'     : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:HVAC_UserOperatingMode1&action=SetModeTarget&NewModeTarget="],                                                                                                                                        
        'CSetTemp'    : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Cool&action=SetCurrentSetpoint&NewCurrentSetpoint="], 
        'HSetTemp'    : ["GET /data_request?id=lu_action&DeviceNum=","&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Heat&action=SetCurrentSetpoint&NewCurrentSetpoint="],
        'Alarm'       : ["GET /data_request?id=action&output_format=xml&Category=4&serviceId=urn:micasaverde-com:","serviceId:SecuritySensor1&action=SetArmed&newArmedValue="],
        'AllVeraData' : ["GET /data_request?id=user_data","&output_format=json"],
        'DevStatus'   : ["GET /data_request?id=status","&output_format=json&DeviceNum="],                                                                                                      
        'AllDevStatus': ["GET /data_request?id=status","&output_format=json"],                                                                                                                          
        'ComRoomList' : ["GET /data_request?id=sdata","&output_format=json"],                                                                                                                         
        'SimRoomList' : ["GET /data_request?","id=invoke"],
        'JSON-XML'    : ["json, xml"],                                                                                     
        'LiveEnergy'  : ["GET /data_request?","id=live_energy_usage"],
        'HostData'    : ["User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
                         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                         "Accept-Encoding: gzip, deflate",
                         ["Referer: http://", "", "/data_request?id=sdata&output_format=xml"],
                         "",""]
        }

        