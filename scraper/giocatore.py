import time
import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup

urlLNP= "https://www.legapallacanestro.com/"
userAgent = "Mozilla/5.0"

# posizione di ogni statistica nella tabella Totali all'interno della pagina del giocatore
colonne = {
    "punti": 1,
    "partite": 2,
    "minuti": 3,
    "falli": 4,
    "falli_subiti": 5,
    "tiri2_segnati": 6,
    "tiri2_tentati": 7,
    "tiri3_segnati": 9,
    "tiri3_tentati": 10,
    "liberi_segnati": 12,
    "liberi_tentati": 13,
    "rimbalzi_offensivi": 15,
    "rimbalzi_difensivi": 16,
    "stoppate": 18,
    "stoppate_subite": 19,
    "palle_perse": 20,
    "palle_recuperate": 21,
    "assist": 22,
    "valutazione": 23,
}

stagioni = ["24/25", "25/26"]

def dividiNome(cognomeNome, nomeCognome):

    """
    funzione necessaria perché nome e cognome non si trovano in due campi separati,
    questo è un problema soprattutto per giocatori con nomi o cognomi doppi
    """

    parole = cognomeNome.split()
    for k in range(1, len(parole)):
        cognome = parole[:k]
        nome = parole[k:]
        if nome + cognome == nomeCognome.split():
            return " ".join(nome), " ".join(cognome)
    return None, None

def leggiAnagrafica(soup):
    cognomeNome = soup.find("div", class_ ="player-name").text
    nomeCognome = soup.find("h1", class_ ="page-header").text
    nome, cognome = dividiNome(cognomeNome, nomeCognome)
    if nome is None:
        print(f"Attenzione: nome da controllare a mano: {cognomeNome.strip()}")

    # coppie label - value
    scheda = {}
    labels = soup.find_all("span", class_="spec-label")
    values = soup.find_all("span", class_="spec-value")

    for i in range(len(labels)):
        scheda[labels[i].text.strip()] = values[i].text.strip()

    dataNascita = None
    if scheda.get("Data di nascita:"):
        try:
            dataNascita = datetime.strptime(scheda["Data di nascita:"], "%d/%m/%Y").date()
        except ValueError:
            dataNascita = None

    altezza = None
    if scheda.get("Altezza:"):
        numero = scheda["Altezza:"].split()[0]  # 190 cm --> 190
        if numero.isdigit():
            altezza = int(numero)

    ruolo = None
    divRuolo = soup.find("div", class_ = "ruolo")
    if divRuolo is not None:
        ruolo = divRuolo.text.strip()

    nazionalita = scheda.get("Nazionalità:")

    # alcune giocatori italiani hanno nazionalità "Italia" invece di "ITA"
    nomiPaesi = {"Italia": "ITA"}
    nazionalita = nomiPaesi.get(nazionalita, nazionalita)

    return {
        "nome": nome,
        "cognome": cognome,
        "data_nascita": dataNascita,
        "nazionalita": nazionalita,
        "altezza_cm": altezza,
        "ruolo": ruolo,
    }

def riconosciCompetizione(parteSinistra):

    """
    dalla prima colonna della tabella Totali ricava campionato stagione e girone;
    restituisce None se la riga non è di serie A2 o B delle stagioni scelte
    """

    for stagione in stagioni:
        if parteSinistra == "Serie A2 " + stagione:
            return "Serie A2", stagione, None
        if parteSinistra.startswith("Serie B - Girone ") and parteSinistra.endswith(" " + stagione):
            girone = parteSinistra.replace("Serie B - Girone ", "").replace(" " + stagione, "")
            return "Serie B Nazionale", stagione, girone
    return None


def leggiStatistiche(html):

    """
    restituisce le righe di regular season di A2 e B delle stagioni 24/25 e 25/26,
    di solito è una ma possono essere più di una se il giocatore
    ha cambiato squadra durante la stagione
    """

    try:
        totali = pd.read_html(StringIO(html))[0]
    except:
        return [] # il giocatore non ha statistiche

    tabella = totali.fillna(0).values.tolist()

    righe = []

    for riga in tabella[1:]: # la riga 0 contiene i nomi delle colonne
        competizione = str(riga[0])

        if ": " not in competizione:
            continue
        parteSinistra, squadra = competizione.split(": ", 1)

        risultato = riconosciCompetizione(parteSinistra)
        if risultato is None:
            continue
        if int(riga[colonne["partite"]]) == 0:
            continue

        campionato, stagione, girone = risultato
        statistica = {"campionato": campionato, "stagione": stagione, "girone": girone, "squadra": squadra}
        for nomeColonna, posizione in colonne.items():
            statistica[nomeColonna] = int(riga[posizione])
        righe.append(statistica)

    return righe


def leggiPaginaGiocatore(slug):

    """
    Legge la pagiona di un giocatore, restituisce l'anagrafica
    e le statistiche stagionali
    """

    risposta = requests.get(urlLNP + slug, headers={"User-Agent": userAgent}, timeout = 30)

    if risposta.status_code != 200:
        print(f"Errore {risposta.status_code} per {slug}")
        return None, []

    soup = BeautifulSoup(risposta.text, "html.parser")
    giocatore = leggiAnagrafica(soup)
    giocatore["slug_lnp"] = slug
    statistiche = leggiStatistiche(risposta.text)
    return giocatore, statistiche

if __name__ == "__main__":

    for slug in ["marini-pierpaolo", "landi-aristide", "radunic-matej", "cappelletti-carlo"]:
        giocatore, statistiche = leggiPaginaGiocatore(slug)
        if giocatore is None:
            continue
        print(f"{giocatore['cognome']} {giocatore['nome']}")
        for riga in statistiche:
            print(f"{riga['campionato']} {riga['stagione']} {riga['girone']} {riga['squadra']} partite: {riga['partite']}")
        time.sleep(10)