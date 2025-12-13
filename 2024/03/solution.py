import re

with open('./03/input.txt', 'r') as input:
    lines = input.readlines()

# <mul(> + <1 to 3 digit integer> + <,> + <1 to 3 digit integer> + <)>
mul_pattern = re.compile("mul\(\w{1,3},\w{1,3}\)")

total = 0

for line in lines:
    muls = mul_pattern.findall(line)
    for mul in muls:
        num_1, num_2 = mul[4:-1].split(",")
        total += int(num_1)*int(num_2)

print(f"{total:,}")

# Part 2

do_pattern = re.compile("do\(\)")
dont_pattern = re.compile("don\'t\(\)")

def sum_muls(input: str):
    total = 0
    muls = mul_pattern.findall(input)
    for mul in muls:
        num_1, num_2 = mul[4:-1].split(",")
        total += int(num_1)*int(num_2)
    return total

total=0

status = "do"

with open('./03/input.txt', 'r') as input:
    line = input.read()


next_do = 0
scanning = True
while scanning:
    if status == "do":
        try:
            next_dont = dont_pattern.search(line, pos=next_do).regs[0][1]
        except AttributeError:
            next_dont = len(line)
            scanning = False
        total += sum_muls(line[next_do:next_dont])
        status = "dont"
        print(f"Do from {next_do} to {next_dont}. Total = {total:,}")
    elif status == "dont":
        try:
            next_do = do_pattern.search(line, pos=next_dont).regs[0][1]
        except AttributeError:
            next_do = len(line)
            scanning = False
        status = "do"
        print(f"Dont from {next_dont} to {next_do}. Total = {total:,}")