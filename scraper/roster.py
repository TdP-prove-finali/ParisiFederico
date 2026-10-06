import requests
from bs4 import BeautifulSoup



def leggiPaginaSquadra(url):
    """
    Legge il Wayback della pagina di una squadra.
    Restituisce il codice LNP della squadra e la lista dei giocatori (slug, nome).
    """
    risposta = requests.get(url)
    soup = BeautifulSoup(risposta.text, "html.parser")

    # il codice della squadra è nella classe del body
    idLNP = None
    for classe in soup.body["class"]:
        numero = classe.replace("page-node-", "")
        if classe.startswith("page-node-") and numero.isdigit():
            idLNP = int(numero)

    # cerco i link solo dentro il contenitore del roster
    giocatori = []
    roster = soup.find("div", class_="view-roster")
    for link in roster.find_all("a"):
        nome = " ".join(link.text.split())
        href = link.get("href", "")
        if nome != "" and "legapallacanestro.com/" in href:
            slug = href.split("legapallacanestro.com/")[1]
            giocatori.append((slug, nome))

    return idLNP, giocatori


if __name__ == "__main__":
    url = "https://web.archive.org/web/20260617144705/https://www.legapallacanestro.com/serie-b/allianz-pazienza-san-severo"  # snapshot Wayback di una squadra
    idLNP, giocatori = leggiPaginaSquadra(url)
    print("Codice squadra:", idLNP)
    print("Giocatori trovati:", len(giocatori))
    for giocatore in giocatori:
        print(giocatore)