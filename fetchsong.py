# Checking for OS
from sys import platform

if platform == "windows":
    import win32gui, win32process
    import psutil
    
    def get_process_name(pid):
        try:
            return psutil.Process(pid).name()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    
    title_out = "wakakak"
    
    def winEnumHandler( hwnd, ctx ):
        global title_out
        if win32gui.IsWindowVisible( hwnd ):
            title = win32gui.GetWindowText( hwnd )
            _class = win32gui.GetClassName(hwnd)
            if _class == "Chrome_WidgetWin_1":
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if get_process_name(pid) == "Spotify.exe":
                    title_out = title
    
    def get_song_info():
        win32gui.EnumWindows( winEnumHandler, None )
        if "-" not in title_out and "Spotify" in title_out:
            return None
        wow = title_out.split(" - ")
        info = {"author":wow[0], "title":" - ".join(wow[1:])}
        return info

elif platform == "linux":
    def get_song_info():
        from pydbus import SessionBus
        bus = SessionBus()
        Spotify= bus.get(
            "org.mpris.MediaPlayer2.spotify", # Bus name
            "/org/mpris/MediaPlayer2" # Object path
        )
        data = Spotify.Metadata
        info = {"author":data["xesam:artist"][0], "title":data["xesam:title"]}
        if (Spotify.PlaybackStatus == "Paused"):
            return None

        else:
            return info
