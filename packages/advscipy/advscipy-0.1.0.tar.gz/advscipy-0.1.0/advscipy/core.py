from scipy.optimize import minimize

def advanced_minimize(func, x0, method='BFGS', verbose=True):
    """
    An advanced version of SciPy's minimize function.
    Adds additional metadata about the optimization process.

    Parameters:
        func (callable): The objective function to minimize.
        x0 (array-like): Initial guess.
        method (str): Optimization method (default is 'BFGS').
        verbose (bool): Whether to print metadata.

    Returns:
        dict: A dictionary containing the optimization result and metadata.
    """
    result = minimize(func, x0, method=method)
    
    if verbose:
        print(f"Optimization Method: {method}")
        print(f"Initial Guess: {x0}")
        print(f"Success: {result.success}")
        print(f"Optimal Value: {result.fun}")
        print(f"Optimal Parameters: {result.x}")
    
    return {
        "success": result.success,
        "optimal_value": result.fun,
        "optimal_parameters": result.x,
        "metadata": {
            "method": method,
            "initial_guess": x0,
            "message": result.message
        }
    }