import pygame

SIZE = 300

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_green = (0, 255, 0)
O_green = (144, 238, 144)
board_rows = 3
board_cols = 3
cell_size = 100 
dark_green = (0, 100, 0)
X = "X"
O = "O"
current_player = X
running = True
board = [[None for _ in range(board_cols)] for _ in range(board_rows)]
bestScore = 0


screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Tic tac toe")
clock = pygame.time.Clock()

def drawBoard():
    screen.fill(WHITE)
    if winner_check(board) == False:
        pygame.draw.line(screen, BLACK, (cell_size, 0), (cell_size, SIZE), 3)
        pygame.draw.line(screen, BLACK, (2 * cell_size, 0), (2 * cell_size, SIZE), 3)
        pygame.draw.line(screen, BLACK, (0, cell_size), (SIZE, cell_size), 3)
        pygame.draw.line(screen, BLACK, (0, 2 * cell_size), (SIZE, 2 * cell_size), 3)

        for row in range(board_rows):
            for col in range(board_cols):
                if board[row][col] == X:
                    pygame.draw.line(screen, X_green, (row * cell_size + 20, col * cell_size + 20), 
                                (row * cell_size + 80, col * cell_size + 80), 3)
                    pygame.draw.line(screen, X_green, (row * cell_size + 80, col * cell_size + 20), 
                                (row * cell_size + 20, col * cell_size + 80), 3)
                elif board[row][col] == O:
                    pygame.draw.circle(screen, O_green, (row * cell_size + 50, col * cell_size + 50), 30, 3)

def winner_check(board):
    for row in range(board_rows):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            if board[row][0] == X:
                return X
            else:
                return O
    for col in range(board_cols):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            if board[0][col] == X:
                return X
            return O
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        if board[0][0] == X:
            return X
        return O
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        if board[0][2] == X:
            return X
        return O

    return False

def gameEnd(board):
    font = pygame.font.Font('freesansbold.ttf', 32)
    if winner_check(board) == False and board_full(board):
        text = font.render("TIE", True, dark_green)
        textRect = text.get_rect()
        textRect.center = (150, 150)
        screen.fill(WHITE)
        screen.blit(text, textRect)

    if winner_check(board) == X:
        text = font.render("You won!", True, dark_green)
        textRect = text.get_rect()
        textRect.center = (150, 150)
        screen.fill(WHITE)
        screen.blit(text, textRect)

    if winner_check(board) == O:
        text = font.render("Computer won!", True, dark_green)
        textRect = text.get_rect()
        textRect.center = (150, 150)
        screen.fill(WHITE)
        screen.blit(text, textRect)
    
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    exit()


def board_full(board):
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == None:
                return False            
    return True

def minimax(board, depth, isMaximizing):
    if winner_check(board) == X:
        return 1
    if winner_check(board) == O:
        return -1
    if board_full(board):
        return 0

    if isMaximizing:
        bestScore = -float('inf')
        bestMove = None
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = X
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    if score > bestScore:
                        bestScore = score
                        bestMove = (row, col)
        if depth == 0 and bestMove is not None:
            return bestMove
        return bestScore
    else:
        bestScore = float('inf')
        bestMove = None
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = O
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    if score < bestScore:
                        bestScore = score
                        bestMove = (row, col)
        if depth == 0 and bestMove is not None:
            return bestMove
        return bestScore







while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif current_player == X and e.type == pygame.MOUSEBUTTONUP:
            x, y = e.pos
            row, col = x // cell_size, y // cell_size
            if board[row][col] == None:
                board[row][col] = current_player
                current_player = O
    if current_player == O:
        move = minimax(board, 0, False)
        if move is None or move is 0:
            gameEnd(board)
        (row, col) = move
        board[row][col] = current_player
        current_player = X
    
    if current_player == O:
        if type(minimax(board, 0, True)) != list:
            gameEnd(board)

        [row, col] = minimax(board, current_player, True)
        board[row][col] = current_player
        current_player = X

    pygame.display.flip()
    if board_full(board) or winner_check(board) != False:
        gameEnd(board)
    else:    
        drawBoard()
    clock.tick(60)
quit()

