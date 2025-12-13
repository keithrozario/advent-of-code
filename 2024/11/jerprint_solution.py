def load_data(file):
    with open(file) as f:
        data = f.read()
    return list(data.split())



def update_stone(stone):

    if stone == "0":
        return ["1"]

    elif len(stone) % 2 == 0:
        L = len(stone)
        first_half = str(int(stone[:L//2]))
        second_half = str(int(stone[L//2:]))



        return [first_half, second_half]
    else:
        return [str(int(stone)*2024)]


def blink(stones):
    new_stones = []
    for stone in stones:
        next_stones = update_stone(stone)
        new_stones.extend(next_stones)
    return new_stones


stones = load_data("./11/input.txt")
blinks = 25
for i in range(blinks):
    stones = blink(stones)

print(len(stones))




## Part two

# Use a dict to keep track instead of a list

def get_counts(stones):
    counts = {}
    for stone in stones:
        counts[stone] = counts.get(stone, 0) + 1

    return counts


def blink(stone_counts):
    new_counts = {}
    for stone, count in stone_counts.items():
        new_stones = update_stone(stone)

        for s in new_stones:
            new_counts[s] = new_counts.get(s, 0) + 1 * count

    return new_counts


def get_total_stones(stone_counts):
    total = 0

    for stone, count in stone_counts.items():
        total += count
    return total


stones = load_data("./11/input.txt")
stone_counts = get_counts(stones)
blinks = 75

for idx in range(blinks):
    stone_counts = blink(stone_counts)

print(get_total_stones(stone_counts))
