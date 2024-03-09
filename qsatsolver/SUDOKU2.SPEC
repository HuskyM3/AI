
# The standard Sudoku puzzle with a 9 X 9 grid

type r13 = { 1,2,3 };
type r46 = { 4,5,6 };
type r79 = { 7,8,9 };

type all = r13 U r46 U r79;


predicates C/3;

# Each number is in exactly one cell in each column.

forall(n : all, x : all) exactly 1 (y : all) C(x,y,n);

# Each number is in exactly one cell in each row.

forall(n : all, y : all) exactly 1 (x : all) C(x,y,n);

# In each cell there is exactly one number.

forall(x : all, y : all) exactly 1 (n : all) C(x,y,n);

# Each number is in exactly one of each of the nine 3 X 3 sub-grids.

forall(dx : { 0, 3, 6 }, dy : { 0, 3, 6 }, n : all)
   exactly 1 (x : r13, y : r13) C(x+dx,y+dy,n);

# An easy Sudoku

C(1,1,2);
C(1,2,8);
C(1,3,7);
C(1,5,1);
C(1,9,9);
C(2,3,6);
C(2,4,2);
C(2,5,7);
C(2,7,3);
C(2,9,1);
C(3,3,3);
C(3,4,4);
C(3,5,9);
C(3,8,8);
C(3,9,2);
C(4,1,7);
C(4,4,5);
C(4,6,9);
C(4,8,6);
C(4,9,3);
C(5,1,6);
C(5,2,5);
C(5,6,4);
C(5,8,1);
C(5,9,8);
C(6,1,3);
C(6,2,4);
C(6,5,2);
C(6,6,1);
C(6,8,9);
C(7,3,4);
C(7,4,9);
C(7,6,7);
C(7,7,1);
C(7,8,2);
C(8,1,1);
C(8,2,6);
C(8,6,3);
C(8,7,9);
C(8,8,7);
C(9,2,7);
C(9,3,5);
C(9,4,1);
C(9,5,6);
C(9,7,8);
