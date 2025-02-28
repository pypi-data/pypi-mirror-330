## Use the test_fens.txt file to read up the fen strings, and use chess library to generate legal moves for the given position
import json
import time
import chess

def write_json(data, file):
    with open(file, 'w') as f:
        json.dump(data, f)


def generate_test_data():
    filepath = "./test_fens.txt"
    outfile = "./test_legal_moves.json"

    with open(filepath, 'r') as f:
        data = f.readlines()

    test_data = []
    start_time = time.time()
    for da in data:
        da = da.replace('\n', '')
        data_dict = {}

        board = chess.Board(da)

        legal_moves = [move.uci() for move in board.legal_moves]

        data_dict['fen'] = da
        data_dict['legal_moves'] = legal_moves

        test_data.append(data_dict)
    end_time = time.time()

    write_json(test_data, outfile)

    print(f"Time taken to generate legal moves for {len(test_data)} fen strings: {round(end_time - start_time, 3)}")


def main():
    generate_test_data()


if __name__ == "__main__":
    main()