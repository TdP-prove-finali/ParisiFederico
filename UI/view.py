import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Scouting basket 2026"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self._title = None

    def load_interface(self):

        self._title = ft.Text("Scouting Basket 2026", color="blue", size=24)

        # parte in alto

        self._ddStagione = ft.Dropdown(label="Stagione")
        self._ddCampionato = ft.Dropdown(label="Campionato")
        self._controller.fillDropdownStagioni()
        self._controller.fillDropdownCampionati()

        self._btnCaricaGiocatori = ft.ElevatedButton(text="Carica giocatori",
                                                     on_click=self._controller.handleCaricaGiocatori)


        self._rowDati = ft.Row([ft.Container(self._ddStagione, width=250),
                          ft.Container(self._ddCampionato, width=250),
                          ft.Container(self._btnCaricaGiocatori, width=250)],
                         alignment=ft.MainAxisAlignment.CENTER)

        self._txtMessaggio = ft.Text("")

        #scheda ricerca
        self._ddRuolo = ft.Dropdown(label="Ruolo")
        for ruolo in ["Tutti", "Play", "Guardia", "Ala", "Centro"]:
            self._ddRuolo.options.append(ft.dropdown.Option(key=ruolo))

        self._txtInEta = ft.TextField(label="Età massima")

        # si riempie quando si caricano i giocatori: i numeri dipendono da stagione e campionato
        self._ddNazionalita = ft.Dropdown(label="Nazionalità")

        self._ddSpecialita = ft.Dropdown(label="Specialità")
        for specialita in ["Tutte", "Tiratore", "Passatore", "Tiri liberi", "Difensore", "Rimbalzista"]:
            self._ddSpecialita.options.append(ft.dropdown.Option(key=specialita))

        self._btnCerca = ft.ElevatedButton(text="Cerca",
                                           on_click=self._controller.handleCerca,
                                           disabled=True)

        rowFiltri = ft.Row([ft.Container(self._ddRuolo, width=180),
                            ft.Container(self._txtInEta, width=180),
                            ft.Container(self._ddNazionalita, width=180),
                            ft.Container(self._ddSpecialita, width=180),
                            ft.Container(self._btnCerca, width=180)],
                           alignment=ft.MainAxisAlignment.CENTER)

        self._txtAggiuntaRicerca = ft.Text("")

        self.txtResultsRicerca = ft.ListView(expand=1, spacing=10, padding=20)

        schedaRicerca = ft.Column([ft.Container(height=10), rowFiltri,
                                   ft.Row([self._txtAggiuntaRicerca], alignment=ft.MainAxisAlignment.CENTER),
                                   self.txtResultsRicerca],
                                  spacing=20)

        # scheda giocatore

        self._txtInCognome = ft.TextField(label="Cognome",
                                          on_change=self._controller.handleFiltraGiocatori,
                                          disabled=True)

        self._ddGiocatore = ft.Dropdown(label="Giocatore")

        self._btnAggiungiLista = ft.ElevatedButton(text="Aggiungi alla lista",
                                                   on_click=self._controller.handleAggiungiLista)

        rowCerca = ft.Row([ft.Container(self._txtInCognome, width=250),
                           ft.Container(self._ddGiocatore, width=250),
                           ft.Container(self._btnAggiungiLista, width=250,
                                        padding=ft.padding.only(top=12))],
                          alignment=ft.MainAxisAlignment.CENTER,
                          vertical_alignment=ft.CrossAxisAlignment.START)

        self._ddProfilo = ft.Dropdown(label="Profilo")
        self._controller.fillDropdownProfili()

        self._btnTrovaSostituto = ft.ElevatedButton(text="Trova sostituto",
                                                    on_click=self._controller.handleTrovaSostituto)
        self._btnTrovaMigliore = ft.ElevatedButton(text="Trova migliore",
                                                   on_click=self._controller.handleTrovaMigliore)

        rowProfilo = ft.Row([ft.Container(self._ddProfilo, width=250),
                             ft.Container(self._btnTrovaSostituto, width=250),
                             ft.Container(self._btnTrovaMigliore, width=250)],
                            alignment=ft.MainAxisAlignment.CENTER)

        self._txtAggiuntaLista = ft.Text("")

        self.txtResultsGiocatore = ft.ListView(expand=1, spacing=10, padding=20)

        schedaGiocatore = ft.Column([ft.Container(height=10), rowCerca, rowProfilo,
                                     ft.Row([self._txtAggiuntaLista], alignment=ft.MainAxisAlignment.CENTER),
                                     self.txtResultsGiocatore],
                                    spacing=20)


        # scheda lista e simulatore
        self._ddQuintetti = ft.Dropdown(label="Tipo di quintetto")
        self._controller.fillDropdownQuintetti()
        self._ddStranieri = self.creaMenuNumero("Stranieri al massimo")
        self._ddStranieri.options[5].text = "5 (nessun limite)"
        self._btnSimula = ft.ElevatedButton(text="Simula quintetto",
                                            on_click=self._controller.handleSimulaQuintetto)

        rowSimulatore = ft.Row([ft.Container(self._ddQuintetti, width=250),
                                ft.Container(self._ddStranieri, width=250),
                                ft.Container(self._btnSimula, width=250)],
                               alignment=ft.MainAxisAlignment.CENTER)

        # numero minimo di giocatori del quintetto per ogni specialità
        self._ddTiratori = self.creaMenuNumero("Tiratori")
        self._ddPassatori = self.creaMenuNumero("Passatori")
        self._ddTiriLiberi = self.creaMenuNumero("Tiri liberi")
        self._ddDifensori = self.creaMenuNumero("Difensori")
        self._ddRimbalzisti = self.creaMenuNumero("Rimbalzisti")

        rowSpecialita = ft.Row([ft.Text("Minimo per specialità:"),
                                ft.Container(self._ddTiratori, width=140),
                                ft.Container(self._ddPassatori, width=140),
                                ft.Container(self._ddTiriLiberi, width=140),
                                ft.Container(self._ddDifensori, width=140),
                                ft.Container(self._ddRimbalzisti, width=140)],
                               alignment=ft.MainAxisAlignment.CENTER)

        self.txtResultsLista = ft.ListView(expand=1, spacing=10, padding=20)
        self._controller.mostraLista()

        schedaLista = ft.Column([ft.Container(height=10), rowSimulatore, rowSpecialita, self.txtResultsLista],
                                spacing=20)

        # schede
        self._tabs = ft.Tabs(selected_index=0,
                             tabs=[ft.Tab(text="Ricerca", content=schedaRicerca),
                                   ft.Tab(text="Giocatore", content=schedaGiocatore),
                                   ft.Tab(text="Lista e simulatore", content=schedaLista)],
                             expand=1,
                             tab_alignment=ft.TabAlignment.CENTER)

        self._page.add(self._title, self._rowDati, self._txtMessaggio, self._tabs)
        self._page.update()

    def mostraNone(self, valore):
        # per i dati che mancano nel database
        if valore is None:
            return "n.d."
        return valore

    def mostraSpecialita(self, specialita):
        # testo delle specialità da mostrare a schermo
        if specialita is None:
            return "n.d."
        if len(specialita) == 0:
            return "nessuna"
        return ", ".join(specialita)

    def creaMenuNumero(self, etichetta):
        menu = ft.Dropdown(label=etichetta)
        for numero in range(6):
            menu.options.append(ft.dropdown.Option(key=str(numero)))
        return menu

    def mostraSchedaGiocatore(self, giocatore, stat, squadre, specialita):
        risultati = self.txtResultsGiocatore.controls
        risultati.clear()

        # nome giocatore
        risultati.append(ft.Row([ft.Text(f"{giocatore}", size=20, weight=ft.FontWeight.BOLD)],
                                alignment=ft.MainAxisAlignment.CENTER))

        # riquadro anagrafica
        datiPersonali = [("Ruolo", giocatore.ruolo),
                         ("Età", giocatore.getEta()),
                         ("Altezza (cm)", giocatore.altezza_cm),
                         ("Nazionalità", giocatore.nazionalita),
                         ("Specialità", self.mostraSpecialita(specialita))]

        testiDati = []
        for nome, valore in datiPersonali:
            testiDati.append(ft.Text(f"{nome}: {self.mostraNone(valore)}"))

        riquadroDati = ft.Container(content=ft.Column([ft.Text("Anagrafica", weight=ft.FontWeight.BOLD),
                                                       ft.Row(testiDati[0:2], spacing=30, alignment=ft.MainAxisAlignment.CENTER),
                                                       ft.Row(testiDati[2:4], spacing=30, alignment=ft.MainAxisAlignment.CENTER),
                                                       testiDati[4]],
                                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    border=ft.border.all(1, "grey"),
                                    border_radius=10,
                                    padding=15,
                                    height=150)

        # riquadro con le squadre in cui il giocatore ha giocato nella stagione e campionato scelti
        testiSquadre = [ft.Text("Squadre", weight=ft.FontWeight.BOLD)]
        for squadra in squadre:
            nomeSquadra = squadra["nome"]
            partite = squadra["partite"]
            punti = squadra["punti"]
            posizione = squadra["posizione"]
            girone = squadra["girone"]

            if girone is None:
                classifica = f"{posizione}° posto"
            else:
                classifica = f"{posizione}° posto, girone {girone}"
            testiSquadre.append(ft.Text(f"{nomeSquadra} ({classifica}): {partite} partite, {punti} punti"))

        riquadroSquadre = ft.Container(content=ft.Column(testiSquadre, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                       border=ft.border.all(1, "grey"),
                                       border_radius=10,
                                       padding=15,
                                       height=150)

        risultati.append(ft.Row([riquadroDati, riquadroSquadre],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.START))

        # tabella statistiche per partita

        medie = [("MIN", stat.minuti),
                 ("PT", stat.punti),
                 ("RO", stat.rimbalzi_offensivi),
                 ("RD", stat.rimbalzi_difensivi),
                 ("ASS", stat.assist),
                 ("PR", stat.palle_recuperate),
                 ("PP", stat.palle_perse),
                 ("STP", stat.stoppate),
                 ("VAL", stat.valutazione)]

        tiri = [("T2", stat.tiri2_segnati, stat.tiri2_tentati),
                ("T3", stat.tiri3_segnati, stat.tiri3_tentati),
                ("TL", stat.liberi_segnati, stat.liberi_tentati)]

        tabella = ft.DataTable(column_spacing=20)
        riga = ft.DataRow()

        for nome, totale in medie:
            media = stat.perPartita(totale)
            tabella.columns.append(ft.DataColumn(ft.Container(ft.Text(nome), width=45, alignment=ft.alignment.center)))
            riga.cells.append(ft.DataCell(ft.Container(ft.Text(f"{media:.2f}"), width=45, alignment=ft.alignment.center)))

        for nome, segnati, tentati in tiri:
            mediaSegnati = stat.perPartita(segnati)
            mediaTentati = stat.perPartita(tentati)
            percentuale = stat.percentuale(segnati, tentati)
            if percentuale is None:
                testoPercentuale = "-"
            else:
                testoPercentuale = f"{percentuale:.2f}%"
            tabella.columns.append(ft.DataColumn(ft.Container(ft.Text(nome), width=160, alignment=ft.alignment.center)))
            riga.cells.append(ft.DataCell(ft.Container(ft.Text(f"{mediaSegnati:.2f}/{mediaTentati:.2f} ({testoPercentuale})"),
                                                       width=160,
                                                       alignment=ft.alignment.center)))

        tabella.rows.append(riga)
        riquadroStatistiche = ft.Container(content=ft.Column([
            ft.Text("Statistiche per partita", weight=ft.FontWeight.BOLD), tabella],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
           border=ft.border.all(1, "grey"),
           border_radius=10,
           padding=15)
        risultati.append(ft.Row([riquadroStatistiche], alignment=ft.MainAxisAlignment.CENTER))

        self.update_page()

    def creaTabellaGiocatori(self, statisticheProfilo, scelto, giocatori):
        # nomi brevi delle statistiche per le intestazioni
        nomiColonne = {"punti": "PT",
                       "rimbalzi": "RIM",
                       "assist": "AST",
                       "tiri3_tentati": "T3 tentati",
                       "percentuale_tiri3": "% T3",
                       "liberi_tentati": "TL tentati",
                       "percentuale_liberi": "% TL",
                       "rapporto_assist": "AST/PP",
                       "palle_recuperate": "PR",
                       "stoppate": "STP",
                       "rimbalzi_offensivi": "RO",
                       "rimbalzi_difensivi": "RD",
                       "valutazione": "VAL"}

        tabella = ft.DataTable(column_spacing=20)

        # intestazioni
        tabella.columns.append(ft.DataColumn(ft.Container(ft.Text("N."), width=30, alignment=ft.alignment.center)))
        tabella.columns.append(ft.DataColumn(ft.Container(ft.Text("Giocatore"), width=200, alignment=ft.alignment.center)))
        tabella.columns.append(ft.DataColumn(ft.Container(ft.Text("Ruolo"), width=110, alignment=ft.alignment.center)))
        tabella.columns.append(ft.DataColumn(ft.Container(ft.Text("Squadra"), width=300, alignment=ft.alignment.center)))
        for nomeStatistica in statisticheProfilo:
            tabella.columns.append(ft.DataColumn(ft.Container(ft.Text(nomiColonne[nomeStatistica]), width=80, alignment=ft.alignment.center)))

        tabella.rows.append(self.creaRigaTabella("", scelto, statisticheProfilo, True))

        # una riga per ogni giocatore trovato, dal peso più basso
        numero = 1
        for dati in giocatori:
            tabella.rows.append(self.creaRigaTabella(f"{numero}", dati, statisticheProfilo, False))
            numero += 1

        return tabella

    def mostraSostituti(self, scelto, profilo, statisticheProfilo, sostituti):

        giocatore = scelto[0]
        if len(sostituti) == 0:
            testo = "Nessun giocatore simile trovato"
        elif len(sostituti) == 1:
            testo = "Trovato 1 giocatore simile"
        else:
            testo = f"Trovati {len(sostituti)} giocatori simili"

        contenuto = [ft.Text(f"Sostituti di {giocatore} - profilo {profilo}", weight=ft.FontWeight.BOLD),
                     ft.Text(testo)]
        if len(sostituti) > 0:
            contenuto.append(self.creaTabellaGiocatori(statisticheProfilo, scelto, sostituti))

        riquadroSostituti = ft.Container(content=ft.Column(contenuto,
                                                           horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                         border=ft.border.all(1, "grey"),
                                         border_radius=10,
                                         padding=15)

        self.txtResultsGiocatore.controls.append(ft.Row([riquadroSostituti], alignment=ft.MainAxisAlignment.CENTER))
        self.update_page()

    def mostraMigliori(self, scelto, profilo, statisticheProfilo, migliori, nPeggiori):

        giocatore = scelto[0]
        if len(migliori) == 0:
            testoMigliori = f"Nessun giocatore è migliore di {giocatore} nel profilo {profilo}, è tra i migliori del suo ruolo"
        elif len(migliori) == 1:
            testoMigliori = "Trovato 1 giocatore migliore"
        else:
            testoMigliori = f"Trovati {len(migliori)} giocatori migliori"

        if nPeggiori == 0:
            testoPeggiori = f"{giocatore} non è migliore di nessun giocatore"
        elif nPeggiori == 1:
            testoPeggiori = f"{giocatore} è migliore di 1 giocatore"
        else:
            testoPeggiori = f"{giocatore} è migliore di {nPeggiori} giocatori"

        contenuto = [ft.Text(f"Giocatori migliori di {giocatore} - profilo {profilo}", weight=ft.FontWeight.BOLD),
                     ft.Text(testoMigliori),
                     ft.Text(testoPeggiori)]

        if len(migliori) > 0:
            contenuto.append(self.creaTabellaGiocatori(statisticheProfilo, scelto, migliori))

        riquadroMigliori = ft.Container(content=ft.Column(contenuto,
                                                          horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        border=ft.border.all(1, "grey"),
                                        border_radius=10,
                                        padding=15)

        self.txtResultsGiocatore.controls.append(ft.Row([riquadroMigliori], alignment=ft.MainAxisAlignment.CENTER))
        self.update_page()

    def creaRigaTabella(self, numero, dati, statisticheProfilo, grassetto):
        giocatore, peso, valori, squadre = dati

        celle = [(numero, 30), (f"{giocatore}", 200), (giocatore.ruolo, 110), (squadre, 300)]

        for i in range(len(statisticheProfilo)):
            if statisticheProfilo[i].startswith("percentuale"):
                celle.append((f"{valori[i]:.2f}%", 80))
            else:
                celle.append((f"{valori[i]:.2f}", 80))

        if grassetto:
            stile = ft.FontWeight.BOLD
        else:
            stile = ft.FontWeight.NORMAL

        riga = ft.DataRow()
        for testo, larghezza in celle:
            riga.cells.append(ft.DataCell(ft.Container(ft.Text(testo, weight=stile),
                                                       width=larghezza,
                                                       alignment=ft.alignment.center)))
        return riga

    def mostraListaDesideri(self, listaDesideri):
        if len(listaDesideri) == 0:
            testo = "Nessun giocatore nella lista: si aggiungono dalla scheda Giocatore"
        else:
            testo = f"Giocatori nella lista: {len(listaDesideri)}"

        contenuto = [ft.Text("Lista dei desideri", weight=ft.FontWeight.BOLD),
                     ft.Text(testo)]
        if len(listaDesideri) > 0:
            contenuto.append(self.creaTabellaLista(listaDesideri))

        riquadroLista = ft.Container(content=ft.Column(contenuto,
                                                       horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                     border=ft.border.all(1, "grey"),
                                     border_radius=10,
                                     padding=15)

        self.txtResultsLista.controls.clear()
        self.txtResultsLista.controls.append(ft.Row([riquadroLista], alignment=ft.MainAxisAlignment.CENTER))
        self.update_page()

    def creaTabellaLista(self, listaDesideri):
        tabella = ft.DataTable(column_spacing=15)

        colonne = [("Giocatore", 200), ("Ruolo", 110), ("Età", 40), ("Naz.", 70),
                   ("Campionato e stagione", 180),
                   ("PT", 50), ("RIM", 50), ("ASS", 50), ("VAL", 50),
                   ("Punteggio", 80),
                   ("Specialità", 300), ("", 40)]

        for nome, larghezza in colonne:
            tabella.columns.append(ft.DataColumn(ft.Container(ft.Text(nome), width=larghezza, alignment=ft.alignment.center)))

        for giocatore in listaDesideri:
            stagione, campionato, stat, specialita, punteggioRuolo = listaDesideri[giocatore]

            celle = [(f"{giocatore}", 200),
                     (f"{self.mostraNone(giocatore.ruolo)}", 110),
                     (f"{self.mostraNone(giocatore.getEta())}", 40),
                     (f"{self.mostraNone(giocatore.nazionalita)}", 70),
                     (f"{campionato} {stagione}", 180)]

            # medie per partita
            totali = [stat.punti,
                      stat.rimbalzi_offensivi + stat.rimbalzi_difensivi,
                      stat.assist,
                      stat.valutazione]
            for totale in totali:
                media = stat.perPartita(totale)
                celle.append((f"{media:.2f}", 50))

            # punteggio nel ruolo
            if punteggioRuolo is None:
                celle.append(("n.d.", 80))
            else:
                celle.append((f"{punteggioRuolo:.1f}", 80))

            celle.append((self.mostraSpecialita(specialita), 300))

            riga = ft.DataRow()
            for testo, larghezza in celle:
                riga.cells.append(ft.DataCell(ft.Container(ft.Text(testo), width=larghezza, alignment=ft.alignment.center)))

            btnRimuovi = ft.IconButton(icon=ft.icons.DELETE,
                                       icon_color="red",
                                       tooltip="Rimuovi dalla lista",
                                       data=giocatore,
                                       on_click=self._controller.handleRimuoviLista)
            riga.cells.append(ft.DataCell(ft.Container(btnRimuovi, width=40, alignment=ft.alignment.center)))

            tabella.rows.append(riga)

        return tabella

    def mostraQuintetto(self, tipoQuintetto, quintetto, ruoli, sommaPunteggi, esclusi, listaDesideri):
        contenuto = [ft.Text(f"Quintetto migliore - {tipoQuintetto}", weight=ft.FontWeight.BOLD)]

        if len(quintetto) == 0:
            contenuto.append(ft.Text("Nessun quintetto rispetta le condizioni"))
        else:
            media = sommaPunteggi / len(quintetto)
            contenuto.append(ft.Text(f"Punteggio medio nel ruolo: {media:.1f}"))
            contenuto.append(self.creaTabellaQuintetto(quintetto, ruoli, listaDesideri))

        # giocatori della lista scartati prima della ricorsione
        if len(esclusi) > 0:
            contenuto.append(ft.Text("Esclusi dalla simulazione:"))
            for giocatore, motivo in esclusi:
                contenuto.append(ft.Text(f"{giocatore}: {motivo}"))

        riquadroQuintetto = ft.Container(content=ft.Column(contenuto,
                                                           horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                         border=ft.border.all(1, "grey"),
                                         border_radius=10,
                                         padding=15)

        # sopra la lista dei desideri, così si vede senza scorrere
        self.txtResultsLista.controls.insert(0, ft.Row([riquadroQuintetto], alignment=ft.MainAxisAlignment.CENTER))
        self.update_page()

    def creaTabellaQuintetto(self, quintetto, ruoli, listaDesideri):
        tabella = ft.DataTable(column_spacing=20)

        colonne = [("Gioca da", 90), ("Giocatore", 200), ("Ruolo", 110), ("Naz.", 70),
                   ("Campionato e stagione", 180), ("VAL", 50), ("Punteggio", 80), ("Specialità", 300)]
        for nome, larghezza in colonne:
            tabella.columns.append(ft.DataColumn(ft.Container(ft.Text(nome), width=larghezza, alignment=ft.alignment.center)))

        for i in range(len(quintetto)):
            giocatore = quintetto[i]
            stagione, campionato, stat, specialita, punteggioRuolo = listaDesideri[giocatore]
            valutazione = stat.perPartita(stat.valutazione)

            celle = [(ruoli[i], 90),
                     (f"{giocatore}", 200),
                     (giocatore.ruolo, 110),
                     (f"{self.mostraNone(giocatore.nazionalita)}", 70),
                     (f"{campionato} {stagione}", 180),
                     (f"{valutazione:.2f}", 50),
                     (f"{punteggioRuolo:.1f}", 80),
                     (self.mostraSpecialita(specialita), 300)]

            riga = ft.DataRow()
            for testo, larghezza in celle:
                riga.cells.append(ft.DataCell(ft.Container(ft.Text(testo), width=larghezza, alignment=ft.alignment.center)))
            tabella.rows.append(riga)

        return tabella

    def mostraRicerca(self, risultati):
        if len(risultati) == 0:
            testo = "Nessun giocatore rispetta i filtri"
        elif len(risultati) == 1:
            testo = "Trovato 1 giocatore"
        else:
            testo = f"Trovati {len(risultati)} giocatori"

        contenuto = [ft.Text("Risultati della ricerca", weight=ft.FontWeight.BOLD),
                     ft.Text(testo)]
        if len(risultati) > 0:
            contenuto.append(self.creaTabellaRicerca(risultati))

        riquadroRicerca = ft.Container(content=ft.Column(contenuto,
                                                         horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                       border=ft.border.all(1, "grey"),
                                       border_radius=10,
                                       padding=15)

        self.txtResultsRicerca.controls.clear()
        self.txtResultsRicerca.controls.append(ft.Row([riquadroRicerca], alignment=ft.MainAxisAlignment.CENTER))
        self.update_page()

    def creaTabellaRicerca(self, risultati):
        tabella = ft.DataTable(column_spacing=15)

        colonne = [("Giocatore", 200), ("Ruolo", 110), ("Età", 40), ("Naz.", 70),
                   ("Squadra", 220),
                   ("PT", 50), ("RIM", 50), ("ASS", 50), ("VAL", 50),
                   ("Punteggio", 80),
                   ("Specialità", 260), ("", 40)]

        for nome, larghezza in colonne:
            tabella.columns.append(ft.DataColumn(ft.Container(ft.Text(nome), width=larghezza, alignment=ft.alignment.center)))

        for giocatore, stat, specialita, punteggioRuolo, squadre in risultati:
            celle = [(f"{giocatore}", 200),
                     (giocatore.ruolo, 110),
                     (f"{self.mostraNone(giocatore.getEta())}", 40),
                     (f"{self.mostraNone(giocatore.nazionalita)}", 70),
                     (squadre, 220)]

            # medie per partita
            totali = [stat.punti,
                      stat.rimbalzi_offensivi + stat.rimbalzi_difensivi,
                      stat.assist,
                      stat.valutazione]
            for totale in totali:
                media = stat.perPartita(totale)
                celle.append((f"{media:.2f}", 50))

            celle.append((f"{punteggioRuolo:.1f}", 80))
            celle.append((self.mostraSpecialita(specialita), 260))

            riga = ft.DataRow()
            for testo, larghezza in celle:
                riga.cells.append(ft.DataCell(ft.Container(ft.Text(testo), width=larghezza, alignment=ft.alignment.center)))

            btnAggiungi = ft.IconButton(icon=ft.icons.ADD,
                                        icon_color="green",
                                        tooltip="Aggiungi alla lista",
                                        data=giocatore,
                                        on_click=self._controller.handleAggiungiDaRicerca)
            riga.cells.append(ft.DataCell(ft.Container(btnAggiungi, width=40, alignment=ft.alignment.center)))

            tabella.rows.append(riga)

        return tabella


    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()