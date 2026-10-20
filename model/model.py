import networkx as nx
from networkx import Graph

from database.DAO import DAO


class Model:
    def __init__(self):
        self._giocatori = DAO.getAllGiocatori()
        self._idMapGiocatori = {}
        for giocatore in self._giocatori:
            self._idMapGiocatori[giocatore.id_giocatore] = giocatore
        self._statistiche = {}

    def getAllStagioni(self):
        return DAO.getAllStagioni()

    def getAllCampionati(self):
        return DAO.getAllCampionati()

    def caricaGiocatori(self, stagione, campionato):
        self._statistiche = {}
        for statistica in DAO.getStatisticheGiocatori(stagione.id_stagione, campionato.id_campionato):
            giocatore = self._idMapGiocatori[statistica.id_giocatore]
            self._statistiche[giocatore] = statistica
        return len(self._statistiche)

    def cercaGiocatori(self, testo):
        testo = testo.lower()
        risultato = []
        for giocatore in self._statistiche:
            if testo in giocatore.cognome.lower():
                risultato.append(giocatore)
        risultato.sort(key=lambda x: str(x))
        return risultato