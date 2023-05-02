# Code Change Analysis for Enhanced Fault Localization: An Empirical Investigation of Unchanged Line Metrics, Graph-Based Representation Learning, and Code Evolution Insights

1. Run `checkout.sh` and `run_gzoltar.sh` for checking out all the buggy version and run Gzoltar on them for generating fault localization data.
2. Run `MethodSignatureExtractor.java` for getting all methods.
3. Run `fail_test_gen.py` for parsing the failed tests from the text files.
4. Run `coverage_gen.py` for getting the full coverage data.
5. Run `defects_graph_gen_all.py` for generating the graph based coverage representation. 
6. Run `extract_line_churn.py` and `extract_method_churnpy` for getting the line and method churn.

All the generated files can be found here: https://drive.google.com/drive/folders/1SqvwE37bavMPMaKH5u5KNSgdtkCFeHXN?usp=sharing