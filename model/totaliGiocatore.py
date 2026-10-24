from dataclasses import dataclass
from datetime import date


@dataclass
class TotaliGiocatore:
    # totali di un giocatore in una stagione e in un campionato:
    # se ha cambiato squadra nello stesso campionato, le sue righe sono sommate
    id_giocatore: int
    partite: int
    minuti: int
    punti: int
    tiri2_segnati: int
    tiri2_tentati: int
    tiri3_segnati: int
    tiri3_tentati: int
    liberi_segnati: int
    liberi_tentati: int
    rimbalzi_offensivi: int
    rimbalzi_difensivi: int
    assist: int
    palle_recuperate: int
    palle_perse: int
    stoppate: int
    stoppate_subite: int
    falli: int
    falli_subiti: int
    valutazione: int

    def __hash__(self):
        return hash(self.id_giocatore)

    def __eq__(self, other):
        return self.id_giocatore == other.id_giocatore

    def perPartita(self, valore):
        return valore / self.partite # nel database sono presenti solo giocatori con almeno una partita

    def percentuale(self, segnati, tentati):
        if tentati == 0:
            return None
        return segnati / tentati * 100




