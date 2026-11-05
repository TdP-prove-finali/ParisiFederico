SCOUTING BASKET - Serie A2 e B Nazionale
Federico Parisi (s314176) - Prova finale di Tecniche di Programmazione

Applicazione di scouting e analisi per i Dirigenti Sportivi dei campionati di
pallacanestro Serie A2 e Serie B Nazionale (stagioni 2024/25 e 2025/26).

Video dimostrativo: (link da aggiungere)

ISTRUZIONI PER L'UTILIZZO
1. Fare il fork del progetto al seguente link: https://github.com/TdP-prove-finali/ParisiFederico
2. Installare le librerie con: pip install -r requirements.txt
3. Creare il database eseguendo in MariaDB lo script database/scoutingBasket_completo.sql: contiene sia la struttura delle tabelle sia i dati raccolti.
4. Inserire i propri dati di accesso a MariaDB nel file database/connector.cnf
5. Eseguire main.py

PROVA
- Scegliere la stagione 25/26 e la Serie B Nazionale e premere "Carica giocatori": 516 giocatori
- Scheda Ricerca: ruolo Play, specialità Passatore, "Cerca": 24 giocatori
- Scheda Giocatore: Cappelletti Carlo con il profilo Passatore: "Trova sostituto" trova 13 giocatori, "Trova migliore" 54

LICENZE
- Software: Apache License 2.0 (file Apache License)
- Relazione tecnica: Creative Commons BY-NC-SA 4.0 (cartella documenti)