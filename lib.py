"""
SCP SL SERVERS LIST LIB
BY ELYCRAFT
"""

### IMPORTS ###

import requests
import json

### CONSTANTES ###

HEADERS = {
    'authority': 'scplist.kr',
    'x-mod-sbb-ctype': 'xhr',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://scplist.kr',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://scplist.kr/',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'dnt': '1',
}

DATA = '{"search":"","countryFilter":[],"hideEmptyServer":false,"hideFullServer":false,"friendlyFire":"null","whitelist":"null","modded":"null","sort":"DISTANCE_ASC"}'

HEAVEN_RP = 34873 #For exemple

### FONCTIONS ###

def get_json(headers=HEADERS,data=DATA,local=False):
  """
  Prend un headers et un data (fournit par defaut) et local : requete ou fichier local.

  Keyword arguments:
    headers -- Headers de la requete
    data -- Data de la requete
    local -- Fichier local (True) ou non (False). 
  """


  if local:

    with open("output.json", "rb") as fic:
        out_raw = fic.read()
  else:

    response = requests.post('https://scplist.kr/api/servers', headers=headers, data=data)
    out_raw = response.content
    with open("output.json", "wb") as fic:
        fic.write(out_raw)

  out_raw = json.loads(out_raw)
  servers_raw = out_raw["servers"]
  servers_raw = json.dumps(servers_raw)
  servers = json.loads(servers_raw)
  return servers

def search_players (serverId,serversJson):
  """
  Cherche dans le json et renvoi un str de l'entrée "players" d'un "serverId".

  Keyword arguments:
    serverId -- l'id du serveur dans le json
    serversJson -- la variable qui contient le json
  """

  for i in serversJson:
      
      if i['serverId'] == serverId:
          return i['players']
          break

def get_players(serverId):
  """
  Renvoi un tuple de l'entrée "players" d'un serveur.

  Keyword arguments:
    serverId -- l'id du serveur dans le json
  """
  a = search_players(serverId,get_json(local=False))
  return (a.split("/")[0],a.split("/")[1])

### MAIN ###

if __name__ == "__main__":
  print(get_players(HEAVEN_RP))