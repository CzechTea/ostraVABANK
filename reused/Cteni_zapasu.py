import json

with open("zapas.json") as z:
    zapas = json.load(z)

print(zapas["DOMACI"] + " vs. " + zapas["HOST"] + "\n" + zapas["DOMACI_SKORE"]+ ":"+zapas["HOST_SKORE"])