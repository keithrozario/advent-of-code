
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
    """
    Returns true if all elements in report are within 3 of each other
    """
    for i in range(1, len(report)):
        if abs(report[i] - report[i-1]) > 3:
            return False
    return True

def check_safety(report: list)->bool:
    """
    Returns true if report is safe, false otherwise
    """
    if check_ascending(report) or check_descending(report):
        if check_diff(report):
            return True    
    return False

def check_safety_with_dampener(report: list)->bool:
    """
    Checks for report will be safe if one value is removed
    """
    for i, num in enumerate(report):
        # remove one element at a time
        report_copy = report.copy()
        report_copy.pop(i)
        # check if report is now safe
        if check_safety(report_copy):
            return True
    return False

# get input
with open("./02/input.txt","r") as input:
    lines = input.readlines() 
    report_strings = [line.strip().split(" ") for line in lines]
    # convert all elements from str to int
    reports = [[int(x) for x in report] for report in report_strings]


safe_reports = [report for report in reports if check_safety(report)]
print(f"Number of safe reports: {len(safe_reports)}")

# Problem Dampener
unsafe_reports = [report for report in reports if not check_safety(report)]
safe_reports_after_dampener = [
    report for report in unsafe_reports if check_safety_with_dampener(report)
]

print(f"Number of safe reports with damperner: {len(safe_reports_after_dampener)}")
print(f"Total safe reports with dampening: {len(safe_reports)+len(safe_reports_after_dampener)}")