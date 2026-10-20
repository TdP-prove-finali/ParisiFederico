from dataclasses import dataclass


@dataclass
class StatisticaStagionale:
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