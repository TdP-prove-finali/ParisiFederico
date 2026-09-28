-- Database scouting basket
-- ATTENZIONE: la prima riga cancella il database e tutti i dati

DROP DATABASE IF EXISTS scouting_basket;
CREATE DATABASE scouting_basket CHARACTER SET utf8mb4;
USE scouting_basket;

CREATE TABLE stagione (
    id_stagione     INT AUTO_INCREMENT PRIMARY KEY,
    anno_inizio     INT NOT NULL UNIQUE          -- 2024 = stagione 2024/2025
);

CREATE TABLE campionato (
    id_campionato   INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(50) NOT NULL,
    livello         INT NOT NULL                 -- 3 = B Naz, 4 = B Interreg, 5 = C
);

CREATE TABLE squadra (
    id_squadra      INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    id_lnp          INT NULL UNIQUE,             -- codice squadra sul sito LNP
    id_playbasket   VARCHAR(20) NULL UNIQUE      -- codice squadra su playbasket
);

CREATE TABLE partecipazione_squadra (
    id_partecipazione   INT AUTO_INCREMENT PRIMARY KEY,
    id_squadra          INT NOT NULL,
    id_stagione         INT NOT NULL,
    id_campionato       INT NOT NULL,
    girone              VARCHAR(50) NULL,
    UNIQUE (id_squadra, id_stagione, id_campionato),
    FOREIGN KEY (id_squadra)    REFERENCES squadra(id_squadra),
    FOREIGN KEY (id_stagione)   REFERENCES stagione(id_stagione),
    FOREIGN KEY (id_campionato) REFERENCES campionato(id_campionato)
);

CREATE TABLE giocatore (
    id_giocatore    INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(60) NOT NULL,
    cognome         VARCHAR(60) NOT NULL,
    data_nascita    DATE NULL,
    nazionalita     VARCHAR(3) NULL,
    altezza_cm      INT NULL,
    ruolo           VARCHAR(30) NULL,
    slug_lnp        VARCHAR(120) NULL UNIQUE,    -- fine dell'URL LNP, es. stankevicius-eimantas
    id_playbasket   VARCHAR(20) NULL UNIQUE      -- codice giocatore su playbasket
);

-- Solo totali: medie e percentuali si calcolano.
-- Per i campionati presi da playbasket molte colonne resteranno NULL.
CREATE TABLE statistica_stagionale (
    id_statistica       INT AUTO_INCREMENT PRIMARY KEY,
    id_giocatore        INT NOT NULL,
    id_partecipazione   INT NOT NULL,
    partite             INT NOT NULL,
    partite_titolare    INT NULL,
    minuti              INT NULL,
    punti               INT NULL,
    tiri2_segnati       INT NULL,
    tiri2_tentati       INT NULL,
    tiri3_segnati       INT NULL,
    tiri3_tentati       INT NULL,
    liberi_segnati      INT NULL,
    liberi_tentati      INT NULL,
    rimbalzi_offensivi  INT NULL,
    rimbalzi_difensivi  INT NULL,
    assist              INT NULL,
    palle_recuperate    INT NULL,
    palle_perse         INT NULL,
    stoppate            INT NULL,
    falli               INT NULL,
    valutazione         INT NULL,
    UNIQUE (id_giocatore, id_partecipazione),
    FOREIGN KEY (id_giocatore)      REFERENCES giocatore(id_giocatore),
    FOREIGN KEY (id_partecipazione) REFERENCES partecipazione_squadra(id_partecipazione)
);

INSERT INTO campionato (nome, livello) VALUES
    ('Serie B Nazionale', 3),
    ('Serie B Interregionale', 4),
    ('Serie C', 5);
