import os

ids = [5, 7, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20, 21, 22, 24, 25, 27, 29, 32, 33, 34, 39, 41, 45, 46, 47, 49, 51, 52, 57, 58, 60]
# ids.append(1)

for n in ids:
    #defect/Lang-3b/coverage.xml defect/Lang-3b/failing_tests

    fail_test_file = open('lang_'+str(n)+'_copy/failing_tests').readlines()
    s = ''
    for i in fail_test_file:
        if '---' in i:
            s = i.split()[1] + '\n'
            with open('FailedTests/'+str(n)+'.txt', 'a') as fr:
                fr.write(s)