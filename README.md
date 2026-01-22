# SchemeCompiler

## Instructions

### Running tests:
- In the **SchemeCompiler** directory, run `python3 run_tests.py`. This will run unit tests on each component.
- Each component is tested separately. Tests can be found in **SchemeCompiler/tests/unit_tests/**.
- To run tests for a given construct in a given component, in **SchemeCompiler** run `python3 -m unittest discover -s tests -p test_\<component\>_\<construct\>.py`.
    - If individually testing an interpreter component, make sure the interpreter has been built beforehand. In both **SchemeCompiler/interpreter/utils/** and **SchemeCompiler/interpreter/execs** run `make clean; make`.
    - The interpreter is automatically built by the *run_tests.py* script.
- To run tests for a given construct in a given component, in **SchemeCompiler** run `python3 -m unittest discover -s tests -p "test_\<component\>_\*.py"`.
    - Again, ensure that the interpreter has been built before testing it individually.

### Running the compiler:
- In the **SchemeComppiler** directory, run `python3 run_scheme.py`.
- You can then input any valid Scheme expression and observe the output.

