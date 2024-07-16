class GameSetup:
    def __init__(self):
        self._board = None
        self._ships = [Ship("Carrier", 5), Ship("Battleship",4), Ship("Cruiser", 3), Ship("Submarine", 3), Ship("Destroyer", 2)]
        self._hitsBoard = None

    def create_board(self):
        """Create a simple 8x8 board"""
        print("Creating Empty Board...")
        self._board = [["0" for _ in range(8)] for _ in range(8)]
        self._hitsBoard = [["0" for _ in range(8)] for _ in range(8)]
        print("(+) 8x8 Board Created Successfully\n")

    def place_ships(self):
        """Ask the user where they want to place each of their ships"""
        ships = self.get_ships()
        for ship in ships:

            canPlace = False
            while not canPlace:
                # Print the board for the user to visualise
                self.print_board()

                # Get information from user about where ship should be
                x, y, orientation = self.get_placement_info(ship)

                # Place the ship on the board
                canPlace = self.place_ship(self._board, x, y, ship.get_size(), orientation)

                if not canPlace:
                    print("(-) Invalid information for ship, try again.")
        print("(+) All ships placed! Here is you board.")
        self.print_board()

    def get_placement_info(self, ship):
        spaces = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}

        # Pick a start space (e.g. A8)
        startpoint = self.enter_position(ship)

        # Split the string position entered by user
        x = startpoint[0]
        y = startpoint[1]

        try:
            y = int(y)
            y -= 1
            isInt = True
        except ValueError:
            isInt = False

        # If startpoint is not a valid space
        while x not in spaces or not isInt or y < 0 or y > 7:
            print("(-) Invalid Space. Try Again.")
            startpoint = self.enter_position(ship)
            x = startpoint[0]
            y = startpoint[1]

            try:
                y = int(y)
                y -= 1
                isInt = True
            except ValueError:
                isInt = False

        x = spaces[x]

        # Pick an orientation
        orientation = input("Enter orientation of piece (Up/Down/Left/Right): ").lower()

        while orientation != "right" and orientation != "down" and orientation != "left" and orientation != "up":
            print("(-) Invalid orientation, try again.")
            orientation = input("Enter orientation of piece (Up/Down/Left/Right): ").lower()

        return x, y, orientation

    def add_to_board(self, start, n, ship):
        for space in range(n):
            self._board[start][space] = ship

    def get_ships(self):
        ships = []
        for ship in self._ships:
            ships.append(ship)
        return ships
    
    def enter_position(self, ship):
        """Get the initial position of the ship in the grid"""
        startpoint = input(f"Where do you want to place {ship.get_type()}, (Length: {ship.get_size()}): ").upper()
        while len(startpoint) != 2:
            print("(-) Invalid Space, try again.")
            startpoint = input(f"Where do you want to place {ship.get_type()}, (Length: {ship.get_size()}): ").upper()
        return startpoint
    
    def can_place_ship(self, board, x, y, length, orientation):
        """Check is the ship can be placed in the selected squares"""
        if orientation == "right":
            if y + length > 8:
                return False    # Invalid placement
            for i in range(length):
                if board[x][y+i] != "0":
                    return False    # Invalid placement
        elif orientation == "down":
            if x + length > 8:
                return False    # Invalid placement
            for i in range(length):
                if board[x+i][y] != "0":
                    return False    # Invalid placement
        elif orientation == "left":
            if y - length < -1:
                return False    # Invalid placement
            for i in range(length):
                if board[x][y-i] != "0":
                    return False    # Invalid placement
        elif orientation == "up":
            if x - length < -1:
                return False    # Invalid placement
            for i in range(length):
                if board[x-i][y] != "0":
                    return False    # Invalid placement
        else:
            return False  # Invalid placement
        
        return True # Valid placement
        
    def place_ship(self, board, x, y, length, orientation):
        if self.can_place_ship(board, x, y, length, orientation):   # If you can place the ship, place it
            if orientation == 'right':
                for i in range(length):
                    board[x][y+i] = "S"
            elif orientation == 'down':
                for i in range(length):
                    board[x+i][y] = "S"
            elif orientation == 'left':
                for i in range(length):
                    board[x][y-i] = "S"
            elif orientation == 'up':
                for i in range(length):
                    board[x-i][y] = "S"
            print("(+) Ship placed\n")
            return True
        else:
            return False    # Ship cannot be placed
        
    def print_board(self):
        """Print a visual representation of the board"""
        board = self._board
        num_map = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H"}

        header = "  1 2 3 4 5 6 7 8"
        print(header)
        for i, row in enumerate(board):
            row_str = f"{num_map[i+1]} " + " ".join(row)
            print(row_str)

    def check_board(self, space):
        """Check if the chosen space has a piece of a ship in it"""
        board = self._board
        spaces = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}
        x = spaces[space[0]]
        y = int(space[1]) - 1
        if board[x][y] == "S":
            print("\nOpponent Hits @ %s: HIT" % space)
            return True
        print("\nOpponent Hits @ %s: MISS" % space)
        return False

    def print_hits(self):
        board = self._hitsBoard
        num_map = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H"}

        header = "  1 2 3 4 5 6 7 8"
        print(header)
        for i, row in enumerate(board):
            row_str = f"{num_map[i+1]} " + " ".join(row)
            print(row_str)

    def update_hits(self, space, outcome):
        board = self._hitsBoard
        spaces = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}
        x = spaces[space[0]]
        y = int(space[1]) - 1
        if outcome == "HIT":
            board[x][y] = "H"
        elif outcome == "MISS":
            board[x][y] = "M"
            
class Ship:
    def __init__(self, type, size):
        self._type = type
        self._size = size
        self._location = []

    def get_size(self):
        return self._size
    
    def get_type(self):
        return self._type
    
    
if __name__ == "__main__":
    s = GameSetup()
    s.create_board()
    s.place_ships()