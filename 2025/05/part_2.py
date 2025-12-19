from typing import Tuple, List, Literal

def get_full_ranges(id_ranges: list)->list:

    full_ranges = []
    for id_range in id_ranges:
        start_id_range, end_id_range = id_range.split("-")
        full_ranges.append((int(start_id_range), int(end_id_range)))

    return full_ranges


def get_ingredient_list(file_path: str)->Tuple[List[str],List[int]]:
    with open(file_path, "r") as ingredient_list:
        full_inventory = ingredient_list.readlines()
        fresh_id_ranges = [line.strip() for line in full_inventory if "-" in line]
        ingredients = [int(line.strip()) for line in full_inventory if "-" not in line and line != "\n"]

    return fresh_id_ranges, ingredients

def check_overlapping_ranges(range_a: Tuple, range_b:Tuple)->Tuple[Tuple,bool]:
    """
    Calculates the length of overlap between two inclusive ranges.
    returns:
        merged_range: A new merged range if the ranges overlap; or range_a if there is no overlap
    """
    # 1. Find the latest start time and earliest end time
    overlap_start = max(range_a[0], range_b[0])
    overlap_end = min(range_a[1], range_b[1])

    overlap = overlap_end - overlap_start
    if overlap >= 0:
        merged = True
        merged_range = (min(range_a[0], range_b[0]), max(range_b[1], range_a[1]))
    else:
        merged = False
        merged_range = range_a
    
    return merged_range, merged

def substitute(id_range: Tuple, visited_ranges: dict)-> Tuple:
    if id_range in visited_ranges.keys():
        return visited_ranges[id_range]
    else:
        return id_range

if __name__ == "__main__":
    assert get_full_ranges(["1-5","4-7"]) == [(1,5),(4,7)]
    assert check_overlapping_ranges ((8,12),(10,14)) == ((8,14), True)
    assert check_overlapping_ranges ((8,12),(14,15)) == ((8,12), False)
    assert check_overlapping_ranges ((8,12),(8,12)) == ((8,12), True)
    assert check_overlapping_ranges ((8,12),(9,11)) == ((8,12),True)
    assert check_overlapping_ranges ((8,12),(5,10)) == ((5,12), True)
    
    fresh_id_ranges, ingredients = get_ingredient_list("./2025/05/input.txt")
    full_ranges = get_full_ranges(id_ranges=fresh_id_ranges)
    full_ranges.sort(key=lambda x: x[0])
    
    """
    Not too happy with this.

    Code starts from the smallest range, and loops through the list.
    If it finds an overlapping range:
        it merges it with current range and
        substitutes it for the overlapping range
        then it breaks and proceeds to the next range in the list
    If it does not find an overlappint range:
        it will be added to the final list of merged_ranges.
    
    The list of merged_ranges is the final list of non-overlapping ranges
    """
    visited_ranges = {}
    merged_ranges = []
    for index, range_a in enumerate(full_ranges):
        range_to_check = substitute(range_a, visited_ranges)
        for range_b in full_ranges[index+1:]:
            substituted_range = substitute(range_b, visited_ranges)
            new_merged_range, merged = check_overlapping_ranges(range_to_check,substituted_range)
            if merged:
                visited_ranges[range_b] = new_merged_range
                break
        else:
            merged_ranges.append(range_to_check)
    totals = 0
    for merged_range in merged_ranges:
        totals += (merged_range[1]-merged_range[0]+1)
    print(merged_ranges)
    print(totals)    