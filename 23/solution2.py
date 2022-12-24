import math
from collections import defaultdict
from typing import Tuple

# proposed_moves = {
#     (x, y): [move],
#     (toXY): listOfFrom[],
# }

# Elfs
#
# elfs = [[x, y], [x, y], ...]
#
#

with open("input.txt", "r") as file:
    board = file.read().split("\n")[:-1]

initial_elfs = []

for y in range(len(board)):
    for x in range(len(board[y])):
        c = board[y][x]
        if c == "#":
            initial_elfs.append((y, x))

elf_count = len(initial_elfs)

# (Y, X)
# N, S, W, E
MOVES = (
    ((-1, 0), ((-1, -1), (-1, 0), (-1, 1))),  # N
    ((1, 0), ((1, 1), (1, 0), (1, -1))),  # S
    ((0, -1), ((1, -1), (0, -1), (-1, -1))),  # W
    ((0, 1), ((-1, 1), (0, 1), (1, 1))),  # E
)


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


def get_board(elfs):
    (min_y, max_y), (min_x, max_x) = get_min_max(elfs)
    board = []
    for i, y in enumerate(range(min_y, max_y + 1)):
        board.append("")
        for j, x in enumerate(range(min_x, max_x + 1)):
            if (y, x) in elfs:
                board[i] += "#"
            else:
                board[i] += "."
    return board


def print_board(elfs):
    board = get_board(elfs)
    for l in board:
        print(l)


def get_elf_moves(offset) -> Tuple[Tuple[int, int], Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
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


def get_free_square_count(elfs):
    print("----- FINAL -----")
    print_board(elfs)
    size_y, size_x = get_size(elfs)
    return (size_x + 1) * (size_y + 1) - len(elfs)


print("INITIAL")
print_board(initial_elfs)


def propose_elf_move(elfs, elf, moves):
    if should_stay(elfs, elf):
        return elf

    for move, to_check in moves:
        for check in to_check:
            if sum_coord(elf, check) in elfs:
                break
        else:
            return sum_coord(elf, move)

    return elf


def propose_elf_moves(elfs, move_index):
    result = defaultdict(list)
    moves = get_elf_moves(move_index)

    for elf in elfs:
        result[propose_elf_move(elfs, elf, moves)].append(elf)

    return result


def perform_elf_moves(proposed_moves):
    result = []
    for move, elfs_to_move in proposed_moves.items():
        if len(elfs_to_move) > 1:
            result.extend(elfs_to_move)
        else:
            result.append(move)
    return result


def compute_elfs(elfs, move_counter, max_moves):
    if move_counter >= max_moves:
        return elfs

    new_elfs = perform_elf_moves(propose_elf_moves(elfs, move_counter % 4))
    if new_elfs == elfs:
        print("MOVE COUNT", move_counter + 1)
        return elfs
    elfs = new_elfs

    if move_counter % 10 == 0:
        print("----- AFTER", move_counter + 1, "-----")
        print_board(elfs)

    return compute_elfs(elfs, move_counter + 1, max_moves)
    # if len(result) != elf_count:
    #     raise Exception("Not all elfs are alive, or too many elfs")
    # return result


print("Result:", get_free_square_count(compute_elfs(initial_elfs, move_counter=0, max_moves=math.inf)))
