# DPLL: The Davis-Putnam-Logemann-Loveland (DPLL) algorithm
#
# The most basic way of testing satisfiability is equivalent to the
# truth-table method: exhaustively generate all 2^n valuations with
# a binary tree of depth n, with each leaf representing a valuation and
# each inner node representing case analysis on the two possible values
# of a propositional variable.
#
# The Davis-Putnam procedure improves on this by performing Unit Propagation
# after each case analysis: some variable must have a certain value, because
# otherwise one of the clauses would be false, and instead of doing a case
# analysis on that variable, we will assign the forced value to the variable.
#
# What Unit Propagation does is to identify clauses l1 V l2 V ... V Ln
# that does not contain any True literals under the current (partial) valuation,
# and that contains n-1 False literals. The remaining literal (which does not
# have a value) must be made True, because otherwise the clause and the whole
# clause set would be False. If the literal is positive, assign the variable in
# it True, and otherwise the literal is negative and assign the variable False.
#
# This, relatively simple, improvement makes it possible to solve orders of
# magnitudes harder satisfiability problems than what is possible with the
# truth-table method. Additional improvements in implementation technology (best
# possible data structures, minimization of cache misses etc.) as well as clever
# ways of choosing the variables for case analysis, and many other improvements,
# have lifted the scalability of SAT solving still dramatically further in
# the past 25 years.


def unit_propagation(valuation, clauses):
    """
    Performs Unit Propagation in the clause set

    Performs unit propagation, until no change takes place, by going through all
    clauses, and:
    * If at least one literal in a clause is True, then the clause is True. We
      can go to the next clause.
    * If the value of more than one variable in a clause is not determined yet,
      we cannot draw any inference; we should continue with next clause.
    * If a clause has no True literals and all literals except one
      are False, then the remaining literal must be made True.
    * Otherwise, if all literals of a clause are False, then the whole clause
      set would be false.

    Parameters
    ----------
    valuation: Dict[str, bool]
        Current partial valuation of the propositional variables. It maps the
        name of variables to their assigned truth-values.
    clauses: List[List[(str, bool)]]
        The CNF formula; Literals are described by a pair of (str, bool), which
        denotes the variable and its polarity, respectively.

    Returns
    -------
    Tuple[bool, Dict[str, bool]]
        If the formula is:
        unsatisfiable => it returns `(False, {})`; the first element is `False`,
                         and the second element is an empty dictionary
        otherwise     => it returns `(True, valuation)`; the first element is
                         `True`, and the second element, valuation, is a
                         dictionary that contains the truth-value of variables
                         after the unit propagation.
    """
    #                                 TASK 1
    # --------------------------------------------------------------------------
    # Implement unit propagation
    #
    # The first step to develop the DPLL algorithm is to implement the unit
    # propagation procedure. This procedure should find all unsatisfied clauses
    # with only one unassigned literal (these clauses are called unit clauses);
    # thus, the remaining literal has just one possible value to satisfy the
    # clause. For example, let assume the input is:
    #
    # valuation = {'a': True}
    # clauses = [[('a', False), ('b', True) ],
    #            [('b', False), ('c', False)],
    #            [('d': True),  ('e': False)]]
    #
    # It means the given formula is: (¬a ∨ b) ∧ (¬b ∨ ¬c) ∧ (d ∨ ¬e)
    # and, until now, we assume the value of `a` is `True`.
    #
    # The only unsatisfied clause that has just one unassigned literal is
    # `[('a', False), ('b', True)]`, so, to satisfy this clause, we need to
    # assign the value of `True` to `b`.
    # It is possible that applying unit propagation makes some other clauses
    # become new unit clauses. Thus, in the unit propagation procedure, we
    # should continue searching until there is no other unit clause in the
    # clause set.
    # In our example, after updating `valuation` to `{'a': True, 'b': True}`,
    # the clause `[('b', False), ('c', False)]` becomes a new unit clause; so,
    # we can update `valuation` to `{'a': True, 'b': True, 'c': False}`. After
    # this update, the clause set will have no other unit clause anymore.
    #
    # =====
    # Tips
    # =====
    # 1. Please remember that we have four kinds of clauses:
    #    1.1 at least one literal in a clause is True => the clause is True,
    #    1.2 the value of more than one variable in a clause is not determined
    #        yet => we cannot draw any inference,
    #    1.3 a clause has no True literals and all literals except one
    #        are False => the remaining literal must be True,
    #    1.4 all literals of a clause are False => the whole clause set
    #        would be false.
    # 2. You can use the most simple version of the unit propagation procedure;
    #    its pseudocode is provided in the course materials.


def dpll(valuation, clauses, variables):
    """
    The Davis-Putnam-Logemann-Loveland (DPLL) algorithm

    Determines if a Conjunctive Normal Form (CNF) formula is satisfiable or not;
    if the formula is satisfiable, it specifies the truth values of the
    variables.

    The CNF formula is given as a list of clauses; each clause is a list of
    literals and a literal is a propositional variable or its negation. Here,
    We represent a literal with a pair of (str, bool), where the first element
    represent the variable, and its second element represent the polarity of the
    literal.

    Parameters
    ----------
    valuation: Dict[str, bool]
        Current partial valuation of the propositional variables. It maps the
        name of variables to their assigned truth-values.
    clauses: List[List[(str, bool)]]
        The CNF formula; Literals are described by a pair of (str, bool), which
        denotes the variable and its polarity, respectively.
    variables: List[str]
        List of variables.

    Returns
    -------
    Tuple[bool, Dict[str, bool]]
        If the formula is:
            satisfiable   => it returns `(True, valuation)`; the first element
                             is `True`, and the second element, valuation, is a
                             dictionary that contains the truth-value of
                             variables that makes the formula satisfiable.
            
            unsatisfiable => it returns `(False, {})`; the first element is
                             `False`, and the second element is an empty
                             dictionary.
    """
    valuation = valuation.copy()  # Working on a copy instance of valuation
                                  # rather than modifying the input variable.
    (satisfiability, valuation) = unit_propagation(valuation, clauses)
    if not satisfiability:
        return (False, {})

    # Choose new variable for case analysis
    branching_variable = None
    for variable in variables:
        if variable not in valuation:
            branching_variable = variable
            break
    else:
        # No unassigned variables left; the formula is SAT
        return (True, valuation)

    #                                 TASK 2
    # --------------------------------------------------------------------------
    # If the satisfiability of the formula is not determined after the unit
    # propagation, we need to choose a variable and perform case analysis on it.
    # We have already chosen the variable: `branching_variable`. So, we need to
    # test whether assigning `True` to it makes the formula satisfiable or
    # assigning `False`. If none of those values makes the formula satisfiable,
    # then it is unsatisfiable, and this function should return `False`.
    #
    # =====
    # Tips
    # =====
    # Satisfiability testing can be done by updating the `valuation` dictionary
    # and recursively calling the `dpll` function.
