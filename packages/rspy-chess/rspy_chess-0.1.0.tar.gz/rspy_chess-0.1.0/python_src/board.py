from functools import lru_cache
from dataclasses import dataclass

# Values for colors
WHITE = True
BLACK = False


# Pieces
PIECES_LIST = {
    WHITE: ["P", "R", "N", "B", "Q", "K"],
    BLACK: ["p", "r", "n", "b", "q", "k"]
}
PIECE_INDICES = {
    "p": 0,
    "r": 1,
    "n": 2,
    "b": 3,
    "q": 4,
    "k": 5
}


# Empty bitboard
BOARD_EMPTY = 0
# All squares on the board
BOARD_ALL = 0xffff_ffff_ffff_ffff
# Board FILES
BOARD_FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# Knight movement directions
KNIGHT_DIRS = [17, 15, 10, 6, -6, -10, -15, -17]

# King movement directions
KING_DIRS = [9, 8, 7, 1, -1, -7, -8, -9]

# Bishop movement directions
BISHOP_DIRS = [9, 7, -7, -9]

# Rook movement directions
ROOK_DIRS = [8, 1, -1, -8]

# Queen movement directions
QUEEN_DIRS = [9, 8, 7, 1, -1, -7, -8, -9]

# Useful rank and file representations
BOARD_RANK_1 = 0xff
BOARD_RANK_3 = 0xff << (8*2)
BOARD_RANK_4 = 0xff << (8*3)
BOARD_RANK_5 = 0xff << (8*4)
BOARD_RANK_6 = 0xff << (8*5)
BOARD_RANK_8 = 0xff << (8*7)

# BOARD_FILE
BOARD_FILE_A = 0x0101_0101_0101_0101
BOARD_FILE_B = 0x0101_0101_0101_0101 << 1
BOARD_FILE_C = 0x0101_0101_0101_0101 << 2
BOARD_FILE_D = 0x0101_0101_0101_0101 << 3
BOARD_FILE_F = 0x0101_0101_0101_0101 << 5
BOARD_FILE_G = 0x0101_0101_0101_0101 << 6
BOARD_FILE_H = 0x0101_0101_0101_0101 << 7

# Castling stuff
# list of squares that can't be under attack for king side castle
KING_SIDE_CASTLE_SQUARES = {
    WHITE: [4, 5, 6],
    BLACK: [60, 61, 62]
}
# list of square that can't be under attack for queen side castle
QUEEN_SIDE_CASTLE_SQUARES = {
    WHITE: [4, 3, 2],
    BLACK: [60, 59, 58]
}

## Store masks for all the squares on the board
BOARD_SQUARES = [1 << i for i in range(64)]




# Get indices of all the set bits (taken from python-chess)
def scan_reversed(bitboard):
    while bitboard:
        i = bitboard.bit_length() - 1
        yield i
        # unset the msb
        bitboard ^= BOARD_SQUARES[i]


@lru_cache()
def get_square_rank(square):
    return (square >> 3) + 1


@lru_cache()
def get_square_file(square):
    return BOARD_FILES[square & 7]


# Just get the index/value of the file
# Precomputing
@lru_cache()
def get_square_file_index(square):
    return square & 7


@lru_cache()
def get_square_name(square):
    return get_square_file(square) + str(get_square_rank(square))


@lru_cache()
def get_square_index(name):
    return 8*(int(name[1]) - 1) + BOARD_FILES.index(name[0])


SQUARE_RANK_INDICES = [get_square_rank(i) for i in range(64)]
SQUARE_FILE_INDICES = [get_square_file_index(i) for i in range(64)]
@lru_cache()
def square_distance(sq_a, sq_b):
    """
    Chebyshev Distance; Numbers of squares for king to move from a to b
    """
    return max(abs(SQUARE_FILE_INDICES[sq_a] - SQUARE_FILE_INDICES[sq_b]),
               abs(SQUARE_RANK_INDICES[sq_a] - SQUARE_RANK_INDICES[sq_b]))


####################
## Get attack squares; used in precomputing attack squares
def _get_attack_mask(from_square, delta, allowed_distance):
    attack_mask = 0x00
    for de in delta:
        to_square = from_square + de
        if 0 <= to_square < 64 and square_distance(from_square, to_square) < allowed_distance:
            attack_mask |= BOARD_SQUARES[to_square]
    return attack_mask


def _get_sliding_attack_masks(from_square, delta, allowed_distance):
    masks = []
    for de in delta:
        to_square = from_square + de
        movement_mask = 0
        while 0 <= to_square < 64 and square_distance(to_square, to_square - de) < allowed_distance:
            movement_mask |= BOARD_SQUARES[to_square]

            to_square += de
        masks.append(movement_mask)
    return masks


# Precomputed attack masks
KNIGHT_ATTACK_MASKS = [_get_attack_mask(i, KNIGHT_DIRS, 3) for i in range(64)]
KING_ATTACK_MASKS = [_get_attack_mask(i, KING_DIRS, 2) for i in range(64)]



# TODO: check copy methods after setting up the new pieces
class BoardState:
    def __init__(self, board):
        self.PAWNS = board.PAWNS
        self.KNIGHTS = board.KNIGHTS
        self.BISHOPS = board.BISHOPS
        self.ROOKS = board.ROOKS
        self.KINGS = board.KINGS
        self.QUEENS = board.QUEENS
        self.WHITE_PIECES = board.WHITE_PIECES
        self.BLACK_PIECES = board.BLACK_PIECES

        self._ep_square = board._ep_square
        self._half_move_clock = board._half_move_clock
        self._full_move_counter = board._full_move_counter
        self._castling_abilities = board._castling_abilities
        self.turn = board.turn


    def restore(self, board):
        #board._pieces = self._pieces.copy()
        board.PAWNS = self.PAWNS
        board.KNIGHTS = self.KNIGHTS
        board.BISHOPS = self.BISHOPS
        board.ROOKS = self.ROOKS
        board.KINGS = self.KINGS
        board.QUEENS = self.QUEENS
        board.WHITE_PIECES = self.WHITE_PIECES
        board.BLACK_PIECES = self.BLACK_PIECES

        board._ep_square = self._ep_square
        board._half_move_clock = self._half_move_clock
        board._full_move_counter = self._full_move_counter
        board._castling_abilities = self._castling_abilities
        board.turn = self.turn



@dataclass(unsafe_hash=True)
class Move:
    from_square: int
    to_square: int
    promotion: str = None

    def uci(self):
        if self.promotion:
            return get_square_name(self.from_square) + get_square_name(self.to_square) + self.promotion
        elif self:
            return get_square_name(self.from_square) + get_square_name(self.to_square)
        else:
            return '0000'


class PIECES:
    def __init__(self):
        self.PAWNS = 0
        self.KNIGHTS = 0
        self.BISHOPS = 0
        self.ROOKS = 0
        self.KINGS = 0
        self.QUEENS = 0
        self.WHITE_PIECES = 0
        self.BLACK_PIECES = 0


    def _get_pieces(self, symbol):
        if symbol == 'p':
            return self.PAWNS

        elif symbol == 'r':
            return self.ROOKS

        elif symbol == 'n':
            return self.KNIGHTS

        elif symbol == 'b':
            return self.BISHOPS

        elif symbol == 'q':
            return self.QUEENS

        elif symbol == 'k':
            return self.KINGS


    def _set_piece_xor(self, symbol, bb):
        if symbol == 'p':
            self.PAWNS ^= bb

        elif symbol == 'r':
            self.ROOKS ^= bb

        elif symbol == 'n':
            self.KNIGHTS ^= bb

        elif symbol == 'b':
            self.BISHOPS ^= bb

        elif symbol == 'q':
            self.QUEENS ^= bb

        elif symbol == 'k':
            self.KINGS ^= bb


    def _set_piece_or(self, symbol, bb):
        if symbol == 'p':
            self.PAWNS |= bb

        elif symbol == 'r':
            self.ROOKS |= bb

        elif symbol == 'n':
            self.KNIGHTS |= bb

        elif symbol == 'b':
            self.BISHOPS |= bb

        elif symbol == 'q':
            self.QUEENS |= bb

        elif symbol == 'k':
            self.KINGS |= bb


class Board(PIECES):
    def __init__(self, fen=None):
        super().__init__()
        if not fen:
            # Default opening
            fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        # Not maintaining the fen at every state of the board currently
        self._starting_fen = fen
        self._ep_square = None
        self._half_move_clock = 0
        self._full_move_counter = 0
        self._castling_abilities = None
        self._set_board()
        self._move_stack = []
        self._board_states = []


    # set the board based on the starting fen string
    def _set_board(self):
        starting_fen = self._starting_fen.split()

        count = 55  # starts from a file
        for char in starting_fen[0]:
            if char.isdigit():
                count += int(char)
            elif char == '/':
                count -= 16
            else:
                count += 1
                self._set_piece_or(char.lower(), BOARD_SQUARES[count])
                if char.islower():
                    self.BLACK_PIECES |= BOARD_SQUARES[count]
                else:
                    self.WHITE_PIECES |= BOARD_SQUARES[count]


        # Set the active player
        if starting_fen[1] == 'w':
            self.turn = WHITE
        else:
            self.turn = BLACK

        # Set the castling rights
        if starting_fen[2] != "-":
            self._castling_abilities = starting_fen[2]

        # Set the enpassant square
        if starting_fen[3] != "-":
            self._ep_square = starting_fen[3]

        # Set the half-move clock
        self._half_move_clock = int(starting_fen[4])

        # Set the full move counter
        self._full_move_counter = int(starting_fen[5])


    def __str__(self):
        show_str = ['.'] * 64
        for i in range(64):
            mask = BOARD_SQUARES[i]
            for piece in PIECE_INDICES:
                piece_mask = self._get_pieces(piece)
                if piece_mask & mask:
                    if mask & self.WHITE_PIECES:
                        show_str[i] = piece.upper()
                        break
                    elif mask & self.BLACK_PIECES:
                        show_str[i] = piece
                        break
        return '\n'.join([' '.join(show_str[i:i+8]) for i in range(0, 64, 8)][::-1])


    # TODO: [Fix] there's a bit of repetition of code here
    def _pawn_moves(self):
        #all_pieces = self._get_all_pieces(None)
        all_pieces = self.BLACK_PIECES | self.WHITE_PIECES

        # White
        if self.turn:
            white_pawns = self.PAWNS & self.WHITE_PIECES
            # Single Push
            single_moves = white_pawns << 8 & ~all_pieces
            # Double push
            double_moves = single_moves << 8 & ~all_pieces & BOARD_RANK_4

            # for single moves
            for to_square in scan_reversed(single_moves):
                from_square = to_square - 8

                # if get_square_rank(to_square) == 8:
                if SQUARE_RANK_INDICES[to_square] == 8:
                    yield Move(from_square, to_square, 'q')
                    yield Move(from_square, to_square, 'b')
                    yield Move(from_square, to_square, 'r')
                    yield Move(from_square, to_square, 'n')
                else:
                    yield Move(from_square, to_square)

            # for double moves
            for to_square in scan_reversed(double_moves):
                from_square = to_square - 16
                yield Move(from_square, to_square)

            # For captures
            black_pieces = self.BLACK_PIECES

            captures = (white_pawns & ~BOARD_FILE_A) << 7 & black_pieces
            captures |= (white_pawns & ~BOARD_FILE_H) << 9 & black_pieces

            for to_square in scan_reversed(captures):
                if (BOARD_SQUARES[to_square - 9] & ~BOARD_FILE_A) & white_pawns:
                    from_square = to_square - 9
                    if SQUARE_RANK_INDICES[to_square] == 8:
                        yield Move(from_square, to_square, 'q')
                        yield Move(from_square, to_square, 'b')
                        yield Move(from_square, to_square, 'r')
                        yield Move(from_square, to_square, 'n')
                    else:
                        yield Move(from_square, to_square)

                if (BOARD_SQUARES[to_square - 7] & ~BOARD_FILE_H) & white_pawns:
                    from_square = to_square - 7

                    if SQUARE_RANK_INDICES[to_square] == 8:
                        yield Move(from_square, to_square, 'q')
                        yield Move(from_square, to_square, 'b')
                        yield Move(from_square, to_square, 'r')
                        yield Move(from_square, to_square, 'n')
                    else:
                        yield Move(from_square, to_square)
        # For turn = BLACK
        else:
            black_pawns = self.PAWNS & self.BLACK_PIECES
            single_moves = black_pawns >> 8 & ~all_pieces
            double_moves = single_moves >> 8 & ~all_pieces & BOARD_RANK_5

            # for single moves
            for to_square in scan_reversed(single_moves):
                from_square = to_square + 8

                if SQUARE_RANK_INDICES[to_square] == 1:
                    yield Move(from_square, to_square, 'q')
                    yield Move(from_square, to_square, 'b')
                    yield Move(from_square, to_square, 'r')
                    yield Move(from_square, to_square, 'n')
                else:
                    yield Move(from_square, to_square)

            # for double moves
            for to_square in scan_reversed(double_moves):
                from_square = to_square + 16
                yield Move(from_square, to_square)

            # For captures
            white_pieces = self.WHITE_PIECES

            captures = (black_pawns >> 7 & ~BOARD_FILE_A) & white_pieces
            captures |= (black_pawns >> 9 & ~BOARD_FILE_H) & white_pieces

            for to_square in scan_reversed(captures):
                if (BOARD_SQUARES[to_square + 9] & ~BOARD_FILE_A) & black_pawns:
                    from_square = to_square + 9

                    if SQUARE_RANK_INDICES[to_square] == 1:
                        yield Move(from_square, to_square, 'q')
                        yield Move(from_square, to_square, 'b')
                        yield Move(from_square, to_square, 'r')
                        yield Move(from_square, to_square, 'n')
                    else:
                        yield Move(from_square, to_square)

                if (BOARD_SQUARES[to_square + 7] & ~BOARD_FILE_H) & black_pawns:
                    from_square = to_square + 7
                    if get_square_rank(to_square) == 1:
                        yield Move(from_square, to_square, 'q')
                        yield Move(from_square, to_square, 'b')
                        yield Move(from_square, to_square, 'r')
                        yield Move(from_square, to_square, 'n')
                    else:
                        yield Move(from_square, to_square)

        # Add en-passant
        if self._ep_square:
            to_square = get_square_index(self._ep_square)
            to_mask = BOARD_SQUARES[to_square]
            if self.turn:
                capturers = white_pawns & BOARD_RANK_5
                from_mask = capturers & (to_mask >> 7) & ~BOARD_FILE_A
                from_mask |= capturers & (to_mask >> 9) & ~BOARD_FILE_H
            else:
                capturers = black_pawns & BOARD_RANK_3

                from_mask = capturers & (to_mask << 7) & ~BOARD_FILE_H
                from_mask |= capturers & (to_mask << 9) & ~BOARD_FILE_A

            for from_square in scan_reversed(from_mask):
                yield Move(from_square, to_square)




    # Note: could be precomputed
    def _knight_moves(self):
        if self.turn:
            knights_bb = self.KNIGHTS & self.WHITE_PIECES
            pieces = self.WHITE_PIECES
        else:
            knights_bb = self.KNIGHTS & self.BLACK_PIECES
            pieces = self.BLACK_PIECES

        for from_square in scan_reversed(knights_bb):
            movement_mask = KNIGHT_ATTACK_MASKS[from_square] & ~pieces

            for to_square in scan_reversed(movement_mask):
                yield Move(from_square, to_square)


    def _king_moves(self):
        if self.turn:
            pieces = self.WHITE_PIECES
        else:
            pieces = self.BLACK_PIECES

        king_bb = self.KINGS & pieces

        # It will only have 1 value
        from_square = king_bb.bit_length() - 1

        movement_mask = KING_ATTACK_MASKS[from_square] & ~pieces

        for to_square in scan_reversed(movement_mask):
            yield Move(from_square, to_square)



    def _bishop_moves(self):
        if self.turn:
            pieces = self.WHITE_PIECES
            opp_pieces = self.BLACK_PIECES
        else:
            pieces = self.BLACK_PIECES
            opp_pieces = self.WHITE_PIECES

        bishop_bb = self.BISHOPS & pieces

        for from_square in scan_reversed(bishop_bb):
            for delta in BISHOP_DIRS:
                to_square = from_square + delta

                while 0 <= to_square < 64 and square_distance(to_square, to_square - delta) < 2:
                    to_mask = BOARD_SQUARES[to_square]
                    if to_mask & pieces:
                        break
                    elif to_mask & opp_pieces:
                        yield Move(from_square, to_square)
                        break
                    else:
                        yield Move(from_square, to_square)
                        to_square += delta


    def _rook_moves(self):
        if self.turn:
            pieces = self.WHITE_PIECES
            opp_pieces = self.BLACK_PIECES
        else:
            pieces = self.BLACK_PIECES
            opp_pieces = self.WHITE_PIECES

        rook_bb = self.ROOKS & pieces

        #ROOK_ATTACK_MASKS
        for from_square in scan_reversed(rook_bb):
            for delta in ROOK_DIRS:
                to_square = from_square + delta

                while 0 <= to_square < 64 and square_distance(to_square, to_square - delta) < 2:
                    to_mask = BOARD_SQUARES[to_square]
                    if to_mask & pieces:
                        break
                    elif to_mask & opp_pieces:
                        yield Move(from_square, to_square)
                        break
                    else:
                        yield Move(from_square, to_square)
                        to_square += delta


    def _queen_moves(self):
        if self.turn:
            pieces = self.WHITE_PIECES
            opp_pieces = self.BLACK_PIECES
        else:
            pieces = self.BLACK_PIECES
            opp_pieces = self.WHITE_PIECES

        queen_bb = self.QUEENS & pieces

        for from_square in scan_reversed(queen_bb):
            for delta in QUEEN_DIRS:
                to_square = from_square + delta

                # Not very efficient
                while 0 <= to_square < 64 and square_distance(to_square, to_square - delta) < 2:
                    to_mask = BOARD_SQUARES[to_square]
                    if to_mask & pieces:
                        break
                    elif to_mask & opp_pieces:
                        yield Move(from_square, to_square)
                        break
                    else:
                        yield Move(from_square, to_square)
                        to_square += delta

    # TODO: set test cases
    # Check if a given square is under attack by the opponent
    def _is_attacked(self, square):
        is_attacked = False
        # flip the turn
        self.turn = not self.turn

        #square_mask = BOARD_SQUARES[square]
        # Get the pseudo legal moves; look for square == to_square for any of the moves
        #square_mask = BOARD_SQUARES[square]
        for move in self._pseudo_legal_moves():
            if move.to_square == square:
                is_attacked = True
                break

        # reset the turn
        self.turn = not self.turn
        return is_attacked


    # Return possible castling moves
    def _castling_moves(self):
        if self._castling_abilities:
            if self.turn:
                sides = [side for side in self._castling_abilities if side.isupper()]
            else:
                sides = [side for side in self._castling_abilities if side.islower()]

            backrank = BOARD_RANK_1 if self.turn else BOARD_RANK_8

            bb_b = backrank & BOARD_FILE_B
            bb_c = backrank & BOARD_FILE_C
            bb_d = backrank & BOARD_FILE_D
            bb_f = backrank & BOARD_FILE_F
            bb_g = backrank & BOARD_FILE_G

            all_pieces = self.BLACK_PIECES | self.WHITE_PIECES

            for side in sides:
                if side in 'kK':
                    # Check there are no occupied squares in between
                    if not all_pieces & (bb_f | bb_g):
                        squares_under_attack = False
                        for square in KING_SIDE_CASTLE_SQUARES[self.turn]:
                            if self._is_attacked(square):
                                squares_under_attack = True
                                break
                        # None of the squares that the king moves through are under attack
                        if not squares_under_attack:
                            to_square = KING_SIDE_CASTLE_SQUARES[self.turn][-1]
                            from_square = KING_SIDE_CASTLE_SQUARES[self.turn][0]
                            yield Move(from_square, to_square)
                else:
                    if not all_pieces & (bb_c | bb_d | bb_b):
                        squares_under_attack = False
                        for square in QUEEN_SIDE_CASTLE_SQUARES[self.turn]:
                            if self._is_attacked(square):
                                squares_under_attack = True
                                break
                        # None of the squares that the king moves through are under attack
                        if not squares_under_attack:
                            to_square = QUEEN_SIDE_CASTLE_SQUARES[self.turn][-1]
                            from_square = QUEEN_SIDE_CASTLE_SQUARES[self.turn][0]
                            yield Move(from_square, to_square)


    # get pseudo legal moves
    def _pseudo_legal_moves(self):
        yield from self._pawn_moves()
        yield from self._knight_moves()
        yield from self._king_moves()
        yield from self._rook_moves()
        yield from self._bishop_moves()
        yield from self._queen_moves()


    # Check if the king is in check
    def is_check(self):
        if self.turn:
            pieces = self.WHITE_PIECES
        else:
            pieces = self.BLACK_PIECES

        king_bb = self.KINGS & pieces
        kings_square = king_bb.bit_length() - 1

        return self._is_attacked(kings_square)


    # Pseudo legal moves that don't put the king in check
    def get_legal_moves(self):
        yield from self._castling_moves()
        for move in self._pseudo_legal_moves():
            self.apply_move(move)

            # Check if our king is under check by the opponent
            ## flip the turn
            self.turn = not self.turn
            if not self.is_check():
                self.turn = not self.turn
                self.pop()
                yield move
            else:
                self.turn = not self.turn
                self.pop()


    # check if the move is a capture, or a pawn move
    def _reset_half_move_clock(self, from_mask, to_mask):
        # look for pawn move
        if self.turn:
            pieces = self.WHITE_PIECES
            opp_pieces = self.BLACK_PIECES
        else:
            pieces = self.BLACK_PIECES
            opp_pieces = self.WHITE_PIECES

        reset_mask = from_mask & (pieces & self.PAWNS)

        if not reset_mask:
            reset_mask |= (opp_pieces & to_mask)

        return bool(reset_mask)


    # Check if the active player has castling rights
    def _check_castling_rights(self):
        if self._castling_abilities is None:
            return False
        if self.turn:
            if 'K' in self._castling_abilities or 'Q' in self._castling_abilities:
                return True
        else:
            if 'k' in self._castling_abilities or 'q' in self._castling_abilities:
                return True
        return False


    # Remove castling rights
    def _remove_castling_rights(self, side=None):
        """
        Remove castling rights for the active player
        Args:
            side (None/'k'/'q'): remove both/king side/queen side castling rights

        Returns:
        """
        if side:
            if self.turn:
                self._castling_abilities.replace(side.upper(), '')
            else:
                self._castling_abilities.replace(side, '')
        else:
            if self.turn:
                self._castling_abilities.replace('K', '').replace('Q', '')
            else:
                self._castling_abilities.replace('k', '').replace('q', '')

        if not self._castling_abilities:
            self._castling_abilities = None



    def apply_move(self, move: Move):
        # Update the move stack
        self._move_stack.append(move)

        # Do I need to maintain board state..?
        self._board_states.append(BoardState(self))

        # Related to moving the piece
        from_mask = BOARD_SQUARES[move.from_square]
        to_mask = BOARD_SQUARES[move.to_square]
        movement_mask = from_mask | to_mask

        # set the pieces, opposition pieces
        if self.turn:
            pieces = self.WHITE_PIECES
            opp_pieces = self.BLACK_PIECES
        else:
            pieces = self.BLACK_PIECES
            opp_pieces = self.WHITE_PIECES

        # Move distance
        move_distance = square_distance(move.from_square, move.to_square)

        # Set the piece that was moved
        moved_piece = None
        for piece in PIECE_INDICES:
            if from_mask & self._get_pieces(piece):
                moved_piece = piece
                break

        ## Set the piece that was captured (direct capture)
        captured_piece = None
        if opp_pieces & to_mask:
            for piece in PIECE_INDICES:
                if self._get_pieces(piece) & to_mask:
                    captured_piece = piece
                    break

        # For debugging
        if not moved_piece:
            # TODO:  Raise an exception!!
            print(f"Did not find the active player's piece for {move.uci()}")

        # reset the half move clock if there was a capture a pawn move
        if self._reset_half_move_clock(from_mask, to_mask):
            self._half_move_clock = 0
        else:
            self._half_move_clock += 1

        # Increment the full move clock
        if not self.turn:
            self._full_move_counter += 1

        # Check if the move is an en-passant capture
        is_en_passant_capture = False
        if moved_piece == 'p' and self._ep_square and abs(get_square_index(self._ep_square) - move.to_square) == 8:
            is_en_passant_capture = True

        # Set en passant target square (a pawn being moved 2 squares)
        if moved_piece == "p" and move_distance == 2:
            if self.turn:
                self._ep_square = get_square_name(move.to_square - 8)
            else:
                self._ep_square = get_square_name(move.to_square + 8)
        else:
            # Reset the square
            self._ep_square = None

        # check if castling abilities are available, and a king or rook was moved
        is_castling = False # used later; saves a square distance calculation
        if moved_piece in "kr" and self._check_castling_rights():
            # king_piece_mask = self.KINGS & pieces
            rook_pieces_mask = self.ROOKS & pieces

            # Castling (king is moved)
            if move_distance == 2 and moved_piece == "k":
                # Remove castling rights for the active player
                self._remove_castling_rights()
                is_castling = True
            else:
                # Check if King was moved
                if moved_piece == "k":
                    self._remove_castling_rights()
                # Check if Rook on file A was moved
                elif from_mask & (rook_pieces_mask & BOARD_FILE_A):
                    self._remove_castling_rights("q")
                # Check if Rook on file H was moved
                elif from_mask & (rook_pieces_mask & BOARD_FILE_H):
                    self._remove_castling_rights("k")
                # else:
                #     print("What!!?")

        ## Move the piece
        self._set_piece_xor(moved_piece, movement_mask)
        if self.turn:
            self.WHITE_PIECES ^= movement_mask
        else:
            self.BLACK_PIECES ^= movement_mask


        # Check for promotion
        if move.promotion:
            # Remove the pawn from the position
            self.PAWNS ^= to_mask

            if move.promotion == 'q':
                # Add a queen; queen piece identifier is at index
                self.QUEENS |= to_mask

            elif move.promotion == 'b':
                # Add a bishop
                self.BISHOPS |= to_mask

            elif move.promotion == 'r':
                # Add a rook
                self.ROOKS |= to_mask

            elif move.promotion == 'n':
                # Add a knight
                self.KNIGHTS |= to_mask

            else:
                raise ValueError(f"unexpected promption type; for move: {move.uci()}")

            if captured_piece and captured_piece == move.promotion:
                ## unset captured piece value;
                captured_piece = None
                if self.turn:
                    self.BLACK_PIECES ^= to_mask
                else:
                    self.WHITE_PIECES ^= to_mask

        # Is castling...
        elif is_castling:
            # King side castle
            if move.to_square > move.from_square:
                rook_movement_mask = (to_mask >> 1) | (to_mask << 1)
            else:
                rook_movement_mask = (to_mask << 2) | (to_mask >> 1)

            self.ROOKS ^= rook_movement_mask
            if self.turn:
                self.WHITE_PIECES ^= rook_movement_mask
            else:
                self.BLACK_PIECES ^= rook_movement_mask

        ## Is en passant capture
        elif is_en_passant_capture:
            if self.turn:
                self.PAWNS ^= (to_mask << 8)
                self.BLACK_PIECES ^= (to_mask << 8)
            else:
                self.PAWNS ^= (to_mask >> 8)
                self.WHITE_PIECES ^= (to_mask >> 8)

        ## Check for direct capture
        if captured_piece:
            self._set_piece_xor(captured_piece, to_mask)
            if self.turn:
                self.BLACK_PIECES ^= to_mask
            else:
                self.WHITE_PIECES ^= to_mask
        # Change the turn
        self.turn = not self.turn


    # unmake the last move
    def pop(self):
        move = self._move_stack.pop()
        self._board_states.pop().restore(self)
        return move


    # Check if the game is in checkmate situation
    def is_checkmate(self):
        if not self.is_check():
            return False
        return not any(self.get_legal_moves())


    # Check if the game in stalemate situation
    def is_stalemate(self):
        if self.is_check():
            return False
        # check for any other reasons for the game to end..?
        return not any(self.get_legal_moves())


    def is_game_over(self):
        return self.is_checkmate() | self.is_stalemate()



