from database.DB_connect import DBConnect
from model.Partecipazione import Partecipazione
from model.giocatore import Giocatore
from model.stagione import Stagione
from model.campionato import Campionato
from model.totaliGiocatore import TotaliGiocatore


class DAO():

    @staticmethod
    def getAllGiocatori():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
            FROM giocatore g 
            ORDER BY g.cognome, g.nome"""

        cursor.execute(query)

        for row in cursor:
            result.append(Giocatore(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllStagioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
            FROM stagione s
            ORDER BY s.anno_inizio DESC"""

        cursor.execute(query)

        for row in cursor:
            result.append(Stagione(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllCampionati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
           FROM campionato c
           ORDER BY c.livello"""

        cursor.execute(query)

        for row in cursor:
            result.append(Campionato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStatisticheGiocatori(idStagione, idCampionato):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT ss.id_giocatore,
                          SUM(ss.partite) AS partite, SUM(ss.minuti) AS minuti, SUM(ss.punti) AS punti,
                          SUM(ss.tiri2_segnati) AS tiri2_segnati, SUM(ss.tiri2_tentati) AS tiri2_tentati,
                          SUM(ss.tiri3_segnati) AS tiri3_segnati, SUM(ss.tiri3_tentati) AS tiri3_tentati,
                          SUM(ss.liberi_segnati) AS liberi_segnati, SUM(ss.liberi_tentati) AS liberi_tentati,
                          SUM(ss.rimbalzi_offensivi) AS rimbalzi_offensivi,
                          SUM(ss.rimbalzi_difensivi) AS rimbalzi_difensivi,
                          SUM(ss.assist) AS assist, SUM(ss.palle_recuperate) AS palle_recuperate,
                          SUM(ss.palle_perse) AS palle_perse, SUM(ss.stoppate) AS stoppate,
                          SUM(ss.stoppate_subite) AS stoppate_subite, SUM(ss.falli) AS falli,
                          SUM(ss.falli_subiti) AS falli_subiti, SUM(ss.valutazione) AS valutazione
                   FROM statistica_stagionale ss, partecipazione_squadra p
                   WHERE ss.id_partecipazione = p.id_partecipazione
                   AND p.id_stagione = %s
                   AND p.id_campionato = %s
                   GROUP BY ss.id_giocatore"""

        cursor.execute(query, (idStagione, idCampionato))

        for row in cursor:
            # SUM restituisce numeri decimali: li trasformo in interi
            for chiave in row:
                row[chiave] = int(row[chiave])
            result.append(TotaliGiocatore(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSquadreGiocatore(idGiocatore, idStagione, idCampionato):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT p.nome, p.posizione, p.girone, ss.partite, ss.punti
                   FROM statistica_stagionale ss, partecipazione_squadra p
                   WHERE ss.id_partecipazione = p.id_partecipazione
                   AND ss.id_giocatore = %s
                   AND p.id_stagione = %s
                   AND p.id_campionato = %s"""

        cursor.execute(query, (idGiocatore, idStagione, idCampionato))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPartecipazioni(idStagione, idCampionato):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT p.id_partecipazione, p.nome, p.girone, p.posizione,
                          p.vittorie, p.sconfitte, p.punti_fatti, p.punti_subiti
                   FROM partecipazione_squadra p
                   WHERE p.id_stagione = %s
                   AND p.id_campionato = %s
                   ORDER BY p.girone, p.posizione"""

        cursor.execute(query, (idStagione, idCampionato))

        for row in cursor:
            result.append(Partecipazione(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getGiocatoriSquadra(idPartecipazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT ss.id_giocatore, ss.partite, ss.minuti, ss.punti,
                          ss.tiri2_segnati, ss.tiri2_tentati, ss.tiri3_segnati, ss.tiri3_tentati,
                          ss.liberi_segnati, ss.liberi_tentati,
                          ss.rimbalzi_offensivi, ss.rimbalzi_difensivi,
                          ss.assist, ss.palle_recuperate, ss.palle_perse, ss.stoppate,
                          ss.stoppate_subite, ss.falli, ss.falli_subiti, ss.valutazione
                   FROM statistica_stagionale ss
                   WHERE ss.id_partecipazione = %s"""

        cursor.execute(query, (idPartecipazione,))

        for row in cursor:
            result.append(TotaliGiocatore(**row))

        cursor.close()
        conn.close()
        return result