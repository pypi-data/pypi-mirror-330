import numpy as np
from advscipy.core import advanced_minimize

def test_advanced_minimize():
    # Define a simple quadratic function: f(x) = (x - 3)^2
    def objective_function(x):
        return (x - 3) ** 2

    # Perform optimization
    result = advanced_minimize(objective_function, x0=[0], method='BFGS', verbose=False)

    # Validate results
    assert result["success"], "Test failed: Optimization did not succeed"
    assert np.isclose(result["optimal_value"], 0), "Test failed: Incorrect optimal value"
    assert np.isclose(result["optimal_parameters"][0], 3), "Test failed: Incorrect optimal parameters"

    print("Test passed!")

# Add this block to make the file executable
if __name__ == "__main__":
    test_advanced_minimize()