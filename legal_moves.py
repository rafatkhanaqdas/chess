from pseudo_moves import get_pawn_moves, get_bishop_moves, get_knight_moves, get_rook_moves, get_queen_moves, get_king_moves

move_dispatch = {
        "P": get_pawn_moves,
        "N": get_knight_moves,
        "B": get_bishop_moves,
        "R": get_rook_moves,
        "Q": get_queen_moves,
        "K": get_king_moves,
    }

white_pieces = ["wP", "wN", "wB", "wR", "wQ"]
black_pieces = ["bP", "bN", "bB", "bR", "bQ"]

# legal move filter
def filter_legal_moves(board: object, pos: tuple, pseudo_moves: list, color: str):
    legal = []
    for move in pseudo_moves:
        captured_piece = board.make_move((pos, move))
        if not is_in_check(board, color):
            legal.append(move)
        board.undo_move((pos, move),captured_piece)
    return legal

# get all playable moves
def get_all_legal_moves(board: object, color: str):
    moves = []
    king_pos = board.wk_pos if color == "w" else board.bk_pos
    pieces = white_pieces if color == "w" else black_pieces
    for piece in pieces:
        for pos in list(board.piece_pos[piece]):
            row, col = pos//8, pos%8
            pseudo = move_dispatch[piece[1]](board.board, (row, col))
            legal = filter_legal_moves(board, (row, col), pseudo, color)
            if piece in {"wP","bP"}:
                for dest in legal:
                    if piece == "wP" and dest[0] == 0:
                        moves += [((row, col), dest, piece) for piece in ["wQ","wR","wB","wN"]]
                    elif piece == "bP" and dest[0] == 7:
                        moves += [((row, col), dest, piece) for piece in ["bQ","bR","bB","bN"]]
                    else:
                        moves.append(((row, col), dest))
            else:    
                moves += [((row, col), dest) for dest in legal]
    # for the king
    row, col = king_pos//8, king_pos%8
    pseudo = move_dispatch["K"](board.board, (row, col))
    legal = filter_legal_moves(board, (row, col), pseudo, color)
    moves += [((row, col), dest) for dest in legal]
    # castling for white
    if color == "w":
        if board.w_Kside:
            if not is_in_check(board, color):
                if board.board[king_pos+1] == None and board.board[king_pos+2] == None:
                    undo1 = board.make_move(((row,col),(row,col+1)))
                    if not is_in_check(board, color):
                        undo2 = board.make_move(((row,col+1),(row,col+2)))
                        if not is_in_check(board, color):
                            moves.append(((row,col),(row,col+2)))
                        board.undo_move(((row,col+1),(row,col+2)),undo2)
                    board.undo_move(((row,col),(row,col+1)),undo1)
        if board.w_Qside:
            if not is_in_check(board, color):
                if board.board[king_pos-1] == None and board.board[king_pos-2] == None and board.board[king_pos-3] == None:
                    undo1 = board.make_move(((row,col),(row,col-1)))
                    if not is_in_check(board, color):
                        undo2 = board.make_move(((row,col-1),(row,col-2)))
                        if not is_in_check(board, color):
                            moves.append(((row,col),(row,col-2)))
                        board.undo_move(((row,col-1),(row,col-2)),undo2)
                    board.undo_move(((row,col),(row,col-1)),undo1)
    # castling for black
    else:
        if board.b_Kside:
            if not is_in_check(board, color):
                if board.board[king_pos+1] == None and board.board[king_pos+2] == None:
                    undo1 = board.make_move(((row,col),(row,col+1)))
                    if not is_in_check(board, color):
                        undo2 = board.make_move(((row,col+1),(row,col+2)))
                        if not is_in_check(board, color):
                            moves.append(((row,col),(row,col+2)))
                        board.undo_move(((row,col+1),(row,col+2)),undo2)
                    board.undo_move(((row,col),(row,col+1)),undo1)
        if board.b_Qside:
            if not is_in_check(board, color):
                if board.board[king_pos-1] == None and board.board[king_pos-2] == None and board.board[king_pos-3] == None:
                    undo1 = board.make_move(((row,col),(row,col-1)))
                    if not is_in_check(board, color):
                        undo2 = board.make_move(((row,col-1),(row,col-2)))
                        if not is_in_check(board, color):
                            moves.append(((row,col),(row,col-2)))
                        board.undo_move(((row,col-1),(row,col-2)),undo2)
                    board.undo_move(((row,col),(row,col-1)),undo1)
    return moves

# check checker
def is_in_check(board_obj: object, color: str):
    index =  board_obj.wk_pos if color == "w" else board_obj.bk_pos
    board = board_obj.board
    eny_color = "b" if color == "w" else "w"
    eny_r = eny_color + "R"
    eny_q = eny_color + "Q"
    eny_b = eny_color + "B"
    eny_n = eny_color + "N"
    eny_k = eny_color + "K"
    king_index = (index//8, index%8)
    row, col = king_index
    # rook/queen moves
    if row != 7:
        for i in range(row+1,8):
            if board[i*8+col] is None:
                continue
            elif board[i*8+col] in {eny_r,eny_q}:
                return True
            else:
                break
    if row != 0:
        for i in range(row-1,-1,-1):
            if board[i*8+col] is None:
                continue
            elif board[i*8+col] in {eny_r,eny_q}:
                return True
            else:
                break
    if col != 7:
        for i in range(col+1,8):
            if board[row*8+i] is None:
                continue
            elif board[row*8+i] in {eny_r,eny_q}:
                return True
            else:
                break    
    if col != 0:
        for i in range(col-1,-1,-1):
            if board[row*8+i] is None:
                continue
            elif board[row*8+i] in {eny_r,eny_q}:
                return True
            else:
                break
    # bishop/queen moves
    while row < 7 and col < 7:
        if board[(row+1)*8+col+1] is None:
            pass
        elif board[(row+1)*8+col+1] in {eny_b,eny_q}:
            return True
        else:
            break
        row+=1
        col+=1
    row, col = king_index
    while row > 0 and col < 7:
        if board[(row-1)*8+col+1] is None:
            pass
        elif board[(row-1)*8+col+1] in {eny_b,eny_q}:
            return True
        else:
            break
        row-=1
        col+=1
    row, col = king_index
    while row < 7 and col > 0:
        if board[(row+1)*8+col-1] is None:
            pass
        elif board[(row+1)*8+col-1] in {eny_b,eny_q}:
            return True
        else:
            break
        row+=1
        col-=1
    row, col = king_index
    while row > 0 and col > 0:
        if board[(row-1)*8+col-1] is None:
            pass
        elif board[(row-1)*8+col-1] in {eny_b,eny_q}:
            return True
        else:
            break
        row-=1
        col-=1
    row, col = king_index
    # knight moves
    if col != 7 and row not in [0,1]:
        if board[(row-2)*8+col+1] == eny_n:
            return True
    if col != 0 and row not in [0,1]:
        if board[(row-2)*8+col-1] == eny_n:
            return True
    if col != 7 and row not in [6,7]:
        if board[(row+2)*8+col+1] == eny_n:
            return True
    if col != 0 and row not in [6,7]:
        if board[(row+2)*8+col-1] == eny_n:
            return True
    if row != 7 and col not in [0,1]:
        if board[(row+1)*8+col-2] == eny_n:
            return True
    if row != 0 and col not in [0,1]:
        if board[(row-1)*8+col-2] == eny_n:
            return True
    if row != 7 and col not in [6,7]:
        if board[(row+1)*8+col+2] == eny_n:
            return True
    if row != 0 and col not in [6,7]:
        if board[(row-1)*8+col+2] == eny_n:
            return True
    # pawn moves
    if eny_color == "w" and row != 7:
        if col!=7 and board[(row+1)*8+col+1] == "wP":
                return True
        if col!=0 and board[(row+1)*8+col-1] == "wP":
                return True
    elif eny_color == "b" and row != 0:
        if col!=7 and board[(row-1)*8+col+1] == "bP":
                return True
        if col!=0 and board[(row-1)*8+col-1] == "bP":
                return True
    # king moves
    if row != 7:
        if board[(row+1)*8+col] == eny_k:
            return True
        if col != 7:
            if board[(row+1)*8+col+1] == eny_k:
                return True
        if col != 0:
            if board[(row+1)*8+col-1] == eny_k:
                return True
    if row != 0:
        if board[(row-1)*8+col] == eny_k:
            return True
        if col != 7:
            if board[(row-1)*8+col+1] == eny_k:
                return True
        if col != 0:
            if board[(row-1)*8+col-1] == eny_k:
                return True
    if col != 0:
        if board[row*8+col-1] == eny_k:
            return True
    if col != 7:
        if board[row*8+col+1] == eny_k:
            return True
    return False

# check if game has ended or not
def get_game_state(board: object, color: str):
    if is_in_check(board, color) and get_all_legal_moves(board, color) == []:
        return ("checkmate")
    elif not is_in_check(board, color) and get_all_legal_moves(board, color) == []:
        return ("stalemate")
    else:
        return("ongoing")

# user move input and verification
def user_move(board_obj: object, move: str, color: str) -> None:
    board = board_obj.board
    move = move.replace("x","")
    if len(move) == 3:
        piece = move[0]
        src = [index for index, value in enumerate(board) if value == color+piece]
    elif len(move) == 2:
        piece = "P"
        src = [index for index, value in enumerate(board) if value == color+piece]
    elif len(move) == 4 and not isinstance(move[1], int):
        piece = move[0]
        src = [index for index, value in enumerate(board) if (value == color+piece and index%8 == col[move[1]])]
    elif len(move) == 4 and isinstance(move[1], int):
        piece = move[0]
        index = [index for index, value in enumerate(board) if (value == color+piece and index//8 == int(move[1]))]
    dest_row = 8-int(move[-1])
    dest_col = col[move[-2]]
    for index in src:
        src_row, src_col = (index//8, index %8)
        legal = filter_legal_moves(board_obj, (src_row, src_col), move_dispatch[piece](board, (src_row, src_col)), color)
        if (dest_row,dest_col) in legal:
            return ((src_row, src_col), (dest_row,dest_col))

#  used to adjust the user input to int 
col = {
    'a' : 0,
    'b' : 1,
    'c' : 2,
    'd' : 3,
    'e' : 4,
    'f' : 5,
    'g' : 6,
    'h' : 7,
}