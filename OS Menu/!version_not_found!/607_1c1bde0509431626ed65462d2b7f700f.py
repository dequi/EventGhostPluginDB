version="0.1.1" 
# plugins/OSM/__init__.py
#
# Copyright (C)  2008 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
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

eg.RegisterPlugin(
    name = "OS Menu",
    author = "Pako",
    version = version,
    kind = "other",
    description = (
        'Allows you to create custom On Screen Menu.'
    ),
    createMacrosOnAdd = True,    
    url = "http://www.eventghost.org/xxxxx",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABoAAAAaCAMAAACelLz8AAADAFBMVEX/////9/f/goL/"
        "z8//x8f//v7/2dn/Kir/gID/c3P/5ub/vb3/TU3/QED/ysr/oqL/7Oz/3t7/rq7/hob/"
        "t7f/qKj/k5P/a2v/hYX/d3f/T0//WVn/NDT/7u7/MTH/vLz/MzP/+fn/0ND/ZGT/tbX/"
        "nJz/LS3/UlL/l5f/wsL/mZn/Skr/8PD/Vlb/qqr/pqb/fn7/wMD/ior/YmL/4uL/kZH/"
        "enr/0dH/b2//Rkb/4OD/aGj/6ur/6Oj/MDD/Pz//Pj7/Ly//Nzf/5OT/cXH/QkL/yMj/"
        "srL/W1v/1dX/rKz/iYn/29v/dnb/ubn/PDz/j4//np7/dHT/e3v/qan/09P/o6P/r6//"
        "ZWX/19f/ODj/Q0P/8fEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABoAABoAAFAY"
        "AAEaAAAAACgAABoAABoYAAEAAAAACCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAPAAASf/////9/fP/4LHx////v4q/9mAgP//c3O9/+ZNTf//QECi/8rs7P//3t6G"
        "/663t///qKhr/5OFhf//d3dZ/080NP//7u68/zEzM///+flk/9C1tf//nJxS/y2Xl///"
        "wsJK/5nw8P//Vlam/6p+fv//wMBi/4ri4v//kZHR/3pvb///RkZo/+Dq6v//6Og//zA+"
        "Pv//Ly/k/zdxcf//QkKy/8hbW///1dWJ/6zb2///dnY8/7mPj///np57/3Spqf//09Ov"
        "/6NlZf//19dD/zjx8f8AAAAABWgAABfHxtwAEQTHyQAAAGjHzBjHzBgAAFxuZVJpcmUu"
        "LmcAABwAAENCblQAAABBmj0AAAAAAAAAAAAAAAAAAAABAAFCadPG/kwAAADabVLsAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAThJREFUeNp9kudWAjEQRkcQ"
        "BxSkWSgKVlAXBFQUVBTF3ju2938O55sJ7i/NOZvcL3fPTrIJ0b9tKIAWtDCsIeTUCKOF"
        "LUQ0jDo1pilqIaZh3Km4Jk6Ak8Ypp9IWJ8CTxlNOTVvM+KU461TOYs4vxXmnZizy7G8p"
        "jplJgAvyFK3UHPK8qgXgojxpKwXkpKol4HKJuaylCivIq6rWgEWPuVRBqeo6ck1VHRjM"
        "StfAbEZ/zoaqTeAWZpvb2PkOcktVW1e0K91eVLr9DnIZJnQgdEjUZe4eMXs2cQzVw0tV"
        "ohPbbJ3oFGNF1Jn7dM3UOdEFxktRV4BrohtTHaJbjHeimoC4wD2gLfAAeBR4GrzTAjwL"
        "vAACAnnAq8AboC/QALyTLtoO/wPQG1wjT26aHonu/ZP5C+O3P/VH+wFJCR8UaaZiYgAA"
        "AABJRU5ErkJggg=="
    )
)

import os
from win32com.client.dynamic import Dispatch
from win32api import GetSystemMetrics
from win32gui import SetFocus, SetForegroundWindow, SetActiveWindow
from eg.WinApi import SendMessageTimeout
from eg.WinApi.Dynamic import PostMessage

WM_CLOSE      = 16
WM_SYSCOMMAND = 274
SC_MINIMIZE   = 61472
WM_KEYDOWN    = 0x0100
WM_KEYUP      = 0x0101
VK_RETURN     = 0x0D


def ExtractFromList(list,index):
    tmp=[]
    for item in list:
        tmp.append(item[index])
    return tmp

#====================================================================
#cls types for ACTIONS list :
#====================================================================
class ShowMenu(eg.ActionClass):
    panel = None
    
    class text:
        label = 'Label:'
        evtString = 'Event:'
        menuPreview = 'On screen menu preview:'
        delete = 'Delete'
        insert = 'Insert new'
        menuFont = 'Menu font:'
        txtColour = 'Text colour'
        background = 'Background colour'        
        
#====================================================================
    class MenuColourSelectButton(wx.BitmapButton):

        def __init__(
            self, 
            id = -1,
            value=(255, 255, 255),
            name="ColourSelectButton",
            pos=wx.DefaultPosition, 
            size=(40, wx.Button.GetDefaultSize()[1]),
            style=wx.BU_AUTODRAW, 
            validator=wx.DefaultValidator, 
        ):
            self.id = id
            self.value = value
            self.name = name
            wx.BitmapButton.__init__(
                self, panel, id, wx.NullBitmap, pos, size, style, validator, name
            )
            self.SetValue(value)
            self.Bind(wx.EVT_BUTTON, self.OnButton)


        def OnButton(self, event):
            colourData = wx.ColourData()
            colourData.SetChooseFull(True)
            colourData.SetColour(self.value)
            for n, colour in enumerate(eg.config.colourPickerCustomColours):
                colourData.SetCustomColour(n, colour)
            colourDlg = wx.ColourDialog(self.GetParent(), colourData)
            colourDlg.SetTitle(self.name)
            if colourDlg.ShowModal() == wx.ID_OK:
                colourData = colourDlg.GetColourData()
                colour=colourData.GetColour().Get()
                self.SetValue(colour)
                listBoxCtrl = event.GetEventObject().GetParent().GetSizer().\
                    GetChildren()[0].GetSizer().GetChildren()[1].GetSizer().\
                    GetChildren()[1].GetWindow()                
                btnId = event.GetId()
                if btnId == 1:
                    listBoxCtrl.SetBackgroundColour(colour)
                    listBoxCtrl.Refresh()
                else:
                    listBoxCtrl.SetForegroundColour(colour)
                    listBoxCtrl.Refresh()
                event.Skip()
            eg.config.colourPickerCustomColours = [
                colourData.GetCustomColour(n).Get() for n in range(16)
            ]
            colourDlg.Destroy()

            
        def GetValue(self):
            return self.value

            
        def SetValue(self, value):
            self.value = value
            w, h = self.GetSize()
            image = wx.EmptyImage(w-10, h-10)
            image.SetRGBRect((1, 1, w-12, h-12), *value)
            self.SetBitmapLabel(image.ConvertToBitmap())
#====================================================================
    class MenuFontButton(wx.BitmapButton):

        def __init__(
            self, 
            fontInfo = None,
            id=-1,
            pos=wx.DefaultPosition, 
            size=(40, wx.Button.GetDefaultSize()[1]),
            style=wx.BU_AUTODRAW, 
            validator=wx.DefaultValidator,
            name="MenuFontButton", 
        ):
            self.window = panel
            self.fontInfo = fontInfo
            wx.BitmapButton.__init__(
                self,
                panel,
                id,
                wx.Bitmap("images/font.png"), 
                pos,
                size,
                style,
                validator,
                name
            )
            self.Bind(wx.EVT_BUTTON, self.OnButton)


        def OnButton(self, event):
            data = wx.FontData()
            if self.fontInfo is not None:
                font = wx.FontFromNativeInfoString(self.fontInfo)
                data.SetInitialFont(font)
            else:
                data.SetInitialFont(
                    wx.SystemSettings_GetFont(wx.SYS_ANSI_VAR_FONT )
                )
            dlg = wx.FontDialog(self.window, data)
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetFontData()
                font = data.GetChosenFont()
                listBoxCtrl =  self.window.GetSizer().GetChildren()[0].\
                    GetSizer().GetChildren()[1].GetSizer().GetChildren()[1].\
                    GetWindow()
                for n in range(10,20):
                    font.SetPointSize(n)
                    listBoxCtrl.SetFont(font)
                    if listBoxCtrl.GetTextExtent('X')[1]>20:
                        break
                self.fontInfo = data.GetChosenFont().GetNativeFontInfo().\
                    ToString()
                event.Skip()
            dlg.Destroy()


        def GetValue(self):
            return self.fontInfo


        def SetValue(self, fontInfo):
            self.fontInfo = fontInfo

            
    def Move(self,index,direction):
        tmpList=self.choices[:]
        max = len(self.choices)-1
        #Last to first position, other down
        if index == max and direction == 1:
            tmpList[1:] = self.choices[:-1]
            tmpList[0] = self.choices[max]
            index2 = 0
        #First to last position, other up
        elif index == 0 and direction == -1:
            tmpList[:-1] = self.choices[1:]
            tmpList[max] = self.choices[0]
            index2 = max
        else:
            index2 = index+direction
            tmpList[index] = self.choices[index2]
            tmpList[index2] = self.choices[index]
        self.choices=tmpList
        return index2


    def __call__(
        self,
        choices=[],
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None
        #bold = False
    ):
        # transferred to Plugin Class ;; Luigi
	self.plugin.ShowMenu (choices,fore,back,fontInfo)
       

    def GetLabel(
        self,
        choices,
        fore,
        back,
        fontInfo,
    #    bold
    ):
        res=self.text.showMenu+' '
        for n in range(0,min(3,len(choices))):
            res=res+choices[n][0]+', '
        res = res[:-2]
        if len(choices) > 3:
            res += ', ...'
        return res


    def Configure(
        self,
        choices=[],
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None
    #    bold = False
    ):
        self.choices = choices[:]
        self.fore = fore
        self.back = back
        self.oldSel=0
        global panel
        panel = eg.ConfigPanel(self)
        w1 = panel.GetTextExtent(self.text.label)[0]
        w2 = panel.GetTextExtent(self.text.evtString)[0]
        w = max((w1,w2))
        mainSizer=wx.BoxSizer(wx.VERTICAL)
        topSizer=wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer=wx.FlexGridSizer(2,2,hgap=5,vgap=5)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        topRightSizer=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        previewLblSizer = wx.BoxSizer(wx.HORIZONTAL)
        previewLblSizer.Add((w+5,1))
        previewLblSizer.Add(previewLbl)
        mainSizer.Add(previewLblSizer)
        mainSizer.Add(topSizer,0,wx.TOP,5)
        mainSizer.Add(bottomSizer,0,wx.TOP,16)
        panel.sizer.Add(mainSizer)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(160,120),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB 
        )
        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        if fontInfo is None:
            font = listBoxCtrl.GetFont()
            fontInfo = listBoxCtrl.GetFont()
            fontInfo.SetPointSize(36)
            fontInfo = fontInfo.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            listBoxCtrl.SetFont(font)
            if listBoxCtrl.GetTextExtent('X')[1]>20:
                break
        topSizer.Add((w+5,1))
        topSizer.Add(listBoxCtrl)
        topSizer.Add((10,1))
        topSizer.Add(topMiddleSizer)
        topSizer.Add((50,1))
        topSizer.Add(topRightSizer)
        labelLbl=wx.StaticText(panel, -1, self.text.label)
        labelCtrl=wx.TextCtrl(panel,-1,'',size=wx.Size(160,-1))
        bottomSizer.Add(labelLbl,0,wx.TOP,3)
        labelCtrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelCtrlSizer.Add(labelCtrl,0,wx.EXPAND)
        bottomSizer.Add(labelCtrlSizer)
        eventLbl=wx.StaticText(panel, -1, self.text.evtString)
        eventCtrl = wx.TextCtrl(panel,-1,'',size=wx.Size(160,-1))
        bottomSizer.Add(eventLbl,0,wx.TOP,3)
        bottomSizer.Add(eventCtrl,0,wx.EXPAND)
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(panel, -1, bmp)
        btnUP.Enable(False)
        topMiddleSizer.Add(btnUP)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(panel, -1, bmp)
        btnDOWN.Enable(False)
        topMiddleSizer.Add(btnDOWN,0,wx.TOP,3)
        #Buttons 'Delete' and 'Insert new'
        w1 = panel.GetTextExtent(self.text.delete)[0]
        w2 = panel.GetTextExtent(self.text.insert)[0]
        if w1 > w2:
            btnDEL=wx.Button(panel,-1,self.text.delete)
            btnApp=wx.Button(panel,-1,self.text.insert,size=btnDEL.GetSize())
        else:
            btnApp=wx.Button(panel,-1,self.text.insert)
            btnDEL=wx.Button(panel,-1,self.text.delete,size=btnApp.GetSize())
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = self.MenuFontButton(fontInfo)
        topRightSizer.Add(fontLbl,0,wx.TOP,-15)
        topRightSizer.Add(fontButton,0,wx.TOP,2)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = self.MenuColourSelectButton(
            0,
            fore,
            self.text.txtColour
        )
        topRightSizer.Add(foreLbl,0,wx.TOP,10)
        topRightSizer.Add(foreColourButton,0,wx.TOP,2)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = self.MenuColourSelectButton(
            1,
            back,
            self.text.background
        )
        topRightSizer.Add(backLbl,0,wx.TOP,10)
        topRightSizer.Add(backColourButton,0,wx.TOP,2)
        #Check box Bold font
    #    boldChkBoxCtrl = wx.CheckBox(panel, label='Bold font')
    #    boldChkBoxCtrl.SetValue(bold)
    #    topRightSizer.Add(boldChkBoxCtrl,0,wx.TOP,15)
        
    #    def OnBoldSwitch(evt):
    #        font = listBoxCtrl.GetFont()
    #        if boldChkBoxCtrl.GetValue():
    #            font.SetWeight(wx.BOLD)
    #        else:
    #            font.SetWeight(wx.NORMAL)
    #        listBoxCtrl.SetFont(font)
    #        labelCtrl.SetFont(font)
    #        evt.Skip()
    #    boldChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnBoldSwitch)


        def OnClick(evt):
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            event = eventCtrl.GetValue()
            if label.strip()<>"":
                if ExtractFromList(self.choices,0).count(label)==1:
                    self.oldSel=sel
                    item = self.choices[sel]
                    labelCtrl.SetValue(item[0])
                    eventCtrl.SetValue(item[1])
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, OnClick)


        def OnButtonUp(evt):
            newSel=self.Move(listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set(ExtractFromList(self.choices,0))
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, OnButtonUp)


        def OnButtonDown(evt):
            newSel=self.Move(listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set(ExtractFromList(self.choices,0))
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, OnButtonDown)


        def OnButtonDelete(evt):
            lngth=len(self.choices)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.choices=[]
                listBoxCtrl.Set([])
                labelCtrl.SetValue('')
                eventCtrl.SetValue('')
                labelCtrl.Enable(False)
                labelLbl.Enable(False)
                eventCtrl.Enable(False)
                eventLbl.Enable(False)
                panel.EnableButtons(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = self.choices.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set(ExtractFromList(self.choices,0))
            listBoxCtrl.SetSelection(sel)
            item = self.choices[sel]
            labelCtrl.SetValue(item[0])
            eventCtrl.SetValue(item[1])
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, OnButtonDelete)
        if len(self.choices) > 0:
            listBoxCtrl.Set(ExtractFromList(self.choices,0))
            listBoxCtrl.SetSelection(0)
            labelCtrl.SetValue(self.choices[0][0])
            eventCtrl.SetValue(self.choices[0][1])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            labelCtrl.Enable(False)
            labelLbl.Enable(False)
            eventCtrl.Enable(False)
            eventLbl.Enable(False)
            panel.EnableButtons(False)
        panel.sizer.Layout()


        def OnTextChange(evt):
            if self.choices<>[]:
                flag = False
                sel = self.oldSel
                label = labelCtrl.GetValue()
                event = eventCtrl.GetValue()
                self.choices[sel]=(label,event)
                listBoxCtrl.Set(ExtractFromList(self.choices,0))
                listBoxCtrl.SetSelection(sel)
                if label.strip()<>"":
                    if event.strip()<>"":
                        if ExtractFromList(self.choices,0).count(label)==1:
                            flag = True
                panel.EnableButtons(flag)
                btnApp.Enable(flag)
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        eventCtrl.Bind(wx.EVT_TEXT, OnTextChange)


        def OnButtonAppend(evt):
            if len(self.choices)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            labelCtrl.Enable(True)
            labelLbl.Enable(True)
            eventCtrl.Enable(True)
            eventLbl.Enable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            self.choices.insert(sel,('',''))
            listBoxCtrl.Set(ExtractFromList(self.choices,0))
            listBoxCtrl.SetSelection(sel)
            labelCtrl.SetValue('')
            labelCtrl.SetFocus()
            eventCtrl.SetValue('')
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)
   
            
    #    if bold:
    #        font.SetWeight(wx.BOLD)
    #        listBoxCtrl.SetFont(font)
    #        labelCtrl.SetFont(font)

        while panel.Affirmed():
            panel.SetResult(
            self.choices,
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontButton.GetValue(), 

    #        boldChkBoxCtrl.GetValue(),
        )

#====================================================================
class MoveCursor(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            max=len(self.plugin.choices)
            if max > 0:
                sel=self.plugin.menuDlg.GetSizer().GetChildren()[0].\
                    GetWindow().GetSelection()
                if sel == eval(self.value[0]):
                    sel = eval(self.value[1])
                self.plugin.menuDlg.GetSizer().GetChildren()[0].GetWindow().\
                    SetSelection(sel+self.value[2])
                

        
#====================================================================
class Cancel_Btn(eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            self.plugin.menuDlg.Destroy()
            self.plugin.menuDlg = None
            self.plugin.choices = []

#====================================================================

# Additions and Changes by Luigi for ShowMenuTree

#====================================================================
class OK_Btn(eg.ActionClass):

    def __call__(self):
        self.plugin.accept()
        	
				
#====================================================================
#Move into Submenu
            
class MoveRight (eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            if self.plugin.SelIsSubmenu():
		self.plugin.selPath.append (self.plugin.SelIndex())
		self.plugin.Refresh()
				
#====================================================================
#Move back one level
class MoveLeft (eg.ActionClass):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            if self.plugin.selPath != []:

                lastindex=self.plugin.selPath[len (self.plugin.selPath)-1]
		self.plugin.selPath = self.plugin.selPath [:len (self.plugin.selPath) -1]
		self.plugin.Refresh()
		self.plugin.menuDlg.GetSizer().GetChildren()[0].GetWindow().\
                    SetSelection(lastindex)
		
#=====================================================================

# Example for a Structure to use with ShowMenuTree. It is the same as for
# ShowTree, but allows nesting
		
exampleTree=(
    ('label 11','event 11'),
    ('label 12','event 12'),
    ('label 13','event 13'),
    ('submenu 14', (
        ('label 21', 'event 21'),
        ('label 22', 'event 22'),
        ('label 23', 'event 23'),
        ('submenu 24', (
            ('label 241','event241'),
            ('label 242','event 242'),
            ('label 243','event 243'),
            ('submenu 244',(
                ('label 2441', 'event 2441'),
                ('label 2442', 'event 2442'))),
            ('label 245', 'event 245'))),
        ('label 25', 'event 25'))),
    ('label 15','event 15'),
    ('submenu 16',(
                ('label 161', 'event 161'),
                ('label 162', 'event 162'))),
    ('label 17','event 17'),
    ('label 18','event 18'),
    ('label 19','event 19'),)

def IsSomeString (item):
    return ( type(item) ==type(u'') or
             type(item)==type(''))
    
class ShowMenuTree (eg.ActionClass):
    
    def TreeCopy(self,item, backstring=''):
        copy=[]
        for el in item:
            if not IsSomeString (el[1]):
                label=backstring+el[0]+u' >'
                copy.append([label,self.TreeCopy(el[1],'< ')])
            else:
                label= backstring + el[0] 
                copy.append ( [label ,el[1]] )
        return (copy)
    
    def __call__(
        self,
        tree =exampleTree,
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = u'0;-48;0;0;0;400;0;0;0;0;0;0;0;0;MS Shell Dlg 2'
    ):
        self.plugin.tree=self.TreeCopy(tree)
        self.plugin.fore=fore
        self.plugin.back=back
        self.plugin.fontInfo=fontInfo
	
        self.plugin.selPath=[]
        self.plugin.Refresh()
	
#====================================================================

ACTIONS = (
    (ShowMenu, 'ShowMenu', 'Show menu', 'Show on screen menu.', None),
    (ShowMenuTree, 'ShowMenuTree', 'Show a nested menu. For use within a Script', 'Show on screen nested menu.', None),
    (MoveCursor, 'MoveDown', 'Cursor Down', 'Cursor Down.', ('max-1', '-1', 1)),
    (MoveCursor, 'MoveUp', 'Cursor Up', 'Cursor Up.', ('0', 'max', -1)),
    (OK_Btn, 'OK_Btn', 'OK', 'OK button pressed.', None),
    (MoveRight, 'MoveRight', 'Select Submenu', 'Select Submenu', None),
    (MoveLeft, 'MoveLeft', 'Close Submenu', 'Close Submenu', None),    
    (Cancel_Btn, 'Cancel_Btn', 'Cancel', 'Cancel button pressed.', None),
)

#======================================================================

class OSM (eg.PluginClass):
    fore = (0, 0, 0)
    back = (255, 255, 255)
    fontInfo = None
    menuDlg = None
    choices = []
    tree=[]                 # Tree structure
    selPath=[]              # List of submenu-selections

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    # transferred from Action Class (to use it with ShowMenuTree)
    
    def ShowMenu (
        self,
        choices=[],
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None
        #bold = False
    ):
        self.fore=fore
        self.back=back
        if self.menuDlg is not None:
            return
        self.choices=choices
        self.menuDlg = wx.Frame(
                None, -1, 'OS_Menu', 
                style=wx.STAY_ON_TOP | wx.SIMPLE_BORDER
            )
        items=len(choices)
        #font = self.menuDlg.GetFont()
        #font.SetPointSize(32)
        #if bold:
        #    font.SetWeight(wx.BOLD)
        font = wx.FontFromNativeInfoString(fontInfo)
        self.menuDlg.SetFont(font)
        # menu height calculation:
        h=self.menuDlg.GetCharHeight()
        height0 = items*h+5
        height1 = h*((GetSystemMetrics (1)-20)/h)+5
        height = min(height0,height1)
        # menu width calculation:
        width_lst=[]
        for item in ExtractFromList(choices,0):
            width_lst.append(self.menuDlg.GetTextExtent(item+' ')[0])
        width = max(width_lst)
        width = min((width,GetSystemMetrics (0)-50))
        self.menuDlg.SetSize((width+6,height+6))
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        self.menuDlg.SetSizer(mainSizer)
        presChoiceCtrl=wx.ListBox(
            self.menuDlg,
            pos = ((2,2)),
            size=wx.Size(width,height),
            choices = ExtractFromList(choices,0),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB 
        )
        presChoiceCtrl.SetBackgroundColour(self.back)
        self.menuDlg.SetBackgroundColour((0,0,0))
        presChoiceCtrl.SetForegroundColour(self.fore)
        presChoiceCtrl.SetSelection(0)
        mainSizer.Add(presChoiceCtrl, 0, wx.EXPAND)
        
        def On2Click(evt):
            self.accept()
            evt.Skip()
                
        presChoiceCtrl.Bind(wx.EVT_LISTBOX_DCLICK, On2Click)
        self.menuDlg.Centre()
        self.menuDlg.Show()


    def SelIndex(self):
	if self.menuDlg is not None:
	    return (self.menuDlg.GetSizer().GetChildren()[0].\
                    GetWindow().GetSelection())
				
    def SelIsSubmenu(self):
	if self.menuDlg is not None:
            sel=self.SelIndex()
            return (not IsSomeString(self.choices[sel][1]))

    def accept(self):
        if (self.menuDlg is not None) and not self.SelIsSubmenu():
            sel=self.SelIndex()
            self.TriggerEvent(self.choices[sel][1])
            self.menuDlg.Destroy()
            self.menuDlg = None
            self.choices = []
            
    def Refresh(self):
 
        subtree=self.tree
        for sel in self.selPath:
            subtree=subtree[sel][1]
          
        if self.menuDlg is not None:
            self.menuDlg.Destroy()
        self.menuDlg = None
        self.choices = []
        self.ShowMenu(subtree,self.fore,self.back,self.fontInfo)
			

       

#====================================================================
