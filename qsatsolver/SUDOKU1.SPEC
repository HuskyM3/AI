
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

# Clues for the "The Hardest Sudoku" by A. Inkala.

C(1,1,8);
C(2,3,3);
C(2,4,6);
C(3,2,7);
C(3,5,9);
C(3,7,2);
C(4,2,5);
C(4,6,7);
C(5,5,4);
C(5,6,5);
C(5,7,7);
C(6,4,1);
C(6,8,3);
C(7,3,1);
C(7,8,6);
C(7,9,8);
C(8,3,8);
C(8,4,5);
C(8,8,1);
C(9,2,9);
C(9,7,4);
