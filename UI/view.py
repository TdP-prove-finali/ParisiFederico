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

        self._title = ft.Text("Scouting basket 2026", color="blue", size=24)

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
        self._btnTrovaSostituto = ft.ElevatedButton(text="Trova sostituto",
                                                    on_click=self._controller.handleTrovaSostituto)
        self._btnTrovaMigliore = ft.ElevatedButton(text="Trova migliore",
                                                   on_click=self._controller.handleTrovaMigliore)

        rowProfilo = ft.Row([ft.Container(self._ddProfilo, width=250),
                             ft.Container(self._btnTrovaSostituto, width=250),
                             ft.Container(self._btnTrovaMigliore, width=250)],
                            alignment=ft.MainAxisAlignment.CENTER)

        self.txtResultsGiocatore = ft.ListView(expand=1, spacing=10, padding=20)

        schedaGiocatore = ft.Column([ft.Container(height=10), rowCerca, rowProfilo,
                                     self.txtResultsGiocatore],
                                    spacing=20)

        # schede
        self._tabs = ft.Tabs(selected_index=0,
                             tabs=[ft.Tab(text="Giocatore", content=schedaGiocatore)],
                             expand=1,
                             tab_alignment= ft.TabAlignment.CENTER)

        self._page.add(self._title, self._rowDati, self._txtMessaggio, self._tabs)
        self._page.update()

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