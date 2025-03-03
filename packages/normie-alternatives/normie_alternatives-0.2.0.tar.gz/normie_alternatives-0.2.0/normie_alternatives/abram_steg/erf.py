import math

# Approximation 7.1.25
def erf_approx_7_1_25(x):
    p = 0.47047
    a1, a2, a3 = 0.3480242, -0.0958798, 0.7478556
    t = 1 / (1 + p * x)
    return 1 - (a1 * t + a2 * t**2 + a3 * t**3) * math.exp(-x**2)

# Approximation 7.1.26
def erf_approx_7_1_26(x):
    p = 0.3275911
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    t = 1 / (1 + p * x)
    return 1 - (a1 * t + a2 * t**2 + a3 * t**3 + a4 * t**4 + a5 * t**5) * math.exp(-x**2)

# Approximation 7.1.27
def erf_approx_7_1_27(x):
    a1, a2, a3, a4 = 0.278393, 0.230389, 0.000972, 0.078108
    return 1 - 1 / (1 + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4)**4

# Approximation 7.1.28
def erf_approx_7_1_28(x):
    a1, a2, a3, a4, a5 = 0.0705230784, 0.0422820123, 0.0092705272, 0.0001520143, 0.0002765672
    return 1 - 1 / (1 + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4 + a5 * x**5)**16

# Test the functions
if __name__ == "__main__":
    x_values = [0.5, 1.0, 1.5, 2.0]  # Example test inputs
    print("Approximations for erf(x):")
    for x in x_values:
        print(f"x = {x}")
        print(f"  7.1.25: {erf_approx_7_1_25(x)}")
        print(f"  7.1.26: {erf_approx_7_1_26(x)}")
        print(f"  7.1.27: {erf_approx_7_1_27(x)}")
        print(f"  7.1.28: {erf_approx_7_1_28(x)}")
      
