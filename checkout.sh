#!/bin/bash

# Set the project name
project="Lang"

# Set the versions to checkout
# versions=("10" "101" "103" "104" "105" "106" "14" "15" "17" "2" "23" "24" "25" "26" "28" "3" "35" "42" "45" "46")

# Loop through the versions and checkout the buggy version of the project
for version in 5 7 9 10 11 12 14 15 16 18 19 20 21 22 24 25 27 29 32 33 34 39 41 45 46 47 49 51 52 57 58 60;
do
    # Checkout the buggy version of the project
    echo $version
    # defects4j checkout -p $project -v ${version}b -w lang_${version}_b
    # cp -R lang_${version}_b lang_${version}_copy
    # mkdir lang_${version}_copy
    cd lang_${version}_copy
    # echo 'org.apache.commons.**.*' > all-classes.txt
    # defects4j coverage
    # defects4j compile
    # defects4j test
    # cp .defects4j.config defects4j.build.properties build.xml pom.xml all_tests maven-build.xml ../lang_${version}_copy
    # cp failing_tests /Users/tahminaakter/Desktop/ASE23-Bias/f_b/${version}.txt
    cp -R sfl ../lang_gzoltar_prior/lang_${version}_prior
    cd .. 

    # Change back to the parent directory
    
done
