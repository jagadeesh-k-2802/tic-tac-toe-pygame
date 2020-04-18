# <==================[SETUP]==================> #
import pygame
import random
pygame.init()

win = pygame.display.set_mode((450, 500))
pygame.display.set_caption("Tic Tac Toe - Game")
circle_icon = pygame.image.load('resources/circle.png')
x_icon = pygame.image.load('resources/x_symbol.png')
run = True

inner_board = ['-'] * 9
player_score = ai_score = 0

zero = pygame.image.load('resources/0.png')
one = pygame.image.load('resources/1.png')
two = pygame.image.load('resources/2.png')
three = pygame.image.load('resources/3.png')
game_over = pygame.image.load('resources/game_over.png')

position_mappings = [
    [(36, 164), (111, 221), (50, 115), 0],
    [(162, 308), (111, 221), (188, 115), 1],
    [(308, 428), (111, 221), (319, 115), 2],

    [(36, 164), (220, 358), (50, 243), 3],
    [(162, 308), (220, 358), (188, 243), 4],
    [(308, 428), (220, 358), (319, 243), 5],

    [(36, 156), (361, 473), (50, 374), 6],
    [(162, 308), (361, 473), (188, 374), 7],
    [(308, 428), (361, 473), (319, 374), 8]
]

drawed = []


# <===========================================> #


def show_score():
    if player_score == 0:
        win.blit(zero, (182,8))
    elif player_score == 1:
        win.blit(one, (182, 8))
    elif player_score == 2:
        win.blit(two, (182, 8))
    else:
        win.blit(three, (182, 8))

    if ai_score == 0:
        win.blit(zero, (239, 8))
    elif ai_score == 1:
        win.blit(one, (239, 8))
    elif ai_score == 2:
        win.blit(two, (239, 8))
    else:
        win.blit(three, (239, 8))


def reset_board(board):
    bg_color_num = random.randint(1, 4)
    bg = pygame.image.load('resources/board_bg' + str(bg_color_num) + '.png')
    win.blit(bg, (0,0))
    show_score()

    for i in range(9):
        board[i] = '-'

    drawed.clear()


reset_board(inner_board)

def mapper(x, y):
    """
    position_mappings
    -----------------
    [x1, x2] [y1, y2], [to_draw_symbol], [location_in_board]

    This function will return the best (x,y) co-ordinates to draw
    based on given (x,y) co-ordinates
    """

    for position in position_mappings:
        if position[0][0] < x < position[0][1] and position[1][0] < y < position[1][1]:
            mapped_value = (position[2], position[3])
            return mapped_value


def select_possible_moves(board, moves):
    possible_moves = [move for move in moves if board[move] == '-']

    if len(possible_moves) == 0:
        return None
    return random.choice(possible_moves)


def is_winner(tag, board):
    # CHECKS ROWS
    if board[0] == tag and board[1] == tag and board[2] == tag:
        return True
    elif board[3] == tag and board[4] == tag and board[5] == tag:
        return True
    elif board[6] == tag and board[7] == tag and board[8] == tag:
        return True
    # CHECKS COLUMNS
    elif board[0] == tag and board[3] == tag and board[6] == tag:
        return True
    elif board[1] == tag and board[4] == tag and board[7] == tag:
        return True
    elif board[2] == tag and board[5] == tag and board[8] == tag:
        return True
    # CHECKS DIAGONALS
    elif board[0] == tag and board[4] == tag and board[8] == tag:
        return True
    elif board[2] == tag and board[4] == tag and board[6] == tag:
        return True
    return False


def is_board_filled(board):
    if board.count('-') == 0:
        return True
    return False


def is_game_over():
    global player_score, ai_score

    if is_winner("X", inner_board):
        print("Player \"X\" Won The Game")
        player_score += 1
        return True

    elif is_winner("O", inner_board):
        print("Computer \"O\" Won The Game")
        ai_score += 1
        return True

    elif is_board_filled(inner_board):
        print("The game is draw")
        return True
    return False


def ai_move(board):
    # CHECKS IF AI CAN WIN IN ONE MOVE
    for i in range(0, 9):
        copied_board = [square for square in board]
        if copied_board[i] == '-':
            copied_board[i] = "O"
        if is_winner("O", copied_board):
            return i

    # CHECK IF PLAYER CAN WIN IN ONE MOVE IF YES BLOCK HIM
    for i in range(0, 9):
        copied_board = [square for square in board]
        if copied_board[i] == '-':
            copied_board[i] = "X"
        if is_winner("X", copied_board):
            return i

    # TAKE CORNERS IF THEY ARE FREE
    corner = select_possible_moves(board, (6, 8, 0, 2))
    if corner != None:
        return corner

    # TAKE CENTER IF IT'S FREE
    if board[4] == '-':
        return 4

    # MOVE ONE OF THE SIDES -> 7 3 5 1
    sides = select_possible_moves(board, (7, 3, 5, 1))
    if sides:
        return sides

# <===========================================> #

# Game Loop
while run:
    if player_score == 3 or ai_score == 3:
        win.blit(game_over, (0 ,0))
        show_score()

        i = 0
        while i < 500:
            pygame.time.delay(1)
            i += 1
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()

                if keys[pygame.K_SPACE]:
                    player_score = 0
                    ai_score = 0
                    reset_board(inner_board)

                if event.type == pygame.QUIT:
                    i = 501
                    run = False

    pygame.time.delay(100)

    # Is Game Over
    if is_game_over():
        pygame.time.delay(1000)
        reset_board(inner_board)

    # Close Button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # On Mouse Click
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Player's Choice
            mapped_value = mapper(x, y)

            try:
                if mapped_value[1] in drawed:
                    continue

                if inner_board[mapped_value[1]] == "-":
                    win.blit(x_icon, mapped_value[0])
                    inner_board[mapped_value[1]] = "X"
                    drawed.append(mapped_value[1])
                    pygame.display.update()

            except TypeError:
                pass

            else:
                # Computer's Choice
                choosed = ai_move(inner_board)

                for position in position_mappings:
                    if position[3] == choosed:
                        i = 0
                        while i < 190:
                            pygame.time.delay(1)
                            i += 1

                        win.blit(circle_icon, (position[2]))
                        inner_board[position[3]] = "O"
                        drawed.append(position[3])


    # Grab The Input Keys
    keys = pygame.key.get_pressed()

    # ALT + F4 Shorcut Will Close The Game
    if keys[pygame.K_LALT] and keys[pygame.K_F4]:
        run = False

    pygame.display.update()

pygame.quit()
