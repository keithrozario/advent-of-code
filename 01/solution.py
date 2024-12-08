
list_1, list_2 = [], []

# Get input texts
with open('./01/input.txt', 'r') as input:
    lines = input.readlines()
    for line in lines:
        num_1, num_2 = line.strip().split("   ")
        list_1.append(int(num_1))
        list_2.append(int(num_2))

# sort the lists
list_1.sort()
list_2.sort()

# Get diff into a single list
total_diff = 0
for i,num in enumerate(list_1):
    total_diff += abs(list_2[i] - num)
    
print(f"The total diff is: {total_diff}")

# now get similarity score
total_similarity = 0
for num in list_1:
    num_occurence = list_2.count(num)
    total_similarity += num * num_occurence

print(f"The total similarity is: {total_similarity}")