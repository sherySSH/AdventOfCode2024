import os
from collections import Counter
from copy import deepcopy

def read_file(fpath : str) -> list:
    with open(fpath) as f:
        content : list = f.readlines()
    return content


def preprocessing(content : str):
    report_list = []
    for report in content:
        prep_report = report.replace("\n","")
        prep_report = [int(value) for value in prep_report.split(' ')]
        report_list.append(prep_report)
    return report_list

def check_trend(current_level : int, next_level : int):
    # increasing trend
    if current_level < next_level:
        return 1
    # decreasing trend
    elif current_level > next_level:
        return 0
    # stationary trend
    else:
        return -1


def is_report_unsafe(report : list):
    # first estimate the trend
    current_level = report[0]
    next_level = report[1]
    trend = check_trend(current_level, next_level)
    is_unsafe = 0
    # then check the constraints for all levels
    for next_level in report[1:]:
        if (trend != check_trend(current_level, next_level)) or (abs(next_level - current_level) > 3) or ((next_level - current_level) == 0):
            is_unsafe = 1
            break
        current_level = next_level

    return is_unsafe

def count_safe_reports(report_list : list):
    unsafe = 0
    for report in report_list:
        is_unsafe = is_report_unsafe(report)
        if is_unsafe:
            unsafe += 1
    
    total_reports = len(report_list)
    safe = total_reports - unsafe
    return safe


def count_safe_reports_by_removal(report_list  : list):
    unsafe = 0
    for report in report_list:
        # first estimate the trend
        current_level = report[0]
        next_level = report[1]
        trend = check_trend(current_level, next_level)
        
        is_dampener_active = 0
        is_unsafe_current = 0
        is_unsafe_next = 0

        current_idx = 0
        next_idx = current_idx + 1
        # then check the constraints for all levels
        while next_idx < len(report):  
            current_level = report[current_idx]
            next_level = report[next_idx]
            if ((trend != check_trend(current_level, next_level)) or (abs(next_level - current_level) > 3) or ((next_level - current_level) == 0)):
                # activating dampener toleration
                is_dampener_active = 1
                break
            else:
                current_idx = next_idx
                next_idx = current_idx + 1
            
        if is_dampener_active:
                # left path of stump decision tree
                left_report = deepcopy(report)
                left_report.pop(current_idx)
                is_unsafe_current = is_report_unsafe(left_report)

                # right path of stump decision tree
                right_report = deepcopy(report)
                right_report.pop(next_idx)
                is_unsafe_next = is_report_unsafe(right_report)

        # if report remains unsafe, irrespective of current or next level that we remove, then we classify it as unsafe
        if is_unsafe_current and is_unsafe_next:
            # there can be edge cases where only by removing first element we can get correct report, e.g 1 4 3 2 1
            # this case must be checked after left_report and right_report unsafety because 1 4 3 2 1 will be classified 
            # as unsafe by left_reprot and right_report check
            # remove first element and then check
            trailing_report = deepcopy(report)
            trailing_report.pop(0)
            is_unsafe = is_report_unsafe(trailing_report)
            if is_unsafe:
                unsafe += 1
    
    total_reports = len(report_list)
    safe = total_reports - unsafe
    return safe

if __name__ == "__main__":
    content = read_file("input.txt")
    report_list = preprocessing(content)
    safe = count_safe_reports(report_list)
    print("Part a", safe)

    safe = count_safe_reports_by_removal(report_list)
    print("Part b", safe)