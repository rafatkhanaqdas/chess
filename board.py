import json

class Board:
    def __init__(self):
        self.board = ["bR","bN","bB","bQ","bK","bB","bN","bR",
                "bP","bP","bP","bP","bP","bP","bP","bP",
                None,None,None,None,None,None,None,None,
                None,None,None,None,None,None,None,None,
                None,None,None,None,None,None,None,None,
                None,None,None,None,None,None,None,None,
                "wP","wP","wP","wP","wP","wP","wP","wP",
                "wR","wN","wB","wQ","wK","wB","wN","wR"]
        self.piece_pos ={
            "wP" : [48, 49, 50, 51, 52, 53, 54, 55],
            "wR" : [56, 63],
            "wN" : [57, 62],
            "wB" : [58, 61],
            "wQ" : [59],
            "bP" : [8, 9, 10, 11, 12, 13, 14, 15],
            "bR" : [0, 7],
            "bN" : [1, 6],
            "bB" : [2, 5],
            "bQ" : [3]
        }
        self.wk_pos = 60
        self.bk_pos = 4
        # for castling
        self.w_Kside = True
        self.w_Qside = True
        self.b_Kside = True
        self.b_Qside = True
        # for en passant
        self.en_passant = {}

    def print_board(self):
        for row in range(0,8):
            print(8-row , end=" ")
            for cell in range(0,8):
                if self.board[row*8+cell] is None:
                    print("  ", end=" ")
                else:
                    print(self.board[row*8+cell], end=" ")
            print("")
        print ("  A  B  C  D  E  F  G  H")
    
    # make moves on the board
    def make_move(self, move: tuple):
        if len(move) == 2:
            src, dest = move
            promoted_piece = None
        else:
            src, dest, promoted_piece = move
        src_index = src[0]*8+src[1]
        dest_index = dest[0]*8+dest[1]
        piece = self.board[src_index]
        self.board[src_index] = None
        captured_piece = self.board[dest_index]
        undo_list = [captured_piece, self.w_Kside, self.w_Qside, self.b_Kside, self.b_Qside]
        self.board[dest_index] = piece
        if piece not in {"wK","bK"}:
            self.piece_pos[piece].remove(src_index)
            if piece == "wP" and src[0] - dest[0] == 2:
                self.en_passant = src[0]*8+8+src[1]
            if promoted_piece:
                self.piece_pos[promoted_piece].append(dest_index)
                self.board[dest_index] = promoted_piece
            else:
                self.piece_pos[piece].append(dest_index)
            if src_index == 63 and piece == "wR":
                self.w_Kside = False
            elif src_index == 56 and piece == "wR":
                self.w_Qside = False
            elif src_index == 7 and piece == "bR":
                self.b_Kside =  False
            elif src_index == 0 and piece == "bR":
                self.b_Qside = False
        elif piece == "wK":
            self.wk_pos = dest_index
            if self.w_Kside and dest[1] - src[1] == 2:
                self.board[63] = None
                self.board[61] = "wR"
                self.piece_pos["wR"].remove(63)
                self.piece_pos["wR"].append(61)
            elif self.w_Qside and src[1] - dest[1] == 2:
                self.board[56] = None
                self.board[59] = "wR"
                self.piece_pos["wR"].remove(56)
                self.piece_pos["wR"].append(59)
            self.w_Kside = False
            self.w_Qside = False
        else:
            self.bk_pos = dest_index
            if self.b_Kside and dest[1] - src[1] == 2:
                self.board[7] = None
                self.board[5] = "bR"
                self.piece_pos["bR"].remove(7)
                self.piece_pos["bR"].append(5)
            elif self.b_Qside and src[1] - dest[1] == 2:
                self.board[0] = None
                self.board[3] = "bR"
                self.piece_pos["bR"].remove(0)
                self.piece_pos["bR"].append(3)
            self.b_Kside = False
            self.b_Qside = False
        if captured_piece:
            self.piece_pos[captured_piece].remove(dest_index)
            if dest_index == 63 and captured_piece == "wR":
                self.w_Kside = False
            elif dest_index == 56 and captured_piece == "wR":
                self.w_Qside = False
            elif dest_index == 7 and captured_piece == "bR":
                self.b_Kside =  False
            elif dest_index == 0 and captured_piece == "bR":
                self.b_Qside = False
        return undo_list
    
    def undo_move(self, move: tuple, undo: list):
        if len(move) == 2:
            dest, src = move
            promoted_piece = None
        else:
            dest, src, promoted_piece = move
        src_index = src[0]*8+src[1]
        dest_index = dest[0]*8+dest[1]
        piece = self.board[src_index]
        self.board[src_index] = None
        self.board[dest_index] = piece
        if piece not in {"wK","bK"}:
            if promoted_piece:
                self.piece_pos[promoted_piece].remove(src_index)
                pawn =  "wP" if piece[0] == "w" else "bP"
                self.board[dest_index] = pawn
                self.piece_pos[pawn].append(dest_index)
            else:
                self.piece_pos[piece].remove(src_index)
                self.piece_pos[piece].append(dest_index)
        elif piece == "wK":
            self.wk_pos = dest_index
            if src[1] - dest[1] == 2 and not self.w_Kside:
                self.board[61] = None
                self.board[63] = "wR"
                self.piece_pos["wR"].remove(61)
                self.piece_pos["wR"].append(63)
            elif dest[1] - src[1] == 2 and not self.w_Qside:
                self.board[59] = None
                self.board[56] = "wR"
                self.piece_pos["wR"].remove(59)
                self.piece_pos["wR"].append(56)            
        else:
            self.bk_pos = dest_index
            if src[1] - dest[1] == 2 and not self.b_Kside:
                self.board[5] = None
                self.board[7] = "bR"
                self.piece_pos["bR"].remove(5)
                self.piece_pos["bR"].append(7)
            elif dest[1] - src[1] == 2 and not self.b_Qside:
                self.board[3] = None
                self.board[0] = "bR"
                self.piece_pos["bR"].remove(3)
                self.piece_pos["bR"].append(0)
        if undo[0]:
            self.board[src_index] = undo[0]
            self.piece_pos[undo[0]].append(src_index)
        self.w_Kside = undo[1]
        self.w_Qside = undo[2]
        self.b_Kside = undo[3]
        self.b_Qside = undo[4]