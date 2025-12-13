#Get input
with open('./05/input.txt', 'r') as input_file:
    lines = input_file.readlines()
    page_ordering_rules = [line.strip() for line in lines if '|' in line]
    updates = [line.strip() for line in lines if ',' in line]
    
# Helper Functions
def sum_middle_elems(update_list: list) -> int:
    middle_elems = [update[len(update) // 2] for update in update_list]
    return sum(middle_elems)

def check(update: list, rules_dict: dict)->bool:
    """
    Checks where a given update adheres to all the rules in the rules_dict
    """
    for i, num in enumerate(update):
            numbers_after = set(update[i:])
            try:
                if (numbers_after & rules_dict[num]):
                    return False 
            except KeyError:
                pass # number has no rule associated with it
    return True
    

# Create Rules
"""
Create a dictionary of rules.
The key is the number, and the set of numbers that it must *not* come before
e.g.

3|5
4|5
3|4

result:

{
    5: [3,4],
    4: [3]
}
"""
rules_dict = {}
for rule in page_ordering_rules:
    not_before, number = rule.split('|')
    try:
        rules_dict[int(number)].add(int(not_before))
    except KeyError:
        rules_dict[int(number)] = set([int(not_before)])

# Check all updates
good_updates = []
bad_updates = []
for update in updates:
    update_as_int_list = [int(update) for update in update.split(',')]
    if check(update_as_int_list, rules_dict):
        good_updates.append(update_as_int_list)
    else:
        bad_updates.append(update_as_int_list)

print(f"The sum of middle elements in the good updates are {sum_middle_elems(good_updates)}")

## PART 2

def move_num_i(num_i: int, update: list, i: int, rules_dict: dict) -> list:
    """
    Moves the number at index i to its legal position
    """
    # we go in reverse order to simplify the search
    numbers_after = reversed(update[i:])
    for j, num_j in enumerate(numbers_after):
        try:
            if num_j in rules_dict[num_i]:
                # find it's position original update
                new_index = update.index(num_j)
                # insert it in the original update, and simultaneously pop it out of original position
                update.insert(new_index, update.pop(i))
                return update, True
        except KeyError:
            pass
    return update, False


fixed_updates = []
for update in bad_updates:
    while not check(update, rules_dict):
        for i, num_i in enumerate(update):
            update, fixed = move_num_i(num_i, update, i, rules_dict)
            if fixed: break # we fixed the list, and changed the positions of the elements, break and restart
    fixed_updates.append(update)

print(f"The sum of middle elements in the fixed updates are {sum_middle_elems(fixed_updates)}")