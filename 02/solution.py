
def check_ascending(report):
    for i in range(1, len(report)):
        if report[i] <= report[i-1]:
            return False
    return True

def check_descending(report):
    for i in range(1, len(report)):
        if report[i] >= report[i-1]:
            return False
    return True

def check_diff(report):
    for i in range(1, len(report)):
        if abs(report[i] - report[i-1]) > 3:
            return False
    return True

def check(report):
    if check_ascending(report) or check_descending(report):
        if check_diff(report):
            return True    
    return False

# get input
with open("./02/input.txt","r") as input:
    lines = input.readlines() 
    reports = [line.strip().split(" ") for line in lines]

# count good reports
good_report_count = 0
bad_reports = []
for report in reports:
    report_num = [int(x) for x in report]
    if check(report_num):
        good_report_count += 1
    else:
        bad_reports.append(report_num)

print(good_report_count)

# Problem Dampener
dampened_report_count = 0
for report in bad_reports:
    for i in range(len(report)):
        # remove one element at a time
        report_copy = report.copy()
        report_copy.pop(i)
        
        # check if report is now safe
        if check(report_copy):
            dampened_report_count += 1
            # no longer have to check this report it's already safe
            break

print(good_report_count + dampened_report_count)