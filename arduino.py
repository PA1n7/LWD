import time
from pyfirmata import STRING_DATA, Arduino, util
from fetchsong import get_song_info
from unidecode import unidecode

port = '/dev/ttyACM0' # Set the port being used

board = Arduino(port)

def msg( text ):
    text = text[:16]
    if text:
        board.send_sysex( STRING_DATA, util.str_to_two_byte_iter( text ) )
    else:
        board.send_sysex( STRING_DATA, util.str_to_two_byte_iter( ' ' ) )

upper_text = "Track Reader"
lower_text = "Starting..."

U_shown = 0
D_shown = 0

#Separation in scroll
sep = 2
mku = 0

# time per check
lic = True # Set to True if you want to let text scroll before update
tpc = 3
_tpc = tpc
tpC = 0 #counter

def update():
    info = get_song_info()
    if info == None:
        info = {
            "title":"Waiting for",
            "author":"Song :D"
            }
    global U_shown, D_shown, upper_text, lower_text
    U_shown = 0
    D_shown = 0
    upper_text = unidecode(info["title"])
    lower_text = unidecode(info["author"])



while True:
    if len(upper_text) > 16 and len(lower_text)>16:
        mku = abs(len(upper_text)-len(lower_text))
    if lic and (len(upper_text)>16 or len(lower_text)>16):
        tpc = max([len(upper_text), len(lower_text)])+sep
    else:
        tpc = int(_tpc)
    if len(upper_text) > 16:
        if len(upper_text)<len(lower_text):
            _sep=sep+mku
        else:
            _sep = sep
        if U_shown == len(upper_text):
            U_shown = -_sep+1
            msg(" "*_sep+upper_text)
        elif U_shown >= 0 and U_shown<len(upper_text):
            msg(upper_text[U_shown:]+_sep*" "+upper_text)
            U_shown+=1
        elif U_shown<0:
            msg(" "*-U_shown+upper_text)
            U_shown+=1
    else:
        msg(upper_text)
    if len(lower_text) > 16:
        if len(upper_text)>len(lower_text):
            _sep=sep+mku
        else:
            _sep = sep
        if D_shown == len(lower_text):
            D_shown = -_sep+1
            msg(" "*_sep+lower_text)
        elif D_shown >= 0 and D_shown<len(lower_text):
            msg(lower_text[D_shown:]+" "*_sep+lower_text)
            D_shown+=1
        elif D_shown<0:
            msg(" "*-D_shown+lower_text)
            D_shown+=1
    else:
        msg(lower_text)

    time.sleep(1)
    tpC+=1
    if tpC == tpc:
        tpC = 0
        update()
