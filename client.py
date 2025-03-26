from socket import *
import sys
from utils import GameSetup
from time import sleep

if len(sys.argv) != 3:
    print("(-) Usage: python <path> <ip> <port>")
    print("Example: python client.py 127.0.0.1 10000")
    sys.exit(-1)

# Cast port to integer
try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
except ValueError:
    print("(-) Port must be an integer.")
    sys.exit(-1)

# Create TCP/IP socket
sock = socket(AF_INET, SOCK_STREAM)
server_address = (ip, port)

# Connect to the server
print(f'Connecting to server at {server_address[0]} port {server_address[1]}')
sock.connect(server_address)

while True:
    try:
        # Receive a message from server after connecting to confirm opponent
        message = sock.recv(128).decode()
        print(message)

        # Setup the game
        g = GameSetup()
        g.create_board()
        g.place_ships()

        # Let server know you are ready
        print("Waiting for opponent...")
        num = sock.recv(128).decode()  # player number, necessary for later
        sock.sendall("ACK".encode())

        # Playing the game        
        hits = set()    # hits you've taken
        misses = set()  # misses you've received
        flag = False
        hitRes = None

        while len(hits) < 17:

            if flag:
                ans = sock.recv(128).decode()
                print(ans)
                g.update_hits(space, ans)

            if flag or num == "p2":
                # Check for a hit
                toCheck = sock.recv(128).decode()
                if toCheck == "lost":
                    break

                isHit = g.check_board(toCheck)
                if isHit:
                    hitRes = "HIT"
                    hits.add(toCheck)
                    sleep(0.2)
                else:
                    hitRes = "MISS"
                    misses.add(toCheck)
                    sleep(0.2)

            if hitRes:
                sock.sendall(hitRes.encode())

            if len(hits) < 17:
                sock.sendall("No".encode())
            else:
                sock.sendall("Yes".encode())
                break

            question = sock.recv(128).decode()  # Where will you hit
            print("<-- Opponents Board -->")
            g.print_hits()

            space = input(question).upper()
            sock.sendall(space.encode())

            # Choose a spot to hit on other player
            res = sock.recv(128).decode()  # Sound or Try Again
            while res == "Already hit, try again: ":
                space = input(question).upper()
                while len(space) != 2:
                    print("(-) Invalid input. Try Again")
                    space = input(question).upper()
                
                sock.sendall(space.encode())
                res = sock.recv(128).decode()  # Sound or Try Again
            flag = True

        # Print the results
        result = sock.recv(128).decode()
        print(result)
    finally:
        sock.close()
        break
