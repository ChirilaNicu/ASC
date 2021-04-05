# Testing


* Use the run_tests.sh script.
* Change the PYTHON variable inside it with the path on your system before running it
* Input and output reference files are in the tests / directory
    * also in this directory the output file of the theme run is generated using test.py

The test-genre directory contains scripts for generating tests.

* README_TESTS - describes the json format of input files
* test_generator.py - generates test files
* test_utils.py - constants used in test_generator
* generate_tests.sh - generates the 10 tests provided in the skeleton 