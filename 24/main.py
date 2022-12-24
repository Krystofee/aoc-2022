import functools
from collections import deque
from copy import deepcopy

STORM_MOVES = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0)
}


INV_STORM_MOVES = {
    v: k for k, v in STORM_MOVES.items()
}


class Storm:
    def __init__(self, x, y, dx, dy, maxx, maxy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.maxx = maxx
        self.maxy = maxy

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x < 0:
            self.x = self.maxx -1
        elif self.x >= self.maxx:
            self.x = 0

        if self.y < 0:
            self.y = self.maxy - 1
        elif self.y >= self.maxy:
            self.y = 0

    def copy(self):
        return Storm(self.x, self.y, self.dx, self.dy, self.maxx, self.maxy)

    def __repr__(self):
        return f"Storm(x: {self.x}, y:{self.y})"


init_storms = []
with open('input.txt', 'r') as file:
    inp = file.read()
    size_y = inp.count('\n') + 1
    for y, line in enumerate(inp.split('\n')):
        size_x = len(line)
        for x, char in enumerate(line):
            storm_move = STORM_MOVES.get(char)
            if storm_move:
                init_storms.append(Storm(
                    x, y, storm_move[0], storm_move[1], size_x, size_y
                ))


@functools.lru_cache(maxsize=None)
def get_storms_at_move_cached(move_count):
    result = deepcopy(init_storms)
    for _ in range(move_count):
        for storm in result:
            storm.move()
    return result


def get_storms_at_move(move_count):
    return get_storms_at_move_cached(move_count % period)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a*b) // gcd(a, b)


period = lcm(size_x, size_y)


print("lcm:", period)
print("size:", size_x, size_y)
print("------")


def construct_board(storms):
    board = [['.' for _ in range(size_x)] for _ in range(size_y)]
    for storm in storms:
        if board[storm.y][storm.x] == '.':
            board[storm.y][storm.x] = INV_STORM_MOVES[(storm.dx, storm.dy)]
        else:
            try:
                c = int(board[storm.y][storm.x]) + 1
            except:
                c = 2
            board[storm.y][storm.x] = str(c)
    return board


def print_board(board, x=None, y=None):
    print("----- BOARD -----")
    if x is not None and y is not None:
        try:
            board[y][x] = 'X'
        except:
            pass
    for line in board:
        print(''.join(line))
    print()


# print_board(construct_board(get_storms_at_move(0)))
# print_board(construct_board(get_storms_at_move(1)))
# print_board(construct_board(get_storms_at_move(2)))


def move_storms(storms):
    for storm in storms:
        storm.move()
    return storms


def can_move(tox, toy, storms, sx, sy):
    # Start is valid
    if tox == sx and toy == sy:
        return True

    # Check out of bounds
    if tox < 0 or tox >= size_x or toy < 0 or toy >= size_y:
        return False

    # Check if storm is in the way
    for storm in storms:
        if storm.x == tox and storm.y == toy:
            return False
    return True


POSSIBLE_MOVES = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
)


def find_exit_bfs(start_move, sx, sy, ex, ey):
    q = deque()
    visited = set()

    q.append((sx, sy, start_move))
    visited.add((sx, sy, start_move))

    while q:
        x, y, move_count = q.popleft()
        p_mc = (move_count + 1) % period
        # print_board(construct_board(get_storms_at_move(move_count)), x, y)
        # print("x:", x, "y:", y, "mc:", move_count, "p_mc:", p_mc)
        if x == ex and y == ey:
            return move_count + 1 - start_move

        # Check all possible moves
        for move in POSSIBLE_MOVES:
            tox, toy = x + move[0], y + move[1]
            if can_move(tox, toy, get_storms_at_move(move_count + 1), sx, sy) and (tox, toy, p_mc) not in visited:
                q.append((tox, toy, move_count + 1))
                visited.add((tox, toy, p_mc))

        # Check if can stay
        if can_move(x, y, get_storms_at_move(move_count + 1), sx, sy) and (x, y, p_mc) not in visited:
            q.append((x, y, move_count + 1))
            visited.add((x, y, p_mc))

    return -1


to_1 = find_exit_bfs(0, 0, -1, size_x - 1, size_y - 1)
print("to", to_1)
back = find_exit_bfs(to_1, size_x - 1, size_y, 0, 0)
print("back", back)
to_2 = find_exit_bfs(to_1 + back, 0, -1, size_x - 1, size_y - 1)
print("to", to_2)

print(to_1 + back + to_2)
