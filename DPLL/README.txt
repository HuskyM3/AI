Programming exercise: DPLL and Scheduling
--------------------------------------------------------------------------------

In this exercise, we will implement the DPLL algorithm.


Instructions
============
1. In this exercise, you need the Z3 SMT solver; to install it, you can use the
   following command:

   `pip install z3-solver`

   See https://github.com/Z3Prover/z3 for more information.
2. Copy the file `template-dpll.py` to `dpll.py`.
3. Read its documentation and complete the code.
4. Test your implementation and verify its correctness. We have provided some
   unit tests in `test_dpll.py` to make your life a little easier :)
5. Well done! Submit your code.


Structure
=========
./
├── README.txt
├── examples-sudoku.py
├── logic.py
├── sudoku.py
├── template-dpll.py
├── test_dpll.py
└── z3_wrapper.py


Example
=======
As an example, we have provided the encoding of Sudoku problems for SAT solvers.
You can see the encoding in the `sudoku.py` file and find some examples in
`example-sudoku.py`.


Testing
=======
1. `python test_dpll.py`: executes some unit tests on your DPLL implementation.
2. `python example-sudoku.py`: Using your DPLL implementation, it tries to solve
   the encoded Sudoku problems. Besides testing your DPLL implementation, you
   can compare your run-time against the Z3 solver with this script. Moreover,
   you can solve your own Sudoku problems with this script ;)


GL HF :)
