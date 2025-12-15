def max_joltage(battery: str) -> int:
    last_found_index = -1
    result_digits = []
    max_number_length = 12
    battery_len = len(battery)

    # We need to select `max_number_length` digits
    for i in range(max_number_length):
        digits_to_pick_later = (max_number_length - 1) - i
        search_start = last_found_index + 1
        search_end = battery_len - digits_to_pick_later

        search_window = battery[search_start:search_end]
        best_digit = max(search_window)
        # Find the index of the best digit within the current search window.
        relative_index = search_window.find(best_digit)
        
        last_found_index = search_start + relative_index
        
        result_digits.append(best_digit)

    return int("".join(result_digits))

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
