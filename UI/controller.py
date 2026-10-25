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
        print(f"Sostituti di {self._giocatoreScelto}: {len(sostituti)}")
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
        print(f"Giocatori migliori di {self._giocatoreScelto}: {len(migliori)}")
        print(f"{self._giocatoreScelto} è migliore di {nPeggiori} giocatori")
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
        print(f"Rimosso dalla lista {giocatore}")
        self._model.rimuoviLista(giocatore)
        self._view._txtAggiuntaLista.value = ""
        self.mostraLista()