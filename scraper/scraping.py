import time
import pandas as pd
from roster import leggiPaginaSquadra
from classifica import leggiClassifica
from giocatore import leggiPaginaGiocatore


def leggiSquadre():

    """
    legge le classifiche e le pagine delle squadre.
    Restituisce la lista delle squadre, il dizionario nome -> id_lnp e gli slug di tutti i giocatori.
    """


    classifiche = {}

    for girone in ["A", "B"]:
        for squadra in leggiClassifica("pagine/classificaSerieBGirone"+girone+".html", girone):
            classifiche[squadra["nome"].upper()] = squadra

    fileExcel = pd.read_excel("SquadreBNazionale.xlsx").values.tolist()

    squadre = []
    idSquadre = {}
    slugGiocatori = set() # per non ammettere doppioni

    for nome, girone, url in fileExcel:
        squadra = classifiche[nome]
        idLNP, giocatori = leggiPaginaSquadra(url)

        print(f"{nome}; codice: {idLNP}; numero giocatori: {len(giocatori)}")

        for slug, nomeGiocatore in giocatori:
            slugGiocatori.add(slug)

        time.sleep(10)

        squadra["id_lnp"] = idLNP
        squadre.append(squadra)
        idSquadre[nome] = idLNP

    return squadre, idSquadre, slugGiocatori


def leggiGiocatori(slugGiocatori, idSquadre):

    """
    legge dal sito la pagina di ogni giocatore.
    Restituisce la lista dei giocatori e la lista delle squadre.
    """

    giocatori = []
    statistiche = []
    erroriSlug = []

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
            continue # non ha giocato in B nazionale nel 25/26

        giocatori.append(giocatore)

        for riga in righe:
            riga["slug_lnp"] = slug
            nomeSquadra = riga["squadra"].upper()
            if nomeSquadra in idSquadre:
                riga["id_lnp_squadra"] = idSquadre[nomeSquadra]
            else:
                riga["id_lnp_squadra"] = None
                print(f"Squadra non trovata: {riga['squadra']}")
            statistiche.append(riga)

    print(f"Pagine con errori: {erroriSlug}")
    return giocatori, statistiche





if __name__ == "__main__":
    squadre, idSquadre, slugGiocatori = leggiSquadre()

    pd.DataFrame(squadre).to_csv("csv/squadre.csv", index=False)

    print(f"Squadre lette: {len(squadre)}")
    print(f"Giocatori da leggere: {len(slugGiocatori)}")

    giocatori, statistiche = leggiGiocatori(slugGiocatori, idSquadre)
    pd.DataFrame(giocatori).to_csv("csv/giocatori.csv", index=False)
    pd.DataFrame(statistiche).to_csv("csv/statistiche.csv", index=False)
    print(f"Giocatori salvati: {len(giocatori)}")
    print(f"Righe di statistiche: {len(statistiche)}")