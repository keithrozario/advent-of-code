def max_joltage(battery: str) -> int:

    largest_number_index = -1
    largest_number = ""
    max_number_length = 12
    for i in range(1,max_number_length+1):
        if max_number_length - i == 0:
            # empty and zero (or negative 0) do not mean the same thing
            new_battery = battery[largest_number_index+1:]
        else:
            new_battery = battery[largest_number_index+1:-(max_number_length-i)]
        largest_number_in_range = max([int(x) for x in new_battery])
        largest_number_index += new_battery.find(str(largest_number_in_range)) + 1 
        largest_number += battery[largest_number_index]

    return int(largest_number)

def total_joltage(batteries: list)->int:
    total_joltage = 0 
    for battery in batteries:
        total_joltage += max_joltage(battery=battery.strip())
    return total_joltage


if __name__ == "__main__":
    assert max_joltage("987654321111111") == 987654321111
    assert max_joltage("811111111111119") == 811111111119
    assert max_joltage("234234234234278") == 434234234278
    assert max_joltage("818181911112111") == 888911112111

    with open("./2025/03/sample.txt", 'r') as sample_file:
        batteries = sample_file.readlines()
    print(f"Total Joltage: {total_joltage(batteries=batteries)}")

    with open("./2025/03/input.txt", 'r') as sample_file:
        batteries = sample_file.readlines()
    print(f"Total Joltage: {total_joltage(batteries=batteries)}")
