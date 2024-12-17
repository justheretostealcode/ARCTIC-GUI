from itertools import product
import sympy

def generate_truth_table_from_expr(expr):
    # Parse the boolean expression
    expression = sympy.sympify(expr)

    # Find all symbols (variables) in the expression
    variables = sorted(expression.atoms(sympy.Symbol), key=lambda x: str(x))

    # Generate all combinations of truth values for the variables
    truth_combinations = list(product([False, True], repeat=len(variables)))

    # Evaluate the expression for each combination
    truth_table = []
    for combination in truth_combinations:
        evaluation = {str(var): val for var, val in zip(variables, combination)}
        result = expression.subs(evaluation)
        result_int = int(bool(result))
        truth_table.append([int(val) for val in combination] + [result_int])

    # Return a list of rows, where each row is a list of variable values and the result
    return truth_table