from dataclasses import dataclass
from datetime import date


@dataclass
class Giocatore:
    id_giocatore: int
    nome: str
    cognome: str
    data_nascita: date
    nazionalita: str
    altezza_cm: int
    ruolo: str
    slug_lnp: str

    def __hash__(self):
        return hash(self.id_giocatore)

    def __eq__(self, other):
        return self.id_giocatore == other.id_giocatore

    def __str__(self):
        return f"{self.cognome} {self.nome}"

    def getEta(self):
        if self.data_nascita is None:
            return None
        oggi = date.today()
        eta = oggi.year - self.data_nascita.year
        if oggi.month < self.data_nascita.month:
            eta = eta - 1
        elif oggi.month == self.data_nascita.month and oggi.day < self.data_nascita.day:
            eta = eta - 1
        return eta


