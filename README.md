# SchemeCompiler

## Note to grader:
Please see assignment2 branch.

## Instructions

### Running tests:
- In the **SchemeCompiler** directory, run `python3 run_tests.py`. This will run unit tests on each component.
- Each component is tested separately. Tests can be found in **SchemeCompiler/tests/unit_tests/**.
- To run tests for a given construct in a given component, in **SchemeCompiler** run `python3 -m unittest discover -s tests -p test_<component>_<construct>.py`.
    - If individually testing an interpreter component, make sure the interpreter has been built beforehand. In both **SchemeCompiler/interpreter/utils/** and **SchemeCompiler/interpreter/execs** run `make clean; make`.
    - The interpreter is automatically built by the *run_tests.py* script.
- To run tests for a given construct in a given component, in **SchemeCompiler** run `python3 -m unittest discover -s tests -p "test_<component>_*.py"`.
    - Again, ensure that the interpreter has been built before testing it individually.

### Running the compiler:
- In the **SchemeComppiler** directory, run `python3 run_scheme.py`.
- You can then input a valid Scheme expression and observe the output.

## Notes

### `let`
I am just noting the way I implemented `let` since I just wanted to ensure that it is okay as it seems a bit complicated, but I tried to follow along with the paper as much as possible. In my runtime, I created a vector of vectors which carries the environment for each `let` binding. I did this to allow for nested `let` bindings. A `let` instruction is always followed by a number indicating the number of bindings it is associated with. Each time a `let` instruction is encountered by the interpreter, it pops the given number of values off the stack and places them in the environment associated with that binding. Instead of the usual `LOAD64` instruction, I created a `GET_FROM_ENV` instruction which is always followed by a 64-bit integer value indicating the index in the environment from whch to load. This instruction pushes the relevant value from the environment onto the stack. Any operations may then be performed as per usual with values on the stack. I am thinking that this step of loading the value onto the stack may not be entirely necessary, but I did it to avoid the complexity of having to implement operations that use the environment as opposed to the stack.
