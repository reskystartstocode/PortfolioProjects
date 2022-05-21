import random

def create_board():
    row = []
    board = []
    for _ in range(10):
        row.append(' ')
    for _ in range(10):
        board.append(row.copy())
    return board


def format_board(board):
    top = ' '.join('  ABCDEFGHIJ')
    row = []
    board_matrix = [top]
    for n, row in enumerate(board):
        if n + 1 < 10:
            row = f" {n + 1} |{'|'.join(row)}"
        else:
            row = f"{n + 1} |{'|'.join(row)}"
        board_matrix.append(row + '|')
    separator = '-'.join('+' * 11)
    board_matrix = f'\n   {separator}\n'.join(board_matrix) + f'\n   {separator}\n'
    print(board_matrix)


def alpha_to_coords(board_coords):
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    num = range(10)
    alpha_dict = dict(zip(alpha, num))
    if len(board_coords) == 2:
        system_coords = [alpha_dict[board_coords[0].upper()], int(board_coords[1]) - 1]
    elif len(board_coords) == 3:
        system_coords = [alpha_dict[board_coords[0].upper()], int(board_coords[-2:]) - 1]
    row = system_coords[1]
    col = system_coords[0]
    return row, col


def coords_to_alpha(row, col):
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    num = range(10)
    alpha_dict = dict(zip(num, alpha))
    board_coords = f"{alpha_dict[col]}{row + 1}"
    return board_coords

def ship_selector(classes):
    if classes == 'carrier':
        ship = 'Aircraft Carrier'
        cell = 5
    elif classes == 'battleship':
        ship = 'Battleship'
        cell = 4
    elif classes == 'destroyer':
        ship = 'Destroyer'
        cell = 3
    elif classes == 'submarine':
        ship = 'Submarine'
        cell = 3
    elif classes == 'patrol_boat':
        ship = 'Patrol Boat'
        cell = 2
    return ship, cell


def coords_input():
    # Format for input is 'A1','B5','E10' etc.
    # Returns the intended coordinate in the board.
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    while True:
        try:
            coords = input('Enter coordinates: ')
            if len(coords) < 2:
                print('Must be [A-J][1-10].')
            elif coords[0].upper() in alpha and int(coords[1]) in range(1, 11):
                break
            else:
                print('Must be [A-J][1-10].')
        except ValueError:
            print('Must be [A-J][1-10].')

    row, col = alpha_to_coords(coords)
    return row, col


def coords_input_head():
    # Format for input is 'A1','B5','E10' etc.
    # Returns the intended coordinate in the board.
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    while True:
        try:
            coords = input('Enter head coordinates: ')
            if len(coords) < 2:
                print('Must be [A-J][1-10].')
            elif coords[0].upper() in alpha and int(coords[1]) in range(1, 11):
                break
            else:
                print('Must be [A-J][1-10].')
        except ValueError:
            print('Must be [A-J][1-10].')

    num = range(10)
    alpha_dict = dict(zip(alpha, num))
    if len(coords) == 2:
        system_coords = [alpha_dict[coords[0].upper()], int(coords[1]) - 1]
    elif len(coords) == 3:
        system_coords = [alpha_dict[coords[0].upper()], int(coords[-2:]) - 1]
    row = system_coords[1]
    col = system_coords[0]
    return row, col


def coords_input_tail():
    # Format for input is 'A1','B5','E10' etc.
    # Returns the intended coordinate in the board.
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    while True:
        try:
            coords = input('Enter tail coordinates: ')
            if len(coords) < 2:
                print('Must be [A-J][1-10].')
            elif coords[0].upper() in alpha and int(coords[1]) in range(1, 11):
                break
            else:
                print('Must be [A-J][1-10].')
        except ValueError:
            print('Must be [A-J][1-10].')

    num = range(10)
    alpha_dict = dict(zip(alpha, num))
    if len(coords) == 2:
        system_coords = [alpha_dict[coords[0].upper()], int(coords[1]) - 1]
    elif len(coords) == 3:
        system_coords = [alpha_dict[coords[0].upper()], int(coords[-2:]) - 1]
    row = system_coords[1]
    col = system_coords[0]
    return row, col


def detect_existing(board, symbol):
    existing = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == symbol:
                existing.append([i, j])
    return existing


def check_existing(classes, board):
    exists = detect_existing(board, 'O')
    while True:
        try:
            head_row, head_col = coords_input_head()
            tail_coords = tail_coords_selector(classes, head_row, head_col)
            if [head_row, head_col] not in exists:
                break
            else:
                print('Must not be in existing ships!')
        except ValueError:
            print('Must not be in existing ships!')
    system_coords = []
    for i in tail_coords:
        system_coords.append(alpha_to_coords(i))
    for coords in system_coords:
        row, col = coords
        a, b = head_row, row
        c, d = head_col, col
        if row < head_row:
            a, b = row, head_row
        if col < head_col:
            c, d = col, head_col
        for i in range(a, b + 1):
            for j in range(c, d + 1):
                if board[i][j] != ' ':
                    tail_coords.remove(coords_to_alpha(row, col))
                    break
            else:
                continue
            break
    print(f"Available tail coordinates: {', '.join(tail_coords)}")
    while True:
        try:
            tail_row, tail_col = coords_input_tail()
            if coords_to_alpha(tail_row, tail_col) in tail_coords:
                break
            else:
                print('Tail must be in recommended coordinates!')
        except ValueError:
            print('Tail must be in recommended coordinates!')
    return head_row, head_col, tail_row, tail_col


def tail_coords_selector(classes, head_row, head_col):
    ship, cell = ship_selector(classes)
    choices = []
    tail_row = []
    tail_col = []
    tail_row.append(head_row - (cell - 1))
    tail_row.append(head_row + (cell - 1))
    tail_col.append(head_col - (cell - 1))
    tail_col.append(head_col + (cell - 1))
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    num = range(10)
    alpha_dict = dict(zip(num, alpha))
    for i in tail_row:
        if i >= 0 and i <= 9:
            choices.append(coords_to_alpha(i, head_col))
        else:
            continue
    for i in tail_col:
        if i >= 0 and i <= 9:
            choices.append(coords_to_alpha(head_row, i))
        else:
            continue
    return choices


def place_ship(fleet, board):
    for classes in fleet:
        format_board(board)
        ship, cell = ship_selector(classes)
        print(f"Place your {ship}!")
        while True:
            try:
                head_row, head_col, tail_row, tail_col = check_existing(classes, board)
                if (abs(head_row - tail_row) == (cell - 1) and head_col == tail_col) or (
                        abs(head_col - tail_col) == (cell - 1) and head_row == tail_row):
                    break
                else:
                    print(f'Must be {cell} tiles apart!')
            except ValueError:
                print(f'Must be {cell} tiles apart and in one line!')
        if abs(head_row - tail_row) == cell - 1:
            for row in range(min(head_row, tail_row), max(head_row, tail_row) + 1):
                board[row][head_col] = 'O'
        else:
            for col in range(min(head_col, tail_col), max(head_col, tail_col) + 1):
                board[head_row][col] = 'O'
        format_board(board)

def auto_place_ship(fleet, board):
    for classes in fleet:
        random.seed(random.randint(0,10000))
        ship, cell = ship_selector(classes)
        available_coords = detect_existing(board,' ')
        head_coords = available_coords[random.randint(0,len(available_coords)-1)]
        head_row = head_coords[0]
        head_col = head_coords[1]
        tail_coords = tail_coords_selector(classes, head_row, head_col)
        system_coords = []
        for i in tail_coords:
            system_coords.append(alpha_to_coords(i))
        for coords in system_coords:
            row, col = coords
            a, b = head_row, row
            c, d = head_col, col
            if row < head_row:
                a, b = row, head_row
            if col < head_col:
                c, d = col, head_col
            for i in range(a, b + 1):
                for j in range(c, d + 1):
                    if board[i][j] != ' ':
                        tail_coords.remove(coords_to_alpha(row, col))
                        break
                else:
                    continue
                break
        tail_row, tail_col = alpha_to_coords(tail_coords[random.randint(0,len(tail_coords)-1)])
        if abs(head_row - tail_row) == cell - 1:
            for row in range(min(head_row, tail_row), max(head_row, tail_row) + 1):
                board[row][head_col] = 'O'
        else:
            for col in range(min(head_col, tail_col), max(head_col, tail_col) + 1):
                board[head_row][col] = 'O'

def fire(player, player_board, enemy_board, target_board):
    print(f'{player}, where do you want to fire?')
    while True:
        try:
            row, col = coords_input()
            if target_board[row][col]  == ' ':
                break
            else:
                print('Must select new coordinates!')
        except ValueError:
            print('Must select new coordinates!')
    if enemy_board[row][col] == ' ':
        enemy_board[row][col] = '.'
        target_board[row][col] = '.'
        print("Miss!")
    elif enemy_board[row][col] == 'O':
        enemy_board[row][col] = 'X'
        target_board[row][col] = 'X'
        print("Hit!")
    player_display = merge_board(player_board, target_board, player)
    print(player_display)

def auto_fire(enemy_board, target_board):
    available_blanks = detect_existing(enemy_board,' ')
    available_ships = detect_existing(enemy_board,'O')
    available_coords = sorted(available_blanks + available_ships)
    coords = available_coords[random.randint(0, len(available_coords) - 1)]
    row = coords[0]
    col = coords[1]
    print(f"Your opponent shot at {coords_to_alpha(row, col)}!")
    if enemy_board[row][col] == ' ':
        enemy_board[row][col] = '.'
        target_board[row][col] = '.'
        print("Miss!")
    elif enemy_board[row][col] == 'O':
        enemy_board[row][col] = 'X'
        target_board[row][col] = 'X'
        print("Hit!")

def player_initialisation(player_name ,fleet):
    player_board = create_board()
    target_board = create_board()
    while True:
        try:
            placing = input(f'{player_name}: [manual] or [auto] ship placement?').lower()
            if placing == 'manual':
                place_ship(fleet, player_board)
                break
            elif placing == 'auto':
                auto_place_ship(fleet, player_board)
                break
            else:
                print("Must enter 'auto' or 'manual'")
        except ValueError:
            print("Must enter 'auto' or 'manual'")
    return player_board, target_board

def merge_board(player_board, target_board, player):
    top = [f'       Player {player} Board            Target Board']
    top.append(' '.join('  ABCDEFGHIJ') + '  ' + ' '.join('  ABCDEFGHIJ'))
    matrix = ['\n'.join(top)]
    for i in range(1,11):
        if i < 10:
            matrix.append(f" {i} |{'|'.join(player_board[i - 1])}|  {i} |{'|'.join(target_board[i - 1])}|")
        else:
            matrix.append(f"{i} |{'|'.join(player_board[i - 1])}| {i} |{'|'.join(target_board[i - 1])}|")
    separator = '-'.join('+' * 11)
    return f'\n   {separator}    {separator}\n'.join(matrix) + f'\n   {separator}    {separator}'

def navy():
    fleet = ['carrier','battleship','destroyer','submarine','patrol_boat']
    return fleet

def winning_condition(enemy_board):
    enemy_lives = 0
    for i in range(len(enemy_board)):
        for j in range(len(enemy_board[i])):
            if enemy_board[i][j] == 'O':
                enemy_lives += 1
    return enemy_lives == 0

def play_game(player1, player2):
    fleet = navy()
    player1_board, player1_target = player_initialisation(player1, fleet)
    player2_board, player2_target = player_initialisation(player2, fleet)
    turn = 1
    while turn <= 200:
        if turn % 2 == 1:
            player = player1
            player_board, enemy_board, target_board = player1_board, player2_board, player1_target
            player_display = merge_board(player_board, player1_target, player)
        else:
            player = player2
            player_board, enemy_board, target_board = player2_board, player1_board, player2_target
            player_display = merge_board(player_board, player2_target, player)
        print(f"{player} turn # {turn}")
        print(player_display)
        fire(player, player_board, enemy_board, target_board)
        input("Press Enter to continue")
        if winning_condition(enemy_board):
            print(f'Game Over! {player} wins!)')
            break
        turn += 1

def play_game_vs_comp(player1):
    fleet = navy()
    player1_board, player1_target = player_initialisation(player1, fleet)
    player_display = merge_board(player1_board, player1_target, player1)
    comp_board, comp_target = player_initialisation('COMP', fleet)
    turn = 1
    while turn <= 100:
        print(f"This is turn #{turn}")
        player_display = merge_board(player1_board, player1_target, player1)
        print(player_display)
        fire(player1, player1_board, comp_board, player1_target)

        auto_fire(player1_board,comp_target)
        turn += 1

play_game_vs_comp('X')