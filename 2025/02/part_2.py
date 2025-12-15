from typing import List
import math


def get_factors(id_len: int)->List[int]:
    """
    Args:
        len_id: The length of the id
    returns:
        factors: The factors of the number, including 1
    """
    factors = set()
    for i in range(1, int(math.sqrt(id_len)) + 1):
        if id_len % i == 0:
            factors.add(i)
            factors.add(id_len // i)
    return sorted(list(factors))

def check_repetition(id: str, len_rep: int)->bool:
    """
    Checks if the id is made of a repeating sequence of length len_rep
    assumes len_rep is a factor of id.
    """
    pattern = id[:len_rep]
    for i in range(len_rep,len(id),len_rep):
        if id[i:i+len_rep] != pattern:
            return False
    return True


def is_valid(id: str)->bool:
    """
    Args:
        id: the id to check
    returns:
        bool: if the id is valid or not
    """
    id_len = len(id)
    factors = get_factors(id_len)

    # can't have a repetition with more than half the string
    factors_less_than_half = list(filter(lambda x: x<=id_len/2, factors))
    for factor in factors_less_than_half:
        if check_repetition(id, factor):
            return False

    return True

def get_invalid_ids(number_ranges: list[str])->list:

    invalid_ids = []
    for number_range in number_ranges:
        start_num,end_num = number_range.split("-")
        for i in range(int(start_num), int(end_num)+1):
            if not is_valid(str(i)):
                invalid_ids.append(i)
    print(invalid_ids)
    return invalid_ids

def sum_invalid_ids(invalid_ids: list[int])->int:
    total = 0
    for id in invalid_ids:
        total += id
    print(total)
    return total

if __name__ == "__main__":
    assert get_factors(12) == [1,2,3,4,6,12]
    assert get_factors(10) == [1,2,5,10]
    
    assert check_repetition("123123123",3) == True
    assert check_repetition("123123123",4) == False
    assert check_repetition("11",1) == True
    assert check_repetition("1111111", 1) == True
    assert check_repetition("2121212121", 2) == True

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
    





