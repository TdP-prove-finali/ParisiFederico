import copy

import networkx as nx
from networkx import Graph, DiGraph

from database.DAO import DAO


class Model:
    def __init__(self):
        self._giocatori = DAO.getAllGiocatori()
        self._idMapGiocatori = {}
        for giocatore in self._giocatori:
            self._idMapGiocatori[giocatore.id_giocatore] = giocatore
        self._statistiche = {}
        self._stagione = None
        self._campionato = None
        self._listaDesideri = {}
        self._maxLista = 30

        # simulatore: i ruoli da riempire per ogni tipo di quintetto
        self._quintetti = {"Standard": ["Play", "Guardia", "Ala", "Ala", "Centro"],
                            "Piccolo": ["Play", "Guardia", "Guardia", "Ala", "Ala"],
                            "Alto": ["Play", "Ala", "Ala", "Centro", "Centro"],
                            "Due play": ["Play", "Play", "Ala", "Ala", "Centro"]}


        # profili per il confronto
        self._profili = {"Generale": ["punti", "rimbalzi", "assist"],
                         "Valutazione": ["valutazione"],
                         "Tiratore": ["tiri3_tentati", "percentuale_tiri3"],
                         "Passatore": ["assist", "rapporto_assist"],
                         "Tiri liberi": ["liberi_tentati", "percentuale_liberi"],
                         "Difensore": ["palle_recuperate", "stoppate"],
                         "Rimbalzista": ["rimbalzi_offensivi", "rimbalzi_difensivi"]}

        #statistiche per rendere un giocatore confrontabile
        self._partiteMinime = 5
        self._minutiMinimi = 3  #per partita
        self._tripleMinime = 20  #nella stagione intera
        self._assistMinimi = 20  # stagione intera
        self._rangeSimilarita = 0.10
        self._sogliaSpecialita = 75

        self._grafoSimilarita = Graph()
        self._valoriProfilo = {}
        self._grafoDominanze = DiGraph()

        self._candidati = []
        self._bestQuintetto = []
        self._bestPunteggio = -1
        self._nQuintettiProvati = 0
        self._tipoQuintetto = None
        self._maxStranieri = None
        self._minimiSpecialita = {}
        self._specialitaPiccolo = ["Rimbalzista", "Difensore"]

    def getAllStagioni(self):
        return DAO.getAllStagioni()

    def getAllCampionati(self):
        return DAO.getAllCampionati()

    def caricaGiocatori(self, stagione, campionato):
        self._statistiche = {}
        self._stagione = stagione
        self._campionato = campionato
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

    def getStatistica(self, giocatore):
        return self._statistiche[giocatore]

    def getSquadreGiocatore(self, giocatore):
        return DAO.getSquadreGiocatore(giocatore.id_giocatore, self._stagione.id_stagione, self._campionato.id_campionato)

    def getNomiSquadre(self, giocatore):
        nomi = []
        for squadra in self.getSquadreGiocatore(giocatore):
            nomi.append(squadra["nome"])
        return " / ".join(nomi)

    def getProfili(self):
        return list(self._profili.keys())

    def getStatisticheProfilo(self, profilo):
        return self._profili[profilo]

    def getValore(self, stat, nomeStatistica):

        if nomeStatistica == "percentuale_tiri3":
            return stat.percentuale(stat.tiri3_segnati, stat.tiri3_tentati)
        if nomeStatistica == "percentuale_liberi":
            return stat.percentuale(stat.liberi_segnati, stat.liberi_tentati)
        if nomeStatistica == "rimbalzi":
            return stat.perPartita(stat.rimbalzi_offensivi + stat.rimbalzi_difensivi)
        if nomeStatistica == "rapporto_assist":
            return stat.assist / stat.palle_perse

        totali = {"punti": stat.punti,
                  "assist": stat.assist,
                  "tiri3_tentati": stat.tiri3_tentati,
                  "liberi_tentati": stat.liberi_tentati,
                  "palle_recuperate": stat.palle_recuperate,
                  "stoppate": stat.stoppate,
                  "rimbalzi_offensivi": stat.rimbalzi_offensivi,
                  "rimbalzi_difensivi": stat.rimbalzi_difensivi,
                  "valutazione": stat.valutazione}

        return stat.perPartita(totali[nomeStatistica])

    def getMotivoEsclusione(self, giocatore, profilo):

        """
        controlla se il giocatore si può confrontare nel profilo scelto
        restituisce il motivo dell'esclusione oppure None se il giocatore va bene
        """

        stat = self._statistiche[giocatore]
        statisticheProfilo = self._profili[profilo]

        if giocatore.ruolo is None:
            return "ruolo non disponibile"
        if stat.partite < self._partiteMinime:
            return f"meno di {self._partiteMinime} partite giocate"
        if stat.perPartita(stat.minuti) < self._minutiMinimi:
            return f"meno di {self._minutiMinimi} minuti a partita"
        if "percentuale_tiri3" in statisticheProfilo and stat.tiri3_tentati < self._tripleMinime:
            return f"meno di {self._tripleMinime} triple tentate"
        if "percentuale_liberi" in statisticheProfilo and stat.liberi_tentati == 0:
            return "nessun tiro libero tentato"
        if "rapporto_assist" in statisticheProfilo and stat.assist < self._assistMinimi:
            return f"meno di {self._assistMinimi} assist"
        if "rapporto_assist" in statisticheProfilo and stat.palle_perse == 0:
            return "nessuna palla persa"

        return None

    def getGiocatoriConfrontabili(self, profilo):
        """
        giocatori caricati che si possono confrontare nel profilo scelto.
        Restituisce il dizionario giocatore -> lista dei valori delle statistiche del profilo
        """
        statisticheProfilo = self._profili[profilo]
        result = {}

        for giocatore in self._statistiche:
            if self.getMotivoEsclusione(giocatore, profilo) is not None:
                continue

            stat = self._statistiche[giocatore]
            valori = []
            for nomeStatistica in statisticheProfilo:
                valori.append(self.getValore(stat, nomeStatistica))
            result[giocatore] = valori

        return result

    def buildGrafoSimilarita(self, profilo):
        self._grafoSimilarita.clear()
        self._valoriProfilo = self.getGiocatoriConfrontabili(profilo)
        self._grafoSimilarita.add_nodes_from(self._valoriProfilo.keys())

        intervalli = self.getIntervalloValori(profilo)
        self.addEdgesSimilarita(intervalli)


    def getGraphDetails(self):
        return len(self._grafoSimilarita.nodes), len(self._grafoSimilarita.edges)

    def getSostituti(self, giocatore):
        """vicini del giocatore nel grafo delle similarità, ordinati per peso crescente (i più simili prima)"""
        sostituti = []
        for vicino in self._grafoSimilarita.neighbors(giocatore):
            peso = self._grafoSimilarita[giocatore][vicino]["weight"]
            valori = self._valoriProfilo[vicino]
            squadre = self.getNomiSquadre(vicino)
            sostituti.append((vicino, peso, valori, squadre))
        sostituti.sort(key=lambda x: x[1])
        return sostituti

    def getDatiGiocatore(self, giocatore):
        return (giocatore, 0, self._valoriProfilo[giocatore], self.getNomiSquadre(giocatore))

    def getIntervalloValori(self, profilo):
        """
        fornisce la differenza tra il valore piu alto e piu in basso di una statistica
        """
        scale = []
        for i in range(len(self._profili[profilo])):
            valoriStatistica = []
            for giocatore in self._valoriProfilo:
                valoriStatistica.append(self._valoriProfilo[giocatore][i])
            scale.append(max(valoriStatistica) - min(valoriStatistica))
        return scale

    def ruoliCompatibili(self, giocatore1, giocatore2):
        """compatibili se i ruoli hanno almeno una parte in comune (es. Play e Play/Guardia)"""
        ruoli1 = giocatore1.ruolo.split("/")
        ruoli2 = giocatore2.ruolo.split("/")
        for ruolo in ruoli1:
            if ruolo in ruoli2:
                return True
        return False

    def getPesoSimilarita(self, valori1, valori2, intervalli):
        """
        None se in almeno una statistica la differenza supera il range,
        altrimenti la somma delle differenze divise per l'intervallo (più è basso, più i giocatori sono simili)
        """
        peso = 0
        for i in range(len(intervalli)):
            differenza = abs(valori1[i] - valori2[i])
            if differenza > self._rangeSimilarita * intervalli[i]:
                return None
            peso += differenza / intervalli[i]
        return peso

    def addEdgesSimilarita(self, intervalli):
        giocatori = list(self._valoriProfilo.keys())
        for i in range(len(giocatori)):
            for j in range(i + 1, len(giocatori)):
                giocatore1 = giocatori[i]
                giocatore2 = giocatori[j]
                if self.ruoliCompatibili(giocatore1, giocatore2):
                    peso = self.getPesoSimilarita(self._valoriProfilo[giocatore1],
                                                  self._valoriProfilo[giocatore2],
                                                  intervalli)
                    if peso is not None:
                        self._grafoSimilarita.add_edge(giocatore1, giocatore2, weight=peso)

    def buildGrafoDominanze(self, profilo):
        self._grafoDominanze.clear()
        self._valoriProfilo = self.getGiocatoriConfrontabili(profilo)
        self._grafoDominanze.add_nodes_from(self._valoriProfilo.keys())

        intervalli = self.getIntervalloValori(profilo)
        self.addEdgesDominanza(intervalli)

    def addEdgesDominanza(self, intervalli):
        for giocatore1 in self._valoriProfilo:
            for giocatore2 in self._valoriProfilo:
                if giocatore1 != giocatore2 and self.ruoliCompatibili(giocatore1, giocatore2):
                    peso = self.getPesoDominanza(self._valoriProfilo[giocatore1],
                                                 self._valoriProfilo[giocatore2],
                                                 intervalli)
                    if peso is not None:
                        self._grafoDominanze.add_edge(giocatore1, giocatore2, weight=peso)

    def getGraphDetailsDominanze(self):
        return len(self._grafoDominanze.nodes), len(self._grafoDominanze.edges)

    def getPesoDominanza(self, valori1, valori2, intervalli):
        """
        peso dell'arco se il primo è nettamente migliore del secondo:
        migliore o uguale in tutte le statistiche del profilo e in almeno una
        con una differenza maggiore del range
        """

        peso = 0
        nettamenteMigliore = False
        for i in range(len(intervalli)):
            differenza = valori1[i] - valori2[i]
            if differenza < 0:
                return None
            if differenza > self._rangeSimilarita * intervalli[i]:
                nettamenteMigliore = True
            peso += differenza / intervalli[i]

        if not nettamenteMigliore:
            return None
        return peso

    def getMigliori(self, giocatore):
        """giocatori nettamente migliori del giocatore ordinati per peso crescente"""
        migliori = []
        for predecessore in self._grafoDominanze.predecessors(giocatore):
            peso = self._grafoDominanze[predecessore][giocatore]["weight"]
            valori = self._valoriProfilo[predecessore]
            squadre = self.getNomiSquadre(predecessore)
            migliori.append((predecessore, peso, valori, squadre))
        migliori.sort(key=lambda x: x[1])
        return migliori

    def getNumeroPeggiori(self, giocatore):
        """numero di giocatori di cui il giocatore è nettamente migliore"""
        return self._grafoDominanze.out_degree(giocatore)

    def getPunteggioProfilo(self, giocatore, profilo):

        """
        per ogni statistica del profilo, percentuale di giocatori del suo ruolo con un valore più basso;
        restituisce la media di queste percentuali (da 0 a 100) oppure None se il giocatore non è confrontabile
        """
        if self.getMotivoEsclusione(giocatore, profilo) is not None:
            return None

        confrontabili = self.getGiocatoriConfrontabili(profilo)
        valoriGiocatore = confrontabili[giocatore]

        # giocatori di ruolo compatibile confrontabili nello stesso profilo
        giocatoriCompatibili = []
        for altro in confrontabili:
            if altro != giocatore and self.ruoliCompatibili(giocatore, altro):
                giocatoriCompatibili.append(altro)

        if len(giocatoriCompatibili) == 0:
            return None

        sommaPercentuali = 0
        for i in range(len(valoriGiocatore)):
            nSuperati = 0
            for altro in giocatoriCompatibili:
                if confrontabili[altro][i] < valoriGiocatore[i]:
                    nSuperati += 1
            percentuale = nSuperati / len(giocatoriCompatibili) * 100
            sommaPercentuali += percentuale

        return sommaPercentuali / len(valoriGiocatore)

    def getSpecialita(self, giocatore):
        """
        lista dei profili in cui il giocatore ha un punteggio di almeno 75"""

        punteggi = []
        for profilo in self._profili:
            if profilo == "Generale" or profilo == "Valutazione":
                continue
            punteggio = self.getPunteggioProfilo(giocatore, profilo)
            if punteggio is None:
                print(f"{giocatore} - {profilo}: non confrontabile")
            else:
                print(f"{giocatore} - {profilo}: {punteggio:.1f}")
                punteggi.append((profilo, punteggio))

        if len(punteggi) == 0:
            return None

        punteggi.sort(key=lambda x: x[1], reverse=True)
        specialita = []
        for profilo, punteggio in punteggi:
            if punteggio >= self._sogliaSpecialita:
                specialita.append(profilo)
        return specialita

    def getMotivoNonAggiungibile(self, giocatore):

        if giocatore in self._listaDesideri:
            stagione, campionato, stat, specialita, punteggioRuolo = self._listaDesideri[giocatore]
            return f"{giocatore} è già nella lista ({campionato} {stagione})"
        if len(self._listaDesideri) >= self._maxLista:
            return f"La lista è piena ({self._maxLista} giocatori)"
        return None

    def aggiungiLista(self, giocatore):

        stat = self._statistiche[giocatore]
        specialita = self.getSpecialita(giocatore)
        punteggioRuolo = self.getPunteggioProfilo(giocatore, "Valutazione")
        self._listaDesideri[giocatore] = (self._stagione, self._campionato, stat, specialita, punteggioRuolo)
        return self._stagione, self._campionato, len(self._listaDesideri)

    def getListaDesideri(self):
        return self._listaDesideri

    def rimuoviLista(self, giocatore):
        del self._listaDesideri[giocatore]

    def getQuintetti(self):
        return list(self._quintetti.keys())

    def getCandidati(self):

        """non uso getMotivoEsclusione perché legge la stagione caricata in quel momento"""
        candidati = []
        esclusi = []
        for giocatore in self._listaDesideri:
            stagione, campionato, stat, specialita, punteggioRuolo = self._listaDesideri[giocatore]
            if giocatore.ruolo is None:
                esclusi.append((giocatore, "ruolo non disponibile"))
            elif stat.partite < self._partiteMinime:
                esclusi.append((giocatore, f"meno di {self._partiteMinime} partite giocate"))
            elif stat.perPartita(stat.minuti) < self._minutiMinimi:
                esclusi.append((giocatore, f"meno di {self._minutiMinimi} minuti a partita"))
            else:
                candidati.append(giocatore)
        return candidati, esclusi

    def getRuoliQuintetto(self, tipoQuintetto):
        return self._quintetti[tipoQuintetto]

    def getQuintettoMigliore(self, tipoQuintetto, candidati, maxStranieri,minimiSpecialita):
        self._candidati = candidati
        self._tipoQuintetto = tipoQuintetto
        self._maxStranieri = maxStranieri
        self._minimiSpecialita = minimiSpecialita
        self._bestQuintetto = []
        self._bestPunteggio = -1
        self._nQuintettiProvati = 0

        ruoli = self._quintetti[tipoQuintetto]
        parziale = []
        self._ricorsione(parziale, ruoli)

        return self._bestQuintetto, self._bestPunteggio, self._nQuintettiProvati

    def _ricorsione(self, parziale, ruoli):

        if self._getNumeroStranieri(parziale) > self._maxStranieri:
            return

        if len(parziale) == len(ruoli):
            self._nQuintettiProvati += 1
            if self._rispettaCondizioni(parziale, ruoli):
                punteggio = self._getPunteggioQuintetto(parziale)
                if punteggio > self._bestPunteggio:
                    self._bestQuintetto = copy.deepcopy(parziale)
                    self._bestPunteggio = punteggio
            return

        prossimoRuolo = ruoli[len(parziale)]
        for giocatore in self._candidati:
            if giocatore not in parziale and prossimoRuolo in giocatore.ruolo.split("/"):
                parziale.append(giocatore)
                self._ricorsione(parziale, ruoli)
                parziale.pop()

    def _getPunteggioQuintetto(self, quintetto):
        sommaPunteggi = 0
        for giocatore in quintetto:
            stagione, campionato, stat, specialita, punteggioRuolo = self._listaDesideri[giocatore]
            sommaPunteggi += punteggioRuolo
        return sommaPunteggi

    def _getNumeroStranieri(self, quintetto):
        nStranieri = 0
        for giocatore in quintetto:
            if giocatore.nazionalita is not None and "ITA" not in giocatore.nazionalita:
                nStranieri += 1
        return nStranieri

    def _haSpecialita(self, giocatore, nomeSpecialita):
        stagione, campionato, stat, specialita, punteggioRuolo = self._listaDesideri[giocatore]
        if nomeSpecialita in specialita:
            return True
        else:
            return False

    def _rispettaCondizioni(self, quintetto, ruoli):

        # numero minimo di giocatori per ogni specialità
        for nomeSpecialita in self._minimiSpecialita:
            nGiocatori = 0
            for giocatore in quintetto:
                if self._haSpecialita(giocatore, nomeSpecialita):
                    nGiocatori += 1
            if nGiocatori < self._minimiSpecialita[nomeSpecialita]:
                return False

        if self._tipoQuintetto == "Piccolo":
            alaAdatta = False
            for i in range(len(quintetto)):
                if ruoli[i] == "Ala":
                    for nomeSpecialita in self._specialitaPiccolo:
                        if self._haSpecialita(quintetto[i], nomeSpecialita):
                            alaAdatta = True
            if not alaAdatta:
                return False

        return True
