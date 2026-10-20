from dataclasses import dataclass

@dataclass
class Stagione:
    id_stagione: int
    anno_inizio: int

    def __hash__(self):
        return hash(self.id_stagione)

    def __eq__(self, other):
        return self.id_stagione == other.id_stagione

    def __str__(self):
        return f"{str(self.anno_inizio)[2:]}/{str(self.anno_inizio + 1)[2:]}"
