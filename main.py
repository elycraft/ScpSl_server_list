"""
SCP SL SERVERS LIST MAIN
BY ELYCRAFT
"""

###Imports

import lib
from notifypy import Notify
import pickle
from os.path import exists
from termcolor import cprint
from time import sleep
from _thread import *

###Constantes

VERSION = "1.0"

DEBUG = True

START = """
|  SCP SL SERVERS LIST  |
| 2021 v1.0 by ElyCraft |

"""
OK = "  OK!\n"

PATRON_CONFIG = {"version":VERSION,"server_name":None,"server_id":None}

FILENAME = 'config.ssc'

INVITE = "|USER|> "

CONSIGNE = """
> Help:
  - 1 for a notification every one minute
  - 2 to warn when there is room
  - stop for stop all commands
  - exit for exit the program
"""

###Global variable

stopThreads = False
config = {}

###Fonctions

#Techniques

def notif(playersTuple,serverName,b=False):
    notification.application_name = "SCP:SL Serveurs"
    if b:
       notification.title = playersTuple
    else:
        notification.title = "%s/%s joueurs"%playersTuple
    notification.message = serverName
    notification.icon = "logo.png"
    notification.send()

def save(objectToSave):
    outfile = open(FILENAME,'wb')
    pickle.dump(objectToSave,outfile)
    outfile.close()

def openC():
    infile = open(FILENAME,'rb')
    new_dict = pickle.load(infile)
    infile.close()
    return new_dict

def convert(config):
    p = list(PATRON_CONFIG.keys())
    n = list(config.keys())
    tr = []
    m = []
    for i in n:
        if i in p:
            pass
        else:
            tr.append(i)
    for i in p:
        if i in n:
            pass
        else:
            m.append(i)
    for i in tr:
        del(config[i])
    for i in m:
        config[i] = PATRON_CONFIG[i]
    config["version"] = VERSION
    return config

#Affichages

def nprint(message):
    cprint(message, 'white')

def ok():
    cprint(OK, 'green')

def warn(message):
    cprint("  [WARN] %s"%message,"yellow")

def error(message):
    cprint("  [ERROR] %s"%message,"red")

def debug(message):
    if not DEBUG:
        return None
    cprint("  [DEBUG] %s"%message,"blue")

#Principales

def rappel():
    while True:
        if stopThreads:
            return None

        notif(lib.get_players(int(config["server_id"])),config["server_name"])
        sleep(60)

def room():
    while True:
        if stopThreads:
            return None

        r = lib.get_players(int(config["server_id"]))
        if r[0] < r[1]:
            notif("There is room on the server",config["server_name"],True)
        sleep(60)

def main():
    global config
    cprint(START, 'blue')
    nprint('> Starting...')
    ok()
    nprint("> Searching config file...")
    if exists("config.ssc"):
        pass
    else:
        warn("Config file not found. Generating...")
        save(PATRON_CONFIG)
    ok()
    nprint("> Loading config file...")
    try:
        config = openC()
        ok()
    except Exception as e:
        error(str(e))
    nprint("> Scan config file...")
    if config["version"] == VERSION:
        pass
    else:
        warn("Old or new config detected. Converting...")
        config = convert(config)
        #debug(config)
        save(config)
    ok()
    if config["server_id"] == None:
        nprint("> No server id in the config. Please give a server id:")
        config["server_id"] = input(INVITE)
    if config["server_name"] == None:
        nprint("> The server %s has no name. Please give the server name:"%config["server_id"])
        config["server_name"] = input(INVITE)
    save(config)
    cprint("Startup finished!\n","green")
    
    while True:
        cprint(CONSIGNE, 'blue')
        cmd = input(INVITE)
        if cmd == "1":
            start_new_thread( rappel ,())
        elif cmd =="2":
            start_new_thread( room ,())
        elif cmd == "stop":
            global stopThreads
            stopThreads = True
        elif cmd == "exit":
            nprint("\n> Save... ")
            save(config)
            ok()
            nprint("> Exit...")
            break

###Main
   
notification = Notify()    

if __name__ == "__main__":
    main()