#!/bin/bash



work_dirr="/Users/tahminaakter/Desktop/ASE23-Bias/Grace/Lang"



cd "$work_dirr"
# # git clone https://github.com/rjust/defects4j.git
# cd "$work_dir/defects4j"
# ./init.sh
#5 7 9 10 11 12 14 15 16 18 19 20 21 22 24 25 27 29 32 33 34 36 39 41 45 46 47 49 51 52 57 58 60
# hash_values=(75944e54 366badaf c45d5bff afe5dff7 c821fafc c9d786a4 c8afaa3e 8185a9e6 13c7f19a 2aa9dca9 d25f73fc 68ee605f 55f64272 b219cb01 b219cb01 2bae6878 7c915333 a45b7e63 806ed8e6 0603aef5 496525b0 b2a360da ec09e01c 841f743e 091a9ab6 916639bd d5e34304 0ac772a4 3b46d611 e96b0142 bbd990b8 1fd45a4f a8203b65)
# values=(1 3 6 9 11 12 13 14 15 16 17 20 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38)
values=(5 7 9 10 11 12 14 15 16 18 19 20 21 22 24 25 27 29 32 33 34 36 39 41 45 46 47 49 51 52 57 58 60)
# hash_values=(2037361be 9b2cf8072 81a380951 620f8faed 77cb20373 b7d3e760b d0c872e4b 82935114a c17169c2c a6ccf070a af44738c7 a8ec4fa29 0464f5657 918f0a5ae 3c924f80a 62b6bdf44 4f7060cc5 5cb37751c e8cebe01a 27a2f5151 84c142f56 c0222c2db c1f2c4e6b)
# hash_values=(7a647a702)
for i in "${!values[@]}"
do
    PID=$1
    BID=${values[$i]}
    # hashid=${hash_values[$i]}

    cd $work_dirr/${PID}_${BID}_b
    echo "*****************"
    pwd
    test_classpath=$(defects4j export -p cp.test)
    src_classes_dir=$(defects4j export -p dir.bin.classes)
    src_classes_dir="$work_dirr/${PID}_${BID}_b/$src_classes_dir"
    test_classes_dir=$(defects4j export -p dir.bin.tests)
    test_classes_dir="$work_dirr/${PID}_${BID}_b/$test_classes_dir"
    echo "${PID}_${BID}_b's classpath: $test_classpath" >&2
    echo "${PID}_${BID}_b's bin dir: $src_classes_dir" >&2
    echo "${PID}_${BID}_b's test bin dir: $test_classes_dir" >&2


    cd "$work_dirr/${PID}_${BID}_b"
    unit_tests_file="$work_dirr/${PID}_${BID}_b/unit_tests.txt"


    java -cp "$test_classpath:$test_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$GZOLTAR_CLI_JAR" \
    com.gzoltar.cli.Main listTestMethods \
        "$test_classes_dir" \
        --outputFile "$unit_tests_file" 
    head "$unit_tests_file"


    cd "$work_dirr/${PID}_${BID}_b"

    loaded_classes_file="$D4J_HOME/framework/projects/$PID/loaded_classes/$BID.src"
    normal_classes=$(cat "$loaded_classes_file" | sed 's/$/:/' | sed ':a;N;$!ba;s/\n//g')
    inner_classes=$(cat "$loaded_classes_file" | sed 's/$/$*:/' | sed ':a;N;$!ba;s/\n//g')
    classes_to_debug="$normal_classes$inner_classes"
    echo "Likely faulty classes: $classes_to_debug" >&2


    cd "$work_dirr/${PID}_${BID}_b"

    
    ser_file="$work_dirr/${PID}_${BID}_b/gzoltar.ser"
    java -XX:MaxPermSize=4096M -javaagent:$GZOLTAR_AGENT_JAR=destfile=$ser_file,buildlocation=$src_classes_dir,inclnolocationclasses=false,output="FILE" \
    -cp "$src_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$test_classpath:$GZOLTAR_CLI_JAR" \
    com.gzoltar.cli.Main runTestMethods \
        --testMethods "$unit_tests_file" \
        --collectCoverage


    cd "$work_dirr/${PID}_${BID}_b"

    java -cp "$src_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$test_classpath:$GZOLTAR_CLI_JAR" \
        com.gzoltar.cli.Main faultLocalizationReport \
        --buildLocation "$src_classes_dir" \
        --granularity "line" \
        --inclPublicMethods \
        --inclStaticConstructors \
        --inclDeprecatedMethods \
        --dataFile "$ser_file" \
        --outputDirectory "$work_dirr/${PID}_${BID}_b" \
        --family "sfl" \
        --formula "ochiai" \
        --metric "entropy" \
        --formatter "txt"
    
    cd ..
done