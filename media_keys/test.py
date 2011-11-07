import pythoncom, pyHook

def OnKeyboardEvent(event):
    if event.MessageName == "key_down":
        if event.Key == "Media_Play_Pause":
            pass
        elif event.Key == "Media_Prev_Track":
            pass
        elif event.Key == "Media_Next_Track":
            pass
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


# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
