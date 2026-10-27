from dataclasses import dataclass


@dataclass
class Partecipazione:
    id_partecipazione: int
    nome: str
    girone: str
    posizione: int
    vittorie: int
    sconfitte: int
    punti_fatti: int
    punti_subiti: int

    def __hash__(self):
        return hash(self.id_partecipazione)

    def __eq__(self, other):
        return self.id_partecipazione == other.id_partecipazione

    def __str__(self):
        return self.nome