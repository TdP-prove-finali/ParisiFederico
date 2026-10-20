from dataclasses import dataclass


@dataclass
class Campionato:
    id_campionato: int
    nome: str
    livello: int

    def __hash__(self):
        return hash(self.id_campionato)

    def __eq__(self, other):
        return self.id_campionato == other.id_campionato

    def __str__(self):
        return f"{self.nome}"

