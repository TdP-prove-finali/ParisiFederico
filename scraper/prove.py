import requests

url = "https://web.archive.org/web/20260622113109/https://www.legapallacanestro.com/serie-b/tav-treviglio-brianza-basket"  # lo snapshot Wayback di una squadra
risposta = requests.get(url)
print("Codice risposta:", risposta.status_code)
print("rubbini" in risposta.text.lower())