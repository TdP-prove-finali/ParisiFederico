import time
import pandas as pd
from roster import leggiPaginaSquadra
from classifica import leggiClassifica
from giocatore import leggiPaginaGiocatore

cartellaCsv = "csv_completo/"

fileClassifiche = [
    ("classificaB_2526_GironeA.html", "Serie B Nazionale", "25/26", "A"),
    ("classificaB_2526_GironeB.html", "Serie B Nazionale", "25/26", "B"),
    ("classificaB_2425_GironeA.html", "Serie B Nazionale", "24/25", "A"),
    ("classificaB_2425_GironeB.html", "Serie B Nazionale", "24/25", "B"),
    ("classificaA2_2526.html", "Serie A2", "25/26", None),
    ("classificaA2_2425.html", "Serie A2", "24/25", None),
]

def leggiSquadre():

    """
    legge le classifiche e le pagine delle squadre.
    Restituisce la lista delle partecipazioni,
    il dizionario (stagione, nome)-> id_lnp, gli slug di tutti i giocatori
    e le squadre da controllare.
    """


    classifiche = {}

    for nomeFile, campionato, stagione, girone in fileClassifiche:
        for squadra in leggiClassifica("pagine/"+nomeFile,  girone):
            squadra["campionato"] = campionato
            squadra["stagione"] = stagione
            classifiche[(stagione, squadra["nome"].upper())] = squadra

    fileExcel = pd.read_excel("Squadre.xlsx").values.tolist()

    squadre = []
    idSquadre = {}
    slugGiocatori = set() # per non ammettere doppioni
    daControllare = []

    for campionato, stagione, girone, nome, url in fileExcel:
        squadra = classifiche[(stagione, nome)]
        idLNP, giocatori = leggiPaginaSquadra(url)

        print(f"{campionato} {stagione} {nome}; codice: {idLNP}; numero giocatori: {len(giocatori)}")

        if idLNP is None or len(giocatori) == 0:
            daControllare.append(f"{nome} ({stagione})")

        for slug, nomeGiocatore in giocatori:
            slugGiocatori.add(slug)

        time.sleep(10)

        squadra["id_lnp"] = idLNP
        squadre.append(squadra)
        idSquadre[(stagione, nome)] = idLNP

    return squadre, idSquadre, slugGiocatori, daControllare


def leggiGiocatori(slugGiocatori, idSquadre):

    """
    legge dal sito la pagina di ogni giocatore.
    Restituisce la lista dei giocatori e la lista delle statistiche.
    """

    giocatori = []
    statistiche = []
    erroriSlug = []
    squadreNonTrovate = set()

    letti = 0
    for slug in slugGiocatori:
        time.sleep(10)
        letti += 1

        try:
            giocatore, righe = leggiPaginaGiocatore(slug)
        except Exception:
            giocatore, righe = None, []

        print(f"{letti} su {len(slugGiocatori)}; righe: {len(righe)}")

        if giocatore is None:
            erroriSlug.append(slug) #pagina non letta
        if len(righe) == 0:
            continue # non ha giocato in B nazionale o in A2

        giocatori.append(giocatore)

        for riga in righe:
            riga["slug_lnp"] = slug
            chiave = (riga["stagione"], riga["squadra"].upper())
            if chiave in idSquadre:
                riga["id_lnp_squadra"] = idSquadre[chiave]
            else:
                riga["id_lnp_squadra"] = None
                squadreNonTrovate.add(chiave)
                print(f"Squadra non trovata: {riga['squadra']} ({riga['stagione']})")
            statistiche.append(riga)

    print(f"Pagine con errori: {erroriSlug}")
    print(f"squadre non trovate: {squadreNonTrovate}")
    return giocatori, statistiche


if __name__ == "__main__":
    squadre, idSquadre, slugGiocatori, daControllare = leggiSquadre()

    pd.DataFrame(squadre).to_csv(cartellaCsv + "squadre.csv", index=False)

    print(f"Squadre lette: {len(squadre)}")
    print(f"Giocatori da leggere: {len(slugGiocatori)}")

    if len(daControllare) > 0:
        print(f"Squadre da controllare: {daControllare}")
    else:
        giocatori, statistiche = leggiGiocatori(slugGiocatori, idSquadre)
        pd.DataFrame(giocatori).to_csv(cartellaCsv + "giocatori.csv", index=False)
        pd.DataFrame(statistiche).to_csv(cartellaCsv + "statistiche.csv", index=False)
        print(f"Giocatori salvati: {len(giocatori)}")
        print(f"Righe di statistiche: {len(statistiche)}")