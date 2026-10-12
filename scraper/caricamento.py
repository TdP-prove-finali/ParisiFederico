import pandas as pd
from database.DB_connect import DBConnect


def valore(x):
    """ le celle vuote del CSV vengono lette da pandas come NaN """
    if pd.isna(x):
        return None
    return x

conn = DBConnect.get_connection()
cursor = conn.cursor(dictionary=True)

# id di stagione e campionato, già inseriti dallo script SQL
query = """SELECT id_stagione FROM stagione WHERE anno_inizio = 2025"""
cursor.execute(query)
idStagione = cursor.fetchone()["id_stagione"]

query = """SELECT id_campionato FROM campionato WHERE nome = 'Serie B Nazionale'"""
cursor.execute(query)
idCampionato = cursor.fetchone()["id_campionato"]

squadre = pd.read_csv("csv/squadre.csv")
giocatori = pd.read_csv("csv/giocatori.csv")
statistiche = pd.read_csv("csv/statistiche.csv")


# Squadre e Partecipazioni

idPartecipazioni ={}

for riga in squadre.to_dict("records"):

    query = """ INSERT INTO squadra ( nome, id_lnp) VALUES (%s,%s)"""
    cursor.execute(query, (riga["nome"], riga["id_lnp"]))
    idSquadra = cursor.lastrowid


    query = """INSERT INTO partecipazione_squadra
               (id_squadra, id_stagione, id_campionato, girone, posizione,
                vittorie, sconfitte, punti_fatti, punti_subiti)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.execute(query, (idSquadra, idStagione, idCampionato, riga["girone"], riga["posizione"],
                          riga["vittorie"], riga["sconfitte"], riga["punti_fatti"], riga["punti_subiti"]))
    idPartecipazioni[riga["id_lnp"]] = cursor.lastrowid

# Giocatori

idGiocatori = {}

for riga in giocatori.to_dict("records"):
    dataNascita = valore(riga["data_nascita"])
    nazionalita = valore(riga["nazionalita"])
    ruolo = valore(riga["ruolo"])
    altezza = valore(riga["altezza_cm"])
    if altezza is not None:
        altezza = int(altezza)

    query = """INSERT INTO giocatore (nome, cognome, data_nascita,
                                      nazionalita, altezza_cm, ruolo, slug_lnp)
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (riga["nome"], riga["cognome"], dataNascita,
                           nazionalita, altezza, ruolo, riga["slug_lnp"]))
    idGiocatori[riga["slug_lnp"]] = cursor.lastrowid

# Stats

for riga in statistiche.to_dict("records"):
    idGiocatore = idGiocatori[riga["slug_lnp"]]
    idPartecipazione = idPartecipazioni[riga["id_lnp_squadra"]]

    query = """INSERT INTO statistica_stagionale
               (id_giocatore, id_partecipazione, partite, minuti, punti,
                tiri2_segnati, tiri2_tentati, tiri3_segnati, tiri3_tentati,
                liberi_segnati, liberi_tentati, rimbalzi_offensivi, rimbalzi_difensivi,
                assist, palle_recuperate, palle_perse, stoppate, stoppate_subite,
                falli, falli_subiti, valutazione)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.execute(query, (idGiocatore, idPartecipazione, riga["partite"], riga["minuti"], riga["punti"],
                           riga["tiri2_segnati"], riga["tiri2_tentati"], riga["tiri3_segnati"], riga["tiri3_tentati"],
                           riga["liberi_segnati"], riga["liberi_tentati"], riga["rimbalzi_offensivi"], riga["rimbalzi_difensivi"],
                           riga["assist"], riga["palle_recuperate"], riga["palle_perse"], riga["stoppate"], riga["stoppate_subite"],
                           riga["falli"], riga["falli_subiti"], riga["valutazione"]))

conn.commit()
print(f"Squadre: {len(squadre)}, giocatori: {len(giocatori)}, statistiche: {len(statistiche)}")
cursor.close()
conn.close()