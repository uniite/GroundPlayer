import pyHook, pythoncom
import threading
from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol
import win32api
import win32con


class HookHandlerThread(threading.Thread):
    def run(self):
        print "New connection"
        # Create a hook manager
        hm = pyHook.HookManager()
        # Watch all key events
        hm.KeyDown = self.key_event
        # Add the hook
        hm.HookKeyboard()
        # Process the hook events
        pythoncom.PumpMessages()
        # Remove hook
        hm.UnhookKeyboard()
        print "Done"

    def key_event(self, event):
        if event.MessageName == "key down":
            if event.Key == "Media_Play_Pause":
                print "Play/Pause"
                self.socket.sendMessage("p")
            elif event.Key == "Media_Prev_Track":
                print "Prev"
                self.socket.sendMessage("<")
            elif event.Key == "Media_Next_Track":
                print "Next"
                self.socket.sendMessage(">")
            elif event.Key == "Volume_Mute":
                pass
            elif event.Key == "Volume_Down":
                pass
            elif event.Key == "Volume_Up":
                pass
            elif event.Key == "Launch_Media_Select":
                pass
            else:
                return True


class EchoServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.hook = HookHandlerThread()
        self.hook.socket = self
        self.hook.start()

    def onClose(self, wasClean, code, reason):
        if hasattr(self, "hook"):
            print "Closing %s" % self.hook.ident
            win32api.PostThreadMessage(self.hook.ident, win32con.WM_QUIT, 0, 0);
        print "Closed"

if __name__ == '__main__':
   factory = WebSocketServerFactory()
   factory.protocol = EchoServerProtocol
   factory.port = 8002
   reactor.listenTCP(8002, factory)
   reactor.run()
