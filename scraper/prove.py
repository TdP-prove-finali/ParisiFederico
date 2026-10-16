import pandas as pd

cartellaCsv = "csv_completo/"

# giocatori con due pagine (e due slug) sul sito LNP:
# si tiene lo slug scritto correttamente e si toglie l'altro
slugDoppi = [
    "forti-franesco",         # doppione di forti-francesco
    "wojciechowksi-jakub",    # doppione di wojciechowski-jakub
    "dimeco-manuel",          # doppione di di-meco-manuel
    "dellagnello-giacomo-0",  # doppione di dell-agnello-giacomo
    "krisjanis-mazburss",     # doppione di mazburss-krisjanis
]

giocatori = pd.read_csv(cartellaCsv + "giocatori.csv")
statistiche = pd.read_csv(cartellaCsv + "statistiche.csv")

print(f"Prima: giocatori {len(giocatori)}, statistiche {len(statistiche)}")

# alcune nazionalità sono scritte in minuscolo (ita, alb)
giocatori["nazionalita"] = giocatori["nazionalita"].str.upper()

# tolgo le righe dei doppioni da entrambi i file
giocatori = giocatori[~giocatori["slug_lnp"].isin(slugDoppi)]
statistiche = statistiche[~statistiche["slug_lnp"].isin(slugDoppi)]

giocatori.to_csv(cartellaCsv + "giocatori.csv", index=False)
statistiche.to_csv(cartellaCsv + "statistiche.csv", index=False)

print(f"Dopo: giocatori {len(giocatori)}, statistiche {len(statistiche)}")