import math


SNAFU_NUMBERS = (2, 1, 0, -1, -2)


def get_snafu_digit_value(digit, position):
    if digit == "-":
        digit = -1
    elif digit == "=":
        digit = -2
    else:
        digit = int(digit)
    multiplier = 5 ** position
    return digit * multiplier


def snafu_to_int(snafu):
    r = 0
    for i, c in enumerate(reversed(snafu)):
        r += get_snafu_digit_value(c, i)
    return r


def int_to_snafu_digit(digit):
    if digit == -1:
        return "-"
    elif digit == -2:
        return "="
    else:
        return str(digit)


def int_to_snafu_dfs(start, remaining, current_root):
    current_pow = 5 ** current_root

    if current_root == 0:
        if remaining in SNAFU_NUMBERS:
            return str(remaining)
        else:
            return None

    for n in SNAFU_NUMBERS:
        new_remaining = remaining - n * current_pow

        # This is the key, we prevent going out of bounds for smaller powers of 5
        if new_remaining != 0 and int(math.log(abs(new_remaining), 5)) > current_root - 1:
            continue

        result = int_to_snafu_dfs(start, new_remaining, current_root - 1)
        if result is not None:
            return int_to_snafu_digit(n) + result


def int_to_snafu(i):
    return int_to_snafu_dfs(i, i, int(math.log(i, 5)))


with open("input.txt", "r") as file:
    lines = file.readlines()

sum = 0
for line in lines:
    sum += snafu_to_int(line.strip())

x = int_to_snafu(sum)
print("DONE", x, "(sum check=", snafu_to_int(x), ")")
