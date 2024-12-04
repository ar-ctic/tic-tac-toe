import random
import time

def getUserCoordinates(board):
    """
    Returns user input coordinates
    
    @params {list} board: current game board
    
    @returns {int, int}: row and col 
    """
    
    length1 = len(board)
    length2 = len(board[0])
    
    while True:
        try: 
            row: int = int(input(f"Enter Row (1-{length1}): "))
            col: int = int(input(f"Enter Column (1-{length2}): "))
            
            if not (1 <= row <= length1) or not (1 <= col <= length2):  
                raise Exception("Input out of bounds.")

            row -= 1
            col -= 1

            if board[row][col] != '#':
                raise Exception(f"Board on {row} {col} is already filled.")
                    
            return row, col
                    
        except ValueError as error:
            print("Input must be integer.")
        
        except Exception as error:
            print(error)

def getComputerCoordinates(board):
    """
    TODO: Create better engine with difficulties. Maybe train AI
    
    Computer selects random '#' in board
    
    @params {list} - 2d list board
    
    @returns {int, int} - row and col of board
    """
    length1 = len(board)-1
    length2 = len(board[0])-1
    
    while True:
        row = random.randint(0, length1)
        col = random.randint(0, length2)

        if board[row][col] == '#':
            return row, col



def checkHorizontal(board, lengthToWin):
    
    for row in board:
        x_cnt = o_cnt = 0
        for item in row:
            if item == 'x':
                x_cnt+=1
                o_cnt=0
            elif item == 'o':
                o_cnt+=1
                x_cnt=0
            else:
                x_cnt = o_cnt = 0
                
            if x_cnt >= lengthToWin or o_cnt >= lengthToWin:
                return True

    return None


def isWinDiagonal(board, lengthToWin, row, col, symbol):
    """
    Checks if lengthToWin symbols are in one diagonal line
    
    @params {list} board - 2d list board
    @params {int} lengthToWin - amount of symbols in one line to win
    @params {int} row - index of row 
    @params {int} col - index of col
    @params {char} symbol - symbol of current player ('x', 'o')
    
    @returns {bool} - returns True if won else False
    """

    # Diagonal counter - increments if diagonal symbol is same else resets
    diag_r_cnt = diag_l_cnt = 0
    
    """
    Checks if a position on board is even relevant to consider, as the most right element can´t have a diagonal to the right.
    LengthToWin = 3
    #X#
    ##X     As shown we don´t even need to consider board[0][1]
    ###(X)
    
    First check checks if there are enough rows, second if there are enough cols
    """
    if row + lengthToWin <= len(board) and col + lengthToWin <= len(board[0]):
        for k in range(lengthToWin):
            if board[row+k][col+k] == symbol:
                diag_r_cnt +=1
            else:
                diag_r_cnt = 0
                
    if diag_r_cnt >= lengthToWin:
        return True
            
    """
    Same as above but checks diagonal to the left
    """
    if row + lengthToWin <= len(board) and col - lengthToWin + 1 >= 0:
        for k in range(lengthToWin):
            if board[row+k][col-k] == symbol:
                diag_l_cnt +=1
            else:
                diag_l_cnt = 0

    if diag_l_cnt >= lengthToWin:
        return True
    
    return False
                    
                    
def checkDiagonals(board, lengthToWin):
    """
    Organizer function
    
    @params {list} board - 2d list board
    @params {int} lengthToWin - amount of symbols in one line to win
    
    @returns {bool} - True if won else False
    """
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            isWin_x = isWinDiagonal(board, lengthToWin, i, j, 'x')
            isWin_o = isWinDiagonal(board, lengthToWin, i, j, 'o')
            
            if isWin_x or isWin_o:
                return True
    
    return False
        
def checkWin(board, lengthToWin):
    """
    TODO: Only check for relevant symbol (player that made the move)
    TODO: Cache indexes that don´t need to be checked anymore 
    xo#
    oo# board[0][0] can be ignored
    ###
     
    Checks if winning criteria is met: LengthToWin symbols in one line (straight and diagonal)
    
    @params {list} board - 2d list board
    @params {int} lengthToWin - amount of symbols in one line to win
    
    @returns {bool} isWin - Returns True if won else False
    """
    isWin = checkHorizontal(board, lengthToWin)
    if isWin:
        return isWin
    # Rotate board 90° counter-clockwise to use checkHorizontal() function again
    rotatedBoard: list = [list(row) for row in zip(*board)][::-1]
    isWin = checkHorizontal(rotatedBoard, lengthToWin)
    if isWin:
        return isWin
        
    isWin = checkDiagonals(board, lengthToWin)
        
    return isWin

def printBoard(board):
    """
    Prints out the board with spaceholders
    
    @params {list} - 2d list board
    """
    for row in board:
        for col in row:
            print(f" {col}", end=" |")
            
        print()
        for col in row:
            print('───|',end="")
            
        print()


def gameLoop(rows, cols, lengthToWin):
    
    player1_symbol = 'x'
    player2_symbol = 'o'
    
    player1_toMove = random.choice([True, False])
    
    if not player1_toMove:
        player1_symbol = 'o'
        player2_symbol = 'x'
    
    board = [['#' for _ in range(cols)] for _ in range(rows)]
    
    printBoard(board)
    
    while True:
        
        if player1_toMove:
            print("\nYOUR MOVE")
            row, col = getUserCoordinates(board)
            board[row][col] = player1_symbol
            player1_toMove = False
            
        else:
            print("\nCOMPUTER MOVES")
            time.sleep(1)
            row, col = getComputerCoordinates(board)
            board[row][col] = player2_symbol
            player1_toMove = True
            
        printBoard(board)
        isWin = checkWin(board, lengthToWin)
        
        print()
        if isWin:
            print(f"Winner is: {player2_symbol if player1_toMove else player1_symbol}!")
            return
       
        isDraw = True
        for row in board:
            if not '#' in row:
                continue
            isDraw = False
        if isDraw:
            print("DRAW")
            return
     
def getBoardInfo():
    while True:
        try: 
            rows: int = int(input(f"Enter Rows (int): "))
            cols: int = int(input(f"Enter Columns (int): "))
            lengthToWin: int = int(input(f"Enter Length to Win (int): "))
            
            if rows <= 0 or cols <= 0 or lengthToWin <= 0:
                raise Exception("Rows/Cols or Length to Win can´t be 0 or less.")
                  
            if lengthToWin > rows or lengthToWin > cols:
                raise Exception("Length to win can´t be greater than Rows or Cols")
                    
            return rows, cols, lengthToWin
                    
        except ValueError as error:
            print("Input must be integer.")
        
        except Exception as error:
            print(error)

        
def main():
    print("TIC TAC TOE")
    rows, cols, lengthToWin = getBoardInfo()
    gameLoop(rows, cols, lengthToWin)
    
    


if __name__ == '__main__':
    main()