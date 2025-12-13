from collections import Counter

def blink(condition: list)->list:

    new_condition = []

    for elem in condition:
        if elem == 0:
            new_condition.append(1)
        elif len(str(elem)) % 2 == 0:
            element_str = str(elem)
            midpoint = len(element_str) // 2
            new_condition.append(int(element_str[:midpoint]))
            new_condition.append(int(element_str[midpoint:]))
        else:
            new_condition.append(elem*2024)

    return new_condition

def faster_blink(condition: dict)->dict:
    """
    The actual location of the number is irrelevant as rules do not include adjacent numbers.
    As a list grows, so too the number of operations 
    aand past 30 blinks, the list is too large to process efficiently.

    Using a dictionary, we take advantage of the fact that a 0 anywhere in the list is subjected to the same rules,
    and thus we can apply the same rule to all 0's at once. Instead of iterating through the entire list

    Similarly a 17 will result in a '1' and '7' anywhere in the list regardless of its location.

    The dictionary will hold the number and the count of that number.
    After every iteration we create a new dict, and update it with new counts (but for all numbers at once)

    e.g.

    condition = {
    "17": 1
    "0" : 3
    }

    new_condition = {
    "1" : 2
    "7" : 1
    }

    """
    new_condition = {}

    for elem, count in condition.items():
        if elem == '0':
            new_condition['1'] = new_condition.get('1', 0) + 1 * count
        elif len(elem) % 2 == 0:
            midpoint = len(elem) // 2

            first_half = str(int(elem[:midpoint]))
            second_half = str(int(elem[midpoint:]))

            new_condition[first_half] = new_condition.get(first_half, 0) + 1 * count
            new_condition[second_half] = new_condition.get(second_half, 0) + 1 * count
        else:
            mul_2024 = str(int(elem)*2024)
            new_condition[mul_2024] = new_condition.get(mul_2024, 0) + 1 * count

    return new_condition

def get_total_stones(stone_counts):
    total = 0

    for stone, count in stone_counts.items():
        total += count
    
    return total


with open('./11/input.txt', 'r') as f:
    nums = [int(num) for num in f.read().split(' ')]

condition = nums
# condition = [125, 17]

for _ in range(25):
    condition = blink(condition)
    
print(f"Blinked {_+1} times, now there are {len(condition)} elements in the list")


num_as_strs = [str(num) for num in nums]
condition = dict(Counter(num_as_strs))
for _ in range(75):
    condition = faster_blink(condition)
    
print(f"Blinked {_+1} times, now there are {get_total_stones(condition)} elements in the list")
    
