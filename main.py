from board import Board
from legal_moves import get_game_state, user_move
from move_generator import find_best_move
from evaluation import evaluate
import traceback

def main():
    board = Board()
    color = 'w'
    move = 0
    try:
        while get_game_state(board, color) == "ongoing" and move !=30:
            if color == 'w':
                board.print_board()
                white_move = find_best_move(board, 4, 'w')
                print(white_move)
                board.make_move(white_move)
                color = 'b'
            else:
                board.print_board()
                black_move = find_best_move(board, 4, 'b')
                board.make_move(black_move)
                print(black_move)
                color = 'w'
            move += 1
    except Exception as e:
        traceback.print_exc()
    print(evaluate(board.piece_pos, board.wk_pos, board.bk_pos))
    for piece in board.piece_pos.keys():
        print(piece, board.piece_pos[piece])
    print("white king", board.wk_pos)
    print("black king", board.bk_pos)
    print(move)
    board.print_board()

if __name__ == "__main__":
    main()