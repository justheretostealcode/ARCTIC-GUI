from itertools import product
import sympy
import re

def generate_truth_table_from_expr(expr):
    """
    Generates a truth table for a given Boolean expression. This function standardizes the expression by converting
    bitwise XOR operators to SymPy's 'Xor' function, parses it with SymPy, and then evaluates it across all possible
    combinations of truth values for the variables involved.

    Args:
        expr (str): A Boolean expression containing logical operators and variables.

    Returns:
        list[list[int]]: A truth table as a list of lists. The first row is the header with variable names and the
                          expression, followed by rows for each variable combination showing their truth values and
                          the evaluation result.
    """
    expr = re.sub(r'(\w+)\s*\^\s*(\w+)', r'Xor(\1, \2)', expr)
    # Parse the boolean expression
    expression = sympy.sympify(expr)
    # Find all symbols (variables) in the expression
    variables = sorted(expression.atoms(sympy.Symbol), key=lambda x: str(x))

    # Generate all combinations of truth values for the variables
    truth_combinations = list(product([False, True], repeat=len(variables)))

    #let the header be the titles
    header = [str(var) for var in variables] + [str(expr)]

    # Evaluate the expression for each combination
    truth_table = [header]  # Start the table with the header row
    for combination in truth_combinations:
        evaluation = {str(var): val for var, val in zip(variables, combination)}
        result = expression.subs(evaluation)
        result_int = int(bool(result))
        truth_table.append([int(val) for val in combination] + [result_int])

    # Return a list of rows, where each row is a list of variable values and the result
    return truth_table
