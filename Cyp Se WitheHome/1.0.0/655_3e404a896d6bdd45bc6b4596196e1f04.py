import eg

eg.RegisterPlugin(
    name = "Cyp Se WitheHome",
    author = "Vishal",
    version = "1.0.0",
    kind = "remote",
    description = __doc__,
)

CODES = {
    (2,1,0,0,0,0,0,0,2,0,0,0,0,0,0,0): "Power",
    (1,1,0,4,0,0,0,0,1,0,0,0,0,0,0,0): "Radio",
    (1,1,0,23,0,0,0,0,1,0,0,0,0,0,0,0): "TV",
    (4,1,0,0,0,0,0,0,4,0,0,0,0,0,0,0): "Media Center",
    (1,1,0,17,0,0,0,0,1,0,0,0,0,0,0,0): "DVD",
    (1,1,0,16,0,0,0,0,1,0,0,0,0,0,0,0): "Music",
    (1,1,0,12,0,0,0,0,1,0,0,0,0,0,0,0): "Photo",
    (1,1,0,8,0,0,0,0,1,0,0,0,0,0,0,0): "Video",
    (1,1,0,25,0,0,0,0,1,0,0,0,0,0,0,0): "DVD Menu",
    (1,0,0,65,0,0,0,0,1,0,0,0,0,0,0,0): "Mute",
    (1,0,0,42,0,0,0,0,1,0,0,0,0,0,0,0): "Back",
    (1,0,0,58,0,0,0,0,1,0,0,0,0,0,0,0): "Guide",
    (1,1,0,21,0,0,0,0,1,0,0,0,0,0,0,0): "Record",
    (1,3,0,21,0,0,0,0,1,0,0,0,0,0,0,0): "Repeat",
    (1,0,0,40,0,0,0,0,1,0,0,0,0,0,0,0): "Enter",
    (1,0,0,82,0,0,0,0,1,0,0,0,0,0,0,0): "Arrow Up",
    (1,0,0,79,0,0,0,0,1,0,0,0,0,0,0,0): "Arrow Left",
    (1,0,0,81,0,0,0,0,1,0,0,0,0,0,0,0): "Arrow Down",
    (1,0,0,80,0,0,0,0,1,0,0,0,0,0,0,0): "Arrow Right",
    (3,1,0,0,0,0,0,0,3,0,0,0,0,0,0,0): "Volume +",
    (3,2,0,0,0,0,0,0,3,0,0,0,0,0,0,0): "Volume -",
    (1,0,0,75,0,0,0,0,1,0,0,0,0,0,0,0): "Channel +",
    (1,0,0,78,0,0,0,0,1,0,0,0,0,0,0,0): "Channel -",
    (1,0,0,30,0,0,0,0,1,0,0,0,0,0,0,0): "Number 1",
    (1,0,0,31,0,0,0,0,1,0,0,0,0,0,0,0): "Number 2",
    (1,0,0,32,0,0,0,0,1,0,0,0,0,0,0,0): "Number 3",
    (1,0,0,33,0,0,0,0,1,0,0,0,0,0,0,0): "Number 4",
    (1,0,0,34,0,0,0,0,1,0,0,0,0,0,0,0): "Number 5",
    (1,0,0,35,0,0,0,0,1,0,0,0,0,0,0,0): "Number 6",
    (1,0,0,36,0,0,0,0,1,0,0,0,0,0,0,0): "Number 7",
    (1,0,0,37,0,0,0,0,1,0,0,0,0,0,0,0): "Number 8",
    (1,0,0,38,0,0,0,0,1,0,0,0,0,0,0,0): "Number 9",
    (1,0,0,39,0,0,0,0,1,0,0,0,0,0,0,0): "Number 0",
    (1,3,0,19,0,0,0,0,1,0,0,0,0,0,0,0): "Play",
    (1,1,0,19,0,0,0,0,1,0,0,0,0,0,0,0): "Pause",
    (1,1,0,22,0,0,0,0,1,0,0,0,0,0,0,0): "Stop",
    (1,3,0,7,0,0,0,0,1,0,0,0,0,0,0,0): "Rewind",
    (1,3,0,9,0,0,0,0,1,0,0,0,0,0,0,0): "Forward",
    (1,1,0,5,0,0,0,0,1,0,0,0,0,0,0,0): "Skip Back",
    (1,1,0,9,0,0,0,0,1,0,0,0,0,0,0,0): "Skip Forward",

}

class Cyp_Se_WitheHome(eg.PluginBase):
               
    def __start__(self):
        self.usb = eg.WinUsbRemote(
            "{5607ED2F-AD3C-4CE8-9DE6-97CD4B0FFEF1}",
            self.Callback,
            16
        )
        if not self.usb.IsOk():
            raise self.Exceptions.DeviceNotFound

    def __stop__(self):
        self.usb.Close()

    def Callback(self, data):
        value = data[:16]
        if value in CODES:
            self.TriggerEvent(CODES[value])
        else:
            print data