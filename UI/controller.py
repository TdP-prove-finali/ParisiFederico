import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._stagioneScelta = None
        self._campionatoScelto = None
        self._giocatoreScelto = None
        self._profiloScelto = None

    def fillDropdownStagioni(self):
        for stagione in self._model.getAllStagioni():
            self._view._ddStagione.options.append(
                ft.dropdown.Option(data=stagione,
                                   key=str(stagione),
                                   on_click=self._choiceDdStagione)
            )

    def fillDropdownCampionati(self):
        for campionato in self._model.getAllCampionati():
            self._view._ddCampionato.options.append(
                ft.dropdown.Option(data=campionato,
                                   key=campionato.nome,
                                   on_click=self._choiceDdCampionato)
            )

    def _choiceDdStagione(self, e):
        self._stagioneScelta = e.control.data
        print(f"Hai selezionato la stagione {self._stagioneScelta}")
        self._view._txtMessaggio.value = ""
        self._view.update_page()

    def _choiceDdCampionato(self, e):
        self._campionatoScelto = e.control.data
        print(f"Hai selezionato il campionato {self._campionatoScelto}")
        self._view._txtMessaggio.value = ""
        self._view.update_page()

    def handleCaricaGiocatori(self, e):
        if self._stagioneScelta is None:
            self._view.create_alert("Selezionare una stagione")
            return

        if self._campionatoScelto is None:
            self._view.create_alert("Selezionare un campionato")
            return

        nGiocatori = self._model.caricaGiocatori(self._stagioneScelta, self._campionatoScelto)
        self._view._txtMessaggio.value = f"Caricati {nGiocatori} giocatori della {self._campionatoScelto} {self._stagioneScelta}"
        self._view._txtMessaggio.color = "green"

        self._view._txtInCognome.value = ""
        self._view._txtInCognome.error_text = None
        self._view._txtInCognome.disabled = False
        self._view._ddGiocatore.options.clear()
        self._view._ddGiocatore.value = None
        self._giocatoreScelto = None
        self._view.txtResultsGiocatore.controls.clear()

        self.fillDropdownNazionalita()
        self._view._btnCerca.disabled = False
        self._view._txtAggiuntaRicerca.value = ""
        self._view.txtResultsRicerca.controls.clear()

        self._view.update_page()

    def handleFiltraGiocatori(self, e):
        testo = self._view._txtInCognome.value
        self._view._ddGiocatore.options.clear()
        self._view._ddGiocatore.value = None
        self._giocatoreScelto = None
        self._view._txtInCognome.error_text = None

        if testo != "":
            giocatori = self._model.cercaGiocatori(testo)
            if len(giocatori) == 0:
                self._view._txtInCognome.error_text = "Nessun giocatore trovato"

            for giocatore in giocatori:
                self._view._ddGiocatore.options.append(
                    ft.dropdown.Option(data=giocatore,
                                       key=str(giocatore.id_giocatore),
                                       text=str(giocatore),
                                       on_click=self.handleSceltaGiocatore)
                )
        self._view.update_page()

    def mostraScheda(self):
        stat = self._model.getStatistica(self._giocatoreScelto)
        squadre = self._model.getSquadreGiocatore(self._giocatoreScelto)
        specialita = self._model.getSpecialita(self._giocatoreScelto)
        self._view.mostraSchedaGiocatore(self._giocatoreScelto, stat, squadre, specialita)

    def handleSceltaGiocatore(self, e):
        self._giocatoreScelto = e.control.data
        self._view._txtAggiuntaLista.value = ""
        self.mostraScheda()

    def fillDropdownProfili(self):
        for profilo in self._model.getProfili():
            self._view._ddProfilo.options.append(
                ft.dropdown.Option(data=profilo,
                                   key=profilo,
                                   on_click=self._choiceDdProfilo)
            )

    def fillDropdownQuintetti(self):
        for quintetto in self._model.getQuintetti():
            self._view._ddQuintetti.options.append(ft.dropdown.Option(key=quintetto))

    def _choiceDdProfilo(self, e):
        self._profiloScelto = e.control.data
        print(f"Hai selezionato il profilo {self._profiloScelto}")

        if self._giocatoreScelto is not None:
            self.mostraScheda()

    def handleTrovaSostituto(self, e):
        if self._giocatoreScelto is None:
            self._view.create_alert("Selezionare un giocatore")
            return

        if self._profiloScelto is None:
            self._view.create_alert("Selezionare un profilo")
            return

        motivo = self._model.getMotivoEsclusione(self._giocatoreScelto, self._profiloScelto)
        if motivo is not None:
            self._view.create_alert(f"{self._giocatoreScelto} non è confrontabile: {motivo}")
            return

        self._model.buildGrafoSimilarita(self._profiloScelto)
        nNodi, nArchi = self._model.getGraphDetails()
        print(f"Grafo delle similarità, profilo {self._profiloScelto}: {nNodi} nodi e {nArchi} archi")

        sostituti = self._model.getSostituti(self._giocatoreScelto)
        for sostituto, peso, valori, squadre in sostituti:
            print(f"{sostituto} - peso {peso:.3f}")

        statisticheProfilo = self._model.getStatisticheProfilo(self._profiloScelto)
        scelto = self._model.getDatiGiocatore(self._giocatoreScelto)
        self.mostraScheda()
        self._view.mostraSostituti(scelto, self._profiloScelto, statisticheProfilo, sostituti)

    def handleTrovaMigliore(self, e):
        if self._giocatoreScelto is None:
            self._view.create_alert("Selezionare un giocatore")
            return

        if self._profiloScelto is None:
            self._view.create_alert("Selezionare un profilo")
            return

        motivo = self._model.getMotivoEsclusione(self._giocatoreScelto, self._profiloScelto)
        if motivo is not None:
            self._view.create_alert(f"{self._giocatoreScelto} non è confrontabile: {motivo}")
            return

        self._model.buildGrafoDominanze(self._profiloScelto)
        nNodi, nArchi = self._model.getGraphDetailsDominanze()
        print(f"Grafo delle dominanze, profilo {self._profiloScelto}: {nNodi} nodi e {nArchi} archi")

        migliori = self._model.getMigliori(self._giocatoreScelto)
        nPeggiori = self._model.getNumeroPeggiori(self._giocatoreScelto)
        for migliore, peso, valori, squadre in migliori:
            print(f"{migliore} - peso {peso:.3f}")

        statisticheProfilo = self._model.getStatisticheProfilo(self._profiloScelto)
        scelto = self._model.getDatiGiocatore(self._giocatoreScelto)
        self.mostraScheda()
        self._view.mostraMigliori(scelto, self._profiloScelto, statisticheProfilo, migliori, nPeggiori)

    def mostraLista(self):
        listaDesideri = self._model.getListaDesideri()
        self._view.mostraListaDesideri(listaDesideri)


    def handleAggiungiLista(self, e):
        if self._giocatoreScelto is None:
            self._view.create_alert("Selezionare un giocatore")
            return

        motivo = self._model.getMotivoNonAggiungibile(self._giocatoreScelto)
        if motivo is not None:
            self._view.create_alert(motivo)
            return

        stagione, campionato, nGiocatori = self._model.aggiungiLista(self._giocatoreScelto)
        self._view._txtAggiuntaLista.value = f"{self._giocatoreScelto} ({campionato} {stagione}) aggiunto alla lista. Giocatori nella lista: {nGiocatori}"
        self._view._txtAggiuntaLista.color = "green"
        self.mostraLista()

    def handleRimuoviLista(self, e):
        giocatore = e.control.data
        self._model.rimuoviLista(giocatore)
        self._view._txtAggiuntaLista.value = ""
        self.mostraLista()

    def handleSimulaQuintetto(self, e):
        if len(self._model.getListaDesideri()) == 0:
            self._view.create_alert("La lista è vuota: aggiungere giocatori dalla scheda Giocatore")
            return

        tipoQuintetto = self._view._ddQuintetti.value
        if tipoQuintetto is None:
            self._view.create_alert("Selezionare il tipo di quintetto")
            return

        if self._view._ddStranieri.value is None:
            maxStranieri = 5
        else:
            maxStranieri = int(self._view._ddStranieri.value)

        # numero minimo di giocatori per specialità, senza scelta 0
        menuSpecialita = [("Tiratore", self._view._ddTiratori),
                          ("Passatore", self._view._ddPassatori),
                          ("Tiri liberi", self._view._ddTiriLiberi),
                          ("Difensore", self._view._ddDifensori),
                          ("Rimbalzista", self._view._ddRimbalzisti)]
        minimiSpecialita = {}
        for specialita, menu in menuSpecialita:
            if menu.value is None:
                minimiSpecialita[specialita] = 0
            else:
                minimiSpecialita[specialita] = int(menu.value)

        candidati, esclusi = self._model.getCandidati()

        quintetto, sommaPunteggi, nProvati = self._model.getQuintettoMigliore(tipoQuintetto, candidati, maxStranieri, minimiSpecialita)
        ruoli = self._model.getRuoliQuintetto(tipoQuintetto)
        print(f"Quintetti provati: {nProvati}")

        listaDesideri = self._model.getListaDesideri()
        self.mostraLista()
        self._view.mostraQuintetto(tipoQuintetto, quintetto, ruoli, sommaPunteggi, esclusi, listaDesideri)

    def fillDropdownNazionalita(self):
        self._view._ddNazionalita.options.clear()
        self._view._ddNazionalita.value = None
        nazionalita, nStranieri = self._model.getNazionalita()

        self._view._ddNazionalita.options.append(ft.dropdown.Option(key="Tutte"))
        self._view._ddNazionalita.options.append(ft.dropdown.Option(key="Stranieri", text=f"Stranieri ({nStranieri})"))
        for codice, numero in nazionalita:
            self._view._ddNazionalita.options.append(ft.dropdown.Option(key=codice, text=f"{codice} ({numero})"))

    def handleCerca(self, e):
        # menu non scelto (None) o voce "Tutti"/"Tutte": nessun filtro
        ruolo = self._view._ddRuolo.value
        if ruolo == "Tutti":
            ruolo = None

        nazionalita = self._view._ddNazionalita.value
        if nazionalita == "Tutte":
            nazionalita = None

        specialita = self._view._ddSpecialita.value
        if specialita == "Tutte":
            specialita = None

        testoEta = self._view._txtInEta.value
        if testoEta == "":
            etaMassima = None
        else:
            try:
                etaMassima = int(testoEta)
            except ValueError:
                self._view.create_alert("L'età massima deve essere un numero intero")
                return

        risultati = self._model.getGiocatoriRicerca(ruolo, etaMassima, nazionalita, specialita)

        self._view._txtAggiuntaRicerca.value = ""
        self._view.mostraRicerca(risultati)

    def handleAggiungiDaRicerca(self, e):
        giocatore = e.control.data
        motivo = self._model.getMotivoNonAggiungibile(giocatore)
        if motivo is not None:
            self._view.create_alert(motivo)
            return

        stagione, campionato, nGiocatori = self._model.aggiungiLista(giocatore)
        self._view._txtAggiuntaRicerca.value = f"{giocatore} ({campionato} {stagione}) aggiunto alla lista. Giocatori nella lista: {nGiocatori}"
        self._view._txtAggiuntaRicerca.color = "green"
        self.mostraLista()