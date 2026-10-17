import pandas as pd
from database.DB_connect import DBConnect

cartellaCsv ="csv_completo/"

def valore(x):
    """ le celle vuote del CSV vengono lette da pandas come NaN """
    if pd.isna(x):
        return None
    return x


def getIdStagioni():

    """ restituisce il dizionario stagione -> id_stagione"""

    anniInizio = {"24/25": 2024, "25/26": 2025}

    conn = DBConnect.get_connection()
    result = {}

    cursor = conn.cursor(dictionary=True)
    query = """SELECT id_stagione FROM stagione WHERE anno_inizio = %s"""

    for stagione, anno in anniInizio.items():
        cursor.execute(query, (anno,))
        row = cursor.fetchone()
        result[stagione] = row["id_stagione"]

    cursor.close()
    conn.close()
    return result


def getIdCampionati():

    """
    restituisce il dizionario nome campionato -> id_campionato
    """

    conn = DBConnect.get_connection()

    result = {}

    cursor = conn.cursor(dictionary=True)
    query = """SELECT id_campionato, nome
               FROM campionato"""

    cursor.execute(query)

    for row in cursor:
        result[row["nome"]] = row["id_campionato"]

    cursor.close()
    conn.close()
    return result


def caricaSquadre(squadre, idStagioni, idCampionati):
    """
    inserisce i club in squadra e una riga in partecipazione_squadra per ogni riga del CSV.
    Restituisce i dizionari id_lnp -> id_squadra e (id_lnp, stagione) -> id_partecipazione
    """

    conn = DBConnect.get_connection()

    idSquadre = {}
    idPartecipazioni = {}

    cursor = conn.cursor(dictionary=True)

    # prima le righe del 25/26 così in squadra finisce il nome più recente
    squadre = squadre.sort_values("stagione", ascending=False)

    for riga in squadre.to_dict("records"):
        idLnp = riga["id_lnp"]
        stagione = riga["stagione"]

        if idLnp not in idSquadre:
            query = """INSERT INTO squadra (nome, id_lnp) VALUES (%s, %s)"""
            cursor.execute(query, (riga["nome"], idLnp))
            idSquadre[idLnp] = cursor.lastrowid

        idSquadra = idSquadre[idLnp]
        idStagione = idStagioni[stagione]
        idCampionato = idCampionati[riga["campionato"]]
        girone = valore(riga["girone"])

        query = """INSERT INTO partecipazione_squadra (id_squadra, id_stagione, id_campionato, nome, girone,
                                                        posizione, vittorie, sconfitte, punti_fatti, punti_subiti)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(query, (idSquadra, idStagione, idCampionato, riga["nome"], girone,
                               riga["posizione"], riga["vittorie"], riga["sconfitte"],
                               riga["punti_fatti"], riga["punti_subiti"]))
        idPartecipazioni[(idLnp, stagione)] = cursor.lastrowid

    conn.commit()
    cursor.close()
    conn.close()
    return idSquadre, idPartecipazioni


def caricaGiocatori(giocatori):

    """
    inserisce i giocatori nella tabella giocatore.
    Restituisce il dizionario slug_lnp -> id_giocatore
    """

    conn = DBConnect.get_connection()

    idGiocatori = {}

    cursor = conn.cursor(dictionary=True)

    # qui abbiamo molti valori che potrebbero essere NaN
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

    conn.commit()
    cursor.close()
    conn.close()
    return idGiocatori


def caricaStatistiche(statistiche, idGiocatori, idPartecipazioni):

    """
    inserisce le righe nella tabella statistica_stagionale, trasformando
    le colonne ponte del CSV (slug_lnp, id_lnp_squadra e stagione) negli id del database
    """

    conn = DBConnect.get_connection()

    cursor = conn.cursor(dictionary=True)

    for riga in statistiche.to_dict("records"):
        idGiocatore = idGiocatori[riga["slug_lnp"]]
        idPartecipazione = idPartecipazioni[(riga["id_lnp_squadra"], riga["stagione"])]

        query = """INSERT INTO statistica_stagionale
                   (id_giocatore, id_partecipazione, partite, minuti, punti,
                    tiri2_segnati, tiri2_tentati, tiri3_segnati, tiri3_tentati,
                    liberi_segnati, liberi_tentati, rimbalzi_offensivi, rimbalzi_difensivi,
                    assist, palle_recuperate, palle_perse, stoppate, stoppate_subite,
                    falli, falli_subiti, valutazione)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (idGiocatore, idPartecipazione,
                               riga["partite"], riga["minuti"], riga["punti"],
                               riga["tiri2_segnati"], riga["tiri2_tentati"],
                               riga["tiri3_segnati"], riga["tiri3_tentati"],
                               riga["liberi_segnati"], riga["liberi_tentati"],
                               riga["rimbalzi_offensivi"], riga["rimbalzi_difensivi"],
                               riga["assist"], riga["palle_recuperate"], riga["palle_perse"],
                               riga["stoppate"], riga["stoppate_subite"],
                               riga["falli"], riga["falli_subiti"], riga["valutazione"]))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":

    squadre = pd.read_csv(cartellaCsv + "squadre.csv")
    giocatori = pd.read_csv(cartellaCsv + "giocatori.csv")
    statistiche = pd.read_csv(cartellaCsv + "statistiche.csv")
    idStagioni = getIdStagioni()
    idCampionati = getIdCampionati()
    idSquadre, idPartecipazioni = caricaSquadre(squadre, idStagioni, idCampionati)
    idGiocatori = caricaGiocatori(giocatori)
    caricaStatistiche(statistiche, idGiocatori, idPartecipazioni)

    print(f"Squadre: {len(idSquadre)}, partecipazioni: {len(idPartecipazioni)}, giocatori: {len(idGiocatori)}, statistiche: {len(statistiche)}")