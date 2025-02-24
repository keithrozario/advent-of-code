def mix(a, secret_number):
    return a ^ secret_number

def prune(secret_number):
    return secret_number % 16777216

def get_next_num(secret_number: int)->int:
    secret_number = prune(mix(secret_number, secret_number * 64))
    secret_number = prune(mix(secret_number, int(secret_number/32)))
    secret_number = prune(mix(secret_number, secret_number * 2048))
    return secret_number

def get_input(file_name: str)->int:
    with open(file_name, "r") as f:
        lines = f.readlines()
    
    init_secrets = [int(x.strip()) for x in lines]
    return init_secrets


def get_bananas(monkeys: list, combo: list)->int:
    total_bananas = 0
    for monkey in monkeys:
        # monkey[0] = prices, monkey[1] = changes
        change_str =  ",".join(map(str, combo))
        try:
            i = monkey[1].index(change_str)
            price = monkey[0][i+len(combo)]
            total_bananas += price
        except ValueError:
            continue
    return total_bananas

def get_monkeys(init_secrets: list, iterations: int=2000, debug_change: str=None) -> dict:
    """
    from a list of secrets (1 per monkey)
    iterate through the list and update the price for each price change in a dict
    the dict called change holds the price change for each combination across all monkeys
    where the change is a string of the last 4 price changes, and the price it the value of the key.
    """

    changes = {}

    for monkey_num, secret_number in enumerate(init_secrets):
        prices = []  # Reset prices list for each secret number
        monkey_combinations = {}

        for x in range(iterations):
            secret_number = get_next_num(secret_number)
            price = secret_number % 10
            prices.append(price)
            if x >= 4:
                # Setup unique string for price combination
                change_str = f"{prices[x-3] - prices[x-4]},{prices[x-2] - prices[x-3]},{prices[x-1] - prices[x-2]},{prices[x] - prices[x-1]}"
                if change_str not in monkey_combinations.keys():
                    monkey_combinations[change_str] = True
                    changes[change_str] = changes.get(change_str, 0) + price
                    
                    # placed this here for when I needed to debug the function
                    if change_str == debug_change:
                        print(f"{monkey_num}. {change_str}. {x}. {price} Prices: {prices[x-4:x+1]}, price: {price}")
                    
    return changes

# Begin with some tests
secret_number = 123
for x in range(10):
    secret_number = get_next_num(secret_number)
assert secret_number == 5908254

# Sample
init_secrets = get_input("./22/sample.txt")
total_secrets = 0
for secret_number in init_secrets:
    for x in range(2000):
        secret_number = get_next_num(secret_number)
    total_secrets += secret_number
assert secret_number == 8667524
assert total_secrets == 37327623


# Part 1
init_secrets = get_input("./22/input.txt")
total_secrets = 0
for secret_number in init_secrets:
    for x in range(2000):
        secret_number = get_next_num(secret_number)
    total_secrets += secret_number
print(f"Total secrets: {total_secrets}")
assert total_secrets == 20506453102

# Part 2

## Test
combo = [-2,1,-1,3]
change_str =  ",".join(map(str, combo))

init_secrets = get_input("./22/sample-2.txt")
changes_dict = get_monkeys(init_secrets)
assert changes_dict[change_str] == 23
assert max(changes_dict.values()) == 23

# Part 2
init_secrets = get_input("./22/input.txt")
changes_dict = get_monkeys(init_secrets)
change_combo = max(changes_dict, key=changes_dict.get)
# max_bananas = max(changes_dict.values()) # equally acceptable
max_bananas = changes_dict[change_combo]

print(f"The Maximum number of bananas is: {max(changes_dict.values())} with the combination: {change_combo}")
assert max_bananas == 2423