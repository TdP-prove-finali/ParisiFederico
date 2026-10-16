import pandas as pd

giocatori = pd.read_csv("csv_completo/giocatori.csv")

# anno scritto senza secolo sul sito (0093 invece di 1993): si aggiunge "19"
sbagliate = giocatori["data_nascita"] < "1900-01-01"
giocatori.loc[sbagliate, "data_nascita"] = "19" + giocatori.loc[sbagliate, "data_nascita"].str[2:]
print(giocatori[sbagliate][["nome", "cognome", "data_nascita"]])

giocatori.to_csv("csv_completo/giocatori.csv", index=False)