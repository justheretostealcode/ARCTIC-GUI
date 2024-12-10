from itertools import product
import sympy

def generate_truth_table(inputs, operation):
    """Generates truth table for given boolean operation"""
    table = []
    for combination in product([0, 1], repeat=inputs):
        result = operation(*combination)
        table.append((*combination, result))
    return table

def and_operation(*inputs):
    return all(inputs)

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
        # Zip together the variables names with the values in this combination
        evaluation = {str(var): val for var, val in zip(variables, combination)}
        # Evaluate the expression with these values
        result = expression.subs(evaluation)
        # Convert sympy Boolean to standard Python int (0 or 1)
        result_int = int(bool(result))
        # Append the result along with the variable values
        truth_table.append([int(val) for val in combination] + [result_int])

    # Return a list of rows, where each row is a list of variable values and the result
    return truth_table