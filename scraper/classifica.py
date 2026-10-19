import pandas as pd

def leggiClassifica(percorsoFile, girone):

    """
    Legge la classifica di un girone, restituisce una
    lista di dizionari, uno per squadra
    """

    # la prima tabella contiene solo l'intestazione, i dati sono nella seconda
    classifica = pd.read_html(percorsoFile, encoding="utf-8")[1]

    tabella = classifica.values.tolist()

    squadre = []
    for i in range(len(tabella)):
        riga = tabella[i]
        squadre.append({
            "nome": riga[0],
            "girone": girone,
            "posizione": i + 1,
            "vittorie": int(riga[3]),
            "sconfitte": int(riga[4]),
            "punti_fatti": int(riga[6]),
            "punti_subiti": int(riga[7]),
        })
    return squadre


if __name__ == "__main__":
    fileProva = [("classificaA2_2526.html", None), ("classificaA2_2425.html", None),
                 ("classificaB_2526_GironeA.html", "A"), ("classificaB_2526_GironeB.html", "B"),
                 ("classificaB_2425_GironeA.html", "A"), ("classificaB_2425_GironeB.html", "B")]

    for nomeFile, girone in fileProva:
        squadre = leggiClassifica("pagine/" + nomeFile, girone)
        print(f"{nomeFile} (girone {girone}): {len(squadre)} squadre")
        for squadra in squadre:
            print(f"{squadra['posizione']} {squadra['nome']} V: {squadra['vittorie']} P: {squadra['sconfitte']}")