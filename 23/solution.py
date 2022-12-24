import math
from collections import defaultdict

# proposed_moves = {
#     (x, y): [move],
#     (toXY): listOfFrom[],
# }

# Elfs
#
# elfs = [[x, y], [x, y], ...]
#
#

board = []

with open("input_2.txt", "r") as file:
    board = file.read().split("\n")[:-1]

elfs = []

for y in range(len(board)):
    for x in range(len(board[y])):
        c = board[y][x]
        if c == "#":
            elfs.append((y, x))

elf_count = len(elfs)


# Y, X
# N, S, W, E
MOVES = [
    ((-1, 0), ((-1, -1), (-1, 0), (-1, 1))),  # N
    ((1, 0), ((1, 1), (1, 0), (1, -1))),  # S
    ((0, -1), ((1, -1), (0, -1), (-1, -1))),  # W
    ((0, 1), ((-1, 1), (0, 1), (1, 1))),  # E
]


def sum_coord(c1, c2):
    return (c1[0] + c2[0], c1[1] + c2[1])


def get_min_max(elfs):
    min_y, max_y = math.inf, -math.inf
    min_x, max_x = math.inf, -math.inf
    for (y, x) in elfs:
        min_y, max_y = min(y, min_y), max(y, max_y)
        min_x, max_x = min(x, min_x), max(x, max_x)
    return (
        (min_y, max_y),
        (min_x, max_x),
    )


def get_size(elfs):
    (min_y, max_y), (min_x, max_x) = get_min_max(elfs)
    return abs(min_y - max_y), abs(min_x - max_x)


def print_board(elfs):
    (min_y, max_y), (min_x, max_x) = get_min_max(elfs)
    board = []
    for i, y in enumerate(range(min_y, max_y + 1)):
        board.append("")
        for j, x in enumerate(range(min_x, max_x + 1)):
            if (y, x) in elfs:
                board[i] += "#"
            else:
                board[i] += "."
    for l in board:
        print(l)


def get_elf_moves(offset):
    return MOVES[offset:] + MOVES[:offset]


def should_stay(elfs, elf):
    all_directions = (
        (elf[0] - 1, elf[1]),
        (elf[0] + 1, elf[1]),
        (elf[0], elf[1] - 1),
        (elf[0], elf[1] + 1),
        (elf[0] - 1, elf[1] - 1),
        (elf[0] - 1, elf[1] + 1),
        (elf[0] + 1, elf[1] - 1),
        (elf[0] + 1, elf[1] + 1),
    )
    for dir in all_directions:
        if dir in elfs:
            return False
    return True


print("INITIAL")
print_board(elfs)


move_counter = 0
while move_counter < 10:
    proposed_moves = defaultdict(list)

    staying_elfs = []
    for elf in elfs:
        if should_stay(elfs, elf):
            staying_elfs.append(elf)
            continue
        found_move = False
        for move, to_check in get_elf_moves(move_counter % 4):
            check_failed = False
            for check in to_check:
                result_coord = sum_coord(elf, check)
                if result_coord in elfs:
                    check_failed = True
                    break
            if not check_failed:
                proposed_moves[sum_coord(elf, move)].append(elf)
                found_move = True
                break
        if not found_move:
            staying_elfs.append(elf)

    result_elfs = []
    for proposed_move, elfs in proposed_moves.items():
        if len(elfs) > 1:
            staying_elfs.extend(elfs)
        result_elfs.append(proposed_move)

    elfs = result_elfs + staying_elfs
    print("-------- MOVE", move_counter, "--------")
    print_board(elfs)
    move_counter += 1
    if len(elfs) != elf_count:
        raise Exception("fails")


size_y, size_x = get_size(elfs)
empty_count = size_x * size_y - len(elfs)


# print(get_min_max(elfs))
# print_board(elfs)
print(empty_count)
# for elf in elfs:
#     print(elf)
