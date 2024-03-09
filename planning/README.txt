Programming exercise: Planning and SAT
--------------------------------------------------------------------------------

In this exercise, we will solve the state-space search problem
by translating it into propositional formulas and solving them
as a SAT problem. The state-space search problem is used in AI
to solving the planning problem, which is choosing a sequence of
actions to reach a goal.

Instructions
============
1. In this exercise, you need the Z3 SMT solver; to install it, you can use the
   following command:

   `pip install z3-solver`

   See https://github.com/Z3Prover/z3 for more information.
2. Copy the file `template-planning.py` to `planning.py`.
3. Read and understand the `logic.py` and the `planning.py` files.
4. Complete the required sections in `planning.py`.
5. Test your implementation and verify its correctness. Again, you can find
   some unit tests in `test_planning.py`.
6. Well done! Submit your code.


Structure
=========
./
├── README.txt
├── logic.py
├── template-planning.py
├── test_planning.py
└── z3_wrapper.py


What you need to do is:
1. Iterate over action sequence lengths 0,...,MAX.
2. For each length, instantiate the formulas for source states,
   the transition relation, and target states with integer times.
3. Put together the formula, and call the Z3 SAT solver.

Testing
=======
1. `python3 test_planning.py`: Using your code, it tries to solve some
   basic planning problems by using the Z3 SAT solver.
