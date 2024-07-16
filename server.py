from socket import *
import threading
from collections import deque

# Create TCP/IP Socket
sock = socket(AF_INET, SOCK_STREAM)

# Get Address of server
hostname = gethostname()
hostIP = gethostbyname(hostname)
port = 10000
serverAddress = (hostIP, port)

# Bind the server and listen for connections
sock.bind(serverAddress)
sock.listen(20)  # Can handle up to 20 pending connections
print(f"Server started at {hostIP}:{port}")
print("Finding Opponent...")

matchQueue = deque()

def play(player1, player2):
    # Spaces already guessed
    p1_used = set()
    p2_used = set()

    counter = 0
    hasLost = "No"
    while hasLost == "No":
        if counter % 2 == 0:
            current_player, other_player = player1, player2
            current_used = p1_used
        else:
            current_player, other_player = player2, player1
            current_used = p2_used

        if counter > 1:
            current_player[0].sendall(isHit.encode())

        if counter > 0:
            current_player[0].sendall(space.encode())
            isHit = current_player[0].recv(128).decode()

        hasLost = current_player[0].recv(128).decode()
        if hasLost == "Yes":
            other_player[0].sendall("lost".encode())
            break   

        # Ask player where they choose to hit
        current_player[0].sendall("Where will you hit: ".encode())
        space = current_player[0].recv(128).decode()

        # Check if already guessed
        while space in current_used:
            current_player[0].sendall("Already hit, try again: ".encode())
            space = current_player[0].recv(128).decode()

        current_used.add(space)
        current_player[0].sendall("Sound".encode())
        
        counter += 1

    return player1 if current_player == player1 else player2, player2 if current_player == player1 else player1

def handle_client(player1, player2):
    print(f"Starting game between {player1[1]} and {player2[1]}")
    try:
        # Match confirmation
        player1[0].sendall("Matched with an opponent. Game starting...".encode())
        player2[0].sendall("Matched with an opponent. Game starting...".encode())
        player1[0].sendall("p1".encode())
        player1[0].recv(128)
        player2[0].sendall("p2".encode())
        player2[0].recv(128)

        # Play the game
        loser, winner = play(player1, player2)
        winner[0].sendall("You Win!".encode())
        loser[0].sendall("You Lose.".encode())

    except Exception as e:
        print(f"Error during game session: {e}")
    finally:
        player1[0].close()
        player2[0].close()

def match_players():
    while True:
        if len(matchQueue) >= 2:
            player1 = matchQueue.popleft()
            player2 = matchQueue.popleft()
            threading.Thread(target=handle_client, args=(player1, player2)).start()

threading.Thread(target=match_players).start()

while True:
    try:
        connection, clientAddress = sock.accept()
        print(f"Connection from {clientAddress}")
        matchQueue.append((connection, clientAddress))
    except KeyboardInterrupt:
        print("Server is shutting down.")
        sock.close()
        break
