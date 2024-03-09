import unittest
from unittest.mock import patch
import dpll
from logic import ATOM, AND, OR, NOT, IMPL, EQVI
from z3_wrapper import solve
from random import seed, randint, choice, random


seed(0)


class MyTestCase(unittest.TestCase):
    def check(self, formula):
        model = dict()
        my_result, model = dpll.dpll(model, formula.clauses(), formula.vars())
        z3_result, _, _ = solve(formula)
        sat_to_string = {True: 'Satisfiable', False: 'Unsatisfiable'}
        self.assertEqual(z3_result, my_result, "Expected value: {}, Actual value: {}".format(sat_to_string[z3_result],
                                                                                             sat_to_string[my_result]))
        if my_result:
            self.assertTrue(formula.is_satisfiable(model), "Valuation is not correct")
        return my_result

    def test_case_analysis(self):
        variable = 'test_variable'
        with patch('dpll.unit_propagation') as mock_unit_propagation:
            mock_unit_propagation.side_effect = [(True, {}), (False, {}), (False, {})]
            dpll.dpll({}, [[variable, False]], [variable])
            valuations = []
            for (_, args, kwarags) in mock_unit_propagation.mock_calls:
                valuations.append(args[0] if len(args) > 0 else kwarags["valuation"])
            self.assertIn({variable: True}, valuations, "\nError: Case analysis problem) Analyzing `True` case is not done correctly!")
            self.assertIn({variable: False}, valuations, "\nError: Case analysis problem) Analyzing `False` case is not done correctly!")

    def test_unit_propagation(self):
        clauses = [[('a', True), ('b', True)]]
        self.assertEqual((True, {'a': True}),
                         dpll.unit_propagation({'a': True}, clauses),
                         "\nError: Unit propagation problem) If at least one literal in a clause is True, then the "\
                         "clause is True")

        self.assertEqual((True, {}),
                         dpll.unit_propagation({}, clauses),
                         "\nError: Unit propagation problem) If the value of more than one variable in a cluase is "\
                         "not deteremined yet, we cannot draw any inference!")

        self.assertEqual((True, {'a': False, 'b': True}),
                         dpll.unit_propagation({'a': False}, clauses),
                         "\nError: Unit propagation problem) If a clause has no True literals and all literals except"\
                         " one are False, then the remaining literal must be made True.")

        self.assertEqual((False, {}),
                         dpll.unit_propagation({'a': False, 'b': False}, clauses),
                         "\nError: Unit propagation problem) If all literals of a clause are False, the whole clause"\
                         " set would be false.")

    def test_unit_propagation_2(self):
        number_of_variables = 600
        variables = [ATOM("a_{}".format(index)) for index in range(number_of_variables)]
        sub_formulas = list()
        for variable_1, variable_2 in zip(variables[:-1], variables[1:]):
            sub_formulas.append(EQVI(variable_1, variable_2))
        formula_1 = AND([*sub_formulas, variables[0]])
        formula_2 = AND([*sub_formulas, NOT(variables[0])])
        self.check(formula_1)
        self.check(formula_2)

    def test_simple_positive_literal(self):
        formula = ATOM("x")
        self.check(formula)

    def test_simple_negative_literal(self):
        formula = NOT(ATOM("x"))
        self.check(formula)

    def test_simple_unsat(self):
        formula = AND([ATOM("x"), NOT(ATOM("x"))])
        result = self.check(formula)
        self.assertFalse(result, "`x and not(x)` is UNSAT")

    def test_simple_two_variables_1(self):
        x = ATOM('x')
        y = ATOM('y')
        formula = AND([OR([x, y]), OR([NOT(x), NOT(y)])])
        self.check(formula)

    def test_simple_two_variables_2(self):
        x = ATOM('x')
        y = ATOM('y')
        formula = AND([IMPL(x, y), IMPL(y, x)])
        self.check(formula)

    def test_simple_two_variables_3(self):
        x = ATOM('x')
        y = ATOM('y')
        formula = AND([EQVI(x, y), NOT(x)])
        self.check(formula)

    def test_3SAT_1(self):
        x = ATOM('x')
        y = ATOM('y')
        z = ATOM('z')
        clauses = list()
        clauses.append(OR([x, NOT(y), z]))
        clauses.append(OR([NOT(x), y, NOT(z)]))
        clauses.append(OR([NOT(x), NOT(y)]))
        clauses.append(OR([x, y, z]))
        formula = AND(clauses)
        self.check(formula)

    def test_random_3SAT(self):
        variables = [ATOM(i) for i in "abcdefghijklmno"]
        number_of_formulas = 40
        number_of_clauses = 75
        for _ in range(number_of_formulas):
            clauses = list()
            while len(clauses) < number_of_clauses:
                clause = list()
                for _ in range(3):
                    literal = choice(variables)
                    if random() < 0.5:
                        literal = NOT(literal)
                    clause.append(literal)
                clauses.append(OR(clause))
            formula = AND(clauses)
            self.check(formula)

if __name__ == '__main__':
    unittest.main()
