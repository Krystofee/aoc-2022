import math

with open("input.txt", "r") as file:
    lines = file.readlines()


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
    # print("TO INT")
    r = 0
    for i, c in enumerate(reversed(snafu)):
        # print(i, c, get_snafu_digit_value(c, i))
        r += get_snafu_digit_value(c, i)
    return r


sum = 0
for line in lines:
    sum += snafu_to_int(line.strip())


print("SUM", sum)


max_root = math.log(sum, 5)


SNAFU_NUMBERS = (2, 1, 0, -1, -2)


def int_to_snafu_digit(digit):
    if digit == -1:
        return "-"
    elif digit == -2:
        return "="
    else:
        return str(digit)


def find_snafu_from_int_dfs(start, remaining, current_root):
    current_pow = 5 ** current_root

    # Prevent going too high
    if start < remaining:
        return None

    if current_root == 0:
        if remaining in SNAFU_NUMBERS:
            return str(remaining)
        else:
            print("ERROR", remaining)
            return None

    if remaining == 0:
        return "0" * current_root

    for n in SNAFU_NUMBERS:
        new_remaining = remaining - n * current_pow

        if new_remaining != 0 and int(math.log(abs(new_remaining), 5)) > current_root - 1:
            continue

        result = find_snafu_from_int_dfs(start, new_remaining, current_root - 1)
        if result is not None:
            return int_to_snafu_digit(n) + result


def int_to_snafu(i):
    # print("TO SNAFU")
    return find_snafu_from_int_dfs(i, i, int(math.log(i, 5)))


print("FINDING")
x = int_to_snafu(sum)
print("DONE", x, "check=", snafu_to_int(x))
