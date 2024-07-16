# CMDBattleship
Command Prompt BattleShip
Play Battleship using the command prompt/terminal.

Made entirely using Python. Uses network sockets via a TCP connection to play a client-server version of the game battleship.
A queue is implemented that holds players waiting for at least 2 connections (done via threading). When 2 players are in the queue, they are connected to eachother via the server.
The players then setup their boards using user input and once both players have setup their board, the game begins.
Keep guessing spaces on the users board until all ships have been sunk.
Once all of a players ships have been sunk, the player with remaining ships wins the game!
