import pickle
import csv
import subprocess
import pdb
import os

# lang = [4, 6, 13, 14, 19, 21, 22, 25, 26, 28, 31, 39, 40, 43, 44, 45, 46, 47, 48, 49, 51, 52, 53, 54, 55, 57, 61, 64]
# Load the pkl file
math = [10, 101, 103, 104, 105, 106, 14, 15, 17, 2, 23, 24, 25, 26, 28, 3, 35, 42, 45, 46, 48, 50, 53, 54, 55, 60, 63, 64, 70, 75, 79, 87, 88, 89, 92, 94, 96, 97]

def count_line_modifications(file_path, line_number):
    try:
        output = subprocess.check_output(["git", "log", "-L", f"{line_number},{line_number}:{file_path}", "-w", "--pretty=format:''"]).decode("utf-8")
        lines = output.strip().split("\n")
        modifications = len(lines) - 1
        return modifications
    except subprocess.CalledProcessError:
        return 0




def make_folder_str(proj):
    input_string = proj
    chars = ""
    ints = ""

    for char in input_string:
        if char.isdigit():
            ints += char
        else:
            chars += char

    new_string = f"{chars.lower()}_{ints}_b"
    return new_string


root_path = os.getcwd()
with open('Lang_lite_churn.pkl', 'rb') as f:
    data = pickle.load(f)
    for d in data:
        churn = {}
        liness = d['lines']
        proj = d['proj']
        print(proj)
        folder_name = make_folder_str(proj)
        os.chdir('/Users/tahminaakter/Desktop/check/defects4j/math/'+folder_name)
        
        for key, value in liness.items():
            path_str = key.split(':')
            path = path_str[0].replace('.','/')
            if '$' in path:
                path = path.split('$')[0]
            full_path = '/Users/tahminaakter/Desktop/check/defects4j/math/'+folder_name+'/src/main/java/'+path+'.java'
            line_number = path_str[1]
            modifications = count_line_modifications(full_path, line_number)
            # print(f"Line number {line_number} in {full_path} was modified {modifications} times since it was introduced.")
            churn[value] = modifications
        d['modification'] = churn
        os.chdir(root_path)

with open('Math_lite_modi.pkl', 'wb') as f:
    pickle.dump(data, f)

