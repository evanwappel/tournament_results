# PROJECT DESCRIPTION: Tournament Planner

In this project, there is a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

This project has two parts: defining the database schema (SQL table definitions), and writing the code that will use it.

The goal of the Swiss pairings system is to pair each player with an opponent who has won the same number of matches, or as close as possible.

More info on the Swiss-system tournament can be found here:
http://en.wikipedia.org/wiki/Swiss-system_tournament



## INSTRUCTIONS ON HOW TO USE THIS PROJECT:

Install Vagrant and VirtualBox
- Clone the fullstack-nanodegree-vm repository
- Launch the Vagrant VM
- Navigate to the fullstack\tournament folder
- Type `psql` to get into PostgreSQL
- Type `\i tournament.sql` to connect to the database and populate example rows to work with
- The Python functions for filling out a template of an API are in the file "tournament.py"
- The code is verified using a test suite called "tournament_test.py"



### FUNCTIONS in tournament.py

#### registerPlayer(name)
Adds a player to the tournament by putting an entry in the database. The database should assign an ID number to the player. Different players may have the same names but will receive different ID numbers.

#### countPlayers()
Returns the number of currently registered players. This function should not use the Python len() function; it should have the database count the players.

#### deletePlayers()
Clear out all the player records from the database.

#### reportMatch(winner, loser)
Stores the outcome of a single match between two players in the database.

#### deleteMatches()
Clear out all the match records from the database.

#### playerStandings()
Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.

#### swissPairings()
Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. For instance, if there are eight registered players, this function should return four pairings. This function should use playerStandings to find the ranking of players.
