import os
import subprocess
import re
from datetime import date
from dateutil import parser
import csv
from itertools import zip_longest
import shutil
import sys
from git import Repo
import pdb

def get_commit_timestamp(repo_path, commit_sha):
    repo = Repo(repo_path)
    commit = repo.commit(commit_sha)
    timestamp = commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(repo_path)
    print(timestamp)
    return timestamp



def generate_csv(folder_name, commit_sha):
    current_date = get_commit_timestamp(os.getcwd()+"/"+folder_name, commit_sha)
    all_java_files = open(folder_name+'/allJavaFiles_b.txt').readlines()


    # Command to get all the files without the test files in a Java project
    # `find src -name '*.java' ! -path '*/test/*' -print`

    # Date of today
    # current_date = today.strftime("%Y-%m-%d")
    date1 = parser.parse(current_date)
    age_dict = {}
    if os.path.exists(folder_name+"/FilesAge_b"):
        shutil.rmtree(folder_name+"/FilesAge_b")
            # Create the folder again
    os.makedirs(folder_name+"/FilesAge_b")
    os.chdir(folder_name)
    for files in all_java_files:
        # File path of the java files
        file_path = files.strip()
        file_name = os.path.basename(file_path).split('.')[0]
        command = "git blame "+file_path+" -w"
        
        # print(command)
        with open('AgeOfLines/'+folder_name+'.csv', 'w') as fr:
            # fr.write(file_name+': ')
            writer = csv.writer(fr)
            age_dict[file_name] = []
            with open('FilesAge_b/'+file_name+'.txt', "w", encoding='iso-8859-1') as file:
                subprocess.run(command, shell=True, stdout=file)
            
            
            #os.system(f'{command} > '+ 'FilesAge/'+file_name+'.txt')
            
            age_lines = open('FilesAge_b/'+file_name+'.txt','r', encoding='iso-8859-1').readlines()

            # Find the first string within parentheses
            count = 0
            for i in age_lines:
                date_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', i)
                #time_match = re.search(r'\d{2}:\d{2}:\d{2}', i)
                

                if date_match:
                    count+=1
                    date = date_match.group()
                    date2 = parser.parse(date)
                    day_diff = (date1 - date2)
                    if day_diff.days == 0 and day_diff.seconds == 0:
                        age_dict[file_name].append(0)
                    else:
                        age_dict[file_name].append(day_diff.days)

                    #print(file_name,date, day_diff)
                    # print(day_diff.days+"_"+day_diff.seconds)
                    # fr.write(str(day_diff.days)+":"+str(day_diff.seconds)+' ')
                    

                    #time = time_match.group()
                    #print(count, date)
                else:
                    print("No match found.")
            sorted_dict = dict(sorted(age_dict.items(), key=lambda x: x[1].count(0), reverse=True))

            writer.writerow(sorted_dict.keys())
            for row in zip_longest(*sorted_dict.values()):
                writer.writerow(row)
    os.chdir("..")

# 'math_50_b': '2f066a5', 'math_53_b': '6ef3b29', 'math_54_b': '1eb0c0d',
# project_commit_hash = {
#  'math_55_b': '89ac173', 'math_60_b': '6ef3b29', 'math_63_b': 'b1ade04',
#  'math_64_b': '615ca9a', 'math_70_b': '583dffc', 'math_75_b': '18b61a1',
#  'math_79_b': 'dfd9f06', 'math_87_b': '24a6a26', 'math_88_b': 'b03d685',
#  'math_89_b': '0c84b28', 'math_92_b': '0a90446', 'math_93_b': '0a90446',
#  'math_94_b': '20786a6', 'math_96_b': '0a90446', 'math_97_b': '4f1e69b',
#  'math_101_b': '3227063', 'math_103_b': 'ac9e22b', 'math_104_b': '0a90446',
#  'math_105_b': 'b456529', 'math_106_b': '41598b0, 'math_42_b': 'f36be8e', 'math_45_b': '8742126', 'math_46_b': '330f3fe'
# }

project_commit_hash = {'math_48_b': '39cf5e6'}

for key, value in project_commit_hash.items():
    generate_csv(key, value)
    # pdb.set_trace()