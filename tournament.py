#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("UPDATE player_list SET total_wins = 0, total_matches = 0;")
    conn.commit()
    cur.close()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("DELETE FROM player_list;")
    conn.commit()
    cur.close()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(player_name) FROM player_list;")
    row = cur.fetchone()
    c = row[0]
    return c
    cur.close()
    conn.close()

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # if player count = 0, reset the primary key sequence:
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(player_name) FROM player_list;")
    row = cur.fetchone()
    c = row[0]
    if c==0:
        cur.execute("ALTER SEQUENCE player_list_player_id_seq RESTART WITH 1;")

    # add player
    cur.execute("""INSERT INTO player_list (player_name, total_wins, total_matches) VALUES (%s, %s, %s);""", (name, 0, 0))

    conn.commit()
    cur.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    cur.execute("SELECT player_id, player_name, total_wins, total_matches FROM player_list ORDER BY total_wins DESC;")
    standings = cur.fetchall()
    return standings
    conn.commit()
    cur.close()
    conn.close()



def reportMatch(winner, loser):
    # winner = 1
    # loser = 2
    #reportMatch(id1, id2)
    #reportMatch(id3, id4)

    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()

    # get the latest standings:
    cur.execute("SELECT player_id, player_name, total_wins, total_matches FROM player_list ORDER BY player_id;")
    standings_before_match = cur.fetchall()


    winner_current_wins = standings_before_match[winner-1][2]
    #print "winner_current_wins = ", winner_current_wins
    winner_adjusted_wins = winner_current_wins + 1
    #print "winner_adjusted_wins = ", winner_adjusted_wins

    winner_current_matches = standings_before_match[winner-1][3]
    #print "winner_current_matches = ", winner_current_matches
    winner_adjusted_matches = winner_current_matches + 1
    #print "winner_adjusted_matches = ", winner_adjusted_matches

    loser_current_matches = standings_before_match[loser-1][3]
    #print "loser_current_matches = ", loser_current_matches
    loser_adjusted_matches = loser_current_matches + 1
    #print "loser_adjusted_matches = ", loser_adjusted_matches

    cur.execute("UPDATE player_list SET total_wins = %s WHERE player_id = %s",(winner_adjusted_wins, winner))
    cur.execute("UPDATE player_list SET total_matches = %s WHERE player_id = %s", (winner_adjusted_matches, winner))
    cur.execute("UPDATE player_list SET total_matches = %s WHERE player_id = %s", (loser_adjusted_matches, loser))
    conn.commit()

    cur.execute("SELECT player_id, player_name, total_wins, total_matches FROM player_list ORDER BY player_id;")
    standings_after_match = cur.fetchall()
    #print "\nstandings_after_match: ", standings_after_match

    cur.execute("SELECT player_id, player_name, total_wins, total_matches FROM player_list ORDER BY player_id;")
    standings = cur.fetchall()
    #print "\ncheck standings variable: ", standings
    return standings_after_match


    cur.close()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()

    # get the latest standings sorted by wins descending:
    cur.execute("SELECT player_id, player_name, total_wins, total_matches FROM player_list ORDER BY total_wins DESC;")
    standings_after = cur.fetchall()
    #print "\nstandings going into swiss pairings = ", standings_after
    #return standings_after

    #1st tuple: (1,twilight sparkle, 3 applejack)
    #2nd tuple: (2, fluttershy, 4, pinkie pie)
    #3rd tuple: ()
    #4th tuple: ()...

    #count rows:
    cur.execute("SELECT COUNT(player_id) FROM player_list;")
    row_count = cur.fetchall()
    #print "\nstandings_row_count = ", row_count[0][0]

    #count_rows type
    #print "\nrow_count type = ", type(row_count[0][0])

    #loop 1 to (row_count/2) times to assign tuples
    test_list = [0]
    #print "\ntest_list start= ", test_list
    for x in range(0, row_count[0][0],2):
        #print x
        #print x, "id=", standings_after[x][0], "name=", standings_after[x][1], "wins=", standings_after[x][2]
        #print "tuple#", (x+1), "=(", standings_after[x][0], standings_after[x][1], standings_after[x+1][0], standings_after[x+1][1],")"
        test_tuple = standings_after[x][0], standings_after[x][1], standings_after[x+1][0], standings_after[x+1][1]
        #print "\ntest_tuple= ", test_tuple

        test_list.append(test_tuple)
        #print "\ntest_list= ", test_list

    test_list.remove(0)
    #print "\ntest_list end= ", test_list

    return test_list


    cur.close()
    conn.close()
