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

            for giocatore in self._model.cercaGiocatori(testo):
                self._view._ddGiocatore.options.append(
                    ft.dropdown.Option(data=giocatore,
                                       key=str(giocatore.id_giocatore),
                                       text=str(giocatore),
                                       on_click=self.handleSceltaGiocatore)
                )
        self._view.update_page()

    def handleSceltaGiocatore(self, e):
        self._giocatoreScelto = e.control.data
        print(f"Hai selezionato {self._giocatoreScelto}")


    def handleAggiungiLista(self, e):
        pass

    def handleTrovaSostituto(self, e):
        pass

    def handleTrovaMigliore(self, e):
        pass