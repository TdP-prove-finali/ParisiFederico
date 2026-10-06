import pandas as pd

pd.set_option("display.max_columns", None)
tabelle = pd.read_html("pagine/classificaSerieBGironeB.html", encoding="utf-8")
print(len(tabelle))
print(tabelle[1])