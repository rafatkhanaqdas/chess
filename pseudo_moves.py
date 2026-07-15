# get enemy color based on position
def get_eny_color(board: list, pos: tuple):
    row, col = pos
    if board[row*8+col][0] =="w":
        return "b"
    else:
        return "w"

# pawn moves
def get_pawn_moves(board: list ,pos : tuple): 
    legal = []
    row , col = pos
    if board[row*8+col][0] == "w":
        if row != 0:
            if board[(row-1)*8+col] is None:
                legal.append((row-1,col))
                if row == 6 and board[(row-2)*8+col] is None:
                    legal.append((row-2,col))
            if col!=7 and board[(row-1)*8+col+1] is not None:
                if board[(row-1)*8+col+1][0]=="b":
                    legal.append((row-1,col+1))
            if col!=0 and board[(row-1)*8+col-1] is not None:
                if board[(row-1)*8+col-1][0]=="b":
                    legal.append((row-1,col-1))
    # black pawn
    else:
        if row != 7:
            if board[(row+1)*8+col] is None:
                legal.append((row+1,col))
                if row == 1:
                    if board[(row+2)*8+col] is None:
                        legal.append((row+2,col))
            if col!=7 and board[(row+1)*8+col+1] is not None:
                if board[(row+1)*8+col+1][0]=="w":
                    legal.append((row+1,col+1))
            if col!=0 and board[(row+1)*8+col-1] is not None:
                if board[(row+1)*8+col-1][0]=="w":
                    legal.append((row+1,col-1))
    return legal

# knigth moves
def get_knight_moves(board: list, pos: tuple):
    legal = []
    row, col = pos
    eny_color = get_eny_color(board, pos)
    if col != 7 and row not in [0,1]:
        if board[(row-2)*8+col+1] is None or board[(row-2)*8+col+1][0]==eny_color:
            legal.append((row-2,col+1))
    if col != 0 and row not in [0,1]:
        if board[(row-2)*8+col-1] is None or board[(row-2)*8+col-1][0]==eny_color:
            legal.append((row-2,col-1))
    if col != 7 and row not in [6,7]:
        if board[(row+2)*8+col+1] is None or board[(row+2)*8+col+1][0]==eny_color:
            legal.append((row+2,col+1))
    if col != 0 and row not in [6,7]:
        if board[(row+2)*8+col-1] is None or board[(row+2)*8+col-1][0]==eny_color:
            legal.append((row+2,col-1))
    if row != 7 and col not in [0,1]:
        if board[(row+1)*8+col-2] is None or board[(row+1)*8+col-2][0]==eny_color:
            legal.append((row+1,col-2))
    if row != 0 and col not in [0,1]:
        if board[(row-1)*8+col-2] is None or board[(row-1)*8+col-2][0]==eny_color:
            legal.append((row-1,col-2))
    if row != 7 and col not in [6,7]:
        if board[(row+1)*8+col+2] is None or board[(row+1)*8+col+2][0]==eny_color:
            legal.append((row+1,col+2))
    if row != 0 and col not in [6,7]:
        if board[(row-1)*8+col+2] is None or board[(row-1)*8+col+2][0]==eny_color:
            legal.append((row-1,col+2))
    return legal

# king moves
def get_king_moves(board: list, pos: tuple):
    legal =  []
    row, col = pos
    eny_color = get_eny_color(board,pos)
    if row != 7:
        if board[(row+1)*8+col] is None or board[(row+1)*8+col][0] == eny_color:
            legal.append((row+1,col))
        if col != 7:
            if board[(row+1)*8+col+1] is None or board[(row+1)*8+col+1][0] == eny_color:
                legal.append((row+1,col+1))
        if col != 0:
            if board[(row+1)*8+col-1] is None or board[(row+1)*8+col-1][0] == eny_color:
                legal.append((row+1,col-1))
    if row != 0:
        if board[(row-1)*8+col] is None or board[(row-1)*8+col][0] == eny_color:
            legal.append((row-1,col))
        if col != 7:
            if board[(row-1)*8+col+1] is None or board[(row-1)*8+col+1][0] == eny_color:
                legal.append((row-1,col+1))
        if col != 0:
            if board[(row-1)*8+col-1] is None or board[(row-1)*8+col-1][0] == eny_color:
                legal.append((row-1,col-1))
    if col != 0:
        if board[row*8+col-1] is None or board[row*8+col-1][0] == eny_color:
            legal.append((row,col-1))
    if col != 7:
        if board[row*8+col+1] is None or board[row*8+col+1][0] == eny_color:
            legal.append((row,col+1))
    return legal

# rook moves
def get_rook_moves(board: list, pos: tuple):
    legal = []
    row, col = pos
    eny_color = get_eny_color(board, pos)
    if row != 7:
        for i in range(row+1,8):
            if board[i*8+col] is None:
                legal.append((i,col))
            elif board[i*8+col][0] == eny_color:
                legal.append((i,col))
                break
            else:
                break
    if row != 0:
        for i in range(row-1,-1,-1):
            if board[i*8+col] is None:
                legal.append((i,col))
            elif board[i*8+col][0] == eny_color:
                legal.append((i,col))
                break
            else:
                break
    if col != 7:
        for i in range(col+1,8):
            if board[row*8+i] is None:
                legal.append((row,i))
            elif board[row*8+i][0] == eny_color:
                legal.append((row,i))
                break
            else:
                break    
    if col != 0:
        for i in range(col-1,-1,-1):
            if board[row*8+i] is None:
                legal.append((row,i))
            elif board[row*8+i][0] == eny_color:
                legal.append((row,i))
                break
            else:
                break
    return legal

# bishop moves
def get_bishop_moves(board: list, pos: tuple):
    legal = []
    row, col = pos
    eny_color = get_eny_color(board, pos)
    while row < 7 and col < 7:
        if board[(row+1)*8+col+1] is None:
            legal.append((row+1,col+1))
        elif board[(row+1)*8+col+1][0] == eny_color:
            legal.append((row+1,col+1))
            break
        else:
            break
        row+=1
        col+=1
    row, col = pos
    while row > 0 and col < 7:
        if board[(row-1)*8+col+1] is None:
            legal.append((row-1,col+1))
        elif board[(row-1)*8+col+1][0] == eny_color:
            legal.append((row-1,col+1))
            break
        else:
            break
        row-=1
        col+=1
    row, col = pos
    while row < 7 and col > 0:
        if board[(row+1)*8+col-1] is None:
            legal.append((row+1,col-1))
        elif board[(row+1)*8+col-1][0] == eny_color:
            legal.append((row+1,col-1))
            break
        else:
            break
        row+=1
        col-=1
    row, col = pos
    while row > 0 and col > 0:
        if board[(row-1)*8+col-1] is None:
            legal.append((row-1,col-1))
        elif board[(row-1)*8+col-1][0] == eny_color:
            legal.append((row-1,col-1))
            break
        else:
            break
        row-=1
        col-=1
    return legal

# queen moves
def get_queen_moves(board: list, pos: tuple):
    return get_rook_moves(board, pos)+get_bishop_moves(board, pos)
