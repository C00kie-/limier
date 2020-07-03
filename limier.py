#!/usr/bin/env python3

# un fix super chelou Oo
# https://stackoverflow.com/questions/46457179/python3-cannot-import-name-cached-property
import werkzeug 
werkzeug.cached_property = werkzeug.utils.cached_property

from robobrowser import RoboBrowser
import re, time, argparse

#import locaux
import research, utils

print("Limier par darcosion (https://github.com/darcosion/limier)")

# paramètres de CLI
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", type=str,
                    help="domain to investigate")
parser.add_argument('-a', "--user-agent", type=str,
                    help="User-agent to use")

args = parser.parse_args()

if(args.user_agent):
    user_agent = args.user_agent
else:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'

# Création d'un browser pour les recherches
browser = RoboBrowser(user_agent=user_agent
                      , history=True
                      , parser='html.parser'
                      , allow_redirects=False)

# TODO : faire une vérification du domaine pour être sur...)
# une fonction réutilisable sera donc un plus, dans utils.py
assert utils.tld_check(args.domain), "le paramètre nom de domaine est incorrecte"
browser.open("https://" + args.domain)

#moulinette, pour le moment locale
listurl = []
listResearch = [research.getFluxLink
                , research.getSiteMapFlux
                , research.getFluxByGoogle]
#                , research.getFluxBruteForce]

for i in listResearch:
    listurl = list(set(listurl) | set(i(browser)))

#gestion des résultats
print('------------------------------------------')
print("--- Traitement des résultats collectés ---")
print('------------------------------------------')

#retire tout un bordel...
for n, i in enumerate(listurl):
    listurl[n] = re.sub("http(s?)://", '', i)
    listurl[n] = i.replace('//', '/')

listurl = list(set(listurl))

for i in listurl:
    print("[+] - " + i )
                   
