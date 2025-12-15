def is_valid(id: str)->bool:
    """
    Args:
        id: the id to check
    returns:
        bool: if the id is valid or not
    """
    id_len = len(id)
    if id_len % 2 == 0:
        middle_index = int(id_len/2)
        if id[middle_index:] == id[:middle_index]:
            return False

    return True

def get_invalid_ids(number_ranges: list[str])->list:

    invalid_ids = []
    for number_range in number_ranges:
        start_num,end_num = number_range.split("-")
        for i in range(int(start_num), int(end_num)+1):
            if not is_valid(str(i)):
                invalid_ids.append(i)
    
    return invalid_ids

def sum_invalid_ids(invalid_ids: list[int])->int:
    total = 0
    for id in invalid_ids:
        total += id
    print(total)
    return total

if __name__ == "__main__":
    assert is_valid("11") == False
    assert is_valid("123") == True
    assert is_valid("99") == False
    assert is_valid("123123") == False
    assert is_valid("123144") == True
    assert is_valid("1188511885") == False

    with open('./2025/02/sample.txt', 'r') as sample_file:
        number_ranges = sample_file.read().split(",")

    invalid_ids = get_invalid_ids(number_ranges)
    total = sum_invalid_ids(invalid_ids)

    with open('./2025/02/input.txt', 'r') as sample_file:
        number_ranges = sample_file.read().split(",")

    invalid_ids = get_invalid_ids(number_ranges)
    total = sum_invalid_ids(invalid_ids)
    





