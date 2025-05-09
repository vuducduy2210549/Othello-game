class Board():
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self):
        """ Set up initial board configuration. """
        self.__pieces = [None]*8
        for i in range(8):
            self.__pieces[i] = [0]*8
        self.__pieces[3][4] = 1
        self.__pieces[4][3] = 1
        self.__pieces[3][3] = -1
        self.__pieces[4][4] = -1

    def __getitem__(self, index):
        return self.__pieces[index]

    def display(self, time):
        """" Display the board and the statistics of the ongoing game. """
        legel_moves = self.get_legal_moves(-1)
        print("    A B C D E F G H")
        print("    ---------------")
        for y in range(7,-1,-1):
            print(str(y+1) + ' |', end=' ')
            for x in range(8):
                piece = self[x][y]
                if piece == -1:
                    print("B", end=' ')
                elif piece == 1:
                    print("W", end=' ')
                elif (x, y) in legel_moves:
                    print("O", end=' ')
                else:
                    print(".", end=' ')
            print('| ' + str(y+1))
        print("    ---------------")
        print("    A B C D E F G H\n")
        print("STATISTICS (score / remaining time):")
        print("Black: " + str(self.count(-1)) + ' / ' + str(time[-1]))
        print("White: " + str(self.count(1)) + ' / ' + str(time[1]) + '\n')

    def count(self, color):
        """ Count the number of pieces of the given color.
        (1 for white, -1 for black, 0 for empty spaces) """
        count = 0
        for y in range(8):
            for x in range(8):
                if self[x][y] == color:
                    count += 1
        return count

    def get_squares(self, color):
        """ Get the coordinates (x,y) for all pieces on the board of the given color.
        (1 for white, -1 for black, 0 for empty spaces) """
        squares = []
        for y in range(8):
            for x in range(8):
                if self[x][y] == color:
                    squares.append((x,y))
        return squares

    def get_legal_moves(self, color):
        """ Return all the legal moves for the given color.
        (1 for white, -1 for black) """
        moves = set()
        for square in self.get_squares(color):
            newmoves = self.get_moves_for_square(square)
            if newmoves:
                moves.update(newmoves)
        return list(moves)

    def get_moves_for_square(self, square):
        # Return all the legal moves that use the given square as a base 
        # square. That is, if the given square is (3,4) and it contains a black 
        # piece, and (3,5) and (3,6) contain white pieces, and (3,7) is empty, 
        # one of the returned moves is (3,7) because everything from there to 
        # (3,4) can be flipped.
        (x, y) = square
        color = self[x][y]
        if color == 0:
            return None
        moves = []
        for direction in self.__directions:
            move = self._discover_move(square, direction)
            if move:
                moves.append(move)
        return moves

    def execute_move(self, move, color):
        """ Perform the given move on the board, and flips pieces as necessary.
        color gives the color of the piece to play (1 for white, -1 for black) """
        # Start at the new piece's square and follow it on all 8 directions
        # to look for pieces allowing flipping
        
        # Add the piece to the empty square
        flips = (flip for direction in self.__directions
                      for flip in self._get_flips(move, direction, color))
        for x, y in flips:
            self[x][y] = color

    def _discover_move(self, origin, direction):
        # Return the endpoint of a legal move, starting at the given origin,
        # and moving in the given direction.
        x, y = origin
        color = self[x][y]
        flips = []

        for move in Board._increment_move(origin, direction):
            x, y = move
            if self[x][y] == 0 and flips:
                return (x, y)
            elif self[x][y] == color or (self[x][y] == 0 and not flips):
                return None
            elif self[x][y] == -color:
                flips.append((x, y))

    def _get_flips(self, origin, direction, color):
        # Get the list of flips for a vertex and a direction to use within 
        # the execute_move function.
        flips = [origin]
        for move in Board._increment_move(origin, direction):
            x, y = move
            if self[x][y] == -color:
                flips.append((x, y))
            elif self[x][y] == 0:
                break
            elif self[x][y] == color and len(flips) > 1:
                return flips
            elif self[x][y] == color and len(flips) <= 1:
                return []
        return []

    @staticmethod
    def _increment_move(move, direction):
        # Generator expression for incrementing moves
        move = list(map(sum, zip(move, direction)))
        while all(map(lambda x: 0 <= x < 8, move)):
            yield tuple(move)
            move = list(map(sum, zip(move, direction)))

def get_col_char(col):
    return chr(ord('a') + col)

def move_string(move):
    (x, y) = move
    return get_col_char(x) + str(y + 1)

def moves_string(moves):
    return ', '.join([move_string(m) for m in moves])

def print_moves(moves):
    print(moves_string(moves))

if __name__ == '__main__':
    board = Board()
    dummy_time = {1: 300, -1: 300}  # Giả lập thời gian còn lại
    board.display(dummy_time)

    print("Black: ", end='')
    print_moves(board.get_legal_moves(-1))

    print("White: ", end='')
    print_moves(board.get_legal_moves(1))