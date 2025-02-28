use pyo3::prelude::*;
//use std::collections::HashMap;
use std::cmp;
use std::fmt;
use std::io;
use std::io::Write;
use std::sync::OnceLock;



//////////////////////
// 1. using u64 for bitboards, and u8 for squares
//////////////////////////////////////////////


// Piece Colors
const WHITE: bool = true;
const BLACK: bool = false;

// Piece List
static PIECE_COLORS: [bool; 2] = [WHITE, BLACK];
static WHITE_PIECES: [char; 6] = ['P', 'R', 'N', 'B', 'Q', 'K'];
static BLACK_PIECES: [char; 6] = ['p', 'r', 'n', 'b', 'q', 'k'];

fn get_pieces_list(piece_color: bool) -> [char; 6] {
    match piece_color {
        WHITE => {
            WHITE_PIECES
        }
        BLACK => {
            BLACK_PIECES
        }
    }
}


// // Piece Indices
fn get_piece_indices(piece_type: char) -> usize {
    match piece_type {
        'p' => {
            0
        }
        'r' => {
            1
        }
        'n' => {
            2
        }
        'b' => {
            3
        }
        'q' => {
            4
        }
        'k' => {
            5
        }
        _ => {
            panic!("Invalid piece: {}", piece_type);
        }
    }
}

// Names of files
static BOARD_FILES: [char; 8] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

// Useful Bitboard representations
static BOARD_EMPTY: u64 = 0;
static BOARD_FULL: u64 = 0xffff_ffff_ffff_ffff;

// Represention of all the squares
static BOARD_SQUARES: [u64; 64] = {
    let mut arr: [u64; 64] = [0; 64];
    let mut i = 0;

    while i < 64 {
        arr[i] = 1 << i;
        i += 1;
    }
    arr
};

// Ranks
static BOARD_RANK_1: u64 = 0xff;
static BOARD_RANK_3: u64 = 0xff << (8*2);
static BOARD_RANK_4: u64 = 0xff << (8*3);
static BOARD_RANK_5: u64 = 0xff << (8*4);
static BOARD_RANK_6: u64 = 0xff << (8*5);
static BOARD_RANK_8: u64 = 0xff << (8*7);

// Files
static BOARD_FILE_A: u64 = 0x0101_0101_0101_0101;
static BOARD_FILE_B: u64 = 0x0101_0101_0101_0101 << 1;
static BOARD_FILE_C: u64 = 0x0101_0101_0101_0101 << 2;
static BOARD_FILE_D: u64 = 0x0101_0101_0101_0101 << 3;
static BOARD_FILE_F: u64 = 0x0101_0101_0101_0101 << 5;
static BOARD_FILE_G: u64 = 0x0101_0101_0101_0101 << 6;
static BOARD_FILE_H: u64 = 0x0101_0101_0101_0101 << 7;


// Movement Directions
static KNIGHT_DIRS: [i8; 8]= [17, 15, 10, 6, -6, -10, -15, -17];
static KING_DIRS: [i8; 8] = [9, 8, 7, 1, -1, -7, -8, -9];
static BISHOP_DIRS: [i8; 4] = [9, 7, -7, -9];
static ROOK_DIRS: [i8; 4] = [8, 1, -1, -8];
static QUEEN_DIRS: [i8; 8] = [9, 8, 7, 1, -1, -7, -8, -9];


// Castling data
// list of squares that can't be under attack for king side castle
fn get_king_side_castle_squares(piece_color: bool) -> [usize; 3] {
    match piece_color {
        WHITE => {
            [4, 5, 6]
        }
        BLACK => {
            [60, 61, 62]
        }
    }
}


//list of square that can't be under attack for queen side castle
fn get_queen_side_castle_squares(piece_color: bool) -> [usize; 3] {
    match piece_color {
        WHITE => {[4, 3, 2]}
        BLACK => {[60, 59, 58]}
    }
}


// Not implementing with a yield like functionality.. just creating a vector
// fn scan_reversed
fn scan_reversed(mut bitboard: u64) -> Vec<u32> {
    let mut set_bits: Vec<u32> = Vec::new();

    while bitboard != 0 {
        let i: u32 = 63 - bitboard.leading_zeros();
        set_bits.push(i);
        bitboard ^= 1 << i;
    }
    set_bits
}


// get the rank of a square
const fn square_rank(square: u8) -> u8 {
    (square >> 3) + 1
}


// get the square file
fn square_file(square: usize) -> char {
    BOARD_FILES.get(square & 7).copied().unwrap()
}


// Square file index
const fn square_file_index(square: u8) -> u8 {
    square & 7
}


// Get name of a square; eg: a1, f7, etc
fn square_name(square: u8) -> String {
    // String::from(square_file(square).to_string()).push_str(square_rank(square).to_string())
    format!("{}{}", square_file(square as usize), square_rank(square))
}


fn square_index(square_name: &str) -> usize {
    let split_square: Vec<char> = square_name.chars().collect();
    //let rank: char = 'a';
    8 * (split_square[1].to_digit(10).unwrap_or(0) - 1) as usize + BOARD_FILES.iter().position(|&file| file == split_square[0]).unwrap_or(0)
}

// Precomputing the indices for files, and ranks for all the squares
static SQUARE_RANK_INDICES: [u8; 64] = {
    let mut arr: [u8; 64] = [0; 64];
    let mut i: usize = 0;

    while i < 64 {
        arr[i] = square_rank(i as u8);
        i += 1;
    }
    arr
};

static SQUARE_FILE_INDICES: [u8; 64] = {
    let mut arr: [u8; 64] = [0; 64];
    let mut i: usize = 0;

    while i < 64 {
        arr[i] = square_file_index(i as u8);
        i+= 1;
    }
    arr
};


// Get the Chebyshev distance between two squares
fn square_distance(sq1: i8, sq2: i8) -> i8 {
    cmp::max(
        i8::abs(SQUARE_FILE_INDICES[sq1 as usize] as i8 - SQUARE_FILE_INDICES[sq2 as usize] as i8),
        i8::abs(SQUARE_RANK_INDICES[sq1 as usize] as i8 - SQUARE_RANK_INDICES[sq2 as usize] as i8)
    )
}


// Get attack/movement masks sliding pieces, and other pieces
fn get_attack_masks(from_square: u8, directions: &[i8], allowed_distance: u8) -> u64 {
    let mut attack_mask: u64 = 0;

    for &dir in directions {
        let to_square: i8 = from_square as i8 + dir;

        if (0..64).contains(&to_square)  && square_distance(from_square as i8, to_square) < allowed_distance as i8 {
            attack_mask |= BOARD_SQUARES[to_square as usize];
        }
    }

    attack_mask
}

// Precomputed King and Knight attack masks
static KING_ATTACK_MASKS: OnceLock<[u64; 64]> = OnceLock::new();
static KNIGHT_ATTACK_MASKS: OnceLock<[u64; 64]> = OnceLock::new();

fn precompute_king_attacks() -> [u64; 64] {
    let mut king_attacks: [u64; 64] = [0;64];

    for i in 0..64 {
        king_attacks[i] = get_attack_masks(i as u8, &KING_DIRS, 2);
    }
    king_attacks
}


fn precompute_knight_attacks() -> [u64; 64] {
    let mut knight_attacks: [u64; 64] = [0;64];

    for i in 0..64 {
        knight_attacks[i] = get_attack_masks(i as u8, &KNIGHT_DIRS, 3);
    }
    knight_attacks
}

// Calculate precomputed knight attack masks once
fn get_precomputed_knight_attacks() -> &'static [u64; 64] {
    KNIGHT_ATTACK_MASKS.get_or_init(|| precompute_knight_attacks())
}

// Calculate Precomputed king attack masks once
fn get_precomputed_king_attacks() -> &'static [u64; 64] {
    KING_ATTACK_MASKS.get_or_init(|| precompute_king_attacks())
}


//TODO: Implement BOARD_SQUARES
fn get_sliding_attack_masks(from_square: u8, directions: &[i8], allowed_distance: u8) -> Vec<u64> {
    let mut attack_masks: Vec<u64> = Vec::new();

    for &dir in directions {
        let mut to_square: i8 = from_square as i8 + dir;
        let mut attack_mask: u64 = 0;

        while (0..64).contains(&to_square) && square_distance(from_square as i8, to_square) < allowed_distance as i8 {
            attack_mask |= BOARD_SQUARES[to_square as usize];
            to_square += dir;
        }
        if attack_mask != 0 {
            attack_masks.push(attack_mask);
        }
    }
    attack_masks
}


// Representing a move
#[pyclass]
pub struct Move {
    #[pyo3(get, set)]
    to_square: u32,
    #[pyo3(get, set)]
    from_square: u32,
    #[pyo3(get, set)]
    promotion: Option<char>,
}

#[pymethods]
impl Move {
    #[new]
    fn new(from_square: u32, to_square: u32, promotion: Option<char>) -> Move {
        Move{
            from_square,
            to_square,
            promotion
        }
    }

    fn uci(&self) -> String {
        match self.promotion {
            Some(promotion) => format!("{}{}{}", square_name(self.from_square as u8), square_name(self.to_square as u8), promotion),
            None => format!("{}{}", square_name(self.from_square as u8), square_name(self.to_square as u8)),
        }
    }

    // For python __str__
    fn __str__(&self)  -> String {
        format!("{}", self)
    }

    fn __repr__(&self)  -> String {
        format!("{}", self)
    }
}


// Representing a board at a given time
#[pyclass]
#[derive(Clone)]
struct BoardState {
    pawns: u64,
    rooks: u64,
    knights: u64,
    bishops: u64,
    queens: u64,
    kings: u64,

    white_pieces: u64,
    black_pieces: u64,

    ep_square: Option<u8>,
    half_move_clock: usize,
    full_move_clock: usize,
    castling_abilities: Option<String>,
    turn: bool
}

impl BoardState {
    fn new(board: &Board) -> Self {
        let board_state = BoardState {
            pawns: board.pawns,
            rooks: board.rooks,
            knights: board.knights,
            bishops: board.bishops,
            queens: board.queens,
            kings: board.kings,

            white_pieces: board.white_pieces,
            black_pieces: board.black_pieces,

            ep_square: board.ep_square,
            half_move_clock: board.half_move_clock,
            full_move_clock: board.full_move_clock,
            castling_abilities: board.castling_abilities.clone(),
            turn: board.turn
        };
        board_state
    }

    // Not implementing restore method here. It should be a part of Board struct!
    // fn restore() {}
}


#[pyclass]
pub struct Board {
    // Pieces
    pawns: u64,
    rooks: u64,
    knights: u64,
    bishops: u64,
    queens: u64,
    kings: u64,
    white_pieces: u64,
    black_pieces: u64,

    // Other info
    starting_fen: String,
    ep_square: Option<u8>,
    half_move_clock: usize,
    full_move_clock: usize,
    castling_abilities: Option<String>,
    #[pyo3(get, set)]
    turn: bool,

    // Previous moves and board states
    _move_stack: Vec<Move>,
    _board_states: Vec<BoardState>
}

#[pymethods]
impl Board {
    #[new]
    fn new(starting_fen: Option<&str>) -> Self {
        let fen = starting_fen
            .unwrap_or("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            .to_string();

        let mut board = Board {
            pawns: 0,
            rooks: 0,
            knights: 0,
            bishops: 0,
            queens: 0,
            kings: 0,
            white_pieces: 0,
            black_pieces: 0,
            starting_fen: fen,
            ep_square: None,
            half_move_clock: 0,
            full_move_clock: 0,
            castling_abilities: None,
            turn: WHITE,
            _move_stack: Vec::new(),
            _board_states: Vec::new()
        };
        board.set_board();
        board
    }

    fn set_board(&mut self) {
        let starting_fen: String = self.starting_fen.clone();
       let parts: Vec<&str> = starting_fen.split(' ' ).collect();

        if parts.len() < 6 {
            panic!("Invalid starting fen; got {}, with {} parts", self.starting_fen, parts.len());
        }

        // set the piece values
        let board_position = parts[0].to_string();
        let mut counter: isize = 55;
        for char in board_position.chars() {
            //eprintln!("{} {}", char, counter);
            //io::stderr().flush().expect("Failed to flush stderr");
            if char.is_digit(10) {
                counter += char.to_digit(10).unwrap_or(0) as isize;
            } else if char == '/' {
                //eprintln! ("here with counter {}", counter);
                counter -= 16;
            } else {
                counter += 1;
                self.set_pieces_or(char, BOARD_SQUARES[counter as usize]);
            }
        }

        // Set turn
        if parts[1].to_string() == "w" {
            self.turn = WHITE;
        } else {
            self.turn = BLACK;
        }

        // Set the castling rights
        if parts[2].to_string() != "-" {
            self.castling_abilities = Some(parts[2].to_string());
        }

        // Set the En-passant square
        if parts[3].to_string() != "-" {
            self.ep_square = Some(square_index(&parts[3]) as u8);
        }

        // Set the half move clock
        self.half_move_clock = parts[4].to_string().parse().unwrap_or(0);

        // Set the full move clock
        self.full_move_clock = parts[5].to_string().parse().unwrap_or(0);

    }


    fn get_pieces(&self, piece_type: char) -> u64 {
        match piece_type {
            'p' | 'P' => {
                self.pawns
            }
            'r' | 'R' => {
                self.rooks
            }
            'n' | 'N' => {
                self.knights
            }
            'b' | 'B' => {
                self.bishops
            }
            'q' | 'Q' => {
                self.queens
            }
            'k' | 'K' => {
                self.kings
            }
            'w' | 'W' => {
                self.white_pieces
            }
            'a' | 'A' => {
                self.black_pieces | self.white_pieces
            }
            _ => {
                panic!("Invalid piece type: {}", piece_type);
            }
        }
    }

    // Update the values of a piece_type by performing an OR with a bitboard
    fn set_pieces_or(&mut self, piece_type: char, bitboard: u64) {
        match piece_type {
            'p' | 'P' => {
                self.pawns |= bitboard;
            }
            'r' | 'R' => {
                self.rooks |= bitboard;
            }
            'n' | 'N' => {
                self.knights |= bitboard;
            }
            'b' | 'B' => {
                self.bishops |= bitboard;
            }
            'q' | 'Q' => {
                self.queens |= bitboard;
            }
            'k' | 'K' => {
                self.kings |= bitboard;
            }
            _ => panic!("Invalid piece type")
        }

        if piece_type.is_ascii_uppercase() {
            self.white_pieces |= bitboard;
        } else {
            self.black_pieces |= bitboard;
        }
    }

    fn set_pieces_xor(&mut self, piece_type: char, bitboard: u64) {
        match piece_type {
            'p' | 'P' => {
                self.pawns ^= bitboard;
            }
            'r' | 'R' => {
                self.rooks ^= bitboard;
            }
            'n' | 'N' => {
                self.knights ^= bitboard;
            }
            'b' | 'B' => {
                self.bishops ^= bitboard;
            }
            'q' | 'Q' => {
                self.queens ^= bitboard;
            }
            'k' | 'K' => {
                self.kings ^= bitboard;
            }
            _ => panic!("Invalid piece type")
        }

        // if piece_type.is_ascii_uppercase() {
        //     self.white_pieces ^= bitboard;
        // } else {
        //     self.black_pieces ^= bitboard;
        // }
    }

    fn pawn_moves(&mut self) -> Vec<Move> {
        let mut pawn_moves: Vec<Move> = Vec::new();

        let mut white_pawns: u64 = 0;
        let mut black_pawns: u64 = 0;
        let all_pieces: u64 = self.white_pieces | self.black_pieces;

        // for white's turn
        if self.turn {
            white_pawns = self.pawns & self.white_pieces;

            //Single Push
            let single_moves: u64 = white_pawns << 8 & !all_pieces;

            //Double Push
            let double_moves: u64 = single_moves << 8 & !all_pieces & BOARD_RANK_4;

            for to_square in scan_reversed(single_moves).into_iter() {
                let from_square: u32 = to_square - 8;

                if SQUARE_RANK_INDICES[to_square as usize] == 8 {
                    pawn_moves.push(Move {
                        from_square,
                        to_square,
                        promotion: Some('q')
                    }
                    );

                    pawn_moves.push(Move {
                        from_square,
                        to_square,
                        promotion: Some('r')
                    });

                    pawn_moves.push(Move {
                        from_square,
                        to_square,
                        promotion: Some('n')
                    });

                    pawn_moves.push(Move {
                        from_square,
                        to_square,
                        promotion: Some('b')
                    });
                } else {
                    pawn_moves.push(Move {from_square, to_square, promotion: None});
                }
            }

            // for double push
            for to_square in scan_reversed(double_moves).into_iter() {
                let from_square: u32 = to_square - 16;
                pawn_moves.push(Move{
                    from_square,
                    to_square,
                    promotion: None
                });
            }

            // Captures
            let black_pieces: u64 = self.black_pieces;

            let mut captures: u64 = (white_pawns & !BOARD_FILE_A) << 7 & black_pieces;
            captures |= (white_pawns & !BOARD_FILE_H) << 9 & black_pieces;

            for to_square in scan_reversed(captures).into_iter() {
                if (BOARD_SQUARES[to_square as usize - 9] & !BOARD_FILE_A) & white_pawns != 0{
                    let from_square: u32 = to_square - 9;

                    if SQUARE_RANK_INDICES[to_square as usize] == 8 {
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('q')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('r')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('n')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('b')});
                    } else {
                        pawn_moves.push(Move{from_square, to_square, promotion: None})
                    }
                }

                if (BOARD_SQUARES[to_square as usize - 7] & !BOARD_FILE_H) & white_pawns != 0 {
                    let from_square: u32 = to_square - 7;

                    if SQUARE_RANK_INDICES[to_square as usize] == 8 {
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('q')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('r')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('n')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('b')});
                    } else {
                        pawn_moves.push(Move{from_square, to_square, promotion: None})
                    }
                }
            }
        } else {
            black_pawns = self.pawns & self.black_pieces;

            // Single push
            let single_moves: u64 = black_pawns >> 8 & !all_pieces;

            // Double push
            let double_moves: u64 = single_moves >> 8  & !all_pieces & BOARD_RANK_5;

            // Get single push moves
            for to_square in scan_reversed(single_moves).into_iter() {
                let from_square: u32 = to_square + 8;

                if SQUARE_RANK_INDICES[to_square as usize] == 1 {
                    pawn_moves.push(Move{from_square, to_square, promotion: Some('q')});
                    pawn_moves.push(Move{from_square, to_square, promotion: Some('r')});
                    pawn_moves.push(Move{from_square, to_square, promotion: Some('n')});
                    pawn_moves.push(Move{from_square, to_square, promotion: Some('b')});
                } else {
                    pawn_moves.push(Move{from_square, to_square, promotion: None})
                }
            }

            // Get double push moves
            for to_square in scan_reversed(double_moves).into_iter() {
                let from_square: u32 = to_square + 16;

                pawn_moves.push(Move{from_square, to_square, promotion: None})
            }

            // Captures
            let white_pieces = self.white_pieces;

            let mut captures = (black_pawns >> 7 & !BOARD_FILE_A) & white_pieces;
            captures |= (black_pawns >> 9 & !BOARD_FILE_H) & white_pieces;

            for to_square in scan_reversed(captures).into_iter() {
                if (BOARD_SQUARES[to_square as usize + 9] & !BOARD_FILE_A) & black_pawns != 0 {
                    let from_square: u32 = to_square + 9;

                    if SQUARE_RANK_INDICES[to_square as usize] == 1 {
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('q')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('r')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('n')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('b')});
                    } else {
                        pawn_moves.push(Move{from_square, to_square, promotion: None})
                    }
                }

                if (BOARD_SQUARES[to_square as usize + 7] & !BOARD_FILE_H) & black_pawns != 0 {
                    let from_square: u32 = to_square + 7;

                    if SQUARE_RANK_INDICES[to_square as usize] == 1 {
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('q')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('r')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('n')});
                        pawn_moves.push(Move{from_square, to_square, promotion: Some('b')});
                    } else {
                        pawn_moves.push(Move{from_square, to_square, promotion: None})
                    }
                }
            }
        }

        // Add En-Passant move
        if let Some(ep_square) = self.ep_square {
            // let to_square: u32 = square_index(self.ep_square);
            let to_square: u32 = ep_square as u32;

            let mut from_mask: u64 = 0;
            let to_mask: u64 = BOARD_SQUARES[to_square as usize];

            if self.turn {
                let capturers: u64 = white_pawns & BOARD_RANK_5;
                from_mask = capturers & (to_mask >> 7)  & !BOARD_FILE_A;
                from_mask |= capturers & (to_mask >> 9) & !BOARD_FILE_H;
            } else {
                let capturers: u64 = black_pawns & BOARD_RANK_3;
                let mut from_mask: u64 = capturers & (to_mask << 7)  & !BOARD_FILE_H;
                from_mask |= capturers & (to_mask >> 9) & !BOARD_FILE_A;
            }

            for from_square in scan_reversed(from_mask).into_iter() {
                pawn_moves.push(Move{from_square, to_square, promotion: None});
            }
        }
        pawn_moves
    }

    fn knight_moves(&self) -> Vec<Move> {
        let mut knight_moves: Vec<Move> = Vec::new();
        let attack_masks: &[u64; 64] = get_precomputed_knight_attacks();

        let knight_bb: u64;
        let pieces: u64;

        if self.turn {
            pieces = self.white_pieces;
        } else {
            pieces = self.black_pieces;
        }

        knight_bb = self.knights & pieces;

        for from_square in scan_reversed(knight_bb).into_iter() {
            let movement_mask: u64 = attack_masks[from_square as usize] & !pieces;

            for to_square in scan_reversed(movement_mask).into_iter() {
                knight_moves.push(Move{from_square, to_square, promotion: None});
            }
        }
        knight_moves
    }

    // Get kings's moves
    fn king_moves(&self) -> Vec<Move> {
        let mut king_moves: Vec<Move> = Vec::new();
        let attack_masks: &[u64; 64] = get_precomputed_king_attacks();

        let pieces: u64;
        let king_bb: u64;

        if self.turn {
            pieces = self.white_pieces;
        } else {
            pieces = self.black_pieces;
        }

        king_bb = self.kings & pieces;

        // There should only be one knight
        let from_square: u32 = 63 - king_bb.leading_zeros();
        let movement_mask: u64 = attack_masks[from_square as usize] & !pieces;

        for to_square in scan_reversed(movement_mask).into_iter() {
            king_moves.push(Move{from_square, to_square, promotion: None});
        }
        king_moves
    }

    // Bishop Moves
    fn bishop_moves(&self) -> Vec<Move> {
        let mut bishop_moves: Vec<Move> = Vec::new();

        let bishop_bb: u64;
        let pieces: u64;
        let opp_pieces: u64;

        if self.turn {
            pieces = self.white_pieces;
            opp_pieces = self.black_pieces;
        } else {
            pieces = self.black_pieces;
            opp_pieces = self.white_pieces;
        }

        bishop_bb = self.bishops & pieces;

        for from_square in scan_reversed(bishop_bb).into_iter() {
            for delta in BISHOP_DIRS.iter() {
                let mut to_square: i8 = from_square as i8 + delta;

                while (0..64).contains(&to_square) && square_distance(to_square, to_square - delta) < 2{
                    let to_mask: u64 = BOARD_SQUARES[to_square as usize];
                    if to_mask & pieces != 0 {
                        break;
                    } else if to_mask & opp_pieces != 0 {
                        bishop_moves.push(Move{from_square, to_square: to_square as u32, promotion: None});
                        break;
                    } else {
                        bishop_moves.push(Move{from_square, to_square: to_square as u32, promotion: None});
                        to_square += delta;
                    }
                }
            }
        }
        bishop_moves
    }

    // Rook Moves
    fn rook_moves(&self) -> Vec<Move> {
        let mut rook_moves: Vec<Move> = Vec::new();

        let rook_bb: u64;
        let pieces: u64;
        let opp_pieces: u64;

        if self.turn {
            pieces = self.white_pieces;
            opp_pieces = self.black_pieces;
        } else {
            pieces = self.black_pieces;
            opp_pieces = self.white_pieces;
        }
        rook_bb = self.rooks & pieces;

        for from_square in scan_reversed(rook_bb).into_iter() {
            for delta in ROOK_DIRS.iter() {
                let mut to_square: i8 = from_square as i8 + delta;

                while (0..64).contains(&to_square) && square_distance(to_square, to_square - delta) < 2{
                    let to_mask : u64 = BOARD_SQUARES[to_square as usize];

                    if to_mask & pieces != 0 {
                        break;
                    } else if to_mask & opp_pieces != 0 {
                        rook_moves.push(Move{from_square, to_square: to_square as u32, promotion: None});
                        break;
                    } else {
                        rook_moves.push(Move{from_square, to_square: to_square as u32, promotion: None});
                        to_square += delta;
                    }
                }
            }
        }
        rook_moves
    }


    // Queen Moves
    fn queen_moves(&self) -> Vec<Move> {
        let mut queen_moves: Vec<Move> = Vec::new();

        let queen_bb: u64;
        let pieces: u64;
        let opp_pieces: u64;

        if self.turn {
            pieces = self.white_pieces;
            opp_pieces = self.black_pieces;
        } else {
            pieces = self.black_pieces;
            opp_pieces = self.white_pieces;
        }
        queen_bb = self.queens & pieces;

        for from_square in scan_reversed(queen_bb).into_iter() {
            for delta in QUEEN_DIRS.iter() {
                let mut to_square: i8 = from_square as i8 + delta;

                while (0..64).contains(&to_square) && square_distance(to_square, to_square - delta) < 2 {
                    let to_mask: u64 = BOARD_SQUARES[to_square as usize];

                    if to_mask & pieces != 0 {
                        break;
                    } else if to_mask & opp_pieces != 0 {
                        queen_moves.push(Move{from_square, to_square: to_square as u32, promotion: None});
                        break;
                    } else {
                        queen_moves.push(Move{from_square, to_square: to_square as u32, promotion: None});
                        to_square += delta;
                    }
                }
            }
        }
        queen_moves
    }


    // Get all the pseudo legal moves
    fn pseudo_legal_moves(&mut self) -> Vec<Move> {
        let mut moves: Vec<Move> = Vec::new();
        moves.extend(self.pawn_moves());
        moves.extend(self.knight_moves());
        moves.extend(self.king_moves());
        moves.extend(self.bishop_moves());
        moves.extend(self.rook_moves());
        moves.extend(self.queen_moves());
        moves
    }


    // Check is a square is attacked
    fn _is_attacked(&mut self, square: u8) -> bool {
        let mut is_attacked: bool = false;
        // Flip the turn
        self.turn = !self.turn;

        // Iterate through the pseudo legal moves of the opponent
        for mo in self.pseudo_legal_moves().into_iter() {
            if mo.to_square == square as u32 {
                is_attacked = true;
                break;
            }
        }

        // Flip the turn back
        self.turn = !self.turn;
        is_attacked
    }


    // King in Check
    fn is_check(&mut self) -> bool {
        let pieces: u64;
        let king_bb: u64;

        if self.turn {
            pieces = self.white_pieces;
        } else {
            pieces = self.black_pieces;
        }
        king_bb = self.kings & pieces;
        let king_square: u32 = 63 - king_bb.leading_zeros();

        self._is_attacked(king_square as u8)
    }


    // Get castling Moves
    fn _castling_moves(&mut self) -> Vec<Move> {
        let mut castling_moves: Vec<Move> = Vec::new();

        if let Some(castling_abilities) = self.castling_abilities.clone() {
            let mut sides: Vec<char> = Vec::new();

            for identifier in castling_abilities.chars() {
                if self.turn && identifier.is_uppercase() {
                    sides.push(identifier);
                }

                if !self.turn && identifier.is_uppercase() {
                    sides.push(identifier);
                }
            }

            let backrank: u64 = if self.turn { BOARD_RANK_1 } else {BOARD_RANK_8};

            // Bitboards for all the squares at backrank, for required files
            let bb_b: u64 = backrank & BOARD_FILE_B;
            let bb_c: u64 = backrank & BOARD_FILE_C;
            let bb_d: u64 = backrank & BOARD_FILE_D;
            let bb_f: u64 = backrank & BOARD_FILE_F;
            let bb_g: u64 = backrank & BOARD_FILE_G;

            let all_pieces: u64 = self.white_pieces | self.black_pieces;

            for side in sides {
                if side == 'k' || side == 'K' {
                    if all_pieces & (bb_f | bb_g) == 0 {
                        let mut squares_under_attack: bool = false;

                        let castle_squares: [usize; 3] = get_king_side_castle_squares(self.turn);

                        for square in castle_squares.iter() {
                            if self._is_attacked(*square as u8) {
                                squares_under_attack = true;
                                break;
                            }
                        }

                        // None of the squares that the king will move through are under attack
                        if !squares_under_attack {
                            let to_square: u32 = castle_squares[2] as u32;
                            let from_square: u32 = castle_squares[0] as u32;
                            castling_moves.push(Move{from_square, to_square, promotion: None});
                        }
                    }
                } else {
                    if all_pieces & (bb_b | bb_c | bb_d) == 0 {
                        let mut squares_under_attack: bool = false;

                        let castle_squares: [usize; 3] = get_queen_side_castle_squares(self.turn);

                        for square in castle_squares.iter() {
                            if self._is_attacked(*square as u8) {
                                squares_under_attack = true;
                                break;
                            }
                        }

                        if !squares_under_attack {
                            let to_square: u32 = castle_squares[2] as u32;
                            let from_square: u32 = castle_squares[0] as u32;
                            castling_moves.push(Move{from_square, to_square, promotion: None});
                        }
                    }
                }
            }
        }

        castling_moves
    }


    // Get Legal Moves
    fn legal_moves(&mut self) -> Vec<Move> {
        let mut legal_moves: Vec<Move> = Vec::new();

        legal_moves.extend(self._castling_moves());

        for pseudo_move in self.pseudo_legal_moves() {
            self.apply_move(&pseudo_move);

            self.turn = !self.turn;
            if self.is_check() {
                self.pop();
            } else {
                legal_moves.push(pseudo_move);
                self.pop();
            }
        }
        legal_moves
    }


    // Check if the half move clock needs to be reset
    fn _reset_half_move_clock(&self, from_mask: u64, to_mask: u64) -> bool {
        let pieces: u64;
        let opp_pieces: u64;

        if self.turn {
            pieces = self.white_pieces;
            opp_pieces = self.black_pieces;
        } else {
            pieces = self.black_pieces;
            opp_pieces = self.white_pieces;
        }

        let mut reset_mask: u64 = from_mask & (pieces & self.pawns);

        if reset_mask == 0 {
            reset_mask |= (opp_pieces & to_mask);
        }
        reset_mask != 0
    }


    // Check Castling rights
    fn _check_castling_rights(&self) -> bool {
        if self.castling_abilities.is_none() {
            return false;
        } else {
            let castling_abilities = self.castling_abilities.clone().unwrap().to_string();

            if self.turn {
                if castling_abilities.contains('K') || castling_abilities.contains('Q') {
                    return true;
                }
            } else {
                if castling_abilities.contains('k') || castling_abilities.contains('q') {
                    return true;
                }
            }
        }
        false
    }


    // Remove castling rights
    fn _remove_castling_rights(&mut self, id: char) {

        match id {
            'a' => {
                self.castling_abilities = None;
            }
            'k' => {
                let current_castling_rights = self.castling_abilities.clone().unwrap().to_string();
                if self.turn {
                    self.castling_abilities = Some(current_castling_rights.replace("K", ""));
                } else {
                    self.castling_abilities = Some(current_castling_rights.replace("k", ""));
                }
            }
            'q' => {
                let current_castling_rights = self.castling_abilities.clone().unwrap().to_string();
                if self.turn {
                    self.castling_abilities = Some(current_castling_rights.replace("Q", ""));
                } else {
                    self.castling_abilities = Some(current_castling_rights.replace("q", ""));
                }
            }
            _ => {
                panic!("Invalid castling rights");
            }
        }
    }


    // Apply move
    pub fn apply_move(&mut self, mov: &Move) {
        let pieces: u64;
        let opp_pieces: u64;
        let mut moved_piece: Option<char> = None;
        let mut captured_piece: Option<char> = None;

        // Push to the move stack
        self._move_stack.push(Move{from_square: mov.from_square, to_square: mov.to_square, promotion: mov.promotion.clone()});

        // Push board-state
        self._board_states.push(BoardState::new(&self));

        // For piece movement
        let from_mask: u64 = BOARD_SQUARES[mov.from_square as usize];
        let to_mask: u64 = BOARD_SQUARES[mov.to_square as usize];
        let movement_mask: u64 = from_mask | to_mask;

        let move_distance: i8= square_distance(mov.to_square as i8, mov.from_square as i8);

        // Set pieces and opponent's pieces
        if self.turn{
            pieces = self.white_pieces;
            opp_pieces = self.black_pieces;
        } else {
            pieces = self.black_pieces;
            opp_pieces = self.white_pieces;
        }

        // Set the moved piece
        for piece_type in BLACK_PIECES.iter() {
            if self.get_pieces(*piece_type) & from_mask != 0 {
                moved_piece = Some(*piece_type);
                break;
            }
        }

        if moved_piece.is_none() {
            panic!("Could not find the piece to move for {}", mov);
        }

        // Set the captured piece
        for piece_type in BLACK_PIECES.iter() {
            if self.get_pieces(*piece_type) & to_mask != 0 {
                captured_piece = Some(*piece_type);
                break;
            }
        }


        // Reset the half move clock if there was a capture, or a pawn move
        if self._reset_half_move_clock(from_mask, to_mask) {
            self.half_move_clock = 0;
        } else {
            self.half_move_clock += 1
        }

        // Increment the full move clock
        if !self.turn {
            self.full_move_clock += 1;
        }

        // Check for En-Passant capture
        let mut is_en_passant_capture: bool = false;
        if moved_piece == Some('p') && self.ep_square.is_some() &&  i8::abs(self.ep_square.unwrap() as i8 - mov.to_square as i8) == 8 {
            is_en_passant_capture = true;
        }


        // Update En-Passant target square
        if (self.pawns & from_mask != 0) && move_distance == 2 {
            if self.turn {
                self.ep_square = Some(mov.to_square as u8 - 8);
            } else {
                self.ep_square = Some(mov.to_square as u8 + 8);
            }

        } else {
            self.ep_square = None;
        }


        // Update castling abilities; Check if a king or rook was moved
        let mut is_castling: bool = false;
        let king_piece_mask: u64 = self.kings & pieces;
        let rook_piece_mask: u64 = self.rooks & pieces;

        if (from_mask & (rook_piece_mask | king_piece_mask)) != 0 && self._check_castling_rights() {
            // Castling Happened
            if move_distance == 2 && (from_mask & king_piece_mask) != 0 {
                self._remove_castling_rights('a');
                is_castling = true;
            } else {
                // Check if the king was moved
                if from_mask & king_piece_mask != 0 {
                    self._remove_castling_rights('a');
                } else if from_mask & (rook_piece_mask & BOARD_FILE_A) != 0 {
                    self._remove_castling_rights('q');
                } else if from_mask & (rook_piece_mask & BOARD_FILE_H) != 0 {
                    self._remove_castling_rights('k')
                }
            }
        }

        // Move the piece
        self.set_pieces_xor(moved_piece.unwrap(), movement_mask);
        if self.turn {
            self.white_pieces ^= movement_mask;
        } else {
            self.black_pieces ^= movement_mask;
        }

        // Check for special movements/regular movement
        if mov.promotion.is_some() {
            // Remove the pawn
            self.pawns ^= to_mask;

            match mov.promotion {
                Some('q') => {
                    self.queens |= to_mask;
                }
                Some('r') => {
                    self.rooks |= to_mask;
                }
                Some('b') => {
                    self.bishops |= to_mask;
                }
                Some('n') => {
                    self.knights |= to_mask;
                }
                _ => {panic!("Panic in the disco!!! (promotion issue) for {}", mov)}
            }

            // Captured and promoted piece-type are the same
            if captured_piece.is_some() && captured_piece == mov.promotion {
                captured_piece = None;
                if self.turn {
                    self.black_pieces ^= to_mask;
                } else {
                    self.white_pieces ^= to_mask;
                }
            }

        } else if is_castling {
            // If King side castle
            let rook_movement_mask: u64;
            if mov.to_square > mov.from_square {
                rook_movement_mask = (to_mask >> 1) | (to_mask << 1)
            } else {
                rook_movement_mask = (to_mask >> 2) | (to_mask << 2)
            }

            self.rooks |= rook_movement_mask;
            if self.turn {
                self.white_pieces ^= rook_movement_mask;
            } else {
                self.black_pieces ^= rook_movement_mask;
            }

        } else if is_en_passant_capture {
            if self.turn {
                self.pawns ^= to_mask << 8;
                self.black_pieces ^= to_mask << 8;
            } else {
                self.pawns ^= to_mask >> 8;
                self.white_pieces ^= to_mask >> 8;
            }

        }

        // Direct capture
        if captured_piece.is_some() {
            self.set_pieces_xor(captured_piece.unwrap(), to_mask);

            if self.turn {
                self.black_pieces ^= to_mask;
            } else {
                self.white_pieces ^= to_mask;
            }
        }
        // Flip the turn
        self.turn = !self.turn;
    }


    // Checkmate
    pub fn is_checkmate(&mut self) -> bool {
        if !self.is_check() {
            false
        } else {
            let legal_moves: Vec<Move> = self.legal_moves();
            legal_moves.is_empty() == true
        }
    }


    // Check for stalemate
    pub fn is_stalemate(&mut self) -> bool {
        if self.is_check() {
            false
        } else {
            let legal_moves: Vec<Move> = self.legal_moves();
            legal_moves.is_empty() == true
        }
    }


    // Is game over (only looking at checkmates, and stalemates; No draw rules)
    pub fn is_game_over(&mut self) -> bool {
        self.is_checkmate() || self.is_stalemate()
    }


    // Restore the board from a previous state
    fn _restore(&mut self, board_state: BoardState) {
        self.pawns = board_state.pawns;
        self.rooks = board_state.rooks;
        self.knights = board_state.knights;
        self.bishops = board_state.bishops;
        self.queens = board_state.queens;
        self.kings = board_state.kings;
        self.white_pieces = board_state.white_pieces;
        self.black_pieces = board_state.black_pieces;

        self.turn = board_state.turn;
        self.half_move_clock = board_state.half_move_clock;
        self.full_move_clock = board_state.full_move_clock;
        self.ep_square = board_state.ep_square;
        self.castling_abilities = board_state.castling_abilities.clone();
    }


    // Pop a move (Move back to a previous position
    pub fn pop(&mut self) -> Move {
        let mov: Move = self._move_stack.pop().unwrap();
        let board_state: BoardState = self._board_states.pop().unwrap();
        self._restore(board_state);
        mov
    }


    // For python __str__ method
    fn __str__(&self)  -> String {
        format!("{}", self)
    }

    fn __repr__(&self)  -> String {
        format!("{}", self)
    }
}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut board_rep: [char; 64] = ['.'; 64];

        for piece_color in &PIECE_COLORS {
            let color_pieces = {
                if *piece_color{
                    self.white_pieces
                } else {
                    self.black_pieces
                }
            };

            for piece in &get_pieces_list(*piece_color) {
                let piece_indices = scan_reversed(self.get_pieces(*piece) & color_pieces);

                for i in piece_indices {
                    board_rep[i as usize] = *piece;
                }
            }
        }

        board_rep.reverse();

        let mut rep_string = String::new();
        for mut rank in board_rep.chunks_mut(8) {
            rank.reverse();
            //rep_string.extend(rank.iter().copied());
            rep_string.extend(rank.iter().map(|c| c.to_string()).collect::<Vec<String>>().join(" ").chars());
            rep_string.push('\n');
        }
        write!(f, "{}", rep_string.trim())
    }
}

impl fmt::Display for Move {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.uci())
    }
}




// Commented for the module
// fn main() {
//     println!("Enter a starting position: ");
//
//     let mut fen: String = String::new();
//
//     io::stdin().read_line(&mut fen).expect("Failed to read line");
//
//     let default_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1".to_string();
//
//     if fen.trim().is_empty() {
//         fen = default_string;
//     }
//
//     let mut board = Board::new(Some(fen.as_str()));
//
//     println! ("The board you entered: \n{}", board);
//
//     let moves: Vec<Move> = board.pseudo_legal_moves();
//
//     println!("Got {} moves", moves.len());
//
//     for mo in moves.into_iter() {
//         println!("{}", mo);
//     }
//
//     // Debugging square_distance function!
//     // let to_square: u8 = 2;
//     // let from_square: u8 = 19;
//     // println!("Square distance between {} -> {}; {}", to_square as i8, from_square as i8, square_distance(from_square as i8, to_square as i8));
//
//     println! ("\n\nThat's it..!");
//
// }
//
//
//






