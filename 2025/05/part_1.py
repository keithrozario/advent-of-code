from typing import Tuple, List

def get_full_ranges(id_ranges: list)->set:

    full_ranges = []
    for id_range in id_ranges:
        start_id_range, end_id_range = id_range.split("-")
        full_ranges.append((int(start_id_range), int(end_id_range)))

    return set(full_ranges)


def get_ingredient_list(file_path: str)->Tuple[List[str],List[int]]:
    with open(file_path, "r") as ingredient_list:
        full_inventory = ingredient_list.readlines()
        fresh_id_ranges = [line.strip() for line in full_inventory if "-" in line]
        ingredients = [int(line.strip()) for line in full_inventory if "-" not in line and line != "\n"]

    return fresh_id_ranges, ingredients

def count_fresh_ingredients(fresh_id_ranges: List[str], ingredients: List[int])->int:
    fresh_ingredients = 0
    full_ranges = get_full_ranges(id_ranges=fresh_id_ranges)

    for ingredient in ingredients:
        for range in full_ranges:
            if ingredient >= range[0] and ingredient <= range[1]:
                fresh_ingredients += 1
                break         

    return fresh_ingredients

if __name__ == "__main__":
    assert get_full_ranges(["1-5","4-7"]) == set([(1,5),(4,7)])
    assert count_fresh_ingredients(
        fresh_id_ranges=["1-5","4-7"],
        ingredients=[1,5,12,13,6]) == 3

    fresh_id_ranges, ingredients = get_ingredient_list("./2025/05/sample.txt")
    fresh_ingredient_count = count_fresh_ingredients(fresh_id_ranges, ingredients)
    print(fresh_ingredient_count)

    fresh_id_ranges, ingredients = get_ingredient_list("./2025/05/input.txt")
    fresh_ingredient_count = count_fresh_ingredients(fresh_id_ranges, ingredients)
    print(fresh_ingredient_count)