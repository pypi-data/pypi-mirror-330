# rspy_chess

## Introduction
A Python extension module written in Rust for chess move generation. This is a simple lightweight library for move generation. It uses bitboards for representing pieces on the board.

## Features
 - Set a board using Fen strings (defaults to the starting position)
    ```python
   >>> from rspy_chess import Board
   >>> board = Board("1k1r3r/pp4b1/3qb1p1/3pn2p/4PB2/3N2P1/PP1Q2BP/R4RK1 w - - 1 0")
    ```
 - Board representation in text
    ```python
   >>> board
    . k . r . . . r
    p p . . . . b .
    . . . q b . p .
    . . . p n . . p
    . . . . P B . .
    . . . N . . P .
    P P . Q . . B P
    R . . . . R K .
    ```
 - Move generation
    ```python
    >>> board.legal_moves()
    [g3g4, h2h3, b2b3, a2a3, h2h4, b2b4, a2a4, e4d5, d3e5, d3c5, d3b4, d3f2, d3e1, d3c1, g1f2, g1h1, f4g5, f4h6, 
   f4e5, f4e3, g2h3, g2f3, g2h1, f1f2, f1f3, f1e1, f1d1, f1c1, f1b1, a1b1, a1c1, a1d1, a1e1, d2e3, d2c3, d2b4, 
   d2a5, d2e2, d2f2, d2c2, d2e1, d2d1, d2c1]
    ```
- Move representation in UCI format
   ```python
   >>> from rspy_chess import Move
   >>> move = Move(22, 30)
   >>> move
   g3g4
   ```
 - Make and unmake moves
    ```python
   
   >>> board.apply_move(move) # Make a move
   >>> board.pop() # Unmake a move
   g3g4
    ```
 - Detect for checks, checkmate, stalemate, and attacks on a square
    ```python
    >>> board.is_check()
    False
    >>> board.is_checkmate()
    False
    >>> board.is_stalemate()
    False
    >>> board._is_attacked(28)
    True
    ```

## How to use it
 - Install maturin with `pip install maturin`
 - run `maturin develop --release`. This will install rspy_chess, and it can be used directly.
> Note: the python file in `python_src` folder can also be used directly.


## TODO
 - [ ] Implement checks for draw







    




