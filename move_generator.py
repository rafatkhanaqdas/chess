from legal_moves import is_in_check, get_all_legal_moves
from evaluation import evaluate, PIECE_VALUES

def find_best_move(board: object, depth: int, color: str) -> tuple:
    maximizing_player = True if color == 'w' else False
    best_move = ()
    best_Eval = -float('inf') if maximizing_player else float('inf')
    moves = get_all_legal_moves(board, color)
    moves = order_moves(board.board, moves)
    for move in moves:
        captured_piece = board.make_move(move)
        Eval = minimax(board, depth-1, -float('inf'), float('inf'), not maximizing_player)
        board.undo_move(move, captured_piece)
        if maximizing_player:
            if Eval > best_Eval:
                best_Eval = Eval
                best_move = move
        else:
            if Eval < best_Eval:
                best_Eval = Eval
                best_move = move
    return best_move

def minimax(board: object, depth: int, alpha: float, beta: float, maximizing_player: bool) -> int:
    color = "w" if maximizing_player else "b"
    moves = get_all_legal_moves(board, color)
    if not moves:
        if is_in_check(board, color):
            return -10000 if maximizing_player else 10000
        else:
            return 0
    
    if depth == 0:
        return quiescence(board, alpha, beta, maximizing_player)
    
    if maximizing_player:
        maxEval = -float('inf')
        moves = order_moves(board.board, moves)
        for move in moves:
            captured_piece = board.make_move(move)
            Eval = minimax(board, depth-1, alpha, beta, False)
            board.undo_move(move, captured_piece)
            maxEval = max(maxEval,Eval)
            alpha = max(alpha, Eval)
            if alpha >= beta: break
        return maxEval
    
    else:
        minEval = float('inf')
        moves = order_moves(board.board, moves)
        for move in moves:
            captured_piece = board.make_move(move)
            Eval = minimax(board, depth-1, alpha, beta, True)
            board.undo_move(move, captured_piece)
            minEval = min(minEval,Eval)
            beta = min(beta, Eval)
            if alpha >= beta: break
        return minEval


def quiescence(board: object, alpha: float, beta: float, maximizing_player: bool):
    color = "w" if maximizing_player else "b"
    moves = get_all_legal_moves(board, color)
    if not moves:
        if is_in_check(board, color):
            return -10000 if maximizing_player else 10000
        else:
            return 0
    stand_pat = evaluate(board.piece_pos, board.wk_pos, board.bk_pos)
    if maximizing_player:
        if stand_pat >= beta: return stand_pat
        alpha = max(alpha, stand_pat)
    else:
        if stand_pat <= alpha: return stand_pat
        beta = min(beta, stand_pat)
    try:
        captures = [m for m in moves if board.board[m[1][0]*8 + m[1][1]] is not None]
    except:
        print(moves)
        print(board.piece_pos)
        board.print_board()
    captures = order_moves(board.board, captures)

    if maximizing_player:
        for move in captures:
            captured_piece = board.make_move(move)
            score = quiescence(board, alpha, beta, False)
            board.undo_move(move, captured_piece)
            alpha = max(alpha, score)
            if alpha >= beta: break
        return alpha

    else:
        for move in captures:
            captured_piece = board.make_move(move)
            score =  quiescence(board, alpha, beta, True)
            board.undo_move(move, captured_piece)
            beta = min(beta, score)
            if alpha >= beta: break
        return beta

# score moves and assign value if a piece is captured to get better ordering for pruning
def score_move(move: tuple, board: list) -> int:
    if len(move) == 2:
        src, dest = move
        promoted_piece = None
    else:
        src, dest, promoted_piece = move
    src_row, src_col = src
    dest_row, dest_col = dest
    if board[dest_row*8+dest_col] is None:
        if promoted_piece:
            return PIECE_VALUES[promoted_piece[1]]
        return 0
    else:
        if promoted_piece:
            return PIECE_VALUES[promoted_piece[1]] + PIECE_VALUES[board[dest_row*8+dest_col][1]] - (PIECE_VALUES[board[src_row*8+src_col][1]]/10)
        return PIECE_VALUES[board[dest_row*8+dest_col][1]] - (PIECE_VALUES[board[src_row*8+src_col][1]]/10)
    
# oreder the sorted moves
def order_moves(board: list, moves: list) -> list:
    return sorted(moves, key=lambda m: score_move(m, board), reverse=True)