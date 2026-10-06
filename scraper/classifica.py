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
    nomiSquadreExcel = pd.read_excel("SquadreBNazionale.xlsx")["NOME"].tolist()

    for girone in ["A", "B"]:
        squadre = leggiClassifica("pagine/classificaSerieBGirone" + girone + ".html", girone)
        print("Girone", girone)
        for squadra in squadre:
            print(squadra)
            if squadra["nome"].upper() not in nomiSquadreExcel:
                print("Attenzione: squadra non trovata nel file Excel")