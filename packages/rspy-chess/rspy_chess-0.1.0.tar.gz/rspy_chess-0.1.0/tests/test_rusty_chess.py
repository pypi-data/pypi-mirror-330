import unittest

from rusty_chess import Board, Move

import json

# TODO: functions not exposed yet!!
# For functions related to squares on the board
# class TestSquare(unittest.TestCase):
#     def test_scan_reversed(self):
#         # File A indices
#         bb = 0x0101_0101_0101_0101
#         self.assertCountEqual(list(board.scan_reversed(bb)), [56, 48, 40, 32, 24, 16, 8, 0])
#
#         # Rank 3 indices
#         bb = 0xff << (8 * 2)
#         self.assertCountEqual(list(board.scan_reversed(bb)), [23, 22, 21, 20, 19, 18, 17, 16])
#
#
#     def test_square_rank(self):
#         self.assertEqual(board.get_square_rank(41), 6)
#
#         self.assertEqual(board.get_square_rank(23), 3)
#
#         self.assertEqual(board.get_square_rank(2), 1)
#
#         self.assertEqual(board.get_square_rank(62), 8)
#
#
#     def test_square_file(self):
#         self.assertEqual(board.get_square_file(45), 'f')
#
#         self.assertEqual(board.get_square_file(18), 'c')
#
#         self.assertEqual(board.get_square_file(56), 'a')
#
#         self.assertEqual(board.get_square_file(39), 'h')
#
#
#     def test_square_file_index(self):
#         self.assertEqual(board.get_square_file_index(45), 5)
#
#         self.assertEqual(board.get_square_file_index(18), 2)
#
#         self.assertEqual(board.get_square_file_index(56), 0)
#
#         self.assertEqual(board.get_square_file_index(39), 7)
#
#
#     def test_square_distance(self):
#         self.assertEqual(board.square_distance(10, 28), 2)
#
#         self.assertEqual(board.square_distance(62, 39), 3)
#
#         self.assertEqual(board.square_distance(16, 15), 7)
#
#         self.assertEqual(board.square_distance(17, 46), 5)
#
#         self.assertEqual(board.square_distance(49, 35), 2)
#
#
#     def test_square_name(self):
#         self.assertEqual(board.get_square_name(51), 'd7')
#
#         self.assertEqual(board.get_square_name(34), 'c5')
#
#         self.assertEqual(board.get_square_name(0), 'a1')
#
#         self.assertEqual(board.get_square_name(63), 'h8')
#
#
#     def test_square_index(self):
#         self.assertEqual(board.get_square_index('a1'), 0)
#
#         self.assertEqual(board.get_square_index('h8'), 63)
#
#         self.assertEqual(board.get_square_index('e3'), 20)
#
#         self.assertEqual(board.get_square_index('d7'), 51)
#
#         self.assertEqual(board.get_square_index('a7'), 48)


# For the board object
class TestBoard(unittest.TestCase):
    def test_turn_default(self):
        bb = Board()
        self.assertTrue(bb.turn)

    def test_turn(self):
        bb = Board("8/P1r5/1N4P1/pp3p2/4RK1p/2p3P1/1Bk2pr1/8 w - - 0 1")
        self.assertTrue(bb.turn)

        bb = Board("8/P1r5/1N4P1/pp3p2/4RK1p/2p3P1/1Bk2pr1/8 b - - 0 1")
        self.assertFalse(bb.turn)

    # TODO: Finish it!
    def test_set_board(self):
        bb = Board()


    def test_bb_string(self):
        # Default positions
        bb = Board()
        default_rep = "r n b q k b n r\np p p p p p p p\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\nP P P P P P P P\nR N B Q K B N R\n\n"
        self.assertEqual(str(bb).strip(), default_rep.strip())

        # Random position
        ran_fen = "1k1r3r/pp4b1/3qb1p1/3pn2p/4PB2/3N2P1/PP1Q2BP/R4RK1 w - - 1 0"
        rep = ". k . r . . . r\np p . . . . b .\n. . . q b . p .\n. . . p n . . p\n. . . . P B . .\n. . . N . . P .\nP P . Q . . B P\nR . . . . R K ."
        bb = Board(ran_fen)
        self.assertEqual(str(bb).strip(), rep.strip())


    # def test_get_all_pieces(self):
    #     # Default
    #     bb = Board()
    #     self.assertEqual(bb._get_all_pieces(), 18446462598732906495)
    #     self.assertEqual(bb._get_all_pieces(board.WHITE), 65535)
    #     self.assertEqual(bb._get_all_pieces(board.BLACK), 18446462598732840960)
    #
    #     # Random
    #     fen = "1k1r3r/pp4b1/3qb1p1/3pn2p/4PB2/3N2P1/PP1Q2BP/R4RK1 w - - 1 0"
    #     bb = board.Board(fen)
    #     self.assertEqual(bb._get_all_pieces(), 9962904211342019425)
    #     self.assertEqual(bb._get_all_pieces(board.WHITE), 810077025)
    #     self.assertEqual(bb._get_all_pieces(board.BLACK), 9962904210531942400)


    def test_pawn_moves(self):
        # Default
        bb = Board()
        moves = [move.uci() for move in bb.pawn_moves()]
        expected_moves = ['h2h3', 'g2g3', 'f2f3', 'e2e3', 'd2d3', 'c2c3', 'b2b3', 'a2a3', 'h2h4', 'g2g4', 'f2f4', 'e2e4', 'd2d4', 'c2c4', 'b2b4', 'a2a4']
        self.assertCountEqual(moves, expected_moves)

        # Some captures and promotions
        fen = "8/P1r5/1N4P1/pp3p2/4RK1p/2p3P1/1Bk2pr1/8 b - - 0 1"
        bb = Board(fen)
        moves = [move.uci() for move in bb.pawn_moves()]
        expected_moves = ['b5b4', 'a5a4', 'h4h3', 'f2f1q', 'f2f1b', 'f2f1r', 'f2f1n', 'f5e4', 'h4g3', 'c3b2']
        self.assertCountEqual(moves, expected_moves)


    def test_knight_moves(self):
        # Default
        bb = Board()
        moves = [move.uci() for move in bb.knight_moves()]
        expected_moves = ['g1h3', 'g1f3', 'b1c3', 'b1a3']
        self.assertCountEqual(moves, expected_moves)

        # Random
        fen = "1k1r3r/pp4b1/3qb1p1/3pn2p/4PB2/3N2P1/PP1Q2BP/R4RK1 w - - 1 0"
        bb = Board(fen)
        moves = [move.uci() for move in bb.knight_moves()]
        expected_moves = ['d3e5', 'd3c5', 'd3b4', 'd3f2', 'd3e1', 'd3c1']
        self.assertCountEqual(moves, expected_moves)


    def test_king_moves(self):
        # Default
        bb = Board()
        moves = [move.uci() for move in bb.king_moves()]
        expected_moves = []
        self.assertCountEqual(moves, expected_moves)

        # Random
        fen = "4N3/3R3R/3KpPk1/N5q1/3p4/1Pp5/6P1/1r4Qb w - - 0 1"
        bb = Board(fen)
        moves = [move.uci() for move in bb.king_moves()]
        expected_moves = ['d6e7', 'd6c7', 'd6e6', 'd6c6', 'd6e5', 'd6d5', 'd6c5']
        self.assertCountEqual(moves, expected_moves)


    def test_bishop_moves(self):
        # Random
        fen = "3R3R/p5b1/6p1/3p2Pn/4b3/BK2k3/1Pp1N3/5r2 b - - 0 1"
        bb = Board(fen)
        moves = [move.uci() for move in bb.bishop_moves()]
        expected_moves = ['g7h8', 'g7f8', 'g7h6', 'g7f6', 'g7e5', 'g7d4', 'g7c3', 'g7b2', 'e4f5', 'e4f3', 'e4g2', 'e4h1', 'e4d3']
        self.assertCountEqual(moves, expected_moves)


    def test_rook_moves(self):
        # Random
        fen = "4N3/3R3R/3KpPk1/N5q1/3p4/1Pp5/6P1/1r4Qb w - - 0 1"
        bb = Board(fen)
        moves = [move.uci() for move in bb.rook_moves()]
        expected_moves = ['h7h8', 'h7g7', 'h7f7', 'h7e7', 'h7h6', 'h7h5', 'h7h4', 'h7h3', 'h7h2', 'h7h1', 'd7d8', 'd7e7', 'd7f7', 'd7g7', 'd7c7', 'd7b7', 'd7a7']
        self.assertCountEqual(moves, expected_moves)

    def test_queen_moves(self):
        # Random
        fen = "4N3/3R3R/3KpPk1/N5q1/3p4/1Pp5/6P1/1r4Qb w - - 0 1"
        bb = Board(fen)
        moves = [move.uci() for move in bb.queen_moves()]
        expected_moves = ['g1h2', 'g1f2', 'g1e3', 'g1d4', 'g1h1', 'g1f1', 'g1e1', 'g1d1', 'g1c1', 'g1b1']
        self.assertCountEqual(moves, expected_moves)

    # Compare legal moves against a pre-generated list of legal moves
    def test_legal_moves(self):
        filepath = "./tests/data/test_legal_moves.json"

        with open(filepath, 'r') as f:
            data = json.load(f, strict=False)

        for da in data:
            bb = Board(da['fen'])
            legal_moves = [move.uci() for move in bb.legal_moves()]
            self.assertCountEqual(legal_moves, da['legal_moves'], msg=f"tried for {da['fen']}; got {legal_moves}; expected: {da['legal_moves']}")


    def test_is_checkmate(self):
        ## Most of the test cases taken from https://github.com/schnitzi/rampart/blob/master/src/main/resources/testcases/checkmates.json
        bb = Board("4b1r1/8/1k2p3/5pP1/6K1/3r4/6n1/8 w - f6 0 1")
        self.assertTrue(bb.is_checkmate())

        bb = Board("8/2k5/8/8/8/8/PPn5/KR6 w - - 0 1")
        self.assertTrue(bb.is_checkmate())

        bb = Board("1R3k2/2R5/8/8/8/1K6/8/8 b - - 0 1")
        self.assertTrue(bb.is_checkmate())

        bb = Board("8/8/8/8/8/8/P1n5/K1k5 w - - 0 1")
        self.assertTrue(bb.is_checkmate())

        bb = Board("k1K5/p1N5/8/8/8/8/8/8 b - - 0 1")
        self.assertTrue(bb.is_checkmate())

        bb = Board("kr6/ppN5/8/8/8/8/2K5/8 b - - 0 1")
        self.assertTrue(bb.is_checkmate())

        bb = Board("8/1r6/2k5/8/8/2n5/8/K7 w - - 0 1")
        self.assertFalse(bb.is_checkmate())


    def test_is_stalemate(self):
        bb = Board("8/8/8/8/8/2k5/1r6/K7 w - - 0 1")
        self.assertTrue(bb.is_stalemate())

        bb = Board("k7/1R6/2K5/8/8/8/8/8 b - - 0 1")
        self.assertTrue(bb.is_stalemate())

        bb = Board("k7/2Q5/8/8/8/2K5/8/8 b - - 0 1")
        self.assertTrue(bb.is_stalemate())

        bb = Board("1k6/7b/2p2p2/4pP2/4K3/r7/8/8 w - e6 0 1")
        self.assertTrue(bb.is_stalemate())

        bb = Board("1R3k2/2R5/8/8/8/1K6/8/8 b - - 0 1")
        self.assertFalse(bb.is_stalemate())


    def test_is_check(self):
        ## Test cases taken from checkmate cases
        bb = Board("k1K5/p1N5/8/8/8/8/8/8 b - - 0 1")
        self.assertTrue(bb.is_check())

        bb = Board("8/1r6/2k5/8/8/2n5/8/K7 w - - 0 1")
        self.assertFalse(bb.is_check())







# For the Move objects
class TestMove(unittest.TestCase):
    def test_move_uci(self):
        self.assertEqual(Move(9, 25).uci(), 'b2b4')

        self.assertEqual(Move(52, 36).uci(), 'e7e5')

        self.assertEqual(Move(55, 63, 'q').uci(), 'h7h8q')

        self.assertEqual(Move(10, 2, 'n').uci(), 'c2c1n')

        self.assertEqual(Move(11, 18).uci(), 'd2c3')




if __name__ == "__main__":
    unittest.main()












