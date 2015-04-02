-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--
-- To run this in psql, type:
-- \i tournament.sql
--
\c tournament

DROP table player_list;

CREATE TABLE player_list (
    player_name     varchar,
    total_wins      int,
    total_matches   int,
    player_id       serial
);
INSERT INTO player_list VALUES ('Reggie Watts','5','5');
INSERT INTO player_list VALUES ('Sting','10','10');
INSERT INTO player_list VALUES ('Neil Young','0','7');
INSERT INTO player_list VALUES ('Robert Smith','1','1');
INSERT INTO player_list VALUES ('Mark Knopfler','0','8');
INSERT INTO player_list VALUES ('Steve Winwood','0','1');
INSERT INTO player_list VALUES ('Eric Clapton','0','3');
INSERT INTO player_list VALUES ('Charlie Watts','4','4');
INSERT INTO player_list VALUES ('John Lennon','1','1');
INSERT INTO player_list VALUES ('Jimi Hendrix','1','4');
INSERT INTO player_list VALUES ('Robert Johnson','1','1');
INSERT INTO player_list VALUES ('Eddie Van Halen','1','2');
INSERT INTO player_list VALUES ('Muddy Waters','0','5');
INSERT INTO player_list VALUES ('Stevie Wonder','3','4');
INSERT INTO player_list VALUES ('Mick Jagger','0','0');
INSERT INTO player_list VALUES ('Keith Richards','0','1');

SELECT * FROM player_list;
