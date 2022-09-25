Programming exercise: DPLL and Scheduling
--------------------------------------------------------------------------------

In this exercise, we will encode the constraints of scheduling problems
as propositional formulas and solve them as a SAT problem.


Instructions
============
1. In this exercise, you need the Z3 SMT solver; to install it, you can use the
   following command:

   `pip install z3-solver`

   See https://github.com/Z3Prover/z3 for more information.
2. Copy the file `template-scheduling.py` to `scheduling.py`.
3. Read and understand the `logic.py` and the `scheduling.py` files.
4. Complete the required sections in `scheduling.py`.
5. Test your implementation and verify its correctness. Again, you can find
   some unit tests in `test_scheduling.py`.
6. Well done! Submit your code.


Structure
=========
./
├── README.txt
├── template-scheduling.py
├── test_scheduling.py
└── z3_wrapper.py


Testing
=======
1. `python test_scheduling.py`: Using your encoding, it tries to define some
   basic scheduling problems for SAT solvers. Then, it feeds the encoded problem
   to the SAT solver and shows its result.

GL HF :)
