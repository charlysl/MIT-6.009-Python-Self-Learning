def neighbors(dimensions, r, c):
    all_neighbors = [(r+i, c+j) for i in range(-1,2) for j in range(-1, 2)]
    return [(x,y) for (x,y) in all_neighbors if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]]


def make_board(nrows, ncols, elem):
    return [[elem for c in range(ncols)] for r in range(nrows)]


def new_game(num_rows, num_cols, bombs):
    mask = make_board(num_rows, num_cols, False)
    board = make_board(num_rows, num_cols, 0)
    for br, bc in bombs:
        board[br][bc] = '.'
    for br, bc in bombs:
        for nr, nc in neighbors([num_rows, num_cols], br, bc):
            if board[nr][nc] != '.':
                board[nr][nc] += 1
    return {"dimensions": [num_rows, num_cols], "board" : board, "mask" : mask, "state": "ongoing"}


def is_victory(game):
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] == '.' and game["mask"][r][c]:
                return False
            if game['board'][r][c] != '.' and not game['mask'][r][c]:
                return False
    return True


def dump(game):
    lines = ["dimensions: {}".format(game["dimensions"]),
             "board: {}".format("\n       ".join(map(str, game["board"]))),
             "mask:  {}".format("\n       ".join(map(str, game["mask"])))]
    print("\n".join(lines))


def dig(game, row, col):
    if game['state'] != 'ongoing' or game['mask'][row][col]:
        return 0

    if game["board"][row][col] == '.':
        game["mask"][row][col] = True
        game['state'] = 'defeat'
        return 1

    count = 1
    game['mask'][row][col] = True
    if game['board'][row][col] == 0:
        for nr, nc in neighbors(game['dimensions'], row, col):
            count += dig(game, nr, nc)

    game['state'] = 'victory' if is_victory(game) else 'ongoing'
    return count


def render(game, xray=False):
    nrows, ncols = game['dimensions']
    board = [[None for i in range(ncols)] for j in range(nrows)]
    for r in range(nrows):
        for c in range(ncols):
            if xray or game['mask'][r][c]:
                current = board[r][c]
                if game['board'][r][c] == 0:
                    board[r][c] = ' '
                else:
                    board[r][c] = str(game['board'][r][c])
            else:
                board[r][c] = '_'
    return board


def render_ascii(game, xray=False):
    return "\n".join("".join(r) for r in render(game, xray=xray))
