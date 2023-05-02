import pickle
import csv
import subprocess
import pdb
import os
import re
import io

def find_git_root(path):
    while path != os.path.dirname(path):
        if os.path.exists(os.path.join(path, ".git")):
            return path
        path = os.path.dirname(path)
    return None


def extract_method_info(method_key):
    parts = method_key.split(":")

    # Extract class name and replace '.' with '/'
    class_name = parts[0].replace('.', '/')
    class_parts = parts[0].split(".")

    # Extract method signature
    method_signature = parts[1]

    # Extract method name
    method_name = None
    if "<init>" in method_signature:
        # Check for inner class method
        inner_class_delimiter = "$"
        if inner_class_delimiter in class_parts[-1]:
            class_name = class_name.rsplit(inner_class_delimiter, 1)[0]  # Remove inner class from class_name
        method_name = class_parts[-1]  # Use class name as method name for constructors
    else:
        method_name = method_signature.split('(')[0]
        if '$' in method_name:
            method_name = method_name.split('$', 1)[0]

    # Remove inner class name from class_name for regular methods
    if '$' in class_name:
        class_name = class_name.rsplit('$', 1)[0]

    # Create file path using the class name (without the inner class)
    file_path = f"{class_name}.java"

    return method_name, file_path


def count_method_commits(method_name, file_path):
    try:
        # Form the git log command with the given method_name and file_path
        git_log_command = f'git log -L:{method_name}:{file_path} --date=local'

        # Run the git log command using subprocess
        result = subprocess.run(git_log_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        # Check if the command was successful
        if result.returncode != 0:
            raise Exception(f"Error: {result.stderr.decode('ISO-8859-1').strip()}")

        # Decode the output using 'ISO-8859-1' encoding
        output_text = result.stdout.decode('ISO-8859-1')

        # Split the output by lines
        output_lines = output_text.strip().split("\n")

        # Count the number of commit lines (each commit line starts with "commit")
        commit_count = sum(1 for line in output_lines if line.startswith("commit"))

        return commit_count

    except Exception as e:
        print(f"Error: {e}")
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
with open('Lang_lite.pkl', 'rb') as f:
    data = pickle.load(f)
    for d in data:
        churn = {}
        liness = d['lines']
        proj = d['proj']
        methodss = d['methods']
        edge = d['edge2']
        folder_name = make_folder_str(proj)
        os.chdir('/Users/tahminaakter/Desktop/test/defects4j-1.2.0/Grace/Lang/'+folder_name)
        # os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_361.jdk/Contents/Home"
        # os.system("export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_361.jdk/Contents/Home")
        dirs = os.popen('defects4j export -p dir.src.classes').readlines()[-1]
        # fpath = 'mockito_%d_copy/'%idx + dirs + '/' + x.split(':')[0].split('$')[0].replace('.', '/') + ".java"
        # os.system("export JAVA_HOME=/Users/tahminaakter/Library/Java/JavaVirtualMachines/openjdk-19.0.2/Contents/Home")
        # os.environ["JAVA_HOME"] = "/Users/tahminaakter/Library/Java/JavaVirtualMachines/openjdk-19.0.2/Contents/Home

        method_modification_count = {}
        for key, value in methodss.items():
            method_name, file_path = extract_method_info(key)
            full_path = '/Users/tahminaakter/Desktop/test/defects4j-1.2.0/Grace/Lang/'+folder_name+'/'+dirs+'/'+file_path
            print(proj)
            print(full_path, '------',method_name,'-------')
            modifications = count_method_commits(method_name, full_path)
            # churn[value] = modifications
            method_modification_count[value] = modifications
        
        print(method_modification_count)
        for tup in edge:
            m, l = tup
            churn[l] = method_modification_count[m]
        
        d['modification'] = churn
        os.chdir(root_path)

with open('Lang_lite_modi_method_nn.pkl', 'wb') as f:
    pickle.dump(data, f)

