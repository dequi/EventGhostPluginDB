# -*- coding: utf-8 -*-
#
# plugins/MQTT Client/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright (C) 2013 Walter Kraembring <krambriw>.
#
###############################################################################
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# Revision history:
#
# 2014-11-29  Added option to select if event string and payload should be
#             linked together as combined event content
# 2014-07-31  Changed event prefix to 'MQTT'
#             Added support for utf-8 encoding/decoding
# 2014-04-30  Improved error message contents
# 2014-03-10  Added client connection retry handling
# 2014-01-12  Added timed dictionary to avoid duplicates
# 2013-10-20  The first stumbling version
##############################################################################
#
# Acknowledgement: All credits to Mr Roger Light <roger@atchoo.org> for the
# module mosquitto.py 
#
##############################################################################

eg.RegisterPlugin(
    name = "MQTT Client",
    author = "Walter Kraembring (krambriw)",
    version = "0.0.6_b1",
    canMultiLoad = False,
    kind = "other",
    url = "http://www.eventghost.org",
    description = ("Mosquitto is an open source (BSD licensed) message"+
                   "broker that implements the MQ Telemetry Transport"+
                   "protocol version 3.1. MQTT provides a lightweight"+
                   "method of carrying out messaging using a"+
                   "publish/subscribe model."
    ),
    guid = "{44A1C5BC-311A-4651-B4A6-629BEAC0A80B}"
)

import mosquitto
import time
from threading import Event, Thread



class Text:
    started = "Plugin started"
    listhl = "Currently active threads:"
    colLabels = (
        "MQTT Subscriber Name ",
        "MQTT broker host/ip  ",
        "Port                 ",
        "Topic                ",
        "                     "
    )
    
    #Buttons
    b_abort = "Abort"
    b_abortAll = "Abort all"
    b_restartAll = "Restart All"
    b_refresh = "Refresh"

    #Threads
    n_ThreadMQTT = "MQTT Client"
    thr_abort = "Thread is terminating: "
    connection_problem = 'MQTT Client: Trying to reconnect with...'
    connected = 'Succesfully connected with MQTT broker...'
    
    
class MQTTclientTxt:
    name = "Start a new MQTT subscription "
    description = ("A MQTT subscriber")
    actionName = "MQTT subscriber name: "
    hostName =   "Host ip or name: "
    portName =   "Port number:      "
    topicName =  "Topic: "
    tTopic = "Check to include payload in event string: "


class publishMQTTtxt:
    name = "Publish a MQTT message"
    description = ("A MQTT message")
    empty = '>>EMPTY<<'
    actionName =  "MQTT publisher name: "
    hostName =    "Host ip or name: "
    portName =    "Port number:      "
    topicName =   "Topic: "
    messageName = "Message: "
    qosName =     "QOS:                   "
    retainName =  "Retain:                "



class ThreadMQTT(Thread):
    text = Text

    def __init__(
        self,
        name,
        host,
        port,
        topic,
        topicTrigger
    ):
        Thread.__init__(self, name = self.text.n_ThreadMQTT)
        self.name = name
        self.host = host
        self.port = port
        self.topic = topic
        self.topicTrigger = topicTrigger
        self.finished = Event()
        self.abort = False
        self.eventCollection = []
        self.eventCollection = {}
        self.taskObj = {}
        self.bDelayRepeat = False
        self.delayRepeat = 1.0
        self.prefix = 'MQTT'


    def run(self):

        def RemoveEventFromCollection(t_key, res_key):
            try:
                del self.taskObj[t_key]
                self.eventCollection[res_key] = ''
            except:
                pass


        def TriggerEvent(msg):
            smsg = msg.topic.decode('utf-8')
            pl = str(msg.payload).decode('utf-8')
            if self.topicTrigger:
                smsg = smsg + '.' + pl
            eg.TriggerEvent(
                smsg,
                payload = pl,
                prefix=self.prefix
            )


        def on_connect(mosq, obj, rc):
            mosq.subscribe(self.topic, 0)
            #print("rc: "+str(rc))

        
        def on_message(mosq, obj, msg):
            #print self.eventCollection
            #print self.taskObj
           
            if str(msg.topic).find('zwave') > 0:
                event = str(msg.payload).split(',')
                res_base = str(msg.qos)+" "+str(msg.payload)
                res_key = msg.topic + ', ' + event[0]

                try:
                    v = self.eventCollection[res_key]
                except KeyError:
                    self.eventCollection[res_key] = ''        
        
                if self.eventCollection[res_key] != event:
                    self.eventCollection[res_key] = event
                    TriggerEvent(msg)
                    self.bDelayRepeat = True
                    self.delayRepeat = 10.0
                
                    if self.bDelayRepeat:
                        #Schedule the event removal task
                        t_key = str(time.time())
                        p = eg.scheduler.AddTask(
                            self.delayRepeat,
                            RemoveEventFromCollection,
                            t_key, res_key
                        )
                        self.taskObj[t_key] = str(p)
                return

            if str(msg.topic).find('rfxtrx') > 0:
                event = str(msg.payload).split('id: ')
                res_base = str(msg.payload)
                res_key = msg.topic + ', ' + event[1].split(',')[0]

                try:
                    v = self.eventCollection[res_key]
                except KeyError:
                    self.eventCollection[res_key] = ''        
        
                if self.eventCollection[res_key] != event:
                    self.eventCollection[res_key] = event
                    TriggerEvent(msg)
                    self.bDelayRepeat = True
                    self.delayRepeat = 1.0
    
                    if self.bDelayRepeat:
                        #Schedule the event removal task
                        t_key = str(time.time())
                        p = eg.scheduler.AddTask(
                            self.delayRepeat,
                            RemoveEventFromCollection,
                            t_key, res_key
                        )
                        self.taskObj[t_key] = str(p)
                return
            
            if str(msg.topic).find('nethomeserver') > 0:
                event = str(msg.payload).split(',')
                res_base = str(msg.qos)+" "+str(msg.payload)
                res_key = msg.topic + ', ' + event[0]

                try:
                    v = self.eventCollection[res_key]
                except KeyError:
                    self.eventCollection[res_key] = ''        
        
                if self.eventCollection[res_key] != event:
                    self.eventCollection[res_key] = event
                    TriggerEvent(msg)
                    self.bDelayRepeat = True
                    self.delayRepeat = 1.0
                
                    if self.bDelayRepeat:
                        #Schedule the event removal task
                        t_key = str(time.time())
                        p = eg.scheduler.AddTask(
                            self.delayRepeat,
                            RemoveEventFromCollection,
                            t_key, res_key
                        )
                        self.taskObj[t_key] = str(p)
                return

            if str(msg.topic).find(self.topic.split('/')[1]) > 0:
                event = str(msg.payload).split(',')
                res_base = str(msg.qos)+" "+str(msg.payload)
                res_key = msg.topic + ', ' + event[0]

                try:
                    v = self.eventCollection[res_key]
                except KeyError:
                    self.eventCollection[res_key] = ''        
        
                if self.eventCollection[res_key] != event:
                    self.eventCollection[res_key] = event
                    TriggerEvent(msg)
                    self.bDelayRepeat = True
                    self.delayRepeat = 5.0
                
                    if self.bDelayRepeat:
                        #Schedule the event removal task
                        t_key = str(time.time())
                        p = eg.scheduler.AddTask(
                            self.delayRepeat,
                            RemoveEventFromCollection,
                            t_key, res_key
                        )
                        self.taskObj[t_key] = str(p)
                return

       
        def on_subscribe(mosq, obj, mid, granted_qos):
            print("Subscribed: "+str(mid)+" "+str(granted_qos))
        

        def on_log(mosq, obj, level, string):
            print(string)
        
        
        mqttc = mosquitto.Mosquitto()
        mqttc.on_message = on_message
        mqttc.on_connect = on_connect
        mqttc.on_subscribe = on_subscribe
        #mqttc.on_log = on_log
        resp = None
        
        while resp <> 0 and self.abort == False:
            lrsp = 0
            resp = mqttc.connect(self.host, self.port, 30, "")
            if resp <> 0:
                print self.text.connection_problem +self.topic +' ' +self.host
            else:
                print 'MQTT Client ', self.name +':', self.text.connected
            while lrsp == 0 and self.abort == False:
                lrsp = mqttc.loop(10.0, 1)
                #print 'lrsp', lrsp
                self.finished.wait(0.01)
                #self.finished.clear()
                if lrsp <> 0:
                    resp = -1
                    mqttc.disconnect()
                if self.abort:
                    mqttc.disconnect()
                    self.finished.wait(1.0)
                    break
            self.finished.wait(10.0)
            self.finished.clear()


    def CancelTasks(self):
        for key in self.taskObj:
            try:
                eg.scheduler.CancelTask(key)
            except ValueError:
                pass
        self.taskObj = {}
        

    def AbortMQTT(self):
        print self.text.thr_abort, self.text.n_ThreadMQTT
        self.abort = True
        self.finished.set()
        time.sleep(0.1)
        self.CancelTasks()


               
class MQTTthreads(eg.PluginClass):
    text = Text
        
    def __init__(self):
        self.AddAction(MQTTclient)
        self.AddAction(publishMQTT)
        self.AllMQTTsubscribers = []
        self.lastMQTTName = ""
        self.MQTTThreads = {}
        self.OkButtonClicked = False
        self.started = False


    def __start__(
        self
    ):
        print self.text.started

        if self.OkButtonClicked:
            self.OkButtonClicked = False
            self.RestartAllMQTTs()

        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()
        self.started = True


    def __stop__(self):
        self.mainThreadEvent.set()
        self.AbortAllMQTTs()
        self.started = False


    def __close__(self):
        self.AbortAllMQTTs()
        self.started = False


    def main(self,mainThreadEvent):
        while not mainThreadEvent.isSet():
            self.mainThreadEvent.wait(10.0)
            #print "Main thread is running..."


    #methods to Control MQTTs
    def StartMQTTs(
        self,
        MQTTName,
        host,
        port,
        topic,
        topicTrigger
    ):
        if self.MQTTThreads.has_key(MQTTName):
            t = self.MQTTThreads[MQTTName]
            if t.isAlive():
                t.AbortMQTT()
            del self.MQTTThreads[MQTTName]
        t = ThreadMQTT(
            MQTTName,
            host,
            port,
            topic,
            topicTrigger
        )
        self.MQTTThreads[MQTTName] = t
        t.start()


    def AbortMQTT(self, MQTT):
        if self.MQTTThreads.has_key(MQTT):
            t = self.MQTTThreads[MQTT]
            t.AbortMQTT()
            del self.MQTTThreads[MQTT]


    def AbortAllMQTTs(self):
        for i, item in enumerate(self.MQTTThreads):
            t = self.MQTTThreads[item]
            t.AbortMQTT()
            del t
        self.MQTTThreads = {}


    def RestartAllMQTTs(self, startNewIfNotAlive = True):
        for item in self.GetAllMQTTsubscribers():
            item = item.split(',')
            if startNewIfNotAlive:
                bT = True
                if item[4] == 'False':
                    bT = False
                self.StartMQTTs(
                    item[0],
                    item[1],
                    int(item[2]),
                    item[3],
                    bT
                )


    def Configure(
        self,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)

        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.listhl),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        mySizer = wx.GridBagSizer(5, 5)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)
        mySizer.AddGrowableCol(4)
      
        testListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL
        )
       
        for i, colLabel in enumerate(self.text.colLabels):
            testListCtrl.InsertColumn(i, colLabel)

        #setting col width to fit label
        testListCtrl.InsertStringItem(0, "Test Subscriber Name               ")
        testListCtrl.SetStringItem(0, 1, "                                   ")
        testListCtrl.SetStringItem(0, 2, "           ")
        testListCtrl.SetStringItem(0, 3, "                                   ")
        testListCtrl.SetStringItem(0, 4, "                                   ")

        size = 0
        for i in range(4):
            testListCtrl.SetColumnWidth(
                i,
                wx.LIST_AUTOSIZE_USEHEADER
            ) #wx.LIST_AUTOSIZE
            size += testListCtrl.GetColumnWidth(i)
       
        testListCtrl.SetMinSize((size, -1))
        
        mySizer.Add(testListCtrl, (0,0), (1, 5), flag = wx.EXPAND)

        #buttons
        abortButton = wx.Button(panel, -1, self.text.b_abort)
        mySizer.Add(abortButton, (3,0))
       
        abortAllButton = wx.Button(panel, -1, self.text.b_abortAll)
        mySizer.Add(abortAllButton, (3,1), flag = wx.ALIGN_RIGHT)
       
        restartAllButton = wx.Button(panel, -1, self.text.b_restartAll)
        mySizer.Add(restartAllButton, (3,2), flag = wx.ALIGN_RIGHT)

        refreshButton = wx.Button(panel, -1, self.text.b_refresh)
        mySizer.Add(refreshButton, (3,4), flag = wx.ALIGN_RIGHT)
       
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

       
        def PopulateList (event):
            testListCtrl.DeleteAllItems()
            row = 0
            for i, item in enumerate(self.MQTTThreads):
                t = self.MQTTThreads[item]
                if t.isAlive():
                    testListCtrl.InsertStringItem(
                        row,
                        t.name
                    )
                    testListCtrl.SetStringItem(row,
                        1, t.host)
                    testListCtrl.SetStringItem(row,
                        2, str(t.port))
                    testListCtrl.SetStringItem(row,
                        3, t.topic)
                    row += 1
            ListSelection(wx.CommandEvent())


        def OnAbortButton(event):
            item = testListCtrl.GetFirstSelected()
            while item != -1:
                name = testListCtrl.GetItemText(item)
                self.AbortMQTT(name)
                item = testListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnAbortAllButton(event):
            self.AbortAllMQTTs()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnRestartAllButton(event):
            self.RestartAllMQTTs()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def ListSelection(event):
            flag = testListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            event.Skip()

           
        def OnSize(event):
            testListCtrl.SetColumnWidth(
                6,
                wx.LIST_AUTOSIZE_USEHEADER
            ) #wx.LIST_AUTOSIZE
            event.Skip()


        def OnApplyButton(event): 
            event.Skip()
            self.RestartAllMQTTs()
            PopulateList(wx.CommandEvent())


        def OnOkButton(event): 
            event.Skip()
            self.OkButtonClicked = True
            if not self.started:    
                self.RestartAllMQTTs()
            PopulateList(wx.CommandEvent())
         

        PopulateList(wx.CommandEvent())
        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        restartAllButton.Bind(wx.EVT_BUTTON, OnRestartAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        testListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        testListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyButton)
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnOkButton)

        while panel.Affirmed():
            panel.SetResult(
                        *args
            )


    def GetAllMQTTsubscribers(self):
        return self.AllMQTTsubscribers


    def AddMQTTsubscriber(self, name, host, port, topic, topicTrigger):
        sub = name+','+host+','+str(port)+','+topic+','+str(topicTrigger)
        if not sub in self.AllMQTTsubscribers:
            self.AllMQTTsubscribers.append(sub)
        return self.AllMQTTsubscribers.index(sub)



class MQTTclient(eg.ActionClass):
    text = MQTTclientTxt
    
    def __call__(
        self,
        name,
        host,
        port,
        topic,
        topicTrigger
    ):
        self.plugin.StartMQTTs(
            name,
            host,
            port,
            topic,
            topicTrigger
        )


    def GetLabel(
        self,
        name,
        host,
        port,
        topic,
        topicTrigger
    ):
        self.plugin.AddMQTTsubscriber(name, host, port, topic, topicTrigger)
        print self.text.labelStart % (name)
        return self.text.labelStart % (name)


    def Configure(
        self,
        name="Give this MQTT subscriber a name",
        host="test.mosquitto.org",
        port=1883,
        topic="/eventghost/#",
        topicTrigger=False
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)
        mySizer_3 = wx.GridBagSizer(10, 10)
        mySizer_4 = wx.GridBagSizer(10, 10)
        mySizer_5 = wx.GridBagSizer(10, 10)

        #name
        nameCtrl = wx.TextCtrl(panel, -1, name)
        nameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.actionName), (0,0))
        mySizer_1.Add(nameCtrl, (1,0))

        #host
        hostCtrl = wx.TextCtrl(panel, -1, host)
        hostCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.hostName), (1,0))
        mySizer_2.Add(hostCtrl, (1,1))

        #port
        portCtrl = panel.SpinIntCtrl(port)
        portCtrl.SetInitialSize((50,-1))
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.portName), (1,0))
        mySizer_3.Add(portCtrl, (1,1))

        #topic
        topicCtrl = wx.TextCtrl(panel, -1, topic)
        topicCtrl.SetInitialSize((250,-1))
        mySizer_4.Add(wx.StaticText(panel, -1, self.text.topicName), (1,0))
        mySizer_4.Add(topicCtrl, (2,0))

        #topic Trigger
        tTopicCtrl = wx.CheckBox(panel, -1, "")
        tTopicCtrl.SetValue(topicTrigger)
        mySizer_5.Add(wx.StaticText(panel, -1, self.text.tTopic), (1,0))
        mySizer_5.Add(tTopicCtrl, (2,0))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_4, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_5, 0, flag = wx.EXPAND)


        def OnButton(event): 
            # re-assign the OK button
            event.Skip()
            name = nameCtrl.GetValue()
            host = hostCtrl.GetValue()
            port = portCtrl.GetValue()
            topic = topicCtrl.GetValue()
            topicTrigger = tTopicCtrl.GetValue()
            plugin.lastMQTTName = name
            plugin.AddMQTTsubscriber(name, host, port, topic, topicTrigger)
            self.plugin.RestartAllMQTTs()

        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            name = nameCtrl.GetValue()
            host = hostCtrl.GetValue()
            port = portCtrl.GetValue()
            topic = topicCtrl.GetValue()
            topicTrigger = tTopicCtrl.GetValue()
            plugin.lastMQTTName = name
            plugin.AddMQTTsubscriber(name, host, port, topic, topicTrigger)
            panel.SetResult(
                name,
                host,
                port,
                topic,
                topicTrigger
            )



class publishMQTT(eg.ActionClass):
    text = publishMQTTtxt
    
    def on_connect(self, mosq, obj, rc):
        mosq.subscribe(self.topic, self.qos)
        #print("rc: "+str(rc))


    def on_publish(self, mosq, obj, mid):
        pass
        #print("mid: "+str(mid))

    
    def __call__(
        self,
        name,
        host,
        port,
        topic,
        message,
        qos,
        retain
    ):
        self.name = name
        self.host = host
        self.port = port
        self.topic = topic
        self.message = str(
            (eg.ParseString(message) if message else text.empty).encode("utf-8")
        )
        self.qos = qos
        self.retain = retain
        mqttc = mosquitto.Mosquitto()
        mqttc.on_connect = self.on_connect
        mqttc.on_publish = self.on_publish
        mqttc.connect(
            self.host,
            self.port,
            60,
            ""
        )
        pb = mqttc.publish(
                self.topic,
                self.message,
                self.qos,
                self.retain
            )
        time.sleep(0.05) 
        mqttc.disconnect()

             
    def Configure(
        self,
        name="Give this MQTT message a name",
        host="test.mosquitto.org",
        port=1883,
        topic="/eventghost/performedaction",
        message=u"{eg.event.string}",
        qos=0,
        retain=False
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)
        mySizer_3 = wx.GridBagSizer(10, 10)
        mySizer_4 = wx.GridBagSizer(10, 10)
        mySizer_5 = wx.GridBagSizer(10, 10)
        mySizer_6 = wx.GridBagSizer(10, 10)
        mySizer_7 = wx.GridBagSizer(10, 10)

        #name
        nameCtrl = wx.TextCtrl(panel, -1, name)
        nameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.actionName), (0,0))
        mySizer_1.Add(nameCtrl, (1,0))

        #host
        hostCtrl = wx.TextCtrl(panel, -1, host)
        hostCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.hostName), (1,0))
        mySizer_2.Add(hostCtrl, (1,1))

        #port
        portCtrl = panel.SpinIntCtrl(port)
        portCtrl.SetInitialSize((50,-1))
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.portName), (1,0))
        mySizer_3.Add(portCtrl, (1,1))

        #topic
        topicCtrl = wx.TextCtrl(panel, -1, topic)
        topicCtrl.SetInitialSize((250,-1))
        mySizer_4.Add(wx.StaticText(panel, -1, self.text.topicName), (1,0))
        mySizer_4.Add(topicCtrl, (2,0))

        #message
        messageCtrl = wx.TextCtrl(panel, -1, message)
        messageCtrl.SetInitialSize((250,-1))
        mySizer_5.Add(wx.StaticText(panel, -1, self.text.messageName), (1,0))
        mySizer_5.Add(messageCtrl, (2,0))

        #qos
        qosCtrl = panel.SpinIntCtrl(qos, min=0, max=2)
        qosCtrl.SetInitialSize((50,-1))
        mySizer_6.Add(wx.StaticText(panel, -1, self.text.qosName), (1,0))
        mySizer_6.Add(qosCtrl, (1,1))

        #retain
        retainCtrl = wx.CheckBox(panel, -1, '')               
        retainCtrl.SetValue(retain)
        retainCtrl.SetInitialSize((50,-1))
        mySizer_7.Add(wx.StaticText(panel, -1, self.text.retainName), (1,0))
        mySizer_7.Add(retainCtrl, (1,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_4, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_5, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_6, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_7, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            name = nameCtrl.GetValue()
            host = hostCtrl.GetValue()
            port = portCtrl.GetValue()
            topic = topicCtrl.GetValue()
            message = messageCtrl.GetValue()
            qos = qosCtrl.GetValue()
            retain = retainCtrl.GetValue()
            panel.SetResult(
                name,
                host,
                port,
                topic,
                message,
                qos,
                retain
            )

