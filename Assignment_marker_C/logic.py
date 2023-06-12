import subprocess
import glob
from env_var import *

# List of C files to be checked
c_files = []
student_submission_results = {}

c_files_list = glob.glob(f"{folder_path}/*.c")
for file in c_files_list:
    c_files.append(file)


def run_c_file(file_name):
    execution_faluire = 1
    anwer_didnt_match = 2
    answer_matched = 3
    try:
        subprocess.check_output(["gcc", file_name, "-o", "output"])
        if (subprocess.check_output(["./output"]) in expected_answer or expected_answer in subprocess.check_output(["./output"])):
            return answer_matched
        else:
            return anwer_didnt_match
    except subprocess.CalledProcessError:
        return execution_faluire


def find_includes(file_name):
    include_count = len(include_statements)
    per_include_mark = marks_include_statements / include_count
    total_mark = 0
    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            for include_statement in include_statements:
                if (include_statement in line):
                    total_mark += per_include_mark
                    continue
    return total_mark


def find_exclude(file_name):
    exclude_count = len(exclude_statements)
    per_exclude_mark = marks_exclude_statements / exclude_count
    total_mark = 0
    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            for exclude_statement in exclude_statements:
                if (exclude_statement in line):
                    total_mark -= per_exclude_mark
                    continue
    return total_mark


def find_marks_for_ifs(file_name):
    if_count = 0
    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            if ("if" in line):
                if_count += 1
    per_if_mark = marks_for_ifs / no_of_ifs
    if if_count < no_of_ifs:
        return if_count * per_if_mark
    else:
        return marks_for_ifs


def find_marks_for_whiles(file_name):
    while_count = 0
    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            if ("while" in line):
                while_count += 1
    per_while_mark = marks_for_whiles / no_of_whiles
    if while_count < no_of_whiles:
        return while_count * per_while_mark
    else:
        return marks_for_whiles


def find_marks_for_fors(file_name):
    for_count = 0
    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            if ("for" in line):
                for_count += 1
    per_for_mark = marks_for_fors / no_of_fors
    if for_count < no_of_fors:
        return for_count * per_for_mark
    else:
        return marks_for_fors


for file in c_files:
    student_number = file.split("/")[-1].split(".")[0]
    student_submission_results[student_number] = [0, 0, 0, 0, 0, 0, 0]
    #   0  1  2  3  4  5  6
    casee = run_c_file(file)
    if (casee == 3):
        # print(f"{file} - Done")
        student_submission_results[student_number][5] = marks_for_correct_answer
        student_submission_results[student_number][6] = marks_for_compilation
    elif (casee == 2):
        # print(f"{file} - Answer Wrong")
        student_submission_results[student_number][6] = marks_for_compilation
    elif (casee == 1):
        # print(f"{file} - Error encountered")
        student_submission_results[student_number][5] = 0
        student_submission_results[student_number][6] = 0

    student_submission_results[student_number][0] = int(
        find_marks_for_ifs(file))
    student_submission_results[student_number][1] = int(
        find_marks_for_whiles(file))
    student_submission_results[student_number][2] = int(
        find_marks_for_fors(file))
    student_submission_results[student_number][3] = int(find_includes(file))
    student_submission_results[student_number][4] = int(find_exclude(file))

print("\nIndex\t\t IF \t While \t For \t Inclu \t Exclu \t AnsOK \t Compiled \tTotal\n")
for key, value in student_submission_results.items():
    # print(key, value)
    print(key, end='')
    total = 0
    for val in value:
        total += int(val)
        print(f" \t {val}", end='')
    print("\t\t"+str(total))
print()
