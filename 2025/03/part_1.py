def max_joltage(battery: str) -> int:
    largest_number = max([int(x) for x in battery[:-1]])
    largest_number_index = battery.find(str(largest_number))
    second_largest_number = max([int(x) for x in battery[largest_number_index+1:]])
    return largest_number*10 + second_largest_number

def total_joltage(batteries: list)->int:
    total_joltage = 0 
    for battery in batteries:
        total_joltage += max_joltage(battery=battery.strip())
    return total_joltage


if __name__ == "__main__":
    assert max_joltage("987654321111111") == 98
    assert max_joltage("811111111111119") == 89 
    assert max_joltage("234234234234278") == 78
    assert max_joltage("818181911112111") == 92

    with open("./2025/03/sample.txt", 'r') as sample_file:
        batteries = sample_file.readlines()
    print(f"Total Joltage: {total_joltage(batteries=batteries)}")

    with open("./2025/03/input.txt", 'r') as sample_file:
        batteries = sample_file.readlines()
    print(f"Total Joltage: {total_joltage(batteries=batteries)}")
